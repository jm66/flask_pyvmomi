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

import ssl
from flask import Flask
from pyVim import connect
from base64 import b64decode
from pyVmomi import vim
from exceptions import pyVmomiError
import logging
# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

LOGGER = logging.getLogger('flask_pyvmomi')


class pyVmomi(object):

    def __init__(self, app=None):
        self.app = app
        self.options = None
        self.pyvmomi = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not isinstance(app, Flask):
            raise TypeError('app must be a Flask application')
        app.pyvmomi = self

        self.__load_config(app)
        self.pyvmomi = self.connect()

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def __load_config(self, app):
        """Loads the configuration from the Flask configuration."""
        options = dict()
        vcenter_server = app.config.get('VCENTER_HOST')
        if vcenter_server:
            options['vcenter_server'] = vcenter_server

        vcenter_port = app.config.get('VCENTER_PORT')
        if vcenter_port:
            options['vcenter_port'] = vcenter_port

        vcenter_username = app.config.get('VCENTER_USERNAME')
        if vcenter_username:
            options['vcenter_username'] = vcenter_username

        vcenter_password = b64decode(app.config.get('VCENTER_PASSWORD')) if \
            app.config.get('VCENTER_PASSWORD_ENCODED') else \
            app.config.get('VCENTER_PASSWORD')
        if vcenter_password:
            options['vcenter_password'] = vcenter_password

        vcenter_check_ssl = app.config.get('VCENTER_CHECK_SSL')
        if vcenter_check_ssl:
            options['vcenter_check_ssl'] = vcenter_check_ssl
        self.options = options

    def connect(self):
        try:
            if self.options['vcenter_check_ssl']:
                si = connect.SmartConnect(host=self.options['vcenter_server'],
                                          user=self.options['vcenter_username'],
                                          port=self.options['vcenter_port'],
                                          pwd=self.options['vcenter_password'],
                                          sslContext=ssl._create_unverified_context())
            else:
                si = connect.SmartConnect(host=self.options['vcenter_server'],
                                          user=self.options['vcenter_username'],
                                          port=self.options['vcenter_port'],
                                          pwd=self.options['vcenter_password'])
            print('Flask-pyVmomi: Initializing vCenter connection')
            print('Flask-pyVmomi: Got session key: {}'.format(si.content.sessionManager.currentSession.key))
            return si
        except vim.fault as e:
            raise pyVmomiError(e.msg)
        except RuntimeError as e:
            raise pyVmomiError(str(e))

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'vcenter'):
            connect.Disconnect(ctx.vcenter)

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'vcenter'):
                ctx.vcenter = self.connect()
            return ctx.vcenter
