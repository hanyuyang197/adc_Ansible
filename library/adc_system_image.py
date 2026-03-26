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


def system_image_list(module):
    """获取版本镜像列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.image.list" % (ip, authkey)

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
        module.fail_json(msg="获取版本镜像列表失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取版本镜像列表", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_image_apply(module):
    """指定镜像"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_name = module.params['file_name']

    # 构造请求数据
    apply_data = {
        'file_name': file_name
    }

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.image.apply" % (ip, authkey)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = json.dumps(apply_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            post_data = json.dumps(apply_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="指定镜像失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "指定镜像", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def system_image_upload(module):
    """上传镜像（支持 FTP/TFTP 和 HTTP/HTTPS 方式）"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    # upload_method = module.params.get('upload_method')  # 上传方式：ftp、tftp、http、https



    webfilename = module.params.get('webfilename')
    file_path = module.params.get('file_path')
    reboot = module.params.get('reboot')
    save_config = module.params.get('save_config')

    # 必选参数验证
    if file_path is None:
        module.fail_json(msg="file_path 参数是必需的")

    # 构造请求URL（参数在 URL 中）
    url_params = []
    url_params.append("authkey=%s" % authkey)
    url_params.append("action=system.image.upload")
    url_params.append("webfilename=%s" % webfilename)
    if reboot is not None:
        url_params.append("reboot=%d" % reboot)
    if save_config is not None:
        url_params.append("save_config=%d" % save_config)

    url = "http://%s/webupload/adcapi/v2.0/?%s" % (ip, '&'.join(url_params))

    if sys.version_info[0] >= 3:
        import urllib.request as urllib_request
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # 使用 multipart/form-data 方式上传
        # 注意：Python 标准库不支持 multipart/form-data，需要构造请求
        # 这里简化处理，实际应用中可能需要使用 requests 库或手动构造 multipart
        boundary = '----WebKitFormBoundary' + ''.join([str(i) for i in range(16)])
        
        # 构造 multipart/form-data body
        body = []
        body.append(('--' + boundary).encode('utf-8'))
        body.append(('Content-Disposition: form-data; name="file"; filename="%s"' % webfilename).encode('utf-8'))
        body.append('Content-Type: application/octet-stream'.encode('utf-8'))
        body.append(b'')
        body.append(file_data)
        body.append(('--' + boundary + '--').encode('utf-8'))
        body.append(b'')
        
        post_data = b'\r\n'.join(body)
        
        req = urllib_request.Request(url, data=post_data, headers={
            'Content-Type': 'multipart/form-data; boundary=%s' % boundary
        })
        response = urllib_request.urlopen(req)
        response_data = response.read().decode('utf-8')
    else:
        import urllib2 as urllib_request
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # 构造 multipart/form-data body
        boundary = '----WebKitFormBoundary' + ''.join([str(i) for i in range(16)])
        
        body = []
        body.append('--' + boundary)
        body.append('Content-Disposition: form-data; name="file"; filename="%s"' % webfilename)
        body.append('Content-Type: application/octet-stream')
        body.append('')
        body.append(file_data)
        body.append('--' + boundary + '--')
        body.append('')
        
        post_data = '\r\n'.join(body)
        post_data = post_data.encode('utf-8')
        
        req = urllib_request.Request(url, data=post_data, headers={
            'Content-Type': 'multipart/form-data; boundary=%s' % boundary
        })
        response = urllib_request.urlopen(req)
        response_data = response.read()


    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "上传镜像", True)
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
            'system_image_list', 'system_image_apply', 'system_image_upload']),
        # system.image.apply 参数
        file_name=dict(type='str', required=False),
        # system.image.upload 上传方式（必选）
        # upload_method=dict(type='str', required=False),  # ftp、tftp、http、https
        # FTP/TFTP 上传参数
        host=dict(type='str', required=False),  # FTP/TFTP 服务器 IP
        location=dict(type='str', required=False),  # 镜像名称（在 FTP/TFTP 根目录）
        port=dict(type='int', required=False),  # 端口号
        username=dict(type='str', required=False),  # FTP 用户名
        password=dict(type='str', required=False, no_log=True),  # FTP 密码
        use_mgmt_port=dict(type='int', required=False),  # 是否使用管理口
        # HTTP/HTTPS 上传参数
        webfilename=dict(type='str', required=False),  # 镜像名称（HTTP/HTTPS）
        file_path=dict(type='str', required=False),  # 本地文件路径
        # 通用参数（不设置默认值）
        reboot=dict(type='int', required=False),  # 上传后是否自动重启
        save_config=dict(type='int', required=False),  # 自动重启时是否保存配置
        protocol=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'system_image_list':
        system_image_list(module)
    elif action == 'system_image_apply':
        system_image_apply(module)
    elif action == 'system_image_upload':
        system_image_upload(module)


if __name__ == '__main__':
    main()
