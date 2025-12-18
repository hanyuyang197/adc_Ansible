#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import json
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


def adc_get_web_ciphers(module):
    """获取web网页加密算法和版本"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.web.ciphers.get" % (
        ip, authkey)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='POST')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'POST'
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="获取web网页加密算法和版本失败: %s" % str(e))

    # 对于获取操作，直接返回响应数据
    if response_data:
        try:
            parsed_data = json.loads(response_data)
            # 检查是否有错误信息
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="获取web网页加密算法和版本失败", response=parsed_data)
            else:
                module.exit_json(changed=False, config=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")


def adc_set_web_ciphers(module):
    """设置web网页加密算法和版本"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    ciphers_all = module.params['ciphers_all']
    ciphers = module.params['ciphers']
    protocols = module.params['protocols']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=system.web.ciphers.set" % (
        ip, authkey)

    # 构造加密算法和版本配置数据
    ciphers_data = {}

    # 添加可选参数
    if ciphers_all is not None:
        ciphers_data["ciphers_all"] = ciphers_all
    if ciphers is not None:
        ciphers_data["ciphers"] = ciphers
    if protocols is not None:
        ciphers_data["protocols"] = protocols

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = json.dumps(ciphers_data)
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            post_data = json.dumps(ciphers_data)
            req = urllib_request.Request(url, data=post_data, headers={
                                         'Content-Type': 'application/json'})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="设置web网页加密算法和版本失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "设置web网页加密算法和版本", True)
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
            'get_web_ciphers', 'set_web_ciphers']),
        # 加密算法和版本配置参数
        ciphers_all=dict(type='list', required=False),
        ciphers=dict(type='list', required=False),
        protocols=dict(type='list', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'get_web_ciphers':
        adc_get_web_ciphers(module)
    elif action == 'set_web_ciphers':
        adc_set_web_ciphers(module)


if __name__ == '__main__':
    main()
