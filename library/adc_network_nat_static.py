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


def nat_static_list(module):
    """获取静态NAT列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.static.list" % (
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
        module.fail_json(msg="获取静态NAT列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取静态NAT列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, statics=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def nat_static_get(module):
    """获取静态NAT详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="获取静态NAT详情需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.static.get" % (
        ip, authkey)

    # 构造请求数据
    static_data = {
        "id": id
    }

    # 转换为JSON格式
    post_data = json.dumps(static_data)

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
        module.fail_json(msg="获取静态NAT详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取静态NAT详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, static=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def nat_static_add(module):
    """添加静态NAT"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""
    ip_addr = module.params['ip_addr'] if 'ip_addr' in module.params else ""
    nat_ip = module.params['nat_ip'] if 'nat_ip' in module.params else ""

    # 检查必需参数
    if not id or not ip_addr or not nat_ip:
        module.fail_json(msg="添加静态NAT需要提供id、ip_addr和nat_ip参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.static.add" % (
        ip, authkey)

    # 构造静态NAT数据
    static_data = {
        "id": id,
        "ip_addr": ip_addr,
        "nat_ip": nat_ip
    }

    # 添加可选参数
    if 'description' in module.params and module.params['description'] is not None:
        static_data['description'] = module.params['description']

    # 转换为JSON格式
    post_data = json.dumps(static_data)

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
        module.fail_json(msg="添加静态NAT失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加静态NAT", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def nat_static_edit(module):
    """编辑静态NAT"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="编辑静态NAT需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.static.edit" % (
        ip, authkey)

    # 构造静态NAT数据
    static_data = {
        "id": id
    }

    # 添加可选参数
    if 'ip_addr' in module.params and module.params['ip_addr'] is not None:
        static_data['ip_addr'] = module.params['ip_addr']
    if 'nat_ip' in module.params and module.params['nat_ip'] is not None:
        static_data['nat_ip'] = module.params['nat_ip']
    if 'description' in module.params and module.params['description'] is not None:
        static_data['description'] = module.params['description']

    # 转换为JSON格式
    post_data = json.dumps(static_data)

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
        module.fail_json(msg="编辑静态NAT失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑静态NAT", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def nat_static_del(module):
    """删除静态NAT"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="删除静态NAT需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.static.del" % (
        ip, authkey)

    # 构造请求数据
    static_data = {
        "id": id
    }

    # 转换为JSON格式
    post_data = json.dumps(static_data)

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
        module.fail_json(msg="删除静态NAT失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除静态NAT", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def nat_static_statistics_get(module):
    """获取NAT静态映射统计信息"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.static.statis" % (
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
        module.fail_json(msg="获取NAT静态映射统计信息失败: %s" % str(e))

    # 对于获取统计信息操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取NAT静态映射统计信息失败", response=parsed_data)
            else:
                module.exit_json(changed=False, statistics=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def nat_static_statistics_clear(module):
    """清除NAT静态映射统计信息"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=nat.static.clear" % (
        ip, authkey)

    # 构造空数据
    post_data = json.dumps({})

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
        module.fail_json(msg="清除NAT静态映射统计信息失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "清除NAT静态映射统计信息", True)
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
            'nat_static_list', 'nat_static_get', 'nat_static_add', 'nat_static_edit', 'nat_static_del',
            'nat_static_statistics_get', 'nat_static_statistics_clear']),
        # 静态NAT参数
        id=dict(type='int', required=False),
        ip_addr=dict(type='str', required=False),
        nat_ip=dict(type='str', required=False),
        description=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'nat_static_list':
        nat_static_list(module)
    elif action == 'nat_static_get':
        nat_static_get(module)
    elif action == 'nat_static_add':
        nat_static_add(module)
    elif action == 'nat_static_edit':
        nat_static_edit(module)
    elif action == 'nat_static_del':
        nat_static_del(module)
    elif action == 'nat_static_statistics_get':
        nat_static_statistics_get(module)
    elif action == 'nat_static_statistics_clear':
        nat_static_statistics_clear(module)


if __name__ == '__main__':
    main()
