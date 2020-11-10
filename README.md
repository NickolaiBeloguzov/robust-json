# Robust JSON

The robust-json package is a lightweight, but capable library for working with JSON files and objects in Python.

## Installation
<!--- TODO Add link to PyPI --->
You can install this package directly from [PyPI](https://pypi.org/project/robust-json/):

    pip install robust-json 
This library is supported on python 3.x only.

## Contributing
If you want to improve this project, first discuss your idea by opening a new issue. After that fork this repository and implement this awesome feature or fix this annoying bug. Then create a new PR and wait for approval. 

*Note: please read [contributing.md](https://github.com/NickolaiBeloguzov/robust-json/blob/master/CONTRIBUTING.md) file first. There you can find code of conduct and useful information regarding contribution process.*
    

## Modules

This library includes 4 modules:

* [**file**](#file-mod): This module provides functionality for working with  JSON files.
* [**object**](#obj-mod): This module provides functionality for working with JSON objects (Python dictionaries)
_Note: the difference between file and object modules is that during initialization 'file' module expects path to JSON file while 'object' module expects a Python dictionary. For more information please read corresponding sections._
* [**errors**](#err-mod): This module contains all exceptions that may be raised during package runtime.
* [**ext**](#ext-mod): This module provides some extra functions that can be helpful while working with JSON.

## File module overview
<div id='file-mod'><div>

This module provides various methods for working with JSON files through _JsonFileParser_ class. It automatically parses and loads valid JSON from specified file and also checks if file is ready for processing. To access it, simply import _JsonFileParser_ from file module:

    from robust_json.file import JsonFileParser
and initialize it:

    op = JsonFileParser(path_to_json_file)
During initialization a *JSONFileError* exception may be raised. This means that parser could not process contents of specified file or file has an unsupported extension. Also during this phase a *FileNotFoundError* may be raised marking that specified file doesn't exist.

### File module methods and properties

* **Properties**:
  * **JsonFileParser.file_formats**
    This property lists all file extensions supported by this module in form of an array. At the moment only _.json_ and _.txt_ files are supported. This is used during class initialization to determine if file can pe processed.
  * **JsonFileParser.path**
    This property returns source file path
  * **JsonFileParser.active_json**
    This property returns JSON object with all the recent changes.
  * **JsonFileParser.backup**
    This property returns the initial JSON object, ignoring all the recent changes.
    These two last properties may be confusing, so here is an example
    (_Note: see corresponding documentation section for JsonFileParser.append() function_):
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test1.json') #Class initialization
    # Contents of 'test1.json' file: {'test_key': 'test_value'}

    op.append('$', {'append_key': 'append_value'})
    print(op.active_json)
    # Output: {'test_key': 'test_value', 'append_key': 'append_value'}

    print(op.backup)
    # Output: {'test_key': 'test_value'}

    # As you can see, JsonFileParser.backup property is equal to initial contents of 'test1.json' file.
    # This is useful when there is a need to discard all changes to JSON object.
    ```
* **Methods**:
  * **JsonFileParser.get_json_from_file()**
    This method retrieves all JSON from file and returns it as a Python dictionary. It's called automatically when specified file is processed for the first time.
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test1.json') # JsonFileParser.get_json_from_file() function is called here
    ```
  * **JsonFileParser.get_key_value(json_path: str)**
    This method accesses a value from specific key:value pair in JSON object and returns it.
    _json_path:str_ parameter specifies a path to key:value pair (e.g. field0.field1.[...].fieldn).
    Example:
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test2.json')
    # Contents of 'test2.json' file: {'test_key': 'test_value', 'test_arr': [1, 2, 3]}

    val = op.get_key_value('test_key')
    print(val)
    # Output: 'test_value'

    # You can use this method to retrieve an element from JSON array
    val = op.get_key_value('test_arr[1]')
    print(val)
    # Output: 2
    ```
    This function will raise an *IncorrectFunctionParameterTypeError* if its parameter has an incorrect type. This function will also raise a *JSONPathError* if specified JSON path is not valid (does not exist or could not be accessed).

  * **JsonFileParser.append(json_path: str, append_value: any, append_at_end: bool = False)**
    This method appends value to existing JSON object and returns a Python dictionary with updated contents.
    *json_path:str* parameter specifies a path where new value will be added. To append value to the root of JSON object, *json_path* needs to be equal to '$'. *append_value:any* parameter specifies a value that will be appended. *append_at_end:bool* controls the behaviour of this function regarding JSON arrays of objects (structures like this: [{}, {}, {}, ...]) and general arrays (structures like this: [a, b, c, ...]). It has no influence on other structures. If set to False, function will try to add given value to each object of an array. If set to True, function will try to append given value at the end of an array. (see examples below). This function will return a Python dictionary with updated JSON.

    This function will raise a *IncorrectFunctionParameterTypeEroor* exception if its parameter(-s) has(-ve) an incorrect type. This function will also raise a *ValueError* exception if 'append_value' is empty (is equal to empty string, empty array, empty dictionary, etc.). This function will raise a *JSONPathError* if provided path is not valid (does not exist or could not be accessed). This function will raise any additional exceptions if occurred.

    Examples:

    Adding a simple key:value pair to the root of an object
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test3.json')
    # Contents of 'test3.json' file: {'test_key': 'test_value'}

    op.append('$', {'add_key': 'add_var'})
    print(op.active_json)
    # Output: {'test_key': 'test_value', 'add_key': 'add_var'}
    ```

    Adding new object to the array of objects
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('users.json')
    # Contents of 'users.json' file: {'users': [{'id': 1, 'name': 'Ken'}, {'id': 2, 'name': 'Alec'}]}

    op.append('users', {'id': 3, 'name': 'Liza'})
    print(op.active_json)
    # Output: {'users': [{'id': 3, 'name': 'Lisa'}, {'id': 3, 'name': 'Lisa'}]}

    # This is not good!
    # This happened because 'append_at_end' parameter is set to False.

    # Function appended new object to each of the objects in the array and new values have overwritten the old 
    # ones.

    # Note: we can discard these unwanted/malicious changes using JsonFileParser.reset() function with 
    # its parameter set to True. (please refer to corresponding section in docs)

    op.reset(True)
    print(op.active_json)
    # Output: {'users': [{'id': 1, 'name': 'Ken'}, {'id': 2, 'name': 'Alec'}]}

    # We need to set 'append_at_end' parameter to True to avoid this.

    op.append('users', {'id': 3, 'name': 'Liza'}, True)
    print(op.active_json)
    # Output: {'users': [{'id': 1, 'name': 'Ken'}, {'id': 2, 'name': 'Alec'}, {'id': 3, 'name': 'Lisa'}]}
    ```

    Adding a key:value pair to each object of an array
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('users.json')
    # Contents of 'users.json' file: {'users': [{'id': 1, 'name': 'Ken'}, {'id': 2, 'name': 'Alec'}]}

    op.append('users', {'role': 'guest'})
    print(op.active_json)
    # Output: {'users':[{'id':1, 'name':'Ken', 'role':'guest'}, {'id':2, 'name':'Alec', 'role':'guest'}]}
    ```

    Adding new element to an array of elements:
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test4.json')
    # Contents of 'test4.json' file: {'colors': ['cyan', 'magenta']}

    op.append('colors', 'yellow')
    print(op.active_json)
    # Output: {'colors': ['cyan', 'magenta']}

    # Nothing happened.
    # That's because 'append_at_end' parameter is set to False.
    # Function tried to append new string to each string and failed.
    # To fix this, we need to set 'append_at_end' parameter to True.

    op.append('colors', 'yellow', True)
    print(op.active_json)
    # Output: {'colors': ['cyan', 'magenta', 'yellow']}
    ```
  * **JsonFileParser.update_value(json_path: str, key_or_index: Union[str, int], new_value: any, strict_mode: bool = False)**
    <div id='file-upd'></div>

    This function will update value in key:value pair and return a Python dictionary with updated contents. 
    *json_path:str* parameter specifies a path to key:value pair/array/etc. parent that needs to be updated. (To update value in the root of JSON object, *json_path* needs to be equal to '$') while *key_or_index:Union[str, int]* parameter specifies key (if it's an object) or array index (if it's an array). This implies that if we need to update key with path 'field0.field1.upd_key', then *json_path* will be equal to 'field0.field1' and *key_or_index* parameter will be equal to 'upd_key'. *Note: if you use an array index while 'json_path' parameter is pointing to JSON object, or if you use a property name while 'json_path' is pointing to JSON array, an exception will be raised* (See examples below). *new_value:any* specifies value that will overwrite the old one and *strict_mode:bool* enables Strict Mode. By default this mode is turned off. If turned on, this method will ensure that new value has the same type as the old one (if old value is a string, then the new one also needs to be a string, etc.). If types are not matching, an exception will be raised.

    This function will raise an *IncorrectFunctionParameterTypeError* exception is its parameter(-s) has(-ve) an incorrect type. This function will also raise a *JSONStrictModeError* in case of mismatched types if Strict Mode is enabled and a *JSONPathError* exception if JSON path is not valid (doesn't exist or could not be accessed). This function will raise any additional exceptions if occured.

    Examples:

    Updating key:value pair in root of the object:
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test5.json')
    # Contents of 'test5.json' file: {'app_name': 'HomeCare', 'version', '1.0.0'}

    op.update_value('$', 'version': '1.0.5')
    print(op.active_json)
    # Output: {'app_name': 'HomeCare', 'version': '1.0.5'}
    ```

    Updating item in an array:
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test6.json')
    # Contents of 'test6.json' file: {'app_name': 'HomeCare', 'authors': ['Alec Hammer', 'Nick Rogers']}

    op.update_value('authors', 1, 'Nick Rogerson')
    print(op.active_json)
    # Output: {'app_name': 'HomeCare', 'authors': ['Alec Hammer', 'Nick Rogerson']}
    ```
    ```
    # Note: if you don't know the index of an item, you can use 
    # 'get_item_index()' function from 'robust_json.ext' module to get it. 
    # (See corresponding section in the docs)

    from robust_json.file import JsonFileParser
    import robust_json.ext as ext

    op = JsonFileParser('test6.json')
    # Contents of 'test6.json' file: {'app_name': 'HomeCare', 'authors': ['Alec Hammer', 'Nick Rogers']}

    # Getting an array for future use
    authors_array = op.get_key_value('authors')
    print(authors_array)
    # Output: ['Alec Hammer', 'Nick Rogers']

    # Finding the index
    index = ext.get_item_index('Alec Hammer', authors_array, False)
    print(index)
    # Output: 0

    #Updating value
    op.update_value('authors', index, 'Alain Hammer')
    print(op.active_json)
    # Output: {'app_name': 'HomeCare', 'authors': ['Alain Hammer', 'Nick Rogers']}
    ```
    Updating value with Strict Mode:
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test6.json')
    # Contents of 'test6.json' file: {'app_name': 'HomeCare', 'app_id': 1077}

    op.update_value('$', 'app_id', 'this is a string', True)
    # A 'StrictModeError' exception was raised.
    # This happened because new value has a different type.
    # Let's try again, but with integer.

    op.update_value('$', 'app_id', 1080, True)
    print(op.active_json)
    # Output: {'app_name': 'HomeCare', 'app_id': 1080}
    ```

  * **JsonFileParser.delete(json_path: str, key_or_index: Union[str, int])**
    This function will delete an element from JSON and return a Python dictionary with updated contents.
    *json_path:str* parameter specifies a path to key:value pair/array/etc. parent that needs to be deleted. (To delete value in the root of JSON object, *json_path* needs to be equal to '$') while *key_or_index:Union[str, int]* parameter specifies key (if it's an object) or array index (if it's an array). This implies that if we need to delete key with path 'field0.field1.del_key', then *json_path* will be equal to 'field0.field1' and *key_or_index* parameter will be equal to 'del_key'. *Note: if you use an array index while 'json_path' parameter is pointing to JSON object, or if you use a property name while 'json_path' is pointing to JSON array, an exception will be raised* (See examples below).
    This function will raise an *IncorrectFunctionParameterTypeError* exception is its parameter(-s) has(-ve) an incorrect type. This function will also raise a *JSONPathError* exception if JSON path is not valid (doesn't exist or could not be accessed). This function will raise any additional exceptions if occurred.

    Examples:

    Deleting key:value pair in root of the object:
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test7.json')
    # Contents of 'test5.json' file: {'test_key': 'test_val', 'del_key': 'del_val'}

    op.delete('$', 'del_key')
    print(op.active_json)
    # Output: {'test_key': 'test_val'}
    ```
    Deleting item in an array:
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test8.json')
    # Contents of 'test6.json' file: {'app_name': 'PetShopify', 'authors': ['Alec Hammer', 'Nick Rogers']}

    op.delete('authors', 1)
    print(op.active_json)
    # Output: {'app_name': 'PetShopify', 'authors': ['Alec Hammer']}
    ```
    ```
    # Note: if you don't know the index of an item, you can use 'get_item_index()' 
    # function from 'robust_json.ext' module to get it. (See corresponding section in the docs)

    from robust_json.file import JsonFileParser
    import robust_json.ext as ext

    op = JsonFileParser('test9.json')
    # Contents of 'test6.json' file: {'app_name': 'PetShopify', 'authors': ['Alec Hammer', 'Nick Rogers']}

    # Getting an array for future use
    authors_array = op.get_key_value('authors')
    print(authors_array)
    # Output: ['Alec Hammer', 'Nick Rogers']

    # Finding the index
    index = ext.get_item_index('Alec Hammer', authors_array, False)
    print(index)
    # Output: 0

    #Updating value
    op.delete('authors', index)
    print(op.active_json)
    # Output: {'app_name': 'HomeCare', 'authors': ['Nick Rogers']}
    ```
  * **JsonFileParser.minify()**
    This function will remove all indentations in JSON file. Basically it will compress all JSON into one line.

    This function does not return any value.
  * **JsonFileParser.prettify(indent: int = 4)**
    This function will add indentations to JSON in source file to improve its readability. *indent:int* parameter specifies the number of spaces. By default it is equal to 4. This function is a complete opposite to *JsonFileParser.minify()*

    This function does not return any value.

    This function will raise an *IncorrectFunctionParameterTypeError* if its parameter has an incorrect type.

  * **JsonFileParser.reset(discard_active_object: bool = False)**
    This function will reset active JSON object, removing any changes made to it.
    *discard_active_object:bool* parameter controls the behaviour of this function regarding the active JSON object (JsonFileParser.active_json property). If set to False, this method will simply return an initial object and keep all the changes to the actove JSON. If set to True, this function will still return the initial object, but will also reset the active one, and all changes will be gone for good.

    This function will raise an *IncorrectFunctionParameterTypeError* if its parameter has an incorrect type.

    Examples:

    Getting an intial object and storing it in a variable:

    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test10.json')
    # Contents of `test10.json` file: { "simple_key": "simple_value" }

    op.append('$', { "test_arr": [1, 2, 3] })
    # We appended key:value pair to distinguish objects among each other.

    initial = op.reset()
    print(initial)
    # initial = { "simple_key": "simple_value" }

    print(op.active_json)
    # Output: { "simple_key": "simple_value", "test_arr": [1, 2, 3] }
    # Calling this method without parameters simply makes it return initial
    # object, saving the active one for future use.
    ```

    Getting an initial object and resetting an active one:

    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('test10.json')
    # Contents of `test10.json` file: { "simple_key": "simple_value" }

    op.append('$', { "test_arr": [1, 2, 3] })
    # We appended key:value pair to distinguish objects among each other.

    initial = op.reset(True)
    print(initial)
    # Output: { "simple_key": "simple_value" }

    print(op.active_json)
    # Output: { "simple_key": "simple_value" }

    # Calling this method with 'discard_active_object' set to True.
    # makes it completely revert all changes to active object, making it
    # equal to the initial one.

    # Warning!
    # Note: if called with 'discard_active_object' set to True, there
    # is no way of going back. All changes will be gone for good.
    # Please use this with extreme caution!
    ```
  * **JsonFileParser.save_to_file(path: str = None, prettify: bool = True, create_file: bool = False)**
    This function will save active JSON object into file.
    *path:str* parameter specifies path to the file. If left empty, active object will be saved into source file. *prettify:bool* parameter enables indentations. By default it is set to True. If set to False, JSON will be compressed into one line. *create_file:bool* parameter enables file creation. If set to True, this function will create a new file and save active object there, but obly if *path* parameter is pointing to non-existing file. *Note: if create_file is set to True ans path is pointing to an existing file, an exception will be raised.*

    This function will raise a *JSONFileError* if end file is not supporting JSON (has an unsupported extension). This function will raise a *FileExistsError* if *create_file* is set to True and file already exists under specified path.
    This function will raise a *FileNotFoundError* if *create_file* is set to False and file could not be located under specified path. This function will raise any additional exceptions if occurred.

    Examples:

    Saving active object to the source file:

    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('data.json')
    # Contents of 'data.json' file: {'name': 'Helen Anderson', 'employee_id': 107756}

    op.update_value('$', 'employee_id', 107744)
    print(op.active_json)
    # Output: {'name': 'Helen Anderson', 'employee_id': 107744}

    op.save_to_file()
    # Contents of 'data.json' file: {'name': 'Helen Anderson', 'employee_id': 107744}

    # Calling 'save_to_file' method without any arguments makes it 
    # overwrite an object in source file ('data.json' in this case) 
    # with the value of JsonFileParser.active_json property.
    ```
    Saving active object to a different file (existing):
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('data.json')
    # Contents of 'data.json' file: {'name': 'Helen Anderson', 'employee_id': 107756}

    op.update_value('$', 'employee_id', 107744)
    print(op.active_json)
    # Output: {'name': 'Helen Anderson', 'employee_id': 107744}

    op.save_to_file(path='new_data.json')
    # Contents of 'new_data.json' file: {'name': 'Helen Anderson', 'employee_id': 107744}
    # Calling this function with different 'path' parameter will 
    # make this function save the value of JsonFileParser.active_json property into
    # existing file ('new_data.json' in this case). But if file cannot be found, a 'FileNotFoundError' 
    # exception will be raised.
    ```
    Saving active object to a different file (non-existing):
    ```
    from robust_json.file import JsonFileParser

    op = JsonFileParser('data.json')
    # Contents of 'data.json' file: {'name': 'Helen Anderson', 'employee_id': 107756}

    op.update_value('$', 'employee_id', 107744)
    print(op.active_json)
    # Output: {'name': 'Helen Anderson', 'employee_id': 107744}

    op.save_to_file(path='new_data.json')
    # A 'FileNotFoundError' exception has been raised.
    # It happened because this file does not exist.
    # To fix this we need to set 'create_file' parameter to True.

    op.save_to_file(path='new_data.json', create_file=True)
    # Contents of 'new_data.json' file: {'name': 'Helen Anderson', 'employee_id': 107744}
    # Calling the function with 'create_file' set to True and different path makes it create 
    # a new file and save the value of JsonFileParser.active_json property there.
    # But if file already exists, a 'FileExistsError' will be raised.
    ```
## Object module overview
<div id='obj-mod'>(robust_json.object)</div>

This module provides various methods for working with JSON object directly through _JsonObjectParser_ class. This class is specifically designed to work with JSON received from API calls or to be used in APIs. To access it, simply import _JsonObjectParser_ from file module:

    from robust_json.object import JsonObjectParser
and initialize it:

    op = JsonObjectParser(json_obj)
During initialization a *IncorrectFunctionParameterTypeError* exception may be raised. This means that *json* parameter has an incorrect type.

### Object module methods and properties

* **Properties**:
  * **JsonObjectParser.active_json**
    This property returns JSON object with all the recent changes.
  * **JsonObjectParser.backup**
    This property returns the initial JSON object, ignoring all the recent changes.
    These two last properties may be confusing, so here is an example
    (_Note: see corresponding documentation section for JsonObjectParser.append() function_):
    ```
    from robust_json.object import JsonObjectParser

    obj = {'test_key': 'test_value'}

    op = JsonObjectParser(obj) #Class initialization
    

    op.append('$', {'append_key': 'append_value'})
    print(op.active_json)
    # Output: {'test_key': 'test_value', 'append_key': 'append_value'}

    print(op.backup)
    # Output: {'test_key': 'test_value'}

    # As you can see, JsonObjectParser.backup property is equal to initial object.
    # This is useful when there is a need to discard all changes to JSON object.
    ```
* **Methods**:
  * **JsonObjectParser.get_key_value(json_path: str)**
    This method accesses a value from specific key:value pair in JSON object and returns it.
    _json_path:str_ parameter specifies a path to key:value pair (e.g. field0.field1.[...].fieldn).
    Example:
    ```
    from robust_json.object import JsonObjectParser

    obj = {'test_key': 'test_value', 'test_arr': [1, 2, 3]}

    op = JsonObjectParser(obj)
    

    val = op.get_key_value('test_key')
    print(val)
    # Output: 'test_value'

    # You can use this method to retrieve an element from JSON array
    val = op.get_key_value('test_arr[1]')
    print(val)
    # Output: 2
    ```
    This function will raise an *IncorrectFunctionParameterTypeError* is its parameter has an incorrect type. This function will also raise a *JSONPathError* if specified JSON path is not valid (does not exist or could not be accessed). This function will raise any additional exceptions if occurred.

  * **JsonObjectParser.append(json_path: str, append_value: any, append_at_end: bool = False)**
    This method appends value to existing JSON object and returns a Python dictionary with updated contents.
    *json_path:str* parameter specifies a path where new value will be added. To append value to the root of JSON object, *json_path* needs to be equal to '$'. *append_value:any* parameter specifies a value that will be appended. *append_at_end:bool* controls the behaviour of this function regarding JSON arrays of objects (structures like this: [{}, {}, {}, ...]) and general arrays (structures like this: [a, b, c, ...]). It has no influence on other structures. If set to False, function will try to add given value in each object of an array. If set to True, function will try to append given value at the end of an array. (see examples below). This function will return a Python dictionary with updated JSON.

    This function will raise a *IncorrectFunctionParameterTypeEroor* exception if its parameter(-s) has(-ve) an incorrect type. This function will also raise a *ValueError* exception if 'append_value' is empty (empty string, empty array, empty dictionary). This function will raise a *JSONPathError* if provided path is not valid (does not exist or could not be accessed). This function will raise any additional exceptions if occurred.

    Examples:

    Adding a simple key:value pair to the root of an object
    ```
    from robust_json.object import JsonObjectParser

    obj = {'test_key': 'test_value'}

    op = JsonObjectParser(obj)

    op.append('$', {'add_key': 'add_var'})
    print(op.active_json)
    # Output: {'test_key': 'test_value', 'add_key': 'add_var'}
    ```

    Adding new object to the array of objects
    ```
    from robust_json.object import JsonObjectParser

    obj = {'users': [{'id': 1, 'name': 'Ken'}, {'id': 2, 'name': 'Alec'}]}

    op = JsonObjectParser(obj)

    op.append('users', {'id': 3, 'name': 'Liza'})
    print(op.active_json)
    # Output: {'users': [{'id': 3, 'name': 'Lisa'}, {'id': 3, 'name': 'Lisa'}]}

    # This is not good!
    # This happened because 'append_at_end' parameter is set to False.

    # Function appended new object to each of the objects in the array and new values overwrote the old 
    # ones.

    # Note: we can discard these unwanted/malicious changes using JsonObjectParser.reset() function with 
    # its parameter set to True. (please refer to corresponding section in docs)

    op.reset(True)
    print(op.active_json)
    # Output: {'users': [{'id': 1, 'name': 'Ken'}, {'id': 2, 'name': 'Alec'}]}

    # We need to set 'append_at_end' parameter to True to avoid this.

    op.append('users', {'id': 3, 'name': 'Liza'}, True)
    print(op.active_json)
    # Output: {'users': [{'id': 1, 'name': 'Ken'}, {'id': 2, 'name': 'Alec'}, {'id': 3, 'name': 'Lisa'}]}
    ```

    Adding a key:value pair to each object of an array
    ```
    from robust_json.object import JsonObjectParser

    obj = {'users': [{'id': 1, 'name': 'Ken'}, {'id': 2, 'name': 'Alec'}]}

    op = JsonObjectParser(obj)

    op.append('users', {'role': 'guest'})
    print(op.active_json)
    # Output: {'users':[{'id':1, 'name':'Ken', 'role':'guest'}, {'id':2, 'name':'Alec', 'role':'guest'}]}
    ```

    Adding new element to an array of elements:
    ```
    from robust_json.object import JsonObjectParser

    obj = {'colors': ['cyan', 'magenta']}

    op = JsonObjectParser(obj)

    op.append('colors', 'yellow')
    print(op.active_json)
    # Output: {'colors': ['cyan', 'magenta']}

    # Nothing happened
    # That's because 'append_at_end' parameter is set to False
    # Function tried to append new string to each string and failed
    # To fix this, we need to set 'append_at_end' parameter to True

    op.append('colors', 'yellow', True)
    print(op.active_json)
    # Output: {'colors': ['cyan', 'magenta', 'yellow']}
    ```
  * **JsonObjectParser.update_value(json_path: str, key_or_index: Union[str, int], new_value: any, strict_mode: bool = False)**
    <div id='obj-upd'></div>

    This function will updaate value in key:value pair and return a Python dictionary with updated contents. 
    *json_path:str* parameter specifies a path to key:value pair/array/etc. parent that needs to be updated. (To update value in the root of JSON object, *json_path* needs to be equal to '$') while *key_or_index:Union[str, int]* parameter specifies key (if it's an object) or array index (if it's an array). This implies that if we need to update key with path 'field0.field1.upd_key', then *json_path* will be equal to 'field0.field1' and *key_or_index* parameter will be equal to 'upd_key'. *Note: if you use an array index while 'json_path' parameter is pointing to JSON object, or if you use a property name while 'json_path' is pointing to JSON array, an exception will be raised* (See examples below). *new_value:any* specifies value that will overwrite the old one and *strict_mode:bool* enables Strict Mode. By default this mode is turned off. If turned on, this method will ensure that new value has the same type as the old one (if old value is a string, then the new one also needs to be a string, etc.). If types are not matching, an exception will be raised.

    This function will raise an *IncorrectFunctionParameterTypeError* exception is its parameter(-s) has(-ve) an incorrect type. This function will also raise a *JSONStrictModeError* in case of mismatched types if Strict Mode is enabled and a *JSONPathError* exception if JSON path is not valid (doesn't exist or could not be accessed). This function will raise any additional exceptions if occurred.

    Examples:

    Updating key:value pair in root of the object:
    ```
    from robust_json.object import JsonObjectParser

    op = JsonObjectParser({'app_name': 'HomeCare', 'version', '1.0.0'})

    op.update_value('$', 'version': '1.0.5')
    print(op.active_json)
    # Output: {'app_name': 'HomeCare', 'version': '1.0.5'}
    ```

    Updating item in an array:
    ```
    from robust_json.object import JsonObjectParser

    op = JsonObjectParser({'app_name': 'HomeCare', 'authors': ['Alec Hammer', 'Nick Rogers']})

    op.update_value('authors', 1, 'Nick Rogerson')
    print(op.active_json)
    # Output: {'app_name': 'HomeCare', 'authors': ['Alec Hammer', 'Nick Rogerson']}
    ```
    ```
    # Note: if you don't know the index of an item, you can use 'get_item_index()' 
    # function from 'robust_json.ext' module to get it. (See corresponding section in the docs)

    from robust_json.object import JsonObjectParser
    import robust_json.ext as ext

    op = JsonObjectParser({'app_name': 'HomeCare', 'authors': ['Alec Hammer', 'Nick Rogers']})

    # Getting an array for future use
    authors_array = op.get_key_value('authors')
    print(authors_array)
    # Output: ['Alec Hammer', 'Nick Rogers']

    # Finding the index
    index = ext.get_item_index('Alec Hammer', authors_array, False)
    print(index)
    # Output: 0

    #Updating value
    op.update_value('authors', index, 'Alain Hammer')
    print(op.active_json)
    # Output: {'app_name': 'HomeCare', 'authors': ['Alain Hammer', 'Nick Rogers']}
    ```
    Updating value with Strict Mode:
    ```
    from robust_json.object import JsonObjectParser

    op = JsonObjectParser({'app_name': 'HomeCare', 'app_id': 1077})

    op.update_value('$', 'app_id', 'this is a string', True)
    # An 'StrictModeError' was raised
    # This happened because new value has a different type
    # Let's try again, but with integer

    op.update_value('$', 'app_id', 1080, True)
    print(op.active_json)
    # Output: {'app_name': 'HomeCare', 'app_id': 1080}
    ```

  * **JsonObjectParser.delete(json_path: str, key_or_index: Union[str, int])**
    This function will delete an element from JSON and return a Python dictionary with updated contents.
    *json_path:str* parameter specifies a path to key:value pair/array/etc. parent that needs to be deleted. (To delete value in the root of JSON object, *json_path* needs to be equal to '$') while *key_or_index:Union[str, int]* parameter specifies key (if it's an object) or array index (if it's an array). This implies that if we need to delete key with path 'field0.field1.del_key', then *json_path* will be equal to 'field0.field1' and *key_or_index* parameter will be equal to 'del_key'. *Note: if you use an array index while 'json_path' parameter is pointing to JSON object, or if you use a property name while 'json_path' is pointing to JSON array, an exception will be raised* (See examples below).
    This function will raise an *IncorrectFunctionParameterTypeError* exception is its parameter(-s) has(-ve) an incorrect type. This function will also raise a *JSONPathError* exception if JSON path is not valid (doesn't exist or could not be accessed). This function will raise any additional exceptions if occurred.

    Examples:

    Deleting key:value pair in root of the object:
    ```
    from robust_json.object import JsonObjectParser

    obj = {'test_key': 'test_val', 'del_key': 'del_val'}

    op = JsonObjectParser(obj)
    

    op.delete('$', 'del_key')
    print(op.active_json)
    # Output: {'test_key': 'test_val'}
    ```
    Deleting item in an array:
    ```
    from robust_json.object import JsonObjectParser

    op = JsonObjectParser('test8.json')
    # Contents of 'test6.json' file: {'app_name': 'PetShopify', 'authors': ['Alec Hammer', 'Nick Rogers']}

    op.delete('authors', 1)
    print(op.active_json)
    # Output: {'app_name': 'PetShopify', 'authors': ['Alec Hammer']}
    ```
    ```
    # Note: if you don't know the index of an item, you can use 'get_item_index()' 
    # function from 'robust_json.ext' module to get it. (See corresponding section in the docs)

    from robust_json.object import JsonObjectParser
    import robust_json.ext as ext

    obj = {'app_name': 'PetShopify', 'authors': ['Alec Hammer', 'Nick Rogers']}

    op = JsonObjectParser(obj)


    # Getting an array for future use
    authors_array = op.get_key_value('authors')
    print(authors_array)
    # Output: ['Alec Hammer', 'Nick Rogers']

    # Finding the index
    index = ext.get_item_index('Alec Hammer', authors_array, False)
    print(index)
    # Output: 0

    #Updating value
    op.delete('authors', index)
    print(op.active_json)
    # Output: {'app_name': 'HomeCare', 'authors': ['Nick Rogers']}
    ```

  * **JsonObjectParser.reset(discard_active_object: bool = False)**
    This function will reset active JSON object, removing any changes made to it.
    *discard_active_object:bool* parameter controls the behaviour of this function regarding the active JSON object (JsonObjectParser.active_json property). If set to False, this method will simply return an initial object and keep all the changes to the actove JSON. If set to True, this function will still return the initial object, but will also reset the active one, and all changes will be gone for good.

    This function will raise an *IncorrectFunctionParameterTypeError* if its parameter has an incorrect type. This function will raise any additional exceptions if occurred.

    Examples:

    Getting an intial object and storing it in a variable:

    ```
    from robust_json.object import JsonObjectParser

    obj = { "simple_key": "simple_value" }

    op = JsonObjectParser(obj)

    op.append('$', { "test_arr": [1, 2, 3] })
    # We appended key:value pair to distinguish objects among each other

    initial = op.reset()
    print(initial)
    # initial = { "simple_key": "simple_value" }

    print(op.active_json)
    # Output: { "simple_key": "simple_value", "test_arr": [1, 2, 3] }
    # Calling this method without parameters simply makes it return initial
    # object, saving the active one for future use
    ```

    Getting an initial object and resetting an active one:

    ```
    from robust_json.object import JsonObjectParser

    obj = { "simple_key": "simple_value" }

    op = JsonObjectParser(obj)

    op.append('$', { "test_arr": [1, 2, 3] })
    # We appended key:value pair to distinguish objects among each other

    initial = op.reset(True)
    print(initial)
    # Output: { "simple_key": "simple_value" }

    print(op.active_json)
    # Output: { "simple_key": "simple_value" }

    # Calling this method with 'discard_active_object' set to True
    # makes it completely revert all changes to active object, making it
    # equal to the initial one.

    # Warning!
    # Note: if called with 'discard_active_object' set to True, there
    # is no way of going back. All changes will be gone for good.
    # Please use this with extreme caution!
    ```
  * **JsonObjectParser.save_to_file(path: str, prettify: bool = True, create_file: bool = False)**
    This function will save active JSON object into file.
    *path:str* parameter specifies path to the file. *prettify:bool* parameter enables indentations. By default it is set to True. If set to False, JSON will be compressed into one line. *create_file:bool* parameter enables file creation. If set to True, this function will create a new file and save active object there, but obly if *path* parameter is pointing to non-existing file. *Note: if create_file is set to True ans path is pointing to an existing file, an exception will be raised.*

    This function will raise a *JSONFileError* if end file is not supporting JSON (has an unsupported extension). This function will raise a *FileExistsError* if *cheate_file* is set to True and file already exists under specified path.
    This function will raise a *FileNotFoundError* if *create_file* is set to False and file could not be located under specified path. This function will raise any additional exceptions if occurred.

    Examples:

    Saving active object to a file (existing):
    ```
    from robust_json.object import JsonObjectParser

    obj = {'name': 'Helen Anderson', 'employee_id': 107756}

    op = JsonObjectParser(obj)

    op.update_value('$', 'employee_id', 107744)
    print(op.active_json)
    # Output: {'name': 'Helen Anderson', 'employee_id': 107744}

    op.save_to_file(path='new_data.json')
    # Contents of 'new_data.json' file: {'name': 'Helen Anderson', 'employee_id': 107744}
    # Calling this function with different 'path' parameter will 
    # make this function save the value of JsonObjectParser.active_json property into
    # existing file ('new_data.json' in this case). But if file cannot be found, a 'FileNotFoundError' 
    # exception will be raised.
    ```
    Saving active object to a file (non-existing):
    ```
    from robust_json.object import JsonObjectParser

    obj = {'name': 'Helen Anderson', 'employee_id': 107756}

    op = JsonObjectParser(obj)
    

    op.update_value('$', 'employee_id', 107744)
    print(op.active_json)
    # Output: {'name': 'Helen Anderson', 'employee_id': 107744}

    op.save_to_file(path='new_data.json')
    # A 'FileNotFoundError' exception has been raised.
    # It happened because this file does not exist.
    # To fix this we need to set 'create_file' parameter to True.

    op.save_to_file(path='new_data.json', create_file=True)
    # Contents of 'new_data.json' file: {'name': 'Helen Anderson', 'employee_id': 107744}
    # Calling the function with 'create_file' set to True and different path makes it create 
    # a new file and save the value of JsonObjectParser.active_json property there.
    # But if file already exists, a 'FileExistsError' will be raised.
    ```
## Errors module overview
<div id='err-mod'></div>

This module contains all custom exceptions that can be raised during package runtime. There are a total of 5: *JSONFileError*, *JSONPathError*, *JSONStrictModeError*, *JSONObjectError*, *IncorrectFunctionParameterTypeError*. If you need to import them, it can be done like this:
```
import robust_json.errors as json_err
```
### **Exceptions**
* **JSONFileError**
    This exception indicates that there is an error with JSON file (it has an unsupported extension, cannot be processed, etc.)
* **JSONPathError**
    This exception indicates that JSON path (field0.field1.[...].fieldn) is not valid (cannot be accessed or doesn't exist in the object)
* **JSONStrictModeError**
    This exception can be raised only by [*JsonFileParser.update_value()*](#file-upd) and [*JsonObjectParser.update_value()*](#obj-upd) methods because only these function support Strict Mode at the moment. This exception indicates that there is a type mismatch during update. For further information, you can see the examples of the above mentionned functions in their corresponding sections to see how this works.
* **JSONObjectError**
    This exception indicates that JSON object is not valid (has incorrect format, syntax errors, etc.)
* **IncorrectFunctionParameterTypeError**
    This exception indicates that one or more of function's parameters has incorrect type.

## Extension module overview
<div id='ext-mod'></div>
This module provides some useful methods that can reduce development time.

### **Methods**
* **filter_json_array(json_array: list, field: string, value: any)**
    This function will filter given array of JSON objects and return it. 
    *json_array:list* parameter specifies the list that neesd to be filtered, *field:str* specifies the key and *value:any* specifies the value. Two last parameters form a key:value pair which takes a role of a filter.

    This function will return a list with filtered content.

    This function will raise an *IncorrectFunctionParameterTypeError* exception if one or more of its parameter has an incorrect type. This function will raise a *JSONObjectError* if *json_arr* is not an array of objects ([{}, {}, {}, ...]). This function will raise any additional exceptions if occurred.

    Example:
    Filtering an array of objects by a specific key:value pair
    ```
    from robust_json.ext import filter_json_array

    orders = [{"order_id":1648,"country":"USA" },{"order_id":1830,"country":"Liberia"},
    {"order_id":6703,"country":"USA"},{"order_id":2995,"country":"Russia"}]

    usa_orders = filter_json_array(orders, 'country', 'USA')
    print(usa_orders)
    # Output: [{"order_id":1648,"country":"USA" }, {"order_id":6703,"country":"USA"}]
    ```
* **get_item_index(item: any, array: list, always_array: bool = False)**
    This function will find an intem in given array and return its index(-es).
    *item:any* specifies item which index needs to be found. *array:list* specifies array where this item needs to be present and *always_array:bool* controls the return type of this function. If set to False, this function will return an array if there is multiple matches, but will return an integer if there is only one match. If set to True, this function will always return an array (see examples below).

    Examples:

    ```
    from robust_json.ext import get_item_index

    arr1 = [1, 2, 3, 4]
    index = get_item_index(2, arr1, False)
    print(index)
    # Output: 1
    # Note: we set 'always_array' parameter to False, therefore function returned an integer

    arr2 = [5, 9, 10, 45, 555]
    index = get_item_index(10, arr2, True)
    print(index)
    # Output: [2]
    # Note: we set 'always_array' parameter to True, therefore function returned an array even if there 
    # is only one match. This is useful when this array will be iterated later on.

    arr3 = [1, 6, 'string', 8, 5, 4, 'string', 0, 22]
    index = get_item_index('string', arr3, False)
    # Note: even if 'alway_array' parameter set to False, this function will return an array of 
    # integers because there are multiple matches
    print(index)
    # Output: [2, 6]

    arr4 = [1, 2, 3]
    index = get_item_index(6, arr4, False)
    # Note: if item is not present in the array and 'always_array' parameter set to False, 
    # None will be returned.
    print(index)
    # Output: None

    arr5 = [5, 6, 7]
    index = get_item_index(10, arr5, True)
    # Note: if item is not present in the array and 'always_array' parameter set to True, 
    # an empty array will be returned.
    print(index)
    # Output: []
    ```
* **reverse_array(array: list)**
    This function will reverse an array and return it.

    This function will raise an *IncorrectFunctionParameterTypeError* if its parameter has an incorrect type. This function will raise any additional exceptions if occurred.

    Example:
    ```
    from robust_json.ext import reverse_array

    arr = ['a', 'b', 'c']
    rev_arr = reverse_array(arr)
    print(rev_arr)
    # Output: ['c', 'b', 'a']
    ```



