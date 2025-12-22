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
module: adc_slb_sslclient
short_description: Manage ADC SLB Client SSL profiles
description:
    - Manage ADC SLB Client SSL profiles including add, edit, delete, list and get operations
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
            - The action to perform (list_profiles, list_profiles_withcommon, get_profile, add_profile, edit_profile, delete_profile)
        required: true
        choices: ['list_profiles', 'list_profiles_withcommon', 'get_profile', 'add_profile', 'edit_profile', 'delete_profile']
    name:
        description:
            - The name of the client SSL profile
        required: false
    cert:
        description:
            - First certificate name (optional RSA,ECC,GM signature certificate)
        required: false
    chain_cert:
        description:
            - First certificate chain name (optional RSA,ECC,GM signature certificate)
        required: false
    key:
        description:
            - First certificate private key name
        required: false
    password:
        description:
            - First certificate password
        required: false
    dcert:
        description:
            - Second certificate name
        required: false
    dchain_cert:
        description:
            - Second certificate chain name
        required: false
    dkey:
        description:
            - Second certificate private key name
        required: false
    dpassword:
        description:
            - Second certificate password
        required: false
    ecert:
        description:
            - GM encryption certificate name
        required: false
    ekey:
        description:
            - GM encryption certificate private key
        required: false
    epassword:
        description:
            - GM encryption certificate password
        required: false
    resume_mode:
        description:
            - Session cache mode, 0 for session ticket, 1 for session id
        required: false
    cache_num:
        description:
            - Session cache size (0-131072)
        required: false
    cache_timeout:
        description:
            - Session cache timeout in seconds (0-10000000)
        required: false
    disable_renegotiate:
        description:
            - Disable renegotiation, 0 to disable, 1 to enable
        required: false
    disable_ssl30:
        description:
            - SSL3.0 protocol version switch, 0 to enable, 1 to disable
        required: false
    disable_tls10:
        description:
            - TLS1.0 protocol version switch, 0 to enable, 1 to disable
        required: false
    disable_tls11:
        description:
            - TLS1.1 protocol version switch, 0 to enable, 1 to disable
        required: false
    disable_tls12:
        description:
            - TLS1.2 protocol version switch, 0 to enable, 1 to disable
        required: false
author:
    - Your Name
'''

EXAMPLES = '''
# List all client SSL profiles
- adc_slb_sslclient:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "list_profiles"

# Get a specific client SSL profile
- adc_slb_sslclient:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "get_profile"
    name: "my_ssl_profile"

# Add a client SSL profile
- adc_slb_sslclient:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_profile"
    name: "my_ssl_profile"
    cert: "my_cert"

# Edit a client SSL profile
- adc_slb_sslclient:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "edit_profile"
    name: "my_ssl_profile"
    cert: "new_cert"

# Delete a client SSL profile
- adc_slb_sslclient:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_profile"
    name: "my_ssl_profile"
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


def adc_list_sslclient_profiles(module):
    """List all client SSL profiles"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslclient.list" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_list_sslclient_profiles_withcommon(module):
    """List all client SSL profiles including common partition"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslclient.list.withcommon" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_get_sslclient_profile(module):
    """Get a specific client SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="获取客户端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslclient.get" % (
        ip, authkey)

    data = {
        "name": name
    }

    result = send_request(url, data, method='POST')
    return result


def adc_add_sslclient_profile(module):
    """Add a new client SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="添加客户端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslclient.add" % (
        ip, authkey)

    # Construct profile data
    profile_data = {
        "name": name
    }

    # Only include parameters that are explicitly defined in YAML
    optional_params = [
        'cert', 'chain_cert', 'key', 'password', 'dcert', 'dchain_cert',
        'dkey', 'dpassword', 'ecert', 'ekey', 'epassword', 'resume_mode',
        'cache_num', 'cache_timeout', 'disable_renegotiate', 'disable_ssl30',
        'disable_tls10', 'disable_tls11', 'disable_tls12'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # Send POST request
    result = send_request(url, profile_data, method='POST')
    return result


def adc_edit_sslclient_profile(module):
    """Edit an existing client SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="编辑客户端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslclient.edit" % (
        ip, authkey)

    # Construct profile data
    profile_data = {
        "name": name
    }

    # Only include parameters that are explicitly defined in YAML
    optional_params = [
        'cert', 'chain_cert', 'key', 'password', 'dcert', 'dchain_cert',
        'dkey', 'dpassword', 'ecert', 'ekey', 'epassword', 'resume_mode',
        'cache_num', 'cache_timeout', 'disable_renegotiate', 'disable_ssl30',
        'disable_tls10', 'disable_tls11', 'disable_tls12'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # Send POST request
    result = send_request(url, profile_data, method='POST')
    return result


def adc_delete_sslclient_profile(module):
    """Delete a client SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="删除客户端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslclient.del" % (
        ip, authkey)

    # Construct profile data
    profile_data = {
        "name": name
    }

    # Send POST request
    result = send_request(url, profile_data, method='POST')
    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(type='str', required=True),
            authkey=dict(type='str', required=True),
            action=dict(type='str', required=True, choices=[
                'list_profiles', 'list_profiles_withcommon', 'get_profile',
                'add_profile', 'edit_profile', 'delete_profile'
            ]),
            name=dict(type='str', required=False),
            cert=dict(type='str', required=False),
            chain_cert=dict(type='str', required=False),
            key=dict(type='str', required=False),
            password=dict(type='str', required=False, no_log=True),
            dcert=dict(type='str', required=False),
            dchain_cert=dict(type='str', required=False),
            dkey=dict(type='str', required=False),
            dpassword=dict(type='str', required=False, no_log=True),
            ecert=dict(type='str', required=False),
            ekey=dict(type='str', required=False),
            epassword=dict(type='str', required=False, no_log=True),
            resume_mode=dict(type='int', required=False),
            cache_num=dict(type='int', required=False),
            cache_timeout=dict(type='int', required=False),
            disable_renegotiate=dict(type='int', required=False),
            disable_ssl30=dict(type='int', required=False),
            disable_tls10=dict(type='int', required=False),
            disable_tls11=dict(type='int', required=False),
            disable_tls12=dict(type='int', required=False),
        ),
        supports_check_mode=False
    )

    action = module.params['action']

    if action == 'list_profiles':
        result = adc_list_sslclient_profiles(module)
    elif action == 'list_profiles_withcommon':
        result = adc_list_sslclient_profiles_withcommon(module)
    elif action == 'get_profile':
        result = adc_get_sslclient_profile(module)
    elif action == 'add_profile':
        result = adc_add_sslclient_profile(module)
    elif action == 'edit_profile':
        result = adc_edit_sslclient_profile(module)
    elif action == 'delete_profile':
        result = adc_delete_sslclient_profile(module)
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
