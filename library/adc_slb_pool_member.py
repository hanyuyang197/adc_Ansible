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


def adc_pool_member_add(module):
    """服务池成员添加"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    pool_name = module.params['pool_name']
    node_name = module.params['node_name']
    port = module.params['port']

    if not pool_name or not node_name or not port:
        module.fail_json(msg="服务池成员添加需要提供pool_name, node_name和port参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.member.add" % (
        ip, authkey)

    member_data = {
        "pool_name": pool_name,
        "node_name": node_name,
        "port": port
    }

    # 添加可选参数
    if module.params['weight'] is not None:
        member_data['weight'] = module.params['weight']
    if module.params['status'] is not None:
        member_data['status'] = module.params['status']
    if module.params['conn_limit'] is not None:
        member_data['conn_limit'] = module.params['conn_limit']
    if module.params['healthcheck'] is not None:
        member_data['healthcheck'] = module.params['healthcheck']
    if module.params['desc_member'] is not None:
        member_data['desc_member'] = module.params['desc_member']
    if module.params['graceful_time'] is not None:
        member_data['graceful_time'] = module.params['graceful_time']
    if module.params['graceful_delete'] is not None:
        member_data['graceful_delete'] = module.params['graceful_delete']
    if module.params['graceful_disable'] is not None:
        member_data['graceful_disable'] = module.params['graceful_disable']
    if module.params['graceful_persist'] is not None:
        member_data['graceful_persist'] = module.params['graceful_persist']
    if module.params['phm_profile'] is not None:
        member_data['phm_profile'] = module.params['phm_profile']
    if module.params['upnum'] is not None:
        member_data['upnum'] = module.params['upnum']
    if module.params['nat_strategy'] is not None:
        member_data['nat_strategy'] = module.params['nat_strategy']

    post_data = json.dumps(member_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "服务池成员添加", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="服务池成员添加失败: %s" % str(e))


def adc_pool_member_edit(module):
    """服务池成员编辑"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    pool_name = module.params['pool_name']
    node_name = module.params['node_name']
    port = module.params['port']

    if not pool_name or not node_name or not port:
        module.fail_json(msg="服务池成员编辑需要提供pool_name, node_name和port参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.member.edit" % (
        ip, authkey)

    member_data = {
        "pool_name": pool_name,
        "node_name": node_name,
        "port": port
    }

    # 添加可选参数
    if module.params['weight'] is not None:
        member_data['weight'] = module.params['weight']
    if module.params['status'] is not None:
        member_data['status'] = module.params['status']
    if module.params['conn_limit'] is not None:
        member_data['conn_limit'] = module.params['conn_limit']
    if module.params['healthcheck'] is not None:
        member_data['healthcheck'] = module.params['healthcheck']
    if module.params['desc_member'] is not None:
        member_data['desc_member'] = module.params['desc_member']
    if module.params['graceful_time'] is not None:
        member_data['graceful_time'] = module.params['graceful_time']
    if module.params['graceful_delete'] is not None:
        member_data['graceful_delete'] = module.params['graceful_delete']
    if module.params['graceful_disable'] is not None:
        member_data['graceful_disable'] = module.params['graceful_disable']
    if module.params['graceful_persist'] is not None:
        member_data['graceful_persist'] = module.params['graceful_persist']
    if module.params['phm_profile'] is not None:
        member_data['phm_profile'] = module.params['phm_profile']
    if module.params['upnum'] is not None:
        member_data['upnum'] = module.params['upnum']
    if module.params['nat_strategy'] is not None:
        member_data['nat_strategy'] = module.params['nat_strategy']

    post_data = json.dumps(member_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "服务池成员编辑", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="服务池成员编辑失败: %s" % str(e))


def adc_pool_member_del(module):
    """服务池成员删除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    pool_name = module.params['pool_name']
    node_name = module.params['node_name']
    port = module.params['port']

    if not pool_name or not node_name or not port:
        module.fail_json(msg="服务池成员删除需要提供pool_name, node_name和port参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.member.del" % (
        ip, authkey)

    member_data = {
        "pool_name": pool_name,
        "node_name": node_name,
        "port": port
    }

    post_data = json.dumps(member_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "服务池成员删除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="服务池成员删除失败: %s" % str(e))


def adc_pool_stat_list(module):
    """服务池状态列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.stat.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, pool_stats=response_data)
    except Exception as e:
        module.fail_json(msg="服务池状态列表获取失败: %s" % str(e))


def adc_pool_stat_get(module):
    """服务池状态获取"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    pool_name = module.params['pool_name']

    if not pool_name:
        module.fail_json(msg="服务池状态获取需要提供pool_name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.stat.get" % (
        ip, authkey)

    pool_data = {
        "pool_name": pool_name
    }

    post_data = json.dumps(pool_data)

    try:
        response_data = send_request(url, post_data)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, pool_stat=response_data)
    except Exception as e:
        module.fail_json(msg="服务池状态获取失败: %s" % str(e))


def adc_pool_stat_clear(module):
    """服务池状态清除"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.stat.clear" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "服务池状态清除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="服务池状态清除失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'pool_member_add', 'pool_member_edit', 'pool_member_del',
            'pool_stat_list', 'pool_stat_get', 'pool_stat_clear'
        ]),
        # 服务池成员参数
        pool_name=dict(type='str', required=False),
        node_name=dict(type='str', required=False),
        port=dict(type='int', required=False),
        weight=dict(type='int', required=False),
        status=dict(type='int', required=False, choices=[0, 1]),
        conn_limit=dict(type='int', required=False),
        healthcheck=dict(type='str', required=False),
        desc_member=dict(type='str', required=False),
        graceful_time=dict(type='int', required=False),
        graceful_delete=dict(type='int', required=False, choices=[0, 1]),
        graceful_disable=dict(type='int', required=False, choices=[0, 1]),
        graceful_persist=dict(type='int', required=False, choices=[0, 1]),
        phm_profile=dict(type='str', required=False),
        upnum=dict(type='int', required=False),
        nat_strategy=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'pool_member_add':
        adc_pool_member_add(module)
    elif action == 'pool_member_edit':
        adc_pool_member_edit(module)
    elif action == 'pool_member_del':
        adc_pool_member_del(module)
    elif action == 'pool_stat_list':
        adc_pool_stat_list(module)
    elif action == 'pool_stat_get':
        adc_pool_stat_get(module)
    elif action == 'pool_stat_clear':
        adc_pool_stat_clear(module)


if __name__ == '__main__':
    main()
