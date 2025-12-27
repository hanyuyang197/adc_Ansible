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
                'content_type', 'application/octet-stream')
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


def adc_slb_ssl_certificate_upload(module):
    """上传SSL证书文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_path = module.params['file_path']
    cert_name = module.params['cert_name']

    # 检查文件是否存在
    if not os.path.exists(file_path):
        module.fail_json(msg="证书文件不存在: %s" % file_path)

    # 读取文件内容
    with open(file_path, 'rb') as f:
        file_content = f.read().decode('utf-8')

    # 构造表单数据
    fields = {
        'authkey': authkey
    }

    files = {
        'file': {
            'filename': os.path.basename(file_path) if not cert_name else cert_name,
            'content': file_content,
            'content_type': 'application/x-x509-ca-cert'
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
        module.fail_json(msg="上传SSL证书失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "上传SSL证书", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_slb_ssl_certificate_add(module):
    """生成SSL自签名证书"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ssl.certificate.add" % (
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
        module.fail_json(msg="生成SSL自签名证书失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "生成SSL自签名证书", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_slb_ssl_certificate_list(module):
    """获取SSL证书列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ssl.certificate.list" % (
        ip, authkey)

    try:
        # 发送GET请求
        if sys.version_info[0] >= 3:
            req = urllib_request.Request(url)
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            req = urllib_request.Request(url)
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取SSL证书列表失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取SSL证书列表", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_slb_ssl_certificate_list_withcommon(module):
    """获取SSL证书列表（包含common分区）"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ssl.certificate.list.withcommon" % (
        ip, authkey)

    try:
        # 发送GET请求
        if sys.version_info[0] >= 3:
            req = urllib_request.Request(url)
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            req = urllib_request.Request(url)
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取SSL证书列表（包含common分区）失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取SSL证书列表（包含common分区）", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_slb_ssl_certificate_del(module):
    """删除自签名证书"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ssl.certificate.del" % (
        ip, authkey)

    # 构造请求数据
    request_data = {
        "ip": ip,
        "authkey": authkey
    }

    # 定义可选参数列表（根据API具体需求调整）
    optional_params = [
        'name'
    ]

    # 添加可选参数
    for param in optional_params:
        if get_param_if_exists(module, param) is not None:
            request_data[param] = get_param_if_exists(module, param)

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    # 初始化响应数据
    response_data = ""

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
        module.fail_json(msg="删除自签名证书失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除自签名证书", True)
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
                    'upload', 'add', 'list', 'list_withcommon', 'del']),
        name=dict(type='str', required=False),
        cert_name=dict(type='str', required=False),
        file_path=dict(type='str', required=False),
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
    if module.params['action'] == 'upload':
        adc_slb_ssl_certificate_upload(module)
    elif module.params['action'] == 'add':
        adc_slb_ssl_certificate_add(module)
    elif module.params['action'] == 'list':
        adc_slb_ssl_certificate_list(module)
    elif module.params['action'] == 'list_withcommon':
        adc_slb_ssl_certificate_list_withcommon(module)
    elif module.params['action'] == 'del':
        adc_slb_ssl_certificate_del(module)


if __name__ == '__main__':
    main()
