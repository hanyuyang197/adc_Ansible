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


def system_ntp_add(module):
    """添加NTP配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    server = module.params['server']
    status = module.params['status']
    prefer = module.params['prefer']
    minpoll = module.params['minpoll']
    maxpoll = module.params['maxpoll']

    # 检查必需参数
    if not server:
        module.fail_json(msg="添加NTP配置需要提供server参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.ntp.add" % (
        ip, authkey)

    # 构造NTP配置数据
    ntp_data = {
        "server": server
    }

    # 添加可选参数
    if status is not None:
        ntp_data["status"] = status
    if prefer is not None:
        ntp_data["prefer"] = prefer
    if minpoll is not None:
        ntp_data["minpoll"] = minpoll
    if maxpoll is not None:
        ntp_data["maxpoll"] = maxpoll

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(ntp_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(ntp_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="添加NTP配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加NTP配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_ntp_list(module):
    """获取NTP配置列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.ntp.list" % (
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
        module.fail_json(msg="获取NTP配置列表失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取NTP配置列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, configs=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def system_ntp_get(module):
    """获取指定NTP配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    server = module.params['server']

    # 检查必需参数
    if not server:
        module.fail_json(msg="获取指定NTP配置需要提供server参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.ntp.get" % (
        ip, authkey)

    # 构造NTP配置数据
    ntp_data = {
        "server": server
    }

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            import urllib.parse as urllib_parse
            post_data = json.dumps(ntp_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            import urllib as urllib_parse
            post_data = json.dumps(ntp_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取指定NTP配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取指定NTP配置", False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_ntp_edit(module):
    """编辑NTP配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    server = module.params['server']
    status = module.params['status']
    prefer = module.params['prefer']
    minpoll = module.params['minpoll']
    maxpoll = module.params['maxpoll']

    # 检查必需参数
    if not server:
        module.fail_json(msg="编辑NTP配置需要提供server参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.ntp.edit" % (
        ip, authkey)

    # 构造NTP配置数据
    ntp_data = {
        "server": server
    }

    # 添加可选参数
    if status is not None:
        ntp_data["status"] = status
    if prefer is not None:
        ntp_data["prefer"] = prefer
    if minpoll is not None:
        ntp_data["minpoll"] = minpoll
    if maxpoll is not None:
        ntp_data["maxpoll"] = maxpoll

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(ntp_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(ntp_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="编辑NTP配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑NTP配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_ntp_del(module):
    """删除指定NTP配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    server = module.params['server']

    # 检查必需参数
    if not server:
        module.fail_json(msg="删除指定NTP配置需要提供server参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.ntp.del" % (
        ip, authkey)

    # 构造NTP配置数据
    ntp_data = {
        "server": server
    }

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(ntp_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(ntp_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="删除指定NTP配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除指定NTP配置", True)
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
            'system_ntp_add', 'system_ntp_list', 'system_ntp_get', 'system_ntp_edit', 'system_ntp_del']),
        # NTP配置参数
        server=dict(type='str', required=False),
        status=dict(type='int', required=False),
        prefer=dict(type='int', required=False),
        minpoll=dict(type='int', required=False),
        maxpoll=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'system_ntp_add':
        system_ntp_add(module)
    elif action == 'system_ntp_list':
        system_ntp_list(module)
    elif action == 'system_ntp_get':
        system_ntp_get(module)
    elif action == 'system_ntp_edit':
        system_ntp_edit(module)
    elif action == 'system_ntp_del':
        system_ntp_del(module)


if __name__ == '__main__':
    main()
