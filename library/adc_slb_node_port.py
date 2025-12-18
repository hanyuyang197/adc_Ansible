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


def adc_add_node_port(module):
    """添加节点端口"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    
    # 检查必需参数
    if not name:
        module.fail_json(msg="添加节点端口需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.add" % (ip, authkey)

    # 构造端口数据
    port_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "port" in module.params and module.params["port"] is not None:
        acl_data["port"] = {
            "port_number": module.params['port_number'] if 'port_number' in module.params else 80,
            "protocol": module.params['protocol'] if 'protocol' in module.params else 0,
            "status": module.params['status'] if 'status' in module.params else 1,
            "weight": module.params['weight'] if 'weight' in module.params else 1,
            "conn_limit": module.params['conn_limit'] if 'conn_limit' in module.params else 8000000,
            "graceful_time": module.params['graceful_time'] if 'graceful_time' in module.params else 0,
            "graceful_delete": module.params['graceful_delete'] if 'graceful_delete' in module.params else 0,
            "graceful_disable": module.params['graceful_disable'] if 'graceful_disable' in module.params else 0,
            "graceful_persist": module.params['graceful_persist'] if 'graceful_persist' in module.params else 0,
            "phm_profile": module.params['phm_profile'] if 'phm_profile' in module.params else "",
            "healthcheck": module.params['healthcheck'] if 'healthcheck' in module.params else "",
            "nat_strategy": module.params['nat_strategy'] if 'nat_strategy' in module.params else ""
       
    }

    # 处理可选参数upnum
    if 'upnum' in module.params and module.params['upnum'] is not None:
        port_data['port']['upnum'] = module.params['upnum']

    # 转换为JSON格式
    post_data = json.dumps(port_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
                        post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="添加节点端口失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(response_data, "添加节点端口", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_edit_node_port(module):
    """编辑节点端口"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    
    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑节点端口需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.edit" % (ip, authkey)

    # 构造端口数据
    port_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "port" in module.params and module.params["port"] is not None:
        acl_data["port"] = {
            "port_number": module.params['port_number'] if 'port_number' in module.params else 80,
            "protocol": module.params['protocol'] if 'protocol' in module.params else 0,
            "status": module.params['status'] if 'status' in module.params else 1,
            "weight": module.params['weight'] if 'weight' in module.params else 1,
            "conn_limit": module.params['conn_limit'] if 'conn_limit' in module.params else 8000000,
            "graceful_time": module.params['graceful_time'] if 'graceful_time' in module.params else 0,
            "graceful_delete": module.params['graceful_delete'] if 'graceful_delete' in module.params else 0,
            "graceful_disable": module.params['graceful_disable'] if 'graceful_disable' in module.params else 0,
            "graceful_persist": module.params['graceful_persist'] if 'graceful_persist' in module.params else 0,
            "phm_profile": module.params['phm_profile'] if 'phm_profile' in module.params else "",
            "healthcheck": module.params['healthcheck'] if 'healthcheck' in module.params else "",
            "nat_strategy": module.params['nat_strategy'] if 'nat_strategy' in module.params else ""
       
    }

    # 处理可选参数upnum
    if 'upnum' in module.params and module.params['upnum'] is not None:
        port_data['port']['upnum'] = module.params['upnum']

    # 转换为JSON格式
    post_data = json.dumps(port_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
                        post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="编辑节点端口失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(response_data, "编辑节点端口", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_delete_node_port(module):
    """删除节点端口"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    port_number = module.params['port_number'] if 'port_number' in module.params else 80
    protocol = module.params['protocol'] if 'protocol' in module.params else 0
    
    # 检查必需参数
    if not name:
        module.fail_json(msg="删除节点端口需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.del" % (ip, authkey)

    # 构造端口数据
    port_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "port" in module.params and module.params["port"] is not None:
        acl_data["port"] = {
            "port_number": port_number,
            "protocol": protocol
       
    }

    # 转换为JSON格式
    post_data = json.dumps(port_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
                        post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="删除节点端口失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(response_data, "删除节点端口", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_onoff_node_port(module):
    """启用/禁用节点端口"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name'] if 'name' in module.params else ""
    port_number = module.params['port_number'] if 'port_number' in module.params else 80
    protocol = module.params['protocol'] if 'protocol' in module.params else 0
    status = module.params['status'] if 'status' in module.params else 1
    
    # 检查必需参数
    if not name:
        module.fail_json(msg="启用/禁用节点端口需要提供name参数")

    # 构造请求URL (使用兼容Python 2.7的字符串格式化)
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.node.port.onoff" % (ip, authkey)

    # 构造端口数据
    port_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "port" in module.params and module.params["port"] is not None:
        acl_data["port"] = {
            "port_number": port_number,
            "protocol": protocol,
            "status": status
       
    }

    # 转换为JSON格式
    post_data = json.dumps(port_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
                        post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        req = urllib_request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="启用/禁用节点端口失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(response_data, "启用/禁用节点端口", True)
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
            'add_node_port', 'edit_node_port', 'delete_node_port', 'onoff_node_port']),
        # 节点参数
        name=dict(type='str', required=True),
        # 端口参数
        port_number=dict(type='int', required=False),
        protocol=dict(type='int', required=False),
        status=dict(type='int', required=False),
        weight=dict(type='int', required=False),
        conn_limit=dict(type='int', required=False),
        graceful_time=dict(type='int', required=False),
        graceful_delete=dict(type='int', required=False),
        graceful_disable=dict(type='int', required=False),
        graceful_persist=dict(type='int', required=False),
        phm_profile=dict(type='str', required=False),
        healthcheck=dict(type='str', required=False),
        upnum=dict(type='int', required=False),
        nat_strategy=dict(type='str', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']
    
    if action == 'add_node_port':
        adc_add_node_port(module)
    elif action == 'edit_node_port':
        adc_edit_node_port(module)
    elif action == 'delete_node_port':
        adc_delete_node_port(module)
    elif action == 'onoff_node_port':
        adc_onoff_node_port(module)


if __name__ == '__main__':
    main()