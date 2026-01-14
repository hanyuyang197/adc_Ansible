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


def nat_network_list(module):
    """获取网络NAT列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.network.list" % (
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
        module.fail_json(msg="获取网络NAT列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取网络NAT列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, networks=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def nat_network_get(module):
    """获取网络NAT详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取网络NAT详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.network.get" % (
        ip, authkey)

    # 构造请求数据
    network_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(network_data)

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
        module.fail_json(msg="获取网络NAT详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取网络NAT详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, network=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def nat_network_add(module):
    """添加网络NAT"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    origin_ip = module.params['origin_ip'] if 'origin_ip' in module.params else ""
    origin_mask = module.params['origin_mask'] if 'origin_mask' in module.params else ""
    nat_ip = module.params['nat_ip'] if 'nat_ip' in module.params else ""
    nat_mask = module.params['nat_mask'] if 'nat_mask' in module.params else ""
    number = module.params['number'] if 'number' in module.params else ""

    # 检查必需参数
    if not name or not origin_ip or not origin_mask or not nat_ip or not nat_mask or not number:
        module.fail_json(
            msg="添加网络NAT需要提供name、origin_ip、origin_mask、nat_ip、nat_mask和number参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.network.add" % (
        ip, authkey)

    # 构造网络NAT数据
    network_data = {
        "name": name,
        "origin_ip": origin_ip,
        "origin_mask": origin_mask,
        "nat_ip": nat_ip,
        "nat_mask": nat_mask,
        "number": number
    }

    # 添加可选参数
    if 'vrrp_id' in module.params and module.params['vrrp_id'] is not None:
        network_data['vrrp_id'] = module.params['vrrp_id']

    # 转换为JSON格式
    post_data = json.dumps(network_data)

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
        module.fail_json(msg="添加网络NAT失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加网络NAT", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def nat_network_edit(module):
    """编辑网络NAT"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑网络NAT需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.network.edit" % (
        ip, authkey)

    # 构造网络NAT数据
    network_data = {
        "name": name
    }

    # 添加可选参数
    if 'origin_ip' in module.params and module.params['origin_ip'] is not None:
        network_data['origin_ip'] = module.params['origin_ip']
    if 'origin_mask' in module.params and module.params['origin_mask'] is not None:
        network_data['origin_mask'] = module.params['origin_mask']
    if 'nat_ip' in module.params and module.params['nat_ip'] is not None:
        network_data['nat_ip'] = module.params['nat_ip']
    if 'nat_mask' in module.params and module.params['nat_mask'] is not None:
        network_data['nat_mask'] = module.params['nat_mask']
    if 'number' in module.params and module.params['number'] is not None:
        network_data['number'] = module.params['number']
    if 'vrrp_id' in module.params and module.params['vrrp_id'] is not None:
        network_data['vrrp_id'] = module.params['vrrp_id']

    # 转换为JSON格式
    post_data = json.dumps(network_data)

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
        module.fail_json(msg="编辑网络NAT失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑网络NAT", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def nat_network_del(module):
    """删除网络NAT"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除网络NAT需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.network.del" % (
        ip, authkey)

    # 构造请求数据
    network_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(network_data)

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
        module.fail_json(msg="删除网络NAT失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除网络NAT", True)
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
            'nat_network_list', 'nat_network_get', 'nat_network_add', 'nat_network_edit', 'nat_network_delete']),
        # 网络NAT参数
        name=dict(type='str', required=False),
        origin_ip=dict(type='str', required=False),
        origin_mask=dict(type='str', required=False),
        nat_ip=dict(type='str', required=False),
        nat_mask=dict(type='str', required=False),
        number=dict(type='int', required=False),
        vrrp_id=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'nat_network_list':
        nat_network_list(module)
    elif action == 'nat_network_get':
        nat_network_get(module)
    elif action == 'nat_network_add':
        nat_network_add(module)
    elif action == 'nat_network_edit':
        nat_network_edit(module)
    elif action == 'nat_network_delete':
        nat_network_del(module)


if __name__ == '__main__':
    main()
