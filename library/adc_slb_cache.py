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
    format_adc_response_for_ansible,
    send_request
)
import json
import sys


def slb_cache_list(module):
    """缓存模板列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.cache.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, cache_list=response_data)
    except Exception as e:
        module.fail_json(msg="缓存模板列表获取失败: %s" % str(e))


def slb_cache_list_withcommon(module):
    """获取 common 和本分区缓存文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.cache.list.withcommon" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, cache_list_withcommon=response_data)
    except Exception as e:
        module.fail_json(msg="获取 common 和本分区缓存文件失败: %s" % str(e))


def slb_cache_get(module):
    """缓存模板获取"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="缓存模板获取需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.cache.get" % (
        ip, authkey)

    cache_data = {
        "name": name
    }

    post_data = json.dumps(cache_data)

    try:
        response_data = send_request(url, post_data)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(chchanged=False, cache_data=response_data)
    except Exception as e:
        module.fail_json(msg="缓存模板获取失败: %s" % str(e))


def slb_cache_add(module):
    """缓存模板添加"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="缓存模板添加需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.cache.add" % (
        ip, authkey)

    cache_data = {
        "name": name
    }

    # 添加可选参数（与API文档保持一致）
    optional_params = [
        'age', 'size_max', 'object_min', 'object_max', 
        'handle_reload_req', 'cache_host', 'no_cache', 
        'no_age_header', 'no_via_header', 'cache_policy', 'description'
    ]
    
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            cache_data[param] = module.params[param]

    post_data = json.dumps(cache_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "缓存模板添加", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="缓存模板添加失败: %s" % str(e))


def slb_cache_edit(module):
    """缓存模板编辑"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="缓存模板编辑需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.cache.edit" % (
        ip, authkey)

    cache_data = {
        "name": name
    }

    # 添加可选参数（与API文档保持一致）
    optional_params = [
        'age', 'size_max', 'object_min', 'object_max', 
        'handle_reload_req', 'cache_host', 'no_cache', 
        'no_age_header', 'no_via_header', 'cache_policy', 'description'
    ]
    
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            cache_data[param] = module.params[param]

    post_data = json.dumps(cache_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "缓存模板编辑", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="缓存模板编辑失败: %s" % str(e))


def slb_cache_del(module):
    """缓存模板删除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="缓存模板删除需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.cache.del" % (
        ip, authkey)

    cache_data = {
        "name": name
    }

    post_data = json.dumps(cache_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "缓存模板删除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="缓存模板删除失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'slb_cache_list', 'slb_cache_list_withcommon', 'slb_cache_get',
            'slb_cache_add', 'slb_cache_edit', 'slb_cache_del'
        ]),
        # 缓存模板参数（与API文档保持一致）
        name=dict(type='str', required=False),
        description=dict(type='str', required=False),
        age=dict(type='int', required=False),
        size_max=dict(type='int', required=False),
        object_min=dict(type='int', required=False),
        object_max=dict(type='int', required=False),
        handle_reload_req=dict(type='int', required=False),
        cache_host=dict(type='int', required=False),
        no_cache=dict(type='int', required=False),
        no_age_header=dict(type='int', required=False),
        no_via_header=dict(type='int', required=False),
        cache_policy=dict(type='list', required=False, elements='dict')
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'slb_cache_list':
        slb_cache_list(module)
    elif action == 'slb_cache_list_withcommon':
        slb_cache_list_withcommon(module)
    elif action == 'slb_cache_get':
        slb_cache_get(module)
    elif action == 'slb_cache_add':
        slb_cache_add(module)
    elif action == 'slb_cache_edit':
        slb_cache_edit(module)
    elif action == 'slb_cache_del':
        slb_cache_del(module)


if __name__ == '__main__':
    main()
