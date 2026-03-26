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


def slb_syn_cookie_get(module):
    """获取全局SYN Cookie配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.syn_cookie.get" % (
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
        module.fail_json(msg="获取全局SYN Cookie配置失败: %s" % str(e))

    # 对于获取配置操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取全局SYN Cookie配置失败",
                                 response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_syn_cookie_edit(module):
    """设置全局SYN Cookie配置"""
    device_ip = module.params['ip']
    authkey = module.params['authkey']
    synflood = module.params.get('synflood', {})


    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.syn_cookie.edit" % (
        device_ip, authkey)

    # 构造SYN Cookie配置数据 - 使用API要求的synflood对象
    # 优先使用synflood参数，向后兼容支持扁平参数
    config_data = {"synflood": {}}

    # 如果提供了synflood对象，直接使用
    if synflood:
        config_data['synflood'] = synflood


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
        module.fail_json(msg="设置全局SYN Cookie配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置全局SYN Cookie配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_vs_syn_cookie_get(module):
    """获取每虚拟服务SYN Cookie配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    synflood = module.params.get('synflood', {})


    # 检查必需参数

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.vs.syn_cookie.get" % (
        ip, authkey)

    # 构造请求数据
    config_data = {"synflood": {}}

    # 如果提供了synflood对象，直接使用
    if synflood:
        config_data['synflood'] = synflood

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
        module.fail_json(msg="获取每虚拟服务SYN Cookie配置失败: %s" % str(e))

    # 对于获取配置操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取每虚拟服务SYN Cookie配置失败",
                                 response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_vs_syn_cookie_edit(module):
    """设置每虚拟服务SYN Cookie配置"""
    device_ip = module.params['ip']
    authkey = module.params['authkey']
    vs_name = module.params.get('vs_name')
    vs_synflood = module.params.get('vs_synflood', {})
    sfnum_cfg = module.params.get('sfnum_cfg')
    sfnum_enable = module.params.get('sfnum_enable')
    sfnum_relieve = module.params.get('sfnum_relieve')
    sfnum_interval = module.params.get('sfnum_interval')

    # 检查必需参数
    if not vs_name:
        module.fail_json(msg="设置每虚拟服务SYN Cookie配置需要提供vs_name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.vs.syn_cookie.edit" % (
        device_ip, authkey)

    # 构造SYN Cookie配置数据 - 使用API要求的vs_synflood对象
    # 优先使用vs_synflood参数，向后兼容支持扁平参数
    config_data = {
        "vs_name": vs_name,
        "vs_synflood": {}
    }

    # 如果提供了vs_synflood对象，直接使用
    if vs_synflood:
        config_data['vs_synflood'] = vs_synflood

    # 向后兼容：如果提供了扁平参数，添加到vs_synflood对象中
    if sfnum_cfg is not None:
        config_data['vs_synflood']['sfnum_cfg'] = sfnum_cfg
    if sfnum_enable is not None:
        config_data['vs_synflood']['sfnum_enable'] = sfnum_enable
    if sfnum_relieve is not None:
        config_data['vs_synflood']['sfnum_relieve'] = sfnum_relieve
    if sfnum_interval is not None:
        config_data['vs_synflood']['sfnum_interval'] = sfnum_interval

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
        module.fail_json(msg="设置每虚拟服务SYN Cookie配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置每虚拟服务SYN Cookie配置", True)
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
            'slb_syn_cookie_get', 'slb_syn_cookie_edit',
            'slb_vs_syn_cookie_get', 'slb_vs_syn_cookie_edit']),
        # SYN Cookie参数 - 支持API格式的嵌套对象和向后兼容的扁平参数
        synflood=dict(type='dict', required=False),  # API格式：{"sfnum_cfg": 1, "sfnum_enable": 1000, "sfnum_relieve": 100}
        vs_synflood=dict(type='dict', required=False),  # API格式：{"sfnum_cfg": 1, "sfnum_enable": 1000, "sfnum_relieve": 100, "sfnum_interval": 10}
        sfnum_cfg=dict(type='int', required=False),  # 向后兼容
        sfnum_enable=dict(type='int', required=False),  # 向后兼容
        sfnum_relieve=dict(type='int', required=False),  # 向后兼容
        sfnum_interval=dict(type='int', required=False),  # 向后兼容
        vs_name=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'slb_syn_cookie_get':
        slb_syn_cookie_get(module)
    elif action == 'slb_syn_cookie_edit':
        slb_syn_cookie_edit(module)
    elif action == 'slb_vs_syn_cookie_get':
        slb_vs_syn_cookie_get(module)
    elif action == 'slb_vs_syn_cookie_edit':
        slb_vs_syn_cookie_edit(module)


if __name__ == '__main__':
    main()
