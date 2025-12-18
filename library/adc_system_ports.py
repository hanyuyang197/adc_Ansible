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


def format_adc_response_for_ansible(response_data, action="", is_modify_action=False):
    """
    格式化ADC API响应数据为Ansible模块所需的格式

    Args:
        response_data (str): ADC API返回的响应数据
        action (str): 执行的操作名称
        is_modify_action (bool): 是否为修改类操作

    Returns:
        tuple: (success_bool, result_dict)
    """
    try:
        # 解析JSON响应
        result = json.loads(response_data)

        # 检查是否包含错误信息
        if 'errcode' in result and result['errcode'] != 0:
            # 操作失败
            result_dict = {
                'changed': False,
                'msg': '%s操作失败' % action if action else '操作失败',
                'error': {
                    'result': result.get('result', ''),
                    'errcode': result.get('errcode', ''),
                    'errmsg': result.get('errmsg', '')
                },
                'response': result.get('data', {})
            }
            return False, result_dict
        elif 'errcode' in result and result['errcode'] == 0:
            # 操作成功
            result_dict = {
                'changed': is_modify_action,  # 修改类操作标记为changed
                'msg': '%s操作成功' % action if action else '操作成功',
                'response': result.get('data', {})
            }

            # 如果是幂等性成功（已存在），调整消息
            if 'result' in result and 'already exists' in result['result']:
                result_dict['changed'] = False
                result_dict['msg'] = '%s操作成功（资源已存在，无需更改）' % action if action else '操作成功（资源已存在，无需更改）'

            return True, result_dict
        else:
            # 未知格式的响应
            result_dict = {
                'changed': is_modify_action,
                'msg': '%s操作完成' % action if action else '操作完成',
                'response': result
            }
            return True, result_dict

    except Exception as e:
        # 解析失败
        result_dict = {
            'changed': False,
            'msg': '解析响应失败: %s' % str(e),
            'raw_response': response_data if isinstance(response_data, str) else str(response_data)
        }
        return False, result_dict


def adc_set_system_ports(module):
    """设置系统应用端口配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    sshd_port = module.params['sshd_port']
    telnet_port = module.params['telnet_port']
    http_port = module.params['http_port']
    https_port = module.params['https_port']
    weak_algo = module.params['weak_algo']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.ports.set" % (
        ip, authkey)

    # 构造系统端口配置数据
    ports_data = {}

    # 添加可选参数
    if sshd_port is not None:
        ports_data["sshd_port"] = sshd_port
    if telnet_port is not None:
        ports_data["telnet_port"] = telnet_port
    if http_port is not None:
        ports_data["http_port"] = http_port
    if https_port is not None:
        ports_data["https_port"] = https_port
    if weak_algo is not None:
        ports_data["weak_algo"] = weak_algo

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
                        post_data = json.dumps(ports_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
                        post_data = json.dumps(ports_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                        'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="设置系统应用端口配置失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置系统应用端口配置", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def adc_get_system_ports(module):
    """获取系统应用端口配置"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.ports.get" % (
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
        module.fail_json(msg="获取系统应用端口配置失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取系统应用端口配置失败", response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
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
            'set_system_ports', 'get_system_ports']),
        # 系统端口配置参数
        sshd_port=dict(type='int', required=False),
        telnet_port=dict(type='int', required=False),
        http_port=dict(type='int', required=False),
        https_port=dict(type='int', required=False),
        weak_algo=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'set_system_ports':
        adc_set_system_ports(module)
    elif action == 'get_system_ports':
        adc_get_system_ports(module)


if __name__ == '__main__':
    main()
