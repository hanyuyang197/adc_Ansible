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


def trunk_list(module):
    """获取TRUNK列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.trunk.list" % (
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
        module.fail_json(msg="获取TRUNK列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TRUNK列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, trunks=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def trunk_get(module):
    """获取TRUNK详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="获取TRUNK详情需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.trunk.get" % (
        ip, authkey)

    # 构造请求数据
    trunk_data = {
        "id": id
    }

    # 转换为JSON格式
    post_data = json.dumps(trunk_data)

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
        module.fail_json(msg="获取TRUNK详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TRUNK详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, trunk=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def trunk_add(module):
    """添加TRUNK"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="添加TRUNK需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.trunk.add" % (
        ip, authkey)

    # 构造TRUNK数据
    trunk_data = {
        "id": id,
        "type": module.params['type'] if 'type' in module.params else 0,
        "status": module.params['status'] if 'status' in module.params else 1
    }

    # 添加接口列表（如果有提供）
    if 'interface_list' in module.params and module.params['interface_list']:
        trunk_data['interface_list'] = module.params['interface_list']

    # 转换为JSON格式
    post_data = json.dumps(trunk_data)

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
        module.fail_json(msg="添加TRUNK失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加TRUNK", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def trunk_edit(module):
    """编辑TRUNK"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="编辑TRUNK需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.trunk.edit" % (
        ip, authkey)

    # 构造TRUNK数据
    trunk_data = {
        "id": id,
        "type": module.params['type'] if 'type' in module.params else 0
    }

    # 添加可选参数
    if 'status' in module.params and module.params['status'] is not None:
        trunk_data['status'] = module.params['status']

    # 添加接口列表（如果有提供）
    if 'interface_list' in module.params and module.params['interface_list'] is not None:
        trunk_data['interface_list'] = module.params['interface_list']

    # 转换为JSON格式
    post_data = json.dumps(trunk_data)

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
        module.fail_json(msg="编辑TRUNK失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑TRUNK", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def trunk_delete(module):
    """删除TRUNK"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="删除TRUNK需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.trunk.del" % (
        ip, authkey)

    # 构造请求数据
    trunk_data = {
        "id": id
    }

    # 转换为JSON格式
    post_data = json.dumps(trunk_data)

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
        module.fail_json(msg="删除TRUNK失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除TRUNK", True)
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
            'trunk_list', 'trunk_get', 'trunk_add', 'trunk_edit', 'trunk_delete']),
        # TRUNK参数
        id=dict(type='int', required=False),
        type=dict(type='int', required=False),
        status=dict(type='int', required=False),
        interface_list=dict(type='list', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'trunk_list':
        trunk_list(module)
    elif action == 'trunk_get':
        trunk_get(module)
    elif action == 'trunk_add':
        trunk_add(module)
    elif action == 'trunk_edit':
        trunk_edit(module)
    elif action == 'trunk_delete':
        trunk_delete(module)


if __name__ == '__main__':
    main()
