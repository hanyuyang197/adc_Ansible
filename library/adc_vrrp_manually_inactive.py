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


def vrrp_manually_inactive_set(module):
    """设置vrrp主动降备"""
    device_ip = module.params['ip']
    authkey = module.params['authkey']
    group_id = module.params.get('group_id')
    unit_id = module.params.get('unit_id')
    all_partitions = module.params.get('all_partitions')

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.manually_inactive.set" % (device_ip, authkey)

    # 构造请求数据
    request_data = {}

    # 必选参数：unit_id
    if unit_id is not None:
        request_data["unit_id"] = unit_id
    else:
        module.fail_json(msg="unit_id 参数是必需的")

    # 可选参数：group_id（缺失值:-1 表示所有组）
    if group_id is not None:
        request_data["group_id"] = group_id

    # 可选参数：all_partitions（缺省值:0，当 group_id 存在时，此值无效）
    if all_partitions is not None and group_id is None:
        request_data["all_partitions"] = all_partitions

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="设置vrrp主动降备失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置vrrp主动降备", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=['vrrp_manually_inactive_set']),
        group_id=dict(type='int', required=False),  # 可选，0-8 组序号，缺失值:-1 表示所有组
        unit_id=dict(type='int', required=True),  # 必选，1-8 设备 ID
        all_partitions=dict(type='int', required=False, choices=[0, 1])  # 可选，1 表示应用到所有分区，0 表示不应用到所有分区，缺省值:0
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 执行操作
    vrrp_manually_inactive_set(module)


if __name__ == '__main__':
    main()
