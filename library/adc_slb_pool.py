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


def slb_pool_names_list(module):
    """获取服务池名称列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.names.list" % (ip, authkey)

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
                    module.fail_json(msg="获取服务池名称列表失败", response=parsed_data)
                else:
                    module.exit_json(changed=False, pool_names=parsed_data)
            except Exception as e:
                module.fail_json(msg="解析响应失败: %s" % str(e))
        else:
            module.fail_json(msg="未收到有效响应")

    except Exception as e:
        module.fail_json(msg="获取服务池名称列表失败: %s" % str(e))


def slb_pool_list(module):
    """获取服务池列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.list" % (
        ip, authkey)

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

    except Exception as e:
        module.fail_json(msg="获取服务池列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取服务池列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, pools=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_pool_get(module):
    """获取服务池详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取服务池详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.get" % (
        ip, authkey)

    # 构造请求数据
    pool_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="获取服务池详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取服务池详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, pool=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_pool_add(module):
    """添加服务池"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.add" % (
        ip, authkey)

    # 构造服务池数据 - 手动组装成pool对象
    pool_data = {
        "pool": {}
    }

    # 添加基本参数到pool中
    basic_params = ['name', 'protocol', 'lb_method', 'upnum', 'healthcheck', 'desc_pool',
                    'action_on_service_down', 'aux_node_log', 'slow_ramp_time',
                    'node_select_fail_send_rst']

    for param in basic_params:
        if param in module.params and module.params[param] is not None:
            # 将下划线参数名映射为连字符（与API文档一致）
            api_param = param.replace('_', '-')
            pool_data['pool'][api_param] = module.params[param]

    # 直接使用 up_members_at_least 对象参数
    if 'up_members_at_least' in module.params and module.params['up_members_at_least'] is not None:
        pool_data['pool']['up-members-at-least'] = module.params['up_members_at_least']

    # 添加 members 数组参数
    if 'members' in module.params and module.params['members'] is not None:
        pool_data['pool']['members'] = module.params['members']

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="添加服务池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加服务池", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_pool_edit(module):
    """编辑服务池"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑服务池需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.edit" % (
        ip, authkey)

    # 构造服务池数据 - 手动组装成pool对象
    pool_data = {
        "pool": {}
    }

    # 添加name参数（必需）
    pool_data['pool']['name'] = name

    # 添加可选参数到pool中
    optional_params = ['protocol', 'lb_method', 'upnum', 'healthcheck', 'desc_pool',
                       'action_on_service_down', 'aux_node_log', 'slow_ramp_time',
                       'node_select_fail_send_rst']

    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            # 将下划线参数名映射为连字符（与API文档一致）
            api_param = param.replace('_', '-')
            pool_data['pool'][api_param] = module.params[param]

    # 直接使用 up_members_at_least 对象参数
    if 'up_members_at_least' in module.params and module.params['up_members_at_least'] is not None:
        pool_data['pool']['up-members-at-least'] = module.params['up_members_at_least']

    # 添加 members 数组参数
    if 'members' in module.params and module.params['members'] is not None:
        pool_data['pool']['members'] = module.params['members']

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="编辑服务池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑服务池", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_pool_del(module):
    """删除服务池"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除服务池需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.del" % (
        ip, authkey)

    # 构造服务池数据
    pool_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="删除服务池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除服务池", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_pool_member_add(module):
    """添加节点到服务池"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    # 使用 name 参数（与API文档一致），兼容 pool_name 别名
    pool_name = module.params.get('name', '')

    # 检查必需参数
    if not pool_name:
        module.fail_json(msg="添加节点到服务池需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.member.add" % (
        ip, authkey)

    # 构造请求数据 - 手动组装成member对象（与API文档结构一致）
    pool_data = {
        "name": pool_name,
        "member": {}
    }

    # 如果提供了完整的 member 对象，直接使用
    if 'member' in module.params and module.params['member'] is not None:
        pool_data['member'] = module.params['member']
    else:
        # 否则使用单独的参数构建 member 对象
        member_params = ['nodename', 'server', 'port', 'priority', 'weight', 'status', 'conn_limit']
        for param in member_params:
            if param in module.params and module.params[param] is not None:
                pool_data['member'][param] = module.params[param]

        # 添加 member_protocol 参数（使用 member_protocol 而不是 protocol）
        if 'member_protocol' in module.params and module.params['member_protocol'] is not None:
            pool_data['member']['protocol'] = module.params['member_protocol']

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="添加节点到服务池失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加节点到服务池", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_pool_member_del(module):
    """从服务池删除节点"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    # 使用 name 参数（与API文档一致）
    pool_name = module.params.get('name', '')

    # 检查必需参数
    if not pool_name:
        module.fail_json(msg="从服务池删除节点需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.member.del" % (
        ip, authkey)

    # 构造请求数据 - 使用member对象（与API文档一致）
    pool_data = {
        "name": pool_name
    }

    # 如果提供了完整的 member 对象，直接使用
    if 'member' in module.params and module.params['member'] is not None:
        pool_data['member'] = module.params['member']
    else:
        # 否则使用单独的参数构建 member 对象
        pool_data['member'] = {}
        member_params = ['nodename', 'server', 'port', 'priority', 'weight', 'status', 'conn_limit']
        for param in member_params:
            if param in module.params and module.params[param] is not None:
                pool_data['member'][param] = module.params[param]

        # 添加 member_protocol 参数
        if 'member_protocol' in module.params and module.params['member_protocol'] is not None:
            pool_data['member']['protocol'] = module.params['member_protocol']

    # 转换为JSON格式
    post_data = json.dumps(pool_data)

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
        module.fail_json(msg="从服务池删除节点失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "从服务池删除节点", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")



def slb_pool_list_withcommon(module):
    """获取服务池列表(带公共参数)"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.list.withcommon" % (ip, authkey)

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
        module.fail_json(msg="获取服务池列表(带公共参数)失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取服务池列表(带公共参数)失败", response=parsed_data)
            else:
                module.exit_json(changed=False, pools=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def slb_pool_member_edit(module):
    """编辑服务池成员"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    # 使用 name 参数（与API文档一致），兼容 pool_name 别名
    pool_name = module.params.get('name', '')

    if not pool_name:
        module.fail_json(msg="编辑服务池成员需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.member.edit" % (ip, authkey)

    # 构造请求数据 - 手动组装成member对象（与API文档结构一致）
    pool_data = {
        "name": pool_name,
        "member": {}
    }

    # 如果提供了完整的 member 对象，直接使用
    if 'member' in module.params and module.params['member'] is not None:
        pool_data['member'] = module.params['member']
    else:
        # 否则使用单独的参数构建 member 对象
        member_params = ['nodename', 'server', 'port', 'priority', 'weight', 'status', 'conn_limit']
        for param in member_params:
            if param in module.params and module.params[param] is not None:
                pool_data['member'][param] = module.params[param]

        # 添加 member_protocol 参数（使用 member_protocol 而不是 protocol）
        if 'member_protocol' in module.params and module.params['member_protocol'] is not None:
            pool_data['member']['protocol'] = module.params['member_protocol']

    post_data = json.dumps(pool_data)
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
        module.fail_json(msg="编辑服务池成员失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑服务池成员", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def slb_pool_member_onoff(module):
    """启用/禁用服务池成员"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.pool.member.onoff" % (ip, authkey)

    # 构造请求数据 - 与API文档结构一致
    pool_data = {
        "name": module.params.get('name', ''),
        "member": {}
    }

    # 如果提供了完整的 member 对象，直接使用
    if 'member' in module.params and module.params['member'] is not None:
        pool_data['member'] = module.params['member']
    else:
        # 否则使用单独的参数构建 member 对象
        member_params = ['nodename', 'server', 'port', 'priority', 'weight', 'status', 'conn_limit']
        for param in member_params:
            if param in module.params and module.params[param] is not None:
                pool_data['member'][param] = module.params[param]

        # 添加 member_protocol 参数
        if 'member_protocol' in module.params and module.params['member_protocol'] is not None:
            pool_data['member']['protocol'] = module.params['member_protocol']

    # 特殊处理 status 参数（启用/禁用状态）
    if 'status' in module.params and module.params['status'] is not None:
        pool_data['member']['status'] = module.params['status']

    # 转换为JSON格式
    post_data = json.dumps(pool_data)
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
        module.fail_json(msg="启用/禁用服务池成员失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "启用/禁用服务池成员", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")




def main():
    # 定义模块参数 - 所有参数都单独定义，与API文档字段对应
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
                    'slb_pool_names_list', 'slb_pool_list', 'slb_pool_list_withcommon', 'slb_pool_get', 'slb_pool_add', 'slb_pool_edit', 'slb_pool_del', 'slb_pool_member_add', 'slb_pool_member_del', 'slb_pool_member_edit', 'slb_pool_member_onoff']),
        # 服务池参数（pool对象内的字段）- Python用下划线，YAML可用连字符alias
        name=dict(type='str', required=False),
        protocol=dict(type='int', required=False),
        lb_method=dict(type='int', required=False),
        upnum=dict(type='int', required=False),
        healthcheck=dict(type='str', required=False),
        desc_pool=dict(type='str', required=False),
        action_on_service_down=dict(type='int', required=False, aliases=['action-on-service-down']),
        aux_node_log=dict(type='int', required=False, aliases=['aux-node-log']),
        slow_ramp_time=dict(type='int', required=False, aliases=['slow-ramp-time']),
        node_select_fail_send_rst=dict(type='int', required=False, aliases=['node-select-fail-send-rst']),
        # up-members-at-least 对象
        up_members_at_least=dict(type='dict', required=False, aliases=['up-members-at-least']),
        # members 数组（用于pool.edit）
        members=dict(type='list', required=False, elements='dict'),
        # 服务池成员参数（用于pool.member.add/edit）
        nodename=dict(type='str', required=False),
        server=dict(type='str', required=False),
        port=dict(type='int', required=False),
        member_protocol=dict(type='int', required=False),
        priority=dict(type='int', required=False),
        weight=dict(type='int', required=False),
        status=dict(type='int', required=False),
        conn_limit=dict(type='int', required=False),
        # member 对象（用于pool.member.add/edit）
        member=dict(type='dict', required=False),
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    # 为了解决静态检查工具的问题，我们进行类型转换
    action = module.params['action']
    if hasattr(action, '__str__'):
        action = str(action)

    if action == 'slb_pool_names_list':
        slb_pool_names_list(module)
    elif action == 'slb_pool_list':
        slb_pool_list(module)
    elif action == 'slb_pool_list_withcommon':
        slb_pool_list_withcommon(module)
    elif action == 'slb_pool_get':
        slb_pool_get(module)
    elif action == 'slb_pool_add':
        slb_pool_add(module)
    elif action == 'slb_pool_edit':
        slb_pool_edit(module)
    elif action == 'slb_pool_del':
        slb_pool_del(module)
    elif action == 'slb_pool_member_add':
        slb_pool_member_add(module)
    elif action == 'slb_pool_member_del':
        slb_pool_member_del(module)
    elif action == 'slb_pool_member_edit':
        slb_pool_member_edit(module)
    elif action == 'slb_pool_member_onoff':
        slb_pool_member_onoff(module)



if __name__ == '__main__':
    main()
