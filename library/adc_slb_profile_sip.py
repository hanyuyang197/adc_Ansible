#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
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
    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
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
            import urllib2 as urllib_request
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
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.get" % (
        ip, authkey)

    # 构造请求数据
    data = {
        "name": name
    }

    # 发送POST请求
    result = send_request(url, data, method='POST')
    return result

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
    profile_data = {
        "name": name
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
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.edit" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name
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
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除SIP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.sip.del" % (
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

    # 处理结果
    if 'status' in result and result['status'] == 'error':
        module.fail_json(msg=result['msg'])
    else:
        module.exit_json(changed=True, result=result)


if __name__ == '__main__':
    main()
