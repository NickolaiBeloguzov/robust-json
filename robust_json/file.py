# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

################################
# * This file contains `JsonFileParser` class
# * and all of its methods and properties
################################


# JSON modules import
import json as JSON
import os
import jsonpath_ng.ext as jsonpath

# Misc import
from typing import Union, Any

# Other modules import
from robust_json.errors import (
    JSONFileError,
    JSONPathError,
    JSONStrictModeError,
    IncorrectFunctionParameterTypeError,
)
from robust_json.__internal_utils import service


class JsonFileParser:
    """
    This class provides functionality for working with JSON files.

    For more information please visit:
    https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#file-module-overview
    """

    def __init__(self, path, autosave: bool = False, **kwargs):
        self.__path = path
        self.__file_formats = [".json", ".txt"]
        self.__service = service()
        self.__is_autosaving = autosave
        self.__kwargs = kwargs

        if self.__service.check_file(self.__path, self.__file_formats):
            self.active_json = self.get_json_from_file()
            self.__backup = self.get_json_from_file()
        else:
            raise JSONFileError(f"Error parsing file `{self.path}`. Its content cannot be parsed.")

    @property
    def file_formats(self):
        """
        All supported file extensions.
        """
        return self.__file_formats

    @property
    def path(self):
        """
        Path to file with JSON.
        """
        return self.__path

    @property
    def backup(self):
        """
        The initial JSON object (without any recent changes).
        """
        return self.__backup

    def get_json_from_file(self) -> dict:
        """
        Extract all JSON from source file.

        This function reads the source file and returns JSON object from it
        as a Python dictionary.

        This function is automatically called when class instance is
        created.

        For more information please visit: https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#file-module-methods-and-properties
        """
        file = open(self.__path, "r")
        cont = file.read()
        file.close()

        self.active_json = JSON.loads(
            cont
        )  # * May deprecate this line due to the fact that in __init__ its return value is assigned to self.active_json (double assignment)
        return JSON.loads(cont)

    def get_key_value(self, json_path: str) -> Any:
        """
        Retrieve specific key:value pair from JSON.

        This function fetches key:value pair from JSON object according to provided path
        and returns only the value.

        Parameters: `json_path : str` specifies JSON property path (e.g. field1.field2.[...].fieldn).

        This function raises an `IncorrectFunctionParameterTypeError` if
        `json_path` parameter has an incorrect type.
        This function raises a `JSONPathError` if JSON path is not valid.
        This function raises any additional exceptions if occurred.

        Examples:

        Retrieving key:value pair from a simple object:

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('test_file.json')
        # Object from `test_file.json` >> { "test_key": "test_value", "test_arr": [1, 2, 3] }
        >>> val = op.get_key_value('test_key')
        >>> val
        # val = 'test_value'

        Retrieving element from an array

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('test_file.json')
        # Object from `test_file.json` >> { "test_key": "test_value", "test_arr": [1, 2, 3] }
        >>> arr_val = op.get_key_value('test_arr.[1]') # Path is equal to 'test_arr[1]'
        >>> arr_val
        # arr_val = 2

        For more information about this method please visit:
        https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#file-module-methods-and-properties
        """

        # Checkint parameter type
        if type(json_path) != str:
            raise IncorrectFunctionParameterTypeError("json_path", "str", type(json_path).__name__)

        json_content = self.active_json

        # Verifying JSON path
        if not self.__service.check_json_path(json_path, json_content):
            raise JSONPathError(f"Path `{json_path}` is not valid.")

        js_expr = jsonpath.parse(json_path)  # Parsing JSON

        res = [
            item.value for item in js_expr.find(json_content)
        ]  # Filling an array with all matches

        if len(res) == 1:
            return res[0]
        return res

    def append(self, json_path: str, append_value: Any, append_at_end: bool = False) -> dict:
        """
        Append new value to an existing JSON object.

        This function takes value and adds it to the JSON object.

        Parameters: `json_path : str` specifies JSON property path where the given
        value needs to be added. If there is a need to append a value
        to the root of the object, this parameter needs to be equal to `$`. `append_value : Any`
        specifies the value that will be appended to the object. `append_at_end : bool`
        controls the behaviour of this function regarding JSON arrays of objects (structures like this: [{}, {}, {}, ...])
        and general arrays (structures like this: [a, b, c, ...]). It has no influence on other structures. If set to False,
        function will try to add value to each object of an array. If set to True, function will try to append
        value at the end of an array. (see examples below).


        This function returns a Python dictionary with updated content.

        This function raises a `FunctionParameterTypeError` exception if one or more of its parameters have an incorrect type.
        This function raises a `ValueError` exception if `append_value` parameter is empty (i.e
        is equal to an empty string, an empty array or empty dictionary).
        This function raises a `JSONPathError` exception if JSON path is not valid.
        This function raises any additional exceptions if occurred.

        Examples:

        Adding a simple key:value pair to the root object:

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('test.json')
        # object from `test.json` >> { "key": "value" }
        >>> op.append('$', { 'test': 'test' })
        >>> op.active_json
        # Output: { "key": "value", "test": "test" }

        Adding a new JSON object to an array of objects:

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('users.json')
        # object from `users.json` >> { "users": [ {"id": 1, "name": "Ken"}, { "id": 2, "name": "Liza" } ] }
        >>> op.append('users', { 'id': 3, 'name': 'Nick' }, True)
        >>> op.active_json
        # Output: { "users": [ {"id": 1, "name": "Ken"}, { "id": 2, "name": "Liza" }, { "id": 3, "name": "Nick" } ] }

        Adding a key:value pair to each object of array

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('users.json')
        # object from `users.json` >> { "users": [ {"id": 1, "name": "Ken"}, { "id": 2, "name": "Liza" } ] }
        >>> op.append('users', { 'role': 'guest' })
        >>> op.active_json
        # Output: { "users": [ { "id": 1, "name": "Ken", "role": "guest" }, { "id": 2, "name": "Liza", "role": "guest" } ] }

        Adding a new element to an array of strings:

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('array.json')
        # object from `array.json` >> { "colors": [ "red", "blue" ] }
        >>> op.append('colors', 'green')
        >>> op.active_json
        # Output: { "colors": [ "red", "blue" ] }
        # Nothing has appended. It's because this function tried to append given
        # value to each string in array and failed
        # To fix this, we need to set `append_at_end` parameter to `True`
        >>> op.append('colors', 'green', True)
        >>> op.active_json
        # Output: { "colors": [ "red", "blue", "green" ] }


        For more information about this method please visit:
        https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#file-module-methods-and-properties
        """

        if type(json_path) != str:
            raise IncorrectFunctionParameterTypeError("json_path", "str", type(json_path).__name__)

        if type(append_at_end) != bool:
            raise IncorrectFunctionParameterTypeError(
                "append_at_end", "bool", type(append_at_end).__name__
            )

        empty_obj = [[], {}, ""]

        if append_value in empty_obj:
            raise ValueError(f"Parameter `append_value` is empty.")

        json_content = self.active_json

        if not self.__service.check_json_path(json_path, json_content):
            raise JSONPathError(f"Path `{json_path}` is not valid.")

        js_expr = jsonpath.parse(json_path)

        for item in js_expr.find(json_content):
            temp = item.value

            if type(temp) == list:

                if append_at_end == True:
                    temp.append(append_value)
                    self.active_json = json_content
                    return json_content
                else:
                    for i in iter(temp):
                        if type(i) == dict:
                            if type(append_value) == dict:
                                i.update(append_value)
                            else:
                                raise TypeError(
                                    f"To append to a JSON object, parameter `append_value` must be a dictionary; got `{type(append_value).__name__}` instead."
                                )
                    self.active_json = json_content
                    return json_content
            temp.update(append_value)
            self.active_json = json_content
            if self.__is_autosaving:
                if "autosave_path" in self.__kwargs:
                    if type(self.__kwargs["autosave_path"]) != str:
                        raise IncorrectFunctionParameterTypeError(
                            "autosave_path", "str", type(self.__kwargs["autosave_path"]).__name__
                        )
                    path = self.__kwargs["autosave_path"]
                    if not os.path.exists(path):
                        create_file = True
                    else:
                        create_file = False
                else:
                    path = self.__path
                    create_file = False
                self.save_to_file(path=path, create_file=create_file)
            return json_content

    def update_value(
        self,
        json_path: str,
        key_or_index: Union[str, int],
        new_value: Any,
        strict_mode: bool = False,
    ) -> dict:
        """
        Update value in JSON.

        Parameters: `json_path : str` specifies property path, while `key_or_index : Union[str, int]`
        specifies key in JSON object/item index in JSON array. For example, if you
        need to update value with key `update_key` located under `field1.field2.field3.update_key`
        then parameter `key_or_index` will be equal to 'update_key' and `json_path` parameter will
        be equal to `field1.field2.field3`. If you want to update value in the root of the object then `json_path`
        parameter needs to be equal to `$`. To update item in an array, simply pass this items'
        index (integer) as `key_or_index` parameter. Note: if you use an array index while `json_path`
        parameter is pointing to the JSON object or if you use a key name while `json_path` is pointing
        to the JSON array, this function will raise an exception. `new_value : Any` specifies value that will overwrite
        the old one. `strict_mode : bool` parameter enables Strict Mode. If set to `True`, this function will
        compare the types of previous value and the new one. If they are not identical, this function will raise an exception.

        This function returns a Python dictionary with updated content.

        This function raises an `IncorrectFunctionParameterTypeError` exception if one or more of its' parameters
        have incorrect types.
        Tis function raises a `JSONPathError` if JSON path is not valid.
        This function raises a `JSONStrictModeError` if types of old and new values are not the same while Strict Mode is enabled.
        This function raises any additional exceptions if occurred.

        Examples:

        Updating key:value pair in a root of the object:

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('simple.json')
        # Object from `simple.json` >> { "app_name": "Test App", "version": "1.0.5" }
        >>> op.update('$', 'version', '1.1.0')
        >>> op.active_json
        # Output: { "app_name": "Test App", "version": "1.1.0" }

        Updating item in an array:

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('array.json')
        # Object from `array.json` >> { "colors": [ "red", "yellow", "green", "purple" ] }
        >>> op.update_value('colors', 3, "magenta")
        >>> op.active_json
        # Output: { "colors": [ "red", "yellow", "green", "magenta" ] }

        Note: if you don't know an item's index, you can use `get_item_index`
        function from `robust_json.ext` package to get it.

        >>> from robust_json.file import JSonFileParser
        >>> import robust_json.ext as ext
        >>> op = JsonFileParser('array.json')
        # Object from `array.json` >> { "colors": [ "red", "yellow", "green", "purple" ] }
        >>> colors_array = op.get_key_value('colors')
        # Note: please refer to this function's docs if you have
        # any questions
        # colors_array = [ "red", "yellow", "green", "purple" ]
        >>> index = ext.get_item_index('green', colors_array, False)
        # Note: please refer to this function's docs if you have
        # any questions
        # index = 2
        >>> op.update_value('colors', index, 'cyan')
        >>> op.active_json
        # Output: { "colors": [ "red", "yellow", "cyan", "purple" ] }

        Updating value with Strict Mode enabled:

        >>> from robust_json.file import JSonFileParser
        >>> op = JsonFileParser('file.json')
        # Object from `file.json` >> { "id": 1046, "name": "Jamie Kellen" }
        >>> op.update_value('$', 'id', 'string', True)
        # JSONStrictModeError exception is raised.
        # When Strict Mode is enabled, new value must be the same
        # type as the previous one (in this case: int)
        >>> op.update_value('$', 'id', 1087, True)
        >>> op.active_json
        # Output: { "id": 1087, "name": "Jamie Kellen" }

        For more information about this method, please visit:
        https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#file-module-methods-and-properties
        """
        # TODO Add link to an appropriate README section from GitHub

        if type(json_path) != str:
            raise IncorrectFunctionParameterTypeError("json_path", "str", type(json_path).__name__)

        if type(strict_mode) != bool:
            raise IncorrectFunctionParameterTypeError(
                "strict_mode", "bool", type(strict_mode).__name__
            )

        if type(key_or_index) not in [str, int]:
            raise IncorrectFunctionParameterTypeError(
                "key_or_index", "str or int", type(key_or_index).__name__
            )

        json_content = self.active_json

        if not self.__service.check_json_path(json_path, json_content):
            raise JSONPathError(f"Path `{json_path}` is not valid.")

        js_expr = jsonpath.parse(json_path)

        for item in js_expr.find(json_content):
            temp = item.value
            if type(temp) == list:
                if type(key_or_index) != int:
                    raise TypeError(
                        f"Path `{json_path}` is pointing to a JSON array, therefore `key_or_index` parameter must have an `int` type; got `{type(key_or_index).__name__}` instead."
                    )
                if strict_mode == True:
                    if type(temp[key_or_index]) != type(new_value):
                        raise JSONStrictModeError(
                            f"If strict mode is enabled, the type of the new value must be identical to the type of the old one ({type(temp[key_or_index]).__name__}); got `{type(new_value).__name__}` instead."
                        )
                temp[key_or_index] = new_value
                self.active_json = json_content
                return json_content
            else:
                if type(key_or_index) != str:
                    raise TypeError(
                        f"Path `{json_path}` is pointing to a JSON object, therefore `key_or_index` parameter must have a `str` type; got `{type(key_or_index).__name__}` instead."
                    )
                if strict_mode == True:
                    if type(temp[key_or_index]) != type(new_value):
                        raise JSONStrictModeError(
                            f"If strict mode is enabled, the type of the new value must be identical to the type of the old one ({type(temp[key_or_index]).__name__}); got `{type(new_value).__name__}` instead."
                        )
                temp.update({key_or_index: new_value})
                self.active_json = json_content
                if self.__is_autosaving:
                    if "autosave_path" in self.__kwargs:
                        if type(self.__kwargs["autosave_path"]) != str:
                            raise IncorrectFunctionParameterTypeError(
                                "autosave_path",
                                "str",
                                type(self.__kwargs["autosave_path"]).__name__,
                            )
                        path = self.__kwargs["autosave_path"]
                        if not os.path.exists(path):
                            create_file = True
                        else:
                            create_file = False
                    else:
                        path = self.__path
                        create_file = False
                    self.save_to_file(path=path, create_file=create_file)
                return json_content

    def delete(self, json_path: str, key_or_index: Union[str, int]) -> dict:
        """
        Delete value from JSON.

        Parameters: `json_path : str` specifies property path, while `key_or_index : Union[str, int]`
        specifies property name in JSON object or item index in JSON array. For example, if you
        need to delete value with key `delete_key` located under `field1.field2.field3.delete_key`
        then parameter `key_or_index` will be equal to 'delete_key' and `json_path` parameter will
        be equal to `field1.field2.field3`.
        To delete an item in the array, simply pass this items'
        index (integer) as `key_or_index` parameter. Note: if you use an array index while `json_path`
        parameter is pointing to a JSON object or if you use a property name while `json_path` is pointing
        to a JSON array, this function will raise an exception.

        This function returns a Python dictionary with updated content.

        This function raises an `IncorrectFunctionParameterTypeError` exception if one or more of its parameters have incorrect types.
        This function raises a `JSONPathError` if JSON path is not valid.
        This function raises any additional exceptions if occurred.

        Examples:

        Deleteing a key:value pair from root of simple object:

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('del_pair.json')
        # Object from `del_pair.json` >> { "application_name": "PetHome", "version": "1.0", "display": "standalone" }
        >>> op.delete('$', 'display')
        >>> op.active_json
        # Output: { "application_name": "PetHome", "version": "1.0" }

        Deleting item an from array

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('array.json')
        # Object from `array.json` >> { "colors": [ "red", "magenta", "green" ] }
        >>> op.delete('colors', 2)
        >>> op.active_json
        # Output: { "colors": [ "red", "magenta" ] }

        Note: if you don't know the item index, you can
        use `get_item_index` function from `robust_json.ext`
        package to get it. See the code below:

        >>> from robust_json.file import JSonFileParser
        >>> import robust_json.ext as ext
        >>> op = JsonFileParser('array.json')
        # Object from `array.json` >> { "colors": [ "red", "magenta", "green" ] }
        >>> array = op.get_key_value('colors')
        # Note: please refer to this function's docs if you have
        # any questions
        # array = [ "red", "magenta", "green" ]
        >>> index = ext.get_item_index('red', array, False)
        # Note: please refer to this function's docs if you have
        # any questions
        # index = 0
        >>> op.delete('colors', index)
        >>> op.active_json
        # Output: { "colors": [ "magenta", "green" ] }

        For more information about this method, please visit:
        https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#file-module-methods-and-properties

        """

        # TODO Add link to an appropriate README section from GitHub

        if type(json_path) != str:
            raise IncorrectFunctionParameterTypeError("json_path", "str", type(json_path).__name__)

        if type(key_or_index) not in [str, int]:
            raise IncorrectFunctionParameterTypeError(
                "key_or_index", "str or int", type(key_or_index).__name__
            )

        json_content = self.active_json

        if not self.__service.check_json_path(json_path, json_content):
            raise JSONPathError(f"Path `{json_path}` is not valid.")

        js_expr = jsonpath.parse(json_path)

        for item in js_expr.find(json_content):
            temp = item.value
            if type(temp) == list:
                if type(key_or_index) != int:
                    raise TypeError(
                        f"Path `{json_path}` is pointing to a JSON array, therefore `key_or_index` parameter must have an `int` type; got `{type(key_or_index).__name__}` instead."
                    )
                del temp[key_or_index]
                self.active_json = json_content
                return json_content
            else:
                if type(key_or_index) != str:
                    raise TypeError(
                        f"Path `{json_path}` is pointing to a JSON object, therefore `key_or_index` parameter must have a `str` type; got `{type(key_or_index).__name__}` instead."
                    )
                del temp[key_or_index]
                self.active_json = json_content
                if self.__is_autosaving:
                    if "autosave_path" in self.__kwargs:
                        if type(self.__kwargs["autosave_path"]) != str:
                            raise IncorrectFunctionParameterTypeError(
                                "autosave_path",
                                "str",
                                type(self.__kwargs["autosave_path"]).__name__,
                            )
                        path = self.__kwargs["autosave_path"]
                        if not os.path.exists(path):
                            create_file = True
                        else:
                            create_file = False
                    else:
                        path = self.__path
                        create_file = False
                    self.save_to_file(path=path, create_file=create_file)
                return json_content

    def minify(self) -> None:
        """
        Minify all JSON in source file into one line.

        For more information about this method
        please visit: https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#file-module-methods-and-properties
        """

        file = open(self.__path, "r")
        unfiltered = file.read()
        cont = JSON.loads(unfiltered)
        file.close()

        file_w = open(self.__path, "w")
        file_w.write(JSON.dumps(cont, indent=None))
        file_w.close()

    def prettify(self, indent: int = 4) -> None:
        """
        Add indentations to JSON in source file to make it look better
        and improve its readability.

        Parameters: `indent : int` specifies the number of spaces added.
        If not provided, this function will use the default value (4 spaces/1 tab)

        This function raises an `IncorrectFunctionParameterTypeError`
        exception if `indent` parameter has an incorrect type.

        For more information about this method please visit:
        https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#file-module-methods-and-properties
        """

        if type(indent) != int and indent != None:
            raise IncorrectFunctionParameterTypeError("indent", "int", type(indent).__name__)

        if indent == 0 or indent == None:
            self.minify()
            return

        file = open(self.__path, "r")
        unfiltered = file.read()
        cont = JSON.loads(unfiltered)
        file.close()

        file_w = open(self.__path, "w")
        file_w.write(JSON.dumps(cont, indent=indent))
        file.close()

    def reset(self, discard_active_object: bool = False) -> dict:
        # ? Do we need autosaving feature here?
        """
        Discard changes to JSON.

        If called, this function will return initial JSON object
        (without any changes).

        Parameters: `discard_active_object : bool` specifies if
        changes will be discarded on active object or not. If
        set to `True`, active object will be reset to an initial
        state, otherwise it will be left untouched.

        This function returns a Python dictionary with initial object.

        This function raises an `IncorrectFunctionParameterTypeError`
        exception if `discard_active_object` has an incorrect type.

        Examples:

        Getting an initial object and storing it in a variable:

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('simple_data.json')
        # Object from `simple_data.json` >> { "simple_key": "simple_value" }
        >>> op.append('$', { "test_arr": [1, 2, 3] })
        # We appended key:value pair to distinguish objects among each other
        >>> initial = op.reset()
        >>> initial
        # initial = { "simple_key": "simple_value" }
        >>> op.active_json
        # Output: { "simple_key": "simple_value", "test_arr": [1, 2, 3] }
        # Calling this method without parameters simply makes it return initial
        # object, saving the active one for future use

        Discarding changes to active object:

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('simple_data.json') # We will use the same object
        # Object from `simple_data.json` >> { "simple_key": "simple_value" }
        >>> op.append('$', { "test_arr": [1, 2, 3] })
        # We appended key:value pair to distinguish objects among each other
        >>> initial = op.reset(discard_active_object=True)
        >>> initial
        # initial = { "simple_key": "simple_value" }
        >>> op.active_json
        # Output: { "simple_key": "simple_value" }
        # Calling this method with `discard_active_object` set to `True`
        # makes it completely revert all changes to active object, making it
        # equal to the initial one.
        # Note: if called with `discard_active_object` set to `True`, there
        # is no way of going back. All changes will be gone for good.
        # Please use this with extreme caution!

        For more information about this method, please visit:
        https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#file-module-methods-and-properties
        """

        if type(discard_active_object) != bool:
            raise IncorrectFunctionParameterTypeError(
                "discard_active_object", "bool", type(discard_active_object).__name__
            )

        if discard_active_object == True:
            self.active_json = self.__backup

        return self.__backup

    def save_to_file(
        self, path: str = None, prettify: bool = True, create_file: bool = False
    ) -> None:
        """
        Save JSON object to file.

        Parameters: `path : str` specifies path to an external file. If not provided, object will be saved into source file.
        `prettify : bool` enables indentations in JSON (improves its readability). `create_file : bool` enables file creation.
        If set to `True`, this function will create a new file and save JSON there, if provided path leads to file that does not exist. Note:
        if set to `True` and path is pointing to an existing file, this function will raise an exception.

        This function raises an `IncorrectFunctionParameterTypeError` if one or more of its parameters have incorrect type.

        Examples:

        Saving active object to the source file:

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('data.json')
        # Object from `data.json` >> { "user_name": "Akama0978", "date_of_registration": "19-07-2019", "role": "guest" }
        >>> op.update_value('$', 'user_name', 'Amasi0022')
        # Let's change some values to see the difference
        >>> op.save_to_file() # Active object had been saved to source file (in this case: `data.json`)
        >>> op.active_json
        # Output: { "user_name": "Amasi0022", "date_of_registration": "19-07-2019", "role": "guest" }
        # Object from 'data.json' >> { "user_name": "Amasi0022", "date_of_registration": "19-07-2019", "role": "guest" }
        # Calling this function without parameters overwrites JSON in the original file with new JSON

        Saving active object to a different file (existing):

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('data.json') # We will use the same file
        # Object from `data.json` >> { "user_name": "Akama0978", "date_of_registration": "19-07-2019", "role": "guest" }
        >>> op.update_value('$', 'user_name', 'Amasi0022')
        # Let's change some values to see the difference
        >>> op.save_to_file(path='updated_data.json')
        # Active object had been saved to a different file
        # (in this case: `updated_data.json`)
        >>> op.active_json
        # Output: { "user_name": "Amasi0022", "date_of_registration": "19-07-2019", "role": "guest" }
        # Object from 'updated_data.json' >> { "user_name": "Amasi0022", "date_of_registration": "19-07-2019", "role": "guest" }
        # Calling this function with different `path` parameter saves active object to a different file.
        # Note: if specified path is not valid (file not found), an exception will be raised.

        Saving active object to a new file (non-existing):

        >>> from robust_json.file import JsonFileParser
        >>> op = JsonFileParser('data.json') # We will use the same file
        # Object from `data.json` >> { "user_name": "Akama0978", "date_of_registration": "19-07-2019", "role": "guest" }
        >>> op.update_value('$', 'user_name', 'Amasi0022')
        # Let's change some values to see the difference
        >>> op.save_to_file(path='new_file.json')
        # FileNotFoundError exception had been raised
        # To complete this operation, `create_file` parameter
        # needs to be set to `True`
        >>> op.save_to_file(path='new_file.json', create_file=True)
        >>> op.active_json
        # Output: { "user_name": "Amasi0022", "date_of_registration": "19-07-2019", "role": "guest" }
        # Object from 'new_file.json' >> { "user_name": "Amasi0022", "date_of_registration": "19-07-2019", "role": "guest" }

        For more information about this method, please visit:
        https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#file-module-methods-and-properties
        """

        if type(path) != str and path != None:
            raise IncorrectFunctionParameterTypeError("path", "str", type(path).__name__)

        if type(prettify) != bool:
            raise IncorrectFunctionParameterTypeError("prettify", "bool", type(prettify).__name__)

        if type(create_file) != bool:
            raise IncorrectFunctionParameterTypeError(
                "create_file", "bool", type(create_file).__name__
            )

        if path == None:
            file_path = self.__path
        else:
            file_path = path

        file_json = self.active_json

        if prettify == True:
            indent = 4
        else:
            indent = None

        if create_file == True:
            if self.__service.check_file_path(file_path):
                raise FileExistsError(
                    f"File `{file_path}` already exists. Either set `create_file` parameter to `False` or change `path` parameter to silence this error."
                )
            file = open(file_path, "x")
            file.write(JSON.dumps(file_json, indent=indent))
            file.close()
        else:
            if not self.__service.check_file_path(file_path):
                raise FileNotFoundError(
                    f"File `{file_path}` doesn't exist. If you want to create a new file under this path, please set `create_file` parameter to `True`."
                )
            file = open(file_path, "w")
            file.write(JSON.dumps(file_json, indent=indent))
            file.close()
