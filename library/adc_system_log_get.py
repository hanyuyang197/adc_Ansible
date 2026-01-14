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


def list_logs(module):
    """List logs of specified type"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # Prepare the action based on log type
    action_map = {
        'service': 'log.service.list',
        'audit': 'log.audit.list',
        'nat': 'log.nat.list',
        'dns': 'log.dns.list'
    }

    log_type = module.params['log_type']
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

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=%s" % (
        ip, authkey, action_map[log_type])

    # Make API call
    response = send_request(url, params, method='POST')

    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'logs': response.get('data', [])}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "获取日志失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据，不尝试解析为JSON格式
            return True, {'logs': response}
    else:
        # 直接返回原始响应，不尝试解析为JSON格式
        return True, {'logs': response if response is not None else 'No response data'}


def clear_logs(module):
    """Clear logs of specified type"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # Prepare the action based on log type
    action_map = {
        'service': 'log.service.clear',
        'audit': 'log.audit.clear',
        'nat': 'log.nat.clear',
        'dns': 'log.dns.clear'
    }

    log_type = module.params['log_type']
    if log_type not in action_map:
        module.fail_json(
            msg="Unsupported log type for clear action: %s" % log_type)

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=%s" % (
        ip, authkey, action_map[log_type])

    # Make API call
    response = send_request(url, method='GET')

    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'result': '日志清除成功'}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "清除日志失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据，不尝试解析为JSON格式
            return True, {'response': response}
    else:
        # 直接返回原始响应，不尝试解析为JSON格式
        return True, {'response': response if response is not None else 'No response data'}


def download_logs(module):
    """Download logs of specified type"""
    import sys
    import os
    ip = module.params['ip']
    authkey = module.params['authkey']

    # Prepare the action based on log type
    action_map = {
        'service': 'log.service.download',
        'audit': 'log.audit.download',
        'nat': 'log.nat.download',
        'dns': 'log.dns.download',
        'coredump': 'log.coredump.download',
        'system': 'log.system.download'
    }

    log_type = module.params['log_type']
    if log_type not in action_map:
        module.fail_json(
            msg="Unsupported log type for download action: %s" % log_type)

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=%s" % (
        ip, authkey, action_map[log_type])

    # 实际下载文件
    try:
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            response = urllib_request.urlopen(url)
        else:
            # Python 2
            import urllib2 as urllib_request
            response = urllib_request.urlopen(url)

        # 读取响应内容（二进制数据）
        content = response.read()

        # 生成本地文件路径 - 使用.tar.gz扩展名
        import tempfile
        import time
        timestamp = int(time.time())
        file_path = os.path.join(
            tempfile.gettempdir(), f"{log_type}_logs_{timestamp}.tar.gz")

        # 以二进制模式写入文件
        with open(file_path, 'wb') as f:
            f.write(content)

        # 返回下载结果
        return True, {
            'file_path': file_path,
            'download_url': url,
            'file_size': len(content),
            'msg': f'日志文件已下载并保存到 {file_path}'
        }
    except Exception as e:
        return False, {'msg': f'下载日志文件失败: {str(e)}'}


def main():
    # Define module arguments
    argument_spec = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
                    'log_service_list', 'log_audit_list', 'log_nat_list', 'log_dns_list',
                    'log_service_clear', 'log_audit_clear', 'log_nat_clear', 'log_dns_clear',
                    'log_service_download', 'log_audit_download', 'log_nat_download', 'log_dns_download',
                    'log_coredump_download', 'log_system_download']),
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
            ('action', 'log_audit_list', ['user_name'], True),
        ]
    )

    # Extract module parameters
    action = module.params['action']

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(changed=False)

    try:
        # Perform requested action
        if action in ['log_service_list', 'log_audit_list', 'log_nat_list', 'log_dns_list']:
            changed, result = list_logs(module)
        elif action in ['log_service_clear', 'log_audit_clear', 'log_nat_clear', 'log_dns_clear']:
            changed, result = clear_logs(module)
        elif action in ['log_service_download', 'log_audit_download', 'log_nat_download', 'log_dns_download', 'log_coredump_download', 'log_system_download']:
            changed, result = download_logs(module)


        # Exit with result
        if changed:
            module.exit_json(changed=True, **result)
        else:
            module.fail_json(msg=result.get('msg', 'Unknown error'))

    except Exception as e:
        module.fail_json(msg="An error occurred: %s" % str(e))


if __name__ == '__main__':
    main()
