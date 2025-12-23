#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Horizon Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
import json
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
    import sys
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
module: adc_system_log_get
short_description: Manage ADC system log retrieval
description:
  - Retrieve various types of logs from ADC devices.
  - Supports service logs, audit logs, NAT logs, DNS logs.
  - Supports listing, clearing, and downloading logs.
version_added: "1.0.0"
options:
  action:
    description:
      - The action to perform on logs.
      - C(list) to list logs.
      - C(clear) to clear logs.
      - C(download) to download logs.
    type: str
    required: true
    choices: [ list, clear, download ]
  log_type:
    description:
      - The type of log to operate on.
    type: str
    required: true
    choices: [ service, audit, nat, dns, coredump, system ]
  # Options for list action
  direct:
    description:
      - Log pagination direction.
      - 0:first, 1:prev, 2:next, 3:last
    type: int
    choices: [0, 1, 2, 3]
    default: 0
  index:
    description:
      - Log index for pagination.
    type: int
    default: 0
  limit:
    description:
      - Output limit for logs.
    type: int
    default: 30
  level:
    description:
      - Output logs at this level and above.
      - 0: emergency, 1: alert, 2: critical, 3: error, 4: warning, 5: notification, 6: information, 7: debugging
    type: int
    choices: [0, 1, 2, 3, 4, 5, 6, 7]
    default: 7
  # Options for audit log list
  start_time:
    description:
      - Filter logs by start time (seconds since epoch).
    type: int
    default: 0
  time_range:
    description:
      - Filter logs by time range (seconds).
    type: int
    default: 0
  user_name:
    description:
      - Filter audit logs by username.
    type: str
author:
  - Horizon Inc.
'''

EXAMPLES = r'''
- name: Get service logs
  adc_system_log_get:
    action: list
    log_type: service
    direct: 0
    index: 0
    limit: 10
    level: 7

- name: Get audit logs for user
  adc_system_log_get:
    action: list
    log_type: audit
    user_name: admin
    limit: 20

- name: Clear NAT logs
  adc_system_log_get:
    action: clear
    log_type: nat

- name: Download DNS logs
  adc_system_log_get:
    action: download
    log_type: dns
'''

RETURN = r'''
logs:
  description: List of logs when action=list
  returned: when action=list
  type: list
  sample: [
    {
      "index": 254,
      "item": "Oct 25 2024 14:48:58 local0.info Horizon/common/ lldp: add neighbor for Ethernet6/0..."
    }
  ]
result:
  description: Result message when action=clear
  returned: when action=clear
  type: str
  sample: "Logs cleared successfully"
file_path:
  description: Path to downloaded file when action=download
  returned: when action=download
  type: str
  sample: "/tmp/service_logs.txt"
'''


def list_logs(module, adc_base, log_type):
    """List logs of specified type"""
    # Prepare the action based on log type
    action_map = {
        'service': 'log.service.list',
        'audit': 'log.audit.list',
        'nat': 'log.nat.list',
        'dns': 'log.dns.list'
    }

    if log_type not in action_map:
        module.fail_json(
            msg="Unsupported log type for list action: %s" % log_type)

    # Prepare parameters
    params = {
        'direct': module.params['direct'],
        'index': module.params['index'],
        'limit': module.params['limit']
    }

    # Add type-specific parameters
    if log_type == 'service':
        params['level'] = module.params['level']
    elif log_type == 'audit':
        params['start_time'] = module.params['start_time']
        params['time_range'] = module.params['time_range']
        params['user_name'] = module.params['user_name']

    # Make API call
    response = adc_base.make_request('POST', action_map[log_type], data=params)

    if response.get('success'):
        return True, {'logs': response.get('data', [])}
    else:
        return False, {'msg': response.get('msg', 'Failed to list logs')}


def clear_logs(module, adc_base, log_type):
    """Clear logs of specified type"""
    # Prepare the action based on log type
    action_map = {
        'service': 'log.service.clear',
        'audit': 'log.audit.clear',
        'nat': 'log.nat.clear',
        'dns': 'log.dns.clear'
    }

    if log_type not in action_map:
        module.fail_json(
            msg="Unsupported log type for clear action: %s" % log_type)

    # Make API call
    response = adc_base.make_request('GET', action_map[log_type])

    if response.get('success'):
        return True, {'result': 'Logs cleared successfully'}
    else:
        return False, {'msg': response.get('msg', 'Failed to clear logs')}


def download_logs(module, adc_base, log_type):
    """Download logs of specified type"""
    # Prepare the action based on log type
    action_map = {
        'service': 'log.service.download',
        'audit': 'log.audit.download',
        'nat': 'log.nat.download',
        'dns': 'log.dns.download',
        'coredump': 'log.coredump.download',
        'system': 'log.system.download'
    }

    if log_type not in action_map:
        module.fail_json(
            msg="Unsupported log type for download action: %s" % log_type)

    # Make API call to download file
    file_path = "/tmp/%s_logs.txt" % log_type
    success = adc_base.download_file(action_map[log_type], file_path)

    if success:
        return True, {'file_path': file_path}
    else:
        return False, {'msg': 'Failed to download logs'}


def main():
    # Define module arguments
    argument_spec = dict(
        action=dict(type='str', required=True, choices=[
                    'list', 'clear', 'download']),
        log_type=dict(type='str', required=True, choices=[
                      'service', 'audit', 'nat', 'dns', 'coredump', 'system']),
        # Options for list action
        direct=dict(type='int', choices=[0, 1, 2, 3], default=0),
        index=dict(type='int', default=0),
        limit=dict(type='int', default=30),
        level=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6, 7], default=7),
        # Options for audit log list
        start_time=dict(type='int', default=0),
        time_range=dict(type='int', default=0),
        user_name=dict(type='str'),
    )

    # Create Ansible module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ('log_type', 'audit', ['user_name'], True),
        ]
    )

    # Extract module parameters
    action = module.params['action']
    log_type = module.params['log_type']

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(changed=False)

    # Create ADC base object
    adc_base = ADCBase(module)

    try:
        # Perform requested action
        if action == 'list':
            changed, result = list_logs(module, adc_base, log_type)
        elif action == 'clear':
            changed, result = clear_logs(module, adc_base, log_type)
        elif action == 'download':
            changed, result = download_logs(module, adc_base, log_type)
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
