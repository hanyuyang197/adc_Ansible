#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import json
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


def adc_list_http_profiles(module):
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


def adc_list_http_profiles_withcommon(module):
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


def adc_get_http_profile(module):
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


def adc_add_http_profile(module):
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

    # 构造模板数据
    profile_data = {
        "name": name,
        "description": module.params['description'] if 'description' in module.params else "",
        "fallback_url": module.params['fallback_url'] if 'fallback_url' in module.params else "",
        "force_reselect": module.params['force_reselect'] if 'force_reselect' in module.params else 0,
        "clientip_insert": module.params['clientip_insert'] if 'clientip_insert' in module.params else "",
        "clientip_insert_replace": module.params['clientip_insert_replace'] if 'clientip_insert_replace' in module.params else 0,
        "retry_503": module.params['retry_503'] if 'retry_503' in module.params else 0,
        "websocket": module.params['websocket'] if 'websocket' in module.params else 0,
        "node_select_fail_response_504": module.params['node_select_fail_response_504'] if 'node_select_fail_response_504' in module.params else 1,
        "cookie_encrypt_name": module.params['cookie_encrypt_name'] if 'cookie_encrypt_name' in module.params else "",
        "cookie_encrypt_password": module.params['cookie_encrypt_password'] if 'cookie_encrypt_password' in module.params else "",
        "req_header_del": module.params['req_header_del'] if 'req_header_del' in module.params else [],
        "rsp_header_del": module.params['rsp_header_del'] if 'rsp_header_del' in module.params else [],
        "req_header_insert": module.params['req_header_insert'] if 'req_header_insert' in module.params else [],
        "rsp_header_insert": module.params['rsp_header_insert'] if 'rsp_header_insert' in module.params else [],
        "url_class": module.params['url_class'] if 'url_class' in module.params else [],
        "host_class": module.params['host_class'] if 'host_class' in module.params else [],
        "url_hash": module.params['url_hash'] if 'url_hash' in module.params else 0,
        "url_hash_len": module.params['url_hash_len'] if 'url_hash_len' in module.params else 0,
        "url_hash_offset": module.params['url_hash_offset'] if 'url_hash_offset' in module.params else 0,
        "redirect_modify": module.params['redirect_modify'] if 'redirect_modify' in module.params else [],
        "redirect_modify_https": module.params['redirect_modify_https'] if 'redirect_modify_https' in module.params else 0,
        "redirect_modify_https_port": module.params['redirect_modify_https_port'] if 'redirect_modify_https_port' in module.params else 0,
        "cookie_select": module.params['cookie_select'] if 'cookie_select' in module.params else 0,
        "cookie_expire": module.params['cookie_expire'] if 'cookie_expire' in module.params else 0,
        "cookie_expire_enable": module.params['cookie_expire_enable'] if 'cookie_expire_enable' in module.params else 0,
        "compress": module.params['compress'] if 'compress' in module.params else 0,
        "compress_keep_header": module.params['compress_keep_header'] if 'compress_keep_header' in module.params else 0,
        "compress_level": module.params['compress_level'] if 'compress_level' in module.params else 1,
        "compress_min_len": module.params['compress_min_len'] if 'compress_min_len' in module.params else 0,
        "chunking_request": module.params['chunking_request'] if 'chunking_request' in module.params else 0,
        "chunking_response": module.params['chunking_response'] if 'chunking_response' in module.params else 0,
        "compress_content_type": module.params['compress_content_type'] if 'compress_content_type' in module.params else [],
        "compress_content_type_exclude": module.params['compress_content_type_exclude'] if 'compress_content_type_exclude' in module.params else [],
        "compress_url_exclude": module.params['compress_url_exclude'] if 'compress_url_exclude' in module.params else [],
        "req_header_insert_cert": module.params['req_header_insert_cert'] if 'req_header_insert_cert' in module.params else [],
        "req_url_insert_cert": module.params['req_url_insert_cert'] if 'req_url_insert_cert' in module.params else [],
        "req_cookie_insert_cert": module.params['req_cookie_insert_cert'] if 'req_cookie_insert_cert' in module.params else [],
        "client_cert_code": module.params['client_cert_code'] if 'client_cert_code' in module.params else []
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


def adc_edit_http_profile(module):
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
    profile_data = {
        "name": name
    }

    # 添加可选参数
    if 'description' in module.params and module.params['description'] is not None:
        profile_data['description'] = module.params['description']
    if 'fallback_url' in module.params and module.params['fallback_url'] is not None:
        profile_data['fallback_url'] = module.params['fallback_url']
    if 'force_reselect' in module.params and module.params['force_reselect'] is not None:
        profile_data['force_reselect'] = module.params['force_reselect']
    if 'clientip_insert' in module.params and module.params['clientip_insert'] is not None:
        profile_data['clientip_insert'] = module.params['clientip_insert']
    if 'clientip_insert_replace' in module.params and module.params['clientip_insert_replace'] is not None:
        profile_data['clientip_insert_replace'] = module.params['clientip_insert_replace']
    if 'retry_503' in module.params and module.params['retry_503'] is not None:
        profile_data['retry_503'] = module.params['retry_503']
    if 'websocket' in module.params and module.params['websocket'] is not None:
        profile_data['websocket'] = module.params['websocket']
    if 'node_select_fail_response_504' in module.params and module.params['node_select_fail_response_504'] is not None:
        profile_data['node_select_fail_response_504'] = module.params['node_select_fail_response_504']
    if 'cookie_encrypt_name' in module.params and module.params['cookie_encrypt_name'] is not None:
        profile_data['cookie_encrypt_name'] = module.params['cookie_encrypt_name']
    if 'cookie_encrypt_password' in module.params and module.params['cookie_encrypt_password'] is not None:
        profile_data['cookie_encrypt_password'] = module.params['cookie_encrypt_password']
    if 'req_header_del' in module.params and module.params['req_header_del'] is not None:
        profile_data['req_header_del'] = module.params['req_header_del']
    if 'rsp_header_del' in module.params and module.params['rsp_header_del'] is not None:
        profile_data['rsp_header_del'] = module.params['rsp_header_del']
    if 'req_header_insert' in module.params and module.params['req_header_insert'] is not None:
        profile_data['req_header_insert'] = module.params['req_header_insert']
    if 'rsp_header_insert' in module.params and module.params['rsp_header_insert'] is not None:
        profile_data['rsp_header_insert'] = module.params['rsp_header_insert']
    if 'url_class' in module.params and module.params['url_class'] is not None:
        profile_data['url_class'] = module.params['url_class']
    if 'host_class' in module.params and module.params['host_class'] is not None:
        profile_data['host_class'] = module.params['host_class']
    if 'url_hash' in module.params and module.params['url_hash'] is not None:
        profile_data['url_hash'] = module.params['url_hash']
    if 'url_hash_len' in module.params and module.params['url_hash_len'] is not None:
        profile_data['url_hash_len'] = module.params['url_hash_len']
    if 'url_hash_offset' in module.params and module.params['url_hash_offset'] is not None:
        profile_data['url_hash_offset'] = module.params['url_hash_offset']
    if 'redirect_modify' in module.params and module.params['redirect_modify'] is not None:
        profile_data['redirect_modify'] = module.params['redirect_modify']
    if 'redirect_modify_https' in module.params and module.params['redirect_modify_https'] is not None:
        profile_data['redirect_modify_https'] = module.params['redirect_modify_https']
    if 'redirect_modify_https_port' in module.params and module.params['redirect_modify_https_port'] is not None:
        profile_data['redirect_modify_https_port'] = module.params['redirect_modify_https_port']
    if 'cookie_select' in module.params and module.params['cookie_select'] is not None:
        profile_data['cookie_select'] = module.params['cookie_select']
    if 'cookie_expire' in module.params and module.params['cookie_expire'] is not None:
        profile_data['cookie_expire'] = module.params['cookie_expire']
    if 'cookie_expire_enable' in module.params and module.params['cookie_expire_enable'] is not None:
        profile_data['cookie_expire_enable'] = module.params['cookie_expire_enable']
    if 'compress' in module.params and module.params['compress'] is not None:
        profile_data['compress'] = module.params['compress']
    if 'compress_keep_header' in module.params and module.params['compress_keep_header'] is not None:
        profile_data['compress_keep_header'] = module.params['compress_keep_header']
    if 'compress_level' in module.params and module.params['compress_level'] is not None:
        profile_data['compress_level'] = module.params['compress_level']
    if 'compress_min_len' in module.params and module.params['compress_min_len'] is not None:
        profile_data['compress_min_len'] = module.params['compress_min_len']
    if 'chunking_request' in module.params and module.params['chunking_request'] is not None:
        profile_data['chunking_request'] = module.params['chunking_request']
    if 'chunking_response' in module.params and module.params['chunking_response'] is not None:
        profile_data['chunking_response'] = module.params['chunking_response']
    if 'compress_content_type' in module.params and module.params['compress_content_type'] is not None:
        profile_data['compress_content_type'] = module.params['compress_content_type']
    if 'compress_content_type_exclude' in module.params and module.params['compress_content_type_exclude'] is not None:
        profile_data['compress_content_type_exclude'] = module.params['compress_content_type_exclude']
    if 'compress_url_exclude' in module.params and module.params['compress_url_exclude'] is not None:
        profile_data['compress_url_exclude'] = module.params['compress_url_exclude']
    if 'req_header_insert_cert' in module.params and module.params['req_header_insert_cert'] is not None:
        profile_data['req_header_insert_cert'] = module.params['req_header_insert_cert']
    if 'req_url_insert_cert' in module.params and module.params['req_url_insert_cert'] is not None:
        profile_data['req_url_insert_cert'] = module.params['req_url_insert_cert']
    if 'req_cookie_insert_cert' in module.params and module.params['req_cookie_insert_cert'] is not None:
        profile_data['req_cookie_insert_cert'] = module.params['req_cookie_insert_cert']
    if 'client_cert_code' in module.params and module.params['client_cert_code'] is not None:
        profile_data['client_cert_code'] = module.params['client_cert_code']

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


def adc_delete_http_profile(module):
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
            'list_profiles', 'list_profiles_withcommon', 'get_profile', 'add_profile', 'edit_profile', 'delete_profile']),
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
        cookie_encrypt_password=dict(type='str', required=False),
        req_header_del=dict(type='list', required=False),
        rsp_header_del=dict(type='list', required=False),
        req_header_insert=dict(type='list', required=False),
        rsp_header_insert=dict(type='list', required=False),
        url_class=dict(type='list', required=False),
        host_class=dict(type='list', required=False),
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
        req_header_insert_cert=dict(type='list', required=False),
        req_url_insert_cert=dict(type='list', required=False),
        req_cookie_insert_cert=dict(type='list', required=False),
        client_cert_code=dict(type='list', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list_profiles':
        adc_list_http_profiles(module)
    elif action == 'list_profiles_withcommon':
        adc_list_http_profiles_withcommon(module)
    elif action == 'get_profile':
        adc_get_http_profile(module)
    elif action == 'add_profile':
        adc_add_http_profile(module)
    elif action == 'edit_profile':
        adc_edit_http_profile(module)
    elif action == 'delete_profile':
        adc_delete_http_profile(module)


if __name__ == '__main__':
    main()
