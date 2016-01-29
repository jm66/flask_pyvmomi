# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(
    name='Flask-pyVmomi',
    version='1.1.2016.1.29',
    packages=['flask_pyvmomi'],
    url='https://gitlab.eis.utoronto.ca/vss/flask-pyvmomi',
    license='Apache 2.0',
    author='University of Toronto',
    author_email='jm.lopez@utoronto.ca',
    description='Adds pyVmomi support to Flask',
    keywords=['pyvmomi', 'vmware'],
    install_requires=['flask>=0.10.1', 'pyvmomi>=6.0.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ]
)
