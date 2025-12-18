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
        # 请求日志模板参数
        name=dict(type='str', required=False),
        request_log=dict(type='int', required=False),
        log_source_port_mode=dict(type='int', required=False),
        request_log_error_response=dict(type='int', required=False),
        request_log_error_close=dict(type='int', required=False),
        request_log_error_log_enable=dict(type='int', required=False),
        response_log=dict(type='int', required=False),
        response_log_error_log_enable=dict(type='int', required=False),
        request_log_pool=dict(type='str', required=False),
        request_log_error_log_pool=dict(type='str', required=False),
        response_log_pool=dict(type='str', required=False),
        response_log_error_log_pool=dict(type='str', required=False),
        request_log_template=dict(type='str', required=False),
        request_log_error_response_content=dict(type='str', required=False),
        request_log_error_log_template=dict(type='str', required=False),
        response_log_template=dict(type='str', required=False),
        response_log_error_log_template=dict(type='str', required=False),
        description=dict(type='str', required=False, default="")
    )

# 发送HTTP请求
def send_request(url, data=None, method='GET'):
    try:
        if data:
            data = json.dumps(data).encode('utf-8')
            req = urllib_request.Request(url, data=data)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib_request.Request(url)
        
        if method == 'POST':
            req.get_method = lambda: 'POST'
        elif method == 'PUT':
            req.get_method = lambda: 'PUT'
        elif method == 'DELETE':
            req.get_method = lambda: 'DELETE'
            
        response = urllib_request.urlopen(req)
        result = response.read()
        return json.loads(result) if result else {}
    except Exception as e:
        return {'status': 'error', 'msg': str(e)}

# 获取请求日志模板列表
def adc_list_request_log_profiles(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.request_log.list" % (ip, authkey)
    
    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取包含common分区的请求日志模板列表
def adc_list_request_log_profiles_withcommon(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.request_log.list.withcommon" % (ip, authkey)
    
    # 发送GET请求
    result = send_request(url, method='GET')
    return result

# 获取指定请求日志模板
def adc_get_request_log_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    
    # 检查必需参数
    if not name:
        module.fail_json(msg="获取请求日志模板需要提供name参数")
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.request_log.get" % (ip, authkey)
    
    # 构造请求数据
    data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]
    
    # 发送POST请求
    result = send_request(url, data, method='POST')
    return result

# 添加请求日志模板
def adc_add_request_log_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    description = module.params['description']
    
    # 检查必需参数
    if not name:
        module.fail_json(msg="添加请求日志模板需要提供name参数")
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.request_log.add" % (ip, authkey)
    
    # 构造模板数据
    profile_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "description" in module.params and module.params["description"] is not None:
        acl_data["description"] = description
   
    
    # 只有当参数在YAML中明确定义时才包含在请求中
    optional_params = [
        'request_log', 'log_source_port_mode', 'request_log_error_response',
        'request_log_error_close', 'request_log_error_log_enable', 'response_log',
        'response_log_error_log_enable', 'request_log_pool', 'request_log_error_log_pool',
        'response_log_pool', 'response_log_error_log_pool', 'request_log_template',
        'request_log_error_response_content', 'request_log_error_log_template',
        'response_log_template', 'response_log_error_log_template'
    ]
    
    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]
    
    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 编辑请求日志模板
def adc_edit_request_log_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    description = module.params['description']
    
    # 检查必需参数
    if not name:
        module.fail_json(msg="编辑请求日志模板需要提供name参数")
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.request_log.edit" % (ip, authkey)
    
    # 构造模板数据
    profile_data = {}
    # 只添加明确指定的参数
    if "name" in module.params and module.params["name"] is not None:
        acl_data["name"] = module.params["name"]
    if "description" in module.params and module.params["description"] is not None:
        acl_data["description"] = description
   
    
    # 只有当参数在YAML中明确定义时才包含在请求中
    optional_params = [
        'request_log', 'log_source_port_mode', 'request_log_error_response',
        'request_log_error_close', 'request_log_error_log_enable', 'response_log',
        'response_log_error_log_enable', 'request_log_pool', 'request_log_error_log_pool',
        'response_log_pool', 'response_log_error_log_pool', 'request_log_template',
        'request_log_error_response_content', 'request_log_error_log_template',
        'response_log_template', 'response_log_error_log_template'
    ]
    
    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]
    
    # 发送POST请求
    result = send_request(url, profile_data, method='POST')
    return result

# 删除请求日志模板
def adc_delete_request_log_profile(module):
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    
    # 检查必需参数
    if not name:
        module.fail_json(msg="删除请求日志模板需要提供name参数")
    
    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.profile.request_log.del" % (ip, authkey)
    
    # 构造请求数据
    data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]
    
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
        result = adc_list_request_log_profiles(module)
    elif action == 'list_profiles_withcommon':
        result = adc_list_request_log_profiles_withcommon(module)
    elif action == 'get_profile':
        result = adc_get_request_log_profile(module)
    elif action == 'add_profile':
        result = adc_add_request_log_profile(module)
    elif action == 'edit_profile':
        result = adc_edit_request_log_profile(module)
    elif action == 'delete_profile':
        result = adc_delete_request_log_profile(module)
    else:
        module.fail_json(msg="不支持的操作: %s" % action)
    
    # 处理结果
    if 'status' in result and result['status'] == 'error':
        module.fail_json(msg=result['msg'])
    else:
        module.exit_json(changed=True, result=result)

if __name__ == '__main__':
    main()