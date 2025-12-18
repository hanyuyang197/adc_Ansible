#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import json
# Python 2/3兼容性处理
try:
    # Python 2
    import urllib2 as urllib_request
except ImportError:
    # Python 3
    import urllib.request as urllib_request
    import urllib.error as urllib_error
import sys

# ADC API响应解析函数


def format_adc_response_for_ansible(response_data, action="", changed_default=True):
    """
    格式化ADC响应为Ansible模块返回格式

    Args:
        response_data (str/dict): API响应数据
        action (str): 执行的操作名称
        changed_default (bool): 默认的changed状态

    Returns:
        tuple: (success, result_dict)
            - success (bool): 操作是否成功
            - result_dict (dict): Ansible模块返回字典
    """

    # 初始化返回结果
    result = {
        'success': False,
        'result': '',
        'errcode': '',
        'errmsg': '',
        'data': {}
    }

    try:
        # 如果是字符串，尝试解析为JSON
        if isinstance(response_data, str):
            parsed_data = json.loads(response_data)
        else:
            parsed_data = response_data

        result['data'] = parsed_data

        # 提取基本字段
        result['result'] = parsed_data.get('result', '')
        result['errcode'] = parsed_data.get('errcode', '')
        result['errmsg'] = parsed_data.get('errmsg', '')

        # 判断操作是否成功
        if result['result'].lower() == 'success':
            result['success'] = True
        else:
            # 处理幂等性问题 - 检查错误信息中是否包含"已存在"等表示已存在的关键词
            errmsg = result['errmsg'].lower() if isinstance(
                result['errmsg'], str) else str(result['errmsg']).lower()
            if any(keyword in errmsg for keyword in ['已存在', 'already exists', 'already exist', 'exists']):
                # 幂等性处理：如果是因为已存在而导致的"失败"，实际上算成功
                result['success'] = True
                result['result'] = 'success (already exists)'

    except json.JSONDecodeError as e:
        result['errmsg'] = "JSON解析失败: %s" % str(e)
        result['errcode'] = 'JSON_PARSE_ERROR'
    except Exception as e:
        result['errmsg'] = "响应解析异常: %s" % str(e)
        result['errcode'] = 'PARSE_EXCEPTION'

    # 格式化为Ansible返回格式
    if result['success']:
        # 操作成功
        result_dict = {
            'changed': changed_default,
            'msg': '%s操作成功' % action if action else '操作成功',
            'response': result['data']
        }

        # 如果是幂等性成功（已存在），调整消息
        if 'already exists' in result['result']:
            result_dict['changed'] = False
            result_dict['msg'] = '%s操作成功（资源已存在，无需更改）' % action if action else '操作成功（资源已存在，无需更改）'

        return True, result_dict
    else:
        # 操作失败
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


