#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
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
    - Manage ADC WAF Profiles including list and get operations
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
            - The action to perform (list_profiles, get_profile)
        required: true
        choices: ['list_profiles', 'get_profile']
    name:
        description:
            - The name of the WAF profile
        required: false
author:
    - Your Name
'''

EXAMPLES = '''
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
'''

RETURN = '''
result:
    description: The response from the ADC device
    returned: success
    type: dict
'''


def send_request(url, data=None, method='GET'):
    """Send HTTP request to ADC device"""
    try:
        if method == 'POST' and data:
            data_json = json.dumps(data)
            data_bytes = data_json.encode('utf-8')
            req = urllib_request.Request(url, data=data_bytes)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib_request.Request(url)

        response = urllib_request.urlopen(req)
        result = json.loads(response.read())

        # 标准化响应格式
        # 成功响应保持原样
        # 错误响应标准化为 {"result":"error","errcode":"REQUEST_ERROR","errmsg":"..."}
        if isinstance(result, dict) and 'status' in result and result['status'] is False:
            return {
                'result': 'error',
                'errcode': 'REQUEST_ERROR',
                'errmsg': result.get('msg', '请求失败')
            }
        else:
            return result
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(type='str', required=True),
            authkey=dict(type='str', required=True),
            action=dict(type='str', required=True, choices=[
                'list_profiles', 'get_profile'
            ]),
            name=dict(type='str', required=False),
        ),
        supports_check_mode=False
    )

    action = module.params['action']

    if action == 'list_profiles':
        result = adc_list_waf_profiles(module)
    elif action == 'get_profile':
        result = adc_get_waf_profile(module)
    else:
        module.fail_json(msg="Unknown action: %s" % action)

    # 统一使用标准的ADC响应格式处理结果
    # 成功响应: {"result":"success"} 或直接返回数据
    # 错误响应: {"result":"error","errcode":"...","errmsg":"..."}
    if isinstance(result, dict):
        if result.get('result', '').lower() == 'success':
            # 成功响应
            module.exit_json(changed=True, result=result)
        elif 'errcode' in result and result['errcode']:
            # 错误响应
            module.fail_json(msg="操作失败: %s" %
                             result.get('errmsg', '未知错误'), result=result)
        else:
            # 查询类API直接返回数据
            module.exit_json(changed=False, result=result)
    elif isinstance(result, list):
        # 列表类型直接返回
        module.exit_json(changed=False, result=result)
    else:
        # 其他类型也直接返回
        module.exit_json(changed=False, result=result)


if __name__ == '__main__':
    main()
