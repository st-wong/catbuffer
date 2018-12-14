# pylint: disable=invalid-name
# pylint: disable=wrong-import-position
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))  # noqa: E402
from _generated.py import catbuffer_generated_output as generated_python


class TestBufferToUintFunction(unittest.TestCase):

    def test_buffer_to_uint_converts_a_1_byte_unsigned_integer(self):
        int8 = 232
        array8 = bytearray(int8.to_bytes(1, byteorder='little', signed=False))
        unsigned_int = generated_python.buffer_to_uint(bytearray(array8))
        self.assertEqual(unsigned_int, int8)

        int8 = 0
        array8 = bytearray(int8.to_bytes(1, byteorder='little', signed=False))
        unsigned_int = generated_python.buffer_to_uint(bytearray(array8))
        self.assertEqual(unsigned_int, 0)

    def test_buffer_to_uint_converts_a_2_byte_unsigned_integer(self):
        int16 = 54345
        array16 = bytearray(int16.to_bytes(2, byteorder='little', signed=False))
        unsigned_int = generated_python.buffer_to_uint(bytearray(array16))
        self.assertEqual(unsigned_int, int16)

        int16 = 0
        array16 = bytearray(int16.to_bytes(2, byteorder='little', signed=False))
        unsigned_int = generated_python.buffer_to_uint(bytearray(array16))
        self.assertEqual(unsigned_int, 0)

    def test_buffer_to_uint_converts_a_4_byte_unsigned_integer(self):
        int32 = 765435
        array32 = bytearray(int32.to_bytes(4, byteorder='little', signed=False))
        unsigned_int = generated_python.buffer_to_uint(bytearray(array32))
        self.assertEqual(unsigned_int, int32)

        int32 = 0
        array32 = bytearray(int32.to_bytes(4, byteorder='little', signed=False))
        unsigned_int = generated_python.buffer_to_uint(bytearray(array32))
        self.assertEqual(unsigned_int, 0)


class TestUintToBufferFunction(unittest.TestCase):

    def test_uint_to_buffer_converts_an_integer_to_a_1_byte_buffer(self):
        int8 = 233
        buffer = generated_python.uint_to_buffer(int8, 1)
        self.assertEqual(len(buffer), 1)
        self.assertEqual(list(buffer), [233])

    def test_uint_to_buffer_converts_an_integer_to_a_2_byte_buffer(self):
        int16 = 54346
        buffer = generated_python.uint_to_buffer(int16, 2)
        self.assertEqual(len(buffer), 2)
        self.assertEqual(list(buffer), [74, 212])

    def test_uint_to_buffer_converts_an_integer_to_a_4_byte_buffer(self):
        int32 = 765436
        buffer = generated_python.uint_to_buffer(int32, 4)
        self.assertEqual(len(buffer), 4)
        self.assertEqual(list(buffer), [252, 173, 11, 0])


class TestConcatTypedArraysFunction(unittest.TestCase):

    def test_returns_an_empty_array_for_two_empty_array_inputs(self):
        array1 = bytearray([])
        array2 = bytearray([])
        result = generated_python.concat_typed_arrays(array1, array2)
        self.assertEqual(list(result), [])

    def test_returns_original_array_if_one_of_the_params_is_empty(self):
        array1 = bytearray([])
        array2 = bytearray([23, 54])

        result = generated_python.concat_typed_arrays(array1, array2)
        self.assertEqual(list(result), list(array2))

        result2 = generated_python.concat_typed_arrays(array2, array1)
        self.assertEqual(list(result2), list(array2))

    def test_returns_the_ordered_concatenation_of_both_params(self):
        array1 = bytearray([23, 54])
        array2 = bytearray([34, 2, 77, 91, 12])
        result = generated_python.concat_typed_arrays(array1, array2)
        self.assertEqual(list(result), list(array1) + list(array2))
        result2 = generated_python.concat_typed_arrays(array2, array1)
        self.assertEqual(list(result2), list(array2) + list(array1))


