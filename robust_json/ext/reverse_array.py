# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from robust_json.errors import IncorrectFunctionParameterTypeError


def reverse_array(array: list) -> list:
    """
    Reverse an array

    This function reverses an array and returns it.

    This function will raise an `IncorrectFunctionParameterTypeError` exception if `array`
    paramete has an incorrect type.
    This function raises any additional exceptions if occurred.

    For more information about this method, please visit:
    https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md#object-module-methods-and-properties
    """
    if type(array) != list:
        raise IncorrectFunctionParameterTypeError("array", "list", type(array).__name__)

    return array[::-1]
