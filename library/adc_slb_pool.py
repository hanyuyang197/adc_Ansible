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


def adc_get_pools(module):
    """获取服务池列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.list" % (
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
        module.fail_json(msg="获取服务池列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取服务池列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, pools=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_pool(module):
    """获取服务池详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取服务池详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.get" % (
        ip, authkey)

    # 构造请求数据
    pool_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="获取服务池详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取服务池详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, pool=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_pool(module):
    """添加服务池"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.add" % (
        ip, authkey)

    # 构造服务池数据
    pool_data = {
        "pool": {
            "name": module.params['name'] if 'name' in module.params else "",
            "protocol": module.params['protocol'] if 'protocol' in module.params else 0,
            "lb_method": module.params['lb_method'] if 'lb_method' in module.params else 0,
            "upnum": module.params['upnum'] if 'upnum' in module.params else 0,
            "healthcheck": module.params['healthcheck'] if 'healthcheck' in module.params else "",
            "desc_pool": module.params['desc_pool'] if 'desc_pool' in module.params else "",
            "action_on_service_down": module.params['action_on_service_down'] if 'action_on_service_down' in module.params else 0,
            "aux_node_log": module.params['aux_node_log'] if 'aux_node_log' in module.params else 0
        }
    }

    # 处理up_members_at_least参数
    up_members_at_least = {}
    if 'up_members_at_least_status' in module.params and module.params['up_members_at_least_status'] is not None:
        up_members_at_least['status'] = module.params['up_members_at_least_status']
    if 'up_members_at_least_num' in module.params and module.params['up_members_at_least_num'] is not None:
        up_members_at_least['num'] = module.params['up_members_at_least_num']
    if 'up_members_at_least_type' in module.params and module.params['up_members_at_least_type'] is not None:
        up_members_at_least['type'] = module.params['up_members_at_least_type']

    if up_members_at_least:
        pool_data['pool']['up-members-at-least'] = up_members_at_least

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="添加服务池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加服务池", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_pool(module):
    """编辑服务池"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑服务池需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.edit" % (
        ip, authkey)

    # 构造服务池数据
    pool_data = {
        "pool": {
            "name": name,
            "protocol": module.params['protocol'] if 'protocol' in module.params else 0,
            "lb_method": module.params['lb_method'] if 'lb_method' in module.params else 0,
            "healthcheck": module.params['healthcheck'] if 'healthcheck' in module.params else "",
            "desc_pool": module.params['desc_pool'] if 'desc_pool' in module.params else "",
            "action_on_service_down": module.params['action_on_service_down'] if 'action_on_service_down' in module.params else 0,
            "aux_node_log": module.params['aux_node_log'] if 'aux_node_log' in module.params else 0
        }
    }

    # 处理up_members_at_least参数
    if 'up_members_at_least_status' in module.params and module.params['up_members_at_least_status'] is not None:
        if 'up-members-at-least' not in pool_data['pool']:
            pool_data['pool']['up-members-at-least'] = {}
        pool_data['pool']['up-members-at-least']['status'] = module.params['up_members_at_least_status']

    if 'up_members_at_least_num' in module.params and module.params['up_members_at_least_num'] is not None:
        if 'up-members-at-least' not in pool_data['pool']:
            pool_data['pool']['up-members-at-least'] = {}
        pool_data['pool']['up-members-at-least']['num'] = module.params['up_members_at_least_num']

    if 'up_members_at_least_type' in module.params and module.params['up_members_at_least_type'] is not None:
        if 'up-members-at-least' not in pool_data['pool']:
            pool_data['pool']['up-members-at-least'] = {}
        pool_data['pool']['up-members-at-least']['type'] = module.params['up_members_at_least_type']

    # 处理upnum参数
    if 'upnum' in module.params and module.params['upnum'] is not None:
        pool_data['pool']['upnum'] = module.params['upnum']

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="编辑服务池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑服务池", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_pool(module):
    """删除服务池"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除服务池需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.del" % (
        ip, authkey)

    # 构造服务池数据
    pool_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="删除服务池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除服务池", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_pool_node(module):
    """添加节点到服务池"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    pool_name = module.params['pool_name'] if 'pool_name' in module.params else ""
    node = module.params['node'] if 'node' in module.params else ""
    port = module.params['port'] if 'port' in module.params else 0
    protocol = module.params['protocol'] if 'protocol' in module.params else 0
    priority = module.params['priority'] if 'priority' in module.params else 1
    weight = module.params['weight'] if 'weight' in module.params else 1
    status = module.params['status'] if 'status' in module.params else 1
    conn_limit = module.params['conn_limit'] if 'conn_limit' in module.params else 0

    # 检查必需参数
    if not pool_name:
        module.fail_json(msg="添加节点到服务池需要提供pool_name参数")
    if not node:
        module.fail_json(msg="添加节点到服务池需要提供node参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.member.add" % (
        ip, authkey)

    # 构造请求数据
    pool_data = {
        "name": pool_name,
        "member": {
            "nodename": node,
            "server": node,
            "port": port,
            "protocol": protocol,
            "priority": priority,
            "weight": weight,
            "status": status,
            "conn_limit": conn_limit
        }
    }

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="添加节点到服务池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加节点到服务池", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_pool_node(module):
    """从服务池删除节点"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    pool_name = module.params['pool_name'] if 'pool_name' in module.params else ""
    node = module.params['node'] if 'node' in module.params else ""
    port = module.params['port'] if 'port' in module.params else 0
    protocol = module.params['protocol'] if 'protocol' in module.params else 0

    # 检查必需参数
    if not pool_name:
        module.fail_json(msg="从服务池删除节点需要提供pool_name参数")
    if not node:
        module.fail_json(msg="从服务池删除节点需要提供node参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.member.del" % (
        ip, authkey)

    # 构造请求数据
    pool_data = {
        "name": pool_name,
        "member": {
            "nodename": node,
            "server": node,
            "port": port,
            "protocol": protocol
        }
    }

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="从服务池删除节点失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "从服务池删除节点", True)
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
                    'get_pools', 'get_pool', 'add_pool', 'edit_pool', 'delete_pool', 'add_pool_node', 'delete_pool_node']),
        # 服务池参数
        name=dict(type='str', required=False),
        protocol=dict(type='int', required=False),
        lb_method=dict(type='int', required=False),
        upnum=dict(type='int', required=False),
        healthcheck=dict(type='str', required=False),
        desc_pool=dict(type='str', required=False),
        action_on_service_down=dict(type='int', required=False),
        aux_node_log=dict(type='int', required=False),
        # up_members_at_least参数
        up_members_at_least_status=dict(type='int', required=False),
        up_members_at_least_num=dict(type='int', required=False),
        up_members_at_least_type=dict(type='int', required=False),
        # 服务池成员参数
        pool_name=dict(type='str', required=False),
        node=dict(type='str', required=False),
        port=dict(type='int', required=False),
        priority=dict(type='int', required=False),
        weight=dict(type='int', required=False),
        status=dict(type='int', required=False),
        conn_limit=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    # 为了解决静态检查工具的问题，我们进行类型转换
    action = module.params['action']
    if hasattr(action, '__str__'):
        action = str(action)

    if action == 'get_pools':
        adc_get_pools(module)
    elif action == 'get_pool':
        adc_get_pool(module)
    elif action == 'add_pool':
        adc_add_pool(module)
    elif action == 'edit_pool':
        adc_edit_pool(module)
    elif action == 'delete_pool':
        adc_delete_pool(module)
    elif action == 'add_pool_node':
        adc_add_pool_node(module)
    elif action == 'delete_pool_node':
        adc_delete_pool_node(module)


if __name__ == '__main__':
    main()
