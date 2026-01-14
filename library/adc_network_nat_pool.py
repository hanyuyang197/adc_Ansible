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


def nat_pool_list(module):
    """获取NAT地址池列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.pool.list" % (
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
        module.fail_json(msg="获取NAT地址池列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取NAT地址池列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, pools=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def nat_pool_get(module):
    """获取NAT地址池详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取NAT地址池详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.pool.get" % (
        ip, authkey)

    # 构造请求数据
    pool_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="获取NAT地址池详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取NAT地址池详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, pool=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def nat_pool_add(module):
    """添加NAT地址池"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    ip_start = module.params['ip_start'] if 'ip_start' in module.params else ""
    ip_end = module.params['ip_end'] if 'ip_end' in module.params else ""

    # 检查必需参数
    if not name or not ip_start or not ip_end:
        module.fail_json(msg="添加NAT地址池需要提供name、ip_start和ip_end参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.pool.add" % (
        ip, authkey)

    # 构造NAT地址池数据 - 按照API文档要求使用外部"pool"对象包装
    pool_object = {
        "name": name,
        "ip_start": ip_start,
        "ip_end": ip_end
    }

    # 添加可选参数到pool对象
    if 'ip_type' in module.params and module.params['ip_type'] is not None:
        pool_object['ip_type'] = module.params['ip_type']
    if 'global_gateway' in module.params and module.params['global_gateway'] is not None:
        pool_object['global_gateway'] = module.params['global_gateway']
    if 'vrid' in module.params and module.params['vrid'] is not None:
        pool_object['vrid'] = module.params['vrid']
    if 'ip_rr' in module.params and module.params['ip_rr'] is not None:
        pool_object['ip_rr'] = module.params['ip_rr']

    # 按照API文档要求，使用外部"pool"对象包装
    pool_data = {
        "pool": pool_object
    }

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="添加NAT地址池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加NAT地址池", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def nat_pool_edit(module):
    """编辑NAT地址池"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑NAT地址池需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.pool.edit" % (
        ip, authkey)

    # 构造NAT地址池数据 - 按照API文档要求使用外部"pool"对象包装
    pool_object = {
        "name": name
    }

    # 添加可选参数到pool对象
    if 'ip_start' in module.params and module.params['ip_start'] is not None:
        pool_object['ip_start'] = module.params['ip_start']
    if 'ip_end' in module.params and module.params['ip_end'] is not None:
        pool_object['ip_end'] = module.params['ip_end']
    if 'ip_type' in module.params and module.params['ip_type'] is not None:
        pool_object['ip_type'] = module.params['ip_type']
    if 'global_gateway' in module.params and module.params['global_gateway'] is not None:
        pool_object['global_gateway'] = module.params['global_gateway']
    if 'vrid' in module.params and module.params['vrid'] is not None:
        pool_object['vrid'] = module.params['vrid']
    if 'ip_rr' in module.params and module.params['ip_rr'] is not None:
        pool_object['ip_rr'] = module.params['ip_rr']

    # 按照API文档要求，使用外部"pool"对象包装
    pool_data = {
        "pool": pool_object
    }

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="编辑NAT地址池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑NAT地址池", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def nat_pool_del(module):
    """删除NAT地址池"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除NAT地址池需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.pool.del" % (
        ip, authkey)

    # 构造请求数据
    pool_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="删除NAT地址池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除NAT地址池", True)
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
            'nat_pool_list', 'nat_pool_get', 'nat_pool_add', 'nat_pool_edit', 'nat_pool_delete']),
        # NAT地址池参数
        name=dict(type='str', required=False),
        ip_start=dict(type='str', required=False),
        ip_end=dict(type='str', required=False),
        ip_type=dict(type='int', required=False),
        global_gateway=dict(type='str', required=False),
        vrid=dict(type='int', required=False),
        ip_rr=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'nat_pool_list':
        nat_pool_list(module)
    elif action == 'nat_pool_get':
        nat_pool_get(module)
    elif action == 'nat_pool_add':
        nat_pool_add(module)
    elif action == 'nat_pool_edit':
        nat_pool_edit(module)
    elif action == 'nat_pool_delete':
        nat_pool_del(module)


if __name__ == '__main__':
    main()
