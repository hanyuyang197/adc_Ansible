#!/usr/bin/python
# -*- coding: utf-8 -*-

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
# Python 2/3兼容性处理
try:
    # Python 2
    import urllib2 as urllib_request
except ImportError:
    # Python 3
    import urllib.request as urllib_request
    import urllib.error as urllib_error

DOCUMENTATION = '''
---
module: adc_waf_profile
short_description: Manage ADC WAF Profiles
description:
    - Manage ADC WAF Profiles including add, list, get, edit, and delete operations
version_added: "2.4"
options:
    ip:
        description:
            - The IP address of the ADC device
        required: true
    authkey:
        description:
            - The authentication key for the ADC device
        required: true
    action:
        description:
            - The action to perform (add_profile, list_profiles, get_profile, edit_profile, delete_profile)
        required: true
        choices: ['add_profile', 'list_profiles', 'get_profile', 'edit_profile', 'delete_profile']
    name:
        description:
            - The name of the WAF profile
        required: false
    rule_name:
        description:
            - The rule name for the WAF profile
        required: false
    white_url_list:
        description:
            - List of white URL patterns
        required: false
    black_url_list:
        description:
            - List of black URL patterns
        required: false
    uri_stick_check:
        description:
            - URI stick check setting
        required: false
    mode:
        description:
            - WAF mode
        required: false
    behavior:
        description:
            - WAF behavior
        required: false
    enable:
        description:
            - Enable status
        required: false
    logging:
        description:
            - Logging status
        required: false
    injection_sql:
        description:
            - SQL injection protection
        required: false
    injection_xss:
        description:
            - XSS injection protection
        required: false
    disable_len_check:
        description:
            - Disable length check
        required: false
    headers_mlen:
        description:
            - Maximum header length
        required: false
    url_mlen:
        description:
            - Maximum URL length
        required: false
    cookie_mlen:
        description:
            - Maximum cookie length
        required: false
author:
    - Your Name
'''

EXAMPLES = '''
# Add a WAF profile
- adc_waf_profile:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_profile"
    name: "my_waf_profile"
    rule_name: "wrule_123.txt"
    white_url_list: ["^/"]
    black_url_list: ["^/"]
    uri_stick_check: 1
    mode: 2
    behavior: 1

# List all WAF profiles
- adc_waf_profile:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "list_profiles"

# Get a specific WAF profile
- adc_waf_profile:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "get_profile"
    name: "my_waf_profile"

# Edit a WAF profile
- adc_waf_profile:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "edit_profile"
    name: "my_waf_profile"
    mode: 3

# Delete a WAF profile
- adc_waf_profile:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_profile"
    name: "my_waf_profile"
'''

RETURN = '''
result:
    description: The response from the ADC device
    returned: success
    type: dict
'''


def send_request(url, data=None, method='GET'):
    """Send HTTP request to ADC device"""
    response_data = None
    try:
        if method == 'POST' and data:
            data_json = json.dumps(data)
            data_bytes = data_json.encode('utf-8')
            req = urllib_request.Request(url, data=data_bytes)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib_request.Request(url)

        if method == 'POST':
            req.get_method = lambda: 'POST'
        elif method == 'PUT':
            req.get_method = lambda: 'PUT'
        elif method == 'DELETE':
            req.get_method = lambda: 'DELETE'

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


