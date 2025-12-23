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


def adc_list_acls(module):
    """获取IPv6访问列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.list" % (
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
        module.fail_json(msg="获取IPv6访问列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv6访问列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, acls=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_acl(module):
    """获取IPv6访问列表详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取IPv6访问列表详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.get" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {
        "name": name
    }

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="获取IPv6访问列表详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv6访问列表详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, acl=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_acl_item(module):
    """添加IPv6访问列表条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    seq_num = module.params['seq_num'] if 'seq_num' in module.params else ""

    # 检查必需参数
    if not name or not seq_num:
        module.fail_json(msg="添加IPv6访问列表条目需要提供name和seq_num参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.item.add" % (
        ip, authkey)

    # 构造ACL条目数据 - 只包含在YAML中明确定义的参数
    acl_data = {
        "name": name,
        "seq_num": seq_num
    }

    # 定义可选参数列表
    optional_params = [
        'acl_action', 'src_addr', 'src_prefix', 'dst_addr', 'dst_prefix',
        'protocol', 'src_port_op', 'src_port1', 'src_port2',
        'dst_port_op', 'dst_port1', 'dst_port2', 'icmp_type', 'icmp_code',
        'dscp', 'fragment', 'log', 'time_range'
    ]

    # 添加可选参数
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            acl_data[param] = module.params[param]

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="添加IPv6访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加IPv6访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_acl_item(module):
    """编辑IPv6访问列表条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    seq_num = module.params['seq_num'] if 'seq_num' in module.params else ""

    # 检查必需参数
    if not name or not seq_num:
        module.fail_json(msg="编辑IPv6访问列表条目需要提供name和seq_num参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.item.edit" % (
        ip, authkey)

    # 构造ACL条目数据
    acl_data = {
        "name": name,
        "seq_num": seq_num
    }

    # 添加可选参数
    if 'acl_action' in module.params and module.params['acl_action'] is not None:
        acl_data['action'] = module.params['acl_action']
    if 'src_addr' in module.params and module.params['src_addr'] is not None:
        acl_data['src_addr'] = module.params['src_addr']
    if 'src_prefix' in module.params and module.params['src_prefix'] is not None:
        acl_data['src_prefix'] = module.params['src_prefix']
    if 'dst_addr' in module.params and module.params['dst_addr'] is not None:
        acl_data['dst_addr'] = module.params['dst_addr']
    if 'dst_prefix' in module.params and module.params['dst_prefix'] is not None:
        acl_data['dst_prefix'] = module.params['dst_prefix']
    if 'protocol' in module.params and module.params['protocol'] is not None:
        acl_data['protocol'] = module.params['protocol']
    if 'src_port_op' in module.params and module.params['src_port_op'] is not None:
        acl_data['src_port_op'] = module.params['src_port_op']
    if 'src_port1' in module.params and module.params['src_port1'] is not None:
        acl_data['src_port1'] = module.params['src_port1']
    if 'src_port2' in module.params and module.params['src_port2'] is not None:
        acl_data['src_port2'] = module.params['src_port2']
    if 'dst_port_op' in module.params and module.params['dst_port_op'] is not None:
        acl_data['dst_port_op'] = module.params['dst_port_op']
    if 'dst_port1' in module.params and module.params['dst_port1'] is not None:
        acl_data['dst_port1'] = module.params['dst_port1']
    if 'dst_port2' in module.params and module.params['dst_port2'] is not None:
        acl_data['dst_port2'] = module.params['dst_port2']
    if 'icmp_type' in module.params and module.params['icmp_type'] is not None:
        acl_data['icmp_type'] = module.params['icmp_type']
    if 'icmp_code' in module.params and module.params['icmp_code'] is not None:
        acl_data['icmp_code'] = module.params['icmp_code']
    if 'dscp' in module.params and module.params['dscp'] is not None:
        acl_data['dscp'] = module.params['dscp']
    if 'fragment' in module.params and module.params['fragment'] is not None:
        acl_data['fragment'] = module.params['fragment']
    if 'log' in module.params and module.params['log'] is not None:
        acl_data['log'] = module.params['log']
    if 'time_range' in module.params and module.params['time_range'] is not None:
        acl_data['time_range'] = module.params['time_range']

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="编辑IPv6访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑IPv6访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_acl_item(module):
    """删除IPv6访问列表条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除IPv6访问列表条目需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.item.del" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {
        "name": name
    }

    # 如果提供了seq_num参数，则添加到请求数据中
    if 'seq_num' in module.params and module.params['seq_num'] is not None:
        acl_data['seq_num'] = module.params['seq_num']

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="删除IPv6访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除IPv6访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_set_acl_description(module):
    """设置IPv6访问列表描述"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    description = module.params['description'] if 'description' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="设置IPv6访问列表描述需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv6.ext.desc.set" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {
        "name": name,
        "description": description
    }

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="设置IPv6访问列表描述失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置IPv6访问列表描述", True)
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
        module_action=dict(type='str', required=True, choices=[
            'list_acls', 'get_acl', 'add_acl_item', 'edit_acl_item', 'delete_acl_item', 'set_acl_description']),
        # ACL参数
        name=dict(type='str', required=False),
        seq_num=dict(type='int', required=False),
        acl_action=dict(type='str', required=False),
        src_addr=dict(type='str', required=False),
        src_prefix=dict(type='int', required=False),
        dst_addr=dict(type='str', required=False),
        dst_prefix=dict(type='int', required=False),
        protocol=dict(type='str', required=False),
        src_port_op=dict(type='str', required=False),
        src_port1=dict(type='int', required=False),
        src_port2=dict(type='int', required=False),
        dst_port_op=dict(type='str', required=False),
        dst_port1=dict(type='int', required=False),
        dst_port2=dict(type='int', required=False),
        icmp_type=dict(type='int', required=False),
        icmp_code=dict(type='int', required=False),
        dscp=dict(type='int', required=False),
        fragment=dict(type='str', required=False),
        log=dict(type='int', required=False),
        time_range=dict(type='str', required=False),
        description=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据module_action执行相应操作
    module_action = module.params['module_action']

    if module_action == 'list_acls':
        adc_list_acls(module)
    elif module_action == 'get_acl':
        adc_get_acl(module)
    elif module_action == 'add_acl_item':
        adc_add_acl_item(module)
    elif module_action == 'edit_acl_item':
        adc_edit_acl_item(module)
    elif module_action == 'delete_acl_item':
        adc_delete_acl_item(module)
    elif module_action == 'set_acl_description':
        adc_set_acl_description(module)


if __name__ == '__main__':
    main()
