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
#!/usr/bin/python
# -*- coding: utf-8 -*-

# ADC模块通用工具函数
# 用于处理参数构建等通用功能

import sys
try:
except ImportError:
    pass


def build_request_data(module, required_params=None, optional_params=None):
    """
    构建请求数据，只包含在YAML中明确指定的参数

    Args:
        module: Ansible模块实例
        required_params: 必需参数列表
        optional_params: 可选参数列表

    Returns:
        dict: 构建的请求数据
    """
    if required_params is None:
        required_params = []
    if optional_params is None:
        optional_params = []

    # 构建请求数据
    data = {}

    # 添加必需参数
    for param in required_params:
        if param in module.params and module.params[param] is not None:
            data[param] = module.params[param]
        else:
            # 必需参数缺失
            return None, "必需参数 '%s' 未提供或为空" % param

    # 添加可选参数（只添加在YAML中明确指定且非None的参数）
    for param in optional_params:
        if param in module.params and module.params[param] is not None:
            # 特殊处理列表类型参数
            if isinstance(module.params[param], list) and len(module.params[param]) == 0:
                # 空列表不添加
                continue
            data[param] = module.params[param]

    return data, None


def build_nested_request_data(module, structure):
    """
    构建嵌套结构的请求数据

    Args:
        module: Ansible模块实例
        structure: 数据结构定义，格式为 {'parent_key': {'required': [...], 'optional': [...]}}

    Returns:
        dict: 构建的请求数据
    """
    data = {}

    for parent_key, params_def in structure.items():
        required_params = params_def.get('required', [])
        optional_params = params_def.get('optional', [])

        # 构建子数据
        sub_data = {}
        valid = True
        error_msg = ""

        # 添加必需参数
        for param in required_params:
            if param in module.params and module.params[param] is not None:
                sub_data[param] = module.params[param]
            else:
                valid = False
                error_msg = "必需参数 '%s' 未提供或为空" % param
                break

        if not valid:
            return None, error_msg

        # 添加可选参数（只添加在YAML中明确指定且非None的参数）
        for param in optional_params:
            if param in module.params and module.params[param] is not None:
                # 特殊处理列表类型参数
                if isinstance(module.params[param], list) and len(module.params[param]) == 0:
                    # 空列表不添加
                    continue
                sub_data[param] = module.params[param]

        # 只有当子数据不为空时才添加到父数据中
        if sub_data:
            data[parent_key] = sub_data

    return data, None


def send_adc_request(url, data=None, method='GET'):
    """
    发送ADC API请求

    Args:
        url: 请求URL
        data: 请求数据
        method: HTTP方法

    Returns:
        dict: 响应数据
    """
    try:
        if sys.version_info[0] >= 3:
            # Python 3
                        if method == 'POST' and data:
                data_json = json.dumps(data)
                data_bytes = data_json.encode('utf-8')
                req = urllib_request.Request(url, data=data_bytes)
                req.add_header('Content-Type', 'application/json')
            else:
                req = urllib_request.Request(url)

            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        if method == 'POST' and data:
                data_json = json.dumps(data)
                req = urllib_request.Request(url, data=data_json)
                req.add_header('Content-Type', 'application/json')
            else:
                req = urllib_request.Request(url)

            response = urllib_request.urlopen(req)
            response_data = response.read()

        return json.loads(response_data)
    except Exception as e:
        return {'status': False, 'msg': str(e)}


def format_adc_response_for_ansible(response_data, operation_name="", changed_flag=False):
    """
    格式化ADC响应数据以适配Ansible

    Args:
        response_data: 响应数据（字符串或字典）
        operation_name: 操作名称
        changed_flag: 是否标记为已更改

    Returns:
        tuple: (success, result_dict)
    """
    try:
        # 如果是字符串则解析为JSON
        if isinstance(response_data, str):
            parsed_data = json.loads(response_data)
        else:
            parsed_data = response_data

        # 检查响应格式
        if isinstance(parsed_data, dict):
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                return False, {
                    'msg': "%s失败: %s" % (operation_name, parsed_data['errmsg']),
                    'response': parsed_data
                }
            elif 'status' in parsed_data and parsed_data['status'] is False:
                return False, {
                    'msg': "%s失败" % operation_name,
                    'response': parsed_data
                }
            else:
                # 成功响应
                result = {
                    'changed': changed_flag,
                    'response': parsed_data
                }
                # 如果响应中有result字段，则也添加到结果中
                if 'result' in parsed_data:
                    result['result'] = parsed_data['result']
                return True, result
        else:
            # 非字典响应，直接返回
            return True, {
                'changed': changed_flag,
                'response': parsed_data
            }

    except Exception as e:
        return False, {
            'msg': "解析%s响应失败: %s" % (operation_name, str(e)),
            'raw_response': response_data
        }
