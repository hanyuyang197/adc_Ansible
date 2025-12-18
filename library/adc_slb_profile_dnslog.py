#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import json
try:
    # Python 2
    import urllib2
except ImportError:
    # Python 3
    import urllib.request as urllib2
    import urllib.error as urllib_error

# 定义模块参数


def define_module_args():
    return dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'list_profiles', 'list_profiles_withcommon', 'get_profile',
            'add_profile', 'edit_profile', 'delete_profile'
        ]),
        # DNS日志模板参数
        name=dict(type='str', required=False),
        description=dict(type='str', required=False),
        pool=dict(type='str', required=False),
        host=dict(type='str', required=False),
        facility=dict(type='int', required=False),
        severity=dict(type='int', required=False),
        src_port=dict(type='int', required=False),
        enable_local_record=dict(type='int', required=False),
        dst_port=dict(type='int', required=False),
        query=dict(type='int', required=False),
        response=dict(type='int', required=False)
    )

# 发送HTTP请求


def send_request(url, data=None, method='GET'):
    try:
        if data:
            data = json.dumps(data).encode('utf-8')
            req = urllib2.Request(url, data=data)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib2.Request(url)

        if method == 'POST':
            req.get_method = lambda: 'POST'
        elif method == 'PUT':
            req.get_method = lambda: 'PUT'
        elif method == 'DELETE':
            req.get_method = lambda: 'DELETE'

        response = urllib2.urlopen(req)
        result = response.read()
        return json.loads(result) if result else {}
    except Exception as e:
        return {'status': 'error', 'msg': str(e)}

# 获取DNS日志模板列表


def adc_list_dnslog_profiles(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dnslog.list" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取包含common分区的DNS日志模板列表


def adc_list_dnslog_profiles_withcommon(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dnslog.list.withcommon" % (
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取指定DNS日志模板


def adc_get_dnslog_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="获取DNS日志模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dnslog.get" % (
        ip, authkey)

    # 构造请求数据
    data = {
        "name": name
    }

    # 发送POST请求
    result = send_request(url, data, method='POST')
    return result

# 添加DNS日志模板


def adc_add_dnslog_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="添加DNS日志模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dnslog.add" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name
    }

    # 只有当参数在YAML中明确定义时才包含在请求中
    optional_params = [
        'description', 'pool', 'host', 'facility', 'severity',
        'src_port', 'enable_local_record', 'dst_port', 'query', 'response'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 编辑DNS日志模板


def adc_edit_dnslog_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑DNS日志模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dnslog.edit" % (
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name
    }

    # 只有当参数在YAML中明确定义时才包含在请求中
    optional_params = [
        'description', 'pool', 'host', 'facility', 'severity',
        'src_port', 'enable_local_record', 'dst_port', 'query', 'response'
    ]

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 删除DNS日志模板


def adc_delete_dnslog_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        module.fail_json(msg="删除DNS日志模板需要提供name参数")

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.dnslog.del" % (
        ip, authkey)

    # 构造请求数据
    data = {
        "name": name
    }

    # 发送POST请求
    result = send_request(url, data, method='POST')
    return result

# 主函数


def main():
    # 定义模块参数
    module_args = define_module_args()

    # 创建Ansible模块实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # 获取参数
    action = module.params['action']

    # 根据action执行相应操作
    if action == 'list_profiles':
        result = adc_list_dnslog_profiles(module)
    elif action == 'list_profiles_withcommon':
        result = adc_list_dnslog_profiles_withcommon(module)
    elif action == 'get_profile':
        result = adc_get_dnslog_profile(module)
    elif action == 'add_profile':
        result = adc_add_dnslog_profile(module)
    elif action == 'edit_profile':
        result = adc_edit_dnslog_profile(module)
    elif action == 'delete_profile':
        result = adc_delete_dnslog_profile(module)
    else:
        module.fail_json(msg="不支持的操作: %s" % action)

    # 处理结果
    if 'status' in result and result['status'] == 'error':
        module.fail_json(msg=result['msg'])
    else:
        module.exit_json(changed=True, result=result)


if __name__ == '__main__':
    main()
