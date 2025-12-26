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


def adc_list_acls(module):
    """获取IPv4标准访问列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.std.list" % (
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
        module.fail_json(msg="获取IPv4标准访问列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv4标准访问列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, acls=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_acl(module):
    """获取IPv4标准访问列表详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="获取IPv4标准访问列表详情需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.std.get" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {
        "id": id
    }

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="获取IPv4标准访问列表详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv4标准访问列表详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, acl=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_acl_item(module):
    """添加IPv4标准访问列表条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""
    sequence = module.params['sequence'] if 'sequence' in module.params else ""

    # 检查必需参数
    if not id or not sequence:
        module.fail_json(msg="添加IPv4标准访问列表条目需要提供id和sequence参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.std.item.add" % (
        ip, authkey)

    # 构造ACL条目数据 - 只包含在YAML中明确定义的参数
    acl_data = {
        "id": id,
        "sequence": sequence
    }

    # 定义可选参数列表
    optional_params = [
        'acl_action', 'src_ip', 'src_mask'
    ]

    # 添加可选参数
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            acl_data[param] = module.params[param]

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="添加IPv4标准访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加IPv4标准访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_acl_item(module):
    """编辑IPv4标准访问列表条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""
    sequence = module.params['sequence'] if 'sequence' in module.params else ""

    # 检查必需参数
    if not id or not sequence:
        module.fail_json(msg="编辑IPv4标准访问列表条目需要提供id和sequence参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.std.item.edit" % (
        ip, authkey)

    # 构造ACL条目数据
    acl_data = {
        "id": id,
        "sequence": sequence
    }

    # 添加可选参数
    if 'acl_action' in module.params and module.params['acl_action'] is not None:
        acl_data['acl_action'] = module.params['acl_action']
    if 'src_ip' in module.params and module.params['src_ip'] is not None:
        acl_data['src_ip'] = module.params['src_ip']
    if 'src_mask' in module.params and module.params['src_mask'] is not None:
        acl_data['src_mask'] = module.params['src_mask']

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="编辑IPv4标准访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑IPv4标准访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_acl_item(module):
    """删除IPv4标准访问列表条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="删除IPv4标准访问列表条目需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.std.item.del" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {
        "id": id
    }

    # 如果提供了sequence参数，则添加到请求数据中
    if 'sequence' in module.params and module.params['sequence'] is not None:
        acl_data['sequence'] = module.params['sequence']

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="删除IPv4标准访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除IPv4标准访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_set_acl_description(module):
    """设置IPv4标准访问列表描述"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""
    description = module.params['description'] if 'description' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="设置IPv4标准访问列表描述需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.std.desc.set" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {
        "id": id,
        "description": description
    }

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="设置IPv4标准访问列表描述失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置IPv4标准访问列表描述", True)
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
            'list_acls', 'get_acl', 'add_acl_item', 'edit_acl_item', 'delete_acl_item', 'set_acl_description']),
        # ACL参数
        id=dict(type='int', required=False),
        sequence=dict(type='int', required=False),
        acl_action=dict(type='int', required=False),
        src_ip=dict(type='str', required=False),
        src_mask=dict(type='str', required=False),
        description=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list_acls':
        adc_list_acls(module)
    elif action == 'get_acl':
        adc_get_acl(module)
    elif action == 'add_acl_item':
        adc_add_acl_item(module)
    elif action == 'edit_acl_item':
        adc_edit_acl_item(module)
    elif action == 'delete_acl_item':
        adc_delete_acl_item(module)
    elif action == 'set_acl_description':
        adc_set_acl_description(module)


if __name__ == '__main__':
    main()
