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


def slb_node_port_add(module):
    """添加节点端口 (slb.node.port.add)"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加节点端口需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.add" % (ip, authkey)

    # 构造端口参数 - 按照 API 文档定义
    port_params = {}
    port_fields = [
        'port_number', 'protocol', 'status', 'weight', 'graceful_time',
        'graceful_delete', 'graceful_disable', 'graceful_persist',
        'conn_limit', 'phm_profile', 'healthcheck', 'upnum', 'nat_strategy'
    ]

    for field in port_fields:
        if field in module.params and module.params[field] is not None:
            port_params[field] = module.params[field]

    # 构造请求数据
    request_data = {
        "name": name,
        "port": port_params
    }

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
        module.fail_json(msg="添加节点端口失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加节点端口", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_node_port_edit(module):
    """编辑节点端口 (slb.node.port.edit)"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑节点端口需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.edit" % (ip, authkey)

    # 构造端口参数 - 按照 API 文档定义
    port_params = {}
    port_fields = [
        'port_number', 'protocol', 'status', 'weight', 'graceful_time',
        'graceful_delete', 'graceful_disable', 'graceful_persist',
        'conn_limit', 'phm_profile', 'healthcheck', 'upnum', 'nat_strategy'
    ]

    for field in port_fields:
        if field in module.params and module.params[field] is not None:
            port_params[field] = module.params[field]

    # 构造请求数据
    request_data = {
        "name": name,
        "port": port_params
    }

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
        module.fail_json(msg="编辑节点端口失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑节点端口", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_node_port_del(module):
    """删除节点端口 (slb.node.port.del)"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除节点端口需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.del" % (ip, authkey)

    # 构造端口参数 - 只需要 port_number 和 protocol
    port_params = {}
    if 'port_number' in module.params and module.params['port_number'] is not None:
        port_params['port_number'] = module.params['port_number']
    if 'protocol' in module.params and module.params['protocol'] is not None:
        port_params['protocol'] = module.params['protocol']

    # 构造请求数据
    request_data = {
        "name": name,
        "port": port_params
    }

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
        module.fail_json(msg="删除节点端口失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除节点端口", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_node_port_onoff(module):
    """节点端口启用/禁用 (slb.node.port.onoff)"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="节点端口启用/禁用需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.onoff" % (ip, authkey)

    # 构造请求数据
    request_data = {
        "name": name,
        "port": {
            "port_number": module.params.get('port_number', 0),
            "protocol": module.params.get('protocol', 0),
            "status": module.params.get('status', 1)
        }
    }

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
        module.fail_json(msg="节点端口启用/禁用失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "节点端口启用/禁用", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    # 定义模块参数 - 完全按照 API 文档定义
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
                    'slb_node_port_add', 'slb_node_port_edit',
                    'slb_node_port_del', 'slb_node_port_onoff']),
        name=dict(type='str', required=False),
        # port 对象参数 - 完全按照 API 文档定义
        port_number=dict(type='int', required=False),
        protocol=dict(type='int', required=False),
        status=dict(type='int', required=False),
        weight=dict(type='int', required=False),
        graceful_time=dict(type='int', required=False),
        graceful_delete=dict(type='int', required=False),
        graceful_disable=dict(type='int', required=False),
        graceful_persist=dict(type='int', required=False),
        conn_limit=dict(type='int', required=False),
        phm_profile=dict(type='str', required=False),
        healthcheck=dict(type='str', required=False),
        upnum=dict(type='int', required=False),
        nat_strategy=dict(type='str', required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    action = module.params['action'] if 'action' in module.params else ''
    if hasattr(action, '__str__'):
        action = str(action)

    if action == 'slb_node_port_add':
        slb_node_port_add(module)
    elif action == 'slb_node_port_edit':
        slb_node_port_edit(module)
    elif action == 'slb_node_port_del':
        slb_node_port_del(module)
    elif action == 'slb_node_port_onoff':
        slb_node_port_onoff(module)


if __name__ == '__main__':
    main()
