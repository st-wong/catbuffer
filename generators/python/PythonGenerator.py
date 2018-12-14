import copy
from enum import Enum
from generators.Descriptor import Descriptor


class TypeDescriptorType(Enum):
    Byte = 'byte'
    Struct = 'struct'
    Enum = 'enum'


class TypeDescriptorDisposition(Enum):
    Inline = 'inline'
    Const = 'const'


def indent(code, n_indents=1):
    return ' ' * 4 * n_indents + code


def _get_attribute_name_if_sizeof(attribute_name, attributes):
    for attribute in attributes:
        if 'size' in attribute and attribute['size'] == attribute_name:
            return attribute['name']
    return None


class PythonMethodGenerator:
    def __init__(self, name, params, static=False, is_class=False):
        self.name = name
        copied_params = copy.deepcopy(params)
        if is_class:
            copied_params.insert(0, 'self')
        if static:
            self.method_output = ['@staticmethod', 'def {}({}):'.format(self.name, ', '.join(copied_params))]
        else:
            self.method_output = ['def {}({}):'.format(self.name, ', '.join(copied_params))]

    def add_instructions(self, instructions):
        for instruction in instructions:
            self.method_output.append(indent(instruction))

    def get_method(self):
        return self.method_output


class PythonClassGenerator:
    @staticmethod
    def get_generated_class_name(name):
        return '{}Buffer'.format(name)

    @staticmethod
    def get_generated_getter_name(attribute):
        return 'get_{}'.format(attribute.lower())

    @staticmethod
    def get_generated_setter_name(attribute):
        return 'set_{}'.format(attribute.lower())

    def __init__(self, name):
        self.class_name = PythonClassGenerator.get_generated_class_name(name)
        self.class_output = ['class {}:'.format(self.class_name)]

    def add_constructor(self, initial_values, params):
        params.insert(0, 'self')
        new_constructor = [indent('def __init__({}):'.format(', '.join(params)))]
        for attribute, value in initial_values.items():
            new_constructor += [indent('self.{} = {}'.format(attribute, value), 2)]
        self.class_output += [''] + new_constructor

    def _add_getter(self, attribute):
        new_getter = PythonMethodGenerator(
            PythonClassGenerator.get_generated_getter_name(attribute), [], is_class=True)
        new_getter.add_instructions(['return self.{0}'.format(attribute)])
        self.add_method(new_getter)

    def _add_setter(self, attribute):
        new_setter = PythonMethodGenerator(
            PythonClassGenerator.get_generated_setter_name(attribute),
            [attribute],
            is_class=True)
        new_setter.add_instructions(['self.{0} = {0}'.format(attribute)])
        self.add_method(new_setter)

    def add_getter_setter(self, attribute):
        self._add_getter(attribute)
        self._add_setter(attribute)

    def add_method(self, method):
        self.class_output += [''] + [indent(line) for line in method.get_method()]

    def get_class(self):
        return self.class_output


