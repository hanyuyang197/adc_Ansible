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


def log_alarm_email_get(module):
    """Get email alarm configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.alarm.email.get" % (
        ip, authkey)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            req = urllib_request.Request(url)
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取邮件告警配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取邮件告警配置", False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def log_alarm_email_set(module):
    """Set email alarm configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.alarm.email.set" % (
        ip, authkey)

    # Prepare parameters
    params = {}

    # Add optional parameters if provided
    if module.params['delay_send_buff'] is not None:
        params['delay_send_buff'] = module.params['delay_send_buff']
    if module.params['delay_send_time'] is not None:
        params['delay_send_time'] = module.params['delay_send_time']
    if module.params['send_event'] is not None:
        params['send_event'] = module.params['send_event']
    if module.params['send_level'] is not None:
        params['send_level'] = module.params['send_level']

    # 转换为JSON格式
    post_data = json.dumps(params)

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
        module.fail_json(msg="设置邮件告警配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置邮件告警配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def log_alarm_sms_get(module):
    """Get SMS alarm configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.alarm.sms.get" % (
        ip, authkey)

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            req = urllib_request.Request(url)
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取短信告警配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取短信告警配置", False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def log_alarm_sms_set(module):
    """Set SMS alarm configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=log.alarm.sms.set" % (
        ip, authkey)

    # Prepare parameters
    params = {}

    # Add optional parameters if provided
    if module.params['url'] is not None:
        params['url'] = module.params['url']
    if module.params['send_event'] is not None:
        params['send_event'] = module.params['send_event']
    if module.params['send_level'] is not None:
        params['send_level'] = module.params['send_level']

    # 转换为JSON格式
    post_data = json.dumps(params)

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
        module.fail_json(msg="设置短信告警配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置短信告警配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    # Define module arguments
    argument_spec = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
                    'log_alarm_email_get', 'log_alarm_email_set',
                    'log_alarm_sms_get', 'log_alarm_sms_set']),
        # Parameters for email alarm configuration
        delay_send_buff=dict(type='int'),
        delay_send_time=dict(type='int'),
        send_event=dict(type='list', elements='int'),
        send_level=dict(type='int', choices=[-1, 0, 1, 2, 5]),
        # Parameters for SMS alarm configuration
        url=dict(type='str'),
    )

    # Create Ansible module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    # Extract module parameters
    action = str(module.params['action'])

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(changed=False)

    # Perform requested action
    if action == 'log_alarm_email_get':
        log_alarm_email_get(module)
    elif action == 'log_alarm_email_set':
        log_alarm_email_set(module)
    elif action == 'log_alarm_sms_get':
        log_alarm_sms_get(module)
    elif action == 'log_alarm_sms_set':
        log_alarm_sms_set(module)


if __name__ == '__main__':
    main()
