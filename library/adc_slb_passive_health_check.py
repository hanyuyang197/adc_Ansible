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


def adc_passive_health_check_add(module):
    """被动健康检查添加"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="被动健康检查添加需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.passive-health-check.add" % (
        ip, authkey)

    health_check_data = {
        "name": name
    }

    # 添加可选参数
    if module.params['type'] is not None:
        health_check_data['type'] = module.params['type']
    if module.params['enable'] is not None:
        health_check_data['enable'] = module.params['enable']
    if module.params['phc_action'] is not None:
        health_check_data['action'] = module.params['phc_action']
    if module.params['timeout'] is not None:
        health_check_data['timeout'] = module.params['timeout']
    if module.params['interval'] is not None:
        health_check_data['interval'] = module.params['interval']
    if module.params['rise'] is not None:
        health_check_data['rise'] = module.params['rise']
    if module.params['fall'] is not None:
        health_check_data['fall'] = module.params['fall']
    if module.params['desc_phc'] is not None:
        health_check_data['desc_phc'] = module.params['desc_phc']

    post_data = json.dumps(health_check_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "被动健康检查添加", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="被动健康检查添加失败: %s" % str(e))


def adc_passive_health_check_list(module):
    """被动健康检查列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.passive-health-check.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, passive_health_checks=response_data)
    except Exception as e:
        module.fail_json(msg="被动健康检查列表获取失败: %s" % str(e))


def adc_passive_health_check_get(module):
    """被动健康检查获取"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="被动健康检查获取需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.passive-health-check.get" % (
        ip, authkey)

    health_check_data = {
        "name": name
    }

    post_data = json.dumps(health_check_data)

    try:
        response_data = send_request(url, post_data)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, passive_health_check=response_data)
    except Exception as e:
        module.fail_json(msg="被动健康检查获取失败: %s" % str(e))


def adc_passive_health_check_edit(module):
    """被动健康检查编辑"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="被动健康检查编辑需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.passive-health-check.edit" % (
        ip, authkey)

    health_check_data = {
        "name": name
    }

    # 添加可选参数
    if module.params['type'] is not None:
        health_check_data['type'] = module.params['type']
    if module.params['enable'] is not None:
        health_check_data['enable'] = module.params['enable']
    if module.params['phc_action'] is not None:
        health_check_data['action'] = module.params['phc_action']
    if module.params['timeout'] is not None:
        health_check_data['timeout'] = module.params['timeout']
    if module.params['interval'] is not None:
        health_check_data['interval'] = module.params['interval']
    if module.params['rise'] is not None:
        health_check_data['rise'] = module.params['rise']
    if module.params['fall'] is not None:
        health_check_data['fall'] = module.params['fall']
    if module.params['desc_phc'] is not None:
        health_check_data['desc_phc'] = module.params['desc_phc']

    post_data = json.dumps(health_check_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "被动健康检查编辑", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="被动健康检查编辑失败: %s" % str(e))


def adc_passive_health_check_del(module):
    """被动健康检查删除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="被动健康检查删除需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.passive-health-check.del" % (
        ip, authkey)

    health_check_data = {
        "name": name
    }

    post_data = json.dumps(health_check_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "被动健康检查删除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="被动健康检查删除失败: %s" % str(e))


def adc_passive_health_check_list_withcommon(module):
    """被动健康检查获取 common 和本分区"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.passive-health-check.list.withcommon" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(
            changed=False, passive_health_checks_withcommon=response_data)
    except Exception as e:
        module.fail_json(msg="被动健康检查获取 common 和本分区失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'passive_health_check_add', 'passive_health_check_list', 'passive_health_check_get',
            'passive_health_check_edit', 'passive_health_check_del', 'passive_health_check_list_withcommon'
        ]),
        # 被动健康检查参数
        name=dict(type='str', required=False),
        type=dict(type='str', required=False),
        enable=dict(type='int', required=False, choices=[0, 1]),
        phc_action=dict(type='str', required=False),
        timeout=dict(type='int', required=False),
        interval=dict(type='int', required=False),
        rise=dict(type='int', required=False),
        fall=dict(type='int', required=False),
        desc_phc=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'passive_health_check_add':
        adc_passive_health_check_add(module)
    elif action == 'passive_health_check_list':
        adc_passive_health_check_list(module)
    elif action == 'passive_health_check_get':
        adc_passive_health_check_get(module)
    elif action == 'passive_health_check_edit':
        adc_passive_health_check_edit(module)
    elif action == 'passive_health_check_del':
        adc_passive_health_check_del(module)
    elif action == 'passive_health_check_list_withcommon':
        adc_passive_health_check_list_withcommon(module)


if __name__ == '__main__':
    main()
