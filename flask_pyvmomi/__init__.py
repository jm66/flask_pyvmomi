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

"""Flask extension for pyVmomi."""
import ssl
import sys
import requests

# disable  urllib3 warnings
requests.packages.urllib3.disable_warnings()
# Python 2.7.9, 2.10 CERTIFICATE_VERIFY_FAILED
if sys.version.split(' ')[0] in ['2.7.9', '2.7.10']:
    ssl._create_default_https_context = ssl._create_unverified_context


from flask_pyvmomi.pyvmomi import pyVmomi
from flask_pyvmomi.exceptions import pyVmomiError