class TestFitByteArrayFunction(unittest.TestCase):

    def test_throws_if_data_provided_is_larger_than_the_requested_output_size(self):
        with self.assertRaises(IndexError) as context:

            generated_python.fit_byte_array(bytearray([34, 2, 77, 91, 12]), 2)
            self.assertEqual('Data size larger than allowed', str(context.exception))

    def test_returns_zero_initialized_arrays_for_a_null_array_input(self):
        self.assertEqual(list(generated_python.fit_byte_array(None, 0)), [])
        self.assertEqual(list(generated_python.fit_byte_array(None, 2)), [0, 0])

    def test_returns_the_same_array_if_the_parameter_size_is_the_same_as_the_parameter_array_length(self):
        array1 = bytearray([])
        array2 = bytearray([34, 2, 77, 91, 12])

        self.assertEqual(generated_python.fit_byte_array(array1, len(array1)), array1)
        self.assertEqual(generated_python.fit_byte_array(array2, len(array2)), array2)

    def test_returns_an_array_of_the_provided_size_initialized_with_trailing_0s_if_the_input_array_was_smaller(self):
        array1 = bytearray([4])
        array2 = bytearray([34, 2, 77, 91, 12])
        self.assertEqual(list(generated_python.fit_byte_array(array1, 2)), [0] + list(array1))
        self.assertEqual(list(generated_python.fit_byte_array(array2, 10)), [0, 0, 0, 0, 0] + list(array2))


class TestUint8ArrayConsumableBufferClass(unittest.TestCase):

    def test_constructs_with_buffer_offset_to_0_and_stored_array(self):
        array1 = bytearray([34, 2, 77, 91, 12])
        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(array1)
        self.assertEqual(consumable_buffer.offset, 0)
        self.assertEqual(consumable_buffer.binary, array1)

    def test_get_bytes_method_throws_if_requesting_more_bytes_than_available(self):
        array1 = bytearray([])
        array2 = bytearray([34, 2, 77, 91, 12])
        consumable_buffer_1 = generated_python.Uint8ArrayConsumableBuffer(array1)
        consumable_buffer_2 = generated_python.Uint8ArrayConsumableBuffer(array2)

        with self.assertRaises(IndexError):
            consumable_buffer_1.get_bytes(len(array1) + 1)

        with self.assertRaises(IndexError):
            consumable_buffer_2.get_bytes(len(array2) + 1)

        consumable_buffer_2.offset = 5
        with self.assertRaises(IndexError):
            consumable_buffer_2.get_bytes(1)

    def test_get_bytes_method_returns_requested_bytes_and_increases_offset(self):
        array1 = [34, 2, 77, 91, 12]
        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(bytearray(array1))
        first_batch = 2
        self.assertEqual(list(consumable_buffer.get_bytes(first_batch)), array1[:first_batch])
        self.assertEqual(consumable_buffer.offset, first_batch)
        second_batch = 3
        self.assertEqual(list(consumable_buffer.get_bytes(second_batch)),
                         array1[first_batch:(first_batch + second_batch)])
        self.assertEqual(consumable_buffer.offset, first_batch + second_batch)


class TestMosaicBufferClass(unittest.TestCase):

    def test_has_required_class_attributes(self):
        buffer = generated_python.MosaicBuffer()
        self.assertTrue(hasattr(buffer, 'mosaicId'))
        self.assertTrue(hasattr(buffer, 'amount'))

    def test_load_from_binary_initializes_from_binary_data(self):
        mosaic_id_buffer = bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92])
        mosaic_amount_buffer = bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44])

        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(
            bytearray(mosaic_id_buffer
                      + mosaic_amount_buffer))
        mosaic_buffer = generated_python.MosaicBuffer.load_from_binary(consumable_buffer)

        self.assertEqual(mosaic_buffer.mosaicId, mosaic_id_buffer)
        self.assertEqual(mosaic_buffer.amount, mosaic_amount_buffer)
        self.assertEqual(len(consumable_buffer.binary), consumable_buffer.offset)

    def test_serialize_outputs_a_valid_formatted_buffer(self):
        mosaic_id_buffer = bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92])
        mosaic_amount_buffer = bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44])

        buffer = generated_python.MosaicBuffer()
        buffer.mosaicId = mosaic_id_buffer
        buffer.amount = mosaic_amount_buffer

        self.assertEqual(buffer.serialize(), mosaic_id_buffer + mosaic_amount_buffer)


