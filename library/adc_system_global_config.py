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


def format_adc_response_for_ansible(response_data, action="", changed_default=True):
    """
    格式化ADC响应为Ansible模块返回格式
    """
    result = {
        'success': False,
        'result': '',
        'errcode': '',
        'errmsg': '',
        'data': {}
    }

    try:
        if isinstance(response_data, str):
            parsed_data = json.loads(response_data)
        else:
            parsed_data = response_data

        result['data'] = parsed_data
        result['result'] = parsed_data.get('result', '')
        result['errcode'] = parsed_data.get('errcode', '')
        result['errmsg'] = parsed_data.get('errmsg', '')

        if result['result'].lower() == 'success':
            result['success'] = True
        else:
            errmsg = result['errmsg'].lower() if isinstance(
                result['errmsg'], str) else str(result['errmsg']).lower()
            if any(keyword in errmsg for keyword in ['已存在', 'already exists', 'already exist', 'exists']):
                result['success'] = True
                result['result'] = 'success (already exists)'

    except json.JSONDecodeError as e:
        # 直接返回原始响应内容，不尝试解析为JSON
        result['errmsg'] = response_data
        result['errcode'] = 'RAW_RESPONSE'
    except Exception as e:
        result['errmsg'] = "响应解析异常: %s" % str(e)
        result['errcode'] = 'PARSE_EXCEPTION'

    if result['success']:
        result_dict = {
            'changed': changed_default,
            'msg': '%s操作成功' % action if action else '操作成功',
            'response': result['data']
        }

        if 'already exists' in result['result']:
            result_dict['changed'] = False
            result_dict['msg'] = '%s操作成功（资源已存在，无需更改）' % action if action else '操作成功（资源已存在，无需更改）'

        return True, result_dict
    else:
        result_dict = {
            'changed': False,
            'msg': '%s操作失败' % action if action else '操作失败',
            'error': {
                'result': result['result'],
                'errcode': result['errcode'],
                'errmsg': result['errmsg']
            },
            'response': result['data']
        }
        return False, result_dict


def send_request(url, post_data=None):
    """发送HTTP请求的通用函数"""
    response_data = ""
    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            if post_data:
                post_data = post_data.encode('utf-8')
                req = urllib_request.Request(url, data=post_data, method='POST', headers={
                                             'Content-Type': 'application/json'})
            else:
                req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            if post_data:
                post_data = post_data.encode('utf-8')
                req = urllib_request.Request(url, data=post_data, headers={
                                             'Content-Type': 'application/json'})
                req.get_method = lambda: 'POST'
            else:
                req = urllib_request.Request(url)
                req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        raise Exception(str(e))

    # 直接返回响应内容，不尝试解析JSON
    return response_data


def adc_slb_global_allow_promis_intf_vip_get(module):
    """获取 slb 全局混杂配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.global.allow_promis_intf_vip.get" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, global_promis_config=response_data)
    except Exception as e:
        module.fail_json(msg="获取 slb 全局混杂配置失败: %s" % str(e))


def adc_slb_global_allow_promis_intf_vip_set(module):
    """设置 slb 全局混杂配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    status = module.params['status']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.global.allow_promis_intf_vip.set" % (
        ip, authkey)

    config_data = {
        "status": status
    }

    post_data = json.dumps(config_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置 slb 全局混杂配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="设置 slb 全局混杂配置失败: %s" % str(e))


