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


def system_smtp_get(module):
    """获取SMTP配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.smtp.get" % (
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
        module.fail_json(msg="获取SMTP配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SMTP配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, smtp_config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def system_smtp_set(module):
    """编辑SMTP配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.smtp.set" % (
        ip, authkey)

    # 构造SMTP配置数据
    smtp_data = {}

    # 添加可选参数
    if 'server' in module.params and module.params['server'] is not None:
        smtp_data['server'] = module.params['server']
    if 'port' in module.params and module.params['port'] is not None:
        smtp_data['port'] = module.params['port']
    if 'emailto' in module.params and module.params['emailto'] is not None:
        smtp_data['emailto'] = module.params['emailto']
    if 'emailfrom' in module.params and module.params['emailfrom'] is not None:
        smtp_data['emailfrom'] = module.params['emailfrom']
    if 'auth' in module.params and module.params['auth'] is not None:
        smtp_data['auth'] = module.params['auth']
    if 'user' in module.params and module.params['user'] is not None:
        smtp_data['user'] = module.params['user']
    if 'password' in module.params and module.params['password'] is not None:
        smtp_data['password'] = module.params['password']

    # 转换为JSON格式
    post_data = json.dumps(smtp_data)

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
        module.fail_json(msg="编辑SMTP配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑SMTP配置", True)
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
            'system_smtp_get', 'system_smtp_set']),
        # SMTP配置参数
        server=dict(type='str', required=False),
        port=dict(type='int', required=False),
        emailto=dict(type='str', required=False),
        emailfrom=dict(type='str', required=False),
        auth=dict(type='int', required=False, choices=[0, 1]),
        user=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'system_smtp_get':
        system_smtp_get(module)
    elif action == 'system_smtp_set':
        system_smtp_set(module)


if __name__ == '__main__':
    main()
