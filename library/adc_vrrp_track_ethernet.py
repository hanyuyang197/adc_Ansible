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


def vrrp_track_ethernet_add(module):
    """添加VRRP以太网接口监控条件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    group_id = module.params.get('group_id')
    priority = module.params.get('priority')
    slot = module.params.get('slot')
    port = module.params.get('port')

    # 检查必需参数
    if group_id is None:
        module.fail_json(msg="添加VRRP以太网接口监控需要提供group_id参数")
    if priority is None:
        module.fail_json(msg="添加VRRP以太网接口监控需要提供priority参数")
    if slot is None:
        module.fail_json(msg="添加VRRP以太网接口监控需要提供slot参数")
    if port is None:
        module.fail_json(msg="添加VRRP以太网接口监控需要提供port参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.track.ethernet.add" % (ip, authkey)

    # 构造请求数据
    request_data = {
        "group_id": group_id,
        "priority": priority,
        "slot": slot,
        "port": port
    }

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
        module.fail_json(msg="添加VRRP以太网接口监控失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加VRRP以太网接口监控", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def vrrp_track_ethernet_list(module):
    """获取VRRP以太网接口监控条件列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.track.ethernet.list" % (ip, authkey)

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
        module.fail_json(msg="获取VRRP以太网接口监控列表失败: %s" % str(e))

    # 使用通用响应解析函数 - 只检查errmsg/errcode，不检查status
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取VRRP以太网接口监控列表", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def vrrp_track_ethernet_edit(module):
    """编辑VRRP以太网接口监控条件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    group_id = module.params.get('group_id')
    priority = module.params.get('priority')
    slot = module.params.get('slot')
    port = module.params.get('port')

    # 检查必需参数
    if group_id is None:
        module.fail_json(msg="编辑VRRP以太网接口监控需要提供group_id参数")
    if priority is None:
        module.fail_json(msg="编辑VRRP以太网接口监控需要提供priority参数")
    if slot is None:
        module.fail_json(msg="编辑VRRP以太网接口监控需要提供slot参数")
    if port is None:
        module.fail_json(msg="编辑VRRP以太网接口监控需要提供port参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.track.ethernet.edit" % (ip, authkey)

    # 构造请求数据
    request_data = {
        "group_id": group_id,
        "priority": priority,
        "slot": slot,
        "port": port
    }

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
        module.fail_json(msg="编辑VRRP以太网接口监控失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑VRRP以太网接口监控", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def vrrp_track_ethernet_del(module):
    """删除VRRP以太网接口监控条件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    group_id = module.params.get('group_id')
    slot = module.params.get('slot')
    port = module.params.get('port')

    # 检查必需参数
    if group_id is None:
        module.fail_json(msg="删除VRRP以太网接口监控需要提供group_id参数")
    if slot is None:
        module.fail_json(msg="删除VRRP以太网接口监控需要提供slot参数")
    if port is None:
        module.fail_json(msg="删除VRRP以太网接口监控需要提供port参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.track.ethernet.del" % (ip, authkey)

    # 构造请求数据
    request_data = {
        "group_id": group_id,
        "slot": slot,
        "port": port
    }

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
        module.fail_json(msg="删除VRRP以太网接口监控失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除VRRP以太网接口监控", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    """主函数"""
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'vrrp_track_ethernet_add', 'vrrp_track_ethernet_list',
            'vrrp_track_ethernet_edit', 'vrrp_track_ethernet_del'
        ]),
        group_id=dict(type='int', required=False),
        priority=dict(type='int', required=False),
        slot=dict(type='int', required=False),
        port=dict(type='int', required=False)
    )

    # 创建模块
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # 根据action参数调用相应的函数
    action = module.params.get('action')

    if action == 'vrrp_track_ethernet_add':
        vrrp_track_ethernet_add(module)
    elif action == 'vrrp_track_ethernet_list':
        vrrp_track_ethernet_list(module)
    elif action == 'vrrp_track_ethernet_edit':
        vrrp_track_ethernet_edit(module)
    elif action == 'vrrp_track_ethernet_del':
        vrrp_track_ethernet_del(module)


if __name__ == '__main__':
    main()
