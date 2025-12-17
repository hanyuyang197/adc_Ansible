#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import json
import urllib
import urllib2

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

# 获取RTSP模板列表
def adc_list_rtsp_profiles(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.rtsp.list" % (ip, authkey)
    
    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取包含common分区的RTSP模板列表
def adc_list_rtsp_profiles_withcommon(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.rtsp.list.withcommon" % (ip, authkey)
    
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
        module.fail_json(msg="获取RTSP模板需要提供name参数")
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.rtsp.get" % (ip, authkey)
    
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
        module.fail_json(msg="添加RTSP模板需要提供name参数")
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.rtsp.add" % (ip, authkey)
    
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
        module.fail_json(msg="编辑RTSP模板需要提供name参数")
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.rtsp.edit" % (ip, authkey)
    
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
        module.fail_json(msg="删除RTSP模板需要提供name参数")
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.rtsp.del" % (ip, authkey)
    
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
        module.fail_json(msg="不支持的操作: %s" % action)
    
    # 处理结果
    if 'status' in result and result['status'] == 'error':
        module.fail_json(msg=result['msg'])
    else:
        module.exit_json(changed=True, result=result)

if __name__ == '__main__':
    main()