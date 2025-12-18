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

# 定义模块参数


def define_module_args():
    return dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'list_profiles', 'list_profiles_withcommon', 'get_profile',
            'add_profile', 'edit_profile', 'delete_profile'
        ]),
        # RTSP模板参数
        name=dict(type='str', required=False),
        description=dict(type='str', required=False, default=""),
        uri_switch=dict(type='list', required=False, default=[])
    )

# 发送HTTP请求


def send_request(url, data=None, method='GET'):
    try:
        if method == 'POST' and data:
            data_json = json.dumps(data)
            data_bytes = data_json.encode('utf-8')
            req = urllib_request.Request(url, data=data_bytes)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib_request.Request(url)

        response = urllib_request.urlopen(req)
        result = json.loads(response.read())

        # 标准化响应格式
        # 成功响应保持原样
        # 错误响应标准化为 {"result":"error","errcode":"REQUEST_ERROR","errmsg":"..."}
        if isinstance(result, dict) and 'status' in result and result['status'] == 'error':
            return {
                'result': 'error',
                'errcode': 'REQUEST_ERROR',
                'errmsg': result.get('msg', '请求失败')
            }
        else:
            return result
    except Exception as e:
        return {
            'result': 'error',
            'errcode': 'REQUEST_EXCEPTION',
            'errmsg': str(e)
        }

# 获取RTSP模板列表


def adc_list_rtsp_profiles(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://{0}/adcapi/v2.0/?authkey={1}&action=slb.profile.rtsp.list".format(
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取包含common分区的RTSP模板列表


def adc_list_rtsp_profiles_withcommon(module):
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://{0}/adcapi/v2.0/?authkey={1}&action=slb.profile.rtsp.list.withcommon".format(
        ip, authkey)

    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取指定RTSP模板


def adc_get_rtsp_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "获取RTSP模板需要提供name参数"}

    # 构造请求URL
    url = "http://{0}/adcapi/v2.0/?authkey={1}&action=slb.profile.rtsp.get".format(
        ip, authkey)

    # 构造请求数据
    data = {
        "name": name
    }

    # 发送POST请求
    result = send_request(url, data, method='POST')
    return result

# 添加RTSP模板


def adc_add_rtsp_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    description = module.params['description']
    uri_switch = module.params['uri_switch']

    # 检查必需参数
    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "添加RTSP模板需要提供name参数"}

    # 构造请求URL
    url = "http://{0}/adcapi/v2.0/?authkey={1}&action=slb.profile.rtsp.add".format(
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name,
        "description": description,
        "uri_switch": uri_switch
    }

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 编辑RTSP模板


def adc_edit_rtsp_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    description = module.params['description']
    uri_switch = module.params['uri_switch']

    # 检查必需参数
    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "编辑RTSP模板需要提供name参数"}

    # 构造请求URL
    url = "http://{0}/adcapi/v2.0/?authkey={1}&action=slb.profile.rtsp.edit".format(
        ip, authkey)

    # 构造模板数据
    profile_data = {
        "name": name,
        "description": description,
        "uri_switch": uri_switch
    }

    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 删除RTSP模板


def adc_delete_rtsp_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # 检查必需参数
    if not name:
        return {'result': 'error', 'errcode': 'MISSING_PARAM', 'errmsg': "删除RTSP模板需要提供name参数"}

    # 构造请求URL
    url = "http://{0}/adcapi/v2.0/?authkey={1}&action=slb.profile.rtsp.del".format(
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
        result = adc_list_rtsp_profiles(module)
    elif action == 'list_profiles_withcommon':
        result = adc_list_rtsp_profiles_withcommon(module)
    elif action == 'get_profile':
        result = adc_get_rtsp_profile(module)
    elif action == 'add_profile':
        result = adc_add_rtsp_profile(module)
    elif action == 'edit_profile':
        result = adc_edit_rtsp_profile(module)
    elif action == 'delete_profile':
        result = adc_delete_rtsp_profile(module)
    else:
        module.fail_json(msg="不支持的操作: {0}".format(action))

    # 处理结果 - 使用标准的ADC响应格式
    # 成功响应: {"result":"success"} 或直接返回数据
    # 错误响应: {"result":"error","errcode":"...","errmsg":"..."}
    if isinstance(result, dict):
        if result.get('result', '').lower() == 'success':
            # 成功响应
            module.exit_json(changed=True, result=result)
        elif 'errcode' in result and result['errcode']:
            # 错误响应
            module.fail_json(msg="操作失败: {0}".format(
                result.get('errmsg', '未知错误')), result=result)
        else:
            # 查询类API直接返回数据
            module.exit_json(changed=False, result=result)
    else:
        # 其他类型的数据直接返回
        module.exit_json(changed=False, result=result)


if __name__ == '__main__':
    main()
