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
module: adc_slb_ruletable_dns
short_description: Manage ADC SLB DNS Rule Tables
description:
    - Manage ADC SLB DNS Rule Tables including add and delete operations
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
            - The action to perform (add_dns, delete_dns)
        required: true
        choices: ['add_dns', 'delete_dns']
    name:
        description:
            - The name of the rule table
        required: true
    dnss:
        description:
            - DNS entries array
        required: true
        type: list
author:
    - Your Name
'''

EXAMPLES = '''
# Add DNS entries to rule table
- adc_slb_ruletable_dns:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_dns"
    name: "my_dns_table"
    dnss:
      - domain: "www.example.com"
        lid: 1
        match_type: 0

# Delete DNS entries from rule table
- adc_slb_ruletable_dns:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_dns"
    name: "my_dns_table"
    dnss:
      - domain: "www.example.com"
        lid: 1
        match_type: 0
'''

RETURN = '''
result:
    description: The response from the ADC device
    returned: success
    type: dict
'''


def send_request(url, data=None, method='POST'):
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


def slb_ruletable_dns_add(module):
    """Add DNS entries to a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    dnss = module.params['dnss']

    # Check required parameters
    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "添加DNS规则表条目需要提供name参数"}

    if not dnss:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "添加DNS规则表条目需要提供dnss参数"}

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.dns.add" % (
        ip, authkey)

    # Construct rule table DNS data
    ruletable_data = {
        "name": name,
        "dnss": dnss
    }

    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result


def slb_ruletable_dns_del(module):
    """Delete DNS entries from a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    dnss = module.params['dnss']

    # Check required parameters
    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "删除DNS规则表条目需要提供name参数"}

    if not dnss:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "删除DNS规则表条目需要提供dnss参数"}

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.dns.del" % (
        ip, authkey)

    # Construct rule table DNS data
    ruletable_data = {
        "name": name,
        "dnss": dnss
    }

    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(type='str', required=True),
            authkey=dict(type='str', required=True, no_log=True),
            action=dict(type='str', required=True, choices=[
                'slb_ruletable_dns_add', 'slb_ruletable_dns_del'
            ]),
            name=dict(type='str', required=True),
            dnss=dict(type='list', required=True),
        ),
        supports_check_mode=False
    )

    action = module.params['action']

    if action == 'slb_ruletable_dns_add':
        result = slb_ruletable_dns_add(module)
    elif action == 'slb_ruletable_dns_del':
        result = slb_ruletable_dns_del(module)


    # 统一使用标准的ADC响应格式处理结果
    # 成功响应: {"result":"success"} 或直接返回数据
    # 错误响应: {"result":"error","errcode":"...","errmsg":"..."}
    if isinstance(result, dict):
        if result.get('result', '').lower() == 'success':
            # 成功响应
            module.exit_json(changed=True, result=result)
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
            module.exit_json(changed=False, result=result)
    elif isinstance(result, list):
        # 列表类型直接返回
        module.exit_json(changed=False, result=result)
    else:
        # 其他类型也直接返回
        module.exit_json(changed=False, result=result)


if __name__ == '__main__':
    main()