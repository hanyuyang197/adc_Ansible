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


def adc_get_email_alarm_config(module):
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


def adc_set_email_alarm_config(module):
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


def adc_get_sms_alarm_config(module):
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


def adc_set_sms_alarm_config(module):
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
        alarm_type=dict(type='str', required=True, choices=['email', 'sms']),
        action=dict(type='str', required=True, choices=['get', 'set']),
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
    alarm_type = str(module.params['alarm_type'])
    action = str(module.params['action'])

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(changed=False)

    try:
        # Perform requested action based on alarm type
        if alarm_type == 'email':
            if action == 'get':
                changed, result = adc_get_email_alarm_config(module)
            elif action == 'set':
                changed, result = adc_set_email_alarm_config(module)
            else:
                module.fail_json(
                    msg="Unsupported action for email alarm: %s" % action)
        elif alarm_type == 'sms':
            if action == 'get':
                changed, result = adc_get_sms_alarm_config(module)
            elif action == 'set':
                changed, result = adc_set_sms_alarm_config(module)
            else:
                module.fail_json(
                    msg="Unsupported action for SMS alarm: %s" % action)
        else:
            module.fail_json(msg="Unsupported alarm type: %s" % alarm_type)

        # Exit with result
        if changed:
            module.exit_json(changed=True, **result)
        else:
            module.fail_json(msg=result.get('msg', 'Unknown error'))

    except Exception as e:
        module.fail_json(msg="An error occurred: %s" % str(e))


if __name__ == '__main__':
    main()
