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


def adc_list_acls(module):
    """获取IPv4扩展访问列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.ext.list" % (
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
        module.fail_json(msg="获取IPv4扩展访问列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv4扩展访问列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, acls=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_acl(module):
    """获取IPv4扩展访问列表详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="获取IPv4扩展访问列表详情需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.ext.get" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {}
    # 只添加明确指定的参数
    if "id" in module.params and module.params["id"] is not None:
        acl_data["id"] = module.params["id"]

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="获取IPv4扩展访问列表详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取IPv4扩展访问列表详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, acl=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_acl_item(module):
    """添加IPv4扩展访问列表条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""
    sequence = module.params['sequence'] if 'sequence' in module.params else ""

    # 检查必需参数
    if not id or not sequence:
        module.fail_json(msg="添加IPv4扩展访问列表条目需要提供id和sequence参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.ext.item.add" % (
        ip, authkey)

    # 构造ACL条目数据
    acl_data = {}
    # 只添加明确指定的参数
    if "id" in module.params and module.params["id"] is not None:
        acl_data["id"] = module.params["id"]
    if "sequence" in module.params and module.params["sequence"] is not None:
        acl_data["sequence"] = sequence
    if "acl_action" in module.params and module.params["acl_action"] is not None:
        acl_data["acl_action"] = module.params["acl_action"]
    if "protocol" in module.params and module.params["protocol"] is not None:
        acl_data["protocol"] = module.params["protocol"]
    if "src_ip" in module.params and module.params["src_ip"] is not None:
        acl_data["src_ip"] = module.params["src_ip"]
    if "src_mask" in module.params and module.params["src_mask"] is not None:
        acl_data["src_mask"] = module.params["src_mask"]
    if "dst_ip" in module.params and module.params["dst_ip"] is not None:
        acl_data["dst_ip"] = module.params["dst_ip"]
    if "dst_mask" in module.params and module.params["dst_mask"] is not None:
        acl_data["dst_mask"] = module.params["dst_mask"]

    # 添加可选参数
    if 'icmp_type' in module.params and module.params['icmp_type'] is not None:
        acl_data['icmp_type'] = module.params['icmp_type']
    if 'icmp_code' in module.params and module.params['icmp_code'] is not None:
        acl_data['icmp_code'] = module.params['icmp_code']
    if 'src_port_min' in module.params and module.params['src_port_min'] is not None:
        acl_data['src_port_min'] = module.params['src_port_min']
    if 'src_port_max' in module.params and module.params['src_port_max'] is not None:
        acl_data['src_port_max'] = module.params['src_port_max']
    if 'dst_port_min' in module.params and module.params['dst_port_min'] is not None:
        acl_data['dst_port_min'] = module.params['dst_port_min']
    if 'dst_port_max' in module.params and module.params['dst_port_max'] is not None:
        acl_data['dst_port_max'] = module.params['dst_port_max']
    if 'ip_fragments' in module.params and module.params['ip_fragments'] is not None:
        acl_data['ip_fragments'] = module.params['ip_fragments']
    if 'vlan_id' in module.params and module.params['vlan_id'] is not None:
        acl_data['vlan_id'] = module.params['vlan_id']
    if 'dscp' in module.params and module.params['dscp'] is not None:
        acl_data['dscp'] = module.params['dscp']
    if 'tcp_established' in module.params and module.params['tcp_established'] is not None:
        acl_data['tcp_established'] = module.params['tcp_established']
    if 'description' in module.params and module.params['description'] is not None:
        acl_data['description'] = module.params['description']
    if 'timerange' in module.params and module.params['timerange'] is not None:
        acl_data['timerange'] = module.params['timerange']

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="添加IPv4扩展访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加IPv4扩展访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_acl_item(module):
    """编辑IPv4扩展访问列表条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""
    sequence = module.params['sequence'] if 'sequence' in module.params else ""

    # 检查必需参数
    if not id or not sequence:
        module.fail_json(msg="编辑IPv4扩展访问列表条目需要提供id和sequence参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.ext.item.edit" % (
        ip, authkey)

    # 构造ACL条目数据
    acl_data = {}
    # 只添加明确指定的参数
    if "id" in module.params and module.params["id"] is not None:
        acl_data["id"] = module.params["id"]
    if "sequence" in module.params and module.params["sequence"] is not None:
        acl_data["sequence"] = sequence

    # 添加可选参数
    if 'acl_action' in module.params and module.params['acl_action'] is not None:
        acl_data['acl_action'] = module.params['acl_action']
    if 'protocol' in module.params and module.params['protocol'] is not None:
        acl_data['protocol'] = module.params['protocol']
    if 'src_ip' in module.params and module.params['src_ip'] is not None:
        acl_data['src_ip'] = module.params['src_ip']
    if 'src_mask' in module.params and module.params['src_mask'] is not None:
        acl_data['src_mask'] = module.params['src_mask']
    if 'dst_ip' in module.params and module.params['dst_ip'] is not None:
        acl_data['dst_ip'] = module.params['dst_ip']
    if 'dst_mask' in module.params and module.params['dst_mask'] is not None:
        acl_data['dst_mask'] = module.params['dst_mask']
    if 'icmp_type' in module.params and module.params['icmp_type'] is not None:
        acl_data['icmp_type'] = module.params['icmp_type']
    if 'icmp_code' in module.params and module.params['icmp_code'] is not None:
        acl_data['icmp_code'] = module.params['icmp_code']
    if 'src_port_min' in module.params and module.params['src_port_min'] is not None:
        acl_data['src_port_min'] = module.params['src_port_min']
    if 'src_port_max' in module.params and module.params['src_port_max'] is not None:
        acl_data['src_port_max'] = module.params['src_port_max']
    if 'dst_port_min' in module.params and module.params['dst_port_min'] is not None:
        acl_data['dst_port_min'] = module.params['dst_port_min']
    if 'dst_port_max' in module.params and module.params['dst_port_max'] is not None:
        acl_data['dst_port_max'] = module.params['dst_port_max']
    if 'ip_fragments' in module.params and module.params['ip_fragments'] is not None:
        acl_data['ip_fragments'] = module.params['ip_fragments']
    if 'vlan_id' in module.params and module.params['vlan_id'] is not None:
        acl_data['vlan_id'] = module.params['vlan_id']
    if 'dscp' in module.params and module.params['dscp'] is not None:
        acl_data['dscp'] = module.params['dscp']
    if 'tcp_established' in module.params and module.params['tcp_established'] is not None:
        acl_data['tcp_established'] = module.params['tcp_established']
    if 'description' in module.params and module.params['description'] is not None:
        acl_data['description'] = module.params['description']
    if 'timerange' in module.params and module.params['timerange'] is not None:
        acl_data['timerange'] = module.params['timerange']

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="编辑IPv4扩展访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑IPv4扩展访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_acl_item(module):
    """删除IPv4扩展访问列表条目"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="删除IPv4扩展访问列表条目需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.ext.item.del" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {}
    # 只添加明确指定的参数
    if "id" in module.params and module.params["id"] is not None:
        acl_data["id"] = module.params["id"]

    # 如果提供了sequence参数，则添加到请求数据中
    if 'sequence' in module.params and module.params['sequence'] is not None:
        acl_data['sequence'] = module.params['sequence']

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="删除IPv4扩展访问列表条目失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除IPv4扩展访问列表条目", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_set_acl_description(module):
    """设置IPv4扩展访问列表描述"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    id = module.params['id'] if 'id' in module.params else ""
    description = module.params['description'] if 'description' in module.params else ""

    # 检查必需参数
    if not id:
        module.fail_json(msg="设置IPv4扩展访问列表描述需要提供id参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=acl.ipv4.ext.desc.set" % (
        ip, authkey)

    # 构造请求数据
    acl_data = {}
    # 只添加明确指定的参数
    if "id" in module.params and module.params["id"] is not None:
        acl_data["id"] = module.params["id"]
    if "description" in module.params and module.params["description"] is not None:
        acl_data["description"] = description

    # 转换为JSON格式
    post_data = json.dumps(acl_data)

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
        module.fail_json(msg="设置IPv4扩展访问列表描述失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置IPv4扩展访问列表描述", True)
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
            'list_acls', 'get_acl', 'add_acl_item', 'edit_acl_item', 'delete_acl_item', 'set_acl_description']),
        # ACL参数
        id=dict(type='int', required=False),
        sequence=dict(type='int', required=False),
        acl_action=dict(type='int', required=False),
        protocol=dict(type='int', required=False),
        src_ip=dict(type='str', required=False),
        src_mask=dict(type='str', required=False),
        dst_ip=dict(type='str', required=False),
        dst_mask=dict(type='str', required=False),
        icmp_type=dict(type='int', required=False),
        icmp_code=dict(type='int', required=False),
        src_port_min=dict(type='int', required=False),
        src_port_max=dict(type='int', required=False),
        dst_port_min=dict(type='int', required=False),
        dst_port_max=dict(type='int', required=False),
        ip_fragments=dict(type='int', required=False),
        vlan_id=dict(type='int', required=False),
        dscp=dict(type='int', required=False),
        tcp_established=dict(type='int', required=False),
        description=dict(type='str', required=False),
        timerange=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'list_acls':
        adc_list_acls(module)
    elif action == 'get_acl':
        adc_get_acl(module)
    elif action == 'add_acl_item':
        adc_add_acl_item(module)
    elif action == 'edit_acl_item':
        adc_edit_acl_item(module)
    elif action == 'delete_acl_item':
        adc_delete_acl_item(module)
    elif action == 'set_acl_description':
        adc_set_acl_description(module)


if __name__ == '__main__':
    main()
