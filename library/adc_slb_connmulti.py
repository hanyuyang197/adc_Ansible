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


def send_request(url, post_data=None):
    """发送HTTP请求的通用函数"""
    response_data = ""
    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            if post_data:
                post_data = post_data.encode('utf-8')
                req = urllib_request.Request(url, data=post_data, method='POST', headers={
                                             'Content-Type': 'application/json'})
            else:
                req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            if post_data:
                post_data = post_data.encode('utf-8')
                req = urllib_request.Request(url, data=post_data, headers={
                                             'Content-Type': 'application/json'})
                req.get_method = lambda: 'POST'
            else:
                req = urllib_request.Request(url)
                req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        raise Exception(str(e))

    # 直接返回响应内容，不尝试解析JSON
    return response_data


def adc_connmulti_list(module):
    """连接复用模板列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.connmulti.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, connmulti_list=response_data)
    except Exception as e:
        module.fail_json(msg="连接复用模板列表获取失败: %s" % str(e))


def adc_connmulti_list_withcommon(module):
    """连接复用模板获取 common 和本分区"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.connmulti.list.withcommon" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(
            chchanged=False, connmulti_list_withcommon=response_data)
    except Exception as e:
        module.fail_json(msg="连接复用模板获取 common 和本分区失败: %s" % str(e))


def adc_connmulti_get(module):
    """获取连接复用模板"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="获取连接复用模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.connmulti.get" % (
        ip, authkey)

    connmulti_data = {
        "name": name
    }

    post_data = json.dumps(connmulti_data)

    try:
        response_data = send_request(url, post_data)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, connmulti_data=response_data)
    except Exception as e:
        module.fail_json(msg="获取连接复用模板失败: %s" % str(e))


def adc_connmulti_add(module):
    """连接复用模板添加"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="连接复用模板添加需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.connmulti.add" % (
        ip, authkey)

    connmulti_data = {
        "name": name
    }

    # 添加可选参数
    if module.params['enable'] is not None:
        connmulti_data['enable'] = module.params['enable']
    if module.params['multi_num'] is not None:
        connmulti_data['multi_num'] = module.params['multi_num']
    if module.params['timeout'] is not None:
        connmulti_data['timeout'] = module.params['timeout']
    if module.params['desc_connmulti'] is not None:
        connmulti_data['desc_connmulti'] = module.params['desc_connmulti']

    post_data = json.dumps(connmulti_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "连接复用模板添加", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="连接复用模板添加失败: %s" % str(e))


def adc_connmulti_edit(module):
    """连接复用模板编辑"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="连接复用模板编辑需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.connmulti.edit" % (
        ip, authkey)

    connmulti_data = {
        "name": name
    }

    # 添加可选参数
    if module.params['enable'] is not None:
        connmulti_data['enable'] = module.params['enable']
    if module.params['multi_num'] is not None:
        connmulti_data['multi_num'] = module.params['multi_num']
    if module.params['timeout'] is not None:
        connmulti_data['timeout'] = module.params['timeout']
    if module.params['desc_connmulti'] is not None:
        connmulti_data['desc_connmulti'] = module.params['desc_connmulti']

    post_data = json.dumps(connmulti_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "连接复用模板编辑", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="连接复用模板编辑失败: %s" % str(e))


def adc_connmulti_del(module):
    """连接复用模板删除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="连接复用模板删除需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.connmulti.del" % (
        ip, authkey)

    connmulti_data = {
        "name": name
    }

    post_data = json.dumps(connmulti_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "连接复用模板删除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="连接复用模板删除失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'connmulti_list', 'connmulti_list_withcommon', 'connmulti_get',
            'connmulti_add', 'connmulti_edit', 'connmulti_del'
        ]),
        # 连接复用模板参数
        name=dict(type='str', required=False),
        enable=dict(type='int', required=False, choices=[0, 1]),
        multi_num=dict(type='int', required=False),
        timeout=dict(type='int', required=False),
        desc_connmulti=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'connmulti_list':
        adc_connmulti_list(module)
    elif action == 'connmulti_list_withcommon':
        adc_connmulti_list_withcommon(module)
    elif action == 'connmulti_get':
        adc_connmulti_get(module)
    elif action == 'connmulti_add':
        adc_connmulti_add(module)
    elif action == 'connmulti_edit':
        adc_connmulti_edit(module)
    elif action == 'connmulti_del':
        adc_connmulti_del(module)


if __name__ == '__main__':
    main()
