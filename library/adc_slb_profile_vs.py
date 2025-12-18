#!/usr/bin/python
# -*- coding: utf-8 -*-

# Windows兼容性处理
try:
    from ansible.module_utils.basic import AnsibleModule
except ImportError:
    # 创建一个模拟的AnsibleModule类用于测试
    class AnsibleModule:
        def __init__(self, *args, **kwargs):
            pass

        def fail_json(self, **kwargs):
            raise Exception(str(kwargs))

        def exit_json(self, **kwargs):
            print("SUCCESS:", kwargs)

import json
# Python 2/3兼容性处理
try:
    # Python 2
    import urllib2 as urllib_request
except ImportError:
    # Python 3
    import urllib.request as urllib_request
    import urllib.error as urllib_error
# ADC API响应解析函数


def format_adc_response_for_ansible(response_data, action="", changed_default=True):
    """
    格式化ADC响应为Ansible模块返回格式

    Args:
        response_data (str/dict): API响应数据
        action (str): 执行的操作名称
        changed_default (bool): 默认的changed状态

    Returns:
        tuple: (success, result_dict)
            - success (bool): 操作是否成功
            - result_dict (dict): Ansible模块返回字典
    """

    # 初始化返回结果
    result = {
        'success': False,
        'result': '',
        'errcode': '',
        'errmsg': '',
        'data': {}
    }

    try:
        # 如果是字符串，尝试解析为JSON
        if isinstance(response_data, str):
            parsed_data = json.loads(response_data)
        else:
            parsed_data = response_data

        result['data'] = parsed_data

        # 提取基本字段
        result['result'] = parsed_data.get('result', '')
        result['errcode'] = parsed_data.get('errcode', '')
        result['errmsg'] = parsed_data.get('errmsg', '')

        # 判断操作是否成功
        if result['result'].lower() == 'success':
            result['success'] = True
        else:
            # 处理幂等性问题 - 检查错误信息中是否包含"已存在"等表示已存在的关键词
            errmsg = result['errmsg'].lower() if isinstance(
                result['errmsg'], str) else str(result['errmsg']).lower()
            if any(keyword in errmsg for keyword in ['已存在', 'already exists', 'already exist', 'exists']):
                # 幂等性处理：如果是因为已存在而导致的"失败"，实际上算成功
                result['success'] = True
                result['result'] = 'success (already exists)'

    except json.JSONDecodeError as e:
        result['errmsg'] = "JSON解析失败: %s" % str(e)
        result['errcode'] = 'JSON_PARSE_ERROR'
    except Exception as e:
        result['errmsg'] = "响应解析异常: %s" % str(e)
        result['errcode'] = 'PARSE_EXCEPTION'

    # 格式化为Ansible返回格式
    if result['success']:
        # 操作成功
        result_dict = {
            'changed': changed_default,
            'msg': '%s操作成功' % action if action else '操作成功',
            'response': result['data']
        }

        # 如果是幂等性成功（已存在），调整消息
        if 'already exists' in result['result']:
            result_dict['changed'] = False
            result_dict['msg'] = '%s操作成功（资源已存在，无需更改）' % action if action else '操作成功（资源已存在，无需更改）'

        return True, result_dict
    else:
        # 操作失败
        result_dict = {
            'changed': False,
            'msg': '%s操作失败' % action if action else '操作失败',
            'error': {
                'result': result['result'],
                'errcode': result['errcode'],
                'errmsg': result['errmsg']
            },
            'response': result['data']
        }
        return False, result_dict

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
            req = urllib_request.Request(url, data=data)
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
        result = response.read()
        return json.loads(result) if result else {}
    except Exception as e:
        return {'status': 'error', 'msg': str(e)}

# 获取虚拟服务模板列表


