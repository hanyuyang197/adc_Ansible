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
try:
    # Python 2
    import urllib2
except ImportError:
    # Python 3
    import urllib.request as urllib2
    import urllib.error as urllib_error

# 定义模块参数


def define_module_args():
    return dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'list_profiles', 'list_profiles_withcommon', 'get_profile',
            'add_profile', 'edit_profile', 'delete_profile'
        ]),
        # 虚拟服务模板参数
        name=dict(type='str', required=False),
        ignored_tcp_msl=dict(type='int', required=False),
        reset_unknown_conn=dict(type='int', required=False),
        reset_l7_on_failover=dict(type='int', required=False),
        syn_otherflags=dict(type='int', required=False),
        conn_limit_switch=dict(type='int', required=False),
        conn_limit=dict(type='int', required=False),
        conn_over_limit_action=dict(type='int', required=False),
        log_conn_limit_exceed=dict(type='int', required=False),
        conn_rate_limit_switch=dict(type='int', required=False),
        conn_rate_limit=dict(type='int', required=False),
        conn_rate_over_limit_action=dict(type='int', required=False),
        conn_rate_unit=dict(type='int', required=False),
        log_conn_rate_limit_exceed=dict(type='int', required=False),
        description=dict(type='str', required=False, default="")
    )

# 发送HTTP请求


def send_request(url, data=None, method='GET'):
    """Send HTTP request to ADC device"""
    response_data = None
    try:
        if data:
            data_json = json.dumps(data)
            data_bytes = data_json.encode('utf-8')
            req = urllib2.Request(url, data=data_bytes)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib2.Request(url)

        if method == 'POST':
            req.get_method = lambda: 'POST'
        elif method == 'PUT':
            req.get_method = lambda: 'PUT'
        elif method == 'DELETE':
            req.get_method = lambda: 'DELETE'

        response = urllib2.urlopen(req)
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

        parsed_result = json.loads(response_text) if response_text else {}

        # 标准化响应格式
        # 成功响应保持原样
        # 错误响应标准化为 {"result":"error","errcode":"REQUEST_ERROR","errmsg":"..."}
        if 'status' in parsed_result and parsed_result['status'] == 'error':
            # 修复Unicode解码错误：确保错误消息正确处理中文字符
            error_msg = parsed_result.get('msg', '')
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
            return parsed_result
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

# 获取虚拟服务模板列表


def adc_list_vs_profiles(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.vs.list" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取包含common分区的虚拟服务模板列表


def adc_list_vs_profiles_withcommon(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.vs.list.withcommon" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取指定虚拟服务模板


def adc_get_vs_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取虚拟服务模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.vs.get" % (
        ip, authkey)

    # 构造请求数据
    data = {
        "name": name
    }

    # 发送POST请求
    result = send_request(url, data, method='POST')
    return result

# 添加虚拟服务模板


def adc_add_vs_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加虚拟服务模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.vs.add" % (
        ip, authkey)

    # 构造模板数据 - 只包含在YAML中明确定义的参数
    profile_data = {
        "name": name
    }

    # 添加可选参数（只包含实际定义的参数）
    if 'description' in module.params and module.params['description'] is not None:
        profile_data["description"] = module.params['description']
    if 'ignored_tcp_msl' in module.params and module.params['ignored_tcp_msl'] is not None:
        profile_data["ignored_tcp_msl"] = module.params['ignored_tcp_msl']
    if 'reset_unknown_conn' in module.params and module.params['reset_unknown_conn'] is not None:
        profile_data["reset_unknown_conn"] = module.params['reset_unknown_conn']
    if 'reset_l7_on_failover' in module.params and module.params['reset_l7_on_failover'] is not None:
        profile_data["reset_l7_on_failover"] = module.params['reset_l7_on_failover']
    if 'syn_otherflags' in module.params and module.params['syn_otherflags'] is not None:
        profile_data["syn_otherflags"] = module.params['syn_otherflags']
    if 'conn_limit_switch' in module.params and module.params['conn_limit_switch'] is not None:
        profile_data["conn_limit_switch"] = module.params['conn_limit_switch']
    if 'conn_limit' in module.params and module.params['conn_limit'] is not None:
        profile_data["conn_limit"] = module.params['conn_limit']
    if 'conn_over_limit_action' in module.params and module.params['conn_over_limit_action'] is not None:
        profile_data["conn_over_limit_action"] = module.params['conn_over_limit_action']
    if 'log_conn_limit_exceed' in module.params and module.params['log_conn_limit_exceed'] is not None:
        profile_data["log_conn_limit_exceed"] = module.params['log_conn_limit_exceed']
    if 'conn_rate_limit_switch' in module.params and module.params['conn_rate_limit_switch'] is not None:
        profile_data["conn_rate_limit_switch"] = module.params['conn_rate_limit_switch']
    if 'conn_rate_limit' in module.params and module.params['conn_rate_limit'] is not None:
        profile_data["conn_rate_limit"] = module.params['conn_rate_limit']
    if 'conn_rate_over_limit_action' in module.params and module.params['conn_rate_over_limit_action'] is not None:
        profile_data["conn_rate_over_limit_action"] = module.params['conn_rate_over_limit_action']
    if 'conn_rate_unit' in module.params and module.params['conn_rate_unit'] is not None:
        profile_data["conn_rate_unit"] = module.params['conn_rate_unit']
    if 'log_conn_rate_limit_exceed' in module.params and module.params['log_conn_rate_limit_exceed'] is not None:
        profile_data["log_conn_rate_limit_exceed"] = module.params['log_conn_rate_limit_exceed']

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 编辑虚拟服务模板


