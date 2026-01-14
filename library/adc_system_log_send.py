#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Horizon Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.horizon.modules.plugins.module_utils.adc_common import (
    make_adc_request,
    format_adc_response,
    check_adc_auth,
    handle_adc_error,
    build_adc_params,
    validate_adc_params,
    adc_result_check,
    adc_format_output,
    build_params_with_optional,
    make_http_request,
    get_param_if_exists,
    create_adc_module_args,
    adc_response_to_ansible_result,
    format_adc_response_for_ansible
)
import json
import sys
__metaclass__ = type

# ADC API响应解析函数


def send_request(url, data=None, method='GET'):
    """发送HTTP请求到ADC设备"""
    import sys
    response_data = None
    try:
        if method == 'POST' and data:
            data_json = json.dumps(data)
            data_bytes = data_json.encode('utf-8')

            if sys.version_info[0] >= 3:
                # Python 3
                import urllib.request as urllib_request
                req = urllib_request.Request(url, data=data_bytes)
                req.add_header('Content-Type', 'application/json')
            else:
                # Python 2
                import urllib2 as urllib_request
                req = urllib_request.Request(url, data=data_bytes)
                req.add_header('Content-Type', 'application/json')
        else:
            if sys.version_info[0] >= 3:
                # Python 3
                import urllib.request as urllib_request
                req = urllib_request.Request(url)
            else:
                # Python 2
                import urllib2 as urllib_request
                req = urllib_request.Request(url)

        response = urllib_request.urlopen(req)
        response_data = response.read()

        # 正确处理响应数据的编码
        if isinstance(response_data, bytes):
            # 尝试UTF-8解码，如果失败则使用latin1作为后备
            try:
                response_text = response_data.decode('utf-8')
            except UnicodeDecodeError:
                response_text = response_data.decode('latin1')
        else:
            response_text = response_data

        # 安全地解析JSON响应
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # 如果不是有效的JSON格式，直接返回原始响应内容
            return response_text

        # 标准化响应格式
        # 成功响应保持原样
        # 错误响应标准化为 {"result":"error","errcode":"REQUEST_ERROR","errmsg":"..."}
        if isinstance(result, dict) and 'status' in result and result['status'] is False:
            # 修复Unicode解码错误：确保错误消息正确处理中文字符
            error_msg = result.get('msg', '')
            if isinstance(error_msg, bytes):
                try:
                    error_msg = error_msg.decode('utf-8')
                except UnicodeDecodeError:
                    error_msg = error_msg.decode('latin1')

            return {
                'result': 'error',
                'errcode': 'REQUEST_ERROR',
                'errmsg': error_msg if error_msg else '请求失败'
            }
        else:
            return result
    except UnicodeDecodeError as e:
        # 如果解码失败，直接返回错误信息
        return {
            'result': 'error',
            'errcode': 'UNICODE_DECODE_ERROR',
            'errmsg': f'响应解码失败: {str(e)}'
        }
    except Exception as e:
        return {
            'result': 'error',
            'errcode': 'REQUEST_EXCEPTION',
            'errmsg': str(e)
        }


DOCUMENTATION = r'''
---
module: adc_system_log_send
short_description: Manage ADC system log sending configuration
description:
  - Manage syslog server configuration for ADC devices.
  - Supports adding, listing, getting, editing, and deleting syslog server configurations.
version_added: "1.0.0"
options:
  action:
    description:
      - The action to perform on syslog server configuration.
    type: str
    required: true
    choices: [ add, list, get, edit, delete ]
  # Parameters for add/edit actions
  host:
    description:
      - Syslog server address (hostname/IPv4/IPv6).
    type: str
  port:
    description:
      - Syslog server port.
    type: int
  log_code:
    description:
      - Code encoding status (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  facility:
    description:
      - Syslog facility number (0-7).
    type: int
    choices: [0, 1, 2, 3, 4, 5, 6, 7]
  nat_log:
    description:
      - Send NAT logs (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  audit_log:
    description:
      - Send audit logs (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  service_log:
    description:
      - Send service logs (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  dns_log:
    description:
      - Send DNS logs (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  match_type:
    description:
      - Filter matching type.
      - 0: Disable filtering
      - 1: Level/event/keyword/module OR operation
      - 2: Level/event/keyword/module AND operation
    type: int
    choices: [0, 1, 2]
  level_filter:
    description:
      - Log level filter (0-7).
    type: int
    choices: [0, 1, 2, 3, 4, 5, 6, 7]
  event_list:
    description:
      - Event list array.
      - 1: Interface status
      - 2: Device reboot
      - 3: Login event
      - 4: Health check failure
      - 5: Health check busy
      - 9: VM linkage
      - 11: GSLB log
      - 12: Erule log
    type: list
    elements: int
  keyword_filter:
    description:
      - Keyword filter.
    type: str
  module_filter:
    description:
      - Module filter (comma-separated modules).
    type: str
  keyword_type:
    description:
      - Keyword type (string or regular).
    type: str
    choices: [string, regular]
author:
  - Horizon Inc.
'''

