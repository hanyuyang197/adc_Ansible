#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
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


def adc_erule_upload(module):
    """erule上传"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="erule上传需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.erule.upload&name=%s" % (
        ip, authkey, name)

    try:
        response_data = send_request(url)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "erule上传", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="erule上传失败: %s" % str(e))


def adc_erule_content_add(module):
    """erule在线编辑"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    content = module.params['content']

    if not name or not content:
        module.fail_json(msg="erule在线编辑需要提供name和content参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.erule.content.add" % (
        ip, authkey)

    erule_data = {
        "name": name,
        "content": content
    }

    post_data = json.dumps(erule_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "erule在线编辑", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="erule在线编辑失败: %s" % str(e))


def adc_erule_del(module):
    """erule文件删除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="erule文件删除需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.erule.del" % (
        ip, authkey)

    erule_data = {
        "name": name
    }

    post_data = json.dumps(erule_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "erule文件删除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="erule文件删除失败: %s" % str(e))


def adc_erule_list(module):
    """erule文件列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.erule.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, erule_list=response_data)
    except Exception as e:
        module.fail_json(msg="erule文件列表获取失败: %s" % str(e))


def adc_erulefiles_upload(module):
    """erule服务器文件上传"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="erule服务器文件上传需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.erulefiles.upload" % (
        ip, authkey)

    erule_data = {
        "name": name
    }

    post_data = json.dumps(erule_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "erule服务器文件上传", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="erule服务器文件上传失败: %s" % str(e))


def adc_erulefiles_del(module):
    """erule服务器文件删除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="erule服务器文件删除需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.erulefiles.del" % (
        ip, authkey)

    erule_data = {
        "name": name
    }

    post_data = json.dumps(erule_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "erule服务器文件删除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="erule服务器文件删除失败: %s" % str(e))


def adc_erulefiles_list(module):
    """erule服务器文件列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.erulefiles.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, erulefiles_list=response_data)
    except Exception as e:
        module.fail_json(msg="erule服务器文件列表获取失败: %s" % str(e))


def adc_erule_list_withcommon(module):
    """erule文件获取 common 和本分区"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.erule.list.withcommon" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 直接返回响应数据，不解析为特定格式
        module.exit_json(changed=False, erule_list_withcommon=response_data)
    except Exception as e:
        module.fail_json(msg="erule文件获取 common 和本分区失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'erule_upload', 'erule_content_add', 'erule_del',
            'erule_list', 'erulefiles_upload', 'erulefiles_del',
            'erulefiles_list', 'erule_list_withcommon'
        ]),
        # erule参数
        name=dict(type='str', required=False),
        content=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'erule_upload':
        adc_erule_upload(module)
    elif action == 'erule_content_add':
        adc_erule_content_add(module)
    elif action == 'erule_del':
        adc_erule_del(module)
    elif action == 'erule_list':
        adc_erule_list(module)
    elif action == 'erulefiles_upload':
        adc_erulefiles_upload(module)
    elif action == 'erulefiles_del':
        adc_erulefiles_del(module)
    elif action == 'erulefiles_list':
        adc_erulefiles_list(module)
    elif action == 'erule_list_withcommon':
        adc_erule_list_withcommon(module)


if __name__ == '__main__':
    main()