def adc_slb_graceful_shutdown_get(module):
    """获取 slb 全局软关机"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.graceful-shutdown.get" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, graceful_shutdown_config=response_data)
    except Exception as e:
        module.fail_json(msg="获取 slb 全局软关机失败: %s" % str(e))


def adc_slb_graceful_shutdown_set(module):
    """设置 slb 全局软关机"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    time = module.params.get('time')
    delete = module.params.get('delete')
    disable = module.params.get('disable')
    persist = module.params.get('persist')

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.graceful-shutdown.set" % (
        ip, authkey)

    config_data = {
        "graceful_shutdown_node": {}
    }
    
    if time is not None:
        config_data["graceful_shutdown_node"]["time"] = time
    if delete is not None:
        config_data["graceful_shutdown_node"]["delete"] = delete
    if disable is not None:
        config_data["graceful_shutdown_node"]["disable"] = disable
    if persist is not None:
        config_data["graceful_shutdown_node"]["persist"] = persist

    post_data = json.dumps(config_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置 slb 全局软关机", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="设置 slb 全局软关机失败: %s" % str(e))


def adc_system_rate_limit_icmp_get(module):
    """获取 ICMP 速率限制配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.rate_limit_icmp.get" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(chchanged=False, icmp_rate_limit_config=response_data)
    except Exception as e:
        module.fail_json(msg="获取 ICMP 速率限制配置失败: %s" % str(e))


def adc_system_rate_limit_icmp_set(module):
    """设置 ICMP 速率限制配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    normal_rate_limit = module.params.get('normal_rate_limit')
    max_rate_limit = module.params.get('max_rate_limit')
    lockup_period = module.params.get('lockup_period')

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.rate_limit_icmp.set" % (
        ip, authkey)

    config_data = {
        "rate_limit_icmp": {}
    }
    
    if normal_rate_limit is not None:
        config_data["rate_limit_icmp"]["normal_rate_limit"] = normal_rate_limit
    if max_rate_limit is not None:
        config_data["rate_limit_icmp"]["max_rate_limit"] = max_rate_limit
    if lockup_period is not None:
        config_data["rate_limit_icmp"]["lockup_period"] = lockup_period

    post_data = json.dumps(config_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置 ICMP 速率限制配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="设置 ICMP 速率限制配置失败: %s" % str(e))


def adc_system_tcp_syn_protect_get(module):
    """获取 tcp 新建保护配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.tcp_syn_protect.get" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, tcp_syn_protect_config=response_data)
    except Exception as e:
        module.fail_json(msg="获取 tcp 新建保护配置失败: %s" % str(e))


def adc_system_tcp_syn_protect_set(module):
    """设置 tcp 新建保护配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    reset = module.params['reset']
    rate_limit = module.params.get('rate_limit')

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.tcp_syn_protect.set" % (
        ip, authkey)

    config_data = {
        "reset": reset
    }

    if rate_limit is not None:
        config_data["rate_limit"] = rate_limit

    post_data = json.dumps(config_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置 tcp 新建保护配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="设置 tcp 新建保护配置失败: %s" % str(e))


