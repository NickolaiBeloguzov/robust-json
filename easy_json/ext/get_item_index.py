from typing import Union

from easy_json.errors import IncorrectFunctionParameterTypeError

def get_item_index(item: any, array: list, always_array: bool = False) -> Union[int, list]:
    u"""
    Get item index in an array.

    Parameters: `item : any` parameter specifies an item which index needs to be found.
    `array : list` parameter specifies an array where to search. `always_array : bool`
    parameter sets return type strictly to a list. If set to `True`, this function will
    always return an array even if there is only one element. This is useful when in the future
    this output will be iterated. If set to `False`, return type will be determined automatically.
    
    This function will return an index/an array if indexes. If item is not present in given array,
    `None` will be returned (if `always_array` is set to `True` and item is not found in
    given array, an empty list will be returned)

    This function will raise a `IncorrectFunctionParameterTypeError` if at least one of the
    parameters has an incorrect type.
    This function will raise a `ValueError` exception if `array` parameter is equal to an empty list.

    Examples:

    >>> arr = ['1', '2', '3', '4', '5']
    >>> index = get_item_index('3', arr)
    >>> index
    # index = 2

    >>> arr = ['1', '2', '3', '4', '1', '5', '1']
    >>> index = get_item_index('1', arr)
    >>> index
    # index = [0, 6]

    >>> arr = ['1', '2', '3', '4']
    >>> index = get_item_index('1', arr, True)
    >>> index
    # index = [0]

    >>> arr = ['1', '2', '3', '4', '5']
    >>> index = get_item_index('6', arr)
    >>> index
    # index = None

    >>> arr = ['1', '2', '3', '4', '5']
    >>> index = get_item_index('6', arr, True)
    >>> index
    # index = []
    """

    #? Maybe let uset choose if he wants this function to return only array instead of automatic conversion? (Done)
    
    if type(array) != list:
        raise IncorrectFunctionParameterTypeError('array', 'list', type(array).__name__)

    if array == []:
        raise ValueError('Parameter `array` is an empty list.')

    item_indexes = []



    for i in enumerate(array):
        if i[1] == item:
            item_indexes.append(i[0])
        else:
            pass

    if len(item_indexes) == 1 and always_array == False:
        return item_indexes[0]

    elif len(item_indexes) == 0 and always_array == False:
        return None
    else:
        return item_indexes