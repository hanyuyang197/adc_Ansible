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


def slb_profile_fastl5_del(module):
    """删除FastL5 Profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    if not name:
        module.fail_json(msg="删除FastL5 Profile需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.fastl5.del" % (ip, authkey)

    profile_data = {
        "name": name
    }

    post_data = json.dumps(profile_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="删除FastL5 Profile失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除FastL5 Profile", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_fastl6_edit(module):
    """编辑FastL6 Profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    if not name:
        module.fail_json(msg="编辑FastL6 Profile需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.fastl6.edit" % (ip, authkey)

    profile_data = {
        "name": name
    }

    # 添加可选参数
    if 'description' in module.params and module.params['description']:
        profile_data['description'] = module.params['description']
    if 'protocol' in module.params and module.params['protocol'] is not None:
        profile_data['protocol'] = module.params['protocol']
    if 'timeout' in module.params and module.params['timeout'] is not None:
        profile_data['timeout'] = module.params['timeout']
    if 'enable' in module.params and module.params['enable'] is not None:
        profile_data['enable'] = module.params['enable']

    post_data = json.dumps(profile_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="编辑FastL6 Profile失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑FastL6 Profile", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_fastl7_get(module):
    """获取FastL7 Profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    if not name:
        module.fail_json(msg="获取FastL7 Profile需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.fastl7.get" % (ip, authkey)

    profile_data = {
        "name": name
    }

    post_data = json.dumps(profile_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="获取FastL7 Profile失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取FastL7 Profile失败", response=parsed_data)
            else:
                module.exit_json(changed=False, profile=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_http_hostswitch_del(module):
    """删除HTTP HostSwitch Profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    if not name:
        module.fail_json(msg="删除HTTP HostSwitch Profile需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.http.hostswitch.del" % (ip, authkey)

    profile_data = {
        "name": name
    }

    post_data = json.dumps(profile_data)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="删除HTTP HostSwitch Profile失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除HTTP HostSwitch Profile", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_dns_list_withcommon(module):
    """获取DNS Profile列表（包含common分区）"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dns.list.withcomon" % (ip, authkey)

    response_data = ""
    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="获取DNS Profile列表（包含common分区）失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取DNS Profile列表（包含common分区）失败", response=parsed_data)
            else:
                module.exit_json(changed=False, profiles=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_smtp_list_withcommon(module):
    """获取SMTP Profile列表（包含common分区）"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.smtp.list.withcomon" % (ip, authkey)

    response_data = ""
    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="获取SMTP Profile列表（包含common分区）失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SMTP Profile列表（包含common分区）失败", response=parsed_data)
            else:
                module.exit_json(changed=False, profiles=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_profile_rtsp_list_withcommon(module):
    """获取RTSP Profile列表（包含common分区）"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.rtsp.list.withcomon" % (ip, authkey)

    response_data = ""
    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="获取RTSP Profile列表（包含common分区）失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取RTSP Profile列表（包含common分区）失败", response=parsed_data)
            else:
                module.exit_json(changed=False, profiles=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'slb_profile_fastl5_del', 'slb_profile_fastl6_edit', 'slb_profile_fastl7_get',
            'slb_profile_http_hostswitch_del', 'slb_profile_dns_list_withcommon',
            'slb_profile_smtp_list_withcommon', 'slb_profile_rtsp_list_withcommon'
        ]),
        # Profile通用参数
        name=dict(type='str', required=False),
        description=dict(type='str', required=False),
        protocol=dict(type='int', required=False),
        timeout=dict(type='int', required=False),
        enable=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']
    if hasattr(action, '__str__'):
        action = str(action)

    if action == 'slb_profile_fastl5_del':
        slb_profile_fastl5_del(module)
    elif action == 'slb_profile_fastl6_edit':
        slb_profile_fastl6_edit(module)
    elif action == 'slb_profile_fastl7_get':
        slb_profile_fastl7_get(module)
    elif action == 'slb_profile_http_hostswitch_del':
        slb_profile_http_hostswitch_del(module)
    elif action == 'slb_profile_dns_list_withcommon':
        slb_profile_dns_list_withcommon(module)
    elif action == 'slb_profile_smtp_list_withcommon':
        slb_profile_smtp_list_withcommon(module)
    elif action == 'slb_profile_rtsp_list_withcommon':
        slb_profile_rtsp_list_withcommon(module)


if __name__ == '__main__':
    main()