def adc_system_vlan_keyed_connection_get(module):
    """获取 SLB 全局 VLAN 一致性检查"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.vlan_keyed_connection.get" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(
            changed=False, vlan_keyed_connection_config=response_data)
    except Exception as e:
        module.fail_json(msg="获取 SLB 全局 VLAN 一致性检查失败: %s" % str(e))


def adc_system_vlan_keyed_connection_set(module):
    """设置 SLB 全局 VLAN 一致性检查"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    enable = module.params['enable']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.vlan_keyed_connection.set" % (
        ip, authkey)

    config_data = {
        "vlan_keyed_connection": {
            "enable": enable
        }
    }

    post_data = json.dumps(config_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置 SLB 全局 VLAN 一致性检查", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="设置 SLB 全局 VLAN 一致性检查失败: %s" % str(e))


def adc_global_connection_mirror_get(module):
    """获取 SLB 全局连接镜像"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=global.connection_mirror.get" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, connection_mirror_config=response_data)
    except Exception as e:
        module.fail_json(msg="获取 SLB 全局连接镜像失败: %s" % str(e))


def adc_global_connection_mirror_set(module):
    """设置 SLB 全局连接镜像"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    global_connection_mirror = module.params['global_connection_mirror']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=global.connection_mirror.set" % (
        ip, authkey)

    config_data = {
        "global_connection_mirror": global_connection_mirror
    }

    post_data = json.dumps(config_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置 SLB 全局连接镜像", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="设置 SLB 全局连接镜像失败: %s" % str(e))


def adc_global_path_persist_get(module):
    """获取 SLB 全局路径保持"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=global.path_persist.get" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, path_persist_config=response_data)
    except Exception as e:
        module.fail_json(msg="获取 SLB 全局路径保持失败: %s" % str(e))


def adc_global_path_persist_set(module):
    """设置 SLB 全局路径保持"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    global_path_persist = module.params['global_path_persist']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=global.path_persist.set" % (
        ip, authkey)

    config_data = {
        "global_path_persist": global_path_persist
    }

    post_data = json.dumps(config_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置 SLB 全局路径保持", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="设置 SLB 全局路径保持失败: %s" % str(e))


def adc_global_slb_snat_on_vip_get(module):
    """获取 SLB 全局策略地址转换配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=global.slb_snat_on_vip.get" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(chchanged=False, snat_on_vip_config=response_data)
    except Exception as e:
        module.fail_json(msg="获取 SLB 全局策略地址转换配置失败: %s" % str(e))


def adc_global_slb_snat_on_vip_set(module):
    """设置 SLB 全局策略地址转换配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    global_policy_snat = module.params['global_policy_snat']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=global.slb_snat_on_vip.set" % (
        ip, authkey)

    config_data = {
        "global_policy_snat": global_policy_snat
    }

    post_data = json.dumps(config_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置 SLB 全局策略地址转换配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="设置 SLB 全局策略地址转换配置失败: %s" % str(e))


def adc_global_slb_snat_interface_iprr_get(module):
    """获取 SLB 全局源 NAT 接口地址轮询"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=global.slb_snat_interface_iprr.get" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(
            chchanged=False, snat_interface_iprr_config=response_data)
    except Exception as e:
        module.fail_json(msg="获取 SLB 全局源 NAT 接口地址轮询失败: %s" % str(e))


def adc_global_slb_snat_interface_iprr_set(module):
    """设置 SLB 全局源 NAT 接口地址轮询"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    global_snat_interface_iprr = module.params['global_snat_interface_iprr']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=global.slb_snat_interface_iprr.set" % (
        ip, authkey)

    config_data = {
        "global_snat_interface_iprr": global_snat_interface_iprr
    }

    post_data = json.dumps(config_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置 SLB 全局源 NAT 接口地址轮询", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="设置 SLB 全局源 NAT 接口地址轮询失败: %s" % str(e))


def adc_slb_global_virtual_mac_get(module):
    """获取 SLB 全局虚拟 MAC"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.global.virtual_mac.get" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(chchanged=False, virtual_mac_config=response_data)
    except Exception as e:
        module.fail_json(msg="获取 SLB 全局虚拟 MAC 失败: %s" % str(e))


def adc_slb_global_virtual_mac_set(module):
    """设置 SLB 全局虚拟 MAC"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    gvm = module.params['gvm']
    mac = module.params.get('mac')

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.global.virtual_mac.set" % (
        ip, authkey)

    config_data = {
        "gvm": gvm
    }

    if mac is not None:
        config_data["mac"] = mac

    post_data = json.dumps(config_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置 SLB 全局虚拟 MAC", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="设置 SLB 全局虚拟 MAC 失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'slb_global_allow_promis_intf_vip_get', 'slb_global_allow_promis_intf_vip_set',
            'slb_graceful_shutdown_get', 'slb_graceful_shutdown_set',
            'system_rate_limit_icmp_get', 'system_rate_limit_icmp_set',
            'system_tcp_syn_protect_get', 'system_tcp_syn_protect_set',
            'system_vlan_keyed_connection_get', 'system_vlan_keyed_connection_set',
            'global_connection_mirror_get', 'global_connection_mirror_set',
            'global_path_persist_get', 'global_path_persist_set',
            'global_slb_snat_on_vip_get', 'global_slb_snat_on_vip_set',
            'global_slb_snat_interface_iprr_get', 'global_slb_snat_interface_iprr_set',
            'slb_global_virtual_mac_get', 'slb_global_virtual_mac_set'
        ]),
        # 配置参数
        # 用于 global.connection_mirror.set
        global_connection_mirror=dict(type='int', required=False, choices=[0, 1]),
        # 用于 global.path_persist.set
        global_path_persist=dict(type='int', required=False, choices=[0, 1]),
        # 用于 global.slb_snat_on_vip.set
        global_policy_snat=dict(type='int', required=False, choices=[0, 1]),
        # 用于 global.slb_snat_interface_iprr.set
        global_snat_interface_iprr=dict(type='int', required=False, choices=[0, 1]),
        # 用于 slb.global.virtual_mac.set
        gvm=dict(type='int', required=False, choices=[0, 1]),
        # 用于其他需要enable参数的set操作
        enable=dict(type='int', required=False, choices=[0, 1]),
        # 用于rate相关参数
        rate=dict(type='int', required=False),
        # 用于mac相关参数
        mac=dict(type='str', required=False),
        # 用于 system.rate_limit_icmp.set
        normal_rate_limit=dict(type='int', required=False),
        max_rate_limit=dict(type='int', required=False),
        lockup_period=dict(type='int', required=False),
        # 用于 slb.global.allow_promis_intf_vip.set
        status=dict(type='int', required=False, choices=[0, 1]),
        # 用于 system.tcp_syn_protect.set
        reset=dict(type='int', required=False, choices=[0, 1]),
        rate_limit=dict(type='int', required=False),
        # 用于 slb.graceful-shutdown.set
        time=dict(type='int', required=False),
        delete=dict(type='int', required=False, choices=[0, 1]),
        disable=dict(type='int', required=False, choices=[0, 1]),
        persist=dict(type='int', required=False, choices=[0, 1])
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'slb_global_allow_promis_intf_vip_get':
        adc_slb_global_allow_promis_intf_vip_get(module)
    elif action == 'slb_global_allow_promis_intf_vip_set':
        adc_slb_global_allow_promis_intf_vip_set(module)
    elif action == 'slb_graceful_shutdown_get':
        adc_slb_graceful_shutdown_get(module)
    elif action == 'slb_graceful_shutdown_set':
        adc_slb_graceful_shutdown_set(module)
    elif action == 'system_rate_limit_icmp_get':
        adc_system_rate_limit_icmp_get(module)
    elif action == 'system_rate_limit_icmp_set':
        adc_system_rate_limit_icmp_set(module)
    elif action == 'system_tcp_syn_protect_get':
        adc_system_tcp_syn_protect_get(module)
    elif action == 'system_tcp_syn_protect_set':
        adc_system_tcp_syn_protect_set(module)
    elif action == 'system_vlan_keyed_connection_get':
        adc_system_vlan_keyed_connection_get(module)
    elif action == 'system_vlan_keyed_connection_set':
        adc_system_vlan_keyed_connection_set(module)
    elif action == 'global_connection_mirror_get':
        adc_global_connection_mirror_get(module)
    elif action == 'global_connection_mirror_set':
        adc_global_connection_mirror_set(module)
    elif action == 'global_path_persist_get':
        adc_global_path_persist_get(module)
    elif action == 'global_path_persist_set':
        adc_global_path_persist_set(module)
    elif action == 'global_slb_snat_on_vip_get':
        adc_global_slb_snat_on_vip_get(module)
    elif action == 'global_slb_snat_on_vip_set':
        adc_global_slb_snat_on_vip_set(module)
    elif action == 'global_slb_snat_interface_iprr_get':
        adc_global_slb_snat_interface_iprr_get(module)
    elif action == 'global_slb_snat_interface_iprr_set':
        adc_global_slb_snat_interface_iprr_set(module)
    elif action == 'slb_global_virtual_mac_get':
        adc_slb_global_virtual_mac_get(module)
    elif action == 'slb_global_virtual_mac_set':
        adc_slb_global_virtual_mac_set(module)


if __name__ == '__main__':
    main()