EXAMPLES = r'''
- name: Add syslog server
  adc_system_log_send:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: add
    host: "10.66.30.129"
    port: 514
    nat_log: 1
    audit_log: 1
    service_log: 1
    dns_log: 1

- name: List syslog servers
  adc_system_log_send:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: list

- name: Get specific syslog server
  adc_system_log_send:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: get
    host: "10.66.30.129"
    port: 514

- name: Edit syslog server
  adc_system_log_send:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: edit
    host: "10.66.30.129"
    port: 514
    level_filter: 5
    keyword_filter: "error"

- name: Delete syslog server
  adc_system_log_send:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: delete
    host: "10.66.30.129"
    port: 514
'''

RETURN = r'''
servers:
  description: List of syslog servers when action=list
  returned: when action=list
  type: list
  sample: [
    {
      "host": "10.66.30.129",
      "port": 514,
      "log_code": 0,
      "facility": 1,
      "nat_log": 1,
      "audit_log": 1,
      "service_log": 1,
      "dns_log": 1
    }
  ]
server:
  description: Specific syslog server when action=get
  returned: when action=get
  type: dict
  sample: {
    "host": "10.66.30.129",
    "port": 514,
    "log_code": 0,
      "facility": 1,
      "nat_log": 1,
      "audit_log": 1,
      "service_log": 1,
      "dns_log": 1
  }
msg:
  description: Result message
  returned: always
  type: str
  sample: "Syslog server added successfully"
'''


def log_syslog_server_add(module):
    """Add syslog server configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.syslog.server.add" % (
        ip, authkey)

    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['host'] is not None:
        params['host'] = module.params['host']
    else:
        module.fail_json(msg="host is required for add action")

    if module.params['port'] is not None:
        params['port'] = module.params['port']
    else:
        module.fail_json(msg="port is required for add action")

    # Optional parameters
    if module.params['log_code'] is not None:
        params['log_code'] = module.params['log_code']
    if module.params['facility'] is not None:
        params['facility'] = module.params['facility']
    if module.params['nat_log'] is not None:
        params['nat_log'] = module.params['nat_log']
    if module.params['audit_log'] is not None:
        params['audit_log'] = module.params['audit_log']
    if module.params['service_log'] is not None:
        params['service_log'] = module.params['service_log']
    if module.params['dns_log'] is not None:
        params['dns_log'] = module.params['dns_log']
    if module.params['match_type'] is not None:
        params['match_type'] = module.params['match_type']
    if module.params['level_filter'] is not None:
        params['level_filter'] = module.params['level_filter']
    if module.params['event_list'] is not None:
        params['event_list'] = module.params['event_list']
    if module.params['keyword_filter'] is not None:
        params['keyword_filter'] = module.params['keyword_filter']
    if module.params['module_filter'] is not None:
        params['module_filter'] = module.params['module_filter']
    if module.params['keyword_type'] is not None:
        params['keyword_type'] = module.params['keyword_type']

    # Make API call
    response = send_request(url, params, method='POST')

    # Format response
    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': 'Syslog server added successfully'}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "添加syslog服务器失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据，不尝试解析为JSON格式
            return True, {'response': response}
    else:
        # 直接返回原始响应，不尝试解析为JSON格式
        return True, {'response': response if response is not None else 'No response data'}


def log_syslog_server_list(module):
    """List syslog server configurations"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.syslog.server.list" % (
        ip, authkey)

    # Make API call
    response = send_request(url, method='GET')

    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'servers': response.get('data', [])}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "获取syslog服务器列表失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据，不尝试解析为JSON格式
            return True, {'servers': response}
    else:
        # 直接返回原始响应，不尝试解析为JSON格式
        return True, {'servers': response if response is not None else 'No response data'}


