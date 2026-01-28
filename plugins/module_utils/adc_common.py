from __future__ import absolute_import, division, print_function
# -*- coding: utf-8 -*-
"""
ADC 通用工具函数
提供常用的 ADC 操作函数，供所有模块使用
"""

import json
import sys
__metaclass__ = type


def json_loads_preserve_order(json_str):
    """
    保持字段顺序的 JSON 解析函数

    Python 3.7+ 的 dict 默认保持插入顺序，可以直接使用
    Python 2 使用 OrderedDict

    Args:
        json_str: JSON 格式的字符串

    Returns:
        dict/list: 解析后的数据，保持原始字段顺序
    """
    try:
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 7:
            # Python 3.7+ dict 保持插入顺序
            return json.loads(json_str)
        else:
            # Python 2 或 Python 3.6 及以下，使用 OrderedDict
            try:
                from collections import OrderedDict
                return json.loads(json_str, object_pairs_hook=OrderedDict)
            except ImportError:
                return json.loads(json_str)
    except (ValueError, TypeError) as e:
        raise ValueError("JSON解析失败: %s" % str(e))


def json_dumps_preserve_order(obj):
    """
    保持字段顺序的 JSON 序列化函数

    Args:
        obj: 要序列化的对象

    Returns:
        str: JSON 格式的字符串
    """
    try:
        # ensure_ascii=False 保留中文等非ASCII字符
        # sort_keys=False 保持字段顺序（Python 3.7+）
        return json.dumps(obj, ensure_ascii=False, sort_keys=False)
    except (ValueError, TypeError) as e:
        raise ValueError("JSON序列化失败: %s" % str(e))


def send_request(url, post_data=None):
    """发送HTTP请求的通用函数"""
    response_data = ""
    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            if post_data:
                post_data = post_data.encode('utf-8')
                req = urllib_request.Request(url, data=post_data, method='POST', headers={
                                             'Content-Type': 'application/json'})
            else:
                req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            if post_data:
                post_data = post_data.encode('utf-8')
                req = urllib_request.Request(url, data=post_data, headers={
                                             'Content-Type': 'application/json'})
                req.get_method = lambda: 'POST'
            else:
                req = urllib_request.Request(url)
                req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        raise Exception(str(e))

    # 直接返回响应内容，不尝试解析JSON
    return response_data


def make_adc_request(module, url, data=None, method='GET', headers=None):
    """
    发送 ADC 请求的通用函数

    Args:
        module: AnsibleModule 实例
        url: 请求 URL
        data: 请求数据
        method: HTTP 方法
        headers: 请求头

    Returns:
        dict: 响应数据
    """
    import json
    import ssl
    from ansible.module_utils.urls import open_url
    from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
    from ansible.module_utils.six.moves.urllib.parse import urlencode

    if headers is None:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Ansible-ADC-Module/1.0'
        }

    try:
        # 处理 SSL 验证
        validate_certs = module.params.get('validate_certs', True)

        response = open_url(
            url,
            data=data,
            method=method,
            headers=headers,
            validate_certs=validate_certs,
            timeout=module.params.get('timeout', 30)
        )

        response_data = response.read().decode('utf-8')
        if response_data:
            return json.loads(response_data)
        return {}

    except HTTPError as e:
        error_msg = 'HTTP Error: %s' % str(e)
        module.fail_json(msg=error_msg, status=e.code)
    except URLError as e:
        error_msg = 'URL Error: %s' % str(e)
        module.fail_json(msg=error_msg)
    except Exception as e:
        error_msg = 'Error: %s' % str(e)
        module.fail_json(msg=error_msg)


def format_adc_response(response, action=None):
    """
    格式化 ADC 响应数据

    Args:
        response: 原始响应数据
        action: 操作类型

    Returns:
        dict: 格式化后的响应
    """
    if isinstance(response, dict):
        return {
            'success': True,
            'changed': True,
            'response': response,
            'action': action
        }
    else:
        return {
            'success': True,
            'changed': True,
            'response': response,
            'action': action
        }


def check_adc_auth(module, ip, authkey):
    """
    检查 ADC 认证是否有效

    Args:
        module: AnsibleModule 实例
        ip: ADC IP 地址
        authkey: 认证密钥

    Returns:
        bool: 认证是否有效
    """
    try:
        # 发送测试请求
        test_url = "https://{0}/api/test_auth".format(ip)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Auth-Key': authkey
        }

        response = make_adc_request(
            module, test_url, headers=headers, method='GET')
        return True
    except Exception:
        return False


def handle_adc_error(module, error_msg, error_code=None):
    """
    统一处理 ADC 错误

    Args:
        module: AnsibleModule 实例
        error_msg: 错误消息
        error_code: 错误代码
    """
    module.fail_json(
        msg='ADC Error: %s' % error_msg,
        error_code=error_code,
        success=False
    )