class PythonGenerator:

    def __init__(self, schema):
        self.schema = schema
        self.generated = None
        self.new_class = None
        self.load_from_binary_method = None
        self.serialize_method = None
        self.consumer_class = None
        self.exports = None

    def __iter__(self):
        self.generated = False
        return self

    def __next__(self):
        if self.generated:
            raise StopIteration

        code = self.generate()
        self.generated = True
        return Descriptor('catbuffer_generated_output.py', code)

    def _get_type_size(self, attribute):
        if attribute['type'] != TypeDescriptorType.Byte.value and attribute['type'] != TypeDescriptorType.Enum.value:
            return self.schema[attribute['type']]['size']
        return attribute['size']

    def _recurse_inlines(self, generate_attribute_method, attributes, class_attributes):
        for attribute in attributes:
            if 'disposition' in attribute:
                if attribute['disposition'] == TypeDescriptorDisposition.Inline.value:
                    self._recurse_inlines(generate_attribute_method, self.schema[attribute['type']]['layout'], class_attributes)
                elif attribute['disposition'] == TypeDescriptorDisposition.Const.value:
                    pass
            else:
                sizeof_attribute_name = _get_attribute_name_if_sizeof(attribute['name'], attributes)
                if generate_attribute_method:
                    generate_attribute_method(attribute, sizeof_attribute_name)
                if sizeof_attribute_name is None:
                    class_attributes.append(attribute)
        return class_attributes

    def _generate_load_from_binary_attributes(self, attribute, sizeof_attribute_name):
        if sizeof_attribute_name is not None:
            self.load_from_binary_method.add_instructions([
                '{0} = buffer_to_uint(consumable_buffer.get_bytes({1}))'.format(
                    attribute['name'], attribute['size'])
            ])
        else:
            if attribute['type'] == TypeDescriptorType.Byte.value:
                self.load_from_binary_method.add_instructions([
                    '{0} = consumable_buffer.get_bytes({1})'.format(
                        attribute['name'], self._get_type_size(attribute))
                ])
                self.load_from_binary_method.add_instructions(['object.{0} = {0}'.format(attribute['name'])])

            # Struct object
            else:
                # Required to check if typedef or struct definition
                # (depends if type of typedescriptor is Struct or Byte)
                attribute_typedescriptor = self.schema[attribute['type']]

                # Array of objects
                if 'size' in attribute:
                    # No need to check if attribute['size'] is int (fixed) or a variable reference,
                    # because attribute['size'] will either be a number or a previously code generated reference
                    self.load_from_binary_method.add_instructions(['object.{} = []'.format(attribute['name'])])
                    self.load_from_binary_method.add_instructions(['for _ in range(0, {}):'.format(attribute['size'])])
                    if attribute_typedescriptor['type'] == TypeDescriptorType.Struct.value:
                        self.load_from_binary_method.add_instructions([
                            indent('new_{0} = {1}.load_from_binary(consumable_buffer)'.format(
                                attribute['name'], PythonClassGenerator.get_generated_class_name(attribute['type'])))
                        ])
                    elif attribute_typedescriptor['type'] == TypeDescriptorType.Enum.value:
                        self.load_from_binary_method.add_instructions([
                            indent('new_{0} = consumable_buffer.get_bytes({1})'.format(
                                attribute['name'], self._get_type_size(attribute_typedescriptor)))
                        ])
                    self.load_from_binary_method.add_instructions([
                        indent('object.{0}.append(new_{0})'.format(attribute['name']))
                    ])

                # Single object
                else:
                    if attribute_typedescriptor['type'] == TypeDescriptorType.Struct.value:
                        self.load_from_binary_method.add_instructions([
                            '{0} = {1}.load_from_binary(consumable_buffer)'.format(
                                attribute['name'], PythonClassGenerator.get_generated_class_name(attribute['type']))
                        ])
                    elif attribute_typedescriptor['type'] == TypeDescriptorType.Byte.value \
                            or attribute_typedescriptor['type'] == TypeDescriptorType.Enum.value:
                        self.load_from_binary_method.add_instructions([
                            '{0} = consumable_buffer.get_bytes({1})'.format(
                                attribute['name'], self._get_type_size(attribute_typedescriptor))
                        ])
                    self.load_from_binary_method.add_instructions(['object.{0} = {0}'.format(attribute['name'])])

    def _generate_load_from_binary_method(self, attributes):
        self.load_from_binary_method = PythonMethodGenerator('load_from_binary', ['consumable_buffer'], True)
        self.load_from_binary_method.add_instructions(['object = {}()'.format(self.new_class.class_name)])
        self._recurse_inlines(self._generate_load_from_binary_attributes, attributes, [])
        self.load_from_binary_method.add_instructions(['return object'])
        self.new_class.add_method(self.load_from_binary_method)

    def _generate_serialize_attributes(self, attribute, sizeof_attribute_name):
        if sizeof_attribute_name is not None:
            self.serialize_method.add_instructions([
                'new_array = concat_typed_arrays(new_array, uint_to_buffer(len(self.{0}), {1}))'.format(
                    sizeof_attribute_name, attribute['size'])
            ])
        else:
            if attribute['type'] == TypeDescriptorType.Byte.value:
                if isinstance(attribute['size'], int):
                    self.serialize_method.add_instructions([
                        'fit_array_{0} = fit_byte_array(self.{0}, {1})'.format(
                            attribute['name'], self._get_type_size(attribute))
                    ])
                    self.serialize_method.add_instructions([
                        'new_array = concat_typed_arrays(new_array, fit_array_{})'.format(attribute['name'])
                    ])
                else:
                    self.serialize_method.add_instructions([
                        'new_array = concat_typed_arrays(new_array, self.{})'.format(attribute['name'])
                    ])

            # Struct object
            else:
                # Required to check if typedef or struct definition
                # (depends if type of typedescriptor is Struct or Byte)
                attribute_typedescriptor = self.schema[attribute['type']]

                # Array of objects
                if 'size' in attribute:
                    # No need to check if attribute['size'] is int (fixed) or a variable reference,
                    #  because we iterate with a for util in both cases
                    self.serialize_method.add_instructions(['for attribute in self.{}:'.format(attribute['name'])])
                    if attribute_typedescriptor['type'] == TypeDescriptorType.Struct.value:
                        self.serialize_method.add_instructions([
                            indent('new_array = concat_typed_arrays(new_array, attribute.serialize())')
                        ])
                    elif attribute_typedescriptor['type'] == TypeDescriptorType.Enum.value:
                        self.serialize_method.add_instructions([
                            indent('fit_array_{0} = fit_byte_array(self.{0}, {1})'.format(
                                attribute['name'], self._get_type_size(attribute_typedescriptor)))
                        ])
                        self.serialize_method.add_instructions([
                            indent('new_array = concat_typed_arrays(new_array, fit_array_{})'.format(attribute['name']))
                        ])

                # Single object
                else:
                    if attribute_typedescriptor['type'] == TypeDescriptorType.Struct.value:
                        self.serialize_method.add_instructions([
                            'new_array = concat_typed_arrays(new_array, self.{}.serialize())'.format(
                                attribute['name'])
                        ])
                    elif attribute_typedescriptor['type'] == TypeDescriptorType.Byte.value \
                            or attribute_typedescriptor['type'] == TypeDescriptorType.Enum.value:
                        self.serialize_method.add_instructions([
                            'fit_array_{0} = fit_byte_array(self.{0}, {1})'.format(
                                attribute['name'], self._get_type_size(attribute_typedescriptor))
                        ])
                        self.serialize_method.add_instructions([
                            'new_array = concat_typed_arrays(new_array, fit_array_{})'.format(attribute['name'])
                        ])

    def _generate_serialize_method(self, attributes):
        self.serialize_method = PythonMethodGenerator('serialize', [], is_class=True)
        self.serialize_method.add_instructions(['new_array = bytearray()'])
        self._recurse_inlines(self._generate_serialize_attributes, attributes, [])
        self.serialize_method.add_instructions(['return new_array'])
        self.new_class.add_method(self.serialize_method)

    def _generate_constructor(self, attributes):
        class_attributes = self._recurse_inlines(None, attributes, [])
        initial_values = {attribute['name']: None for attribute in class_attributes}
        self.new_class.add_constructor(initial_values, [])

    def _generate_attributes(self, attribute, sizeof_attribute_name):
        if sizeof_attribute_name is None:
            self.new_class.add_getter_setter(attribute['name'])

    def _generate_schema(self, type_descriptor, schema):
        self.new_class = PythonClassGenerator(type_descriptor)
        self._generate_constructor(schema['layout'])
        self._recurse_inlines(self._generate_attributes, schema['layout'], [])
        self._generate_load_from_binary_method(schema['layout'])
        self._generate_serialize_method(schema['layout'])
        return self.new_class.get_class()

    @staticmethod
    def _generate_concat_typed_arrays():
        method = PythonMethodGenerator('concat_typed_arrays', ['array1', 'array2'])
        method.add_instructions([
            'return array1 + array2',
        ])
        return method.get_method()

    @staticmethod
    def _generate_buffer_to_uint():
        method = PythonMethodGenerator('buffer_to_uint', ['buffer'])
        method.add_instructions([
            'return int.from_bytes(buffer, byteorder=\'little\', signed=False)'
        ])
        return method.get_method()

    @staticmethod
    def _generate_uint_to_buffer():
        method = PythonMethodGenerator('uint_to_buffer', ['uint', 'buffer_size'])
        method.add_instructions([
            'bytes = (uint).to_bytes(buffer_size, byteorder=\'little\', signed=False)',
            'return bytearray(bytes)'
        ])
        return method.get_method()

    @staticmethod
    def _generate_fit_byte_array():
        method = PythonMethodGenerator('fit_byte_array', ['array', 'size'])
        method.add_instructions([
            'if not array:',
            indent('new_array = bytearray([0] * size)'),
            indent('return new_array'),
            'if len(array) > size:',
            indent('raise IndexError(\'Data size larger than allowed\')'),
            'elif len(array) < size:',
            indent('new_array = bytearray(([0] * (size - len(array))))'),
            indent('new_array = new_array + array'),
            indent('return new_array'),
            'return array'
        ])
        return method.get_method()

    def _generate_uint8_array_consumer(self):
        self.consumer_class = PythonClassGenerator('Uint8ArrayConsumable')
        self.consumer_class.add_constructor({'offset': 0, 'binary': 'binary'}, ['binary'])

        get_bytes_method = PythonMethodGenerator('get_bytes', ['count'], is_class=True)
        get_bytes_method.add_instructions([
            'if (count + self.offset) > len(self.binary):',
            indent('raise IndexError'),
            'bytes = self.binary[self.offset:self.offset + count]',
            'self.offset += count',
            'return bytes',
        ])
        self.consumer_class.add_method(get_bytes_method)

        return self.consumer_class.get_class()

    def generate(self):

        new_file = ['# File automatically generated by Catbuffer']

        new_file += ['', ''] + self._generate_concat_typed_arrays()
        new_file += ['', ''] + self._generate_fit_byte_array()
        new_file += ['', ''] + self._generate_uint8_array_consumer()
        new_file += ['', ''] + self._generate_buffer_to_uint()
        new_file += ['', ''] + self._generate_uint_to_buffer()

        for type_descriptor, value in self.schema.items():
            if value['type'] == TypeDescriptorType.Byte.value:
                # Typeless environment, values will be directly assigned
                pass
            elif value['type'] == TypeDescriptorType.Enum.value:
                # Using the constant directly, so enum definition unneeded
                pass
            elif value['type'] == TypeDescriptorType.Struct.value:
                new_file += ['', ''] + self._generate_schema(type_descriptor, value)

        return new_file
