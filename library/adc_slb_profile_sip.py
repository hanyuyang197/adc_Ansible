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
import sys

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
    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
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
            return json.loads(result.decode('utf-8')) if result else {}
        else:
            # Python 2
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

# 获取SIP模板列表


def adc_list_sip_profiles(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.list" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    
    # 对于获取列表操作，直接返回响应数据，不判断success
    if result:
        try:
            # 检查是否有错误信息
            if 'errmsg' in result and result['errmsg']:
                module.fail_json(msg="获取SIP模板列表失败", response=result)
            else:
                module.exit_json(changed=False, profiles=result)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")

# 获取包含common分区的SIP模板列表


def adc_list_sip_profiles_withcommon(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.list.withcommon" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    
    # 对于获取列表操作，直接返回响应数据，不判断success
    if result:
        try:
            # 检查是否有错误信息
            if 'errmsg' in result and result['errmsg']:
                module.fail_json(msg="获取包含common分区的SIP模板列表失败", response=result)
            else:
                module.exit_json(changed=False, profiles=result)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")

# 获取指定SIP模板


def adc_get_sip_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.get" % (
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
                module.fail_json(msg="获取指定SIP模板失败", response=result)
            else:
                module.exit_json(changed=False, profile=result)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")

# 添加SIP模板


def adc_add_sip_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.add" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(profile_data.keys()):
        if profile_data[key] is None or (isinstance(profile_data[key], str) and profile_data[key] == ""):
            del profile_data[key]

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
    
    # 使用通用响应解析函数
    if result:
        success, result_dict = format_adc_response_for_ansible(
            result, "添加SIP模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")

# 编辑SIP模板


def adc_edit_sip_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.edit" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(profile_data.keys()):
        if profile_data[key] is None or (isinstance(profile_data[key], str) and profile_data[key] == ""):
            del profile_data[key]

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
    
    # 使用通用响应解析函数
    if result:
        success, result_dict = format_adc_response_for_ansible(
            result, "编辑SIP模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")

# 删除SIP模板


def adc_delete_sip_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.del" % (
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
            result, "删除SIP模板", True)
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
        action = 

    # 根据action执行相应操作
    if action == 'list_profiles':
        adc_list_sip_profiles(module)
    elif action == 'list_profiles_withcommon':
        adc_list_sip_profiles_withcommon(module)
    elif action == 'get_profile':
        adc_get_sip_profile(module)
    elif action == 'add_profile':
        adc_add_sip_profile(module)
    elif action == 'edit_profile':
        adc_edit_sip_profile(module)
    elif action == 'delete_profile':
        adc_delete_sip_profile(module)
    else:
        module.fail_json(msg="不支持的操作: %s" % action)


if __name__ == '__main__':
    main()
