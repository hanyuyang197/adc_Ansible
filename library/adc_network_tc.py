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


def adc_get_global_tc_config(module):
    """获取全局TC配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.global.get" % (
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
        module.fail_json(msg="获取全局TC配置失败: %s" % str(e))

    # 对于获取配置操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取全局TC配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_set_global_tc_config(module):
    """设置全局TC配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    enable = module.params['enable'] if 'enable' in module.params else ""

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.global.set" % (
        ip, authkey)

    # 构造全局TC配置数据
    config_data = {}

    # 添加可选参数
    if enable != "":
        config_data['enable'] = enable

    # 转换为JSON格式
    post_data = json.dumps(config_data)

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
        module.fail_json(msg="设置全局TC配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置全局TC配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_tc_entries(module):
    """获取TC条目列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    list_type = module.params['list_type'] if 'list_type' in module.params else "normal"

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    if list_type == "withcommon":
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.list.withcommon" % (
            ip, authkey)
    else:
        url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.list" % (
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
        module.fail_json(msg="获取TC条目列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TC条目列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, entries=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_tc_entry(module):
    """获取TC条目详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取TC条目详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.get" % (
        ip, authkey)

    # 构造请求数据
    entry_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    # 转换为JSON格式
    post_data = json.dumps(entry_data)

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
        module.fail_json(msg="获取TC条目详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TC条目详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, entry=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_tc_entry(module):
    """添加TC条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加TC条目需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.add" % (
        ip, authkey)

    # 构造TC条目数据
    entry_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    # 添加可选参数
    if 'description' in module.params and module.params['description'] is not None:
        entry_data['description'] = module.params['description']
    if 'bandwidth' in module.params and module.params['bandwidth'] is not None:
        entry_data['bandwidth'] = module.params['bandwidth']

    # 转换为JSON格式
    post_data = json.dumps(entry_data)

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
        module.fail_json(msg="添加TC条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加TC条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_tc_entry(module):
    """编辑TC条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑TC条目需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.edit" % (
        ip, authkey)

    # 构造TC条目数据
    entry_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    # 添加可选参数
    if 'description' in module.params and module.params['description'] is not None:
        entry_data['description'] = module.params['description']
    if 'bandwidth' in module.params and module.params['bandwidth'] is not None:
        entry_data['bandwidth'] = module.params['bandwidth']

    # 转换为JSON格式
    post_data = json.dumps(entry_data)

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
        module.fail_json(msg="编辑TC条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑TC条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_tc_entry(module):
    """删除TC条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除TC条目需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.del" % (
        ip, authkey)

    # 构造请求数据
    entry_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]

    # 转换为JSON格式
    post_data = json.dumps(entry_data)

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
        module.fail_json(msg="删除TC条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除TC条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_tc_rules(module):
    """获取TC规则列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tc_name = module.params['tc_name'] if 'tc_name' in module.params else ""

    # 检查必需参数
    if not tc_name:
        module.fail_json(msg="获取TC规则列表需要提供tc_name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.rule.list" % (
        ip, authkey)

    # 构造请求数据
    rule_data = {}
    # 只添加明确指定的参数
    if "tc_name" in module.params and module.params["tc_name"] is not None:
        acl_data["tc_name"] = module.params["tc_name"]

    # 转换为JSON格式
    post_data = json.dumps(rule_data)

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
        module.fail_json(msg="获取TC规则列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TC规则列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, rules=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_tc_rule(module):
    """获取TC规则详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tc_name = module.params['tc_name'] if 'tc_name' in module.params else ""
    rule_id = module.params['rule_id'] if 'rule_id' in module.params else ""

    # 检查必需参数
    if not tc_name or not rule_id:
        module.fail_json(msg="获取TC规则详情需要提供tc_name和rule_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.rule.get" % (
        ip, authkey)

    # 构造请求数据
    rule_data = {}
    # 只添加明确指定的参数
    if "tc_name" in module.params and module.params["tc_name"] is not None:
        acl_data["tc_name"] = module.params["tc_name"]
    if "rule_id" in module.params and module.params["rule_id"] is not None:
        acl_data["rule_id"] = rule_id
   

    # 转换为JSON格式
    post_data = json.dumps(rule_data)

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
        module.fail_json(msg="获取TC规则详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取TC规则详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, rule=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_tc_rule(module):
    """添加TC规则"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tc_name = module.params['tc_name'] if 'tc_name' in module.params else ""
    rule_id = module.params['rule_id'] if 'rule_id' in module.params else ""

    # 检查必需参数
    if not tc_name or not rule_id:
        module.fail_json(msg="添加TC规则需要提供tc_name和rule_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.rule.add" % (
        ip, authkey)

    # 构造TC规则数据
    rule_data = {}
    # 只添加明确指定的参数
    if "tc_name" in module.params and module.params["tc_name"] is not None:
        acl_data["tc_name"] = module.params["tc_name"]
    if "rule_id" in module.params and module.params["rule_id"] is not None:
        acl_data["rule_id"] = rule_id
   

    # 添加可选参数
    if 'source_ip' in module.params and module.params['source_ip'] is not None:
        rule_data['source_ip'] = module.params['source_ip']
    if 'destination_ip' in module.params and module.params['destination_ip'] is not None:
        rule_data['destination_ip'] = module.params['destination_ip']
    if 'protocol' in module.params and module.params['protocol'] is not None:
        rule_data['protocol'] = module.params['protocol']
    if 'source_port' in module.params and module.params['source_port'] is not None:
        rule_data['source_port'] = module.params['source_port']
    if 'destination_port' in module.params and module.params['destination_port'] is not None:
        rule_data['destination_port'] = module.params['destination_port']

    # 转换为JSON格式
    post_data = json.dumps(rule_data)

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
        module.fail_json(msg="添加TC规则失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加TC规则", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_tc_rule(module):
    """编辑TC规则"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tc_name = module.params['tc_name'] if 'tc_name' in module.params else ""
    rule_id = module.params['rule_id'] if 'rule_id' in module.params else ""

    # 检查必需参数
    if not tc_name or not rule_id:
        module.fail_json(msg="编辑TC规则需要提供tc_name和rule_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.rule.edit" % (
        ip, authkey)

    # 构造TC规则数据
    rule_data = {}
    # 只添加明确指定的参数
    if "tc_name" in module.params and module.params["tc_name"] is not None:
        acl_data["tc_name"] = module.params["tc_name"]
    if "rule_id" in module.params and module.params["rule_id"] is not None:
        acl_data["rule_id"] = rule_id
   

    # 添加可选参数
    if 'source_ip' in module.params and module.params['source_ip'] is not None:
        rule_data['source_ip'] = module.params['source_ip']
    if 'destination_ip' in module.params and module.params['destination_ip'] is not None:
        rule_data['destination_ip'] = module.params['destination_ip']
    if 'protocol' in module.params and module.params['protocol'] is not None:
        rule_data['protocol'] = module.params['protocol']
    if 'source_port' in module.params and module.params['source_port'] is not None:
        rule_data['source_port'] = module.params['source_port']
    if 'destination_port' in module.params and module.params['destination_port'] is not None:
        rule_data['destination_port'] = module.params['destination_port']

    # 转换为JSON格式
    post_data = json.dumps(rule_data)

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
        module.fail_json(msg="编辑TC规则失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑TC规则", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_tc_rule(module):
    """删除TC规则"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    tc_name = module.params['tc_name'] if 'tc_name' in module.params else ""
    rule_id = module.params['rule_id'] if 'rule_id' in module.params else ""

    # 检查必需参数
    if not tc_name or not rule_id:
        module.fail_json(msg="删除TC规则需要提供tc_name和rule_id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=network.tc.rule.del" % (
        ip, authkey)

    # 构造请求数据
    rule_data = {}
    # 只添加明确指定的参数
    if "tc_name" in module.params and module.params["tc_name"] is not None:
        acl_data["tc_name"] = module.params["tc_name"]
    if "rule_id" in module.params and module.params["rule_id"] is not None:
        acl_data["rule_id"] = rule_id
   

    # 转换为JSON格式
    post_data = json.dumps(rule_data)

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
        module.fail_json(msg="删除TC规则失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除TC规则", True)
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
            'get_global_tc_config', 'set_global_tc_config',
            'list_tc_entries', 'get_tc_entry', 'add_tc_entry', 'edit_tc_entry', 'delete_tc_entry',
            'list_tc_rules', 'get_tc_rule', 'add_tc_rule', 'edit_tc_rule', 'delete_tc_rule']),
        # TC参数
        name=dict(type='str', required=False),
        tc_name=dict(type='str', required=False),
        rule_id=dict(type='str', required=False),
        description=dict(type='str', required=False),
        bandwidth=dict(type='int', required=False),
        source_ip=dict(type='str', required=False),
        destination_ip=dict(type='str', required=False),
        protocol=dict(type='str', required=False),
        source_port=dict(type='int', required=False),
        destination_port=dict(type='int', required=False),
        enable=dict(type='int', required=False),
        list_type=dict(type='str', required=False,
                    choices=['normal', 'withcommon'])
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'get_global_tc_config':
        adc_get_global_tc_config(module)
    elif action == 'set_global_tc_config':
        adc_set_global_tc_config(module)
    elif action == 'list_tc_entries':
        adc_list_tc_entries(module)
    elif action == 'get_tc_entry':
        adc_get_tc_entry(module)
    elif action == 'add_tc_entry':
        adc_add_tc_entry(module)
    elif action == 'edit_tc_entry':
        adc_edit_tc_entry(module)
    elif action == 'delete_tc_entry':
        adc_delete_tc_entry(module)
    elif action == 'list_tc_rules':
        adc_list_tc_rules(module)
    elif action == 'get_tc_rule':
        adc_get_tc_rule(module)
    elif action == 'add_tc_rule':
        adc_add_tc_rule(module)
    elif action == 'edit_tc_rule':
        adc_edit_tc_rule(module)
    elif action == 'delete_tc_rule':
        adc_delete_tc_rule(module)


if __name__ == '__main__':
    main()
