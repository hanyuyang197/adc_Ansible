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
        # HTTP模板参数
        name=dict(type='str', required=False),
        description=dict(type='str', required=False),
        fallback_url=dict(type='str', required=False),
        force_reselect=dict(type='int', required=False),
        clientip_insert=dict(type='str', required=False),
        clientip_insert_replace=dict(type='int', required=False),
        retry_503=dict(type='int', required=False),
        websocket=dict(type='int', required=False),
        node_select_fail_response_504=dict(type='int', required=False),
        cookie_encrypt_name=dict(type='str', required=False),
        cookie_encrypt_password=dict(type='str', required=False, no_log=True),
        req_header_del=dict(type='list', required=False),
        rsp_header_del=dict(type='list', required=False),
        req_header_insert=dict(type='list', required=False),
        rsp_header_insert=dict(type='list', required=False),
        url_hash=dict(type='int', required=False),
        url_hash_len=dict(type='int', required=False),
        url_hash_offset=dict(type='int', required=False),
        redirect_modify=dict(type='list', required=False),
        redirect_modify_https=dict(type='int', required=False),
        redirect_modify_https_port=dict(type='int', required=False),
        cookie_select=dict(type='int', required=False),
        cookie_expire=dict(type='int', required=False),
        cookie_expire_enable=dict(type='int', required=False),
        compress=dict(type='int', required=False),
        compress_keep_header=dict(type='int', required=False),
        compress_level=dict(type='int', required=False),
        compress_min_len=dict(type='int', required=False),
        chunking_request=dict(type='int', required=False),
        chunking_response=dict(type='int', required=False),
        compress_content_type=dict(type='list', required=False),
        compress_content_type_exclude=dict(type='list', required=False),
        compress_url_exclude=dict(type='list', required=False),
        client_cert_code=dict(type='list', required=False),
        req_header_insert_cert=dict(type='list', required=False),
        req_url_insert_cert=dict(type='list', required=False),
        req_cookie_insert_cert=dict(type='list', required=False)
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

# 获取HTTP模板列表


def adc_list_http_profiles(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.list" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取包含common分区的HTTP模板列表


def adc_list_http_profiles_withcommon(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.list.withcommon" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取指定HTTP模板


def adc_get_http_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取HTTP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.get" % (
        ip, authkey)

    # 构造请求数据
    data = {
        "name": name
    }

    # 发送POST请求
    result = send_request(url, data, method='POST')
    return result

# 添加HTTP模板


def adc_add_http_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加HTTP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.add" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name
    }

    # 只有当参数在YAML中明确定义时才包含在请求中
    optional_params = [
        'description', 'fallback_url', 'force_reselect', 'clientip_insert',
        'clientip_insert_replace', 'retry_503', 'websocket',
        'node_select_fail_response_504', 'cookie_encrypt_name',
        'cookie_encrypt_password', 'req_header_del', 'rsp_header_del',
        'req_header_insert', 'rsp_header_insert', 'url_hash', 'url_hash_len',
        'url_hash_offset', 'redirect_modify', 'redirect_modify_https',
        'redirect_modify_https_port', 'cookie_select', 'cookie_expire',
        'cookie_expire_enable', 'compress', 'compress_keep_header',
        'compress_level', 'compress_min_len', 'chunking_request',
        'chunking_response', 'compress_content_type',
        'compress_content_type_exclude', 'compress_url_exclude',
        'client_cert_code', 'req_header_insert_cert', 'req_url_insert_cert',
        'req_cookie_insert_cert'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 编辑HTTP模板


def adc_edit_http_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑HTTP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.edit" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name
    }

    # 只有当参数在YAML中明确定义时才包含在请求中
    optional_params = [
        'description', 'fallback_url', 'force_reselect', 'clientip_insert',
        'clientip_insert_replace', 'retry_503', 'websocket',
        'node_select_fail_response_504', 'cookie_encrypt_name',
        'cookie_encrypt_password', 'req_header_del', 'rsp_header_del',
        'req_header_insert', 'rsp_header_insert', 'url_hash', 'url_hash_len',
        'url_hash_offset', 'redirect_modify', 'redirect_modify_https',
        'redirect_modify_https_port', 'cookie_select', 'cookie_expire',
        'cookie_expire_enable', 'compress', 'compress_keep_header',
        'compress_level', 'compress_min_len', 'chunking_request',
        'chunking_response', 'compress_content_type',
        'compress_content_type_exclude', 'compress_url_exclude',
        'client_cert_code', 'req_header_insert_cert', 'req_url_insert_cert',
        'req_cookie_insert_cert'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 删除HTTP模板


def adc_delete_http_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除HTTP模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.del" % (
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
        result = adc_list_http_profiles(module)
    elif action == 'list_profiles_withcommon':
        result = adc_list_http_profiles_withcommon(module)
    elif action == 'get_profile':
        result = adc_get_http_profile(module)
    elif action == 'add_profile':
        result = adc_add_http_profile(module)
    elif action == 'edit_profile':
        result = adc_edit_http_profile(module)
    elif action == 'delete_profile':
        result = adc_delete_http_profile(module)
    else:
        module.fail_json(msg="不支持的操作: %s" % action)

    # 处理结果
    if 'status' in result and result['status'] == 'error':
        module.fail_json(msg=result['msg'])
    else:
        module.exit_json(changed=True, result=result)


if __name__ == '__main__':
    main()