def adc_list_waf_profiles(module):
    """List all WAF profiles"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.list" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_list_waf_profiles_withcommon(module):
    """List all WAF profiles with common partitions"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.list.withcommon" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_get_waf_profile(module):
    """Get a specific WAF profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "获取WAF模板需要提供name参数"}

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.get" % (
        ip, authkey)

    data = {
        "name": name
    }

    result = send_request(url, data, method='POST')
    return result


def adc_add_waf_profile(module):
    """Add a WAF profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "添加WAF模板需要提供name参数"}

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.add" % (
        ip, authkey)

    # 构造WAF配置数据 - 只包含在YAML中明确定义的参数
    profile_data = {
        "name": name
    }

    # 添加可选参数（只包含实际定义的参数）
    if 'rule_name' in module.params and module.params['rule_name'] is not None:
        profile_data["rule_name"] = module.params['rule_name']
    if 'white_url_list' in module.params and module.params['white_url_list'] is not None:
        profile_data["white_url_list"] = module.params['white_url_list']
    if 'black_url_list' in module.params and module.params['black_url_list'] is not None:
        profile_data["black_url_list"] = module.params['black_url_list']
    if 'uri_stick_check' in module.params and module.params['uri_stick_check'] is not None:
        profile_data["uri_stick_check"] = module.params['uri_stick_check']
    if 'mode' in module.params and module.params['mode'] is not None:
        profile_data["mode"] = module.params['mode']
    if 'behavior' in module.params and module.params['behavior'] is not None:
        profile_data["behavior"] = module.params['behavior']
    if 'enable' in module.params and module.params['enable'] is not None:
        profile_data["enable"] = module.params['enable']
    if 'logging' in module.params and module.params['logging'] is not None:
        profile_data["logging"] = module.params['logging']
    if 'injection_sql' in module.params and module.params['injection_sql'] is not None:
        profile_data["injection_sql"] = module.params['injection_sql']
    if 'injection_xss' in module.params and module.params['injection_xss'] is not None:
        profile_data["injection_xss"] = module.params['injection_xss']
    if 'disable_len_check' in module.params and module.params['disable_len_check'] is not None:
        profile_data["disable_len_check"] = module.params['disable_len_check']
    if 'headers_mlen' in module.params and module.params['headers_mlen'] is not None:
        profile_data["headers_mlen"] = module.params['headers_mlen']
    if 'url_mlen' in module.params and module.params['url_mlen'] is not None:
        profile_data["url_mlen"] = module.params['url_mlen']
    if 'cookie_mlen' in module.params and module.params['cookie_mlen'] is not None:
        profile_data["cookie_mlen"] = module.params['cookie_mlen']

    result = send_request(url, profile_data, method='POST')
    return result


