from generators.cpp_builder.BuilderGenerator import BuilderGenerator
from generators.python.PythonGenerator import PythonGenerator
AVAILABLE_GENERATORS = {
    'cpp-builder': BuilderGenerator,
    'py': PythonGenerator
}
