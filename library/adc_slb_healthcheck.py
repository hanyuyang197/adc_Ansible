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


def adc_list_healthchecks(module):
    """获取健康检查列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.list" % (
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
        module.fail_json(msg="获取健康检查列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取健康检查列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, healthchecks=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_healthcheck(module):
    """获取健康检查详情"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取健康检查详情需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.get" % (
        ip, authkey)

    # 构造请求数据
    hc_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(hc_data.keys()):
        if hc_data[key] is None or (isinstance(hc_data[key], str) and hc_data[key] == ""):
            del hc_data[key]

    # 转换为JSON格式
    post_data = json.dumps(hc_data)

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
        module.fail_json(msg="获取健康检查详情失败: %s" % str(e))

    # 对于获取详情操作，直接返回响应数据，不判断success
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取健康检查详情失败", response=parsed_data)
            else:
                module.exit_json(changed=False, healthcheck=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_healthcheck(module):
    """添加健康检查"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    hc_type = module.params['hc_type'] if 'hc_type' in module.params else "icmp"

    # 检查必需参数
    if 'name' not in module.params or not module.params['name']:
        module.fail_json(msg="添加健康检查需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.add" % (
        ip, authkey)

    # 构造健康检查数据 - 包含所有通用参数
    hc_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        hc_data["name"] = module.params["name"]
    if "type" in module.params and module.params["type"] is not None:
        hc_data["type"] = hc_type
    if "retry" in module.params and module.params["retry"] is not None:
        hc_data["retry"] = module.params['retry'] if 'retry' in module.params and module.params['retry'] is not None else 3
    if "interval" in module.params and module.params["interval"] is not None:
        hc_data["interval"] = module.params['interval'] if 'interval' in module.params and module.params['interval'] is not None else 5
    if "timeout" in module.params and module.params["timeout"] is not None:
        hc_data["timeout"] = module.params['timeout'] if 'timeout' in module.params and module.params['timeout'] is not None else 5
    if "up_check_cnt" in module.params and module.params["up_check_cnt"] is not None:
        hc_data["up_check_cnt"] = module.params['up_check_cnt'] if 'up_check_cnt' in module.params and module.params['up_check_cnt'] is not None else 1
    if "wait_all_retry" in module.params and module.params["wait_all_retry"] is not None:
        hc_data["wait_all_retry"] = module.params['wait_all_retry'] if 'wait_all_retry' in module.params and module.params['wait_all_retry'] is not None else 0

    # 只有当参数在YAML中明确定义时才添加到请求中
    if 'description' in module.params and module.params['description']:
        hc_data['description'] = module.params['description']
    if 'auto_disable' in module.params and module.params['auto_disable'] is not None:
        hc_data['auto_disable'] = module.params['auto_disable']
    if 'alias_ipv4_src' in module.params and module.params['alias_ipv4_src']:
        hc_data['alias_ipv4_src'] = module.params['alias_ipv4_src']
    if 'alias_ipv6_src' in module.params and module.params['alias_ipv6_src']:
        hc_data['alias_ipv6_src'] = module.params['alias_ipv6_src']
    if 'interface' in module.params and module.params['interface']:
        hc_data['interface'] = module.params['interface']
    if 'alias_ipv4' in module.params and module.params['alias_ipv4']:
        hc_data['alias_ipv4'] = module.params['alias_ipv4']
    if 'alias_ipv6' in module.params and module.params['alias_ipv6']:
        hc_data['alias_ipv6'] = module.params['alias_ipv6']
    if 'alias_port' in module.params and module.params['alias_port'] is not None:
        hc_data['alias_port'] = module.params['alias_port']
    if 'port' in module.params and module.params['port'] is not None:
        hc_data['port'] = module.params['port']
    if 'http_version' in module.params and module.params['http_version']:
        hc_data['http_version'] = module.params['http_version']

    # 根据健康检查类型添加特定参数
    if hc_type == "icmp":
        if 'mode' in module.params and module.params['mode']:
            hc_data['mode'] = module.params['mode']
        if 'icmp_alias_addr' in module.params and module.params['icmp_alias_addr']:
            hc_data['icmp_alias_addr'] = module.params['icmp_alias_addr']
    elif hc_type == "http" or hc_type == "https":
        if 'host' in module.params and module.params['host']:
            hc_data['host'] = module.params['host']
        if 'url' in module.params and module.params['url']:
            hc_data['url'] = module.params['url']
        if 'post_data' in module.params and module.params['post_data']:
            hc_data['post_data'] = module.params['post_data']
        if 'post_file' in module.params and module.params['post_file']:
            hc_data['post_file'] = module.params['post_file']
        if 'username' in module.params and module.params['username']:
            hc_data['username'] = module.params['username']
        if 'password' in module.params and module.params['password']:
            hc_data['password'] = module.params['password']
        if 'code' in module.params and module.params['code']:
            hc_data['code'] = module.params['code']
        if 'pattern' in module.params and module.params['pattern']:
            hc_data['pattern'] = module.params['pattern']
        if 'pattern_disable_str' in module.params and module.params['pattern_disable_str']:
            hc_data['pattern_disable_str'] = module.params['pattern_disable_str']
        if 'server_fail_code' in module.params and module.params['server_fail_code']:
            hc_data['server_fail_code'] = module.params['server_fail_code']
        if 'trans_mode' in module.params and module.params['trans_mode'] is not None:
            hc_data['trans_mode'] = module.params['trans_mode']
        if hc_type == "https" and 'sslver' in module.params and module.params['sslver']:
            hc_data['sslver'] = module.params['sslver']
    elif hc_type == "tcp" or hc_type == "udp":
        # TCP/UDP类型参数
        pass
    elif hc_type == "combo":
        if 'combo' in module.params and module.params['combo']:
            hc_data['combo'] = module.params['combo']

    # 转换为JSON格式
    post_data = json.dumps(hc_data)

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
        module.fail_json(msg="添加健康检查失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加健康检查", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_healthcheck(module):
    """编辑健康检查"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑健康检查需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.edit" % (
        ip, authkey)

    # 构造健康检查数据 - 包含所有通用参数
    hc_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(hc_data.keys()):
        if hc_data[key] is None or (isinstance(hc_data[key], str) and hc_data[key] == ""):
            del hc_data[key]

    # 只有当参数在YAML中明确定义时才添加到请求中
    if 'retry' in module.params and module.params['retry'] is not None:
        hc_data['retry'] = module.params['retry']
    if 'interval' in module.params and module.params['interval'] is not None:
        hc_data['interval'] = module.params['interval']
    if 'timeout' in module.params and module.params['timeout'] is not None:
        hc_data['timeout'] = module.params['timeout']
    if 'up_check_cnt' in module.params and module.params['up_check_cnt'] is not None:
        hc_data['up_check_cnt'] = module.params['up_check_cnt']
    if 'wait_all_retry' in module.params and module.params['wait_all_retry'] is not None:
        hc_data['wait_all_retry'] = module.params['wait_all_retry']
    if 'description' in module.params and module.params['description']:
        hc_data['description'] = module.params['description']
    if 'auto_disable' in module.params and module.params['auto_disable'] is not None:
        hc_data['auto_disable'] = module.params['auto_disable']
    if 'alias_ipv4_src' in module.params and module.params['alias_ipv4_src']:
        hc_data['alias_ipv4_src'] = module.params['alias_ipv4_src']
    if 'alias_ipv6_src' in module.params and module.params['alias_ipv6_src']:
        hc_data['alias_ipv6_src'] = module.params['alias_ipv6_src']
    if 'interface' in module.params and module.params['interface']:
        hc_data['interface'] = module.params['interface']
    if 'alias_ipv4' in module.params and module.params['alias_ipv4']:
        hc_data['alias_ipv4'] = module.params['alias_ipv4']
    if 'alias_ipv6' in module.params and module.params['alias_ipv6']:
        hc_data['alias_ipv6'] = module.params['alias_ipv6']
    if 'alias_port' in module.params and module.params['alias_port'] is not None:
        hc_data['alias_port'] = module.params['alias_port']
    if 'port' in module.params and module.params['port'] is not None:
        hc_data['port'] = module.params['port']
    if 'http_version' in module.params and module.params['http_version']:
        hc_data['http_version'] = module.params['http_version']
    if 'hc_type' in module.params and module.params['hc_type']:
        hc_data['type'] = module.params['hc_type']

    # 根据健康检查类型添加特定参数
    hc_type = module.params['hc_type'] if 'hc_type' in module.params else ""
    if hc_type == "icmp":
        if 'mode' in module.params and module.params['mode']:
            hc_data['mode'] = module.params['mode']
        if 'icmp_alias_addr' in module.params and module.params['icmp_alias_addr']:
            hc_data['icmp_alias_addr'] = module.params['icmp_alias_addr']
    elif hc_type == "http" or hc_type == "https":
        if 'host' in module.params and module.params['host']:
            hc_data['host'] = module.params['host']
        if 'url' in module.params and module.params['url']:
            hc_data['url'] = module.params['url']
        if 'post_data' in module.params and module.params['post_data']:
            hc_data['post_data'] = module.params['post_data']
        if 'post_file' in module.params and module.params['post_file']:
            hc_data['post_file'] = module.params['post_file']
        if 'username' in module.params and module.params['username']:
            hc_data['username'] = module.params['username']
        if 'password' in module.params and module.params['password']:
            hc_data['password'] = module.params['password']
        if 'code' in module.params and module.params['code']:
            hc_data['code'] = module.params['code']
        if 'pattern' in module.params and module.params['pattern']:
            hc_data['pattern'] = module.params['pattern']
        if 'pattern_disable_str' in module.params and module.params['pattern_disable_str']:
            hc_data['pattern_disable_str'] = module.params['pattern_disable_str']
        if 'server_fail_code' in module.params and module.params['server_fail_code']:
            hc_data['server_fail_code'] = module.params['server_fail_code']
        if 'trans_mode' in module.params and module.params['trans_mode'] is not None:
            hc_data['trans_mode'] = module.params['trans_mode']
        if hc_type == "https" and 'sslver' in module.params and module.params['sslver']:
            hc_data['sslver'] = module.params['sslver']
    elif hc_type == "combo":
        if 'combo' in module.params and module.params['combo']:
            hc_data['combo'] = module.params['combo']

    # 转换为JSON格式
    post_data = json.dumps(hc_data)

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
        module.fail_json(msg="编辑健康检查失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "编辑健康检查", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_healthcheck(module):
    """删除健康检查"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除健康检查需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.healthcheck.del" % (
        ip, authkey)

    # 构造健康检查数据
    hc_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(hc_data.keys()):
        if hc_data[key] is None or (isinstance(hc_data[key], str) and hc_data[key] == ""):
            del hc_data[key]

    # 转换为JSON格式
    post_data = json.dumps(hc_data)

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
        module.fail_json(msg="删除健康检查失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除健康检查", True)
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
                    'list_healthchecks', 'get_healthcheck', 'add_healthcheck', 'edit_healthcheck', 'delete_healthcheck']),
        # 健康检查通用参数
        name=dict(type='str', required=False),
        hc_type=dict(type='str', required=False, choices=[
            'icmp', 'http', 'https', 'tcp', 'udp', 'combo', 'arp', 'database', 'dns', 'ftp',
            'imap', 'ldap', 'ntp', 'pop3', 'radius', 'rtsp', 'sip', 'smtp', 'snmp']),
        retry=dict(type='int', required=False),
        interval=dict(type='int', required=False),
        timeout=dict(type='int', required=False),
        description=dict(type='str', required=False),
        auto_disable=dict(type='int', required=False),
        alias_ipv4_src=dict(type='str', required=False),
        alias_ipv6_src=dict(type='str', required=False),
        interface=dict(type='str', required=False),
        alias_ipv4=dict(type='str', required=False),
        alias_ipv6=dict(type='str', required=False),
        alias_port=dict(type='int', required=False),
        port=dict(type='int', required=False),
        up_check_cnt=dict(type='int', required=False),
        wait_all_retry=dict(type='int', required=False),
        http_version=dict(type='str', required=False),
        # ICMP类型参数
        mode=dict(type='str', required=False),
        icmp_alias_addr=dict(type='str', required=False),
        # HTTP/HTTPS类型参数
        host=dict(type='str', required=False),
        url=dict(type='str', required=False),
        post_data=dict(type='str', required=False),
        post_file=dict(type='str', required=False),
        username=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        code=dict(type='str', required=False),
        pattern=dict(type='str', required=False),
        pattern_disable_str=dict(type='str', required=False),
        server_fail_code=dict(type='str', required=False),
        trans_mode=dict(type='int', required=False),
        sslver=dict(type='str', required=False),
        # Combo类型参数
        combo=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
        # 获取action参数并确保它是字符串类型
    if 'action' in module.params and module.params['action'] is not None:
        action = str(module.params['action'])
    else:
        action = 

    if action == 'list_healthchecks':
        adc_list_healthchecks(module)
    elif action == 'get_healthcheck':
        adc_get_healthcheck(module)
    elif action == 'add_healthcheck':
        adc_add_healthcheck(module)
    elif action == 'edit_healthcheck':
        adc_edit_healthcheck(module)
    elif action == 'delete_healthcheck':
        adc_delete_healthcheck(module)


if __name__ == '__main__':
    main()
