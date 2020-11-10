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

with open("README.md", "r") as f:
    lond_desc = f.read()

setuptools.setup(
    name="robust-json",  # or robust_json
    version="1.1.6",
    author="Nickolai Beloguzov",
    author_email="nickolai.beloguzov@gmail.com",
    packages=setuptools.find_packages(),
    install_requires=["jsonpath_ng", "pathlib2"],
    long_description=lond_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/NickolaiBeloguzov/robust-json",
    description="Robust and easy-to-use framework for working with JSON",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
)
