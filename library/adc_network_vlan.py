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


def adc_list_vlans(module):
    """获取VLAN列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.vlan.list" % (
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
        module.fail_json(msg="获取VLAN列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取VLAN列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, vlans=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_vlan(module):
    """获取VLAN详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="获取VLAN详情需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.vlan.get" % (
        ip, authkey)

    # 构造请求数据
    vlan_data = {
        "id": id
    }

    # 转换为JSON格式
    post_data = json.dumps(vlan_data)

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
        module.fail_json(msg="获取VLAN详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取VLAN详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, vlan=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_vlan(module):
    """添加VLAN"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="添加VLAN需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.vlan.add" % (
        ip, authkey)

    # 构造VLAN数据
    vlan_data = {
        "id": id,
        "description": module.params['description'] if 'description' in module.params else "",
        "l2_fwd_disable": module.params['l2_fwd_disable'] if 'l2_fwd_disable' in module.params else 1,
        "path_persist": module.params['path_persist'] if 'path_persist' in module.params else 0,
        "ve_if": module.params['ve_if'] if 've_if' in module.params else 0
    }

    # 添加接口列表（如果有提供）
    if 'interface_list' in module.params and module.params['interface_list']:
        vlan_data['interface_list'] = module.params['interface_list']

    # 添加汇聚口列表（如果有提供）
    if 'trunk_list' in module.params and module.params['trunk_list']:
        vlan_data['trunk_list'] = module.params['trunk_list']

    # 转换为JSON格式
    post_data = json.dumps(vlan_data)

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
        module.fail_json(msg="添加VLAN失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加VLAN", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_vlan(module):
    """编辑VLAN"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="编辑VLAN需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.vlan.edit" % (
        ip, authkey)

    # 构造VLAN数据
    vlan_data = {
        "id": id
    }

    # 添加可选参数
    if 'description' in module.params and module.params['description'] is not None:
        vlan_data['description'] = module.params['description']
    if 'l2_fwd_disable' in module.params and module.params['l2_fwd_disable'] is not None:
        vlan_data['l2_fwd_disable'] = module.params['l2_fwd_disable']
    if 'path_persist' in module.params and module.params['path_persist'] is not None:
        vlan_data['path_persist'] = module.params['path_persist']
    if 've_if' in module.params and module.params['ve_if'] is not None:
        vlan_data['ve_if'] = module.params['ve_if']

    # 添加接口列表（如果有提供）
    if 'interface_list' in module.params and module.params['interface_list'] is not None:
        vlan_data['interface_list'] = module.params['interface_list']

    # 添加汇聚口列表（如果有提供）
    if 'trunk_list' in module.params and module.params['trunk_list'] is not None:
        vlan_data['trunk_list'] = module.params['trunk_list']

    # 转换为JSON格式
    post_data = json.dumps(vlan_data)

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
        module.fail_json(msg="编辑VLAN失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑VLAN", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_vlan(module):
    """删除VLAN"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="删除VLAN需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.vlan.del" % (
        ip, authkey)

    # 构造请求数据
    vlan_data = {
        "id": id
    }

    # 转换为JSON格式
    post_data = json.dumps(vlan_data)

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
        module.fail_json(msg="删除VLAN失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除VLAN", True)
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
            'list_vlans', 'get_vlan', 'add_vlan', 'edit_vlan', 'delete_vlan']),
        # VLAN参数
        id=dict(type='int', required=False),
        description=dict(type='str', required=False),
        l2_fwd_disable=dict(type='int', required=False),
        path_persist=dict(type='int', required=False),
        ve_if=dict(type='int', required=False),
        interface_list=dict(type='list', required=False),
        trunk_list=dict(type='list', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list_vlans':
        adc_list_vlans(module)
    elif action == 'get_vlan':
        adc_get_vlan(module)
    elif action == 'add_vlan':
        adc_add_vlan(module)
    elif action == 'edit_vlan':
        adc_edit_vlan(module)
    elif action == 'delete_vlan':
        adc_delete_vlan(module)


if __name__ == '__main__':
    main()