def build_adc_params(module, exclude_params=None):
    """
    从模块参数构建 ADC 请求参数

    Args:
        module: AnsibleModule 实例
        exclude_params: 要排除的参数列表

    Returns:
        dict: 请求参数
    """
    if exclude_params is None:
        exclude_params = ['ip', 'authkey', 'action',
                          'use_https', 'validate_certs', 'timeout']

    params = {}
    for key, value in module.params.items():
        if key not in exclude_params and value is not None:
            params[key] = value

    return params


def validate_adc_params(module, required_params):
    """
    验证必需的 ADC 参数

    Args:
        module: AnsibleModule 实例
        required_params: 必需参数列表

    Raises:
        AnsibleModule.fail_json: 如果缺少必需参数
    """
    missing_params = []
    for param in required_params:
        if module.params.get(param) is None:
            missing_params.append(param)

    if missing_params:
        module.fail_json(msg='Missing required parameters: %s' %
                         ', '.join(missing_params))


def adc_result_check(result):
    """
    检查 ADC 操作结果

    Args:
        result: ADC 操作结果

    Returns:
        bool: 操作是否成功
    """
    if isinstance(result, dict):
        # 检查常见的成功标识
        if result.get('status') == 'success' or result.get('code') == 0:
            return True
        if result.get('result') == 'success' or result.get('success') is True:
            return True
    return False


def adc_format_output(module, result, changed=True):
    """
    格式化 ADC 操作输出

    Args:
        module: AnsibleModule 实例
        result: 操作结果
        changed: 是否有变更

    Returns:
        dict: 格式化后的输出
    """
    success = adc_result_check(result)

    output = {
        'success': success,
        'changed': changed,
        'result': result
    }

    if not success:
        output['msg'] = 'Operation failed'

    return output


def get_adc_session(module, ip, username, password):
    """
    获取 ADC 会话信息

    Args:
        module: AnsibleModule 实例
        ip: ADC IP 地址
        username: 用户名
        password: 密码

    Returns:
        str: 认证密钥
    """
    import json
    from ansible.module_utils.urls import open_url
    from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

    login_url = "https://{0}/api/login".format(ip)
    login_data = {
        'username': username,
        'password': password
    }

    try:
        validate_certs = module.params.get('validate_certs', True)
        response = open_url(
            login_url,
            method='POST',
            data=json.dumps(login_data),
            headers={'Content-Type': 'application/json'},
            validate_certs=validate_certs
        )

        response_data = response.read().decode('utf-8')
        result = json.loads(response_data)

        if result.get('success'):
            return result.get('authkey')
        else:
            module.fail_json(msg='Login failed: %s' %
                             result.get('msg', 'Unknown error'))

    except HTTPError as e:
        module.fail_json(msg='Login HTTP Error: %s' % str(e))
    except URLError as e:
        module.fail_json(msg='Login URL Error: %s' % str(e))
    except Exception as e:
        module.fail_json(msg='Login Error: %s' % str(e))


def adc_logout(module, ip, authkey):
    """
    登出 ADC 会话

    Args:
        module: AnsibleModule 实例
        ip: ADC IP 地址
        authkey: 认证密钥

    Returns:
        bool: 登出是否成功
    """
    import json
    from ansible.module_utils.urls import open_url
    from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

    logout_url = "https://{0}/api/logout".format(ip)
    headers = {
        'Content-Type': 'application/json',
        'Auth-Key': authkey
    }

    try:
        validate_certs = module.params.get('validate_certs', True)
        response = open_url(
            logout_url,
            method='POST',
            headers=headers,
            validate_certs=validate_certs
        )

        response_data = response.read().decode('utf-8')
        result = json.loads(response_data)

        return result.get('success', False)

    except Exception:
        return False  # 即使出错也返回 True，因为可能是会话已过期


def build_params_with_optional(module, optional_params, exclude_list=None):
    """
    构建参数字典，只包含非空的可选参数

    Args:
        module: AnsibleModule 实例
        optional_params: 可选参数名称列表
        exclude_list: 额外排除的参数列表

    Returns:
        dict: 包含非空参数的字典
    """
    if exclude_list is None:
        exclude_list = []

    params = {}
    for param in optional_params:
        if param not in exclude_list and module.params.get(param) is not None:
            params[param] = module.params[param]

    return params


