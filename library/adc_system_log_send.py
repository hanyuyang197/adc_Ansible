#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Horizon Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
import json
import sys
__metaclass__ = type

# ADC API响应解析函数


def format_adc_response_for_ansible(response_data, action="", changed_default=True):
    """
    格式化ADC响应为Ansible模块返回格式

    Args:
        response_data (str/dict): API响应数据
        action (str): 执行的操作名称
        changed_default (bool): 默认的changed状态

    Returns:
        tuple: (success, result_dict)
            - success (bool): 操作是否成功
            - result_dict (dict): Ansible模块返回字典
    """

    # 初始化返回结果
    result = {
        'success': False,
        'result': '',
        'errcode': '',
        'errmsg': '',
        'data': {}
    }

    try:
        # 如果是字符串，尝试解析为JSON
        if isinstance(response_data, str):
            parsed_data = json.loads(response_data)
        else:
            parsed_data = response_data

        result['data'] = parsed_data

        # 提取基本字段
        result['result'] = parsed_data.get('result', '')
        result['errcode'] = parsed_data.get('errcode', '')
        result['errmsg'] = parsed_data.get('errmsg', '')

        # 判断操作是否成功
        if result['result'].lower() == 'success':
            result['success'] = True
        else:
            # 处理幂等性问题 - 检查错误信息中是否包含"已存在"等表示已存在的关键词
            errmsg = result['errmsg'].lower() if isinstance(
                result['errmsg'], str) else str(result['errmsg']).lower()
            if any(keyword in errmsg for keyword in ['已存在', 'already exists', 'already exist', 'exists']):
                # 幂等性处理：如果是因为已存在而导致的"失败"，实际上算成功
                result['success'] = True
                result['result'] = 'success (already exists)'

    except json.JSONDecodeError as e:
        result['errmsg'] = "JSON解析失败: %s" % str(e)
        result['errcode'] = 'JSON_PARSE_ERROR'
    except Exception as e:
        result['errmsg'] = "响应解析异常: %s" % str(e)
        result['errcode'] = 'PARSE_EXCEPTION'

    # 格式化为Ansible返回格式
    if result['success']:
        # 操作成功
        result_dict = {
            'changed': changed_default,
            'msg': '%s操作成功' % action if action else '操作成功',
            'response': result['data']
        }

        # 如果是幂等性成功（已存在），调整消息
        if 'already exists' in result['result']:
            result_dict['changed'] = False
            result_dict['msg'] = '%s操作成功（资源已存在，无需更改）' % action if action else '操作成功（资源已存在，无需更改）'

        return True, result_dict
    else:
        # 操作失败
        result_dict = {
            'changed': False,
            'msg': '%s操作失败' % action if action else '操作失败',
            'error': {
                'result': result['result'],
                'errcode': result['errcode'],
                'errmsg': result['errmsg']
            },
            'response': result['data']
        }
        return False, result_dict


def send_request(url, data=None, method='GET'):
    """发送HTTP请求到ADC设备"""
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

        result = json.loads(response_text)

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
        # 如果JSON解析失败，直接返回原始响应数据
        return {
            'result': 'success',
            'data': str(response_data) if response_data is not None else '',
            'raw_response': True
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


def adc_add_syslog_server(module, adc_base):
    """Add syslog server configuration"""
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
    response = adc_base.make_request(
        'POST', 'log.syslog.server.add', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Add syslog server", True)
    return success, result_dict


def adc_list_syslog_servers(module, adc_base):
    """List syslog server configurations"""
    # Make API call
    response = adc_base.make_request('GET', 'log.syslog.server.list')

    if response.get('success'):
        return True, {'servers': response.get('data', [])}
    else:
        return False, {'msg': response.get('msg', 'Failed to list syslog servers')}


def adc_get_syslog_server(module, adc_base):
    """Get specific syslog server configuration"""
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
    response = adc_base.make_request(
        'POST', 'log.syslog.server.get', data=params)

    if response.get('success'):
        return True, {'server': response.get('data', {})}
    else:
        return False, {'msg': response.get('msg', 'Failed to get syslog server')}


def adc_edit_syslog_server(module, adc_base):
    """Edit syslog server configuration"""
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
    response = adc_base.make_request(
        'POST', 'log.syslog.server.edit', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Edit syslog server", True)
    return success, result_dict


def adc_delete_syslog_server(module, adc_base):
    """Delete syslog server configuration"""
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
    response = adc_base.make_request(
        'POST', 'log.syslog.server.del', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Delete syslog server", True)
    return success, result_dict


def main():
    # Define module arguments
    argument_spec = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
                    'add', 'list', 'get', 'edit', 'delete']),
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

    # Create ADC base object
    adc_base = ADCBase(module)

    try:
        # Perform requested action
        if action == 'add':
            changed, result = adc_add_syslog_server(module, adc_base)
        elif action == 'list':
            changed, result = adc_list_syslog_servers(module, adc_base)
        elif action == 'get':
            changed, result = adc_get_syslog_server(module, adc_base)
        elif action == 'edit':
            changed, result = adc_edit_syslog_server(module, adc_base)
        elif action == 'delete':
            changed, result = adc_delete_syslog_server(module, adc_base)
        else:
            module.fail_json(msg="Unsupported action: %s" % action)

        # Exit with result
        if changed:
            module.exit_json(changed=True, **result)
        else:
            module.fail_json(msg=result.get('msg', 'Unknown error'))

    except Exception as e:
        module.fail_json(msg="An error occurred: %s" % str(e))


if __name__ == '__main__':
    main()
