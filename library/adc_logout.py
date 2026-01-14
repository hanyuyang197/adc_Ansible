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
# Python 2/3兼容性处理
try:
    # Python 2
    import urllib2 as urllib_request
except ImportError:
    # Python 3
    import urllib.request as urllib_request
    import urllib.error as urllib_error
import sys


def logout(module):
    """执行ADC设备登出操作"""
    # 获取参数
    ip = module.params['ip']
    authkey = module.params['authkey']
    use_https = module.params['use_https']
    validate_certs = module.params['validate_certs']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    protocol = "https" if use_https else "http"
    url = "%s://%s/adcapi/v2.0/?authkey=%s&action=logout" % (
        protocol, ip, authkey)

    # 初始化响应数据
    response_data = ""

    # 根据Python版本处理请求
    if sys.version_info[0] >= 3:
        # Python 3
        import ssl

        # 处理SSL证书验证
        if use_https and not validate_certs:
            # 跳过SSL证书验证
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            req = urllib_request.Request(url, method='GET')
            try:
                response = urllib_request.urlopen(req, context=context)
                response_data = response.read().decode('utf-8')
            except Exception as e:
                module.fail_json(msg="登出请求失败: %s" % str(e))
        else:
            req = urllib_request.Request(url, method='GET')
            try:
                response = urllib_request.urlopen(req)
                response_data = response.read().decode('utf-8')
            except Exception as e:
                module.fail_json(msg="登出请求失败: %s" % str(e))
    else:
        # Python 2

        # 处理SSL证书验证 (Python 2)
        if use_https and not validate_certs:
            # 跳过SSL证书验证
            # 注意：Python 2的SSL处理较为简单
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            try:
                response = urllib_request.urlopen(req)
                response_data = response.read()
            except Exception as e:
                module.fail_json(msg="登出请求失败: %s" % str(e))
        else:
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            try:
                response = urllib_request.urlopen(req)
                response_data = response.read()
            except Exception as e:
                module.fail_json(msg="登出请求失败: %s" % str(e))

    # 解析响应
    if response_data:
        try:
            result = json.loads(response_data)
            # 登出成功
            module.exit_json(changed=True, msg="登出成功", response=result)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        use_https=dict(type='bool', required=False, default=False),
        validate_certs=dict(type='bool', required=False, default=True)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 执行登出操作
    logout(module)


if __name__ == '__main__':
    main()
