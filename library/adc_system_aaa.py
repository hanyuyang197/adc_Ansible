#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import json
# Python 2/3兼容性处理
try:
    # Python 2
    import urllib2 as urllib_request
except ImportError:
    # Python 3
    import urllib.request as urllib_request
    import urllib.error as urllib_error
import sys


def format_adc_response_for_ansible(response_data, action="", is_modify_action=False):
    """
    格式化ADC API响应数据为Ansible模块所需的格式

    Args:
        response_data (str): ADC API返回的响应数据
        action (str): 执行的操作名称
        is_modify_action (bool): 是否为修改类操作

    Returns:
        tuple: (success_bool, result_dict)
    """
    try:
        # 解析JSON响应
        result = json.loads(response_data)

        # 检查是否包含错误信息
        if 'errcode' in result and result['errcode'] != 0:
            # 操作失败
            result_dict = {
                'changed': False,
                'msg': '%s操作失败' % action if action else '操作失败',
                'error': {
                    'result': result.get('result', ''),
                    'errcode': result.get('errcode', ''),
                    'errmsg': result.get('errmsg', '')
                },
                'response': result.get('data', {})
            }
            return False, result_dict
        elif 'errcode' in result and result['errcode'] == 0:
            # 操作成功
            result_dict = {
                'changed': is_modify_action,  # 修改类操作标记为changed
                'msg': '%s操作成功' % action if action else '操作成功',
                'response': result.get('data', {})
            }

            # 如果是幂等性成功（已存在），调整消息
            if 'result' in result and 'already exists' in result['result']:
                result_dict['changed'] = False
                result_dict['msg'] = '%s操作成功（资源已存在，无需更改）' % action if action else '操作成功（资源已存在，无需更改）'

            return True, result_dict
        else:
            # 未知格式的响应
            result_dict = {
                'changed': is_modify_action,
                'msg': '%s操作完成' % action if action else '操作完成',
                'response': result
            }
            return True, result_dict

    except Exception as e:
        # 解析失败
        result_dict = {
            'changed': False,
            'msg': '解析响应失败: %s' % str(e),
            'raw_response': response_data if isinstance(response_data, str) else str(response_data)
        }
        return False, result_dict


def adc_set_aaa_general_config(module):
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
                        post_data = json.dumps(aaa_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
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


def adc_get_aaa_general_config(module):
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
                        req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
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


def adc_set_radius_config(module):
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
                        post_data = json.dumps(radius_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
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


def adc_get_radius_config(module):
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
                        req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
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


def adc_set_tacacs_config(module):
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
                        post_data = json.dumps(tacacs_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
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


def adc_get_tacacs_config(module):
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
                        req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
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


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'set_aaa_general_config', 'get_aaa_general_config',
            'set_radius_config', 'get_radius_config',
            'set_tacacs_config', 'get_tacacs_config']),
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
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'set_aaa_general_config':
        adc_set_aaa_general_config(module)
    elif action == 'get_aaa_general_config':
        adc_get_aaa_general_config(module)
    elif action == 'set_radius_config':
        adc_set_radius_config(module)
    elif action == 'get_radius_config':
        adc_get_radius_config(module)
    elif action == 'set_tacacs_config':
        adc_set_tacacs_config(module)
    elif action == 'get_tacacs_config':
        adc_get_tacacs_config(module)


if __name__ == '__main__':
    main()
