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
module: adc_slb_ruletable
short_description: Manage ADC SLB Rule Tables
description:
    - Manage ADC SLB Rule Tables including add, list and get operations
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
            - The action to perform (list_ruletables, list_ruletables_withcommon, get_ruletable, add_ruletable, delete_ruletable, add_ruletable_entry)
        required: true
        choices: ['list_ruletables', 'list_ruletables_withcommon', 'get_ruletable', 'add_ruletable', 'delete_ruletable', 'add_ruletable_entry']
    name:
        description:
            - The name of the rule table
        required: false
    entrys:
        description:
            - Rule entries array
        required: false
        type: list
author:
    - Your Name
'''

EXAMPLES = '''
# List all rule tables
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "list_ruletables"

# Get a specific rule table
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "get_ruletable"
    name: "my_ruletable"

# Add a rule table
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_ruletable"
    name: "my_ruletable"

# Delete a rule table
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_ruletable"
    name: "my_ruletable"

# Add rule table entries
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_ruletable_entry"
    name: "my_ruletable"
    entrys:
      - ip: "1.2.3.4/32"
        id: 1
        age: 0
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


def adc_list_ruletables(module):
    """List all rule tables"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.list" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_list_ruletables_withcommon(module):
    """List all rule tables including common partition"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.list.withcommon" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_get_ruletable(module):
    """Get a specific rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "获取规则表需要提供name参数"}

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.get" % (
        ip, authkey)

    data = {
        "name": name
    }

    result = send_request(url, data, method='POST')
    return result


def adc_add_ruletable(module):
    """Add a new rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "添加规则表需要提供name参数"}

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.add" % (
        ip, authkey)

    # Construct rule table data
    ruletable_data = {
        "ruletable": {
            "name": name
        }
    }

    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result


def adc_delete_ruletable(module):
    """Delete a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "删除规则表需要提供name参数"}

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.del" % (
        ip, authkey)

    # Construct rule table data
    ruletable_data = {
        "name": name
    }

    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result


def adc_add_ruletable_entry(module):
    """Add entries to a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    entrys = module.params['entrys']

    # Check required parameters
    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "添加规则表条目需要提供name参数"}

    if not entrys:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "添加规则表条目需要提供entrys参数"}

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.entry.add" % (
        ip, authkey)

    # Construct rule table entry data
    ruletable_data = {
        "name": name,
        "entrys": entrys
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
                'list_ruletables', 'list_ruletables_withcommon', 'get_ruletable',
                'add_ruletable', 'delete_ruletable', 'add_ruletable_entry'
            ]),
            name=dict(type='str', required=False),
            entrys=dict(type='list', required=False),
        ),
        supports_check_mode=False
    )

    action = module.params['action']

    if action == 'list_ruletables':
        result = adc_list_ruletables(module)
    elif action == 'list_ruletables_withcommon':
        result = adc_list_ruletables_withcommon(module)
    elif action == 'get_ruletable':
        result = adc_get_ruletable(module)
    elif action == 'add_ruletable':
        result = adc_add_ruletable(module)
    elif action == 'delete_ruletable':
        result = adc_delete_ruletable(module)
    elif action == 'add_ruletable_entry':
        result = adc_add_ruletable_entry(module)
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
