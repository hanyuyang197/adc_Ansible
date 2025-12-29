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

# ADC API响应解析函数


def adc_list_domain_tables(module):
    """获取域名解析自定义列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.domaintable.list" % (
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
        module.fail_json(msg="获取域名解析自定义列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取域名解析自定义列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, domain_tables=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_domain_table(module):
    """添加域名解析自定义"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加域名解析自定义需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.domaintable.add" % (
        ip, authkey)

    # 构造域名表数据
    domain_data = {
        "name": name
    }

    # 添加可选参数
    if 'ttl' in module.params and module.params['ttl'] is not None:
        domain_data['ttl'] = module.params['ttl']
    if 'primary_dns_server' in module.params and module.params['primary_dns_server'] is not None:
        domain_data['primary_dns_server'] = module.params['primary_dns_server']
    if 'standby_dns_server' in module.params and module.params['standby_dns_server'] is not None:
        domain_data['standby_dns_server'] = module.params['standby_dns_server']
    if 'ip_type' in module.params and module.params['ip_type'] is not None:
        domain_data['ip_type'] = module.params['ip_type']

    # 转换为JSON格式
    post_data = json.dumps(domain_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
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
        module.fail_json(msg="添加域名解析自定义失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加域名解析自定义", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_domain_table(module):
    """删除域名解析自定义"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除域名解析自定义需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.domaintable.del" % (
        ip, authkey)

    # 构造域名表数据
    domain_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(domain_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
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
        module.fail_json(msg="删除域名解析自定义失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除域名解析自定义", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_domain_files(module):
    """查看域名表文件列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.domaintable.file.list" % (
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
        module.fail_json(msg="查看域名表文件列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="查看域名表文件列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, domain_files=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_upload_domain_file(module):
    """上传域名表文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    file_path = module.params.get('file_path')

    # 检查必需参数
    if not name:
        module.fail_json(msg="上传域名表文件需要提供name参数")
    if not file_path or not os.path.exists(file_path):
        module.fail_json(msg="上传域名表文件需要提供有效的file_path参数")

    # 读取文件内容
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
    except Exception as e:
        module.fail_json(msg="读取文件失败: %s" % str(e))

    # 构造请求URL
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
            body_parts.append('Content-Type: application/octet-stream')  # 二进制文件类型
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
            body_parts.append('Content-Type: application/octet-stream')  # 二进制文件类型
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
                response_data, "上传域名表文件", True)
            if success:
                module.exit_json(**result_dict)
            else:
                module.fail_json(**result_dict)
        else:
            module.fail_json(msg="未收到有效响应")
    except Exception as e:
        module.fail_json(msg="上传域名表文件失败: %s" % str(e))


def adc_delete_domain_file(module):
    """删除域名表文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.domaintable.file.delete" % (
        ip, authkey)

    # 构造域名文件数据
    file_data = {}

    # 添加可选参数
    if 'name' in module.params and module.params['name'] is not None:
        file_data['name'] = module.params['name']

    # 转换为JSON格式
    post_data = json.dumps(file_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
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
        module.fail_json(msg="删除域名表文件失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除域名表文件", True)
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
            'list_domain_tables', 'add_domain_table', 'delete_domain_table',
            'list_domain_files', 'upload_domain_file', 'delete_domain_file']),
        # 域名表参数
        name=dict(type='str', required=False),
        ttl=dict(type='int', required=False),
        primary_dns_server=dict(type='str', required=False),
        standby_dns_server=dict(type='str', required=False),
        ip_type=dict(type='int', required=False, choices=[0, 1]),
        file_path=dict(type='str', required=False)  # 上传时的本地文件路径
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
        required_if=[
            ['action', 'upload_domain_file', ['file_path']]
        ]
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list_domain_tables':
        adc_list_domain_tables(module)
    elif action == 'add_domain_table':
        adc_add_domain_table(module)
    elif action == 'delete_domain_table':
        adc_delete_domain_table(module)
    elif action == 'list_domain_files':
        adc_list_domain_files(module)
    elif action == 'upload_domain_file':
        adc_upload_domain_file(module)
    elif action == 'delete_domain_file':
        adc_delete_domain_file(module)


if __name__ == '__main__':
    main()
