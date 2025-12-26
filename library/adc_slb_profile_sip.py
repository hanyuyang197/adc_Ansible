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

# 定义模块参数


def define_module_args():
    return dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'list_profiles', 'list_profiles_withcommon', 'get_profile',
            'add_profile', 'edit_profile', 'delete_profile'
        ]),
        # SIP模板参数
        name=dict(type='str', required=False),
        timeout=dict(type='str', required=False),
        registrar_pool=dict(type='str', required=False),
        client_keepalive=dict(type='int', required=False),
        server_keepalive=dict(type='int', required=False),
        call_id_persist=dict(type='int', required=False),
        action_for_selclient_err=dict(type='int', required=False),
        action_for_selserver_err=dict(type='int', required=False),
        message_for_selclient_err=dict(type='str', required=False),
        message_for_selserver_err=dict(type='str', required=False),
        insert_client_ip=dict(type='int', required=False),
        dnat_alg=dict(type='int', required=False),
        snat_alg=dict(type='int', required=False),
        start_line_trans=dict(type='int', required=False),
        headers_trans=dict(type='int', required=False),
        body_trans=dict(type='int', required=False),
        nonat_match_acl=dict(type='int', required=False),
        nonat_match_acl6=dict(type='str', required=False),
        header_trans_list=dict(type='list', required=False),
        sdp_dnat_pool=dict(type='str', required=False),
        sdp_snat_pool=dict(type='str', required=False),
        client_request_header_add_list=dict(type='list', required=False),
        client_response_header_add_list=dict(type='list', required=False),
        server_request_header_add_list=dict(type='list', required=False),
        server_response_header_add_list=dict(type='list', required=False),
        client_request_header_del_list=dict(type='list', required=False),
        client_response_header_del_list=dict(type='list', required=False),
        server_request_header_del_list=dict(type='list', required=False),
        server_response_header_del_list=dict(type='list', required=False),
        modify_header_list=dict(type='list', required=False),
        description=dict(type='str', required=False)
    )

# 发送HTTP请求


def send_request(url, data=None, method='GET'):
    """Send HTTP request to ADC device"""
    response_data = None
    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            if data:
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
        else:
            # Python 2
            import urllib2 as urllib_request
            if data:
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

        result = json.loads(response_text) if response_text else {}

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

# 获取SIP模板列表


def adc_list_sip_profiles(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.list" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取包含common分区的SIP模板列表


def adc_list_sip_profiles_withcommon(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.list.withcommon" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取指定SIP模板


def adc_get_sip_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    profile_name = module.params['name']

    # 检查必需参数
    if not profile_name:
        module.fail_json(msg="获取SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.get" % (
        ip, authkey)

    # 构造请求数据
    data = {
        "name": profile_name
    }

    # 发送POST请求
    result = send_request(url, data, method='POST')
    return result

# 添加SIP模板


def adc_add_sip_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    profile_name = module.params['name']

    # 检查必需参数
    if not profile_name:
        module.fail_json(msg="添加SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.add" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": profile_name
    }

    # 只有当参数在YAML中明确定义时才包含在请求中
    optional_params = [
        'timeout', 'registrar_pool', 'client_keepalive', 'server_keepalive',
        'call_id_persist', 'action_for_selclient_err', 'action_for_selserver_err',
        'message_for_selclient_err', 'message_for_selserver_err', 'insert_client_ip',
        'dnat_alg', 'snat_alg', 'start_line_trans', 'headers_trans', 'body_trans',
        'nonat_match_acl', 'nonat_match_acl6', 'header_trans_list', 'sdp_dnat_pool',
        'sdp_snat_pool', 'client_request_header_add_list', 'client_response_header_add_list',
        'server_request_header_add_list', 'server_response_header_add_list',
        'client_request_header_del_list', 'client_response_header_del_list',
        'server_request_header_del_list', 'server_response_header_del_list',
        'modify_header_list'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 编辑SIP模板


def adc_edit_sip_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    profile_name = module.params['name']

    # 检查必需参数
    if not profile_name:
        module.fail_json(msg="编辑SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.edit" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": profile_name
    }

    # 只有当参数在YAML中明确定义时才包含在请求中
    optional_params = [
        'timeout', 'registrar_pool', 'client_keepalive', 'server_keepalive',
        'call_id_persist', 'action_for_selclient_err', 'action_for_selserver_err',
        'message_for_selclient_err', 'message_for_selserver_err', 'insert_client_ip',
        'dnat_alg', 'snat_alg', 'start_line_trans', 'headers_trans', 'body_trans',
        'nonat_match_acl', 'nonat_match_acl6', 'header_trans_list', 'sdp_dnat_pool',
        'sdp_snat_pool', 'client_request_header_add_list', 'client_response_header_add_list',
        'server_request_header_add_list', 'server_response_header_add_list',
        'client_request_header_del_list', 'client_response_header_del_list',
        'server_request_header_del_list', 'server_response_header_del_list',
        'modify_header_list', 'description'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 删除SIP模板


def adc_delete_sip_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    profile_name = module.params['name']

    # 检查必需参数
    if not profile_name:
        module.fail_json(msg="删除SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.del" % (
        ip, authkey)

    # 构造请求数据
    data = {
        "name": profile_name
    }

    # 发送POST请求
    result = send_request(url, data, method='POST')
    return result

# 主函数


def main():
    # 定义模块参数
    module_args = define_module_args()

    # 创建Ansible模块实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # 获取参数
    action = module.params['action']

    # 根据action执行相应操作
    if action == 'list_profiles':
        result = adc_list_sip_profiles(module)
    elif action == 'list_profiles_withcommon':
        result = adc_list_sip_profiles_withcommon(module)
    elif action == 'get_profile':
        result = adc_get_sip_profile(module)
    elif action == 'add_profile':
        result = adc_add_sip_profile(module)
    elif action == 'edit_profile':
        result = adc_edit_sip_profile(module)
    elif action == 'delete_profile':
        result = adc_delete_sip_profile(module)
    else:
        module.fail_json(msg="不支持的操作: %s" % action)

    # 处理结果 - 使用标准的ADC响应格式
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
