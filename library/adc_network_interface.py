#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import json
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


def adc_get_mgmt_interface(module):
    """获取管理接口配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.mgmt.get" % (
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
        module.fail_json(msg="获取管理接口配置失败: %s" % str(e))

    # 对于获取配置操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取管理接口配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_set_mgmt_interface(module):
    """设置管理接口配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    ip_addr = module.params['ip_addr'] if 'ip_addr' in module.params else ""
    netmask = module.params['netmask'] if 'netmask' in module.params else ""
    gateway = module.params['gateway'] if 'gateway' in module.params else ""

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.mgmt.set" % (
        ip, authkey)

    # 构造管理接口配置数据
    config_data = {}

    # 添加可选参数
    if ip_addr:
        config_data['ip_addr'] = ip_addr
    if netmask:
        config_data['netmask'] = netmask
    if gateway:
        config_data['gateway'] = gateway

    # 转换为JSON格式
    post_data = json.dumps(config_data)

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
        module.fail_json(msg="设置管理接口配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置管理接口配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_ethernet_interfaces(module):
    """获取以太网接口列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    list_type = module.params['list_type'] if 'list_type' in module.params else "normal"

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    if list_type == "withcommon":
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.list.withcommon" % (
            ip, authkey)
    elif list_type == "withused":
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.list.withused" % (
            ip, authkey)
    elif list_type == "self":
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.list.self" % (
            ip, authkey)
    else:
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.list" % (
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
        module.fail_json(msg="获取以太网接口列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取以太网接口列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interfaces=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_ethernet_interface(module):
    """获取以太网接口详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    interface_name = module.params['interface_name'] if 'interface_name' in module.params else ""

    # 检查必需参数
    if not interface_name:
        module.fail_json(msg="获取以太网接口详情需要提供interface_name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.get" % (
        ip, authkey)

    # 构造请求数据
    interface_data = {
        "interface_name": interface_name
    }

    # 转换为JSON格式
    post_data = json.dumps(interface_data)

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
        module.fail_json(msg="获取以太网接口详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取以太网接口详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interface=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_ethernet_interface(module):
    """编辑以太网接口配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    interface_name = module.params['interface_name'] if 'interface_name' in module.params else ""

    # 检查必需参数
    if not interface_name:
        module.fail_json(msg="编辑以太网接口配置需要提供interface_name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.edit" % (
        ip, authkey)

    # 构造以太网接口配置数据
    interface_data = {
        "interface_name": interface_name
    }

    # 添加可选参数
    if 'ip_addr' in module.params and module.params['ip_addr'] is not None:
        interface_data['ip_addr'] = module.params['ip_addr']
    if 'netmask' in module.params and module.params['netmask'] is not None:
        interface_data['netmask'] = module.params['netmask']
    if 'speed' in module.params and module.params['speed'] is not None:
        interface_data['speed'] = module.params['speed']
    if 'duplex' in module.params and module.params['duplex'] is not None:
        interface_data['duplex'] = module.params['duplex']
    if 'mtu' in module.params and module.params['mtu'] is not None:
        interface_data['mtu'] = module.params['mtu']
    if 'description' in module.params and module.params['description'] is not None:
        interface_data['description'] = module.params['description']

    # 转换为JSON格式
    post_data = json.dumps(interface_data)

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
        module.fail_json(msg="编辑以太网接口配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑以太网接口配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_ethernet_statistics(module):
    """获取以太网接口统计信息"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    interface_name = module.params['interface_name'] if 'interface_name' in module.params else ""

    # 检查必需参数
    if not interface_name:
        module.fail_json(msg="获取以太网接口统计信息需要提供interface_name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ethernet.statis" % (
        ip, authkey)

    # 构造请求数据
    interface_data = {
        "interface_name": interface_name
    }

    # 转换为JSON格式
    post_data = json.dumps(interface_data)

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
        module.fail_json(msg="获取以太网接口统计信息失败: %s" % str(e))

    # 对于获取统计信息操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取以太网接口统计信息失败", response=parsed_data)
            else:
                module.exit_json(changed=False, statistics=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_ve_interfaces(module):
    """获取VE接口列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ve.list" % (
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
        module.fail_json(msg="获取VE接口列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取VE接口列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interfaces=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_ve_interface(module):
    """获取VE接口详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    ve_id = module.params['ve_id'] if 've_id' in module.params else ""

    # 检查必需参数
    if not ve_id:
        module.fail_json(msg="获取VE接口详情需要提供ve_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ve.get" % (
        ip, authkey)

    # 构造请求数据
    ve_data = {
        "ve_id": ve_id
    }

    # 转换为JSON格式
    post_data = json.dumps(ve_data)

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
        module.fail_json(msg="获取VE接口详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取VE接口详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interface=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_ve_interface(module):
    """编辑VE接口配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    ve_id = module.params['ve_id'] if 've_id' in module.params else ""

    # 检查必需参数
    if not ve_id:
        module.fail_json(msg="编辑VE接口配置需要提供ve_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.ve.edit" % (
        ip, authkey)

    # 构造VE接口配置数据
    ve_data = {
        "ve_id": ve_id
    }

    # 添加可选参数
    if 'ip_addr' in module.params and module.params['ip_addr'] is not None:
        ve_data['ip_addr'] = module.params['ip_addr']
    if 'netmask' in module.params and module.params['netmask'] is not None:
        ve_data['netmask'] = module.params['netmask']
    if 'vlan_id' in module.params and module.params['vlan_id'] is not None:
        ve_data['vlan_id'] = module.params['vlan_id']
    if 'description' in module.params and module.params['description'] is not None:
        ve_data['description'] = module.params['description']

    # 转换为JSON格式
    post_data = json.dumps(ve_data)

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
        module.fail_json(msg="编辑VE接口配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑VE接口配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_trunk_interfaces(module):
    """获取TRUNK接口列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.trunk.list" % (
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
        module.fail_json(msg="获取TRUNK接口列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TRUNK接口列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interfaces=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_trunk_interface(module):
    """获取TRUNK接口详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    trunk_id = module.params['trunk_id'] if 'trunk_id' in module.params else ""

    # 检查必需参数
    if not trunk_id:
        module.fail_json(msg="获取TRUNK接口详情需要提供trunk_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.trunk.get" % (
        ip, authkey)

    # 构造请求数据
    trunk_data = {
        "trunk_id": trunk_id
    }

    # 转换为JSON格式
    post_data = json.dumps(trunk_data)

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
        module.fail_json(msg="获取TRUNK接口详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TRUNK接口详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, interface=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_trunk_interface(module):
    """编辑TRUNK接口配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    trunk_id = module.params['trunk_id'] if 'trunk_id' in module.params else ""

    # 检查必需参数
    if not trunk_id:
        module.fail_json(msg="编辑TRUNK接口配置需要提供trunk_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=interface.trunk.edit" % (
        ip, authkey)

    # 构造TRUNK接口配置数据
    trunk_data = {
        "trunk_id": trunk_id
    }

    # 添加可选参数
    if 'interface_list' in module.params and module.params['interface_list'] is not None:
        trunk_data['interface_list'] = module.params['interface_list']
    if 'description' in module.params and module.params['description'] is not None:
        trunk_data['description'] = module.params['description']

    # 转换为JSON格式
    post_data = json.dumps(trunk_data)

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
        module.fail_json(msg="编辑TRUNK接口配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑TRUNK接口配置", True)
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
            'get_mgmt_interface', 'set_mgmt_interface',
            'list_ethernet_interfaces', 'get_ethernet_interface', 'edit_ethernet_interface', 'get_ethernet_statistics',
            'list_ve_interfaces', 'get_ve_interface', 'edit_ve_interface',
            'list_trunk_interfaces', 'get_trunk_interface', 'edit_trunk_interface']),
        # 管理接口参数
        ip_addr=dict(type='str', required=False),
        netmask=dict(type='str', required=False),
        gateway=dict(type='str', required=False),
        # 以太网接口参数
        interface_name=dict(type='str', required=False),
        speed=dict(type='str', required=False),
        duplex=dict(type='str', required=False),
        mtu=dict(type='int', required=False),
        description=dict(type='str', required=False),
        list_type=dict(type='str', required=False, choices=[
                       'normal', 'withcommon', 'withused', 'self']),
        # VE接口参数
        ve_id=dict(type='int', required=False),
        vlan_id=dict(type='int', required=False),
        # TRUNK接口参数
        trunk_id=dict(type='int', required=False),
        interface_list=dict(type='list', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'get_mgmt_interface':
        adc_get_mgmt_interface(module)
    elif action == 'set_mgmt_interface':
        adc_set_mgmt_interface(module)
    elif action == 'list_ethernet_interfaces':
        adc_list_ethernet_interfaces(module)
    elif action == 'get_ethernet_interface':
        adc_get_ethernet_interface(module)
    elif action == 'edit_ethernet_interface':
        adc_edit_ethernet_interface(module)
    elif action == 'get_ethernet_statistics':
        adc_get_ethernet_statistics(module)
    elif action == 'list_ve_interfaces':
        adc_list_ve_interfaces(module)
    elif action == 'get_ve_interface':
        adc_get_ve_interface(module)
    elif action == 'edit_ve_interface':
        adc_edit_ve_interface(module)
    elif action == 'list_trunk_interfaces':
        adc_list_trunk_interfaces(module)
    elif action == 'get_trunk_interface':
        adc_get_trunk_interface(module)
    elif action == 'edit_trunk_interface':
        adc_edit_trunk_interface(module)


if __name__ == '__main__':
    main()