def adc_list_routes(module):
    """获取IPv6静态路由列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=route.static.ipv6.list" % (
        ip, authkey)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
                        req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取IPv6静态路由列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv6静态路由列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, routes=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_route(module):
    """获取IPv6静态路由详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    destination = module.params['destination'] if 'destination' in module.params else ""
    prefix_len = module.params['prefix_len'] if 'prefix_len' in module.params else ""
    gateway = module.params['gateway'] if 'gateway' in module.params else ""

    # 检查必需参数
    if not destination or not prefix_len or not gateway:
        module.fail_json(
            msg="获取IPv6静态路由详情需要提供destination、prefix_len和gateway参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=route.static.ipv6.get" % (
        ip, authkey)

    # 构造请求数据
    route_data = {}
    # 只添加明确指定的参数
    if "destination" in module.params and module.params["destination"] is not None:
        acl_data["destination"] = module.params["destination"]
    if "prefix_len" in module.params and module.params["prefix_len"] is not None:
        acl_data["prefix_len"] = prefix_len
#         "gateway": gateway
   

    # 转换为JSON格式
    post_data = json.dumps(route_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
                        post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取IPv6静态路由详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv6静态路由详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, route=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_route(module):
    """添加IPv6静态路由"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    destination = module.params['destination'] if 'destination' in module.params else ""
    prefix_len = module.params['prefix_len'] if 'prefix_len' in module.params else ""
    gateway = module.params['gateway'] if 'gateway' in module.params else ""

    # 检查必需参数
    if not destination or not prefix_len or not gateway:
        module.fail_json(msg="添加IPv6静态路由需要提供destination、prefix_len和gateway参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=route.static.ipv6.add" % (
        ip, authkey)

    # 构造IPv6静态路由数据
    route_data = {}
    # 只添加明确指定的参数
    if "destination" in module.params and module.params["destination"] is not None:
        acl_data["destination"] = module.params["destination"]
    if "prefix_len" in module.params and module.params["prefix_len"] is not None:
        acl_data["prefix_len"] = prefix_len
#         "gateway": gateway
   

    # 添加可选参数
    if 'distance' in module.params and module.params['distance'] is not None:
        route_data['distance'] = module.params['distance']
    if 'pool' in module.params and module.params['pool'] is not None:
        route_data['pool'] = module.params['pool']

    # 转换为JSON格式
    post_data = json.dumps(route_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
                        post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="添加IPv6静态路由失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加IPv6静态路由", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_route(module):
    """编辑IPv6静态路由"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    destination = module.params['destination'] if 'destination' in module.params else ""
    prefix_len = module.params['prefix_len'] if 'prefix_len' in module.params else ""
    gateway = module.params['gateway'] if 'gateway' in module.params else ""

    # 检查必需参数
    if not destination or not prefix_len or not gateway:
        module.fail_json(msg="编辑IPv6静态路由需要提供destination、prefix_len和gateway参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=route.static.ipv6.edit" % (
        ip, authkey)

    # 构造IPv6静态路由数据
    route_data = {}
    # 只添加明确指定的参数
    if "destination" in module.params and module.params["destination"] is not None:
        acl_data["destination"] = module.params["destination"]
    if "prefix_len" in module.params and module.params["prefix_len"] is not None:
        acl_data["prefix_len"] = prefix_len
#         "gateway": gateway
   

    # 添加可选参数
    if 'distance' in module.params and module.params['distance'] is not None:
        route_data['distance'] = module.params['distance']
    if 'pool' in module.params and module.params['pool'] is not None:
        route_data['pool'] = module.params['pool']

    # 转换为JSON格式
    post_data = json.dumps(route_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
                        post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="编辑IPv6静态路由失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑IPv6静态路由", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_route(module):
    """删除IPv6静态路由"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    destination = module.params['destination'] if 'destination' in module.params else ""
    prefix_len = module.params['prefix_len'] if 'prefix_len' in module.params else ""
    gateway = module.params['gateway'] if 'gateway' in module.params else ""
    pool = module.params['pool'] if 'pool' in module.params else ""

    # 检查必需参数
    if not destination or not prefix_len or not gateway or not pool:
        module.fail_json(
            msg="删除IPv6静态路由需要提供destination、prefix_len、gateway和pool参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=route.static.ipv6.del" % (
        ip, authkey)

    # 构造请求数据
    route_data = {}
    # 只添加明确指定的参数
    if "destination" in module.params and module.params["destination"] is not None:
        acl_data["destination"] = module.params["destination"]
    if "prefix_len" in module.params and module.params["prefix_len"] is not None:
        acl_data["prefix_len"] = prefix_len
#         "gateway": gateway,
        "pool": pool
   

    # 转换为JSON格式
    post_data = json.dumps(route_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
                        post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="删除IPv6静态路由失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除IPv6静态路由", True)
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
        action=dict(type='str', required=True, choices=[
            'list_routes', 'get_route', 'add_route', 'edit_route', 'delete_route']),
        # IPv6静态路由参数
        destination=dict(type='str', required=False),
        prefix_len=dict(type='int', required=False),
        gateway=dict(type='str', required=False),
        distance=dict(type='int', required=False),
        pool=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list_routes':
        adc_list_routes(module)
    elif action == 'get_route':
        adc_get_route(module)
    elif action == 'add_route':
        adc_add_route(module)
    elif action == 'edit_route':
        adc_edit_route(module)
    elif action == 'delete_route':
        adc_delete_route(module)


if __name__ == '__main__':
    main()
