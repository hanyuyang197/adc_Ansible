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
import sys

# ADC API响应解析函数


def slb_profile_http_list(module):
    """获取HTTP模板列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.list" % (
        ip, authkey)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取HTTP模板列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取HTTP模板列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, profiles=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_http_list_withcommon(module):
    """获取包含common分区的HTTP模板列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.list.withcommon" % (
        ip, authkey)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取包含common分区的HTTP模板列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取包含common分区的HTTP模板列表失败",
                                 response=parsed_data)
            else:
                module.exit_json(changed=False, profiles=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_http_get(module):
    """获取HTTP模板详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取HTTP模板详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.get" % (
        ip, authkey)

    # 构造请求数据
    profile_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(profile_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取HTTP模板详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取HTTP模板详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, profile=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_http_add(module):
    """添加HTTP模板"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加HTTP模板需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.add" % (
        ip, authkey)

    # 构造模板数据 - 只包含在YAML中明确定义的参数

    # 定义可选参数列表
    module_list = [
        'name', 'description', 'fallback_url', 'force_reselect', 'clientip_insert',
        'clientip_insert_replace', 'retry_503', 'websocket', 'node_select_fail_response_504',
        'cookie_encrypt_name', 'cookie_encrypt_password', 'req_header_del', 'rsp_header_del',
        'req_header_insert', 'rsp_header_insert', 'url_class', 'host_class',
        'url_hash', 'url_hash_len', 'url_hash_offset', 'url_class_log_interval', 'redirect_modify',
        'redirect_modify_https', 'redirect_modify_https_port', 'cookie_select',
        'cookie_expire', 'cookie_expire_enable', 'compress', 'compress_keep_header',
        'compress_level', 'compress_min_len', 'chunking_request', 'chunking_response',
        'compress_content_type', 'compress_content_type_exclude', 'compress_url_exclude',
        'req_header_insert_cert', 'req_url_insert_cert', 'req_cookie_insert_cert', 'client_cert_code'
        'max_header_size', 'oversize_client_headers', 'oversize_server_headers',
        'max_header_count', 'excess_client_headers', 'excess_server_headers',
        'compress_algorithm'

    ]

    # 添加可选参数
    request_data = build_params_with_optional(module,module_list,[])

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="添加HTTP模板失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加HTTP模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_http_edit(module):
    """编辑HTTP模板"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑HTTP模板需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.edit" % (
        ip, authkey)

    # 构造模板数据
    module_list = [
        'name', 'description', 'fallback_url', 'force_reselect', 'clientip_insert',
        'clientip_insert_replace', 'retry_503', 'websocket', 'node_select_fail_response_504',
        'cookie_encrypt_name', 'cookie_encrypt_password', 'req_header_del', 'rsp_header_del',
        'req_header_insert', 'rsp_header_insert', 'url_class', 'host_class',
        'url_hash', 'url_hash_len', 'url_hash_offset', 'url_class_log_interval', 'redirect_modify',
        'redirect_modify_https', 'redirect_modify_https_port', 'cookie_select',
        'cookie_expire', 'cookie_expire_enable', 'compress', 'compress_keep_header',
        'compress_level', 'compress_min_len', 'chunking_request', 'chunking_response',
        'compress_content_type', 'compress_content_type_exclude', 'compress_url_exclude',
        'req_header_insert_cert', 'req_url_insert_cert', 'req_cookie_insert_cert', 'client_cert_code'
        'max_header_size', 'oversize_client_headers', 'oversize_server_headers',
        'max_header_count', 'excess_client_headers', 'excess_server_headers',
        'compress_algorithm'

    ]

    # 添加可选参数
    request_data = build_params_with_optional(module,module_list,[])

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="编辑HTTP模板失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑HTTP模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_http_del(module):
    """删除HTTP模板"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除HTTP模板需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.del" % (
        ip, authkey)

    # 构造请求数据
    profile_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(profile_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="删除HTTP模板失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除HTTP模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'slb_profile_http_list', 'slb_profile_http_list_withcommon', 'slb_profile_http_get',
            'slb_profile_http_add', 'slb_profile_http_edit', 'slb_profile_http_del']),
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
        url_class=dict(type='list', required=False),
        host_class=dict(type='list', required=False),
        url_hash=dict(type='int', required=False),
        url_hash_len=dict(type='int', required=False),
        url_hash_offset=dict(type='int', required=False),
        url_class_log_interval=dict(type='int', required=False),
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
        req_header_insert_cert=dict(type='list', required=False),
        req_url_insert_cert=dict(type='list', required=False),
        req_cookie_insert_cert=dict(type='list', required=False),
        client_cert_code=dict(type='list', required=False),
        max_header_size=dict(type='raw', required=False),
        oversize_client_headers=dict(type='raw', required=False),
        oversize_server_headers=dict(type='raw', required=False),
        max_header_count=dict(type='raw', required=False),
        excess_client_headers=dict(type='raw', required=False),
        excess_server_headers=dict(type='raw', required=False),
        compress_algorithm=dict(type='raw', required=False),

    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'slb_profile_http_list':
        slb_profile_http_list(module)
    elif action == 'slb_profile_http_list_withcommon':
        slb_profile_http_list_withcommon(module)
    elif action == 'slb_profile_http_get':
        slb_profile_http_get(module)
    elif action == 'slb_profile_http_add':
        slb_profile_http_add(module)
    elif action == 'slb_profile_http_edit':
        slb_profile_http_edit(module)
    elif action == 'slb_profile_http_del':
        slb_profile_http_del(module)


if __name__ == '__main__':
    main()
