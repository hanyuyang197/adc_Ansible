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


def login(module):
    """执行ADC设备登录操作"""
    # 获取参数
    ip = module.params['ip']
    username = module.params['username']
    password = module.params['password']
    use_https = module.params['use_https']
    validate_certs = module.params['validate_certs']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    protocol = "https" if use_https else "http"
    url = "%s://%s/adcapi/v2.0/?action=login" % (protocol, ip)

    # 构造请求数据
    data = {}
    # 只添加明确指定的参数
    if "username" in module.params and module.params["username"] is not None:
        data["username"] = module.params["username"]
    if "password" in module.params and module.params["password"] is not None:
        data["password"] = module.params["password"]
    elif password is not None:
        data["password"] = password

    # 转换为JSON格式
    post_data = json.dumps(data)

    # 初始化响应数据
    response_data = ""

    # 根据Python版本处理编码和SSL
    if sys.version_info[0] >= 3:
        # Python 3
        import urllib.request as urllib_request
        import ssl
        post_data = post_data.encode('utf-8')

        # 处理SSL证书验证
        if use_https and not validate_certs:
            # 跳过SSL证书验证
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            try:
                response = urllib_request.urlopen(req, context=context)
                response_data = response.read().decode('utf-8')
            except Exception as e:
                module.fail_json(msg="登录请求失败: %s" % str(e))
        else:
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            try:
                response = urllib_request.urlopen(req)
                response_data = response.read().decode('utf-8')
            except Exception as e:
                module.fail_json(msg="登录请求失败: %s" % str(e))
    else:
        # Python 2
        import urllib2 as urllib_request
        req = urllib_request.Request(url, data=post_data, headers={
                                     'Content-Type': 'application/json'})

        # 处理SSL证书验证 (Python 2)
        if use_https and not validate_certs:
            import ssl
            # 跳过SSL证书验证
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            try:
                response = urllib_request.urlopen(req, context=ctx)
                response_data = response.read()
            except Exception as e:
                module.fail_json(msg="登录请求失败: %s" % str(e))
        else:
            try:
                response = urllib_request.urlopen(req)
                response_data = response.read()
            except Exception as e:
                module.fail_json(msg="登录请求失败: %s" % str(e))

    # 确保有响应数据再解析
    if response_data:
        try:
            result = json.loads(response_data)

            # 检查是否有authkey返回
            if 'authkey' in result:
                module.exit_json(changed=True, authkey=result['authkey'])
            else:
                module.fail_json(msg="登录失败，未返回authkey", response=result)

        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        use_https=dict(type='bool', required=False, default=False),
        validate_certs=dict(type='bool', required=False, default=True)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 执行登录操作
    login(module)


if __name__ == '__main__':
    main()
