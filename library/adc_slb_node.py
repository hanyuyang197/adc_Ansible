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


def adc_get_nodes(module):
    """获取节点列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=get_nodes" % (ip, authkey)

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
        module.fail_json(msg="获取节点列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取节点列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, nodes=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_nodes(module):
    """获取节点列表 (slb.node.list)"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.list" % (
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
        module.fail_json(msg="获取节点列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取节点列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, nodes=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_node(module):
    """获取节点详情 (slb.node.get)"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取节点详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.get" % (
        ip, authkey)

    # 构造请求数据
    node_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(node_data)

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
        module.fail_json(msg="获取节点详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取节点详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, node=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_node(module):
    """添加节点"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.add" % (
        ip, authkey)

    # 构造节点数据 - 只包含在YAML中明确定义的参数
    node_data = {
        "node": {}
    }

    # 定义可选参数列表
    optional_params = [
        'tc_name', 'graceful_time', 'graceful_delete', 'graceful_disable', 'graceful_persist',
        'name', 'host', 'domain_ip_version', 'weight', 'healthcheck', 'upnum', 'status',
        'conn_limit', 'template', 'conn_rate_limit', 'cl_log', 'desc_rserver',
        'slow_start_type', 'slow_start_recover', 'slow_start_rate', 'slow_start_from',
        'slow_start_step', 'slow_start_interval', 'slow_start_interval_num', 'slow_start_tail',
        'request_rate_limit', 'ports'
    ]

    # 添加基本参数
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            node_data['node'][param] = module.params[param]

    # 转换为JSON格式
    post_data = json.dumps(node_data)

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
        module.fail_json(msg="添加节点失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加节点", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_node(module):
    """编辑节点"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑节点需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.edit" % (
        ip, authkey)

    # 构造节点数据
    node_data = {
        "node": {
            "name": name,
            "tc_name": module.params['tc_name'] if 'tc_name' in module.params else "",
            "graceful_time": module.params['graceful_time'] if 'graceful_time' in module.params else 0,
            "graceful_delete": module.params['graceful_delete'] if 'graceful_delete' in module.params else 0,
            "graceful_disable": module.params['graceful_disable'] if 'graceful_disable' in module.params else 0,
            "graceful_persist": module.params['graceful_persist'] if 'graceful_persist' in module.params else 0,
            "host": module.params['host'] if 'host' in module.params else "",
            "domain_ip_version": module.params['domain_ip_version'] if 'domain_ip_version' in module.params else 0,
            "weight": module.params['weight'] if 'weight' in module.params else 1,
            "healthcheck": module.params['healthcheck'] if 'healthcheck' in module.params else "",
            "upnum": module.params['upnum'] if 'upnum' in module.params else 0,
            "status": module.params['status'] if 'status' in module.params else 1,
            "conn_limit": module.params['conn_limit'] if 'conn_limit' in module.params else 0,
            "template": module.params['template'] if 'template' in module.params else "",
            "conn_rate_limit": module.params['conn_rate_limit'] if 'conn_rate_limit' in module.params else 0,
            "cl_log": module.params['cl_log'] if 'cl_log' in module.params else "0",
            "desc_rserver": module.params['desc_rserver'] if 'desc_rserver' in module.params else "",
            "slow_start_type": module.params['slow_start_type'] if 'slow_start_type' in module.params else 0,
            "slow_start_recover": module.params['slow_start_recover'] if 'slow_start_recover' in module.params else 15,
            "slow_start_rate": module.params['slow_start_rate'] if 'slow_start_rate' in module.params else 0,
            "slow_start_from": module.params['slow_start_from'] if 'slow_start_from' in module.params else 128,
            "slow_start_step": module.params['slow_start_step'] if 'slow_start_step' in module.params else 2,
            "slow_start_interval": module.params['slow_start_interval'] if 'slow_start_interval' in module.params else 10,
            "slow_start_interval_num": module.params['slow_start_interval_num'] if 'slow_start_interval_num' in module.params else 6,
            "slow_start_tail": module.params['slow_start_tail'] if 'slow_start_tail' in module.params else 4096,
            "request_rate_limit": module.params['request_rate_limit'] if 'request_rate_limit' in module.params else 0
        }
    }

    # 转换为JSON格式
    post_data = json.dumps(node_data)

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
        module.fail_json(msg="编辑节点失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑节点", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_node(module):
    """删除节点"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除节点需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.del" % (
        ip, authkey)

    # 构造节点数据
    node_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(node_data)

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
        module.fail_json(msg="删除节点失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除节点", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_node_port(module):
    """添加节点端口"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加节点端口需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.add" % (
        ip, authkey)

    # 获取端口参数
    port_params = {}
    port_fields = [
        'port_number', 'protocol', 'status', 'weight', 'graceful_time',
        'graceful_delete', 'graceful_disable', 'graceful_persist',
        'conn_limit', 'phm_profile', 'healthcheck', 'upnum', 'nat_strategy'
    ]

    for field in port_fields:
        param_name = field.replace('.', '_')
        if param_name in module.params and module.params[param_name] is not None:
            port_params[field.replace('port_', '')] = module.params[param_name]

    # 构造节点端口数据
    node_data = {
        "name": name,
        "port": port_params
    }

    # 转换为JSON格式
    post_data = json.dumps(node_data)

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
        module.fail_json(msg="添加节点端口失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加节点端口", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_node_port(module):
    """编辑节点端口"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑节点端口需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.edit" % (
        ip, authkey)

    # 获取端口参数
    port_params = {}
    port_fields = [
        'port_number', 'protocol', 'status', 'weight', 'graceful_time',
        'graceful_delete', 'graceful_disable', 'graceful_persist',
        'conn_limit', 'phm_profile', 'healthcheck', 'upnum', 'nat_strategy'
    ]

    for field in port_fields:
        param_name = field.replace('.', '_')
        if param_name in module.params and module.params[param_name] is not None:
            port_params[field.replace('port_', '')] = module.params[param_name]

    # 构造节点端口数据
    node_data = {
        "name": name,
        "port": port_params
    }

    # 转换为JSON格式
    post_data = json.dumps(node_data)

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
        module.fail_json(msg="编辑节点端口失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑节点端口", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_node_port(module):
    """删除节点端口"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除节点端口需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.del" % (
        ip, authkey)

    # 获取端口参数
    port_params = {}
    port_fields = ['port_number', 'protocol']

    for field in port_fields:
        param_name = field.replace('.', '_')
        if param_name in module.params and module.params[param_name] is not None:
            port_params[field.replace('port_', '')] = module.params[param_name]

    # 构造节点端口数据
    node_data = {
        "name": name,
        "port": port_params
    }

    # 转换为JSON格式
    post_data = json.dumps(node_data)

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
        module.fail_json(msg="删除节点端口失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除节点端口", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")



def adc_node_onoff(module):
    """节点启用/禁用"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    enable = module.params['enable'] if 'enable' in module.params else True

    if not name:
        module.fail_json(msg="节点启用/禁用需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.onoff" % (ip, authkey)

    request_data = {
        "name": name,
        "enable": 1 if enable else 0
    }

    post_data = json.dumps(request_data)
    response_data = ""

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
        module.fail_json(msg="节点启用/禁用失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "节点启用/禁用", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_node_port_onoff(module):
    """节点端口启用/禁用"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    port = module.params['port'] if 'port' in module.params else 0
    enable = module.params['enable'] if 'enable' in module.params else True

    if not name:
        module.fail_json(msg="节点端口启用/禁用需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.onoff" % (ip, authkey)

    request_data = {
        "name": name,
        "port": port,
        "enable": 1 if enable else 0
    }

    post_data = json.dumps(request_data)
    response_data = ""

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


def adc_node_stat_list(module):
    """节点统计列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.stat.list" % (ip, authkey)

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
        module.fail_json(msg="节点统计列表获取失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="节点统计列表获取失败", response=parsed_data)
            else:
                module.exit_json(changed=False, stats=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_node_stat_get(module):
    """节点统计详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    if not name:
        module.fail_json(msg="获取节点统计详情需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.stat.get" % (ip, authkey)

    request_data = {"name": name}
    post_data = json.dumps(request_data)
    response_data = ""

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
        module.fail_json(msg="节点统计详情获取失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="节点统计详情获取失败", response=parsed_data)
            else:
                module.exit_json(changed=False, stat=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_node_stat_clear(module):
    """节点统计清除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.stat.clear" % (ip, authkey)

    request_data = {}
    if name:
        request_data["name"] = name

    post_data = json.dumps(request_data)
    response_data = ""

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
        module.fail_json(msg="节点统计清除失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "节点统计清除", True)
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
                    'get_nodes', 'list_nodes', 'get_node', 'add_node', 'edit_node', 'delete_node', 'add_node_port', 'edit_node_port', 'delete_node_port', 'node_onoff', 'node_port_onoff', 'node_stat_list', 'node_stat_get', 'node_stat_clear']),
        # add_node/edit_node参数
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
        # add_node_port/edit_node_port/delete_node_port参数
        port_port_number=dict(type='int', required=False),
        port_protocol=dict(type='int', required=False),
        port_status=dict(type='int', required=False),
        port_weight=dict(type='int', required=False),
        port_graceful_time=dict(type='int', required=False),
        port_graceful_delete=dict(type='int', required=False),
        port_graceful_disable=dict(type='int', required=False),
        port_graceful_persist=dict(type='int', required=False),
        port_conn_limit=dict(type='int', required=False),
        port_phm_profile=dict(type='str', required=False),
        port_healthcheck=dict(type='str', required=False),
        port_upnum=dict(type='int', required=False),
        port_nat_strategy=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action'] if 'action' in module.params else ''
    # 为了解决静态检查工具的问题，我们进行类型转换
    if hasattr(action, '__str__'):
        action = str(action)

    if action == 'get_nodes':
        adc_get_nodes(module)
    elif action == 'list_nodes':
        adc_list_nodes(module)
    elif action == 'get_node':
        adc_get_node(module)
    elif action == 'add_node':
        adc_add_node(module)
    elif action == 'edit_node':
        adc_edit_node(module)
    elif action == 'delete_node':
        adc_delete_node(module)
    elif action == 'add_node_port':
        adc_add_node_port(module)
    elif action == 'edit_node_port':
        adc_edit_node_port(module)
    elif action == 'delete_node_port':
        adc_delete_node_port(module)
    elif action == 'node_onoff':
        adc_node_onoff(module)
    elif action == 'node_port_onoff':
        adc_node_port_onoff(module)
    elif action == 'node_stat_list':
        adc_node_stat_list(module)
    elif action == 'node_stat_get':
        adc_node_stat_get(module)
    elif action == 'node_stat_clear':
        adc_node_stat_clear(module)




if __name__ == '__main__':
    main()