def make_http_request(module, url, method='GET', data=None, headers=None, use_https=True, validate_certs=True):
    """
    通用 HTTP 请求函数，处理 Python 2/3 兼容性

    Args:
        module: AnsibleModule 实例
        url: 请求 URL
        method: HTTP 方法
        data: 请求数据
        headers: 请求头
        use_https: 是否使用 HTTPS
        validate_certs: 是否验证证书

    Returns:
        dict: 响应数据
    """
    import json
    import ssl
    from ansible.module_utils.urls import open_url
    from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Ansible-ADC-Module/1.0'
        }

    try:
        # 处理数据
        post_data = None
        if data:
            post_data = json.dumps(data).encode('utf-8') if isinstance(
                data, dict) else data.encode('utf-8') if isinstance(data, str) else data

        # 发送请求
        response = open_url(
            url,
            data=post_data,
            method=method,
            headers=headers,
            validate_certs=validate_certs,
            timeout=module.params.get('timeout', 30)
        )

        response_data = response.read().decode('utf-8')
        if response_data:
            return json.loads(response_data) if response_data.strip().startswith('{') else response_data
        return {}

    except HTTPError as e:
        error_msg = 'HTTP Error: %s' % str(e)
        module.fail_json(msg=error_msg, status=e.code)
    except URLError as e:
        error_msg = 'URL Error: %s' % str(e)
        module.fail_json(msg=error_msg)
    except Exception as e:
        error_msg = 'Request Error: %s' % str(e)
        module.fail_json(msg=error_msg)


def get_param_if_exists(module, param_name, default=None):
    """
    获取参数值，如果不存在则返回默认值

    Args:
        module: AnsibleModule 实例
        param_name: 参数名
        default: 默认值

    Returns:
        参数值或默认值
    """
    value = module.params.get(param_name)
    return value if value is not None else default


def create_adc_module_args(base_args=None):
    """
    创建 ADC 模块的通用参数定义

    Args:
        base_args: 基础参数字典

    Returns:
        dict: 包含通用参数的参数字典
    """
    if base_args is None:
        base_args = {}

    # 添加通用参数
    common_args = {
        'ip': dict(type='str', required=True),
        'authkey': dict(type='str', required=False, no_log=True),
        'use_https': dict(type='bool', required=False, default=True),
        'validate_certs': dict(type='bool', required=False, default=True),
        'timeout': dict(type='int', required=False, default=30)
    }

    # 合并参数
    common_args.update(base_args)
    return common_args


def adc_response_to_ansible_result(response, changed=True):
    """
    将 ADC 响应转换为 Ansible 结果格式

    Args:
        response: ADC 响应数据
        changed: 是否有变更

    Returns:
        dict: Ansible 格式的结果
    """
    return {
        'changed': changed,
        'response': response,
        'success': adc_result_check(response)
    }


def format_adc_response_for_ansible(response_data, action="", changed_default=True, check_status=True):
    """
    格式化ADC响应为Ansible模块返回格式

    Args:
        response_data (str/dict): API响应数据
        action (str): 执行的操作名称
        changed_default (bool): 默认的changed状态
        check_status (bool): 是否检查status字段，如果为False则只检查errmsg/errcode

    Returns:
        tuple: (success, result_dict)
            - success (bool): 操作是否成功
            - result_dict (dict): Ansible模块返回字典
    """
    # 初始化返回结果
    result = {
        'success': False,  # 默认为失败
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

        # 特殊处理：如果parsed_data是列表，直接视为成功（查询列表操作）
        if isinstance(parsed_data, list):
            result['success'] = True
        elif isinstance(parsed_data, dict):
            # 提取基本字段
            result['result'] = parsed_data.get('result', '')
            result['errcode'] = parsed_data.get('errcode', '')
            result['errmsg'] = parsed_data.get('errmsg', '')

            # 根据check_status参数决定如何检查状态
            if not check_status:
                # 如果check_status为False，只检查errmsg/errcode
                # 如果没有errmsg或errcode就是成功的
                if (not result['errmsg'] or not str(result['errmsg']).strip()) and (not result['errcode'] or not str(result['errcode']).strip()):
                    result['success'] = True
                else:
                    # 有errmsg或errcode，算失败
                    result['success'] = False
            else:
                # 检查result字段模式（适用于add/edit/delete等操作）
                if isinstance(result['result'], str) and result['result'].lower() == 'success':
                    result['success'] = True
                else:
                    # 对于查询类操作（get/list），如果有errmsg且不为空才算失败
                    if result['errmsg'] and str(result['errmsg']).strip():
                        # 有错误信息，检查是否是幂等性错误
                        errmsg_lower = result['errmsg'].lower() if isinstance(result['errmsg'], str) else str(result['errmsg']).lower()
                        if any(keyword in errmsg_lower for keyword in ['已存在', 'already exists']):
                            # 幂等性处理：如果是因为已存在而导致的"失败"，实际上算成功
                            result['success'] = True
                            result['result'] = 'success (already exists)'
                        else:
                            # 真实的错误
                            result['success'] = False
                    else:
                        # 没有错误信息，即使result字段不是'success'也算成功（可能是直接返回数据）
                        result['success'] = True
        else:
            # 其他类型（非列表、非字典），直接视为成功
            result['success'] = True

    except ValueError as e:  # 使用ValueError兼容Python 2/3，因为Python 2.7没有JSONDecodeError
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

