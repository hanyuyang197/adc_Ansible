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


def adc_list_tcp_profiles(module):
    """获取TCP模板列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.tcp.list" % (
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
        module.fail_json(msg="获取TCP模板列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TCP模板列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, profiles=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_tcp_profiles_withcommon(module):
    """获取包含common分区的TCP模板列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.tcp.list.withcommon" % (
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
        module.fail_json(msg="获取包含common分区的TCP模板列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取包含common分区的TCP模板列表失败",
                                 response=parsed_data)
            else:
                module.exit_json(changed=False, profiles=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_tcp_profile(module):
    """获取TCP模板详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    profile_name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not profile_name:
        module.fail_json(msg="获取TCP模板详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.tcp.get" % (
        ip, authkey)

    # 构造请求数据
    profile_data = {
        "name": profile_name
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
        module.fail_json(msg="获取TCP模板详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TCP模板详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, profile=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_tcp_profile(module):
    """添加TCP模板"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    profile_name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not profile_name:
        module.fail_json(msg="添加TCP模板需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.tcp.add" % (
        ip, authkey)

    # 构造模板数据 - 只包含在YAML中明确定义的参数
    profile_data = {
        "name": profile_name
    }

    # 定义可选参数列表
    optional_params = [
        'description', 'timeout', 'reset_timeout', 'start_win_size',
        'half_close_timeout', 'insertcip', 'generate_isn', 'rstnode',
        'rstclient', 'timestamp', 'loose_initiation', 'loose_close', 'time_wait'
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
        module.fail_json(msg="添加TCP模板失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加TCP模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_tcp_profile(module):
    """编辑TCP模板"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    profile_name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not profile_name:
        module.fail_json(msg="编辑TCP模板需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.tcp.edit" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": profile_name
    }

    # 添加可选参数
    if 'description' in module.params and module.params['description'] is not None:
        profile_data['description'] = module.params['description']
    if 'timeout' in module.params and module.params['timeout'] is not None:
        profile_data['timeout'] = module.params['timeout']
    if 'reset_timeout' in module.params and module.params['reset_timeout'] is not None:
        profile_data['reset_timeout'] = module.params['reset_timeout']
    if 'start_win_size' in module.params and module.params['start_win_size'] is not None:
        profile_data['start_win_size'] = module.params['start_win_size']
    if 'half_close_timeout' in module.params and module.params['half_close_timeout'] is not None:
        profile_data['half_close_timeout'] = module.params['half_close_timeout']
    if 'insertcip' in module.params and module.params['insertcip'] is not None:
        profile_data['insertcip'] = module.params['insertcip']
    if 'generate_isn' in module.params and module.params['generate_isn'] is not None:
        profile_data['generate_isn'] = module.params['generate_isn']
    if 'rstnode' in module.params and module.params['rstnode'] is not None:
        profile_data['rstnode'] = module.params['rstnode']
    if 'rstclient' in module.params and module.params['rstclient'] is not None:
        profile_data['rstclient'] = module.params['rstclient']
    if 'timestamp' in module.params and module.params['timestamp'] is not None:
        profile_data['timestamp'] = module.params['timestamp']
    if 'loose_initiation' in module.params and module.params['loose_initiation'] is not None:
        profile_data['loose_initiation'] = module.params['loose_initiation']
    if 'loose_close' in module.params and module.params['loose_close'] is not None:
        profile_data['loose_close'] = module.params['loose_close']
    if 'time_wait' in module.params and module.params['time_wait'] is not None:
        profile_data['time_wait'] = module.params['time_wait']

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
        module.fail_json(msg="编辑TCP模板失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑TCP模板", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_tcp_profile(module):
    """删除TCP模板"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    profile_name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not profile_name:
        module.fail_json(msg="删除TCP模板需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.tcp.del" % (
        ip, authkey)

    # 构造请求数据
    profile_data = {
        "name": profile_name
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
        module.fail_json(msg="删除TCP模板失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除TCP模板", True)
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
            'list_profiles', 'list_profiles_withcommon', 'get_profile', 'add_profile', 'edit_profile', 'delete_profile']),
        # TCP模板参数
        name=dict(type='str', required=False),
        description=dict(type='str', required=False),
        timeout=dict(type='int', required=False),
        reset_timeout=dict(type='int', required=False),
        start_win_size=dict(type='int', required=False),
        half_close_timeout=dict(type='int', required=False),
        insertcip=dict(type='int', required=False),
        generate_isn=dict(type='int', required=False),
        rstnode=dict(type='int', required=False),
        rstclient=dict(type='int', required=False),
        timestamp=dict(type='int', required=False),
        loose_initiation=dict(type='int', required=False),
        loose_close=dict(type='int', required=False),
        time_wait=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list_profiles':
        adc_list_tcp_profiles(module)
    elif action == 'list_profiles_withcommon':
        adc_list_tcp_profiles_withcommon(module)
    elif action == 'get_profile':
        adc_get_tcp_profile(module)
    elif action == 'add_profile':
        adc_add_tcp_profile(module)
    elif action == 'edit_profile':
        adc_edit_tcp_profile(module)
    elif action == 'delete_profile':
        adc_delete_tcp_profile(module)


if __name__ == '__main__':
    main()