def adc_edit_vs_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑虚拟服务模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.vs.edit" % (
        ip, authkey)

    # 构造模板数据 - 只包含在YAML中明确定义的参数
    profile_data = {
        "name": name
    }

    # 添加可选参数（只包含实际定义的参数）
    if 'description' in module.params and module.params['description'] is not None:
        profile_data["description"] = module.params['description']
    if 'ignored_tcp_msl' in module.params and module.params['ignored_tcp_msl'] is not None:
        profile_data["ignored_tcp_msl"] = module.params['ignored_tcp_msl']
    if 'reset_unknown_conn' in module.params and module.params['reset_unknown_conn'] is not None:
        profile_data["reset_unknown_conn"] = module.params['reset_unknown_conn']
    if 'reset_l7_on_failover' in module.params and module.params['reset_l7_on_failover'] is not None:
        profile_data["reset_l7_on_failover"] = module.params['reset_l7_on_failover']
    if 'syn_otherflags' in module.params and module.params['syn_otherflags'] is not None:
        profile_data["syn_otherflags"] = module.params['syn_otherflags']
    if 'conn_limit_switch' in module.params and module.params['conn_limit_switch'] is not None:
        profile_data["conn_limit_switch"] = module.params['conn_limit_switch']
    if 'conn_limit' in module.params and module.params['conn_limit'] is not None:
        profile_data["conn_limit"] = module.params['conn_limit']
    if 'conn_over_limit_action' in module.params and module.params['conn_over_limit_action'] is not None:
        profile_data["conn_over_limit_action"] = module.params['conn_over_limit_action']
    if 'log_conn_limit_exceed' in module.params and module.params['log_conn_limit_exceed'] is not None:
        profile_data["log_conn_limit_exceed"] = module.params['log_conn_limit_exceed']
    if 'conn_rate_limit_switch' in module.params and module.params['conn_rate_limit_switch'] is not None:
        profile_data["conn_rate_limit_switch"] = module.params['conn_rate_limit_switch']
    if 'conn_rate_limit' in module.params and module.params['conn_rate_limit'] is not None:
        profile_data["conn_rate_limit"] = module.params['conn_rate_limit']
    if 'conn_rate_over_limit_action' in module.params and module.params['conn_rate_over_limit_action'] is not None:
        profile_data["conn_rate_over_limit_action"] = module.params['conn_rate_over_limit_action']
    if 'conn_rate_unit' in module.params and module.params['conn_rate_unit'] is not None:
        profile_data["conn_rate_unit"] = module.params['conn_rate_unit']
    if 'log_conn_rate_limit_exceed' in module.params and module.params['log_conn_rate_limit_exceed'] is not None:
        profile_data["log_conn_rate_limit_exceed"] = module.params['log_conn_rate_limit_exceed']

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 删除虚拟服务模板


def adc_delete_vs_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除虚拟服务模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.vs.del" % (
        ip, authkey)

    # 构造请求数据
    data = {
        "name": name
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
        result = adc_list_vs_profiles(module)
    elif action == 'list_profiles_withcommon':
        result = adc_list_vs_profiles_withcommon(module)
    elif action == 'get_profile':
        result = adc_get_vs_profile(module)
    elif action == 'add_profile':
        result = adc_add_vs_profile(module)
    elif action == 'edit_profile':
        result = adc_edit_vs_profile(module)
    elif action == 'delete_profile':
        result = adc_delete_vs_profile(module)
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
    else:
        # 其他类型的数据直接返回
        module.exit_json(changed=False, result=result)


if __name__ == '__main__':
    main()
