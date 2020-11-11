# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

###############################
# * This file contains all internal utils
# * used by main package
###############################

import jsonpath_ng.ext as jsonpath
import os.path
from pathlib2 import Path
import json as JSON

from robust_json.errors import (
    JSONFileError,
    JSONPathError,
    IncorrectFunctionParameterTypeError,
)


class service:
    """
    Internal 'robust_json' package utils
    """

    def __init__(self):
        pass

    def check_file(self, path: str, file_formats: list[str]) -> bool:
        """
        Check if source file is ready for processing.

        This function will check if file exists, has a correct extension and
        contains valid JSON (JSON that can be parsed).

        Parameters: `path : str` specifies path to the file, that need to be checked.
        `file_formats : list of str` contains all supported file extensions. If source
        file extension is not supported, this method will raise an exception.

        This function returnsn a boolean: `True` - file is supported and is ready for processing,
        `False` - Something is wrong with the file. If file is empty, this method will add an empty object ({}) there.
        In this case, function will return `True`.

        This function will raise a `JSONFileError` if file extension is not supported.
        This function will raise a `FileNotFoundError` if specified file doesn't exist or cannot be accessed.
        """
        # Checking parameters type
        if type(path) != str:
            raise IncorrectFunctionParameterTypeError(
                "path", "str", type(path).__name__
            )

        if type(file_formats) != list:
            raise IncorrectFunctionParameterTypeError(
                "file_formats", "str", type(file_formats).__name__
            )

        # Checking type of each array element
        for i in enumerate(file_formats):
            if type(i[1]) != str:
                raise TypeError(
                    f"Array `file_formats` must contain only strings; got {type(i[1]).__name__} instead (Array index: [{i[0]}])."
                )

        # Verifying file extension and path
        if Path(path).suffix not in file_formats:
            raise JSONFileError(
                f'Supported file extensions are {", ".join(file_formats)}; got {Path(path).suffix} instead.'
            )

        # If file does not exist, raise an exception
        if not os.path.exists(path):
            raise FileNotFoundError(f"File `{path}` is not found.")

        file = open(path, "r")
        cont = file.read()
        file.close()

        if cont == None or cont == "":
            # If file is empty, write empty dictionary there and close it
            file = open(path, "w")
            file.write(JSON.dumps({}))
            file.close()

        # Read this file again
        file = open(path, "r")
        cont = file.read()
        file.close()

        try:
            # Try to deserialize JSON fron file
            JSON.loads(cont)
            return True
        except:
            return False

    def check_json_path(self, path: str, json: dict) -> bool:
        """
        Check if JSON path exists

        This function will check if given JSON path exists in specified JSON object.

        Parameters: `path : str` specifies property path that needs to be checked.
        `json : dict` specifies Python dictionary (JSON object), where this JSON path
        needs to be present.

        This function returns `True` if path is found and `False` if path cannot be
        accessed (does not exist).

        This function raises a `IncorrectFunctionParameterTypeError` exception if one or more of its parameters have incorrect types.
        This function raises a `JSONPathError` exception is JSON path is equal to an empty string.
        """
        # Checking types of functions' parameters
        if type(path) != str:
            raise IncorrectFunctionParameterTypeError(
                "path", "str", type(path).__name__
            )

        if path == "":
            raise JSONPathError("JSON path is empty.")

        if type(json) != dict:
            raise IncorrectFunctionParameterTypeError(
                "json", "dict", type(json).__name__
            )

        js_expr = jsonpath.parse(path)  # Parsing JSON using JSON path

        # If path is valid, return True. Otherwise return False
        if js_expr.find(json):
            return True
        else:
            return False

    def check_file_path(self, path: str) -> bool:
        """
        Check if file exists.

        Parameters: `path : str` specifies the path to the file.

        This function returns `True` if file exists,
        otherwise it returns `False`

        This function raises an `IncorrectFunctionParameterTypeError` if `path` parameter
        has an incorrect type.
        This function raises a `ValueError` exception if `path` parameter is
        equal to an empty string.
        """

        if type(path) != str:
            raise IncorrectFunctionParameterTypeError(
                "path", "str", type(path).__name__
            )

        if path == "":
            raise ValueError("Parameter `path` is an empty string.")

        if os.path.exists(path):
            return True
        else:
            return False
