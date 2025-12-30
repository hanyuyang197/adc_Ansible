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


def adc_add_config_file(module):
    """添加配置文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_name = module.params['file_name']
    description = module.params['description']
    flag = module.params['flag']
    password = module.params['password']

    # 检查必需参数
    if not file_name:
        module.fail_json(msg="添加配置文件需要提供file_name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.config.add" % (
        ip, authkey)

    # 构造配置文件数据
    config_data = {
        "file_name": file_name
    }

    # 添加可选参数
    if description is not None:
        config_data["description"] = description
    if flag is not None:
        config_data["flag"] = flag
    if password is not None:
        config_data["password"] = password

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(config_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(config_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="添加配置文件失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加配置文件", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_config_files(module):
    """获取配置文件列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.config.list" % (
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
        module.fail_json(msg="获取配置文件列表失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取配置文件列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, files=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_apply_config_file(module):
    """指定配置文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_name = module.params['file_name']

    # 检查必需参数
    if not file_name:
        module.fail_json(msg="指定配置文件需要提供file_name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.config.apply" % (
        ip, authkey)

    # 构造配置文件数据
    config_data = {
        "file_name": file_name
    }

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(config_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(config_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="指定配置文件失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "指定配置文件", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_config_file(module):
    """删除配置文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    file_name = module.params['file_name']

    # 检查必需参数
    if not file_name:
        module.fail_json(msg="删除配置文件需要提供file_name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.config.del" % (
        ip, authkey)

    # 构造配置文件数据
    config_data = {
        "file_name": file_name
    }

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(config_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(config_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="删除配置文件失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除配置文件", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_backup_config_file(module):
    """配置文件导出"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 构造请求URL
    if name:
        # 导出指定名称备份的配置
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.config.backup" % (
            ip, authkey)
        backup_data = {
            "name": name
        }

        # 初始化响应数据
        response_data = ""

        try:
            # 根据Python版本处理编码
            if sys.version_info[0] >= 3:
                # Python 3
                import urllib.request as urllib_request
                post_data = json.dumps(backup_data)
                post_data = post_data.encode('utf-8')
                req = urllib_request.Request(url, data=post_data, headers={
                                             'Content-Type': 'application/json'})
                response = urllib_request.urlopen(req)
                response_data = response.read().decode('utf-8')
            else:
                # Python 2
                import urllib2 as urllib_request
                post_data = json.dumps(backup_data)
                req = urllib_request.Request(url, data=post_data, headers={
                                             'Content-Type': 'application/json'})
                response = urllib_request.urlopen(req)
                response_data = response.read()

        except Exception as e:
            module.fail_json(msg="配置文件导出失败: %s" % str(e))
    else:
        # 下载当前设备的启动配置文件压缩包
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.config.backup" % (
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
            module.fail_json(msg="配置文件导出失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "配置文件导出", False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_restore_config_file(module):
    """配置文件导入"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.config.restore" % (
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
        module.fail_json(msg="配置文件导入失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "配置文件导入", True)
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
            'add_config_file', 'list_config_files', 'apply_config_file', 'delete_config_file',
            'backup_config_file', 'restore_config_file']),
        # 配置文件参数
        file_name=dict(type='str', required=False),
        description=dict(type='str', required=False),
        flag=dict(type='int', required=False),
        password=dict(type='str', required=False, no_log=True),
        name=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'add_config_file':
        adc_add_config_file(module)
    elif action == 'list_config_files':
        adc_list_config_files(module)
    elif action == 'apply_config_file':
        adc_apply_config_file(module)
    elif action == 'delete_config_file':
        adc_delete_config_file(module)
    elif action == 'backup_config_file':
        adc_backup_config_file(module)
    elif action == 'restore_config_file':
        adc_restore_config_file(module)


if __name__ == '__main__':
    main()
