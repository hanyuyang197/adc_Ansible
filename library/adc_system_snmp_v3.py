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


def adc_add_snmp_v3_view(module):
    """添加SNMPv3视图"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    oid = module.params['oid']

    # 检查必需参数
    if not name or not oid:
        module.fail_json(msg="添加SNMPv3视图需要提供name和oid参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.view.add" % (
        ip, authkey)

    # 构造视图数据
    view_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "oid" in module.params and module.params["oid"] is not None:
        acl_data["oid"] = oid
   

    # 添加可选参数
    if 'mask' in module.params and module.params['mask'] is not None:
        view_data['mask'] = module.params['mask']
    if 'type' in module.params and module.params['type'] is not None:
        view_data['type'] = module.params['type']

    # 转换为JSON格式
    post_data = json.dumps(view_data)

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
        module.fail_json(msg="添加SNMPv3视图失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加SNMPv3视图", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_snmp_v3_views(module):
    """获取SNMPv3视图列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.view.list" % (
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
        module.fail_json(msg="获取SNMPv3视图列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMPv3视图列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, views=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_snmp_v3_view(module):
    """获取SNMPv3视图"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    oid = module.params['oid']

    # 检查必需参数
    if not name or not oid:
        module.fail_json(msg="获取SNMPv3视图需要提供name和oid参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.view.get" % (
        ip, authkey)

    # 构造视图数据
    view_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "oid" in module.params and module.params["oid"] is not None:
        acl_data["oid"] = oid
   

    # 转换为JSON格式
    post_data = json.dumps(view_data)

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
        module.fail_json(msg="获取SNMPv3视图失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMPv3视图失败", response=parsed_data)
            else:
                module.exit_json(changed=False, view=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_snmp_v3_view(module):
    """删除SNMPv3视图"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    oid = module.params['oid']

    # 检查必需参数
    if not name or not oid:
        module.fail_json(msg="删除SNMPv3视图需要提供name和oid参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.view.del" % (
        ip, authkey)

    # 构造视图数据
    view_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "oid" in module.params and module.params["oid"] is not None:
        acl_data["oid"] = oid
   

    # 转换为JSON格式
    post_data = json.dumps(view_data)

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
        module.fail_json(msg="删除SNMPv3视图失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除SNMPv3视图", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_snmp_v3_view(module):
    """编辑SNMPv3视图"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    old_oid = module.params['old_oid']
    oid = module.params['oid']

    # 检查必需参数
    if not name or not old_oid or not oid:
        module.fail_json(msg="编辑SNMPv3视图需要提供name、old_oid和oid参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.view.edit" % (
        ip, authkey)

    # 构造视图数据
    view_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "old_oid" in module.params and module.params["old_oid"] is not None:
        acl_data["old_oid"] = old_oid
#         "oid": oid
   

    # 添加可选参数
    if 'mask' in module.params and module.params['mask'] is not None:
        view_data['mask'] = module.params['mask']
    if 'type' in module.params and module.params['type'] is not None:
        view_data['type'] = module.params['type']

    # 转换为JSON格式
    post_data = json.dumps(view_data)

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
        module.fail_json(msg="编辑SNMPv3视图失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑SNMPv3视图", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_snmp_v3_group(module):
    """添加SNMPv3组"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    view = module.params['view']
    auth_mode = module.params['auth_mode']

    # 检查必需参数
    if not name or not view or not auth_mode:
        module.fail_json(msg="添加SNMPv3组需要提供name、view和auth_mode参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.group.add" % (
        ip, authkey)

    # 构造组数据
    group_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "view" in module.params and module.params["view"] is not None:
        acl_data["view"] = view
#         "auth_mode": auth_mode
   

    # 转换为JSON格式
    post_data = json.dumps(group_data)

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
        module.fail_json(msg="添加SNMPv3组失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加SNMPv3组", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_snmp_v3_groups(module):
    """获取SNMPv3组列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.group.list" % (
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
        module.fail_json(msg="获取SNMPv3组列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMPv3组列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, groups=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_snmp_v3_group(module):
    """获取SNMPv3组"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取SNMPv3组需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.group.get" % (
        ip, authkey)

    # 构造组数据
    group_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    # 转换为JSON格式
    post_data = json.dumps(group_data)

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
        module.fail_json(msg="获取SNMPv3组失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMPv3组失败", response=parsed_data)
            else:
                module.exit_json(changed=False, group=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_snmp_v3_group(module):
    """删除SNMPv3组"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除SNMPv3组需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.group.del" % (
        ip, authkey)

    # 构造组数据
    group_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    # 转换为JSON格式
    post_data = json.dumps(group_data)

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
        module.fail_json(msg="删除SNMPv3组失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除SNMPv3组", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_snmp_v3_group(module):
    """编辑SNMPv3组"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    view = module.params['view']
    auth_mode = module.params['auth_mode']

    # 检查必需参数
    if not name or not view or not auth_mode:
        module.fail_json(msg="编辑SNMPv3组需要提供name、view和auth_mode参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.group.edit" % (
        ip, authkey)

    # 构造组数据
    group_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "view" in module.params and module.params["view"] is not None:
        acl_data["view"] = view
#         "auth_mode": auth_mode
   

    # 转换为JSON格式
    post_data = json.dumps(group_data)

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
        module.fail_json(msg="编辑SNMPv3组失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑SNMPv3组", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_snmp_v3_user(module):
    """添加SNMPv3用户"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    group = module.params['group']
    auth_mode = module.params['auth_mode']

    # 检查必需参数
    if not name or not group or not auth_mode:
        module.fail_json(msg="添加SNMPv3用户需要提供name、group和auth_mode参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.user.add" % (
        ip, authkey)

    # 构造用户数据
    user_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "group" in module.params and module.params["group"] is not None:
        acl_data["group"] = group
#         "auth_mode": auth_mode
   

    # 添加可选参数
    if 'auth_password' in module.params and module.params['auth_password'] is not None:
        user_data['auth_password'] = module.params['auth_password']
    if 'encrypt_mode' in module.params and module.params['encrypt_mode'] is not None:
        user_data['encrypt_mode'] = module.params['encrypt_mode']
    if 'encrypt_password' in module.params and module.params['encrypt_password'] is not None:
        user_data['encrypt_password'] = module.params['encrypt_password']

    # 转换为JSON格式
    post_data = json.dumps(user_data)

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
        module.fail_json(msg="添加SNMPv3用户失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加SNMPv3用户", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_snmp_v3_users(module):
    """获取SNMPv3用户列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.user.list" % (
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
        module.fail_json(msg="获取SNMPv3用户列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMPv3用户列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, users=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_snmp_v3_user(module):
    """获取SNMPv3用户"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取SNMPv3用户需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.user.get" % (
        ip, authkey)

    # 构造用户数据
    user_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    # 转换为JSON格式
    post_data = json.dumps(user_data)

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
        module.fail_json(msg="获取SNMPv3用户失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMPv3用户失败", response=parsed_data)
            else:
                module.exit_json(changed=False, user=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_snmp_v3_user(module):
    """删除SNMPv3用户"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除SNMPv3用户需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.user.del" % (
        ip, authkey)

    # 构造用户数据
    user_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    # 转换为JSON格式
    post_data = json.dumps(user_data)

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
        module.fail_json(msg="删除SNMPv3用户失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除SNMPv3用户", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_snmp_v3_user(module):
    """编辑SNMPv3用户"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    group = module.params['group']
    auth_mode = module.params['auth_mode']

    # 检查必需参数
    if not name or not group or not auth_mode:
        module.fail_json(msg="编辑SNMPv3用户需要提供name、group和auth_mode参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.user.edit" % (
        ip, authkey)

    # 构造用户数据
    user_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "group" in module.params and module.params["group"] is not None:
        acl_data["group"] = group
#         "auth_mode": auth_mode
   

    # 添加可选参数
    if 'auth_password' in module.params and module.params['auth_password'] is not None:
        user_data['auth_password'] = module.params['auth_password']
    if 'encrypt_mode' in module.params and module.params['encrypt_mode'] is not None:
        user_data['encrypt_mode'] = module.params['encrypt_mode']
    if 'encrypt_password' in module.params and module.params['encrypt_password'] is not None:
        user_data['encrypt_password'] = module.params['encrypt_password']

    # 转换为JSON格式
    post_data = json.dumps(user_data)

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
        module.fail_json(msg="编辑SNMPv3用户失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑SNMPv3用户", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_snmp_v3_trap(module):
    """添加SNMPv3 TRAP"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    host = module.params['host']
    name = module.params['name']

    # 检查必需参数
    if not host or not name:
        module.fail_json(msg="添加SNMPv3 TRAP需要提供host和name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.trap.add" % (
        ip, authkey)

    # 构造TRAP数据
    trap_data = {}
    # 只添加明确指定的参数
    if "host" in module.params and module.params["host"] is not None:
        acl_data["host"] = module.params["host"]
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = name
   

    # 添加可选参数
    if 'port' in module.params and module.params['port'] is not None:
        trap_data['port'] = module.params['port']
    if 'version' in module.params and module.params['version'] is not None:
        trap_data['version'] = module.params['version']
    if 'auth_mode' in module.params and module.params['auth_mode'] is not None:
        trap_data['auth_mode'] = module.params['auth_mode']
    if 'auth_password' in module.params and module.params['auth_password'] is not None:
        trap_data['auth_password'] = module.params['auth_password']
    if 'encrypt_mode' in module.params and module.params['encrypt_mode'] is not None:
        trap_data['encrypt_mode'] = module.params['encrypt_mode']
    if 'encrypt_password' in module.params and module.params['encrypt_password'] is not None:
        trap_data['encrypt_password'] = module.params['encrypt_password']

    # 转换为JSON格式
    post_data = json.dumps(trap_data)

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
        module.fail_json(msg="添加SNMPv3 TRAP失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加SNMPv3 TRAP", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_snmp_v3_traps(module):
    """获取SNMPv3 TRAP列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.trap.list" % (
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
        module.fail_json(msg="获取SNMPv3 TRAP列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMPv3 TRAP列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, traps=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_snmp_v3_trap(module):
    """获取SNMPv3 TRAP"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    host = module.params['host']

    # 检查必需参数
    if not host:
        module.fail_json(msg="获取SNMPv3 TRAP需要提供host参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.trap.get" % (
        ip, authkey)

    # 构造TRAP数据
    trap_data = {}
    # 只添加明确指定的参数
    if "host" in module.params and module.params["host"] is not None:
        acl_data["host"] = module.params["host"]

    # 转换为JSON格式
    post_data = json.dumps(trap_data)

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
        module.fail_json(msg="获取SNMPv3 TRAP失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMPv3 TRAP失败", response=parsed_data)
            else:
                module.exit_json(changed=False, trap=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_snmp_v3_trap(module):
    """删除SNMPv3 TRAP"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    host = module.params['host']

    # 检查必需参数
    if not host:
        module.fail_json(msg="删除SNMPv3 TRAP需要提供host参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.trap.del" % (
        ip, authkey)

    # 构造TRAP数据
    trap_data = {}
    # 只添加明确指定的参数
    if "host" in module.params and module.params["host"] is not None:
        acl_data["host"] = module.params["host"]

    # 转换为JSON格式
    post_data = json.dumps(trap_data)

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
        module.fail_json(msg="删除SNMPv3 TRAP失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除SNMPv3 TRAP", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_snmp_v3_trap(module):
    """编辑SNMPv3 TRAP"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    host = module.params['host']
    name = module.params['name']

    # 检查必需参数
    if not host or not name:
        module.fail_json(msg="编辑SNMPv3 TRAP需要提供host和name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.v3.trap.edit" % (
        ip, authkey)

    # 构造TRAP数据
    trap_data = {}
    # 只添加明确指定的参数
    if "host" in module.params and module.params["host"] is not None:
        acl_data["host"] = module.params["host"]
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = name
   

    # 添加可选参数
    if 'port' in module.params and module.params['port'] is not None:
        trap_data['port'] = module.params['port']
    if 'version' in module.params and module.params['version'] is not None:
        trap_data['version'] = module.params['version']
    if 'auth_mode' in module.params and module.params['auth_mode'] is not None:
        trap_data['auth_mode'] = module.params['auth_mode']
    if 'auth_password' in module.params and module.params['auth_password'] is not None:
        trap_data['auth_password'] = module.params['auth_password']
    if 'encrypt_mode' in module.params and module.params['encrypt_mode'] is not None:
        trap_data['encrypt_mode'] = module.params['encrypt_mode']
    if 'encrypt_password' in module.params and module.params['encrypt_password'] is not None:
        trap_data['encrypt_password'] = module.params['encrypt_password']

    # 转换为JSON格式
    post_data = json.dumps(trap_data)

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
        module.fail_json(msg="编辑SNMPv3 TRAP失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑SNMPv3 TRAP", True)
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
            'add_view', 'list_views', 'get_view', 'delete_view', 'edit_view',
            'add_group', 'list_groups', 'get_group', 'delete_group', 'edit_group',
            'add_user', 'list_users', 'get_user', 'delete_user', 'edit_user',
            'add_trap', 'list_traps', 'get_trap', 'delete_trap', 'edit_trap']),
        # SNMPv3视图参数
        name=dict(type='str', required=False),
        oid=dict(type='str', required=False),
        mask=dict(type='str', required=False),
        type=dict(type='str', required=False),
        old_oid=dict(type='str', required=False),
        # SNMPv3组参数
        view=dict(type='str', required=False),
        auth_mode=dict(type='str', required=False),
        # SNMPv3用户参数
        group=dict(type='str', required=False),
        auth_password=dict(type='str', required=False, no_log=True),
        encrypt_mode=dict(type='str', required=False),
        encrypt_password=dict(type='str', required=False, no_log=True),
        # SNMPv3 TRAP参数
        host=dict(type='str', required=False),
        port=dict(type='int', required=False),
        version=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'add_view':
        adc_add_snmp_v3_view(module)
    elif action == 'list_views':
        adc_list_snmp_v3_views(module)
    elif action == 'get_view':
        adc_get_snmp_v3_view(module)
    elif action == 'delete_view':
        adc_delete_snmp_v3_view(module)
    elif action == 'edit_view':
        adc_edit_snmp_v3_view(module)
    elif action == 'add_group':
        adc_add_snmp_v3_group(module)
    elif action == 'list_groups':
        adc_list_snmp_v3_groups(module)
    elif action == 'get_group':
        adc_get_snmp_v3_group(module)
    elif action == 'delete_group':
        adc_delete_snmp_v3_group(module)
    elif action == 'edit_group':
        adc_edit_snmp_v3_group(module)
    elif action == 'add_user':
        adc_add_snmp_v3_user(module)
    elif action == 'list_users':
        adc_list_snmp_v3_users(module)
    elif action == 'get_user':
        adc_get_snmp_v3_user(module)
    elif action == 'delete_user':
        adc_delete_snmp_v3_user(module)
    elif action == 'edit_user':
        adc_edit_snmp_v3_user(module)
    elif action == 'add_trap':
        adc_add_snmp_v3_trap(module)
    elif action == 'list_traps':
        adc_list_snmp_v3_traps(module)
    elif action == 'get_trap':
        adc_get_snmp_v3_trap(module)
    elif action == 'delete_trap':
        adc_delete_snmp_v3_trap(module)
    elif action == 'edit_trap':
        adc_edit_snmp_v3_trap(module)


if __name__ == '__main__':
    main()
