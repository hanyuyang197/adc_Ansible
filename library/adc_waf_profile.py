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
try:
    # Python 2
except ImportError:

DOCUMENTATION = '''
---
module: adc_waf_profile
short_description: Manage ADC WAF Profiles
description:
    - Manage ADC WAF Profiles including add, edit, delete, list and get operations
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
            - The action to perform (add_profile, edit_profile, delete_profile, list_profiles, get_profile)
        required: true
        choices: ['add_profile', 'edit_profile', 'delete_profile', 'list_profiles', 'get_profile']
    name:
        description:
            - The name of the WAF profile
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
    enable: 1
    logging: 1
    injection_sql: 1
    injection_xss: 1
    disable_len_check: 0
    headers_mlen: 8192
    url_mlen: 2803
    cookie_mlen: 4079

# Edit a WAF profile
- adc_waf_profile:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "edit_profile"
    name: "my_waf_profile"
    rule_name: "wrule_123.txt"
    white_url_list: ["^/"]
    black_url_list: ["^/"]
    uri_stick_check: 1
    mode: 2
    behavior: 1
    enable: 1
    logging: 1
    injection_sql: 1
    injection_xss: 1
    disable_len_check: 0
    headers_mlen: 8192
    url_mlen: 28030
    cookie_mlen: 65535

# Delete a WAF profile
- adc_waf_profile:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_profile"
    name: "my_waf_profile"

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
        data_bytes = data_json.encode(\'utf-8\')
        req = urllib_request.Request(url, data=data_bytes)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib_request.Request(url)

        response = urllib_request.urlopen(req)
        result = json.loads(response.read())
        return result
    except Exception as e:
        return {'status': False, 'msg': str(e)}


def adc_add_waf_profile(module):
    """Add a WAF profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="添加WAF模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.add" % (
        ip, authkey)

    # 构建请求数据
    data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]
    
    # 添加可选参数
    optional_params = [
        'rule_name', 'white_url_list', 'black_url_list', 'uri_stick_check',
        'mode', 'behavior', 'enable', 'logging', 'injection_sql', 
        'injection_xss', 'disable_len_check', 'headers_mlen', 
        'url_mlen', 'cookie_mlen', 'description'
    ]
    
    for param in optional_params:
        if module.params.get(param) is not None:
            data[param] = module.params[param]

    result = send_request(url, data, method='POST')
    return result


def adc_edit_waf_profile(module):
    """Edit a WAF profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="编辑WAF模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.edit" % (
        ip, authkey)

    # 构建请求数据
    data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]
    
    # 添加可选参数
    optional_params = [
        'rule_name', 'white_url_list', 'black_url_list', 'uri_stick_check',
        'mode', 'behavior', 'enable', 'logging', 'injection_sql', 
        'injection_xss', 'disable_len_check', 'headers_mlen', 
        'url_mlen', 'cookie_mlen'
    ]
    
    for param in optional_params:
        if module.params.get(param) is not None:
            data[param] = module.params[param]

    result = send_request(url, data, method='POST')
    return result


def adc_delete_waf_profile(module):
    """Delete a WAF profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="删除WAF模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.del" % (
        ip, authkey)

    data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    result = send_request(url, data, method='POST')
    return result


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
        module.fail_json(msg="获取WAF模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.get" % (
        ip, authkey)

    data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    result = send_request(url, data, method='POST')
    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(type='str', required=True),
            authkey=dict(type='str', required=True),
            action=dict(type='str', required=True, choices=[
                'add_profile', 'edit_profile', 'delete_profile', 'list_profiles', 'get_profile'
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
            description=dict(type='str', required=False),
        ),
        supports_check_mode=False
    )

    action = module.params['action']

    if action == 'add_profile':
        result = adc_add_waf_profile(module)
    elif action == 'edit_profile':
        result = adc_edit_waf_profile(module)
    elif action == 'delete_profile':
        result = adc_delete_waf_profile(module)
    elif action == 'list_profiles':
        result = adc_list_waf_profiles(module)
    elif action == 'get_profile':
        result = adc_get_waf_profile(module)
    else:
        module.fail_json(msg="Unknown action: %s" % action)

    # 处理不同类型的返回结果
    if isinstance(result, dict):
        # 字典类型结果，检查status字段
        if result.get('status') is True:
            module.exit_json(changed=True, result=result)
        elif 'result' in result and result['result'] == 'success':
            # 某些API可能使用result字段表示成功
            module.exit_json(changed=True, result=result)
        else:
            # 包含错误信息的字典
            module.fail_json(msg="Operation failed", result=result)
    elif isinstance(result, list):
        # 列表类型结果（如list_profiles操作）
        module.exit_json(changed=True, result=result)
    else:
        # 其他类型结果
        module.fail_json(msg="Operation failed: unexpected result type", result=result)


if __name__ == '__main__':
    main()