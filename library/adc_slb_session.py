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


def adc_clear_session(module):
    """清除会话"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=clear_session" % (ip, authkey)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='POST')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'POST'
            response = urllib_request.urlopen(req)
            response_data = response.read()

        # 解析响应
        result = json.loads(response_data)
        
        # 检查响应状态
        if result.get('status') == 'success':
            module.exit_json(changed=True, msg="会话清除成功", result=result)
        else:
            module.fail_json(msg="会话清除失败: " + result.get('message', '未知错误'))

    except Exception as e:
        module.fail_json(msg="清除会话请求失败: " + str(e))


def main():
    """主函数"""
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True)
    )

    # 创建模块
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # 根据action参数调用相应的函数
    action = module.params.get('action')
    
    if action == 'clear_session':
        adc_clear_session(module)
    else:
        module.fail_json(msg="不支持的action: " + str(action))


if __name__ == '__main__':
    main()