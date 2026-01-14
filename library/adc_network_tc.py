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


def network_tc_global_get(module):
    """获取全局TC配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.global.get" % (
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
        module.fail_json(msg="获取全局TC配置失败: %s" % str(e))

    # 对于获取配置操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取全局TC配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_global_set(module):
    """设置全局TC配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    enable = module.params['enable'] if 'enable' in module.params else ""

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.global.set" % (
        ip, authkey)

    # 构造全局TC配置数据
    config_data = {}

    # 添加可选参数
    if enable != "":
        config_data['enable'] = enable

    # 转换为JSON格式
    post_data = json.dumps(config_data)

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
        module.fail_json(msg="设置全局TC配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置全局TC配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_list(module):
    """获取TC条目列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    list_type = module.params['list_type'] if 'list_type' in module.params else "normal"

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    if list_type == "withcommon":
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.list.withcommon" % (
            ip, authkey)
    else:
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.list" % (
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
        module.fail_json(msg="获取TC条目列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TC条目列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, entries=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_get(module):
    """获取TC条目详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取TC条目详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.get" % (
        ip, authkey)

    # 构造请求数据
    entry_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(entry_data)

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
        module.fail_json(msg="获取TC条目详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TC条目详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, entry=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_add(module):
    """添加TC条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加TC条目需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.add" % (
        ip, authkey)

    # 构造TC条目数据
    entry_data = {
        "name": name
    }

    # 添加可选参数
    if 'description' in module.params and module.params['description'] is not None:
        entry_data['description'] = module.params['description']
    if 'bandwidth' in module.params and module.params['bandwidth'] is not None:
        entry_data['bandwidth'] = module.params['bandwidth']

    # 转换为JSON格式
    post_data = json.dumps(entry_data)

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
        module.fail_json(msg="添加TC条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加TC条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_edit(module):
    """编辑TC条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑TC条目需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.edit" % (
        ip, authkey)

    # 构造TC条目数据
    entry_data = {
        "name": name
    }

    # 添加可选参数
    if 'description' in module.params and module.params['description'] is not None:
        entry_data['description'] = module.params['description']
    if 'bandwidth' in module.params and module.params['bandwidth'] is not None:
        entry_data['bandwidth'] = module.params['bandwidth']

    # 转换为JSON格式
    post_data = json.dumps(entry_data)

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
        module.fail_json(msg="编辑TC条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑TC条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_del(module):
    """删除TC条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除TC条目需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.del" % (
        ip, authkey)

    # 构造请求数据
    entry_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(entry_data)

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
        module.fail_json(msg="删除TC条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除TC条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_rule_list(module):
    """获取TC规则列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tc_name = module.params['tc_name'] if 'tc_name' in module.params else ""

    # 检查必需参数
    if not tc_name:
        module.fail_json(msg="获取TC规则列表需要提供tc_name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.rule.list" % (
        ip, authkey)

    # 构造请求数据
    rule_data = {
        "tc_name": tc_name
    }

    # 转换为JSON格式
    post_data = json.dumps(rule_data)

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
        module.fail_json(msg="获取TC规则列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TC规则列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, rules=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_rule_get(module):
    """获取TC规则详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tc_name = module.params['tc_name'] if 'tc_name' in module.params else ""
    rule_id = module.params['rule_id'] if 'rule_id' in module.params else ""

    # 检查必需参数
    if not tc_name or not rule_id:
        module.fail_json(msg="获取TC规则详情需要提供tc_name和rule_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.rule.get" % (
        ip, authkey)

    # 构造请求数据
    rule_data = {
        "tc_name": tc_name,
        "rule_id": rule_id
    }

    # 转换为JSON格式
    post_data = json.dumps(rule_data)

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
        module.fail_json(msg="获取TC规则详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TC规则详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, rule=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_rule_add(module):
    """添加TC规则"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tc_name = module.params['tc_name'] if 'tc_name' in module.params else ""
    rule_id = module.params['rule_id'] if 'rule_id' in module.params else ""

    # 检查必需参数
    if not tc_name or not rule_id:
        module.fail_json(msg="添加TC规则需要提供tc_name和rule_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.rule.add" % (
        ip, authkey)

    # 构造TC规则数据
    rule_data = {
        "tc_name": tc_name,
        "rule_id": rule_id
    }

    # 添加可选参数
    if 'source_ip' in module.params and module.params['source_ip'] is not None:
        rule_data['source_ip'] = module.params['source_ip']
    if 'destination_ip' in module.params and module.params['destination_ip'] is not None:
        rule_data['destination_ip'] = module.params['destination_ip']
    if 'protocol' in module.params and module.params['protocol'] is not None:
        rule_data['protocol'] = module.params['protocol']
    if 'source_port' in module.params and module.params['source_port'] is not None:
        rule_data['source_port'] = module.params['source_port']
    if 'destination_port' in module.params and module.params['destination_port'] is not None:
        rule_data['destination_port'] = module.params['destination_port']

    # 转换为JSON格式
    post_data = json.dumps(rule_data)

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
        module.fail_json(msg="添加TC规则失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加TC规则", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_rule_edit(module):
    """编辑TC规则"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tc_name = module.params['tc_name'] if 'tc_name' in module.params else ""
    rule_id = module.params['rule_id'] if 'rule_id' in module.params else ""

    # 检查必需参数
    if not tc_name or not rule_id:
        module.fail_json(msg="编辑TC规则需要提供tc_name和rule_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.rule.edit" % (
        ip, authkey)

    # 构造TC规则数据
    rule_data = {
        "tc_name": tc_name,
        "rule_id": rule_id
    }

    # 添加可选参数
    if 'source_ip' in module.params and module.params['source_ip'] is not None:
        rule_data['source_ip'] = module.params['source_ip']
    if 'destination_ip' in module.params and module.params['destination_ip'] is not None:
        rule_data['destination_ip'] = module.params['destination_ip']
    if 'protocol' in module.params and module.params['protocol'] is not None:
        rule_data['protocol'] = module.params['protocol']
    if 'source_port' in module.params and module.params['source_port'] is not None:
        rule_data['source_port'] = module.params['source_port']
    if 'destination_port' in module.params and module.params['destination_port'] is not None:
        rule_data['destination_port'] = module.params['destination_port']

    # 转换为JSON格式
    post_data = json.dumps(rule_data)

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
        module.fail_json(msg="编辑TC规则失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑TC规则", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def network_tc_rule_del(module):
    """删除TC规则"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tc_name = module.params['tc_name'] if 'tc_name' in module.params else ""
    rule_id = module.params['rule_id'] if 'rule_id' in module.params else ""

    # 检查必需参数
    if not tc_name or not rule_id:
        module.fail_json(msg="删除TC规则需要提供tc_name和rule_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.rule.del" % (
        ip, authkey)

    # 构造请求数据
    rule_data = {
        "tc_name": tc_name,
        "rule_id": rule_id
    }

    # 转换为JSON格式
    post_data = json.dumps(rule_data)

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
        module.fail_json(msg="删除TC规则失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除TC规则", True)
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
            'network_tc_global_get', 'network_tc_global_set',
            'network_tc_list', 'network_tc_get', 'network_tc_add', 'network_tc_edit', 'network_tc_del',
            'network_tc_rule_list', 'network_tc_rule_get', 'network_tc_rule_add', 'network_tc_rule_edit', 'network_tc_rule_del']),
        # TC参数
        name=dict(type='str', required=False),
        tc_name=dict(type='str', required=False),
        rule_id=dict(type='str', required=False),
        description=dict(type='str', required=False),
        bandwidth=dict(type='int', required=False),
        source_ip=dict(type='str', required=False),
        destination_ip=dict(type='str', required=False),
        protocol=dict(type='str', required=False),
        source_port=dict(type='int', required=False),
        destination_port=dict(type='int', required=False),
        enable=dict(type='int', required=False),
        list_type=dict(type='str', required=False,
                       choices=['normal', 'withcommon'])
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'network_tc_global_get':
        network_tc_global_get(module)
    elif action == 'network_tc_global_set':
        network_tc_global_set(module)
    elif action == 'network_tc_list':
        network_tc_list(module)
    elif action == 'network_tc_get':
        network_tc_get(module)
    elif action == 'network_tc_add':
        network_tc_add(module)
    elif action == 'network_tc_edit':
        network_tc_edit(module)
    elif action == 'network_tc_del':
        network_tc_del(module)
    elif action == 'network_tc_rule_list':
        network_tc_rule_list(module)
    elif action == 'network_tc_rule_get':
        network_tc_rule_get(module)
    elif action == 'network_tc_rule_add':
        network_tc_rule_add(module)
    elif action == 'network_tc_rule_edit':
        network_tc_rule_edit(module)
    elif action == 'network_tc_rule_del':
        network_tc_rule_del(module)


if __name__ == '__main__':
    main()
