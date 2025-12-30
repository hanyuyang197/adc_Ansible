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


def adc_arp_ipv4_list(module):
    """获取IPv4 ARP条目列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=arp.ipv4.list" % (
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
        module.fail_json(msg="获取IPv4 ARP条目列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv4 ARP条目列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, arp_entries=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_arp_ipv4_get(module):
    """获取IPv4 ARP条目详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    ip_addr = module.params['ip_addr']

    # 检查必需参数
    if not ip_addr:
        module.fail_json(msg="获取IPv4 ARP条目详情需要提供ip_addr参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=arp.ipv4.get" % (
        ip, authkey)

    # 构造请求数据
    request_data = {
        "ip_addr": ip_addr
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
        module.fail_json(msg="获取IPv4 ARP条目详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv4 ARP条目详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, arp_entry=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_arp_ipv4_add(module):
    """添加IPv4 ARP条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    ip_addr = module.params['ip_addr']
    mac_addr = module.params['mac_addr']

    # 检查必需参数
    if not ip_addr or not mac_addr:
        module.fail_json(msg="添加IPv4 ARP条目需要提供ip_addr和mac_addr参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=arp.ipv4.add" % (
        ip, authkey)

    # 构造请求数据
    request_data = {
        "ip_addr": ip_addr,
        "mac_addr": mac_addr
    }

    # 添加可选参数
    if module.params['port_type'] is not None:
        request_data['port_type'] = module.params['port_type']
    if module.params['slot_num'] is not None:
        request_data['slot_num'] = module.params['slot_num']
    if module.params['port_num'] is not None:
        request_data['port_num'] = module.params['port_num']

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
        module.fail_json(msg="添加IPv4 ARP条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加IPv4 ARP条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_arp_ipv4_edit(module):
    """编辑IPv4 ARP条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    ip_addr = module.params['ip_addr']

    # 检查必需参数
    if not ip_addr:
        module.fail_json(msg="编辑IPv4 ARP条目需要提供ip_addr参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=arp.ipv4.edit" % (
        ip, authkey)

    # 构造请求数据
    request_data = {
        "ip_addr": ip_addr
    }

    # 添加可选参数
    if module.params['mac_addr'] is not None:
        request_data['mac_addr'] = module.params['mac_addr']
    if module.params['port_type'] is not None:
        request_data['port_type'] = module.params['port_type']
    if module.params['slot_num'] is not None:
        request_data['slot_num'] = module.params['slot_num']
    if module.params['port_num'] is not None:
        request_data['port_num'] = module.params['port_num']

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
        module.fail_json(msg="编辑IPv4 ARP条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑IPv4 ARP条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_arp_ipv4_delete(module):
    """删除IPv4 ARP条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    ip_addr = module.params['ip_addr']

    # 检查必需参数
    if not ip_addr:
        module.fail_json(msg="删除IPv4 ARP条目需要提供ip_addr参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=arp.ipv4.del" % (
        ip, authkey)

    # 构造请求数据
    request_data = {
        "ip_addr": ip_addr
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
        module.fail_json(msg="删除IPv4 ARP条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除IPv4 ARP条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_arp_ipv4_statis(module):
    """获取ARP状态信息列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=arp.ipv4.statis" % (
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
        module.fail_json(msg="获取ARP状态信息列表失败: %s" % str(e))

    # 对于获取状态信息操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取ARP状态信息列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, arp_stats=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_arp_ipv4_clear(module):
    """清除动态arp"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=arp.ipv4.clear" % (
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
        module.fail_json(msg="清除动态arp失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "清除动态arp", True)
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
                    'list', 'get', 'add', 'edit', 'delete', 'statis', 'clear']),
        # ARP相关参数
        ip_addr=dict(type='str', required=False),
        mac_addr=dict(type='str', required=False),
        port_type=dict(type='int', required=False),
        slot_num=dict(type='int', required=False),
        port_num=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list':
        adc_arp_ipv4_list(module)
    elif action == 'get':
        adc_arp_ipv4_get(module)
    elif action == 'add':
        adc_arp_ipv4_add(module)
    elif action == 'edit':
        adc_arp_ipv4_edit(module)
    elif action == 'delete':
        adc_arp_ipv4_delete(module)
    elif action == 'statis':
        adc_arp_ipv4_statis(module)
    elif action == 'clear':
        adc_arp_ipv4_clear(module)


if __name__ == '__main__':
    main()
