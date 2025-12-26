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


def adc_add_user(module):
    """添加用户"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    password = module.params['password']

    # 检查必需参数
    if not name or not password:
        module.fail_json(msg="添加用户需要提供name和password参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.user.add" % (
        ip, authkey)

    # 构造用户数据
    user_data = {
        "name": name,
        "password": password
    }

    # 添加可选参数
    if 'privilege' in module.params and module.params['privilege'] is not None:
        user_data['privilege'] = module.params['privilege']
    if 'trust_host' in module.params and module.params['trust_host'] is not None:
        user_data['trust_host'] = module.params['trust_host']
    if 'trust_acl' in module.params and module.params['trust_acl'] is not None:
        user_data['trust_acl'] = module.params['trust_acl']
    if 'trust_ipv6_acl' in module.params and module.params['trust_ipv6_acl'] is not None:
        user_data['trust_ipv6_acl'] = module.params['trust_ipv6_acl']
    if 'trust_mask' in module.params and module.params['trust_mask'] is not None:
        user_data['trust_mask'] = module.params['trust_mask']
    if 'role' in module.params and module.params['role'] is not None:
        user_data['role'] = module.params['role']
    if 'partition' in module.params and module.params['partition'] is not None:
        user_data['partition'] = module.params['partition']

    # 转换为JSON格式
    post_data = json.dumps(user_data)

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
        module.fail_json(msg="添加用户失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加用户", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_users(module):
    """获取用户列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.user.list" % (
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
        module.fail_json(msg="获取用户列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取用户列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, users=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_user(module):
    """获取指定用户"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取指定用户需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.user.get" % (
        ip, authkey)

    # 构造用户数据
    user_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(user_data)

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
        module.fail_json(msg="获取指定用户失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取指定用户失败", response=parsed_data)
            else:
                module.exit_json(changed=False, user=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_user(module):
    """编辑指定用户"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑指定用户需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.user.edit" % (
        ip, authkey)

    # 构造用户数据
    user_data = {
        "name": name
    }

    # 添加可选参数
    if 'password' in module.params and module.params['password'] is not None:
        user_data['password'] = module.params['password']
    if 'privilege' in module.params and module.params['privilege'] is not None:
        user_data['privilege'] = module.params['privilege']
    if 'trust_host' in module.params and module.params['trust_host'] is not None:
        user_data['trust_host'] = module.params['trust_host']
    if 'trust_acl' in module.params and module.params['trust_acl'] is not None:
        user_data['trust_acl'] = module.params['trust_acl']
    if 'trust_ipv6_acl' in module.params and module.params['trust_ipv6_acl'] is not None:
        user_data['trust_ipv6_acl'] = module.params['trust_ipv6_acl']
    if 'trust_mask' in module.params and module.params['trust_mask'] is not None:
        user_data['trust_mask'] = module.params['trust_mask']
    if 'role' in module.params and module.params['role'] is not None:
        user_data['role'] = module.params['role']
    if 'partition' in module.params and module.params['partition'] is not None:
        user_data['partition'] = module.params['partition']

    # 转换为JSON格式
    post_data = json.dumps(user_data)

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
        module.fail_json(msg="编辑指定用户失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑指定用户", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_user(module):
    """删除指定用户"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除指定用户需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.user.del" % (
        ip, authkey)

    # 构造用户数据
    user_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(user_data)

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
        module.fail_json(msg="删除指定用户失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除指定用户", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_set_user_config(module):
    """设置用户锁定和密码配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    pwdtimeout = module.params['pwdtimeout']
    pwdlength = module.params['pwdlength']
    pwdcplex = module.params['pwdcplex']
    pwdcpfl = module.params['pwdcpfl']
    duration = module.params['duration']
    resettime = module.params['resettime']
    threshold = module.params['threshold']
    enable = module.params['enable']

    # 检查必需参数
    if (pwdtimeout is None or pwdlength is None or pwdcplex is None or
        pwdcpfl is None or duration is None or resettime is None or
            threshold is None or enable is None):
        module.fail_json(msg="设置用户锁定和密码配置需要提供所有配置参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.cfg.set" % (
        ip, authkey)

    # 构造配置数据
    config_data = {
        "pwdtimeout": pwdtimeout,
        "pwdlength": pwdlength,
        "pwdcplex": pwdcplex,
        "pwdcpfl": pwdcpfl,
        "duration": duration,
        "resettime": resettime,
        "threshold": threshold,
        "enable": enable
    }

    # 转换为JSON格式
    post_data = json.dumps(config_data)

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
        module.fail_json(msg="设置用户锁定和密码配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置用户锁定和密码配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_user_config(module):
    """获取用户锁定配置和密码配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.cfg.get" % (
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
        module.fail_json(msg="获取用户锁定配置和密码配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取用户锁定配置和密码配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_unlock_user(module):
    """解锁锁定用户"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="解锁锁定用户需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=admin.user.unlock" % (
        ip, authkey)

    # 构造用户数据
    user_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(user_data)

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
        module.fail_json(msg="解锁锁定用户失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "解锁锁定用户", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_change_password(module):
    """修改当前用户密码"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    old_password = module.params['old_password']
    password = module.params['password']

    # 检查必需参数
    if not old_password or not password:
        module.fail_json(msg="修改当前用户密码需要提供old_password和password参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.password.set" % (
        ip, authkey)

    # 构造密码数据
    password_data = {
        "old_password": old_password,
        "password": password
    }

    # 转换为JSON格式
    post_data = json.dumps(password_data)

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
        module.fail_json(msg="修改当前用户密码失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "修改当前用户密码", True)
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
            'add_user', 'list_users', 'get_user', 'edit_user', 'delete_user',
            'set_user_config', 'get_user_config', 'unlock_user', 'change_password']),
        # 用户参数
        name=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        old_password=dict(type='str', required=False, no_log=True),
        privilege=dict(type='int', required=False),
        trust_host=dict(type='str', required=False),
        trust_acl=dict(type='int', required=False),
        trust_ipv6_acl=dict(type='str', required=False),
        trust_mask=dict(type='str', required=False),
        role=dict(type='str', required=False),
        partition=dict(type='str', required=False),
        # 用户配置参数
        pwdtimeout=dict(type='int', required=False),
        pwdlength=dict(type='int', required=False),
        pwdcplex=dict(type='int', required=False),
        pwdcpfl=dict(type='int', required=False),
        duration=dict(type='int', required=False),
        resettime=dict(type='int', required=False),
        threshold=dict(type='int', required=False),
        enable=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'add_user':
        adc_add_user(module)
    elif action == 'list_users':
        adc_list_users(module)
    elif action == 'get_user':
        adc_get_user(module)
    elif action == 'edit_user':
        adc_edit_user(module)
    elif action == 'delete_user':
        adc_delete_user(module)
    elif action == 'set_user_config':
        adc_set_user_config(module)
    elif action == 'get_user_config':
        adc_get_user_config(module)
    elif action == 'unlock_user':
        adc_unlock_user(module)
    elif action == 'change_password':
        adc_change_password(module)


if __name__ == '__main__':
    main()
