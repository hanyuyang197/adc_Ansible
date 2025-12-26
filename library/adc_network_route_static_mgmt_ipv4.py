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


def adc_list_routes(module):
    """获取IPv4静态管理路由列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=route.static.mgmt.ipv4.list" % (
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
        module.fail_json(msg="获取IPv4静态管理路由列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv4静态管理路由列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, routes=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_route(module):
    """获取IPv4静态管理路由详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    destination = module.params['destination'] if 'destination' in module.params else ""
    netmask = module.params['netmask'] if 'netmask' in module.params else ""
    gateway = module.params['gateway'] if 'gateway' in module.params else ""

    # 检查必需参数
    if not destination or not netmask or not gateway:
        module.fail_json(msg="获取IPv4静态管理路由详情需要提供destination、netmask和gateway参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=route.static.mgmt.ipv4.get" % (
        ip, authkey)

    # 构造请求数据
    route_data = {
        "destination": destination,
        "netmask": netmask,
        "gateway": gateway
    }

    # 转换为JSON格式
    post_data = json.dumps(route_data)

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
        module.fail_json(msg="获取IPv4静态管理路由详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv4静态管理路由详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, route=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_route(module):
    """添加IPv4静态管理路由"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    destination = module.params['destination'] if 'destination' in module.params else ""
    netmask = module.params['netmask'] if 'netmask' in module.params else ""
    gateway = module.params['gateway'] if 'gateway' in module.params else ""

    # 检查必需参数
    if not destination or not netmask or not gateway:
        module.fail_json(msg="添加IPv4静态管理路由需要提供destination、netmask和gateway参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=route.static.mgmt.ipv4.add" % (
        ip, authkey)

    # 构造IPv4静态管理路由数据
    route_data = {
        "destination": destination,
        "netmask": netmask,
        "gateway": gateway
    }

    # 添加可选参数
    if 'distance' in module.params and module.params['distance'] is not None:
        route_data['distance'] = module.params['distance']
    if 'description' in module.params and module.params['description'] is not None:
        route_data['description'] = module.params['description']

    # 转换为JSON格式
    post_data = json.dumps(route_data)

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
        module.fail_json(msg="添加IPv4静态管理路由失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加IPv4静态管理路由", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_route(module):
    """编辑IPv4静态管理路由"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    destination = module.params['destination'] if 'destination' in module.params else ""
    netmask = module.params['netmask'] if 'netmask' in module.params else ""
    gateway = module.params['gateway'] if 'gateway' in module.params else ""

    # 检查必需参数
    if not destination or not netmask or not gateway:
        module.fail_json(msg="编辑IPv4静态管理路由需要提供destination、netmask和gateway参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=route.static.mgmt.ipv4.edit" % (
        ip, authkey)

    # 构造IPv4静态管理路由数据
    route_data = {
        "destination": destination,
        "netmask": netmask,
        "gateway": gateway
    }

    # 添加可选参数
    if 'distance' in module.params and module.params['distance'] is not None:
        route_data['distance'] = module.params['distance']
    if 'description' in module.params and module.params['description'] is not None:
        route_data['description'] = module.params['description']

    # 转换为JSON格式
    post_data = json.dumps(route_data)

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
        module.fail_json(msg="编辑IPv4静态管理路由失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑IPv4静态管理路由", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_route(module):
    """删除IPv4静态管理路由"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    destination = module.params['destination'] if 'destination' in module.params else ""
    netmask = module.params['netmask'] if 'netmask' in module.params else ""
    gateway = module.params['gateway'] if 'gateway' in module.params else ""

    # 检查必需参数
    if not destination or not netmask or not gateway:
        module.fail_json(msg="删除IPv4静态管理路由需要提供destination、netmask和gateway参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=route.static.mgmt.ipv4.del" % (
        ip, authkey)

    # 构造请求数据
    route_data = {
        "destination": destination,
        "netmask": netmask,
        "gateway": gateway
    }

    # 转换为JSON格式
    post_data = json.dumps(route_data)

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
        module.fail_json(msg="删除IPv4静态管理路由失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除IPv4静态管理路由", True)
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
            'list_routes', 'get_route', 'add_route', 'edit_route', 'delete_route']),
        # IPv4静态管理路由参数
        destination=dict(type='str', required=False),
        netmask=dict(type='str', required=False),
        gateway=dict(type='str', required=False),
        distance=dict(type='int', required=False),
        description=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list_routes':
        adc_list_routes(module)
    elif action == 'get_route':
        adc_get_route(module)
    elif action == 'add_route':
        adc_add_route(module)
    elif action == 'edit_route':
        adc_edit_route(module)
    elif action == 'delete_route':
        adc_delete_route(module)


if __name__ == '__main__':
    main()
