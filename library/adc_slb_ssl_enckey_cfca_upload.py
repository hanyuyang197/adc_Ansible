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
import os


def adc_slb_ssl_enckey_cfca_upload(module):
    """上传CFCA私钥"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    sign_file_name = module.params['sign_file_name']
    sign_file_password = module.params.get('sign_file_password')
    file_path = module.params['file_path']

    # 验证文件是否存在
    if not os.path.exists(file_path):
        module.fail_json(msg="文件不存在: %s" % file_path)

    try:
        # 使用multipart/form-data上传文件
        import tempfile
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            import urllib.parse
            from urllib.request import Request
            import mimetypes
        else:
            import urllib2 as urllib_request
            import urllib
            from urllib2 import Request
            import mimetypes

        # 读取文件内容
        with open(file_path, 'rb') as f:
            file_content = f.read()

        # 创建multipart/form-data格式的请求体
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        body = []
        body.append('--' + boundary)
        body.append('Content-Disposition: form-data; name="file"; filename="%s"' %
                    os.path.basename(file_path))
        body.append('Content-Type: application/octet-stream')
        body.append('')
        if sys.version_info[0] >= 3:
            body.append(file_content.decode('latin-1')
                        if isinstance(file_content, bytes) else file_content)
        else:
            body.append(file_content)
        body.append('--' + boundary + '--')
        body.append('')

        # 将body转换为bytes
        if sys.version_info[0] >= 3:
            body_str = '\r\n'.join(body)
            body_bytes = body_str.encode('latin-1')
        else:
            body_str = '\r\n'.join(body)
            body_bytes = body_str

        # 构建URL参数
        url_params = "authkey=%s&action=slb.ssl.enckey.cfca.upload&sign_file_name=%s" % (
            authkey, sign_file_name)
        if sign_file_password:
            url_params += "&sign_file_password=%s" % sign_file_password

        # 构建完整的URL
        url = "http://%s/adcapi/v2.0/?%s" % (ip, url_params)

        # 创建请求
        req = Request(url, data=body_bytes)
        req.add_header(
            'Content-Type', 'multipart/form-data; boundary=%s' % boundary)

        # 发送请求
        response = urllib_request.urlopen(req)
        response_data = response.read()
        if sys.version_info[0] >= 3:
            response_data = response_data.decode('utf-8')

        # 格式化响应
        success, result_dict = format_adc_response_for_ansible(
            response_data, "上传CFCA私钥", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="上传CFCA私钥失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=['upload']),
        sign_file_name=dict(type='str', required=True),
        sign_file_password=dict(type='str', required=False, no_log=True),
        file_path=dict(type='str', required=True)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'upload':
        adc_slb_ssl_enckey_cfca_upload(module)


if __name__ == '__main__':
    main()