def adc_list_vs_profiles(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.vs.list" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')

    # 对于获取列表操作，直接返回响应数据，不判断success
    if result:
        try:
            # 检查是否有错误信息
            if 'errmsg' in result and result['errmsg']:
                module.fail_json(msg="获取虚拟服务模板列表失败", response=result)
            else:
                module.exit_json(changed=False, profiles=result)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")

# 获取包含common分区的虚拟服务模板列表


def adc_list_vs_profiles_withcommon(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.vs.list.withcommon" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')

    # 对于获取列表操作，直接返回响应数据，不判断success
    if result:
        try:
            # 检查是否有错误信息
            if 'errmsg' in result and result['errmsg']:
                module.fail_json(
                    msg="获取包含common分区的虚拟服务模板列表失败", response=result)
            else:
                module.exit_json(changed=False, profiles=result)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")

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
    data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    # 发送POST请求
    result = send_request(url, data, method='POST')

    # 对于获取操作，直接返回响应数据，不判断success
    if result:
        try:
            # 检查是否有错误信息
            if 'errmsg' in result and result['errmsg']:
                module.fail_json(msg="获取指定虚拟服务模板失败", response=result)
            else:
                module.exit_json(changed=False, profile=result)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")

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
    profile_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        profile_data["name"] = module.params["name"]
    if "description" in module.params and module.params["description"] is not None:
        profile_data["description"] = description
    if "ignored_tcp_msl" in module.params and module.params["ignored_tcp_msl"] is not None:
        profile_data["ignored_tcp_msl"] = module.params["ignored_tcp_msl"]
    if "reset_unknown_conn" in module.params and module.params["reset_unknown_conn"] is not None:
        profile_data["reset_unknown_conn"] = module.params["reset_unknown_conn"]
    if "reset_l7_on_failover" in module.params and module.params["reset_l7_on_failover"] is not None:
        profile_data["reset_l7_on_failover"] = module.params["reset_l7_on_failover"]
    if "syn_otherflags" in module.params and module.params["syn_otherflags"] is not None:
        profile_data["syn_otherflags"] = module.params["syn_otherflags"]
    if "conn_limit_switch" in module.params and module.params["conn_limit_switch"] is not None:
        profile_data["conn_limit_switch"] = module.params["conn_limit_switch"]
    if "conn_limit" in module.params and module.params["conn_limit"] is not None:
        profile_data["conn_limit"] = module.params["conn_limit"]
    if "conn_over_limit_action" in module.params and module.params["conn_over_limit_action"] is not None:
        profile_data["conn_over_limit_action"] = module.params["conn_over_limit_action"]
    if "log_conn_limit_exceed" in module.params and module.params["log_conn_limit_exceed"] is not None:
        profile_data["log_conn_limit_exceed"] = module.params["log_conn_limit_exceed"]
    if "conn_rate_limit_switch" in module.params and module.params["conn_rate_limit_switch"] is not None:
        profile_data["conn_rate_limit_switch"] = module.params["conn_rate_limit_switch"]
    if "conn_rate_limit" in module.params and module.params["conn_rate_limit"] is not None:
        profile_data["conn_rate_limit"] = module.params["conn_rate_limit"]
    if "conn_rate_over_limit_action" in module.params and module.params["conn_rate_over_limit_action"] is not None:
        profile_data["conn_rate_over_limit_action"] = module.params["conn_rate_over_limit_action"]
    if "conn_rate_unit" in module.params and module.params["conn_rate_unit"] is not None:
        profile_data["conn_rate_unit"] = module.params["conn_rate_unit"]
    if "log_conn_rate_limit_exceed" in module.params and module.params["log_conn_rate_limit_exceed"] is not None:
        profile_data["log_conn_rate_limit_exceed"] = module.params["log_conn_rate_limit_exceed"]

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')

    # 使用通用响应解析函数
    if result:
        success, result_dict = format_adc_response_for_ansible(
            result, "添加虚拟服务模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")

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
    profile_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        profile_data["name"] = module.params["name"]
    if "description" in module.params and module.params["description"] is not None:
        profile_data["description"] = description
    if "ignored_tcp_msl" in module.params and module.params["ignored_tcp_msl"] is not None:
        profile_data["ignored_tcp_msl"] = module.params["ignored_tcp_msl"]
    if "reset_unknown_conn" in module.params and module.params["reset_unknown_conn"] is not None:
        profile_data["reset_unknown_conn"] = module.params["reset_unknown_conn"]
    if "reset_l7_on_failover" in module.params and module.params["reset_l7_on_failover"] is not None:
        profile_data["reset_l7_on_failover"] = module.params["reset_l7_on_failover"]
    if "syn_otherflags" in module.params and module.params["syn_otherflags"] is not None:
        profile_data["syn_otherflags"] = module.params["syn_otherflags"]
    if "conn_limit_switch" in module.params and module.params["conn_limit_switch"] is not None:
        profile_data["conn_limit_switch"] = module.params["conn_limit_switch"]
    if "conn_limit" in module.params and module.params["conn_limit"] is not None:
        profile_data["conn_limit"] = module.params["conn_limit"]
    if "conn_over_limit_action" in module.params and module.params["conn_over_limit_action"] is not None:
        profile_data["conn_over_limit_action"] = module.params["conn_over_limit_action"]
    if "log_conn_limit_exceed" in module.params and module.params["log_conn_limit_exceed"] is not None:
        profile_data["log_conn_limit_exceed"] = module.params["log_conn_limit_exceed"]
    if "conn_rate_limit_switch" in module.params and module.params["conn_rate_limit_switch"] is not None:
        profile_data["conn_rate_limit_switch"] = module.params["conn_rate_limit_switch"]
    if "conn_rate_limit" in module.params and module.params["conn_rate_limit"] is not None:
        profile_data["conn_rate_limit"] = module.params["conn_rate_limit"]
    if "conn_rate_over_limit_action" in module.params and module.params["conn_rate_over_limit_action"] is not None:
        profile_data["conn_rate_over_limit_action"] = module.params["conn_rate_over_limit_action"]
    if "conn_rate_unit" in module.params and module.params["conn_rate_unit"] is not None:
        profile_data["conn_rate_unit"] = module.params["conn_rate_unit"]
    if "log_conn_rate_limit_exceed" in module.params and module.params["log_conn_rate_limit_exceed"] is not None:
        profile_data["log_conn_rate_limit_exceed"] = module.params["log_conn_rate_limit_exceed"]

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')

    # 使用通用响应解析函数
    if result:
        success, result_dict = format_adc_response_for_ansible(
            result, "编辑虚拟服务模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")

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
    data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    # 发送POST请求
    result = send_request(url, data, method='POST')

    # 使用通用响应解析函数
    if result:
        success, result_dict = format_adc_response_for_ansible(
            result, "删除虚拟服务模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")

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
    # 获取action参数并确保它是字符串类型
    if 'action' in module.params and module.params['action'] is not None:
        action = str(module.params['action'])
    else:
        action = ''  # 修复不完整的赋值语句

    # 根据action执行相应操作
    if action == 'list_profiles':
        adc_list_vs_profiles(module)
    elif action == 'list_profiles_withcommon':
        adc_list_vs_profiles_withcommon(module)
    elif action == 'get_profile':
        adc_get_vs_profile(module)
    elif action == 'add_profile':
        adc_add_vs_profile(module)
    elif action == 'edit_profile':
        adc_edit_vs_profile(module)
    elif action == 'delete_profile':
        adc_delete_vs_profile(module)
    else:
        module.fail_json(msg="不支持的操作: %s" % action)


if __name__ == '__main__':
    main()