def log_syslog_server_get(module):
    """Get specific syslog server configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.syslog.server.get" % (
        ip, authkey)

    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['host'] is not None:
        params['host'] = module.params['host']
    else:
        module.fail_json(msg="host is required for get action")

    if module.params['port'] is not None:
        params['port'] = module.params['port']
    else:
        module.fail_json(msg="port is required for get action")

    # Make API call
    response = send_request(url, params, method='POST')

    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'server': response.get('data', {})}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "获取syslog服务器失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据，不尝试解析为JSON格式
            return True, {'server': response}
    else:
        # 直接返回原始响应，不尝试解析为JSON格式
        return True, {'server': response if response is not None else 'No response data'}


def log_syslog_server_edit(module):
    """Edit syslog server configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.syslog.server.edit" % (
        ip, authkey)

    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['host'] is not None:
        params['host'] = module.params['host']
    else:
        module.fail_json(msg="host is required for edit action")

    if module.params['port'] is not None:
        params['port'] = module.params['port']
    else:
        module.fail_json(msg="port is required for edit action")

    # Optional parameters
    if module.params['log_code'] is not None:
        params['log_code'] = module.params['log_code']
    if module.params['facility'] is not None:
        params['facility'] = module.params['facility']
    if module.params['nat_log'] is not None:
        params['nat_log'] = module.params['nat_log']
    if module.params['audit_log'] is not None:
        params['audit_log'] = module.params['audit_log']
    if module.params['service_log'] is not None:
        params['service_log'] = module.params['service_log']
    if module.params['dns_log'] is not None:
        params['dns_log'] = module.params['dns_log']
    if module.params['match_type'] is not None:
        params['match_type'] = module.params['match_type']
    if module.params['level_filter'] is not None:
        params['level_filter'] = module.params['level_filter']
    if module.params['event_list'] is not None:
        params['event_list'] = module.params['event_list']
    if module.params['keyword_filter'] is not None:
        params['keyword_filter'] = module.params['keyword_filter']
    if module.params['module_filter'] is not None:
        params['module_filter'] = module.params['module_filter']
    if module.params['keyword_type'] is not None:
        params['keyword_type'] = module.params['keyword_type']

    # Make API call
    response = send_request(url, params, method='POST')

    # Format response
    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': 'Syslog server edited successfully'}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "编辑syslog服务器失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据，不尝试解析为JSON格式
            return True, {'response': response}
    else:
        # 直接返回原始响应，不尝试解析为JSON格式
        return True, {'response': response if response is not None else 'No response data'}


def log_syslog_server_del(module):
    """Delete syslog server configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.syslog.server.del" % (
        ip, authkey)

    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['host'] is not None:
        params['host'] = module.params['host']
    else:
        module.fail_json(msg="host is required for delete action")

    if module.params['port'] is not None:
        params['port'] = module.params['port']
    else:
        module.fail_json(msg="port is required for delete action")

    # Make API call
    response = send_request(url, params, method='POST')

    # Format response
    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': 'Syslog server deleted successfully'}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "删除syslog服务器失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据，不尝试解析为JSON格式
            return True, {'response': response}
    else:
        # 直接返回原始响应，不尝试解析为JSON格式
        return True, {'response': response if response is not None else 'No response data'}


def main():
    # Define module arguments
    argument_spec = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
                    'log_syslog_server_add', 'log_syslog_server_list', 'log_syslog_server_get', 'log_syslog_server_edit', 'log_syslog_server_del']),
        # Parameters for add/edit actions
        host=dict(type='str'),
        port=dict(type='int'),
        log_code=dict(type='int', choices=[0, 1]),
        facility=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6, 7]),
        nat_log=dict(type='int', choices=[0, 1]),
        audit_log=dict(type='int', choices=[0, 1]),
        service_log=dict(type='int', choices=[0, 1]),
        dns_log=dict(type='int', choices=[0, 1]),
        match_type=dict(type='int', choices=[0, 1, 2]),
        level_filter=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6, 7]),
        event_list=dict(type='list', elements='int'),
        keyword_filter=dict(type='str'),
        module_filter=dict(type='str'),
        keyword_type=dict(type='str', choices=['string', 'regular']),
    )

    # Create Ansible module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ('action', 'add', ['host', 'port']),
            ('action', 'get', ['host', 'port']),
            ('action', 'edit', ['host', 'port']),
            ('action', 'delete', ['host', 'port']),
        ]
    )

    # Extract module parameters
    action = str(module.params['action'])

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(changed=False)

    try:
        # Perform requested action
        if action == 'log_syslog_server_add':
            changed, result = log_syslog_server_add(module)
        elif action == 'log_syslog_server_list':
            changed, result = log_syslog_server_list(module)
        elif action == 'log_syslog_server_get':
            changed, result = log_syslog_server_get(module)
        elif action == 'log_syslog_server_edit':
            changed, result = log_syslog_server_edit(module)
        elif action == 'log_syslog_server_del':
            changed, result = log_syslog_server_del(module)


        # Exit with result
        if changed:
            module.exit_json(changed=True, **result)
        else:
            module.fail_json(msg=result.get('msg', 'Unknown error'))

    except Exception as e:
        module.fail_json(msg="An error occurred: %s" % str(e))


if __name__ == '__main__':
    main()
    main()
