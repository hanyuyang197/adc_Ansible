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


def slb_healthtest_list(module):
    """获取健康检查列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthtest.list" % (ip, authkey)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()

        # 对于获取列表操作，直接返回响应数据，不判断success
        if response_data:
            try:
                parsed_data = json.loads(response_data)
                # 检查是否有错误信息
                if 'errmsg' in parsed_data and parsed_data['errmsg']:
                    module.fail_json(msg="获取健康检查列表失败", response=parsed_data)
                else:
                    module.exit_json(changed=False, healthtests=parsed_data)
            except Exception as e:
                module.fail_json(msg="解析响应失败: %s" % str(e))
        else:
            module.fail_json(msg="未收到有效响应")

    except Exception as e:
        module.fail_json(msg="获取健康检查列表失败: %s" % str(e))


def slb_healthtest_add(module):
    """添加健康检查"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthtest.add" % (ip, authkey)

    # 构造请求数据 - 只包含非None的参数
    healthtest_data = {}
    optional_params = ['name', 'type', 'interval', 'timeout', 'retry', 'port', 'send', 'receive']

    for param in optional_params:
        if module.params.get(param) is not None:
            healthtest_data[param] = module.params[param]

    # 转换为JSON格式
    post_data = json.dumps(healthtest_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, data=post_data.encode('utf-8'), method='POST')
            req.add_header('Content-Type', 'application/json')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data)
            req.add_header('Content-Type', 'application/json')
            req.get_method = lambda: 'POST'
            response = urllib_request.urlopen(req)
            response_data = response.read()

        # 解析响应
        result = json.loads(response_data)

        # 检查响应状态
        if result.get('status') == 'success':
            module.exit_json(changed=True, msg="健康检查添加成功", result=result)
        else:
            module.fail_json(msg="健康检查添加失败: " + result.get('message', '未知错误'))

    except Exception as e:
        module.fail_json(msg="添加健康检查请求失败: %s" % str(e))


def slb_healthtest_get(module):
    """获取健康检查详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthtest.get" % (ip, authkey)

    # 构造请求数据 - 只包含非None的参数
    healthtest_data = {}
    optional_params = ['name']

    for param in optional_params:
        if module.params.get(param) is not None:
            healthtest_data[param] = module.params[param]

    # 转换为JSON格式
    post_data = json.dumps(healthtest_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, data=post_data.encode('utf-8'), method='POST')
            req.add_header('Content-Type', 'application/json')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data)
            req.add_header('Content-Type', 'application/json')
            req.get_method = lambda: 'POST'
            response = urllib_request.urlopen(req)
            response_data = response.read()

        # 解析响应
        result = json.loads(response_data)

        # 检查响应状态
        if result.get('status') == 'success' or 'name' in result:
            module.exit_json(changed=False, healthtest=result)
        else:
            module.fail_json(msg="获取健康检查详情失败: " + result.get('message', '未知错误'))

    except Exception as e:
        module.fail_json(msg="获取健康检查详情请求失败: %s" % str(e))


def slb_healthtest_del(module):
    """删除健康检查"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthtest.del" % (ip, authkey)

    # 构造请求数据 - 只包含非None的参数
    healthtest_data = {}
    optional_params = ['name']

    for param in optional_params:
        if module.params.get(param) is not None:
            healthtest_data[param] = module.params[param]

    # 转换为JSON格式
    post_data = json.dumps(healthtest_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, data=post_data.encode('utf-8'), method='POST')
            req.add_header('Content-Type', 'application/json')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data)
            req.add_header('Content-Type', 'application/json')
            req.get_method = lambda: 'POST'
            response = urllib_request.urlopen(req)
            response_data = response.read()

        # 解析响应
        result = json.loads(response_data)

        # 检查响应状态
        if result.get('status') == 'success':
            module.exit_json(changed=True, msg="健康检查删除成功", result=result)
        else:
            module.fail_json(msg="健康检查删除失败: " + result.get('message', '未知错误'))

    except Exception as e:
        module.fail_json(msg="删除健康检查请求失败: %s" % str(e))


def main():
    """主函数"""
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True),
        name=dict(type='str', required=False),
        type=dict(type='str', required=False),
        interval=dict(type='int', required=False),
        timeout=dict(type='int', required=False),
        retry=dict(type='int', required=False),
        port=dict(type='int', required=False),
        send=dict(type='str', required=False),
        receive=dict(type='str', required=False)
    )

    # 创建模块
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # 根据action参数调用相应的函数
    action = module.params.get('action')

    if action == 'slb_healthtest_list':
        slb_healthtest_list(module)
    elif action == 'slb_healthtest_add':
        slb_healthtest_add(module)
    elif action == 'slb_healthtest_get':
        slb_healthtest_get(module)
    elif action == 'slb_healthtest_del':
        slb_healthtest_del(module)


if __name__ == '__main__':
    main()