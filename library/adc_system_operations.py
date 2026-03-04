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


def save(module):
    """保存配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=save" % (ip, authkey)

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
        module.fail_json(msg="保存配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "保存配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def admin_disable_get(module):
    """获取管理员状态"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.disable.get" % (ip, authkey)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='POST')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'POST'
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取管理员状态失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取管理员状态", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def admin_disable_edit(module):
    """禁用管理员用户"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    enable = module.params['enable']
    name = module.params['name']
    password = module.params.get('password')

    # 构造请求数据
    disable_data = {
        'enable': enable,
        'name': name
    }

    # password是可选参数
    if password is not None:
        disable_data['password'] = password

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.disable.edit" % (ip, authkey)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = json.dumps(disable_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            post_data = json.dumps(disable_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="禁用管理员用户失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "禁用管理员用户", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def admin_two_factor_authentication_get(module):
    """获取双因素认证状态"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.two_factor_authentication.get" % (ip, authkey)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='POST')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'POST'
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取双因素认证状态失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取双因素认证状态", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def admin_two_factor_authentication_set(module):
    """开启双因素认证"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tfaenable = module.params['tfaenable']
    admintfaenable = module.params['admintfaenable']

    # 构造请求数据
    tfa_data = {
        'tfaenable': tfaenable,
        'admintfaenable': admintfaenable
    }

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.two_factor_authentication.set" % (ip, authkey)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = json.dumps(tfa_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            post_data = json.dumps(tfa_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="开启双因素认证失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "开启双因素认证", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_action_reboot(module):
    """系统重启"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    save = module.params['save']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.action.reboot" % (
        ip, authkey)

    # 构造重启数据
    reboot_data = {}

    # 添加可选参数
    if save is not None:
        reboot_data["save"] = save

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(reboot_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(reboot_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="系统重启失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "系统重启", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_action_reload(module):
    """重新加载配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    save = module.params['save']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.action.reload" % (
        ip, authkey)

    # 构造重新加载数据
    reload_data = {}

    # 添加可选参数
    if save is not None:
        reload_data["save"] = save

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(reload_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(reload_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="重新加载配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "重新加载配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_action_shutdown(module):
    """系统关机"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    save = module.params['save']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.action.shutdown" % (
        ip, authkey)

    # 构造关机数据
    shutdown_data = {}

    # 添加可选参数
    if save is not None:
        shutdown_data["save"] = save

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(shutdown_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(shutdown_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="系统关机失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "系统关机", True)
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
            'save', 'system_action_reboot', 'system_action_reload', 'system_action_shutdown',
            'admin_disable_get', 'admin_disable_edit', 'admin_two_factor_authentication_get',
            'admin_two_factor_authentication_set']),
        # 系统操作参数
        save=dict(type='int', required=False),
        # admin.disable.edit 参数
        enable=dict(type='int', required=False),
        name=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        # admin.two_factor_authentication.set 参数
        tfaenable=dict(type='int', required=False),
        admintfaenable=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'save':
        save(module)
    elif action == 'system_action_reboot':
        system_action_reboot(module)
    elif action == 'system_action_reload':
        system_action_reload(module)
    elif action == 'system_action_shutdown':
        system_action_shutdown(module)
    elif action == 'admin_disable_get':
        admin_disable_get(module)
    elif action == 'admin_disable_edit':
        admin_disable_edit(module)
    elif action == 'admin_two_factor_authentication_get':
        admin_two_factor_authentication_get(module)
    elif action == 'admin_two_factor_authentication_set':
        admin_two_factor_authentication_set(module)


if __name__ == '__main__':
    main()
