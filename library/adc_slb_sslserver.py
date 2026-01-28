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
module: adc_slb_sslserver
short_description: Manage ADC SLB Server SSL profiles
description:
    - Manage ADC SLB Server SSL profiles including add, edit, delete, list and get operations
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
            - The name of the server SSL profile
        required: false
    cert:
        description:
            - Certificate name
        required: false
    key:
        description:
            - Private key name
        required: false
author:
    - Your Name
'''

EXAMPLES = '''
# List all server SSL profiles
- adc_slb_sslserver:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "list_profiles"

# Get a specific server SSL profile
- adc_slb_sslserver:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "get_profile"
    name: "my_ssl_profile"

# Add a server SSL profile
- adc_slb_sslserver:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_profile"
    name: "my_ssl_profile"
    cert: "my_cert"
    key: "my_key"

# Edit a server SSL profile
- adc_slb_sslserver:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "edit_profile"
    name: "my_ssl_profile"
    cert: "new_cert"

# Delete a server SSL profile
- adc_slb_sslserver:
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


def slb_sslserver_list(module):
    """List all server SSL profiles"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.list" % (
        ip, authkey)
    result = send_request(url)
    return result


def slb_sslserver_list_withcommon(module):
    """List all server SSL profiles including common partition"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.list.withcommon" % (
        ip, authkey)
    result = send_request(url)
    return result


def slb_sslserver_get(module):
    """Get a specific server SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="获取服务端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.get" % (
        ip, authkey)

    data = {
        "name": name
    }

    result = send_request(url, data, method='POST')
    return result


def slb_sslserver_add(module):
    """Add a new server SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="添加服务端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.add" % (
        ip, authkey)

    # Construct profile data
    profile_data = {
        "name": name
    }

    # Only include parameters that are explicitly defined in YAML
    optional_params = [
        'cert', 'key', 'password', 'ca_cert', 'ecert', 'ekey', 'epassword',
        'sni_switch', 'sni_name', 'ssl_version', 'cipher_suite', 'description', 'sign_cipher'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # Send POST request
    result = send_request(url, profile_data, method='POST')
    return result


def slb_sslserver_edit(module):
    """Edit an existing server SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="编辑服务端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.edit" % (
        ip, authkey)

    # Construct profile data
    profile_data = {
        "name": name
    }

    # Only include parameters that are explicitly defined in YAML
    optional_params = [
        'cert', 'key', 'password', 'ca_cert', 'ecert', 'ekey', 'epassword',
        'sni_switch', 'sni_name', 'ssl_version', 'cipher_suite', 'description', 'sign_cipher'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # Send POST request
    result = send_request(url, profile_data, method='POST')
    return result


def slb_sslserver_del(module):
    """Delete a server SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="删除服务端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.del" % (
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
            authkey=dict(type='str', required=True, no_log=True),
            action=dict(type='str', required=True, choices=[
                'slb_sslserver_list', 'slb_sslserver_list_withcommon', 'slb_sslserver_get',
                'slb_sslserver_add', 'slb_sslserver_edit', 'slb_sslserver_del'
            ]),
            name=dict(type='str', required=False),
            cert=dict(type='str', required=False),
            key=dict(type='str', required=False, no_log=True),
            password=dict(type='str', required=False, no_log=True),
            ca_cert=dict(type='str', required=False),
            ecert=dict(type='str', required=False),
            ekey=dict(type='str', required=False, no_log=True),
            epassword=dict(type='str', required=False, no_log=True),
            sni_switch=dict(type='int', required=False, choices=[0, 1]),
            sni_name=dict(type='str', required=False),
            ssl_version=dict(type='int', required=False, choices=[0, 1, 2, 3, 5, 6]),
            cipher_suite=dict(type='list', required=False, elements='str'),
            description=dict(type='str', required=False),
            sign_cipher=dict(type='list', required=False, elements='str'),
        ),
        supports_check_mode=False
    )

    action = module.params['action']

    if action == 'slb_sslserver_list':
        result = slb_sslserver_list(module)
    elif action == 'slb_sslserver_list_withcommon':
        result = slb_sslserver_list_withcommon(module)
    elif action == 'slb_sslserver_get':
        result = slb_sslserver_get(module)
    elif action == 'slb_sslserver_add':
        result = slb_sslserver_add(module)
    elif action == 'slb_sslserver_edit':
        result = slb_sslserver_edit(module)
    elif action == 'slb_sslserver_del':
        result = slb_sslserver_del(module)


    # 统一使用标准的ADC响应格式处理结果
    # 成功响应: {"result":"success"} 或直接返回数据
    # 错误响应: {"result":"error","errcode":"...","errmsg":"..."}
    if isinstance(result, dict):
        if result.get('result', '').lower() == 'success':
            # 成功响应
            module.exit_json(changed=True, result=result)
        elif 'errcode' in result and result['errcode']:
            # 错误响应 - 确保errmsg是unicode字符串（处理Python 2.7编码问题）
            errmsg = result.get('errmsg', '未知错误')
            if isinstance(errmsg, str):
                try:
                    # 尝试将字节字符串解码为unicode（Python 2.7）
                    errmsg = errmsg.decode('utf-8')
                except:
                    try:
                        errmsg = errmsg.decode('latin1')
                    except:
                        pass
            module.fail_json(msg="操作失败: %s" % errmsg, result=result)
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
