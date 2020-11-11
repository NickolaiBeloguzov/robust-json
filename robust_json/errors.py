# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

###################################
# * This file contains all custom exceptions
# * used by main package
###################################


class JSONObjectError(Exception):
    """This exception indicates that something is wrong with JSON object."""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"JSONObjectError: {self.message}"
        else:
            return "JSONObjectError: No message provided"


class JSONPathError(Exception):
    """This exception indicates that there is a problem with JSON path."""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"JSONPathError: {self.message}"
        else:
            return "JSONPathError: No message provided"


class JSONStrictModeError(Exception):
    """This exception indcates that there is an error in Strict Mode."""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"JSONStrictModeError: {self.message}"
        else:
            return "JSONStrictModeError: No message provided"


class JSONFileError(Exception):
    """This exception indicates that there is an error with JSON file."""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"JSONFileError: {self.message}"
        else:
            return "JSONFileError: No message provided"


class IncorrectFunctionParameterTypeError(Exception):
    """This exception indicates that one or more functions' parameters have incorrect types."""

    def __init__(self, variable_name: str, correct_type: str, curr_type: str):
        self.var_name = variable_name
        self.correct_type = correct_type
        self.current_type = curr_type

    def __str__(self):
        if self.var_name and self.current_type and self.correct_type:
            return f"Parameter `{self.var_name}` must have a `{self.correct_type}` type; got `{self.current_type}` instead."
