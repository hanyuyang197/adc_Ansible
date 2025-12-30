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


def adc_slb_ssl_certkey_match(module):
    """校验证书和私钥配对"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    cert_name = module.params['cert_name']
    key_name = module.params['key_name']
    password = module.params.get('password')

    # 构建URL参数
    url_params = "authkey=%s&action=slb.ssl.certkey.match&cert_name=%s&key_name=%s" % (
        authkey, cert_name, key_name)
    if password:
        url_params += "&password=%s" % password

    url = "http://%s/adcapi/v2.0/?%s" % (ip, url_params)

    try:
        # 发送GET请求
        response_data = ""
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()

        # 格式化响应
        success, result_dict = format_adc_response_for_ansible(
            response_data, "校验证书和私钥配对", False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="校验证书和私钥配对失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=['match']),
        cert_name=dict(type='str', required=True),
        key_name=dict(type='str', required=True),
        password=dict(type='str', required=False, no_log=True)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'match':
        adc_slb_ssl_certkey_match(module)


if __name__ == '__main__':
    main()
