#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import json
import sys
import os
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
    format_adc_response_for_ansible,
    send_request
)

# ADC API响应解析函数


def adc_list_healthchecks(module):
    """获取健康检查列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.list" % (
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
        module.fail_json(msg="获取健康检查列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取健康检查列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, healthchecks=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_healthcheck(module):
    """获取健康检查详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取健康检查详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.get" % (
        ip, authkey)

    # 构造请求数据
    hc_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(hc_data)

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
        module.fail_json(msg="获取健康检查详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取健康检查详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, healthcheck=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_healthcheck(module):
    """添加健康检查"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.add" % (
        ip, authkey)

    # 构造健康检查数据 - 只包含在YAML中明确定义的参数
    hc_data = {}

    # 定义可选参数列表
    optional_params = [
        'name', 'type', 'retry', 'interval', 'timeout', 'up_check_cnt', 'wait_all_retry',
        'description', 'auto_disable', 'alias_ipv4_src', 'alias_ipv6_src', 'interface',
        'alias_ipv4', 'alias_ipv6', 'alias_port', 'port', 'http_version',
        'mode', 'icmp_alias_addr', 'host', 'url', 'post_data', 'post_file',
        'username', 'password', 'code', 'pattern', 'pattern_disable_str',
        'server_fail_code', 'trans_mode', 'sslver', 'combo'
    ]

    # 添加基本参数
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            hc_data[param] = module.params[param]

    # 转换为JSON格式
    post_data = json.dumps(hc_data)

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
        module.fail_json(msg="添加健康检查失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加健康检查", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_healthcheck(module):
    """编辑健康检查"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.edit" % (
        ip, authkey)

    # 构造健康检查数据 - 只包含在YAML中明确定义的参数
    hc_data = {}

    # 定义可选参数列表
    optional_params = [
        'name', 'type', 'retry', 'interval', 'timeout', 'up_check_cnt', 'wait_all_retry',
        'description', 'auto_disable', 'alias_ipv4_src', 'alias_ipv6_src', 'interface',
        'alias_ipv4', 'alias_ipv6', 'alias_port', 'port', 'http_version',
        'mode', 'icmp_alias_addr', 'host', 'url', 'post_data', 'post_file',
        'username', 'password', 'code', 'pattern', 'pattern_disable_str',
        'server_fail_code', 'trans_mode', 'sslver', 'combo'
    ]

    # 添加基本参数
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            hc_data[param] = module.params[param]

    # 转换为JSON格式
    post_data = json.dumps(hc_data)

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
        module.fail_json(msg="编辑健康检查失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑健康检查", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_healthcheck(module):
    """删除健康检查"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除健康检查需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.del" % (
        ip, authkey)

    # 构造健康检查数据
    hc_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(hc_data)

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
        module.fail_json(msg="删除健康检查失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除健康检查", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_slb_healthcheck_adc_slb_healthcheck_script_list(module):
    """获取健康检查脚本列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.script.list" % (ip, authkey)

    response_data = ""
    try:
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
    except Exception as e:
        module.fail_json(msg="获取健康检查脚本列表失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取健康检查脚本列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, scripts=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_slb_healthcheck_adc_slb_healthcheck_script_upload(module):
    """上传健康检查脚本"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    script_name = module.params['script_name'] if 'script_name' in module.params else ""
    script_content = module.params['script_content'] if 'script_content' in module.params else ""
    script_path = module.params.get('file_path')

    # 检查必要参数
    if not script_name:
        module.fail_json(msg="上传脚本需要提供script_name参数")

    # 优先使用文件路径读取脚本内容
    if script_path and os.path.exists(script_path):
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
        except Exception as e:
            module.fail_json(msg="读取脚本文件失败: %s" % str(e))
    elif not script_content:
        module.fail_json(msg="上传脚本需要提供script_content参数或file_path参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.script.upload" % (ip, authkey)

    script_data = {
        "name": script_name,
        "content": script_content
    }

    post_data = json.dumps(script_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="上传健康检查脚本失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "上传健康检查脚本", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_slb_healthcheck_adc_slb_healthcheck_script_del(module):
    """删除健康检查脚本"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    script_name = module.params['script_name'] if 'script_name' in module.params else ""

    if not script_name:
        module.fail_json(msg="删除脚本需要提供script_name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.script.del" % (ip, authkey)

    script_data = {
        "name": script_name
    }

    post_data = json.dumps(script_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="删除健康检查脚本失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除健康检查脚本", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_slb_healthcheck_adc_slb_healthcheck_postfile_list(module):
    """获取健康检查后置文件列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.postfile.list" % (ip, authkey)

    response_data = ""
    try:
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
    except Exception as e:
        module.fail_json(msg="获取健康检查后置文件列表失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取健康检查后置文件列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, postfiles=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_slb_healthcheck_adc_slb_healthcheck_postfile_upload(module):
    """上传健康检查后置文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_name = module.params['file_name'] if 'file_name' in module.params else ""
    file_path = module.params.get('file_path')

    # 检查必要参数
    if not file_name:
        module.fail_json(msg="上传后置文件需要提供file_name参数")
    if not file_path or not os.path.exists(file_path):
        module.fail_json(msg="上传后置文件需要提供有效的file_path参数")

    # 读取文件内容
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
    except Exception as e:
        module.fail_json(msg="读取文件失败: %s" % str(e))

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.postfile.upload" % (ip, authkey)

    try:
        # 根据Python版本处理multipart/form-data上传
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
            body_parts.append('--%s' % boundary)
            body_parts.append('Content-Disposition: form-data; name="name"')
            body_parts.append('')
            body_parts.append(file_name)
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
            body_parts.append('--%s' % boundary)
            body_parts.append('Content-Disposition: form-data; name="name"')
            body_parts.append('')
            body_parts.append(file_name)
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
                response_data, "上传健康检查后置文件", True)
            if success:
                module.exit_json(**result_dict)
            else:
                module.fail_json(**result_dict)
        else:
            module.fail_json(msg="未收到有效响应")
    except Exception as e:
        module.fail_json(msg="上传健康检查后置文件失败: %s" % str(e))


def adc_slb_healthcheck_adc_slb_healthcheck_postfile_del(module):
    """删除健康检查后置文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_name = module.params['file_name'] if 'file_name' in module.params else ""

    if not file_name:
        module.fail_json(msg="删除后置文件需要提供file_name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.postfile.del" % (ip, authkey)

    file_data = {
        "name": file_name
    }

    post_data = json.dumps(file_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="删除健康检查后置文件失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除健康检查后置文件", True)
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
                    'list_healthchecks', 'get_healthcheck', 'add_healthcheck', 'edit_healthcheck', 'delete_healthcheck',
                    'adc_slb_healthcheck_script_list', 'adc_slb_healthcheck_script_upload', 'adc_slb_healthcheck_script_del', 'adc_slb_healthcheck_postfile_list', 'adc_slb_healthcheck_postfile_upload', 'adc_slb_healthcheck_postfile_del']),
        # 健康检查通用参数
        name=dict(type='str', required=False),
        hc_type=dict(type='str', required=False, choices=[
            'icmp', 'http', 'https', 'tcp', 'udp', 'combo', 'arp', 'database', 'dns', 'ftp',
            'imap', 'ldap', 'ntp', 'pop3', 'radius', 'rtsp', 'sip', 'smtp', 'snmp']),
        retry=dict(type='int', required=False),
        interval=dict(type='int', required=False),
        timeout=dict(type='int', required=False),
        description=dict(type='str', required=False),
        auto_disable=dict(type='int', required=False),
        alias_ipv4_src=dict(type='str', required=False),
        alias_ipv6_src=dict(type='str', required=False),
        interface=dict(type='str', required=False),
        alias_ipv4=dict(type='str', required=False),
        alias_ipv6=dict(type='str', required=False),
        alias_port=dict(type='int', required=False),
        port=dict(type='int', required=False),
        up_check_cnt=dict(type='int', required=False),
        wait_all_retry=dict(type='int', required=False),
        http_version=dict(type='str', required=False),
        # ICMP类型参数
        mode=dict(type='str', required=False),
        icmp_alias_addr=dict(type='str', required=False),
        # HTTP/HTTPS类型参数
        host=dict(type='str', required=False),
        url=dict(type='str', required=False),
        post_data=dict(type='str', required=False),
        post_file=dict(type='str', required=False),
        username=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        code=dict(type='str', required=False),
        pattern=dict(type='str', required=False),
        pattern_disable_str=dict(type='str', required=False),
        server_fail_code=dict(type='str', required=False),
        trans_mode=dict(type='int', required=False),
        sslver=dict(type='str', required=False),
        # Combo类型参数
        combo=dict(type='str', required=False),
        # 脚本上传参数
        script_name=dict(type='str', required=False),
        script_content=dict(type='str', required=False),
        # 后置文件参数
        file_name=dict(type='str', required=False),
        file_path=dict(type='str', required=False)  # 上传时的本地文件路径
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action'] if 'action' in module.params else ''
    # 为了解决静态检查工具的问题，我们进行类型转换
    if hasattr(action, '__str__'):
        action = str(action)

    if action == 'list_healthchecks':
        adc_list_healthchecks(module)
    elif action == 'get_healthcheck':
        adc_get_healthcheck(module)
    elif action == 'add_healthcheck':
        adc_add_healthcheck(module)
    elif action == 'edit_healthcheck':
        adc_edit_healthcheck(module)
    elif action == 'delete_healthcheck':
        adc_delete_healthcheck(module)
    elif action == 'adc_slb_healthcheck_script_list':
        adc_slb_healthcheck_script_list(module)
    elif action == 'adc_slb_healthcheck_script_upload':
        adc_slb_healthcheck_script_upload(module)
    elif action == 'adc_slb_healthcheck_script_del':
        adc_slb_healthcheck_script_del(module)
    elif action == 'adc_slb_healthcheck_postfile_list':
        adc_slb_healthcheck_postfile_list(module)
    elif action == 'adc_slb_healthcheck_postfile_upload':
        adc_slb_healthcheck_postfile_upload(module)
    elif action == 'adc_slb_healthcheck_postfile_del':
        adc_slb_healthcheck_postfile_del(module)


if __name__ == '__main__':
    main()
