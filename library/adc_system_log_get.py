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


def system_log_service_list(module):
    """获取服务日志列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    direct = module.params.get('direct', 0)
    index = module.params.get('index', 0)
    limit = module.params.get('limit', 30)
    level = module.params.get('level', 7)

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.service.list" % (ip, authkey)

    # 构造请求数据
    request_data = {
        "direct": direct,
        "index": index,
        "limit": limit,
        "level": level
    }

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    try:
        if sys.version_info[0] >= 3:
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
        module.fail_json(msg="获取服务日志列表失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取服务日志列表", False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_log_audit_list(module):
    """获取审计日志列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    direct = module.params.get('direct', 0)
    index = module.params.get('index', 0)
    limit = module.params.get('limit', 30)
    start_time = module.params.get('start_time', 0)
    time_range = module.params.get('time_range', 0)
    user_name = module.params.get('user_name', '')

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.audit.list" % (ip, authkey)

    # 构造请求数据
    request_data = {
        "direct": direct,
        "index": index,
        "limit": limit,
        "start_time": start_time,
        "time_range": time_range,
        "user_name": user_name
    }

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
        module.fail_json(msg="获取审计日志列表失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取审计日志列表", False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_log_nat_list(module):
    """获取NAT日志列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    direct = module.params.get('direct', 0)
    index = module.params.get('index', 0)
    limit = module.params.get('limit', 30)

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.nat.list" % (ip, authkey)

    # 构造请求数据
    request_data = {
        "direct": direct,
        "index": index,
        "limit": limit
    }

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
        module.fail_json(msg="获取NAT日志列表失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取NAT日志列表", False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_log_dns_list(module):
    """获取DNS日志列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    direct = module.params.get('direct', 0)
    index = module.params.get('index', 0)
    limit = module.params.get('limit', 30)

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.dns.list" % (ip, authkey)

    # 构造请求数据
    request_data = {
        "direct": direct,
        "index": index,
        "limit": limit
    }

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
        module.fail_json(msg="获取DNS日志列表失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取DNS日志列表", False)
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
                    'log_service_list', 'log_audit_list', 'log_nat_list', 'log_dns_list']),
        direct=dict(type='int', choices=[0, 1, 2, 3], default=0),
        index=dict(type='int', default=0),
        limit=dict(type='int', default=30),
        level=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6, 7], default=7),
        start_time=dict(type='int', default=0),
        time_range=dict(type='int', default=0),
        user_name=dict(type='str', default=''),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    action = module.params['action']

    if module.check_mode:
        module.exit_json(changed=False)

    if action == 'log_service_list':
        system_log_service_list(module)
    elif action == 'log_audit_list':
        system_log_audit_list(module)
    elif action == 'log_nat_list':
        system_log_nat_list(module)
    elif action == 'log_dns_list':
        system_log_dns_list(module)


if __name__ == '__main__':
    main()
