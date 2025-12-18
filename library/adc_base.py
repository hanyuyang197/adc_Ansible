#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Horizon Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import json
import sys
import os

# Python 2/3兼容性处理
try:
    # Python 2
    import urllib2 as urllib_request
except ImportError:
    # Python 3
    import urllib.request as urllib_request
    import urllib.error as urllib_error


class ADCBase:
    """Base class for ADC modules"""

    def __init__(self, module):
        self.module = module
        self.ip = module.params['ip']
        self.authkey = module.params['authkey']

    def _format_url(self, action):
        """Format URL for ADC API request"""
        return "http://%s/adcapi/v2.0/?authkey=%s&action=%s" % (self.ip, self.authkey, action)

    def make_request(self, method, action, data=None):
        """Make HTTP request to ADC API"""
        url = self._format_url(action)

        try:
            if sys.version_info[0] >= 3:
                # Python 3
                import urllib.parse as urllib_parse

                if method.upper() == 'GET':
                    req = urllib_request.Request(url, method='GET')
                else:  # POST
                    if data:
                        post_data = json.dumps(data).encode('utf-8')
                        req = urllib_request.Request(url, data=post_data, headers={
                                                    'Content-Type': 'application/json'})
                    else:
                        req = urllib_request.Request(
                            url, headers={'Content-Type': 'application/json'})

                response = urllib_request.urlopen(req)
                response_data = response.read().decode('utf-8')
            else:
                # Python 2
                import urllib as urllib_parse

                if method.upper() == 'GET':
                    req = urllib_request.Request(url)
                    req.get_method = lambda: 'GET'
                else:  # POST
                    if data:
                        post_data = json.dumps(data)
                        req = urllib_request.Request(url, data=post_data, headers={
                                                    'Content-Type': 'application/json'})
                    else:
                        req = urllib_request.Request(
                            url, headers={'Content-Type': 'application/json'})

                response = urllib_request.urlopen(req)
                response_data = response.read()

            # Parse response
            if response_data:
                return json.loads(response_data)
            else:
                return {'success': False, 'msg': 'Empty response'}

        except Exception as e:
            return {'success': False, 'msg': 'Request failed: %s' % str(e)}

    def download_file(self, action, file_path):
        """Download file from ADC API"""
        url = self._format_url(action)

        try:
            if sys.version_info[0] >= 3:
                # Python 3
                req = urllib_request.Request(url, method='GET')
                response = urllib_request.urlopen(req)

                # Write to file
                with open(file_path, 'wb') as f:
                    f.write(response.read())
            else:
                # Python 2
                req = urllib_request.Request(url)
                req.get_method = lambda: 'GET'
                response = urllib_request.urlopen(req)

                # Write to file
                with open(file_path, 'wb') as f:
                    f.write(response.read())

            return True

        except Exception as e:
            self.module.fail_json(msg="Failed to download file: %s" % str(e))
            return False

    def format_adc_response_for_ansible(self, response_data, action="", changed_default=True):
        """
        Format ADC response for Ansible module return

        Args:
            response_data (str/dict): API response data
            action (str): Action name
            changed_default (bool): Default changed status

        Returns:
            tuple: (success, result_dict)
        """

        # Initialize result
        result = {
            'success': False,
            'result': '',
            'errcode': '',
            'errmsg': '',
            'data': {}
        }

        try:
            # Parse JSON if string
            if isinstance(response_data, str):
                parsed_data = json.loads(response_data)
            else:
                parsed_data = response_data

            result['data'] = parsed_data

            # Extract fields
            result['result'] = parsed_data.get('result', '')
            result['errcode'] = parsed_data.get('errcode', '')
            result['errmsg'] = parsed_data.get('errmsg', '')

            # Check if successful
            if result['result'].lower() == 'success':
                result['success'] = True
            else:
                # Handle idempotency - check if error contains keywords indicating already exists
                errmsg = result['errmsg'].lower() if isinstance(
                    result['errmsg'], str) else str(result['errmsg']).lower()
                if any(keyword in errmsg for keyword in ['已存在', 'already exists', 'already exist', 'exists']):
                    # Idempotency handling: if failure is due to already existing, consider it success
                    result['success'] = True
                    result['result'] = 'success (already exists)'

        except json.JSONDecodeError as e:
            result['errmsg'] = "JSON parse failed: %s" % str(e)
            result['errcode'] = 'JSON_PARSE_ERROR'
        except Exception as e:
            result['errmsg'] = "Response parse exception: %s" % str(e)
            result['errcode'] = 'PARSE_EXCEPTION'

        # Format for Ansible return
        if result['success']:
            # Success
            result_dict = {
                'changed': changed_default,
                'msg': '%s operation successful' % action if action else 'Operation successful',
                'response': result['data']
            }

            # Adjust for idempotency success
            if 'already exists' in result['result']:
                result_dict['changed'] = False
                result_dict['msg'] = '%s operation successful (resource already exists, no changes needed)' % action if action else 'Operation successful (resource already exists, no changes needed)'

            return True, result_dict
        else:
            # Failure
            result_dict = {
                'changed': False,
                'msg': '%s operation failed' % action if action else 'Operation failed',
                'error': {
                    'result': result['result'],
                    'errcode': result['errcode'],
                    'errmsg': result['errmsg']
                },
                'response': result['data']
            }
            return False, result_dict