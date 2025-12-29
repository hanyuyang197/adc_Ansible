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


def adc_interface_ethernet_list(module):
    """获取以太网接口列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.list" % (ip, authkey)

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
        module.fail_json(msg="获取以太网接口列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取以太网接口列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interfaces=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_interface_ethernet_list_withcommon(module):
    """获取以太网接口列表（包含公共接口）"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.list.withcommon" % (ip, authkey)

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
        module.fail_json(msg="获取以太网接口列表（包含公共接口）失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取以太网接口列表（包含公共接口）失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interfaces=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_interface_ethernet_list_withused(module):
    """获取以太网接口列表（包含已使用接口）"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.list.withused" % (ip, authkey)

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
        module.fail_json(msg="获取以太网接口列表（包含已使用接口）失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取以太网接口列表（包含已使用接口）失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interfaces=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_interface_ethernet_list_self(module):
    """获取以太网接口列表（自身接口）"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.list.self" % (ip, authkey)

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
        module.fail_json(msg="获取以太网接口列表（自身接口）失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取以太网接口列表（自身接口）失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interfaces=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_interface_ethernet_get(module):
    """获取以太网接口详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    slot = module.params['slot']
    port = module.params['port']

    # 检查必需参数
    if slot is None or port is None:
        module.fail_json(msg="获取以太网接口详情需要提供slot和port参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.get" % (ip, authkey)

    # 构造请求数据
    request_data = {
        "slot": slot,
        "port": port
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
        module.fail_json(msg="获取以太网接口详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取以太网接口详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interface=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_interface_ethernet_edit(module):
    """编辑以太网接口配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    slot = module.params['slot']
    port = module.params['port']

    # 检查必需参数
    if slot is None or port is None:
        module.fail_json(msg="编辑以太网接口配置需要提供slot和port参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.edit" % (ip, authkey)

    # 构造请求数据
    request_data = {
        "slot": slot,
        "port": port
    }

    # 添加可选参数
    if module.params['status'] is not None:
        request_data['status'] = module.params['status']
    if module.params['description'] is not None:
        request_data['description'] = module.params['description']
    if module.params['management_services'] is not None:
        request_data['management_services'] = module.params['management_services']
    if module.params['service_ipv4_acl'] is not None:
        request_data['service_ipv4_acl'] = module.params['service_ipv4_acl']
    if module.params['service_ipv6_acl'] is not None:
        request_data['service_ipv6_acl'] = module.params['service_ipv6_acl']
    if module.params['ipv6_nat_dir'] is not None:
        request_data['ipv6_nat_dir'] = module.params['ipv6_nat_dir']
    if module.params['mac_addr'] is not None:
        request_data['mac_addr'] = module.params['mac_addr']
    if module.params['ipv4_addr'] is not None:
        request_data['ipv4_addr'] = module.params['ipv4_addr']
    if module.params['ipv4_mask'] is not None:
        request_data['ipv4_mask'] = module.params['ipv4_mask']
    if module.params['dhcp_client'] is not None:
        request_data['dhcp_client'] = module.params['dhcp_client']
    if module.params['ipv4_acl'] is not None:
        request_data['ipv4_acl'] = module.params['ipv4_acl']
    if module.params['ipv4_list'] is not None:
        request_data['ipv4_list'] = module.params['ipv4_list']
    if module.params['ipv6_list'] is not None:
        request_data['ipv6_list'] = module.params['ipv6_list']
    if module.params['ipv6_addr'] is not None:
        request_data['ipv6_addr'] = module.params['ipv6_addr']
    if module.params['ipv6_prefix'] is not None:
        request_data['ipv6_prefix'] = module.params['ipv6_prefix']
    if module.params['ipv6_anycast'] is not None:
        request_data['ipv6_anycast'] = module.params['ipv6_anycast']
    if module.params['ipv6_local_auto'] is not None:
        request_data['ipv6_local_auto'] = module.params['ipv6_local_auto']
    if module.params['ipv6_local_addr'] is not None:
        request_data['ipv6_local_addr'] = module.params['ipv6_local_addr']
    if module.params['ipv6_local_prefix'] is not None:
        request_data['ipv6_local_prefix'] = module.params['ipv6_local_prefix']
    if module.params['ipv6_local_anycast'] is not None:
        request_data['ipv6_local_anycast'] = module.params['ipv6_local_anycast']
    if module.params['ipv6_acl'] is not None:
        request_data['ipv6_acl'] = module.params['ipv6_acl']
    if module.params['speed'] is not None:
        request_data['speed'] = module.params['speed']
    if module.params['duplexity'] is not None:
        request_data['duplexity'] = module.params['duplexity']
    if module.params['flow_control'] is not None:
        request_data['flow_control'] = module.params['flow_control']
    if module.params['permit_wildcard'] is not None:
        request_data['permit_wildcard'] = module.params['permit_wildcard']
    if module.params['grat_arp'] is not None:
        request_data['grat_arp'] = module.params['grat_arp']
    if module.params['nat_dir'] is not None:
        request_data['nat_dir'] = module.params['nat_dir']
    if module.params['no_vlan_forward'] is not None:
        request_data['no_vlan_forward'] = module.params['no_vlan_forward']
    if module.params['icmp_rate_limit'] is not None:
        request_data['icmp_rate_limit'] = module.params['icmp_rate_limit']
    if module.params['icmp_lock_up_rate'] is not None:
        request_data['icmp_lock_up_rate'] = module.params['icmp_lock_up_rate']
    if module.params['icmp_lock_up_time'] is not None:
        request_data['icmp_lock_up_time'] = module.params['icmp_lock_up_time']
    if module.params['lldp_mode'] is not None:
        request_data['lldp_mode'] = module.params['lldp_mode']
    if module.params['lldp_attr'] is not None:
        request_data['lldp_attr'] = module.params['lldp_attr']

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
        module.fail_json(msg="编辑以太网接口配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑以太网接口配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_interface_ethernet_statis(module):
    """获取接口统计信息"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.statis" % (ip, authkey)

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
        module.fail_json(msg="获取接口统计信息失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取接口统计信息", True)
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
        action=dict(type='str', required=True, choices=['list', 'list_withcommon', 'list_withused', 'list_self', 'get', 'edit', 'statis']),
        # 以太网接口参数
        slot=dict(type='int', required=False),
        port=dict(type='int', required=False),
        status=dict(type='int', required=False),
        description=dict(type='str', required=False),
        management_services=dict(type='list', required=False),
        service_ipv4_acl=dict(type='int', required=False),
        service_ipv6_acl=dict(type='str', required=False),
        ipv6_nat_dir=dict(type='int', required=False),
        mac_addr=dict(type='str', required=False),
        ipv4_addr=dict(type='str', required=False),
        ipv4_mask=dict(type='str', required=False),
        dhcp_client=dict(type='int', required=False),
        ipv4_acl=dict(type='int', required=False),
        ipv4_list=dict(type='list', required=False),
        ipv6_list=dict(type='list', required=False),
        ipv6_addr=dict(type='str', required=False),
        ipv6_prefix=dict(type='int', required=False),
        ipv6_anycast=dict(type='int', required=False),
        ipv6_local_auto=dict(type='int', required=False),
        ipv6_local_addr=dict(type='str', required=False),
        ipv6_local_prefix=dict(type='int', required=False),
        ipv6_local_anycast=dict(type='int', required=False),
        ipv6_acl=dict(type='str', required=False),
        speed=dict(type='int', required=False),
        duplexity=dict(type='int', required=False),
        flow_control=dict(type='int', required=False),
        permit_wildcard=dict(type='int', required=False),
        grat_arp=dict(type='int', required=False),
        nat_dir=dict(type='int', required=False),
        no_vlan_forward=dict(type='int', required=False),
        icmp_rate_limit=dict(type='int', required=False),
        icmp_lock_up_rate=dict(type='int', required=False),
        icmp_lock_up_time=dict(type='int', required=False),
        lldp_mode=dict(type='int', required=False),
        lldp_attr=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list':
        adc_interface_ethernet_list(module)
    elif action == 'list_withcommon':
        adc_interface_ethernet_list_withcommon(module)
    elif action == 'list_withused':
        adc_interface_ethernet_list_withused(module)
    elif action == 'list_self':
        adc_interface_ethernet_list_self(module)
    elif action == 'get':
        adc_interface_ethernet_get(module)
    elif action == 'edit':
        adc_interface_ethernet_edit(module)
    elif action == 'statis':
        adc_interface_ethernet_statis(module)


if __name__ == '__main__':
    main()
