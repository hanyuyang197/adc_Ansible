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


def aaa_general_set(module):
    """设置AAA全局配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    local_disabled = module.params['local_disabled']
    auth_order = module.params['auth_order']
    auth_order_console = module.params['auth_order_console']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=aaa.general.set" % (
        ip, authkey)

    # 构造AAA全局配置数据
    aaa_data = {}

    # 添加可选参数
    if local_disabled is not None:
        aaa_data["local_disabled"] = local_disabled
    if auth_order is not None:
        aaa_data["auth_order"] = auth_order
    if auth_order_console is not None:
        aaa_data["auth_order_console"] = auth_order_console

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(aaa_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(aaa_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="设置AAA全局配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置AAA全局配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def aaa_general_get(module):
    """获取AAA全局配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=aaa.general.get" % (
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
        module.fail_json(msg="获取AAA全局配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取AAA全局配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def aaa_radius_set(module):
    """设置Radius认证配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    server_status = module.params['server_status']
    server_hostname = module.params['server_hostname']
    server_secret = module.params['server_secret']
    server_authentication = module.params['server_authentication']
    server_account = module.params['server_account']
    server_retransmit = module.params['server_retransmit']
    server_timeout = module.params['server_timeout']
    server_status2 = module.params['server_status2']
    server_hostname2 = module.params['server_hostname2']
    server_secret2 = module.params['server_secret2']
    server_authentication2 = module.params['server_authentication2']
    server_account2 = module.params['server_account2']
    server_retransmit2 = module.params['server_retransmit2']
    server_timeout2 = module.params['server_timeout2']
    def_priv_enabled = module.params['def_priv_enabled']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=aaa.radius.set" % (
        ip, authkey)

    # 构造Radius配置数据
    radius_data = {}

    # 添加可选参数
    if server_status is not None:
        radius_data["server_status"] = server_status
    if server_hostname is not None:
        radius_data["server_hostname"] = server_hostname
    if server_secret is not None:
        radius_data["server_secret"] = server_secret
    if server_authentication is not None:
        radius_data["server_authentication"] = server_authentication
    if server_account is not None:
        radius_data["server_account"] = server_account
    if server_retransmit is not None:
        radius_data["server_retransmit"] = server_retransmit
    if server_timeout is not None:
        radius_data["server_timeout"] = server_timeout
    if server_status2 is not None:
        radius_data["server_status2"] = server_status2
    if server_hostname2 is not None:
        radius_data["server_hostname2"] = server_hostname2
    if server_secret2 is not None:
        radius_data["server_secret2"] = server_secret2
    if server_authentication2 is not None:
        radius_data["server_authentication2"] = server_authentication2
    if server_account2 is not None:
        radius_data["server_account2"] = server_account2
    if server_retransmit2 is not None:
        radius_data["server_retransmit2"] = server_retransmit2
    if server_timeout2 is not None:
        radius_data["server_timeout2"] = server_timeout2
    if def_priv_enabled is not None:
        radius_data["def_priv_enabled"] = def_priv_enabled

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(radius_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(radius_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="设置Radius认证配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置Radius认证配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def aaa_radius_get(module):
    """获取Radius认证配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=aaa.radius.get" % (
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
        module.fail_json(msg="获取Radius认证配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取Radius认证配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def aaa_tacacs_set(module):
    """设置TACACS+认证配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    server_status = module.params['server_status']
    server_hostname = module.params['server_hostname']
    server_secret = module.params['server_secret']
    server_authentication = module.params['server_authentication']
    server_timeout = module.params['server_timeout']
    server_status2 = module.params['server_status2']
    server_hostname2 = module.params['server_hostname2']
    server_secret2 = module.params['server_secret2']
    server_authentication2 = module.params['server_authentication2']
    server_timeout2 = module.params['server_timeout2']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=aaa.tacacs.set" % (
        ip, authkey)

    # 构造TACACS+配置数据
    tacacs_data = {}

    # 添加可选参数
    if server_status is not None:
        tacacs_data["server_status"] = server_status
    if server_hostname is not None:
        tacacs_data["server_hostname"] = server_hostname
    if server_secret is not None:
        tacacs_data["server_secret"] = server_secret
    if server_authentication is not None:
        tacacs_data["server_authentication"] = server_authentication
    if server_timeout is not None:
        tacacs_data["server_timeout"] = server_timeout
    if server_status2 is not None:
        tacacs_data["server_status2"] = server_status2
    if server_hostname2 is not None:
        tacacs_data["server_hostname2"] = server_hostname2
    if server_secret2 is not None:
        tacacs_data["server_secret2"] = server_secret2
    if server_authentication2 is not None:
        tacacs_data["server_authentication2"] = server_authentication2
    if server_timeout2 is not None:
        tacacs_data["server_timeout2"] = server_timeout2

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(tacacs_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(tacacs_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="设置TACACS+认证配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置TACACS+认证配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def aaa_tacacs_get(module):
    """获取TACACS+认证配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=aaa.tacacs.get" % (
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
        module.fail_json(msg="获取TACACS+认证配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TACACS+认证配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def aaa_ldap_set(module):
    """设置LDAP认证配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    serverstatus = module.params['serverstatus']
    hostname = module.params['hostname']
    ldap_cn = module.params['ldap_cn']
    ldap_dn = module.params['ldap_dn']
    ldap_timeout = module.params['ldap_timeout']
    ldap_port = module.params['ldap_port']
    ldap_ssl = module.params['ldap_ssl']
    serverstatus2 = module.params['serverstatus2']
    hostname2 = module.params['hostname2']
    ldap_cn2 = module.params['ldap_cn2']
    ldap_dn2 = module.params['ldap_dn2']
    ldap_timeout2 = module.params['ldap_timeout2']
    ldap_port2 = module.params['ldap_port2']
    ldap_ssl2 = module.params['ldap_ssl2']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=aaa.ldap.set" % (
        ip, authkey)

    # 构造LDAP配置数据
    ldap_data = {}

    # 添加可选参数
    if serverstatus is not None:
        ldap_data["serverstatus"] = serverstatus
    if hostname is not None:
        ldap_data["hostname"] = hostname
    if ldap_cn is not None:
        ldap_data["ldap_cn"] = ldap_cn
    if ldap_dn is not None:
        ldap_data["ldap_dn"] = ldap_dn
    if ldap_timeout is not None:
        ldap_data["ldap_timeout"] = ldap_timeout
    if ldap_port is not None:
        ldap_data["ldap_port"] = ldap_port
    if ldap_ssl is not None:
        ldap_data["ldap_ssl"] = ldap_ssl
    if serverstatus2 is not None:
        ldap_data["serverstatus2"] = serverstatus2
    if hostname2 is not None:
        ldap_data["hostname2"] = hostname2
    if ldap_cn2 is not None:
        ldap_data["ldap_cn2"] = ldap_cn2
    if ldap_dn2 is not None:
        ldap_data["ldap_dn2"] = ldap_dn2
    if ldap_timeout2 is not None:
        ldap_data["ldap_timeout2"] = ldap_timeout2
    if ldap_port2 is not None:
        ldap_data["ldap_port2"] = ldap_port2
    if ldap_ssl2 is not None:
        ldap_data["ldap_ssl2"] = ldap_ssl2

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(ldap_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(ldap_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="设置LDAP认证配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置LDAP认证配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def aaa_ldap_get(module):
    """获取LDAP认证配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=aaa.ldap.get" % (
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
        module.fail_json(msg="获取LDAP认证配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取LDAP认证配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
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
            'aaa_general_set', 'aaa_general_get',
            'aaa_radius_set', 'aaa_radius_get',
            'aaa_tacacs_set', 'aaa_tacacs_get',
            'aaa_ldap_set', 'aaa_ldap_get']),
        # AAA全局配置参数
        local_disabled=dict(type='int', required=False),
        auth_order=dict(type='int', required=False),
        auth_order_console=dict(type='int', required=False),
        # Radius配置参数
        server_status=dict(type='int', required=False),
        server_hostname=dict(type='str', required=False),
        server_secret=dict(type='str', required=False, no_log=True),
        server_authentication=dict(type='int', required=False),
        server_account=dict(type='int', required=False),
        server_retransmit=dict(type='int', required=False),
        server_timeout=dict(type='int', required=False),
        server_status2=dict(type='int', required=False),
        server_hostname2=dict(type='str', required=False),
        server_secret2=dict(type='str', required=False, no_log=True),
        server_authentication2=dict(type='int', required=False),
        server_account2=dict(type='int', required=False),
        server_retransmit2=dict(type='int', required=False),
        server_timeout2=dict(type='int', required=False),
        def_priv_enabled=dict(type='int', required=False),
        # TACACS+配置参数
        # server_status, server_hostname, server_secret, server_authentication, server_timeout 已定义
        # server_status2, server_hostname2, server_secret2, server_authentication2, server_timeout2 已定义
        # LDAP配置参数
        serverstatus=dict(type='int', required=False),
        hostname=dict(type='str', required=False),
        ldap_cn=dict(type='str', required=False),
        ldap_dn=dict(type='str', required=False),
        ldap_timeout=dict(type='int', required=False),
        ldap_port=dict(type='int', required=False),
        ldap_ssl=dict(type='int', required=False),
        serverstatus2=dict(type='int', required=False),
        hostname2=dict(type='str', required=False),
        ldap_cn2=dict(type='str', required=False),
        ldap_dn2=dict(type='str', required=False),
        ldap_timeout2=dict(type='int', required=False),
        ldap_port2=dict(type='int', required=False),
        ldap_ssl2=dict(type='int', required=False),
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'aaa_general_set':
        aaa_general_set(module)
    elif action == 'aaa_general_get':
        aaa_general_get(module)
    elif action == 'aaa_radius_set':
        aaa_radius_set(module)
    elif action == 'aaa_radius_get':
        aaa_radius_get(module)
    elif action == 'aaa_tacacs_set':
        aaa_tacacs_set(module)
    elif action == 'aaa_tacacs_get':
        aaa_tacacs_get(module)
    elif action == 'aaa_ldap_set':
        aaa_ldap_set(module)
    elif action == 'aaa_ldap_get':
        aaa_ldap_get(module)


if __name__ == '__main__':
    main()
