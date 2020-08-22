
from easy_json.errors import IncorrectFunctionParameterTypeError

def reverse_array(array: list):
    if type(array) != list:
        raise IncorrectFunctionParameterTypeError('array', 'list', type(array).__name__)

    return array[::-1]