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


def slb_profile_dns_list(module):
    """获取DNS模板列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dns.list" % (
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
        module.fail_json(msg="获取DNS模板列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取DNS模板列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, profiles=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_dns_list_withcommon(module):
    """获取包含common分区的DNS模板列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dns.list.withcommon" % (
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
        module.fail_json(msg="获取包含common分区的DNS模板列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取包含common分区的DNS模板列表失败",
                                 response=parsed_data)
            else:
                module.exit_json(changed=False, profiles=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_dns_get(module):
    """获取DNS模板详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取DNS模板详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dns.get" % (
        ip, authkey)

    # 构造请求数据
    profile_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(profile_data)

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
        module.fail_json(msg="获取DNS模板详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取DNS模板详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, profile=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_dns_add(module):
    """添加DNS模板"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加DNS模板需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dns.add" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name
    }

    # 定义可选参数列表
    optional_params = [
        'description', 'enabled', 'drop_bad_req', 'default_to_cache',
        'cache_size', 'insert_client_ip', 'netmask', 'ruletable_name', 'ruletables'
    ]

    # 添加可选参数
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            profile_data[param] = module.params[param]

    # 转换为JSON格式
    post_data = json.dumps(profile_data)

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
        module.fail_json(msg="添加DNS模板失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加DNS模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_dns_edit(module):
    """编辑DNS模板"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑DNS模板需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dns.edit" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name
    }

    # 添加可选参数
    if 'description' in module.params and module.params['description'] is not None:
        profile_data['description'] = module.params['description']
    if 'enabled' in module.params and module.params['enabled'] is not None:
        profile_data['enabled'] = module.params['enabled']
    if 'drop_bad_req' in module.params and module.params['drop_bad_req'] is not None:
        profile_data['drop_bad_req'] = module.params['drop_bad_req']
    if 'default_to_cache' in module.params and module.params['default_to_cache'] is not None:
        profile_data['default_to_cache'] = module.params['default_to_cache']
    if 'cache_size' in module.params and module.params['cache_size'] is not None:
        profile_data['cache_size'] = module.params['cache_size']
    if 'insert_client_ip' in module.params and module.params['insert_client_ip'] is not None:
        profile_data['insert_client_ip'] = module.params['insert_client_ip']
    if 'netmask' in module.params and module.params['netmask'] is not None:
        profile_data['netmask'] = module.params['netmask']
    if 'ruletable_name' in module.params and module.params['ruletable_name'] is not None:
        profile_data['ruletable_name'] = module.params['ruletable_name']
    if 'ruletables' in module.params and module.params['ruletables'] is not None:
        profile_data['ruletables'] = module.params['ruletables']

    # 转换为JSON格式
    post_data = json.dumps(profile_data)

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
        module.fail_json(msg="编辑DNS模板失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑DNS模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_dns_del(module):
    """删除DNS模板"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除DNS模板需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dns.del" % (
        ip, authkey)

    # 构造请求数据
    profile_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(profile_data)

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
        module.fail_json(msg="删除DNS模板失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除DNS模板", True)
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
            'slb_profile_dns_list', 'slb_profile_dns_list_withcommon', 'slb_profile_dns_get',
            'slb_profile_dns_add', 'slb_profile_dns_edit', 'slb_profile_dns_del']),
        # DNS模板参数
        name=dict(type='str', required=False),
        description=dict(type='str', required=False),
        enabled=dict(type='int', required=False, choices=[0, 1]),
        drop_bad_req=dict(type='int', required=False, choices=[0, 1]),
        default_to_cache=dict(type='int', required=False, choices=[0, 1]),
        cache_size=dict(type='int', required=False),
        insert_client_ip=dict(type='int', required=False, choices=[0, 1]),
        netmask=dict(type='int', required=False),
        ruletable_name=dict(type='str', required=False),
        ruletables=dict(type='list', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'slb_profile_dns_list':
        slb_profile_dns_list(module)
    elif action == 'slb_profile_dns_list_withcommon':
        slb_profile_dns_list_withcommon(module)
    elif action == 'slb_profile_dns_get':
        slb_profile_dns_get(module)
    elif action == 'slb_profile_dns_add':
        slb_profile_dns_add(module)
    elif action == 'slb_profile_dns_edit':
        slb_profile_dns_edit(module)
    elif action == 'slb_profile_dns_del':
        slb_profile_dns_del(module)


if __name__ == '__main__':
    main()