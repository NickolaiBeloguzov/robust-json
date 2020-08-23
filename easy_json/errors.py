###################################
# * This file contains all custom exceptions
# * used by main package
###################################

class JSONObjectError(Exception):
    """Incorrect JSON object"""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'JSONObjectError: {self.message}'
        else:
            return 'JSONObjectError: No message provided'


class JSONPathError(Exception):
    """Incorrect JSON path"""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'JSONPathError: {self.message}'
        else:
            return 'JSONPathError: No message provided'


class JSONStrictModeError(Exception):
    """Error during strict mode"""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'JSONStrictModeError: {self.message}'
        else:
            return 'JSONStrictModeError: No message provided'


class JSONFileError(Exception):
    """Error with JSON file"""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'JSONFileError: {self.message}'
        else:
            return 'JSONFileError: No message provided'
    
class IncorrectFunctionParameterTypeError(Exception):
    """Incorrect function parameter type"""

    def __init__(self, variable_name: str, correct_type: str, curr_type: str):
        self.var_name = variable_name
        self.correct_type = correct_type
        self.current_type = curr_type

    def __str__(self):
        if self.var_name and self.current_type and self.correct_type:
            return f'Parameter `{self.var_name}` must have a `{self.correct_type}` type; got `{self.current_type}` instead.'
