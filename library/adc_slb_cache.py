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


def format_adc_response_for_ansible(response_data, action="", changed_default=True):
    """
    格式化ADC响应为Ansible模块返回格式
    """
    result = {
        'success': False,
        'result': '',
        'errcode': '',
        'errmsg': '',
        'data': {}
    }

    try:
        if isinstance(response_data, str):
            parsed_data = json.loads(response_data)
        else:
            parsed_data = response_data

        result['data'] = parsed_data
        result['result'] = parsed_data.get('result', '')
        result['errcode'] = parsed_data.get('errcode', '')
        result['errmsg'] = parsed_data.get('errmsg', '')

        if result['result'].lower() == 'success':
            result['success'] = True
        else:
            errmsg = result['errmsg'].lower() if isinstance(
                result['errmsg'], str) else str(result['errmsg']).lower()
            if any(keyword in errmsg for keyword in ['已存在', 'already exists', 'already exist', 'exists']):
                result['success'] = True
                result['result'] = 'success (already exists)'

    except json.JSONDecodeError as e:
        # 直接返回原始响应内容，不尝试解析为JSON
        result['errmsg'] = response_data
        result['errcode'] = 'RAW_RESPONSE'
    except Exception as e:
        result['errmsg'] = "响应解析异常: %s" % str(e)
        result['errcode'] = 'PARSE_EXCEPTION'

    if result['success']:
        result_dict = {
            'changed': changed_default,
            'msg': '%s操作成功' % action if action else '操作成功',
            'response': result['data']
        }

        if 'already exists' in result['result']:
            result_dict['changed'] = False
            result_dict['msg'] = '%s操作成功（资源已存在，无需更改）' % action if action else '操作成功（资源已存在，无需更改）'

        return True, result_dict
    else:
        result_dict = {
            'changed': False,
            'msg': '%s操作失败' % action if action else '操作失败',
            'error': {
                'result': result['result'],
                'errcode': result['errcode'],
                'errmsg': result['errmsg']
            },
            'response': result['data']
        }
        return False, result_dict


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


def adc_cache_list(module):
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


def adc_cache_list_withcommon(module):
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


def adc_cache_get(module):
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


def adc_cache_add(module):
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

    # 添加可选参数
    if module.params['enable'] is not None:
        cache_data['enable'] = module.params['enable']
    if module.params['cache_size'] is not None:
        cache_data['cache_size'] = module.params['cache_size']
    if module.params['cache_time'] is not None:
        cache_data['cache_time'] = module.params['cache_time']
    if module.params['cache_type'] is not None:
        cache_data['cache_type'] = module.params['cache_type']
    if module.params['desc_cache'] is not None:
        cache_data['desc_cache'] = module.params['desc_cache']

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


def adc_cache_edit(module):
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

    # 添加可选参数
    if module.params['enable'] is not None:
        cache_data['enable'] = module.params['enable']
    if module.params['cache_size'] is not None:
        cache_data['cache_size'] = module.params['cache_size']
    if module.params['cache_time'] is not None:
        cache_data['cache_time'] = module.params['cache_time']
    if module.params['cache_type'] is not None:
        cache_data['cache_type'] = module.params['cache_type']
    if module.params['desc_cache'] is not None:
        cache_data['desc_cache'] = module.params['desc_cache']

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


def adc_cache_del(module):
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
            'cache_list', 'cache_list_withcommon', 'cache_get',
            'cache_add', 'cache_edit', 'cache_del'
        ]),
        # 缓存模板参数
        name=dict(type='str', required=False),
        enable=dict(type='int', required=False, choices=[0, 1]),
        cache_size=dict(type='int', required=False),
        cache_time=dict(type='int', required=False),
        cache_type=dict(type='str', required=False),
        desc_cache=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'cache_list':
        adc_cache_list(module)
    elif action == 'cache_list_withcommon':
        adc_cache_list_withcommon(module)
    elif action == 'cache_get':
        adc_cache_get(module)
    elif action == 'cache_add':
        adc_cache_add(module)
    elif action == 'cache_edit':
        adc_cache_edit(module)
    elif action == 'cache_del':
        adc_cache_del(module)


if __name__ == '__main__':
    main()
