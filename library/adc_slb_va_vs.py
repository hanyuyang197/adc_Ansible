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


def slb_va_vs_add(module):
    """添加虚拟服务"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    va_name = module.params['va_name'] if 'va_name' in module.params else ""

    # 检查必需参数
    if not va_name:
        module.fail_json(msg="添加虚拟服务需要提供va_name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.vs.add" % (
        ip, authkey)

    # 构造虚拟服务数据 - 只包含在YAML中明确定义的参数
    vs_data = {
        "name": va_name,
        "virtual_service": {}
    }

    # 定义可选参数列表
    optional_params = [
        'name', 'protocol', 'port', 'vs_enable_intf', 'status', 'path_persist',
        'desc_vport', 'snat_on_vip', 'auto_snat', 'send_reset', 'source_nat',
        'srcip_persist', 'dstip_persist', 'cookie_persist', 'sslid_persis',
        'policy_profile', 'aclsnats', 'connection_mirror', 'no_dest_nat',
        'immediate_action_on_service_down', 'vport_template_name',
        'traffic_control', 'service_last_hop', 'force_update_mac',
        'snat_port_preserve_enable', 'snat_port_preserve_type', 'pool',
        'vs_acl_id', 'aclnamev6', 'erules', 'connection_limit_status',
        'connection_limit_number', 'udp_profile', 'dns_profile', 'tcp_profile',
        'ftp_profile', 'http_profile', 'connmulti_profile', 'tcpagent_profile',
        'waf_profile', 'cache_profile', 'request_log_profile', 'serverssl_profile',
        'clientssl_profile', 'rtsp_profile', 'smtp_profile', 'sip_profile',
        'fixup_ftp'
    ]

    # 添加基本参数
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            if param in ['connection_limit_status', 'connection_limit_number']:
                # 特殊处理连接限制参数
                if 'connection_limit' not in vs_data['virtual_service']:
                    vs_data['virtual_service']['connection_limit'] = {}
                vs_data['virtual_service']['connection_limit'][param.replace(
                    'connection_limit_', '')] = module.params[param]
            else:
                vs_data['virtual_service'][param] = module.params[param]

    # 特殊处理syncookie参数
    if 'syncookie' in module.params and module.params['syncookie'] is not None:
        vs_data['virtual_service']['syncookie'] = {
            "syncookie": module.params['syncookie']
        }

    # 根据协议类型添加特定参数
    protocol = module.params['protocol'] if 'protocol' in module.params and module.params['protocol'] is not None else 2
    if protocol == 22:  # DNS
        # DNS类型参数
        if 'udp_profile' in module.params and module.params['udp_profile']:
            vs_data['virtual_service']['udp_profile'] = module.params['udp_profile']
        if 'dns_profile' in module.params and module.params['dns_profile']:
            vs_data['virtual_service']['dns_profile'] = module.params['dns_profile']
    elif protocol == 9:  # FTP
        # FTP类型参数
        if 'tcp_profile' in module.params and module.params['tcp_profile']:
            vs_data['virtual_service']['tcp_profile'] = module.params['tcp_profile']
        # FTP特有参数
        if 'ftp_profile' in module.params and module.params['ftp_profile']:
            vs_data['virtual_service']['ftp_profile'] = module.params['ftp_profile']
    elif protocol == 12:  # HTTP普通
        # HTTP普通类型参数
        if 'tcp_profile' in module.params and module.params['tcp_profile']:
            vs_data['virtual_service']['tcp_profile'] = module.params['tcp_profile']
        if 'http_profile' in module.params and module.params['http_profile']:
            vs_data['virtual_service']['http_profile'] = module.params['http_profile']
        if 'connmulti_profile' in module.params and module.params['connmulti_profile']:
            vs_data['virtual_service']['connmulti_profile'] = module.params['connmulti_profile']
    elif protocol == 14:  # HTTP增强
        # HTTP增强类型参数
        if 'tcpagent_profile' in module.params and module.params['tcpagent_profile']:
            vs_data['virtual_service']['tcpagent_profile'] = module.params['tcpagent_profile']
        if 'http_profile' in module.params and module.params['http_profile']:
            vs_data['virtual_service']['http_profile'] = module.params['http_profile']
        if 'connmulti_profile' in module.params and module.params['connmulti_profile']:
            vs_data['virtual_service']['connmulti_profile'] = module.params['connmulti_profile']
        if 'waf_profile' in module.params and module.params['waf_profile']:
            vs_data['virtual_service']['waf_profile'] = module.params['waf_profile']
        if 'cache_profile' in module.params and module.params['cache_profile']:
            vs_data['virtual_service']['cache_profile'] = module.params['cache_profile']
        if 'request_log_profile' in module.params and module.params['request_log_profile']:
            vs_data['virtual_service']['request_log_profile'] = module.params['request_log_profile']
    elif protocol == 15:  # HTTPS
        # HTTPS类型参数
        if 'tcpagent_profile' in module.params and module.params['tcpagent_profile']:
            vs_data['virtual_service']['tcpagent_profile'] = module.params['tcpagent_profile']
        if 'http_profile' in module.params and module.params['http_profile']:
            vs_data['virtual_service']['http_profile'] = module.params['http_profile']
        if 'connmulti_profile' in module.params and module.params['connmulti_profile']:
            vs_data['virtual_service']['connmulti_profile'] = module.params['connmulti_profile']
        if 'waf_profile' in module.params and module.params['waf_profile']:
            vs_data['virtual_service']['waf_profile'] = module.params['waf_profile']
        if 'cache_profile' in module.params and module.params['cache_profile']:
            vs_data['virtual_service']['cache_profile'] = module.params['cache_profile']
        if 'serverssl_profile' in module.params and module.params['serverssl_profile']:
            vs_data['virtual_service']['serverssl_profile'] = module.params['serverssl_profile']
        if 'clientssl_profile' in module.params and module.params['clientssl_profile']:
            vs_data['virtual_service']['clientssl_profile'] = module.params['clientssl_profile']
    elif protocol == 8:  # RTSP
        # RTSP类型参数
        if 'tcp_profile' in module.params and module.params['tcp_profile']:
            vs_data['virtual_service']['tcp_profile'] = module.params['tcp_profile']
        if 'rtsp_profile' in module.params and module.params['rtsp_profile']:
            vs_data['virtual_service']['rtsp_profile'] = module.params['rtsp_profile']
    elif protocol == 17:  # SMTP
        # SMTP类型参数
        if 'tcpagent_profile' in module.params and module.params['tcpagent_profile']:
            vs_data['virtual_service']['tcpagent_profile'] = module.params['tcpagent_profile']
        if 'smtp_profile' in module.params and module.params['smtp_profile']:
            vs_data['virtual_service']['smtp_profile'] = module.params['smtp_profile']
        if 'clientssl_profile' in module.params and module.params['clientssl_profile']:
            vs_data['virtual_service']['clientssl_profile'] = module.params['clientssl_profile']
    elif protocol == 11:  # SIP
        # SIP类型参数
        if 'udp_profile' in module.params and module.params['udp_profile']:
            vs_data['virtual_service']['udp_profile'] = module.params['udp_profile']
        if 'sip_profile' in module.params and module.params['sip_profile']:
            vs_data['virtual_service']['sip_profile'] = module.params['sip_profile']
    elif protocol == 18:  # SIP-TCP
        # SIP-TCP类型参数
        if 'tcp_profile' in module.params and module.params['tcp_profile']:
            vs_data['virtual_service']['tcp_profile'] = module.params['tcp_profile']
        if 'sip_profile' in module.params and module.params['sip_profile']:
            vs_data['virtual_service']['sip_profile'] = module.params['sip_profile']
    elif protocol == 20:  # TCP_AGENT
        # TCP_AGENT类型参数
        if 'tcpagent_profile' in module.params and module.params['tcpagent_profile']:
            vs_data['virtual_service']['tcpagent_profile'] = module.params['tcpagent_profile']
        if 'fixup_ftp' in module.params and module.params['fixup_ftp'] is not None:
            vs_data['virtual_service']['fixup_ftp'] = module.params['fixup_ftp']
        if 'serverssl_profile' in module.params and module.params['serverssl_profile']:
            vs_data['virtual_service']['serverssl_profile'] = module.params['serverssl_profile']
    elif protocol == 25:  # TCP-EXCHANGE
        # TCP-EXCHANGE类型参数
        if 'tcpagent_profile' in module.params and module.params['tcpagent_profile']:
            vs_data['virtual_service']['tcpagent_profile'] = module.params['tcpagent_profile']
        if 'connmulti_profile' in module.params and module.params['connmulti_profile']:
            vs_data['virtual_service']['connmulti_profile'] = module.params['connmulti_profile']
    elif protocol == 26:  # MBLB
        # MBLB类型参数
        if 'tcpagent_profile' in module.params and module.params['tcpagent_profile']:
            vs_data['virtual_service']['tcpagent_profile'] = module.params['tcpagent_profile']
        if 'connmulti_profile' in module.params and module.params['connmulti_profile']:
            vs_data['virtual_service']['connmulti_profile'] = module.params['connmulti_profile']
    elif protocol == 23:  # TFTP
        # TFTP类型参数
        if 'udp_profile' in module.params and module.params['udp_profile']:
            vs_data['virtual_service']['udp_profile'] = module.params['udp_profile']
    elif protocol == 2:  # TCP
        # TCP类型参数
        if 'tcp_profile' in module.params and module.params['tcp_profile']:
            vs_data['virtual_service']['tcp_profile'] = module.params['tcp_profile']

    # 转换为JSON格式
    post_data = json.dumps(vs_data)

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
        module.fail_json(msg="添加虚拟服务失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加虚拟服务", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_va_vs_edit(module):
    """编辑虚拟服务"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    va_name = module.params['va_name'] if 'va_name' in module.params else ""

    # 检查必需参数
    if not va_name:
        module.fail_json(msg="编辑虚拟服务需要提供va_name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.vs.edit" % (
        ip, authkey)

    # 构造虚拟服务数据 - 只包含在YAML中明确定义的参数
    vs_data = {
        "name": va_name,
        "virtual_service": {}
    }

    # 只有当参数在YAML中明确定义时才包含在请求中
    optional_params = [
        'name', 'protocol', 'port', 'vs_enable_intf', 'status', 'path_persist',
        'desc_vport', 'snat_on_vip', 'auto_snat', 'send_reset', 'source_nat',
        'srcip_persist', 'dstip_persist', 'cookie_persist', 'sslid_persis',
        'policy_profile', 'aclsnats', 'connection_mirror', 'no_dest_nat',
        'syncookie', 'immediate_action_on_service_down', 'vport_template_name',
        'traffic_control', 'service_last_hop', 'force_update_mac',
        'snat_port_preserve_enable', 'snat_port_preserve_type', 'pool',
        'vs_acl_id', 'aclnamev6', 'erules', 'connection_limit_status',
        'connection_limit_number', 'udp_profile', 'dns_profile', 'tcp_profile',
        'ftp_profile', 'http_profile', 'connmulti_profile', 'tcpagent_profile',
        'waf_profile', 'cache_profile', 'request_log_profile', 'serverssl_profile',
        'clientssl_profile', 'rtsp_profile', 'smtp_profile', 'sip_profile',
        'fixup_ftp'
    ]

    # 添加基本参数
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            if param == 'syncookie':
                # 特殊处理syncookie参数
                vs_data['virtual_service']['syncookie'] = {
                    "syncookie": module.params[param]
                }
            elif param in ['connection_limit_status', 'connection_limit_number']:
                # 特殊处理连接限制参数
                if 'connection_limit' not in vs_data['virtual_service']:
                    vs_data['virtual_service']['connection_limit'] = {}
                vs_data['virtual_service']['connection_limit'][param] = module.params[param]
            else:
                vs_data['virtual_service'][param] = module.params[param]

    # 转换为JSON格式
    post_data = json.dumps(vs_data)

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
        module.fail_json(msg="编辑虚拟服务失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑虚拟服务", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_va_vs_del(module):
    """删除虚拟服务"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    va_name = module.params['va_name'] if 'va_name' in module.params else ""

    # 检查必需参数
    if not va_name:
        module.fail_json(msg="删除虚拟服务需要提供va_name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.vs.del" % (
        ip, authkey)

    # 构造虚拟服务数据
    vs_data = {
        "name": va_name,
        "virtual_service": {
            "protocol": module.params['protocol'] if 'protocol' in module.params else 2,
            "port": module.params['port'] if 'port' in module.params else 80
        }
    }

    # 转换为JSON格式
    post_data = json.dumps(vs_data)

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
        module.fail_json(msg="删除虚拟服务失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除虚拟服务", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_va_vs_get(module):
    """获取虚拟服务详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    va_name = module.params['va_name'] if 'va_name' in module.params else ""

    # 检查必需参数
    if not va_name:
        module.fail_json(msg="获取虚拟服务详情需要提供va_name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.va.vs.get" % (
        ip, authkey)

    # 构造请求数据
    vs_data = {
        "name": va_name,
        "virtual_service": {
            "protocol": module.params['protocol'] if 'protocol' in module.params else 2,
            "port": module.params['port'] if 'port' in module.params else 80
        }
    }

    # 转换为JSON格式
    post_data = json.dumps(vs_data)

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
        module.fail_json(msg="获取虚拟服务详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取虚拟服务详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, virtual_service=parsed_data)
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
                    'slb_va_vs_add', 'slb_va_vs_edit', 'slb_va_vs_del', 'slb_va_vs_get']),
        # 虚拟服务参数
        va_name=dict(type='str', required=False),
        name=dict(type='str', required=False),
        protocol=dict(type='int', required=False),
        port=dict(type='int', required=False),
        pool=dict(type='str', required=False),
        vs_enable_intf=dict(type='str', required=False),
        status=dict(type='int', required=False),
        path_persist=dict(type='int', required=False),
        desc_vport=dict(type='str', required=False),
        snat_on_vip=dict(type='int', required=False),
        auto_snat=dict(type='int', required=False),
        vs_acl_id=dict(type='int', required=False),
        aclnamev6=dict(type='str', required=False),
        erules=dict(type='list', required=False),
        send_reset=dict(type='int', required=False),
        source_nat=dict(type='str', required=False),
        srcip_persist=dict(type='str', required=False),
        dstip_persist=dict(type='str', required=False),
        cookie_persist=dict(type='str', required=False),
        sslid_persis=dict(type='str', required=False),
        policy_profile=dict(type='str', required=False),
        aclsnats=dict(type='list', required=False),
        connection_mirror=dict(type='int', required=False),
        no_dest_nat=dict(type='int', required=False),
        syncookie=dict(type='int', required=False),
        immediate_action_on_service_down=dict(type='int', required=False),
        vport_template_name=dict(type='str', required=False),
        traffic_control=dict(type='str', required=False),
        service_last_hop=dict(type='str', required=False),
        force_update_mac=dict(type='int', required=False),
        snat_port_preserve_enable=dict(type='int', required=False),
        snat_port_preserve_type=dict(type='int', required=False),
        # 连接限制参数
        connection_limit_status=dict(type='int', required=False),
        connection_limit_number=dict(type='int', required=False),
        # 协议特定参数
        udp_profile=dict(type='str', required=False),
        dns_profile=dict(type='str', required=False),
        tcp_profile=dict(type='str', required=False),
        ftp_profile=dict(type='str', required=False),
        http_profile=dict(type='str', required=False),
        waf_profile=dict(type='str', required=False),
        cache_profile=dict(type='str', required=False),
        connmulti_profile=dict(type='str', required=False),
        request_log_profile=dict(type='str', required=False),
        clientssl_profile=dict(type='str', required=False),
        serverssl_profile=dict(type='str', required=False),
        rtsp_profile=dict(type='str', required=False),
        smtp_profile=dict(type='str', required=False),
        sip_profile=dict(type='str', required=False),
        tcpagent_profile=dict(type='str', required=False),
        fixup_ftp=dict(type='int', required=False)
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

    if action == 'slb_va_vs_add':
        slb_va_vs_add(module)
    elif action == 'slb_va_vs_edit':
        slb_va_vs_edit(module)
    elif action == 'slb_va_vs_del':
        slb_va_vs_del(module)
    elif action == 'slb_va_vs_get':
        slb_va_vs_get(module)


if __name__ == '__main__':
    main()
