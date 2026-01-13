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


def adc_list_vas(module):
    """获取虚拟地址列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.list" % (
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
        module.fail_json(msg="获取虚拟地址列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取虚拟地址列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, virtual_addresses=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_va(module):
    """获取虚拟地址详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取虚拟地址详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.get" % (ip, authkey)

    # 构造请求数据
    va_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(va_data)

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
        module.fail_json(msg="获取虚拟地址详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取虚拟地址详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, virtual_address=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_va(module):
    """添加虚拟地址"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    va_type = module.params['va_type'] if 'va_type' in module.params else "ipv4"

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.add" % (ip, authkey)

    # 构造虚拟地址数据 - 只包含在YAML中明确定义的参数
    va_data = {
        "virtual_address": {}
    }

    # 添加必需参数（如果提供）
    if 'name' in module.params and module.params['name']:
        va_data['virtual_address']['name'] = module.params['name']
    if 'tc_name' in module.params and module.params['tc_name']:
        va_data['virtual_address']['tc_name'] = module.params['tc_name']

    # 添加可选参数（只包含实际定义的参数）
    if 'status' in module.params and module.params['status'] is not None:
        va_data['virtual_address']['status'] = module.params['status']
    if 'arp_status' in module.params and module.params['arp_status'] is not None:
        va_data['virtual_address']['arp_status'] = module.params['arp_status']
    if 'vrid' in module.params and module.params['vrid'] is not None:
        va_data['virtual_address']['vrid'] = module.params['vrid']
    if 'redistribution' in module.params and module.params['redistribution'] is not None:
        va_data['virtual_address']['redistribution'] = module.params['redistribution']
    if 'policy_profile' in module.params and module.params['policy_profile']:
        va_data['virtual_address']['policy_profile'] = module.params['policy_profile']
    if 'natlog_profile' in module.params and module.params['natlog_profile']:
        va_data['virtual_address']['natlog_profile'] = module.params['natlog_profile']
    if 'virtual_services' in module.params and module.params['virtual_services']:
        va_data['virtual_address']['virtual_services'] = module.params['virtual_services']

    # 根据类型添加特定参数
    if va_type == "ipv4" or va_type == "ipv6":
        # IPv4/IPv6类型的虚拟地址
        if 'address' in module.params and module.params['address']:
            va_data['virtual_address']['address'] = module.params['address']
        if 'icmp_probe' in module.params and module.params['icmp_probe'] is not None:
            va_data['virtual_address']['icmp_probe'] = module.params['icmp_probe']
    elif va_type == "subnet":
        # 子网类型的虚拟地址
        subnet_data = {}
        if 'subnet_address' in module.params and module.params['subnet_address']:
            subnet_data['address'] = module.params['subnet_address']
        if 'subnet_mask_len' in module.params and module.params['subnet_mask_len'] is not None:
            subnet_data['mask_len'] = module.params['subnet_mask_len']
        if subnet_data:
            va_data['virtual_address']['subnet'] = subnet_data
        if 'icmp_probe' in module.params and module.params['icmp_probe'] is not None:
            va_data['virtual_address']['icmp_probe'] = module.params['icmp_probe']
    elif va_type == "acl_ipv4":
        # IPv4 ACL类型的虚拟地址
        if 'acl_id' in module.params and module.params['acl_id'] is not None:
            va_data['virtual_address']['acl_id'] = module.params['acl_id']
        if 'icmp_probe' in module.params and module.params['icmp_probe'] is not None:
            va_data['virtual_address']['icmp_probe'] = module.params['icmp_probe']
    elif va_type == "acl_ipv6":
        # IPv6 ACL类型的虚拟地址
        if 'acl_name' in module.params and module.params['acl_name']:
            va_data['virtual_address']['acl_name'] = module.params['acl_name']
        if 'icmp_disable' in module.params and module.params['icmp_disable'] is not None:
            va_data['virtual_address']['icmp_disable'] = module.params['icmp_disable']

    # 转换为JSON格式
    post_data = json.dumps(va_data)

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
        module.fail_json(msg="添加虚拟地址失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加虚拟地址", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_va(module):
    """编辑虚拟地址"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑虚拟地址需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.edit" % (
        ip, authkey)

    # 构造虚拟地址数据 - 只包含在YAML中明确定义的参数
    va_data = {
        "virtual_address": {
            "name": name  # name是必需参数，必须包含
        }
    }

    # 添加可选参数（只包含实际定义的参数）
    if 'tc_name' in module.params and module.params['tc_name']:
        va_data['virtual_address']['tc_name'] = module.params['tc_name']
    if 'status' in module.params and module.params['status'] is not None:
        va_data['virtual_address']['status'] = module.params['status']
    if 'arp_status' in module.params and module.params['arp_status'] is not None:
        va_data['virtual_address']['arp_status'] = module.params['arp_status']
    if 'vrid' in module.params and module.params['vrid'] is not None:
        va_data['virtual_address']['vrid'] = module.params['vrid']
    if 'redistribution' in module.params and module.params['redistribution'] is not None:
        va_data['virtual_address']['redistribution'] = module.params['redistribution']
    if 'policy_profile' in module.params and module.params['policy_profile']:
        va_data['virtual_address']['policy_profile'] = module.params['policy_profile']
    if 'natlog_profile' in module.params and module.params['natlog_profile']:
        va_data['virtual_address']['natlog_profile'] = module.params['natlog_profile']
    if 'address' in module.params and module.params['address']:
        va_data['virtual_address']['address'] = module.params['address']
    if 'icmp_probe' in module.params and module.params['icmp_probe'] is not None:
        va_data['virtual_address']['icmp_probe'] = module.params['icmp_probe']
    if 'subnet_address' in module.params and module.params['subnet_address']:
        subnet_data = {}
        subnet_data['address'] = module.params['subnet_address']
        if 'subnet_mask_len' in module.params and module.params['subnet_mask_len'] is not None:
            subnet_data['mask_len'] = module.params['subnet_mask_len']
        va_data['virtual_address']['subnet'] = subnet_data
    if 'acl_id' in module.params and module.params['acl_id'] is not None:
        va_data['virtual_address']['acl_id'] = module.params['acl_id']
    if 'acl_name' in module.params and module.params['acl_name']:
        va_data['virtual_address']['acl_name'] = module.params['acl_name']
    if 'icmp_disable' in module.params and module.params['icmp_disable'] is not None:
        va_data['virtual_address']['icmp_disable'] = module.params['icmp_disable']
    if 'virtual_services' in module.params and module.params['virtual_services']:
        va_data['virtual_address']['virtual_services'] = module.params['virtual_services']

    # 转换为JSON格式
    post_data = json.dumps(va_data)

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
        module.fail_json(msg="编辑虚拟地址失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑虚拟地址", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_va(module):
    """删除虚拟地址"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除虚拟地址需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.del" % (ip, authkey)

    # 构造虚拟地址数据
    va_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(va_data)

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
        module.fail_json(msg="删除虚拟地址失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除虚拟地址", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_va_stat_list(module):
    """获取虚拟应用统计列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.stat.list" % (ip, authkey)

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

        # 对于获取列表操作，直接返回响应数据，不判断success
        if response_data:
            try:
                parsed_data = json.loads(response_data)
                # 检查是否有错误信息
                if 'errmsg' in parsed_data and parsed_data['errmsg']:
                    module.fail_json(msg="获取虚拟应用统计列表失败", response=parsed_data)
                else:
                    module.exit_json(changed=False, va_stats=parsed_data)
            except Exception as e:
                module.fail_json(msg="解析响应失败: %s" % str(e))
        else:
            module.fail_json(msg="未收到有效响应")

    except Exception as e:
        module.fail_json(msg="获取虚拟应用统计列表失败: %s" % str(e))


def adc_va_stat_get(module):
    """获取虚拟应用统计详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params.get('name')

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取虚拟应用统计详情需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.stat.get" % (ip, authkey)

    # 构造请求数据
    stat_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(stat_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, data=post_data.encode('utf-8'), method='POST')
            req.add_header('Content-Type', 'application/json')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data)
            req.add_header('Content-Type', 'application/json')
            req.get_method = lambda: 'POST'
            response = urllib_request.urlopen(req)
            response_data = response.read()

        # 解析响应
        result = json.loads(response_data)

        # 检查响应状态
        if result.get('status') == 'success':
            module.exit_json(changed=False, va_stat=result)
        else:
            module.fail_json(msg="获取虚拟应用统计详情失败: " + result.get('message', '未知错误'))

    except Exception as e:
        module.fail_json(msg="获取虚拟应用统计详情请求失败: %s" % str(e))





def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
                    'list_vas', 'get_va', 'add_va', 'edit_va', 'delete_va',
                    'va_stat_list', 'va_stat_get']),
        # 虚拟地址参数
        name=dict(type='str', required=False),
        va_type=dict(type='str', required=False, choices=[
                     'ipv4', 'ipv6', 'subnet', 'acl_ipv4', 'acl_ipv6']),
        tc_name=dict(type='str', required=False),
        address=dict(type='str', required=False),
        status=dict(type='int', required=False),
        arp_status=dict(type='int', required=False),
        icmp_probe=dict(type='int', required=False),
        icmp_disable=dict(type='int', required=False),
        vrid=dict(type='int', required=False),
        redistribution=dict(type='int', required=False),
        policy_profile=dict(type='str', required=False),
        natlog_profile=dict(type='str', required=False),
        virtual_services=dict(type='list', required=False),
        # 子网类型参数
        subnet_address=dict(type='str', required=False),
        subnet_mask_len=dict(type='int', required=False),
        # ACL类型参数
        acl_id=dict(type='int', required=False),
        acl_name=dict(type='str', required=False)
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

    if action == 'list_vas':
        adc_list_vas(module)
    elif action == 'get_va':
        adc_get_va(module)
    elif action == 'add_va':
        adc_add_va(module)
    elif action == 'edit_va':
        adc_edit_va(module)
    elif action == 'delete_va':
        adc_delete_va(module)
    elif action == 'va_stat_list':
        adc_va_stat_list(module)
    elif action == 'va_stat_get':
        adc_va_stat_get(module)



if __name__ == '__main__':
    main()
