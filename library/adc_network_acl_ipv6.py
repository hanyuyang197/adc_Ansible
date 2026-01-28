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


def acl_ipv6_ext_list(module):
    """获取IPv6访问列表列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.list" % (
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
        module.fail_json(msg="获取IPv6访问列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv6访问列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, acls=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def acl_ipv6_ext_get(module):
    """获取IPv6访问列表详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    acl_name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not acl_name:
        module.fail_json(msg="获取IPv6访问列表详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.get" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {
        "name": acl_name
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
        module.fail_json(msg="获取IPv6访问列表详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv6访问列表详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, acl=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def acl_ipv6_ext_item_add(module):
    """添加IPv6访问列表条目"""
    device_ip = module.params['ip']
    authkey = module.params['authkey']
    acl_name = module.params['name'] if 'name' in module.params else ""
    seq_num = module.params['seq_num'] if 'seq_num' in module.params else ""
    sequence = module.params['sequence'] if 'sequence' in module.params else ""

    # 检查必需参数，支持 seq_num 或 sequence
    if not acl_name:
        module.fail_json(msg="添加IPv6访问列表条目需要提供name参数")
    if not seq_num and not sequence:
        module.fail_json(msg="添加IPv6访问列表条目需要提供seq_num或sequence参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.item.add" % (
        device_ip, authkey)

    # 构造ACL条目数据 - 使用API要求的字段名
    acl_data = {
        "name": acl_name,
        "sequence": sequence if sequence else seq_num
    }

    # 参数映射：模块参数名 -> API字段名
    param_mapping = {
        'acl_action': 'acl_action',
        'src_addr': 'src_ip',
        'src_ip': 'src_ip',
        'src_prefix': 'src_mask',
        'src_mask': 'src_mask',
        'dst_addr': 'dst_ip',
        'dst_ip': 'dst_ip',
        'dst_prefix': 'dst_mask',
        'dst_mask': 'dst_mask',
        'protocol': 'protocol',
        'src_port_op': None,  # API 不使用这个字段
        'src_port1': 'src_port_min',
        'src_port_min': 'src_port_min',
        'src_port2': 'src_port_max',
        'src_port_max': 'src_port_max',
        'dst_port_op': None,  # API 不使用这个字段
        'dst_port1': 'dst_port_min',
        'dst_port_min': 'dst_port_min',
        'dst_port2': 'dst_port_max',
        'dst_port_max': 'dst_port_max',
        'icmp_type': None,  # IPv6 API 不使用这个字段
        'icmp_code': None,  # IPv6 API 不使用这个字段
        'dscp': 'dscp',
        'fragment': None,  # IPv6 API 使用 ip_fragments
        'ip_fragments': 'ip_fragments',
        'log': None,  # API 不使用这个字段
        'time_range': None,  # API 不使用这个字段
        'hits': 'hits'
    }

    # 添加可选参数，使用映射后的字段名
    for param, api_field in param_mapping.items():
        if param in module.params and module.params[param] is not None and api_field is not None:
            acl_data[api_field] = module.params[param]

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
        module.fail_json(msg="添加IPv6访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加IPv6访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def acl_ipv6_ext_item_edit(module):
    """编辑IPv6访问列表条目"""
    device_ip = module.params['ip']
    authkey = module.params['authkey']
    acl_name = module.params['name'] if 'name' in module.params else ""
    seq_num = module.params['seq_num'] if 'seq_num' in module.params else ""
    sequence = module.params['sequence'] if 'sequence' in module.params else ""

    # 检查必需参数，支持 seq_num 或 sequence
    if not acl_name:
        module.fail_json(msg="编辑IPv6访问列表条目需要提供name参数")
    if not seq_num and not sequence:
        module.fail_json(msg="编辑IPv6访问列表条目需要提供seq_num或sequence参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.item.edit" % (
        device_ip, authkey)

    # 构造ACL条目数据 - 使用API要求的字段名
    acl_data = {
        "name": acl_name,
        "sequence": sequence if sequence else seq_num
    }

    # 参数映射：模块参数名 -> API字段名
    param_mapping = {
        'acl_action': 'acl_action',
        'src_addr': 'src_ip',
        'src_ip': 'src_ip',
        'src_prefix': 'src_mask',
        'src_mask': 'src_mask',
        'dst_addr': 'dst_ip',
        'dst_ip': 'dst_ip',
        'dst_prefix': 'dst_mask',
        'dst_mask': 'dst_mask',
        'protocol': 'protocol',
        'src_port_op': None,  # API 不使用这个字段
        'src_port1': 'src_port_min',
        'src_port_min': 'src_port_min',
        'src_port2': 'src_port_max',
        'src_port_max': 'src_port_max',
        'dst_port_op': None,  # API 不使用这个字段
        'dst_port1': 'dst_port_min',
        'dst_port_min': 'dst_port_min',
        'dst_port2': 'dst_port_max',
        'dst_port_max': 'dst_port_max',
        'icmp_type': None,  # IPv6 API 不使用这个字段
        'icmp_code': None,  # IPv6 API 不使用这个字段
        'dscp': 'dscp',
        'fragment': None,  # IPv6 API 使用 ip_fragments
        'ip_fragments': 'ip_fragments',
        'log': None,  # API 不使用这个字段
        'time_range': None,  # API 不使用这个字段
        'hits': 'hits'
    }

    # 添加可选参数，使用映射后的字段名
    for param, api_field in param_mapping.items():
        if param in module.params and module.params[param] is not None and api_field is not None:
            acl_data[api_field] = module.params[param]

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
        module.fail_json(msg="编辑IPv6访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑IPv6访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def acl_ipv6_ext_item_del(module):
    """删除IPv6访问列表条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    acl_name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not acl_name:
        module.fail_json(msg="删除IPv6访问列表条目需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.item.del" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {
        "name": acl_name
    }

    # 如果提供了seq_num参数，则添加到请求数据中
    if 'seq_num' in module.params and module.params['seq_num'] is not None:
        acl_data['seq_num'] = module.params['seq_num']

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
        module.fail_json(msg="删除IPv6访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除IPv6访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def acl_ipv6_ext_desc_set(module):
    """设置IPv6访问列表描述"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    acl_name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not acl_name:
        module.fail_json(msg="设置IPv6访问列表描述需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.desc.set" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {
        "name": acl_name
    }

    # 添加可选参数
    if 'description' in module.params and module.params['description'] is not None:
        acl_data['description'] = module.params['description']

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
        module.fail_json(msg="设置IPv6访问列表描述失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置IPv6访问列表描述", True)
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
            'acl_ipv6_ext_list', 'acl_ipv6_ext_get', 'acl_ipv6_ext_item_add', 'acl_ipv6_ext_item_edit', 'acl_ipv6_ext_item_del', 'acl_ipv6_ext_desc_set']),
        # ACL参数
        name=dict(type='str', required=False),
        seq_num=dict(type='int', required=False),
        sequence=dict(type='int', required=False),
        acl_action=dict(type='str', required=False),
        src_addr=dict(type='str', required=False),
        src_ip=dict(type='str', required=False),
        src_prefix=dict(type='int', required=False),
        src_mask=dict(type='int', required=False),
        dst_addr=dict(type='str', required=False),
        dst_ip=dict(type='str', required=False),
        dst_prefix=dict(type='int', required=False),
        dst_mask=dict(type='int', required=False),
        protocol=dict(type='str', required=False),
        src_port_op=dict(type='str', required=False),
        src_port1=dict(type='int', required=False),
        src_port_min=dict(type='int', required=False),
        src_port2=dict(type='int', required=False),
        src_port_max=dict(type='int', required=False),
        dst_port_op=dict(type='str', required=False),
        dst_port1=dict(type='int', required=False),
        dst_port_min=dict(type='int', required=False),
        dst_port2=dict(type='int', required=False),
        dst_port_max=dict(type='int', required=False),
        icmp_type=dict(type='int', required=False),
        icmp_code=dict(type='int', required=False),
        dscp=dict(type='int', required=False),
        fragment=dict(type='str', required=False),
        ip_fragments=dict(type='int', required=False),
        log=dict(type='int', required=False),
        time_range=dict(type='str', required=False),
        hits=dict(type='str', required=False),
        description=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'acl_ipv6_ext_list':
        acl_ipv6_ext_list(module)
    elif action == 'acl_ipv6_ext_get':
        acl_ipv6_ext_get(module)
    elif action == 'acl_ipv6_ext_item_add':
        acl_ipv6_ext_item_add(module)
    elif action == 'acl_ipv6_ext_item_edit':
        acl_ipv6_ext_item_edit(module)
    elif action == 'acl_ipv6_ext_item_del':
        acl_ipv6_ext_item_del(module)
    elif action == 'acl_ipv6_ext_desc_set':
        acl_ipv6_ext_desc_set(module)


if __name__ == '__main__':
    main()
