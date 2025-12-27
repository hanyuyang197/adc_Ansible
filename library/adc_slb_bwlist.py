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


def adc_bwlist_upload(module):
    """上传黑白名单文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="上传黑白名单文件需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.bwlist.upload&name=%s" % (
        ip, authkey, name)

    try:
        response_data = send_request(url)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "上传黑白名单文件", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="上传黑白名单文件失败: %s" % str(e))


def adc_bwlist_del(module):
    """删除黑白名单文件"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="删除黑白名单文件需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.bwlist.del" % (
        ip, authkey)

    bwlist_data = {
        "name": name
    }

    post_data = json.dumps(bwlist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除黑白名单文件", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="删除黑白名单文件失败: %s" % str(e))


def adc_bwlist_list(module):
    """获取黑白名单文件列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.bwlist.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, bwlist_list=response_data)
    except Exception as e:
        module.fail_json(msg="获取黑白名单文件列表失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'bwlist_upload', 'bwlist_del', 'bwlist_list'
        ]),
        # 黑白名单参数
        name=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'bwlist_upload':
        adc_bwlist_upload(module)
    elif action == 'bwlist_del':
        adc_bwlist_del(module)
    elif action == 'bwlist_list':
        adc_bwlist_list(module)


if __name__ == '__main__':
    main()
