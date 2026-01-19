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

def slb_node_list(module):
    """获取节点列表 (slb.node.list)"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.list" % (ip, authkey)

    response_data = ""

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
        module.fail_json(msg="获取节点列表失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取节点列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, nodes=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_node_get(module):
    """获取节点详情 (slb.node.get)"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params.get('name', '')

    if not name:
        module.fail_json(msg="获取节点详情需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.get" % (ip, authkey)

    node_data = {"name": name}
    post_data = json.dumps(node_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取节点详情失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取节点详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, node=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_node_add(module):
    """添加节点"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.add" % (ip, authkey)

    node_data = {"node": {}}

    optional_params = [
        'tc_name', 'graceful_time', 'graceful_delete', 'graceful_disable', 'graceful_persist',
        'name', 'host', 'domain_ip_version', 'weight', 'healthcheck', 'upnum', 'status',
        'conn_limit', 'template', 'conn_rate_limit', 'cl_log', 'desc_rserver',
        'slow_start_type', 'slow_start_recover', 'slow_start_rate', 'slow_start_from',
        'slow_start_step', 'slow_start_interval', 'slow_start_interval_num', 'slow_start_tail',
        'request_rate_limit', 'ports'
    ]

    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            node_data['node'][param] = module.params[param]

    post_data = json.dumps(node_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="添加节点失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(response_data, "添加节点", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_node_edit(module):
    """编辑节点"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params.get('name', '')

    if not name:
        module.fail_json(msg="编辑节点需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.edit" % (ip, authkey)

    node_data = {"node": {"name": name}}

    optional_params = [
        'tc_name', 'graceful_time', 'graceful_delete', 'graceful_disable', 'graceful_persist',
        'host', 'domain_ip_version', 'weight', 'healthcheck', 'upnum', 'status',
        'conn_limit', 'template', 'conn_rate_limit', 'cl_log', 'desc_rserver',
        'slow_start_type', 'slow_start_recover', 'slow_start_rate', 'slow_start_from',
        'slow_start_step', 'slow_start_interval', 'slow_start_interval_num', 'slow_start_tail',
        'request_rate_limit', 'ports'
    ]

    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            node_data['node'][param] = module.params[param]

    post_data = json.dumps(node_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="编辑节点失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(response_data, "编辑节点", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_node_del(module):
    """删除节点"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params.get('name', '')

    if not name:
        module.fail_json(msg="删除节点需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.del" % (ip, authkey)

    node_data = {"name": name}
    post_data = json.dumps(node_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="删除节点失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(response_data, "删除节点", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_node_onoff(module):
    """节点启用/禁用"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params.get('name', '')
    host = module.params.get('host', '')
    status = module.params.get('status', 1)

    if not name:
        module.fail_json(msg="节点启用/禁用需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.onoff" % (ip, authkey)

    request_data = {
        "node": {
            "name": name,
            "host": host,
            "status": status
        }
    }

    post_data = json.dumps(request_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="节点启用/禁用失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(response_data, "节点启用/禁用", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=['slb_node_list', 'slb_node_get', 'slb_node_add', 'slb_node_edit', 'slb_node_del', 'slb_node_onoff']),
        tc_name=dict(type='str', required=False),
        graceful_time=dict(type='int', required=False),
        graceful_delete=dict(type='int', required=False),
        graceful_disable=dict(type='int', required=False),
        graceful_persist=dict(type='int', required=False),
        name=dict(type='str', required=False),
        host=dict(type='str', required=False),
        domain_ip_version=dict(type='int', required=False),
        weight=dict(type='int', required=False),
        healthcheck=dict(type='str', required=False),
        upnum=dict(type='int', required=False),
        status=dict(type='int', required=False),
        conn_limit=dict(type='int', required=False),
        template=dict(type='str', required=False),
        conn_rate_limit=dict(type='int', required=False),
        cl_log=dict(type='str', required=False),
        desc_rserver=dict(type='str', required=False),
        slow_start_type=dict(type='int', required=False),
        slow_start_recover=dict(type='int', required=False),
        slow_start_rate=dict(type='int', required=False),
        slow_start_from=dict(type='int', required=False),
        slow_start_step=dict(type='int', required=False),
        slow_start_interval=dict(type='int', required=False),
        slow_start_interval_num=dict(type='int', required=False),
        slow_start_tail=dict(type='int', required=False),
        request_rate_limit=dict(type='int', required=False),
        ports=dict(type='list', required=False),
        enable=dict(type='bool', required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    action = module.params['action'] if 'action' in module.params else ''
    if hasattr(action, '__str__'):
        action = str(action)

    if action == 'slb_node_list':
        slb_node_list(module)
    elif action == 'slb_node_get':
        slb_node_get(module)
    elif action == 'slb_node_add':
        slb_node_add(module)
    elif action == 'slb_node_edit':
        slb_node_edit(module)
    elif action == 'slb_node_del':
        slb_node_del(module)
    elif action == 'slb_node_onoff':
        slb_node_onoff(module)


if __name__ == '__main__':
    main()
