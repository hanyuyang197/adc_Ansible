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


def system_ports_set(module):
    """设置系统应用端口配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    sshd_port = module.params['sshd_port']
    telnet_port = module.params['telnet_port']
    http_port = module.params['http_port']
    https_port = module.params['https_port']
    weak_algo = module.params['weak_algo']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.ports.set" % (
        ip, authkey)

    # 构造系统端口配置数据
    ports_data = {}

    # 添加可选参数
    if sshd_port is not None:
        ports_data["sshd_port"] = sshd_port
    if telnet_port is not None:
        ports_data["telnet_port"] = telnet_port
    if http_port is not None:
        ports_data["http_port"] = http_port
    if https_port is not None:
        ports_data["https_port"] = https_port
    if weak_algo is not None:
        ports_data["weak_algo"] = weak_algo

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(ports_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(ports_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="设置系统应用端口配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置系统应用端口配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_ports_get(module):
    """获取系统应用端口配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.ports.get" % (
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
        module.fail_json(msg="获取系统应用端口配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取系统应用端口配置失败", response=parsed_data)
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
            'system_ports_set', 'system_ports_get']),
        # 系统端口配置参数
        sshd_port=dict(type='int', required=False),
        telnet_port=dict(type='int', required=False),
        http_port=dict(type='int', required=False),
        https_port=dict(type='int', required=False),
        weak_algo=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'system_ports_set':
        system_ports_set(module)
    elif action == 'system_ports_get':
        system_ports_get(module)


if __name__ == '__main__':
    main()
