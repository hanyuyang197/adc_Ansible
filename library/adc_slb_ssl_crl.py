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
try:
    import urllib.parse as urllib_parse
    import urllib.request as urllib_request
except ImportError:
    import urllib2 as urllib_request
    import urlparse as urllib_parse
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import mimetypes


def create_form_data(fields, files=None):
    """创建multipart/form-data格式的数据"""
    BOUNDARY = '----adcformdataformdata'
    CRLF = '\r\n'
    form_data = []

    # 添加普通字段
    for field_name, field_value in fields.items():
        form_data.append('--' + BOUNDARY)
        form_data.append(
            'Content-Disposition: form-data; name="%s"' % field_name)
        form_data.append('')
        form_data.append(str(field_value))

    # 添加文件字段
    if files:
        for file_name, file_info in files.items():
            filename = file_info['filename']
            content = file_info['content']
            content_type = file_info.get(
                'content_type', 'application/pkix-crl')
            form_data.append('--' + BOUNDARY)
            form_data.append(
                'Content-Disposition: form-data; name="%s"; filename="%s"' % (file_name, filename))
            form_data.append('Content-Type: %s' % content_type)
            form_data.append('')
            form_data.append(content)

    form_data.append('--' + BOUNDARY + '--')
    form_data.append('')
    body = CRLF.join(form_data)
    return body, BOUNDARY


def adc_slb_ssl_crl_upload(module):
    """上传SSL证书吊销列表文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_path = module.params['file_path']
    crl_name = module.params['crl_name']

    # 检查文件是否存在
    if not os.path.exists(file_path):
        module.fail_json(msg="CRL文件不存在: %s" % file_path)

    # 读取文件内容
    with open(file_path, 'rb') as f:
        file_content = f.read().decode('utf-8')

    # 构造表单数据
    fields = {
        'authkey': authkey
    }

    files = {
        'file': {
            'filename': os.path.basename(file_path) if not crl_name else crl_name,
            'content': file_content,
            'content_type': 'application/pkix-crl'
        }
    }

    body, boundary = create_form_data(fields, files)

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/" % ip

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            req = urllib_request.Request(url, data=body.encode('utf-8'))
            req.add_header(
                'Content-Type', 'multipart/form-data; boundary=%s' % boundary)
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            req = urllib_request.Request(url, data=body)
            req.add_header(
                'Content-Type', 'multipart/form-data; boundary=%s' % boundary)
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="上传SSL证书吊销列表失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "上传SSL证书吊销列表", True)
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
        action=dict(type='str', required=True, choices=['upload', 'del']),
        name=dict(type='str', required=False),  # 用于删除操作
        crl_name=dict(type='str', required=False),
        file_path=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    if module.params['action'] == 'upload':
        adc_slb_ssl_crl_upload(module)
    elif module.params['action'] == 'del':
        # 使用通用函数处理删除操作
        ip = module.params['ip']
        authkey = module.params['authkey']
        name = module.params['name']

        # 构造请求URL
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ssl.crl.del" % (
            ip, authkey)

        # 构造请求数据
        request_data = {
            "ip": ip,
            "authkey": authkey
        }

        # 添加可选参数
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
                import urllib2 as urllib_request
                req = urllib_request.Request(url, data=post_data, headers={
                                             'Content-Type': 'application/json'})
                response = urllib_request.urlopen(req)
                response_data = response.read()

        except Exception as e:
            module.fail_json(msg="删除SSL证书吊销列表失败: %s" % str(e))

        # 使用通用响应解析函数
        if response_data:
            success, result_dict = format_adc_response_for_ansible(
                response_data, "删除SSL证书吊销列表", True)
            if success:
                module.exit_json(**result_dict)
            else:
                module.fail_json(**result_dict)
        else:
            module.fail_json(msg="未收到有效响应")


if __name__ == '__main__':
    main()