class TestSizePrefixedEntityBufferClass(unittest.TestCase):

    def test_has_required_class_attributes(self):
        buffer = generated_python.SizePrefixedEntityBuffer()
        self.assertTrue(hasattr(buffer, 'size'))

    def test_load_from_binary_initializes_from_binary_data(self):
        size_buffer = bytes([0xF2, 0x26, 0x6C, 0x06])
        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(size_buffer)
        buffer = generated_python.SizePrefixedEntityBuffer.load_from_binary(consumable_buffer)
        self.assertEqual(buffer.size, size_buffer)
        self.assertEqual(len(consumable_buffer.binary), consumable_buffer.offset)

    def test_serialize_outputs_a_valid_formatted_buffer(self):
        size_buffer = bytes([0xF2, 0x26, 0x6C, 0x06])

        buffer = generated_python.SizePrefixedEntityBuffer()
        buffer.size = size_buffer
        self.assertEqual(buffer.serialize(), size_buffer)


class VerifiableEntityBufferClass(unittest.TestCase):

    def test_has_required_class_attributes(self):
        buffer = generated_python.VerifiableEntityBuffer()
        self.assertTrue(hasattr(buffer, 'signature'))

    def test_load_from_binary_initializes_from_binary_data(self):
        signature_buffer = bytes([
            0xF5, 0x24, 0x8C, 0xB0, 0x05, 0x49, 0xC6, 0x15, 0xFC, 0x56, 0x13, 0x08, 0xE3, 0x4B, 0x60, 0xFF,
            0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC,
            0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2, 0x69, 0xD9, 0xE2, 0x56, 0x29, 0x2B, 0xF3, 0x52, 0xC0,
            0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D, 0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])

        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(signature_buffer)
        buffer = generated_python.VerifiableEntityBuffer.load_from_binary(consumable_buffer)

        self.assertEqual(buffer.signature, signature_buffer)
        self.assertEqual(len(consumable_buffer.binary), consumable_buffer.offset)

    def test_serialize_outputs_a_valid_formatted_buffer(self):
        signature_buffer = bytes([
            0xF5, 0x24, 0x8C, 0xB0, 0x05, 0x49, 0xC6, 0x15, 0xFC, 0x56, 0x13, 0x08, 0xE3, 0x4B, 0x60, 0xFF,
            0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC,
            0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2, 0x69, 0xD9, 0xE2, 0x56, 0x29, 0x2B, 0xF3, 0x52, 0xC0,
            0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D, 0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])

        buffer = generated_python.VerifiableEntityBuffer()
        buffer.signature = signature_buffer

        self.assertEqual(buffer.serialize(), signature_buffer)


class EntityBodyBufferClass(unittest.TestCase):

    def test_has_required_class_attributes(self):
        buffer = generated_python.EntityBodyBuffer()
        self.assertTrue(hasattr(buffer, 'signer'))
        self.assertTrue(hasattr(buffer, 'version'))
        self.assertTrue(hasattr(buffer, 'type'))

    def test_load_from_binary_initializes_from_binary_data(self):
        signer_buffer = bytes([0xF5, 0x24, 0x8C, 0xB0, 0x05, 0x49, 0xC6, 0x15, 0xFC, 0x56, 0x13, 0x08, 0xE3,
                               0x4B, 0x60, 0xFF, 0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C,
                               0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC])
        version_buffer = bytes([0xF2, 0x26])
        type_buffer = bytes([0xFF, 0x34])

        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(
            bytearray(signer_buffer
                      + version_buffer
                      + type_buffer))
        buffer = generated_python.EntityBodyBuffer.load_from_binary(consumable_buffer)

        self.assertEqual(buffer.signer, signer_buffer)
        self.assertEqual(buffer.version, version_buffer)
        self.assertEqual(buffer.type, type_buffer)
        self.assertEqual(len(consumable_buffer.binary), consumable_buffer.offset)

    def test_serialize_outputs_a_valid_formatted_buffer(self):
        signer_buffer = bytes([0xF5, 0x24, 0x8C, 0xB0, 0x05, 0x49, 0xC6, 0x15, 0xFC, 0x56, 0x13, 0x08, 0xE3,
                               0x4B, 0x60, 0xFF, 0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C,
                               0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC])
        version_buffer = bytes([0xF2, 0x26])
        type_buffer = bytes([0xFF, 0x34])

        buffer = generated_python.EntityBodyBuffer()
        buffer.signer = signer_buffer
        buffer.version = version_buffer
        buffer.type = type_buffer

        self.assertEqual(buffer.serialize(), signer_buffer + version_buffer + type_buffer)


