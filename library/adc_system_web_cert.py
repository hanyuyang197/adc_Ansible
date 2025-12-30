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


def adc_list_web_certs(module):
    """获取web证书列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.web.cert.list" % (
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
        module.fail_json(msg="获取web证书列表失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取web证书列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, certs=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_web_cert(module):
    """删除web证书"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除web证书需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.web.cert.del" % (
        ip, authkey)

    # 构造证书数据
    cert_data = {
        "name": name
    }

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(cert_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(cert_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="删除web证书失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除web证书", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_apply_web_cert(module):
    """应用web证书"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.web.cert.apply" % (
        ip, authkey)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='POST')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'POST'
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="应用web证书失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "应用web证书", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_upload_web_key(module):
    """上传web私钥文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_path = module.params.get('file_path')

    # 检查必需参数
    if not file_path or not os.path.exists(file_path):
        module.fail_json(msg="上传web私钥文件需要提供有效的file_path参数")

    # 读取文件内容
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
    except Exception as e:
        module.fail_json(msg="读取文件失败: %s" % str(e))

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.web.key.upload" % (
        ip, authkey)

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
            body_parts.append('Content-Type: application/x-pem-key')  # 私钥文件类型
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
            body_parts.append('Content-Type: application/x-pem-key')  # 私钥文件类型
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
                response_data, "上传web私钥文件", True)
            if success:
                module.exit_json(**result_dict)
            else:
                module.fail_json(**result_dict)
        else:
            module.fail_json(msg="未收到有效响应")
    except Exception as e:
        module.fail_json(msg="上传web私钥文件失败: %s" % str(e))


def adc_download_web_key(module):
    """下载web私钥文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="下载web私钥文件需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.web.key.download" % (
        ip, authkey)

    # 构造证书数据
    cert_data = {
        "name": name
    }

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(cert_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(cert_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="下载web私钥文件失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "下载web私钥文件", False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_upload_web_cert(module):
    """上传web证书文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_path = module.params.get('file_path')

    # 检查必需参数
    if not file_path or not os.path.exists(file_path):
        module.fail_json(msg="上传web证书文件需要提供有效的file_path参数")

    # 读取文件内容
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
    except Exception as e:
        module.fail_json(msg="读取文件失败: %s" % str(e))

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.web.cert.upload" % (
        ip, authkey)

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
                'Content-Type: application/x-x509-ca-cert')  # 证书文件类型
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
                'Content-Type: application/x-x509-ca-cert')  # 证书文件类型
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
                response_data, "上传web证书文件", True)
            if success:
                module.exit_json(**result_dict)
            else:
                module.fail_json(**result_dict)
        else:
            module.fail_json(msg="未收到有效响应")
    except Exception as e:
        module.fail_json(msg="上传web证书文件失败: %s" % str(e))


def adc_download_web_cert(module):
    """下载web证书文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="下载web证书文件需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.web.cert.download" % (
        ip, authkey)

    # 构造证书数据
    cert_data = {
        "name": name
    }

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(cert_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(cert_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="下载web证书文件失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "下载web证书文件", False)
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
            'list_web_certs', 'delete_web_cert', 'apply_web_cert',
            'upload_web_key', 'download_web_key',
            'upload_web_cert', 'download_web_cert']),
        # 证书参数
        name=dict(type='str', required=False),
        file_path=dict(type='str', required=False)  # 上传时的本地文件路径
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
        required_if=[
            ['action', 'upload_web_key', ['file_path']],
            ['action', 'upload_web_cert', ['file_path']]
        ]
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list_web_certs':
        adc_list_web_certs(module)
    elif action == 'delete_web_cert':
        adc_delete_web_cert(module)
    elif action == 'apply_web_cert':
        adc_apply_web_cert(module)
    elif action == 'upload_web_key':
        adc_upload_web_key(module)
    elif action == 'download_web_key':
        adc_download_web_key(module)
    elif action == 'upload_web_cert':
        adc_upload_web_cert(module)
    elif action == 'download_web_cert':
        adc_download_web_cert(module)


if __name__ == '__main__':
    main()
