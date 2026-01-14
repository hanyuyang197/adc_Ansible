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


def system_partition_list(module):
    """获取分区列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.partition.list" % (
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
        module.fail_json(msg="获取分区列表失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取分区列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, partitions=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def system_partition_get(module):
    """获取指定分区"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取指定分区需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.partition.get" % (
        ip, authkey)

    # 构造分区数据
    partition_data = {
        "name": name
    }

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            import urllib.parse as urllib_parse
            post_data = json.dumps(partition_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            import urllib as urllib_parse
            post_data = json.dumps(partition_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取指定分区失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取指定分区", False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_partition_add(module):
    """添加分区"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    partition_id = module.params['partition_id']
    max_erules = module.params['max_erules']
    network = module.params['network']
    active = module.params['active']

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加分区需要提供name参数")

    if network is None:
        module.fail_json(msg="添加分区需要提供network参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.partition.add" % (
        ip, authkey)

    # 构造分区数据
    partition_data = {
        "name": name
    }

    # 添加可选参数
    if partition_id is not None:
        partition_data["id"] = partition_id
    if max_erules is not None:
        partition_data["max-erules"] = max_erules
    if network is not None:
        partition_data["network"] = network
    if active is not None:
        partition_data["active"] = active

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(partition_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(partition_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="添加分区失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加分区", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_partition_edit(module):
    """编辑指定分区"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    partition_id = module.params['partition_id']
    max_erules = module.params['max_erules']
    network = module.params['network']
    active = module.params['active']

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑指定分区需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.partition.set" % (
        ip, authkey)

    # 构造分区数据
    partition_data = {
        "name": name
    }

    # 添加可选参数
    if partition_id is not None:
        partition_data["id"] = partition_id
    if max_erules is not None:
        partition_data["max-erules"] = max_erules
    if network is not None:
        partition_data["network"] = network
    if active is not None:
        partition_data["active"] = active

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(partition_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(partition_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="编辑指定分区失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑指定分区", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_partition_del(module):
    """删除指定分区"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除指定分区需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.partition.del" % (
        ip, authkey)

    # 构造分区数据
    partition_data = {
        "name": name
    }

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(partition_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(partition_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="删除指定分区失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除指定分区", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_partition_active(module):
    """切换不同分区"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="切换不同分区需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.partition.active" % (
        ip, authkey)

    # 构造分区数据
    partition_data = {
        "name": name
    }

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(partition_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(partition_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="切换不同分区失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "切换不同分区", True)
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
            'system_partition_list', 'system_partition_get', 'system_partition_add', 'system_partition_edit', 'system_partition_del', 'system_partition_active']),
        # 分区参数
        name=dict(type='str', required=False),
        partition_id=dict(type='int', required=False),
        max_erules=dict(type='int', required=False),
        network=dict(type='int', required=False),
        active=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'system_partition_list':
        system_partition_list(module)
    elif action == 'system_partition_get':
        system_partition_get(module)
    elif action == 'system_partition_add':
        system_partition_add(module)
    elif action == 'system_partition_edit':
        system_partition_edit(module)
    elif action == 'system_partition_del':
        system_partition_del(module)
    elif action == 'system_partition_active':
        system_partition_active(module)


if __name__ == '__main__':
    main()
