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


def adc_add_snmp_community(module):
    """添加SNMP团体字"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    community = module.params['community']
    host = module.params['host']

    # 检查必需参数
    if not community or not host:
        module.fail_json(msg="添加SNMP团体字需要提供community和host参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.comm.item.add" % (
        ip, authkey)

    # 构造团体字数据
    community_data = {}
    # 只添加明确指定的参数
    if "community" in module.params and module.params["community"] is not None:
        acl_data["community"] = module.params["community"]
    if "host" in module.params and module.params["host"] is not None:
        acl_data["host"] = host
   

    # 转换为JSON格式
    post_data = json.dumps(community_data)

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
        module.fail_json(msg="添加SNMP团体字失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加SNMP团体字", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_snmp_communities(module):
    """获取SNMP团体字列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.comm.item.list" % (
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
        module.fail_json(msg="获取SNMP团体字列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMP团体字列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, communities=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_snmp_community(module):
    """删除SNMP团体字"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    community = module.params['community']
    host = module.params['host']

    # 检查必需参数
    if not community or not host:
        module.fail_json(msg="删除SNMP团体字需要提供community和host参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.comm.item.del" % (
        ip, authkey)

    # 构造团体字数据
    community_data = {}
    # 只添加明确指定的参数
    if "community" in module.params and module.params["community"] is not None:
        acl_data["community"] = module.params["community"]
    if "host" in module.params and module.params["host"] is not None:
        acl_data["host"] = host
   

    # 转换为JSON格式
    post_data = json.dumps(community_data)

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
        module.fail_json(msg="删除SNMP团体字失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除SNMP团体字", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_set_snmp_server(module):
    """设置SNMP服务配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.set" % (
        ip, authkey)

    # 构造SNMP服务配置数据
    server_data = {}

    # 添加可选参数
    if 'status' in module.params and module.params['status'] is not None:
        server_data['status'] = module.params['status']
    if 'port' in module.params and module.params['port'] is not None:
        server_data['port'] = module.params['port']
    if 'contact' in module.params and module.params['contact'] is not None:
        server_data['contact'] = module.params['contact']
    if 'location' in module.params and module.params['location'] is not None:
        server_data['location'] = module.params['location']

    # 转换为JSON格式
    post_data = json.dumps(server_data)

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
        module.fail_json(msg="设置SNMP服务配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置SNMP服务配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_snmp_server(module):
    """获取SNMP服务配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.server.get" % (
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
        module.fail_json(msg="获取SNMP服务配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMP服务配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, server_config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_add_snmp_trap(module):
    """添加SNMP TRAP"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    community = module.params['community']
    host = module.params['host']

    # 检查必需参数
    if not community or not host:
        module.fail_json(msg="添加SNMP TRAP需要提供community和host参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.trap.item.add" % (
        ip, authkey)

    # 构造TRAP数据
    trap_data = {}
    # 只添加明确指定的参数
    if "community" in module.params and module.params["community"] is not None:
        acl_data["community"] = module.params["community"]
    if "host" in module.params and module.params["host"] is not None:
        acl_data["host"] = host
   

    # 添加可选参数
    if 'port' in module.params and module.params['port'] is not None:
        trap_data['port'] = module.params['port']
    if 'version' in module.params and module.params['version'] is not None:
        trap_data['version'] = module.params['version']

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
        module.fail_json(msg="添加SNMP TRAP失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "添加SNMP TRAP", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_list_snmp_traps(module):
    """获取SNMP TRAP列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.trap.item.list" % (
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
        module.fail_json(msg="获取SNMP TRAP列表失败: %s" % str(e))

    # 对于获取列表操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMP TRAP列表失败", response=parsed_data)
            else:
                module.exit_json(changed=False, traps=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_snmp_trap(module):
    """删除SNMP TRAP"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    community = module.params['community']
    host = module.params['host']

    # 检查必需参数
    if not community or not host:
        module.fail_json(msg="删除SNMP TRAP需要提供community和host参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.trap.item.del" % (
        ip, authkey)

    # 构造TRAP数据
    trap_data = {}
    # 只添加明确指定的参数
    if "community" in module.params and module.params["community"] is not None:
        acl_data["community"] = module.params["community"]
    if "host" in module.params and module.params["host"] is not None:
        acl_data["host"] = host
   

    # 添加可选参数
    if 'version' in module.params and module.params['version'] is not None:
        trap_data['version'] = module.params['version']

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
        module.fail_json(msg="删除SNMP TRAP失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "删除SNMP TRAP", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_set_snmp_trap(module):
    """设置SNMP TRAP配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.trap.set" % (
        ip, authkey)

    # 构造TRAP配置数据
    trap_data = {}

    # 添加可选参数
    if 'status' in module.params and module.params['status'] is not None:
        trap_data['status'] = module.params['status']

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
        module.fail_json(msg="设置SNMP TRAP配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置SNMP TRAP配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_snmp_trap(module):
    """获取SNMP TRAP配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=snmp.trap.get" % (
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
        module.fail_json(msg="获取SNMP TRAP配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取SNMP TRAP配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, trap_config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'add_community', 'list_communities', 'delete_community',
            'set_server', 'get_server',
            'add_trap', 'list_traps', 'delete_trap',
            'set_trap', 'get_trap']),
        # SNMP团体字参数
        community=dict(type='str', required=False),
        host=dict(type='str', required=False),
        # SNMP服务配置参数
        status=dict(type='int', required=False),
        port=dict(type='int', required=False),
        contact=dict(type='str', required=False),
        location=dict(type='str', required=False),
        # SNMP TRAP参数
        version=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'add_community':
        adc_add_snmp_community(module)
    elif action == 'list_communities':
        adc_list_snmp_communities(module)
    elif action == 'delete_community':
        adc_delete_snmp_community(module)
    elif action == 'set_server':
        adc_set_snmp_server(module)
    elif action == 'get_server':
        adc_get_snmp_server(module)
    elif action == 'add_trap':
        adc_add_snmp_trap(module)
    elif action == 'list_traps':
        adc_list_snmp_traps(module)
    elif action == 'delete_trap':
        adc_delete_snmp_trap(module)
    elif action == 'set_trap':
        adc_set_snmp_trap(module)
    elif action == 'get_trap':
        adc_get_snmp_trap(module)


if __name__ == '__main__':
    main()
