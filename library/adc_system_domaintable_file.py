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


def adc_system_domaintable_file_upload(module):
    """上传域名表文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_path = module.params['file_path']
    name = module.params['name']

    # 检查文件是否存在
    if not os.path.exists(file_path):
        module.fail_json(msg="文件不存在: %s" % file_path)

    # 读取文件内容
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
    except Exception as e:
        module.fail_json(msg="读取文件失败: %s" % str(e))

    # 构造请求URL - 包含name参数
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.domaintable.file.upload&name=%s" % (
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
            body_parts.append('Content-Type: text/plain')
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
            body_parts.append('Content-Type: text/plain')
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

    except Exception as e:
        module.fail_json(msg="上传域名表文件失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "上传域名表文件", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_system_domaintable_file_download(module):
    """下载域名表文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    dest_path = module.params['dest_path']

    # 构造请求URL - 包含name参数
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.domaintable.file.download&name=%s" % (
        ip, authkey, name)

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request

            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read()

            # 将下载的数据保存到文件
            with open(dest_path, 'wb') as f:
                f.write(response_data)

        else:
            # Python 2
            import urllib2 as urllib_request

            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()

            # 将下载的数据保存到文件
            with open(dest_path, 'wb') as f:
                f.write(response_data)

    except Exception as e:
        module.fail_json(msg="下载域名表文件失败: %s" % str(e))

    # 返回成功结果，包含下载文件路径
    module.exit_json(
        changed=True,
        msg="域名表文件下载成功",
        file_downloaded=True,
        dest_path=dest_path
    )


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=['upload', 'download']),
        name=dict(type='str', required=True),  # 文件名
        file_path=dict(type='str', required=False),  # 上传时的本地文件路径
        dest_path=dict(type='str', required=False),  # 下载时的目标路径
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
        required_if=[
            ['action', 'upload', ['file_path']],
            ['action', 'download', ['dest_path']]
        ]
    )

    # 根据action执行相应操作
    action = module.params['action']
    if action == 'upload':
        if not module.params.get('file_path'):
            module.fail_json(msg="上传操作需要指定file_path参数")
        adc_system_domaintable_file_upload(module)
    elif action == 'download':
        if not module.params.get('dest_path'):
            module.fail_json(msg="下载操作需要指定dest_path参数")
        adc_system_domaintable_file_download(module)



if __name__ == '__main__':
    main()
