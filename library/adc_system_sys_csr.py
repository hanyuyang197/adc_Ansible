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
try:
    import urllib.request as urllib_request
except ImportError:
    import urllib2 as urllib_request


def adc_system_sys_csr_add(module):
    """生成CSR"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.sys.csr.add" % (
        ip, authkey)

    # 构造请求数据
    request_data = {
        "ip": ip,
        "authkey": authkey
    }

    # 定义可选参数列表（根据API具体需求调整）
    optional_params = [
        'name', 'common_name', 'type', 'division', 'organization', 'locality',
        'state', 'country', 'email', 'password', 'confirm_password', 'key_size',
        'md_type', 'padding_type', 'ecc_group', 'subjectaltname'
    ]

    # 添加可选参数
    for param in optional_params:
        if get_param_if_exists(module, param) is not None:
            request_data[param] = get_param_if_exists(module, param)

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="生成CSR失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "生成CSR", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_system_sys_csr_del(module):
    """删除CSR"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.sys.csr.del" % (
        ip, authkey)

    # 构造请求数据
    request_data = {
        "ip": ip,
        "authkey": authkey
    }

    # 添加必需参数
    if name:
        request_data['name'] = name

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="删除CSR失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除CSR", True)
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
        action=dict(type='str', required=True, choices=['system_sys_csr_add', 'system_sys_csr_del']),
        name=dict(type='str', required=False),
        common_name=dict(type='str', required=False),
        type=dict(type='int', required=False),
        division=dict(type='str', required=False),
        organization=dict(type='str', required=False),
        locality=dict(type='str', required=False),
        state=dict(type='str', required=False),
        country=dict(type='str', required=False),
        email=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        confirm_password=dict(type='str', required=False, no_log=True),
        key_size=dict(type='int', required=False),
        md_type=dict(type='int', required=False),
        padding_type=dict(type='str', required=False),
        ecc_group=dict(type='str', required=False),
        subjectaltname=dict(type='dict', required=False),
        description=dict(type='str', required=False),
        status=dict(type='str', required=False),
        config=dict(type='dict', required=False),
        setting=dict(type='dict', required=False),
        value=dict(type='str', required=False),
        enable=dict(type='bool', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    if module.params['action'] == 'system_sys_csr_add':
        adc_system_sys_csr_add(module)
    elif module.params['action'] == 'system_sys_csr_del':
        adc_system_sys_csr_del(module)


if __name__ == '__main__':
    main()
