# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from _typeshed import NoneType
from typing import Union

from robust_json.errors import IncorrectFunctionParameterTypeError


def get_item_index(
    item: any, array: list, always_array: bool = False
) -> Union[int, list, NoneType]:
    """
    Get items' index in an array.

    Parameters: `item : any` parameter specifies item which index needs to be found.
    `array : list` parameter specifies array where to search. `always_array : bool`
    parameter sets return type strictly to a list. If set to `True`, this function will
    always return an array even if there is only one element. This is useful when in the future
    this output will be iterated. If set to `False`, return type will be determined automatically.

    This function returns an index/an array if indexes. If item is not present in the array,
    this function will return `None` (if `always_array` is set to `True` and item is not found in
    the array, this function will return an empty list)

    This function raises a `IncorrectFunctionParameterTypeError` if one or more of its parameters have incorrect types.
    This function raises a `ValueError` exception if `array` parameter is equal to an empty list.
    This function raises any additional exceptions if occurred.

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

    For more information please visit:
    https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#methods
    """

    if type(array) != list:
        raise IncorrectFunctionParameterTypeError("array", "list", type(array).__name__)

    if array == []:
        raise ValueError("Parameter `array` is an empty list.")

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
