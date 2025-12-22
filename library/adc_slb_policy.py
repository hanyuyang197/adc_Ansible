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
module: adc_slb_policy
short_description: Manage ADC SLB Policy Templates
description:
    - Manage ADC SLB Policy Templates including add, edit, delete, list and get operations
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
            - The action to perform (list_policies, list_policies_withcommon, get_policy, add_policy, edit_policy, delete_policy)
        required: true
        choices: ['list_policies', 'list_policies_withcommon', 'get_policy', 'add_policy', 'edit_policy', 'delete_policy']
    name:
        description:
            - The name of the policy template
        required: false
    match_dst_ip:
        description:
            - Match destination IP address; 1: yes; 0: no
        required: false
    match_overlap:
        description:
            - Overlap match; 1: yes; 0: no
        required: false
    bwlist_name:
        description:
            - Black/white list name
        required: false
    ruletable_name:
        description:
            - Rule table name
        required: false
    match_client:
        description:
            - Client matching method; 0: source IP matching; 1: destination IP matching; 2: header name matching
        required: false
    header_name:
        description:
            - Header name
        required: false
    bwlists:
        description:
            - Black/white list policy rules array
        required: false
        type: list
    ruletables:
        description:
            - Rule table policy rules array
        required: false
        type: list
author:
    - Your Name
'''

EXAMPLES = '''
# List all policy templates
- adc_slb_policy:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "list_policies"

# Get a specific policy template
- adc_slb_policy:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "get_policy"
    name: "my_policy"

# Add a policy template
- adc_slb_policy:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_policy"
    name: "my_policy"
    match_dst_ip: 1
    match_overlap: 1
    bwlist_name: "bwl"
    ruletable_name: "rt0"
    match_client: 2
    header_name: "head"

# Edit a policy template
- adc_slb_policy:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "edit_policy"
    name: "my_policy"
    match_dst_ip: 0

# Delete a policy template
- adc_slb_policy:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_policy"
    name: "my_policy"
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


def adc_list_policies(module):
    """List all policy templates"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.list" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_list_policies_withcommon(module):
    """List all policy templates including common partition"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.list.withcommon" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_get_policy(module):
    """Get a specific policy template"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="获取策略模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.get" % (
        ip, authkey)

    data = {
        "name": name
    }

    result = send_request(url, data, method='POST')
    return result


def adc_add_policy(module):
    """Add a new policy template"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="添加策略模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.add" % (
        ip, authkey)

    # Construct policy data
    policy_data = {
        "name": name
    }

    # Only include parameters that are explicitly defined in YAML
    optional_params = [
        'match_dst_ip', 'match_overlap', 'bwlist_name', 'ruletable_name',
        'match_client', 'header_name', 'bwlists', 'ruletables'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            policy_data[param] = module.params[param]

    # Send POST request
    result = send_request(url, policy_data, method='POST')
    return result


def adc_edit_policy(module):
    """Edit an existing policy template"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="编辑策略模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.edit" % (
        ip, authkey)

    # Construct policy data
    policy_data = {
        "name": name
    }

    # Only include parameters that are explicitly defined in YAML
    optional_params = [
        'match_dst_ip', 'match_overlap', 'bwlist_name', 'ruletable_name',
        'match_client', 'header_name', 'bwlists', 'ruletables'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            policy_data[param] = module.params[param]

    # Send POST request
    result = send_request(url, policy_data, method='POST')
    return result


def adc_delete_policy(module):
    """Delete a policy template"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="删除策略模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.del" % (
        ip, authkey)

    # Construct policy data
    policy_data = {
        "name": name
    }

    # Send POST request
    result = send_request(url, policy_data, method='POST')
    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(type='str', required=True),
            authkey=dict(type='str', required=True),
            action=dict(type='str', required=True, choices=[
                'list_policies', 'list_policies_withcommon', 'get_policy',
                'add_policy', 'edit_policy', 'delete_policy'
            ]),
            name=dict(type='str', required=False),
            match_dst_ip=dict(type='int', required=False),
            match_overlap=dict(type='int', required=False),
            bwlist_name=dict(type='str', required=False),
            ruletable_name=dict(type='str', required=False),
            match_client=dict(type='int', required=False),
            header_name=dict(type='str', required=False),
            bwlists=dict(type='list', required=False),
            ruletables=dict(type='list', required=False),
        ),
        supports_check_mode=False
    )

    action = module.params['action']

    if action == 'list_policies':
        result = adc_list_policies(module)
    elif action == 'list_policies_withcommon':
        result = adc_list_policies_withcommon(module)
    elif action == 'get_policy':
        result = adc_get_policy(module)
    elif action == 'add_policy':
        result = adc_add_policy(module)
    elif action == 'edit_policy':
        result = adc_edit_policy(module)
    elif action == 'delete_policy':
        result = adc_delete_policy(module)
    else:
        module.fail_json(msg="Unknown action: %s" % action)

    # 添加详细的调试信息，显示result的类型和内容
    debug_info = {
        'result_type': type(result).__name__,
        'result_repr': str(result)[:200] + ('...' if len(str(result)) > 200 else ''),
        'is_dict': isinstance(result, dict),
        'is_list': isinstance(result, list),
        'dict_keys': list(result.keys()) if isinstance(result, dict) else None,
        'list_length': len(result) if isinstance(result, list) else None
    }

    # 将调试信息添加到返回结果中
    # 注意：这只是临时调试，生产环境中应移除

    # 统一使用标准的ADC响应格式处理结果
    # 成功响应: {"result":"success"} 或直接返回数据
    # 错误响应: {"result":"error","errcode":"...","errmsg":"..."}
    if isinstance(result, dict):
        if result.get('result', '').lower() == 'success':
            # 成功响应
            module.exit_json(changed=True, result=result,
                             debug_info=debug_info)
        elif 'errcode' in result and result['errcode']:
            # 错误响应
            module.fail_json(msg="操作失败: %s" %
                             result.get('errmsg', '未知错误'), result=result, debug_info=debug_info)
        else:
            # 查询类API直接返回数据
            module.exit_json(changed=False, result=result,
                             debug_info=debug_info)
    elif isinstance(result, list):
        # 列表类型直接返回
        module.exit_json(changed=False, result=result, debug_info=debug_info)
    else:
        # 其他类型也直接返回，并添加类型信息便于调试
        module.exit_json(changed=False, result=result, debug_info=debug_info)


if __name__ == '__main__':
    main()
