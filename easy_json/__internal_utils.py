import jsonpath_ng.ext as jsonpath
import os.path
from pathlib2 import Path
import json as JSON

from easy_json.errors import JSONFileError, JSONObjectError, JSONPathError, JSONStrictModeError, IncorrectFunctionParameterTypeError

class service:
    """
    Internal 'easy_json' package utils
    """
    def __init__(self):
        pass

    def check_file(self, path: str, file_formats: list) -> bool:
        """
        Check if source file is ready for processing.

        This function will check if given file exists, has a correct extension and
        contains valid JSON.

        Parameters: `path : str` specifies path to source file, that need to be checked.
        `file_formats : list of str` is an array of all possible file extensions. If source
        file extension is not present here, an exception will be raised.

        This file will return a boolean: `True` - file is supported and is ready for processing,
        `False` - Something is wrong with the contents of file. If file is empty, an empty JSON
        object will be added. In this case, functtion will still return `True`.

        This function will raise a `JSONFileError` if file extension is not supported.
        This function will raise a `FileNotFoundError` if specified file is not found.
        If exception is raised, `None` will be returned.
        """
        # Checking parameter type
        if type(path) != str:
            raise IncorrectFunctionParameterTypeError('path', 'str', type(path).__name__)
        
        if type(file_formats) != list:
            raise IncorrectFunctionParameterTypeError('file_formats', 'str', type(file_formats).__name__)

        # Checking extensions array items type
        for i in enumerate(file_formats):
            if type(i[1]) != str:
                raise TypeError(f'Array `file_formats` must contain only strings; got {type(i[1]).__name__} instead (Array index: [{i[0]}]).')

        # Verifying file extension and path
        if Path(path).suffix not in file_formats:
            raise JSONFileError(f'Supported file extensions are {", ".join(file_formats)}; got {Path(path).suffix} instead.')

        if not os.path.exists(path):
            raise FileNotFoundError(f'File `{path}` is not found.')


        file = open(path, 'r')
        cont = file.read()
        file.close()

        if cont == None or cont == '':
            file = open(path, 'w')
            file.write(JSON.dumps({}))
            file.close()
        
        file = open(path, 'r')
        cont = file.read()
        file.close()

        try:
            js_parse = JSON.loads(cont)
            return True
        except:
            return False

    def check_json_path(self, path: str, json: dict) -> bool:
        """
        Check if path exists in JSON
        
        This function will check if given path exists in given JSON object.

        Parameters: `path : str` specifies property path, that needs to be checked.
        `json : dict` specifies Python dictionary (JSON object), where given path
        needs to be present.

        This function will return `True` if path is found and `False` if path could not be
        located.

        This function will raise a `TypeError` exception if either of parameters has an incorrect type.
        This function will raise a `JSONPathError` exception is given path is empty.
        """

        if type(path) != str:
            raise IncorrectFunctionParameterTypeError('path', 'str', type(path).__name__)

        if path == '':
            raise JSONPathError('Given path is empty.')

        if type(json) != dict:
            raise IncorrectFunctionParameterTypeError('json', 'dict', type(json).__name__)


        js_expr = jsonpath.parse(path)

        if js_expr.find(json):
            return True
        else:
            return False
    
    def check_file_path(self, path: str) -> bool:
        """
        Check if specified file path exists.

        Parameters: `path : str` specifies the file path that needs to
        be checked.

        This function will return `True` if this file path exists on the hard drive,
        otherwise it will return `False`

        This function will raise a `IncorrectFunctionParameterTypeError` if `path` parameter
        has an incorrect type.
        This function will raise a `ValueError` exception if `path` parameter is
        equal to an empty string.
        """

        if type(path) != str:
            raise IncorrectFunctionParameterTypeError('path', 'str', type(path).__name__)

        if path == '':
            raise ValueError('Parameter `path` is an empty string.')

        if os.path.exists(path):
            return True
        else:
            return False
        