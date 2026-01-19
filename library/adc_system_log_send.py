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


def log_syslog_server_add(module):
    """添加syslog服务器配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    host = module.params['host']
    port = module.params['port']

    # 构造请求数据
    request_data = {
        "host": host,
        "port": port
    }

    # 添加可选参数
    if module.params.get('log_code') is not None:
        request_data['log_code'] = module.params['log_code']
    if module.params.get('facility') is not None:
        request_data['facility'] = module.params['facility']
    if module.params.get('nat_log') is not None:
        request_data['nat_log'] = module.params['nat_log']
    if module.params.get('audit_log') is not None:
        request_data['audit_log'] = module.params['audit_log']
    if module.params.get('service_log') is not None:
        request_data['service_log'] = module.params['service_log']
    if module.params.get('dns_log') is not None:
        request_data['dns_log'] = module.params['dns_log']
    if module.params.get('match_type') is not None:
        request_data['match_type'] = module.params['match_type']
    if module.params.get('level_filter') is not None:
        request_data['level_filter'] = module.params['level_filter']
    if module.params.get('event_list') is not None:
        request_data['event_list'] = module.params['event_list']
    if module.params.get('keyword_filter') is not None:
        request_data['keyword_filter'] = module.params['keyword_filter']
    if module.params.get('module_filter') is not None:
        request_data['module_filter'] = module.params['module_filter']
    if module.params.get('keyword_type') is not None:
        request_data['keyword_type'] = module.params['keyword_type']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.syslog.server.add" % (ip, authkey)

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="添加syslog服务器失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加syslog服务器", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def log_syslog_server_list(module):
    """获取syslog服务器列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.syslog.server.list" % (ip, authkey)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取syslog服务器列表失败: %s" % str(e))

    # 解析响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)

            # 检查响应中的错误信息
            def check_error(obj):
                """递归检查对象中是否包含有效的errmsg"""
                if isinstance(obj, dict):
                    errmsg = obj.get('errmsg', '')
                    if errmsg and str(errmsg).strip():
                        return True, errmsg
                    # 递归检查嵌套对象
                    for v in obj.values():
                        err = check_error(v)
                        if err[0]:
                            return True, err[1]
                elif isinstance(obj, list):
                    for item in obj:
                        err = check_error(item)
                        if err[0]:
                            return True, err[1]
                return False, None

            has_error, errmsg = check_error(parsed_data)
            if has_error:
                module.fail_json(msg="获取syslog服务器列表失败", errmsg=errmsg, response=parsed_data)
            else:
                # 没有错误，直接返回原始响应
                module.exit_json(changed=False, response=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def log_syslog_server_get(module):
    """获取指定syslog服务器配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    host = module.params['host']
    port = module.params['port']

    # 构造请求数据
    request_data = {
        "host": host,
        "port": port
    }

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.syslog.server.get" % (ip, authkey)

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取syslog服务器失败: %s" % str(e))

    # 解析响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)

            # 检查响应中的错误信息
            def check_error(obj):
                """递归检查对象中是否包含有效的errmsg"""
                if isinstance(obj, dict):
                    errmsg = obj.get('errmsg', '')
                    if errmsg and str(errmsg).strip():
                        return True, errmsg
                    # 递归检查嵌套对象
                    for v in obj.values():
                        err = check_error(v)
                        if err[0]:
                            return True, err[1]
                elif isinstance(obj, list):
                    for item in obj:
                        err = check_error(item)
                        if err[0]:
                            return True, err[1]
                return False, None

            has_error, errmsg = check_error(parsed_data)
            if has_error:
                module.fail_json(msg="获取syslog服务器列表失败", errmsg=errmsg, response=parsed_data)
            else:
                # 没有错误，直接返回原始响应
                module.exit_json(changed=False, response=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def log_syslog_server_edit(module):
    """编辑syslog服务器配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    host = module.params['host']
    port = module.params['port']

    # 构造请求数据
    request_data = {
        "host": host,
        "port": port
    }

    # 添加可选参数
    if module.params.get('log_code') is not None:
        request_data['log_code'] = module.params['log_code']
    if module.params.get('facility') is not None:
        request_data['facility'] = module.params['facility']
    if module.params.get('nat_log') is not None:
        request_data['nat_log'] = module.params['nat_log']
    if module.params.get('audit_log') is not None:
        request_data['audit_log'] = module.params['audit_log']
    if module.params.get('service_log') is not None:
        request_data['service_log'] = module.params['service_log']
    if module.params.get('dns_log') is not None:
        request_data['dns_log'] = module.params['dns_log']
    if module.params.get('match_type') is not None:
        request_data['match_type'] = module.params['match_type']
    if module.params.get('level_filter') is not None:
        request_data['level_filter'] = module.params['level_filter']
    if module.params.get('event_list') is not None:
        request_data['event_list'] = module.params['event_list']
    if module.params.get('keyword_filter') is not None:
        request_data['keyword_filter'] = module.params['keyword_filter']
    if module.params.get('module_filter') is not None:
        request_data['module_filter'] = module.params['module_filter']
    if module.params.get('keyword_type') is not None:
        request_data['keyword_type'] = module.params['keyword_type']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.syslog.server.edit" % (ip, authkey)

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="编辑syslog服务器失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑syslog服务器", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def log_syslog_server_del(module):
    """删除syslog服务器配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    host = module.params['host']
    port = module.params['port']

    # 构造请求数据
    request_data = {
        "host": host,
        "port": port
    }

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.syslog.server.del" % (ip, authkey)

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="删除syslog服务器失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除syslog服务器", True)
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
                    'log_syslog_server_add', 'log_syslog_server_list', 'log_syslog_server_get',
                    'log_syslog_server_edit', 'log_syslog_server_del']),
        host=dict(type='str'),
        port=dict(type='int'),
        log_code=dict(type='int', choices=[0, 1]),
        facility=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6, 7]),
        nat_log=dict(type='int', choices=[0, 1]),
        audit_log=dict(type='int', choices=[0, 1]),
        service_log=dict(type='int', choices=[0, 1]),
        dns_log=dict(type='int', choices=[0, 1]),
        match_type=dict(type='int', choices=[0, 1, 2]),
        level_filter=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6, 7]),
        event_list=dict(type='list', elements='int'),
        keyword_filter=dict(type='str'),
        module_filter=dict(type='str'),
        keyword_type=dict(type='str', choices=['string', 'regular']),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('action', 'log_syslog_server_add', ['host', 'port']),
            ('action', 'log_syslog_server_get', ['host', 'port']),
            ('action', 'log_syslog_server_edit', ['host', 'port']),
            ('action', 'log_syslog_server_del', ['host', 'port']),
        ]
    )

    action = module.params['action']

    if module.check_mode:
        module.exit_json(changed=False)

    if action == 'log_syslog_server_add':
        log_syslog_server_add(module)
    elif action == 'log_syslog_server_list':
        log_syslog_server_list(module)
    elif action == 'log_syslog_server_get':
        log_syslog_server_get(module)
    elif action == 'log_syslog_server_edit':
        log_syslog_server_edit(module)
    elif action == 'log_syslog_server_del':
        log_syslog_server_del(module)


if __name__ == '__main__':
    main()
