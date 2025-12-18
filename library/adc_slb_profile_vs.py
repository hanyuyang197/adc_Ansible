#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
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
    try:
        if data:
            data = json.dumps(data).encode('utf-8')
            req = urllib2.Request(url, data=data)
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
        result = response.read()
        parsed_result = json.loads(result) if result else {}
        
        # 标准化响应格式
        # 成功响应保持原样
        # 错误响应标准化为 {"result":"error","errcode":"REQUEST_ERROR","errmsg":"..."}
        if 'status' in parsed_result and parsed_result['status'] == 'error':
            return {
                'result': 'error',
                'errcode': 'REQUEST_ERROR',
                'errmsg': parsed_result.get('msg', '请求失败')
            }
        else:
            return parsed_result
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
    description = module.params['description']

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加虚拟服务模板需要提供name参数")

    # 检查必填参数
    required_params = [
        'ignored_tcp_msl', 'reset_unknown_conn', 'reset_l7_on_failover',
        'syn_otherflags', 'conn_limit_switch', 'conn_limit',
        'conn_over_limit_action', 'log_conn_limit_exceed',
        'conn_rate_limit_switch', 'conn_rate_limit',
        'conn_rate_over_limit_action', 'conn_rate_unit',
        'log_conn_rate_limit_exceed'
    ]

    for param in required_params:
        if module.params[param] is None:
            module.fail_json(msg="添加虚拟服务模板需要提供%s参数" % param)

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.vs.add" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name,
        "description": description,
        "ignored_tcp_msl": module.params['ignored_tcp_msl'],
        "reset_unknown_conn": module.params['reset_unknown_conn'],
        "reset_l7_on_failover": module.params['reset_l7_on_failover'],
        "syn_otherflags": module.params['syn_otherflags'],
        "conn_limit_switch": module.params['conn_limit_switch'],
        "conn_limit": module.params['conn_limit'],
        "conn_over_limit_action": module.params['conn_over_limit_action'],
        "log_conn_limit_exceed": module.params['log_conn_limit_exceed'],
        "conn_rate_limit_switch": module.params['conn_rate_limit_switch'],
        "conn_rate_limit": module.params['conn_rate_limit'],
        "conn_rate_over_limit_action": module.params['conn_rate_over_limit_action'],
        "conn_rate_unit": module.params['conn_rate_unit'],
        "log_conn_rate_limit_exceed": module.params['log_conn_rate_limit_exceed']
    }

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 编辑虚拟服务模板


def adc_edit_vs_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    description = module.params['description']

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑虚拟服务模板需要提供name参数")

    # 检查必填参数
    required_params = [
        'ignored_tcp_msl', 'reset_unknown_conn', 'reset_l7_on_failover',
        'syn_otherflags', 'conn_limit_switch', 'conn_limit',
        'conn_over_limit_action', 'log_conn_limit_exceed',
        'conn_rate_limit_switch', 'conn_rate_limit',
        'conn_rate_over_limit_action', 'conn_rate_unit',
        'log_conn_rate_limit_exceed'
    ]

    for param in required_params:
        if module.params[param] is None:
            module.fail_json(msg="编辑虚拟服务模板需要提供%s参数" % param)

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.vs.edit" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name,
        "description": description,
        "ignored_tcp_msl": module.params['ignored_tcp_msl'],
        "reset_unknown_conn": module.params['reset_unknown_conn'],
        "reset_l7_on_failover": module.params['reset_l7_on_failover'],
        "syn_otherflags": module.params['syn_otherflags'],
        "conn_limit_switch": module.params['conn_limit_switch'],
        "conn_limit": module.params['conn_limit'],
        "conn_over_limit_action": module.params['conn_over_limit_action'],
        "log_conn_limit_exceed": module.params['log_conn_limit_exceed'],
        "conn_rate_limit_switch": module.params['conn_rate_limit_switch'],
        "conn_rate_limit": module.params['conn_rate_limit'],
        "conn_rate_over_limit_action": module.params['conn_rate_over_limit_action'],
        "conn_rate_unit": module.params['conn_rate_unit'],
        "log_conn_rate_limit_exceed": module.params['log_conn_rate_limit_exceed']
    }

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
            # 错误响应
            module.fail_json(msg="操作失败: %s" % result.get('errmsg', '未知错误'), result=result)
        else:
            # 查询类API直接返回数据
            module.exit_json(changed=False, result=result)
    else:
        # 其他类型的数据直接返回
        module.exit_json(changed=False, result=result)


if __name__ == '__main__':
    main()
