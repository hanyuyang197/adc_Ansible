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


def adc_slb_ruletable_file_upload(module):
    """上传规则表文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    file_path = module.params.get('file_path')

    # 检查必要参数
    if not name:
        module.fail_json(msg="上传规则表文件需要提供name参数")
    if not file_path or not os.path.exists(file_path):
        module.fail_json(msg="上传规则表文件需要提供有效的file_path参数")

    # 读取文件内容
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
    except Exception as e:
        module.fail_json(msg="读取文件失败: %s" % str(e))

    # 构造请求URL - 包含name参数
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.file.upload&name=%s" % (
        ip, authkey, name)

    try:
        # 根据Python版本处理文件上传
        if sys.version_info[0] >= 3:
            # Python 3 - 使用urllib处理multipart/form-data上传
            import urllib.request as urllib_request

            # 构建multipart/form-data请求
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'

            # 准备表单数据
            body_parts = []
            body_parts.append('--%s' % boundary)
            body_parts.append(
                'Content-Disposition: form-data; name="file"; filename="%s"' % os.path.basename(file_path))
            body_parts.append(
                'Content-Type: application/octet-stream')  # 二进制文件类型
            body_parts.append('')
            # 将body_parts转换为bytes并加上文件内容
            body_content = b''
            for part in body_parts:
                body_content += part.encode('utf-8') + b'\r\n'
            body_content += file_content
            body_content += b'\r\n--%s--\r\n' % boundary.encode('utf-8')

            req = urllib_request.Request(url, data=body_content, headers={
                'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
                'Content-Length': str(len(body_content))
            })

            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2 - 使用urllib2处理multipart/form-data上传
            import urllib2 as urllib_request

            # 构建multipart/form-data请求
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'

            # 准备表单数据
            body_parts = []
            body_parts.append('--%s' % boundary)
            body_parts.append(
                'Content-Disposition: form-data; name="file"; filename="%s"' % os.path.basename(file_path))
            body_parts.append(
                'Content-Type: application/octet-stream')  # 二进制文件类型
            body_parts.append('')
            # 将body_parts转换为字符串并加上文件内容
            body_content = ''
            for part in body_parts:
                body_content += part + '\r\n'
            body_content += file_content
            body_content += '\r\n--%s--\r\n' % boundary

            req = urllib_request.Request(url, data=body_content, headers={
                'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
                'Content-Length': str(len(body_content))
            })

            response = urllib_request.urlopen(req)
            response_data = response.read()

        # 使用通用响应解析函数
        if response_data:
            success, result_dict = format_adc_response_for_ansible(
                response_data, "上传规则表文件", True)
            if success:
                module.exit_json(**result_dict)
            else:
                module.fail_json(**result_dict)
        else:
            module.fail_json(msg="未收到有效响应")
    except Exception as e:
        module.fail_json(msg="上传规则表文件失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'slb_ruletable_file_upload'
        ]),
        # 规则表文件参数
        name=dict(type='str', required=False),
        file_path=dict(type='str', required=False)  # 上传时的本地文件路径
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
        required_if=[
            ['action', 'slb_ruletable_file_upload', ['file_path']]
        ]
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'slb_ruletable_file_upload':
        adc_slb_ruletable_file_upload(module)


if __name__ == '__main__':
    main()