def adc_edit_waf_profile(module):
    """Edit a WAF profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "编辑WAF模板需要提供name参数"}

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.edit" % (
        ip, authkey)

    # 构造WAF配置数据 - 只包含在YAML中明确定义的参数
    profile_data = {
        "name": name
    }

    # 添加可选参数（只包含实际定义的参数）
    if 'rule_name' in module.params and module.params['rule_name'] is not None:
        profile_data["rule_name"] = module.params['rule_name']
    if 'white_url_list' in module.params and module.params['white_url_list'] is not None:
        profile_data["white_url_list"] = module.params['white_url_list']
    if 'black_url_list' in module.params and module.params['black_url_list'] is not None:
        profile_data["black_url_list"] = module.params['black_url_list']
    if 'uri_stick_check' in module.params and module.params['uri_stick_check'] is not None:
        profile_data["uri_stick_check"] = module.params['uri_stick_check']
    if 'mode' in module.params and module.params['mode'] is not None:
        profile_data["mode"] = module.params['mode']
    if 'behavior' in module.params and module.params['behavior'] is not None:
        profile_data["behavior"] = module.params['behavior']
    if 'enable' in module.params and module.params['enable'] is not None:
        profile_data["enable"] = module.params['enable']
    if 'logging' in module.params and module.params['logging'] is not None:
        profile_data["logging"] = module.params['logging']
    if 'injection_sql' in module.params and module.params['injection_sql'] is not None:
        profile_data["injection_sql"] = module.params['injection_sql']
    if 'injection_xss' in module.params and module.params['injection_xss'] is not None:
        profile_data["injection_xss"] = module.params['injection_xss']
    if 'disable_len_check' in module.params and module.params['disable_len_check'] is not None:
        profile_data["disable_len_check"] = module.params['disable_len_check']
    if 'headers_mlen' in module.params and module.params['headers_mlen'] is not None:
        profile_data["headers_mlen"] = module.params['headers_mlen']
    if 'url_mlen' in module.params and module.params['url_mlen'] is not None:
        profile_data["url_mlen"] = module.params['url_mlen']
    if 'cookie_mlen' in module.params and module.params['cookie_mlen'] is not None:
        profile_data["cookie_mlen"] = module.params['cookie_mlen']

    result = send_request(url, profile_data, method='POST')
    return result


def adc_delete_waf_profile(module):
    """Delete a WAF profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "删除WAF模板需要提供name参数"}

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.del" % (
        ip, authkey)

    data = {
        "name": name
    }

    result = send_request(url, data, method='POST')
    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(type='str', required=True),
            authkey=dict(type='str', required=True, no_log=True),
            action=dict(type='str', required=True, choices=[
                'add_profile', 'list_profiles', 'list_profiles_withcommon', 'get_profile', 'edit_profile', 'delete_profile'
            ]),
            name=dict(type='str', required=False),
            rule_name=dict(type='str', required=False),
            white_url_list=dict(type='list', required=False),
            black_url_list=dict(type='list', required=False),
            uri_stick_check=dict(type='int', required=False),
            mode=dict(type='int', required=False),
            behavior=dict(type='int', required=False),
            enable=dict(type='int', required=False),
            logging=dict(type='int', required=False),
            injection_sql=dict(type='int', required=False),
            injection_xss=dict(type='int', required=False),
            disable_len_check=dict(type='int', required=False),
            headers_mlen=dict(type='int', required=False),
            url_mlen=dict(type='int', required=False),
            cookie_mlen=dict(type='int', required=False),
        ),
        supports_check_mode=False
    )

    action = module.params['action']

    if action == 'list_profiles':
        result = adc_list_waf_profiles(module)
    elif action == 'list_profiles_withcommon':
        result = adc_list_waf_profiles_withcommon(module)
    elif action == 'get_profile':
        result = adc_get_waf_profile(module)
    elif action == 'add_profile':
        result = adc_add_waf_profile(module)
    elif action == 'edit_profile':
        result = adc_edit_waf_profile(module)
    elif action == 'delete_profile':
        result = adc_delete_waf_profile(module)
    else:
        module.fail_json(msg="Unknown action: %s" % action)

    # 统一使用标准的ADC响应格式处理结果
    # 成功响应: {"result":"success"} 或直接返回数据
    # 错误响应: {"result":"error","errcode":"...","errmsg":"..."}
    if isinstance(result, dict):
        if result.get('result', '').lower() == 'success':
            # 成功响应
            success, result_dict = format_adc_response_for_ansible(
                result, action, True)
            if success:
                module.exit_json(**result_dict)
            else:
                module.fail_json(**result_dict)
        elif 'errcode' in result and result['errcode']:
            # 错误响应 - 修复Unicode解码错误
            try:
                error_msg = result.get('errmsg', '未知错误')
                # 确保错误消息正确处理Unicode字符
                if isinstance(error_msg, bytes):
                    try:
                        error_msg = error_msg.decode('utf-8')
                    except UnicodeDecodeError:
                        error_msg = error_msg.decode('latin1')
                formatted_msg = "操作失败: %s" % error_msg
            except Exception:
                formatted_msg = "操作失败: 未知错误"

            module.fail_json(msg=formatted_msg, result=result)
        else:
            # 查询类API直接返回数据
            success, result_dict = format_adc_response_for_ansible(
                result, action, False)
            if success:
                module.exit_json(**result_dict)
            else:
                module.fail_json(**result_dict)
    elif isinstance(result, list):
        # 列表类型直接返回
        success, result_dict = format_adc_response_for_ansible(
            result, action, False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        # 其他类型也直接返回
        success, result_dict = format_adc_response_for_ansible(
            result, action, True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)


if __name__ == '__main__':
    main()
