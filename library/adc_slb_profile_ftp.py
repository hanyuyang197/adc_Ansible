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
        # FTP模板参数
        name=dict(type='str', required=False),
        active_mode_port=dict(type='int', required=False),
        disable_active_mode=dict(type='int', required=False),
        disable_passive_mode=dict(type='int', required=False),
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
        return json.loads(result) if result else {}
    except Exception as e:
        return {'status': 'error', 'msg': str(e)}

# 获取FTP模板列表


def adc_list_ftp_profiles(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.ftp.list" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取包含common分区的FTP模板列表


def adc_list_ftp_profiles_withcommon(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.ftp.list.withcommon" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取指定FTP模板


def adc_get_ftp_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取FTP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.ftp.get" % (
        ip, authkey)

    # 构造请求数据
    data = {
        "name": name
    }

    # 发送POST请求
    result = send_request(url, data, method='POST')
    return result

# 添加FTP模板


def adc_add_ftp_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    active_mode_port = module.params['active_mode_port']
    disable_active_mode = module.params['disable_active_mode']
    disable_passive_mode = module.params['disable_passive_mode']
    description = module.params['description']

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加FTP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.ftp.add" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name,
        "description": description
    }

    # 只有当参数在YAML中明确定义时才包含在请求中
    if active_mode_port is not None:
        profile_data["active_mode_port"] = active_mode_port
    if disable_active_mode is not None:
        profile_data["disable_active_mode"] = disable_active_mode
    if disable_passive_mode is not None:
        profile_data["disable_passive_mode"] = disable_passive_mode

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 编辑FTP模板


def adc_edit_ftp_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    active_mode_port = module.params['active_mode_port']
    disable_active_mode = module.params['disable_active_mode']
    disable_passive_mode = module.params['disable_passive_mode']
    description = module.params['description']

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑FTP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.ftp.edit" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name,
        "description": description
    }

    # 只有当参数在YAML中明确定义时才包含在请求中
    if active_mode_port is not None:
        profile_data["active_mode_port"] = active_mode_port
    if disable_active_mode is not None:
        profile_data["disable_active_mode"] = disable_active_mode
    if disable_passive_mode is not None:
        profile_data["disable_passive_mode"] = disable_passive_mode

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 删除FTP模板


def adc_delete_ftp_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除FTP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.ftp.del" % (
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
        module_result = adc_list_ftp_profiles(module)
    elif action == 'list_profiles_withcommon':
        module_result = adc_list_ftp_profiles_withcommon(module)
    elif action == 'get_profile':
        module_result = adc_get_ftp_profile(module)
    elif action == 'add_profile':
        module_result = adc_add_ftp_profile(module)
    elif action == 'edit_profile':
        module_result = adc_edit_ftp_profile(module)
    elif action == 'delete_profile':
        module_result = adc_delete_ftp_profile(module)
    else:
        module.fail_json(msg="不支持的操作: %s" % action)

    # 处理结果
    if 'status' in module_result and module_result['status'] == 'error':
        module.fail_json(msg=module_result['msg'])
    else:
        module.exit_json(changed=True, result=module_result)


if __name__ == '__main__':
    main()
