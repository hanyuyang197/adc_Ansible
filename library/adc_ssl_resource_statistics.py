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


def ssl_resource_statistics_list(module):
    """获取SSL资源统计列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    action = module.params['action']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=ssl.resource_statistics.list" % (
        ip, authkey)
    if action == "ssl_resource_statistics_list_all_partition":
        url += ".all_partition"

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
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
        module.fail_json(msg="获取SSL资源统计列表失败: %s" % str(e))

    # 对于获取统计列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            success, result_dict = format_adc_response_for_ansible(
                response_data, "获取SSL资源统计列表", False)
            if success:
                module.exit_json(**result_dict)
            else:
                module.fail_json(**result_dict)
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
            'ssl_resource_statistics_list', 'ssl_resource_statistics_list_all_partition'])
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'ssl_resource_statistics_list':
        ssl_resource_statistics_list(module)
    elif action == 'ssl_resource_statistics_list_all_partition':
        ssl_resource_statistics_list(module)

if __name__ == '__main__':
    main()
