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


def adc_snmp_comm_item_add(module):
    """添加SNMP团体字"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    community = module.params['community']
    host = module.params['host']

    # 检查必需参数
    if not community or not host:
        module.fail_json(msg="添加SNMP团体字需要提供community和host参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.comm.item.add" % (
        ip, authkey)

    # 构造团体字数据
    community_data = {
        "community": community,
        "host": host
    }

    # 转换为JSON格式
    post_data = json.dumps(community_data)

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
        module.fail_json(msg="添加SNMP团体字失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加SNMP团体字", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_snmp_comm_item_list(module):
    """获取SNMP团体字列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.comm.item.list" % (
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
        module.fail_json(msg="获取SNMP团体字列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMP团体字列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, communities=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_snmp_comm_item_del(module):
    """删除SNMP团体字"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    community = module.params['community']
    host = module.params['host']

    # 检查必需参数
    if not community or not host:
        module.fail_json(msg="删除SNMP团体字需要提供community和host参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.comm.item.del" % (
        ip, authkey)

    # 构造团体字数据
    community_data = {
        "community": community,
        "host": host
    }

    # 转换为JSON格式
    post_data = json.dumps(community_data)

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
        module.fail_json(msg="删除SNMP团体字失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除SNMP团体字", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_snmp_server_set(module):
    """设置SNMP服务配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.set" % (
        ip, authkey)

    # 构造SNMP服务配置数据
    server_data = {}

    # 添加可选参数
    if 'status' in module.params and module.params['status'] is not None:
        server_data['status'] = module.params['status']
    if 'port' in module.params and module.params['port'] is not None:
        server_data['port'] = module.params['port']
    if 'contact' in module.params and module.params['contact'] is not None:
        server_data['contact'] = module.params['contact']
    if 'location' in module.params and module.params['location'] is not None:
        server_data['location'] = module.params['location']

    # 转换为JSON格式
    post_data = json.dumps(server_data)

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
        module.fail_json(msg="设置SNMP服务配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置SNMP服务配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_snmp_server_get(module):
    """获取SNMP服务配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.get" % (
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
        module.fail_json(msg="获取SNMP服务配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMP服务配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, server_config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_snmp_trap_item_add(module):
    """添加SNMP TRAP"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    community = module.params['community']
    host = module.params['host']

    # 检查必需参数
    if not community or not host:
        module.fail_json(msg="添加SNMP TRAP需要提供community和host参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.trap.item.add" % (
        ip, authkey)

    # 构造TRAP数据
    trap_data = {
        "community": community,
        "host": host
    }

    # 添加可选参数
    if 'port' in module.params and module.params['port'] is not None:
        trap_data['port'] = module.params['port']
    if 'version' in module.params and module.params['version'] is not None:
        trap_data['version'] = module.params['version']

    # 转换为JSON格式
    post_data = json.dumps(trap_data)

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
        module.fail_json(msg="添加SNMP TRAP失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加SNMP TRAP", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_snmp_trap_item_list(module):
    """获取SNMP TRAP列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.trap.item.list" % (
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
        module.fail_json(msg="获取SNMP TRAP列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMP TRAP列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, traps=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_snmp_trap_item_del(module):
    """删除SNMP TRAP"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    community = module.params['community']
    host = module.params['host']

    # 检查必需参数
    if not community or not host:
        module.fail_json(msg="删除SNMP TRAP需要提供community和host参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.trap.item.del" % (
        ip, authkey)

    # 构造TRAP数据
    trap_data = {
        "community": community,
        "host": host
    }

    # 添加可选参数
    if 'version' in module.params and module.params['version'] is not None:
        trap_data['version'] = module.params['version']

    # 转换为JSON格式
    post_data = json.dumps(trap_data)

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
        module.fail_json(msg="删除SNMP TRAP失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除SNMP TRAP", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_snmp_trap_set(module):
    """设置SNMP TRAP配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.trap.set" % (
        ip, authkey)

    # 构造TRAP配置数据
    trap_data = {}

    # 添加可选参数
    if 'status' in module.params and module.params['status'] is not None:
        trap_data['status'] = module.params['status']

    # 转换为JSON格式
    post_data = json.dumps(trap_data)

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
        module.fail_json(msg="设置SNMP TRAP配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置SNMP TRAP配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_snmp_trap_get(module):
    """获取SNMP TRAP配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.trap.get" % (
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
        module.fail_json(msg="获取SNMP TRAP配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMP TRAP配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, trap_config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'snmp_comm_item_add', 'snmp_comm_item_list', 'snmp_comm_item_del',
            'snmp_server_set', 'snmp_server_get',
            'snmp_trap_item_add', 'snmp_trap_item_list', 'snmp_trap_item_del',
            'snmp_trap_set', 'snmp_trap_get']),
        # SNMP团体字参数
        community=dict(type='str', required=False),
        host=dict(type='str', required=False),
        # SNMP服务配置参数
        status=dict(type='int', required=False),
        port=dict(type='int', required=False),
        contact=dict(type='str', required=False),
        location=dict(type='str', required=False),
        # SNMP TRAP参数
        version=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'snmp_comm_item_add':
        adc_snmp_comm_item_add(module)
    elif action == 'snmp_comm_item_list':
        adc_snmp_comm_item_list(module)
    elif action == 'snmp_comm_item_del':
        adc_snmp_comm_item_del(module)
    elif action == 'snmp_server_set':
        adc_snmp_server_set(module)
    elif action == 'snmp_server_get':
        adc_snmp_server_get(module)
    elif action == 'snmp_trap_item_add':
        adc_snmp_trap_item_add(module)
    elif action == 'snmp_trap_item_list':
        adc_snmp_trap_item_list(module)
    elif action == 'snmp_trap_item_del':
        adc_snmp_trap_item_del(module)
    elif action == 'snmp_trap_set':
        adc_snmp_trap_set(module)
    elif action == 'snmp_trap_get':
        adc_snmp_trap_get(module)


if __name__ == '__main__':
    main()
