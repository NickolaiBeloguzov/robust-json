# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

setuptools.setup(
    name='robust-json', # or robust_json
    version='1.0',
    author='Nickolai Beloguzov',
    author_email='nickolai.beloguzov@gmail.com',
    packages=setuptools.find_packages(),
    install_requires = [
        'jsonpath_ng'
    ],
    description='Robust and easy-to-use framework for working with JSON' # TODO Add a long description (lond_description property) from README.md 
)
