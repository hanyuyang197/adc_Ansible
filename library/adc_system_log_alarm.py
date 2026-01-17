#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Horizon Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
            # 如果不是有效的JSON格式，返回原始响应
            return {
                'result': 'error',
                'errcode': 'JSON_PARSE_ERROR',
                'errmsg': f'响应不是有效的JSON格式: {response_text}'
            }

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


def log_alarm_email_get(module):
    """Get email alarm configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.alarm.email.get" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')

    if isinstance(result, dict):
        if result.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'email_config': result.get('data', {})}
        elif 'errcode' in result and result['errcode']:
            # 错误响应
            return False, {'msg': "获取邮件告警配置失败: %s" % result.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'email_config': result}
    else:
        return False, {'msg': '响应数据格式错误'}


def log_alarm_email_set(module):
    """Set email alarm configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.alarm.email.set" % (
        ip, authkey)

    # Prepare parameters
    params = {}

    # Add optional parameters if provided
    if module.params['delay_send_buff'] is not None:
        params['delay_send_buff'] = module.params['delay_send_buff']
    if module.params['delay_send_time'] is not None:
        params['delay_send_time'] = module.params['delay_send_time']
    if module.params['send_event'] is not None:
        params['send_event'] = module.params['send_event']
    if module.params['send_level'] is not None:
        params['send_level'] = module.params['send_level']

    # 发送POST请求
    result = send_request(url, params, method='POST')

    # 使用通用响应解析函数
    if isinstance(result, dict):
        if result.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': '邮件告警配置设置成功'}
        elif 'errcode' in result and result['errcode']:
            # 错误响应
            return False, {'msg': "设置邮件告警配置失败: %s" % result.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'response': result}
    else:
        return False, {'msg': '响应数据格式错误'}


def log_alarm_sms_get(module):
    """Get SMS alarm configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.alarm.sms.get" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')

    if isinstance(result, dict):
        if result.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'sms_config': result.get('data', {})}
        elif 'errcode' in result and result['errcode']:
            # 错误响应
            return False, {'msg': "获取短信告警配置失败: %s" % result.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'sms_config': result}
    else:
        return False, {'msg': '响应数据格式错误'}


def log_alarm_sms_set(module):
    """Set SMS alarm configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.alarm.sms.set" % (
        ip, authkey)

    # Prepare parameters
    params = {}

    # Add optional parameters if provided
    if module.params['url'] is not None:
        params['url'] = module.params['url']
    if module.params['send_event'] is not None:
        params['send_event'] = module.params['send_event']
    if module.params['send_level'] is not None:
        params['send_level'] = module.params['send_level']

    # 发送POST请求
    result = send_request(url, params, method='POST')

    # 使用通用响应解析函数
    if isinstance(result, dict):
        if result.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': '短信告警配置设置成功'}
        elif 'errcode' in result and result['errcode']:
            # 错误响应
            return False, {'msg': "设置短信告警配置失败: %s" % result.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'response': result}
    else:
        return False, {'msg': '响应数据格式错误'}


def main():
    # Define module arguments
    argument_spec = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
                    'log_alarm_email_get', 'log_alarm_email_set',
                    'log_alarm_sms_get', 'log_alarm_sms_set']),
        # Parameters for email alarm configuration
        delay_send_buff=dict(type='int'),
        delay_send_time=dict(type='int'),
        send_event=dict(type='list', elements='int'),
        send_level=dict(type='int', choices=[-1, 0, 1, 2, 5]),
        # Parameters for SMS alarm configuration
        url=dict(type='str'),
    )

    # Create Ansible module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    # Extract module parameters
    action = str(module.params['action'])

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(changed=False)

    try:
        # Perform requested action
        if action == 'log_alarm_email_get':
            changed, result = log_alarm_email_get(module)
        elif action == 'log_alarm_email_set':
            changed, result = log_alarm_email_set(module)
        elif action == 'log_alarm_sms_get':
            changed, result = log_alarm_sms_get(module)
        elif action == 'log_alarm_sms_set':
            changed, result = log_alarm_sms_set(module)


        # Exit with result
        if 'msg' in result and '失败' in result['msg']:
            module.fail_json(msg=result['msg'])
        else:
            module.exit_json(changed=changed, **result)

    except Exception as e:
        module.fail_json(msg="An error occurred: %s" % str(e))


if __name__ == '__main__':
    main()