class TransactionBufferClass(unittest.TestCase):

    def test_has_required_class_attributes(self):
        buffer = generated_python.TransactionBuffer()
        self.assertTrue(hasattr(buffer, 'size'))
        self.assertTrue(hasattr(buffer, 'signature'))
        self.assertTrue(hasattr(buffer, 'signer'))
        self.assertTrue(hasattr(buffer, 'version'))
        self.assertTrue(hasattr(buffer, 'type'))
        self.assertTrue(hasattr(buffer, 'fee'))
        self.assertTrue(hasattr(buffer, 'deadline'))

    def test_load_from_binary_initializes_from_binary_data(self):
        size_buffer = bytes([0xF2, 0x26, 0x6C, 0x06])
        signature_buffer = bytes([
            0xF5, 0x24, 0x8C, 0xB0, 0x05, 0x49, 0xC6, 0x15, 0xFC, 0x56, 0x13, 0x08, 0xE3, 0x4B, 0x60, 0xFF,
            0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC,
            0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2, 0x69, 0xD9, 0xE2, 0x56, 0x29, 0x2B, 0xF3, 0x52, 0xC0,
            0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D, 0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        signer_buffer = bytes([
            0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC,
            0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D, 0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        version_buffer = bytes([0xFF, 0x36])
        type_buffer = bytes([0x22, 0x66])
        fee_buffer = bytes([0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF2, 0x06])
        deadline_buffer = bytes([0xF2, 0x26, 0x0C, 0x4C, 0xF7, 0xF1, 0x6C, 0x06])

        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(
            bytearray(size_buffer
                      + signature_buffer
                      + signer_buffer
                      + version_buffer
                      + type_buffer
                      + fee_buffer
                      + deadline_buffer))

        buffer = generated_python.TransactionBuffer.load_from_binary(consumable_buffer)

        self.assertEqual(buffer.size, size_buffer)
        self.assertEqual(buffer.signature, signature_buffer)
        self.assertEqual(buffer.signer, signer_buffer)
        self.assertEqual(buffer.version, version_buffer)
        self.assertEqual(buffer.type, type_buffer)
        self.assertEqual(buffer.fee, fee_buffer)
        self.assertEqual(buffer.deadline, deadline_buffer)
        self.assertEqual(len(consumable_buffer.binary), consumable_buffer.offset)

    def test_serialize_outputs_a_valid_formatted_buffer(self):
        size_buffer = bytes([0xF2, 0x26, 0x6C, 0x06])
        signature_buffer = bytes([
            0xF5, 0x24, 0x8C, 0xB0, 0x05, 0x49, 0xC6, 0x15, 0xFC, 0x56, 0x13, 0x08, 0xE3, 0x4B, 0x60, 0xFF,
            0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC,
            0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2, 0x69, 0xD9, 0xE2, 0x56, 0x29, 0x2B, 0xF3, 0x52, 0xC0,
            0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D, 0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        signer_buffer = bytes([
            0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC,
            0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D, 0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        version_buffer = bytes([0xFF, 0x36])
        type_buffer = bytes([0x22, 0x66])
        fee_buffer = bytes([0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF2, 0x06])
        deadline_buffer = bytes([0xF2, 0x26, 0x0C, 0x4C, 0xF7, 0xF1, 0x6C, 0x06])

        buffer = generated_python.TransactionBuffer()
        buffer.size = size_buffer
        buffer.signature = signature_buffer
        buffer.signer = signer_buffer
        buffer.version = version_buffer
        buffer.type = type_buffer
        buffer.fee = fee_buffer
        buffer.deadline = deadline_buffer

        self.assertEqual(buffer.serialize(), size_buffer
                         + signature_buffer
                         + signer_buffer
                         + version_buffer
                         + type_buffer
                         + fee_buffer
                         + deadline_buffer)


class EmbeddedTransactionBufferClass(unittest.TestCase):

    def test_has_required_class_attributes(self):
        buffer = generated_python.EmbeddedTransactionBuffer()
        self.assertTrue(hasattr(buffer, 'size'))
        self.assertTrue(hasattr(buffer, 'signer'))
        self.assertTrue(hasattr(buffer, 'version'))
        self.assertTrue(hasattr(buffer, 'type'))

    def test_load_from_binary_initializes_from_binary_data(self):
        size_buffer = bytes([0xF2, 0x26, 0x6C, 0x06])
        signer_buffer = bytes([0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1,
                               0x5A, 0xAB, 0xDC, 0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D,
                               0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        version_buffer = bytes([0xFF, 0x36])
        type_buffer = bytes([0x22, 0x66])

        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(
            bytearray(size_buffer
                      + signer_buffer
                      + version_buffer
                      + type_buffer))
        buffer = generated_python.EmbeddedTransactionBuffer.load_from_binary(consumable_buffer)

        self.assertEqual(buffer.size, size_buffer)
        self.assertEqual(buffer.signer, signer_buffer)
        self.assertEqual(buffer.version, version_buffer)
        self.assertEqual(buffer.type, type_buffer)
        self.assertEqual(len(consumable_buffer.binary), consumable_buffer.offset)

    def test_serialize_outputs_a_valid_formatted_buffer(self):
        size_buffer = bytes([0xF2, 0x26, 0x6C, 0x06])
        signer_buffer = bytes([0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1,
                               0x5A, 0xAB, 0xDC, 0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D,
                               0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        version_buffer = bytes([0xFF, 0x36])
        type_buffer = bytes([0x22, 0x66])

        buffer = generated_python.EmbeddedTransactionBuffer()
        buffer.size = size_buffer
        buffer.signer = signer_buffer
        buffer.version = version_buffer
        buffer.type = type_buffer

        self.assertEqual(buffer.serialize(), size_buffer + signer_buffer + version_buffer + type_buffer)


class TransferTransactionBodyBufferClass(unittest.TestCase):

    def test_has_required_class_attributes(self):
        buffer = generated_python.TransferTransactionBodyBuffer()
        self.assertTrue(hasattr(buffer, 'recipient'))
        self.assertTrue(hasattr(buffer, 'message'))
        self.assertTrue(hasattr(buffer, 'mosaics'))

    def test_load_from_binary_initializes_from_binary_data(self):
        mosaic_buffer1 = generated_python.MosaicBuffer()
        mosaic_buffer1.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer1.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        mosaic_buffer2 = generated_python.MosaicBuffer()
        mosaic_buffer2.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer2.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        recipient_buffer = bytes([0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1,
                                  0xB1, 0x5A, 0xAB, 0xDC, 0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2, 0x69,
                                  0xD9])
        message_size_buffer = bytes([0x35, 0x00])
        mosaics_count_buffer = bytes([0x02])
        message_buffer = bytes([0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D, 0x71, 0xED, 0x25,
                                0x72, 0x3F, 0x48, 0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C,
                                0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC, 0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2,
                                0x69, 0xD9, 0xE2, 0x56, 0x29, 0x2B, 0xF3, 0x52, 0xC0, 0xAA, 0xBB, 0x55, 0xFF,
                                0x44])

        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(
            bytearray(recipient_buffer
                      + message_size_buffer
                      + mosaics_count_buffer
                      + message_buffer
                      + mosaic_buffer1.serialize()
                      + mosaic_buffer2.serialize()))

        buffer = generated_python.TransferTransactionBodyBuffer.load_from_binary(consumable_buffer)

        self.assertEqual(buffer.recipient, recipient_buffer)
        self.assertEqual(len(buffer.message), 53)
        self.assertEqual(buffer.message, message_buffer)
        self.assertEqual(len(buffer.mosaics), 2)
        self.assertEqual(buffer.mosaics[0].serialize(), mosaic_buffer1.serialize())
        self.assertEqual(buffer.mosaics[1].serialize(), mosaic_buffer2.serialize())
        self.assertEqual(len(consumable_buffer.binary), consumable_buffer.offset)

    def test_serialize_outputs_a_valid_formatted_buffer(self):

        mosaic_buffer1 = generated_python.MosaicBuffer()
        mosaic_buffer1.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer1.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        mosaic_buffer2 = generated_python.MosaicBuffer()
        mosaic_buffer2.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer2.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        recipient_buffer = bytes([0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1,
                                  0xB1, 0x5A, 0xAB, 0xDC, 0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2, 0x69,
                                  0xD9])
        message_size_buffer = bytes([0x35, 0x00])
        mosaics_count_buffer = bytes([0x02])
        message_buffer = bytes([0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D, 0x71, 0xED, 0x25,
                                0x72, 0x3F, 0x48, 0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C,
                                0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC, 0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2,
                                0x69, 0xD9, 0xE2, 0x56, 0x29, 0x2B, 0xF3, 0x52, 0xC0, 0xAA, 0xBB, 0x55, 0xFF,
                                0x44])

        buffer = generated_python.TransferTransactionBodyBuffer()
        buffer.recipient = recipient_buffer
        buffer.message = message_buffer
        buffer.mosaics = [mosaic_buffer1, mosaic_buffer2]

        self.assertEqual(buffer.serialize(), recipient_buffer
                         + message_size_buffer
                         + mosaics_count_buffer
                         + message_buffer
                         + mosaic_buffer1.serialize()
                         + mosaic_buffer2.serialize())


class TestTransferTransactionBufferClass(unittest.TestCase):

    def test_has_required_class_attributes(self):
        buffer = generated_python.TransferTransactionBuffer()
        self.assertTrue(hasattr(buffer, 'size'))
        self.assertTrue(hasattr(buffer, 'signature'))
        self.assertTrue(hasattr(buffer, 'signer'))
        self.assertTrue(hasattr(buffer, 'version'))
        self.assertTrue(hasattr(buffer, 'type'))
        self.assertTrue(hasattr(buffer, 'fee'))
        self.assertTrue(hasattr(buffer, 'deadline'))
        self.assertTrue(hasattr(buffer, 'recipient'))
        self.assertTrue(hasattr(buffer, 'message'))
        self.assertTrue(hasattr(buffer, 'mosaics'))

    def test_load_from_binary_initializes_from_binary_data(self):
        mosaic_buffer1 = generated_python.MosaicBuffer()
        mosaic_buffer1.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer1.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        mosaic_buffer2 = generated_python.MosaicBuffer()
        mosaic_buffer2.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer2.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        size_buffer = bytes([0xF2, 0x26, 0x6C, 0x06])
        signature_buffer = bytes([0xF5, 0x24, 0x8C, 0xB0, 0x05, 0x49, 0xC6, 0x15, 0xFC, 0x56, 0x13, 0x08, 0xE3,
                                  0x4B, 0x60, 0xFF, 0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C,
                                  0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC, 0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2,
                                  0x69, 0xD9, 0xE2, 0x56, 0x29, 0x2B, 0xF3, 0x52, 0xC0, 0xE8, 0x34, 0x62, 0x6D,
                                  0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D, 0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        signer_buffer = bytes([0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1,
                               0x5A, 0xAB, 0xDC, 0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D,
                               0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        version_buffer = bytes([0xFF, 0x36])
        type_buffer = bytes([0x22, 0x66])
        fee_buffer = bytes([0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF2, 0x06])
        deadline_buffer = bytes([0xF2, 0x26, 0x0C, 0x4C, 0xF7, 0xF1, 0x6C, 0x06])
        recipient_buffer = bytes([
            0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC,
            0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2, 0x69, 0xD9])
        message_size_buffer = bytes([0x12, 0x00])
        mosaics_count_buffer = bytes([0x02])
        message_buffer = bytes([0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05,
                                0xDC, 0x05, 0xDC, 0x05, 0xDC])

        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(
            bytearray(
                size_buffer
                + signature_buffer
                + signer_buffer
                + version_buffer
                + type_buffer
                + fee_buffer
                + deadline_buffer
                + recipient_buffer
                + message_size_buffer
                + mosaics_count_buffer
                + message_buffer
                + mosaic_buffer1.serialize()
                + mosaic_buffer2.serialize()))

        buffer = generated_python.TransferTransactionBuffer.load_from_binary(consumable_buffer)
        self.assertEqual(buffer.size, size_buffer)
        self.assertEqual(buffer.signature, signature_buffer)
        self.assertEqual(buffer.signer, signer_buffer)
        self.assertEqual(buffer.version, version_buffer)
        self.assertEqual(buffer.type, type_buffer)
        self.assertEqual(buffer.fee, fee_buffer)
        self.assertEqual(buffer.deadline, deadline_buffer)
        self.assertEqual(buffer.recipient, recipient_buffer)
        self.assertEqual(buffer.message, message_buffer)
        self.assertEqual(len(buffer.mosaics), 2)
        self.assertEqual(buffer.mosaics[0].serialize(), mosaic_buffer1.serialize())
        self.assertEqual(buffer.mosaics[1].serialize(), mosaic_buffer2.serialize())
        self.assertEqual(len(consumable_buffer.binary), consumable_buffer.offset)

    def test_serialize_outputs_a_valid_formatted_buffer(self):
        mosaic_buffer1 = generated_python.MosaicBuffer()
        mosaic_buffer1.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer1.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        mosaic_buffer2 = generated_python.MosaicBuffer()
        mosaic_buffer2.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer2.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        size_buffer = bytes([0xF2, 0x26, 0x6C, 0x06])
        signature_buffer = bytes([0xF5, 0x24, 0x8C, 0xB0, 0x05, 0x49, 0xC6, 0x15, 0xFC, 0x56, 0x13, 0x08, 0xE3,
                                  0x4B, 0x60, 0xFF, 0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C,
                                  0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC, 0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2,
                                  0x69, 0xD9, 0xE2, 0x56, 0x29, 0x2B, 0xF3, 0x52, 0xC0, 0xE8, 0x34, 0x62, 0x6D,
                                  0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D, 0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        signer_buffer = bytes([0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1,
                               0x5A, 0xAB, 0xDC, 0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D,
                               0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        version_buffer = bytes([0xFF, 0x36])
        type_buffer = bytes([0x22, 0x66])
        fee_buffer = bytes([0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF2, 0x06])
        deadline_buffer = bytes([0xF2, 0x26, 0x0C, 0x4C, 0xF7, 0xF1, 0x6C, 0x06])
        recipient_buffer = bytes([
            0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1, 0x5A, 0xAB, 0xDC,
            0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2, 0x69, 0xD9])
        message_size_buffer = bytes([0x12, 0x00])
        mosaics_count_buffer = bytes([0x02])
        message_buffer = bytes([0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05,
                                0xDC, 0x05, 0xDC, 0x05, 0xDC])

        buffer = generated_python.TransferTransactionBuffer()
        buffer.size = size_buffer
        buffer.signature = signature_buffer
        buffer.signer = signer_buffer
        buffer.version = version_buffer
        buffer.type = type_buffer
        buffer.fee = fee_buffer
        buffer.deadline = deadline_buffer
        buffer.recipient = recipient_buffer
        buffer.message = message_buffer
        buffer.mosaics = [mosaic_buffer1, mosaic_buffer2]

        self.assertEqual(buffer.serialize(),
                         size_buffer
                         + signature_buffer
                         + signer_buffer
                         + version_buffer
                         + type_buffer
                         + fee_buffer
                         + deadline_buffer
                         + recipient_buffer
                         + message_size_buffer
                         + mosaics_count_buffer
                         + message_buffer
                         + mosaic_buffer1.serialize()
                         + mosaic_buffer2.serialize())


class TestEmbeddedTransferTransactionBufferClass(unittest.TestCase):

    def test_has_required_class_attributes(self):
        buffer = generated_python.EmbeddedTransferTransactionBuffer()
        self.assertTrue(hasattr(buffer, 'size'))
        self.assertTrue(hasattr(buffer, 'signer'))
        self.assertTrue(hasattr(buffer, 'version'))
        self.assertTrue(hasattr(buffer, 'type'))
        self.assertTrue(hasattr(buffer, 'recipient'))
        self.assertTrue(hasattr(buffer, 'message'))
        self.assertTrue(hasattr(buffer, 'mosaics'))

    def test_load_from_binary_initializes_from_binary_data(self):
        mosaic_buffer1 = generated_python.MosaicBuffer()
        mosaic_buffer1.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer1.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        mosaic_buffer2 = generated_python.MosaicBuffer()
        mosaic_buffer2.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer2.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        size_buffer = bytes([0xF2, 0x26, 0x6C, 0x06])
        signer_buffer = bytes([0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1,
                               0x5A, 0xAB, 0xDC, 0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D,
                               0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        version_buffer = bytes([0xFF, 0x36])
        type_buffer = bytes([0x22, 0x66])
        recipient_buffer = bytes([0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1,
                                  0xB1, 0x5A, 0xAB, 0xDC, 0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2, 0x69,
                                  0xD9])
        message_size_buffer = bytes([0x12, 0x00])
        mosaics_count_buffer = bytes([0x02])
        message_buffer = bytes([0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC,
                                0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC])

        consumable_buffer = generated_python.Uint8ArrayConsumableBuffer(
            bytearray(
                size_buffer
                + signer_buffer
                + version_buffer
                + type_buffer
                + recipient_buffer
                + message_size_buffer
                + mosaics_count_buffer
                + message_buffer
                + mosaic_buffer1.serialize()
                + mosaic_buffer2.serialize()))

        buffer = generated_python.EmbeddedTransferTransactionBuffer.load_from_binary(consumable_buffer)
        self.assertEqual(buffer.size, size_buffer)
        self.assertEqual(buffer.signer, signer_buffer)
        self.assertEqual(buffer.version, version_buffer)
        self.assertEqual(buffer.type, type_buffer)
        self.assertEqual(buffer.recipient, recipient_buffer)
        self.assertEqual(buffer.message, message_buffer)
        self.assertEqual(len(buffer.mosaics), 2)
        self.assertEqual(buffer.mosaics[0].serialize(), mosaic_buffer1.serialize())
        self.assertEqual(buffer.mosaics[1].serialize(), mosaic_buffer2.serialize())
        self.assertEqual(len(consumable_buffer.binary), consumable_buffer.offset)

    def test_serialize_outputs_a_valid_formatted_buffer(self):
        mosaic_buffer1 = generated_python.MosaicBuffer()
        mosaic_buffer1.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer1.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        mosaic_buffer2 = generated_python.MosaicBuffer()
        mosaic_buffer2.mosaicId = bytearray(bytes([0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92]))
        mosaic_buffer2.amount = bytearray(bytes([0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44]))

        size_buffer = bytes([0xF2, 0x26, 0x6C, 0x06])
        signer_buffer = bytes([0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1, 0xB1,
                               0x5A, 0xAB, 0xDC, 0xE8, 0x34, 0x62, 0x6D, 0x00, 0x3C, 0xBF, 0xC2, 0x18, 0x0D,
                               0x71, 0xED, 0x25, 0x72, 0x3F, 0x48])
        version_buffer = bytes([0xFF, 0x36])
        type_buffer = bytes([0x22, 0x66])
        recipient_buffer = bytes([0x3E, 0xE9, 0xFA, 0x15, 0xA3, 0xB6, 0x05, 0xDC, 0x0C, 0x4C, 0xF7, 0xF1,
                                  0xB1, 0x5A, 0xAB, 0xDC, 0xCC, 0x2E, 0x09, 0x59, 0x38, 0x97, 0xF2, 0x69,
                                  0xD9])
        message_size_buffer = bytes([0x12, 0x00])
        mosaics_count_buffer = bytes([0x02])
        message_buffer = bytes([0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC,
                                0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC])

        buffer = generated_python.EmbeddedTransferTransactionBuffer()
        buffer.size = size_buffer
        buffer.signer = signer_buffer
        buffer.version = version_buffer
        buffer.type = type_buffer
        buffer.recipient = recipient_buffer
        buffer.message = message_buffer
        buffer.mosaics = [mosaic_buffer1, mosaic_buffer2]

        self.assertEqual(buffer.serialize(),
                         size_buffer
                         + signer_buffer
                         + version_buffer
                         + type_buffer
                         + recipient_buffer
                         + message_size_buffer
                         + mosaics_count_buffer
                         + message_buffer
                         + mosaic_buffer1.serialize()
                         + mosaic_buffer2.serialize())


if __name__ == '__main__':
    unittest.main()
