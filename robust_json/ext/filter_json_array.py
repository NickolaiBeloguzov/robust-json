# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from easy_json.errors import IncorrectFunctionParameterTypeError, JSONObjectError

def filter_json_array(json_array: list, field: str, value: any) -> list:
        """
        Filter JSON array of objects according to given parameters.

        This function will filter given array of JSON object,
        using provided during function call.

        Example:

        Filtering an array of objects by a specific key:value pair

        >>> obj = [ { "order_id": 1648, "country": "USA" }, { "order_id": 1830, "country": "Liberia" }, { "order_id": 6703, "country": "USA" } ]
        >>> filtered  = filter_json_array(obj, 'country', 'USA')
        >>> filtered
        # Output: [ { "order_id": 1648, "country": "USA" }, { "order_id": 6703, "country": "USA" } ]
        """
        #TODO Add REGEX support

        

        if type(json_array) != list:
            raise IncorrectFunctionParameterTypeError('json_array', 'list', type(json_array).__name__)

        if type(field) != str:
            raise IncorrectFunctionParameterTypeError('field', 'str', type(field).__name__)

        if field == '':
            raise ValueError('Parameter `field` is empty.')

        item_indexes = []
        for i in enumerate(json_array):
            if type(i[1]) == dict:
                if i[1][field] == value:
                    item_indexes.append(i[1])
                else: 
                    pass
            else:
                raise JSONObjectError(f'Parameter `json_array` must contain only Python dictionaries; got {type(i[1]).__name__} instead (Array index: [{i[0]}])')
        
        return item_indexes