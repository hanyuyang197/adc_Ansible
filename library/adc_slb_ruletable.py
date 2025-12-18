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

DOCUMENTATION = '''
---
module: adc_slb_ruletable
short_description: Manage ADC SLB Rule Tables
description:
    - Manage ADC SLB Rule Tables including add, edit, delete, list and get operations
version_added: "2.4"
options:
    ip:
        description:
            - The IP address of the ADC device
        required: true
    authkey:
        description:
            - The authentication key for the ADC device
        required: true
    action:
        description:
            - The action to perform (list_ruletables, list_ruletables_withcommon, get_ruletable, add_ruletable, delete_ruletable, add_ruletable_entry, delete_ruletable_entry, add_ruletable_string, delete_ruletable_string, add_ruletable_dns, delete_ruletable_dns)
        required: true
        choices: ['list_ruletables', 'list_ruletables_withcommon', 'get_ruletable', 'add_ruletable', 'delete_ruletable', 'add_ruletable_entry', 'delete_ruletable_entry', 'add_ruletable_string', 'delete_ruletable_string', 'add_ruletable_dns', 'delete_ruletable_dns']
    name:
        description:
            - The name of the rule table
        required: false
    entrys:
        description:
            - Rule entries array for IP rules
        required: false
        type: list
    strings:
        description:
            - Rule entries array for string rules
        required: false
        type: list
    dnss:
        description:
            - Rule entries array for DNS rules
        required: false
        type: list
author:
    - Your Name
'''

EXAMPLES = '''
# List all rule tables
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "list_ruletables"

# Get a specific rule table
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "get_ruletable"
    name: "my_ruletable"

# Add a rule table
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_ruletable"
    name: "my_ruletable"

# Delete a rule table
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_ruletable"
    name: "my_ruletable"

# Add rule table entries
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_ruletable_entry"
    name: "my_ruletable"
    entrys:
    - ip: "1.2.3.4/32"
        id: 1
        age: 0

# Delete rule table entries
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_ruletable_entry"
    name: "my_ruletable"
    entrys:
    - ip: "1.2.3.4/32"

# Add rule table string entries
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_ruletable_string"
    name: "my_ruletable"
    strings:
    - key: "test1"
        value: "na"

# Delete rule table string entries
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_ruletable_string"
    name: "my_ruletable"
    strings:
    - key: "test1"
        value: "na"

# Add rule table DNS entries
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_ruletable_dns"
    name: "my_ruletable"
    dnss:
    - domain: "www.ddd.com"
        lid: 3
        match_type: 0

# Delete rule table DNS entries
- adc_slb_ruletable:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_ruletable_dns"
    name: "my_ruletable"
    dnss:
    - domain: "www.ddd.com"
'''

RETURN = '''
result:
    description: The response from the ADC device
    returned: success
    type: dict
'''

def send_request(url, data=None, method='GET'):
    """Send HTTP request to ADC device"""
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
        
        # 根据API文档，检查响应是否成功
        # 对于配置类API，成功时返回 {"result":"success"}
        # 对于查询类API，返回具体的数据
        if isinstance(result, dict):
            if result.get('result', '').lower() == 'success':
                return {'success': True, 'data': result, 'errcode': '', 'errmsg': ''}
            elif 'errcode' in result:
                return {'success': False, 'data': result, 'errcode': result.get('errcode', ''), 'errmsg': result.get('errmsg', '')}
            else:
                # 查询类API返回的数据
                return {'success': True, 'data': result, 'errcode': '', 'errmsg': ''}
        elif isinstance(result, list):
            # 列表类型的查询结果
            return {'success': True, 'data': result, 'errcode': '', 'errmsg': ''}
        else:
            return {'success': True, 'data': result, 'errcode': '', 'errmsg': ''}
            
    except Exception as e:
        return {'success': False, 'data': {}, 'errcode': 'REQUEST_ERROR', 'errmsg': str(e)}

def adc_list_ruletables(module):
    """List all rule tables"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.list" % (ip, authkey)
    result = send_request(url)
    return result

def adc_list_ruletables_withcommon(module):
    """List all rule tables including common partition"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.list.withcommon" % (ip, authkey)
    result = send_request(url)
    return result

def adc_get_ruletable(module):
    """Get a specific rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    
    if not name:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "获取规则表需要提供name参数"}
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.get" % (ip, authkey)
    
    data = {"name": name}
    # 移除未明确指定的参数
    for key in list(data.keys()):
        if data[key] is None or (isinstance(data[key], str) and data[key] == ""):
            del data[key]
    
    result = send_request(url, data, method='POST')
    return result

def adc_add_ruletable(module):
    """Add a new rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    
    # Check required parameters
    if not name:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "添加规则表需要提供name参数"}
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.add" % (ip, authkey)
    
    # Construct rule table data according to API documentation
    ruletable_data = {
        "ruletable": {
            "name": name
        }
    }
    
    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result

def adc_delete_ruletable(module):
    """Delete a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    
    # Check required parameters
    if not name:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "删除规则表需要提供name参数"}
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.del" % (ip, authkey)
    
    # Construct rule table data
    ruletable_data = {"name": name}
    # 移除未明确指定的参数
    for key in list(ruletable_data.keys()):
        if ruletable_data[key] is None or (isinstance(ruletable_data[key], str) and ruletable_data[key] == ""):
            del ruletable_data[key]
    
    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result

def adc_add_ruletable_entry(module):
    """Add entries to a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    entrys = module.params['entrys']
    
    # Check required parameters
    if not name:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "添加规则表条目需要提供name参数"}
    
    if not entrys:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "添加规则表条目需要提供entrys参数"}
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.entry.add" % (ip, authkey)
    
    # Construct rule table entry data
    ruletable_data = {
        "name": name,
        "entrys": entrys
    }
    
    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result

def adc_delete_ruletable_entry(module):
    """Delete entries from a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    entrys = module.params['entrys']
    
    # Check required parameters
    if not name:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "删除规则表条目需要提供name参数"}
    
    if not entrys:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "删除规则表条目需要提供entrys参数"}
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.entry.del" % (ip, authkey)
    
    # Construct rule table entry data
    ruletable_data = {
        "name": name,
        "entrys": entrys
    }
    
    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result

def adc_add_ruletable_string(module):
    """Add string entries to a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    strings = module.params['strings']
    
    # Check required parameters
    if not name:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "添加规则表字符串条目需要提供name参数"}
    
    if not strings:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "添加规则表字符串条目需要提供strings参数"}
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.string.add" % (ip, authkey)
    
    # Construct rule table string data
    ruletable_data = {
        "name": name,
        "strings": strings
    }
    
    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result

def adc_delete_ruletable_string(module):
    """Delete string entries from a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    strings = module.params['strings']
    
    # Check required parameters
    if not name:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "删除规则表字符串条目需要提供name参数"}
    
    if not strings:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "删除规则表字符串条目需要提供strings参数"}
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.string.del" % (ip, authkey)
    
    # Construct rule table string data
    ruletable_data = {
        "name": name,
        "strings": strings
    }
    
    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result

def adc_add_ruletable_dns(module):
    """Add DNS entries to a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    dnss = module.params['dnss']
    
    # Check required parameters
    if not name:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "添加规则表DNS条目需要提供name参数"}
    
    if not dnss:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "添加规则表DNS条目需要提供dnss参数"}
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.dns.add" % (ip, authkey)
    
    # Construct rule table DNS data
    ruletable_data = {
        "name": name,
        "dnss": dnss
    }
    
    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result

def adc_delete_ruletable_dns(module):
    """Delete DNS entries from a rule table"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    dnss = module.params['dnss']
    
    # Check required parameters
    if not name:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "删除规则表DNS条目需要提供name参数"}
    
    if not dnss:
        return {'success': False, 'data': {}, 'errcode': 'MISSING_PARAM', 'errmsg': "删除规则表DNS条目需要提供dnss参数"}
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.ruletable.dns.del" % (ip, authkey)
    
    # Construct rule table DNS data
    ruletable_data = {
        "name": name,
        "dnss": dnss
    }
    
    # Send POST request
    result = send_request(url, ruletable_data, method='POST')
    return result

def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(type='str', required=True),
            authkey=dict(type='str', required=True),
            action=dict(type='str', required=True, choices=[
                'list_ruletables', 'list_ruletables_withcommon', 'get_ruletable', 
                'add_ruletable', 'delete_ruletable', 'add_ruletable_entry', 
                'delete_ruletable_entry', 'add_ruletable_string', 'delete_ruletable_string',
                'add_ruletable_dns', 'delete_ruletable_dns'
            ]),
            name=dict(type='str', required=False),
            entrys=dict(type='list', required=False),
            strings=dict(type='list', required=False),
            dnss=dict(type='list', required=False),
        ),
        supports_check_mode=False
    )

    # 获取action参数并确保它是字符串类型
    if 'action' in module.params and module.params['action'] is not None:
        action = str(module.params['action'])
    else:
        action = ''
    
    if action == 'list_ruletables':
        result = adc_list_ruletables(module)
    elif action == 'list_ruletables_withcommon':
        result = adc_list_ruletables_withcommon(module)
    elif action == 'get_ruletable':
        result = adc_get_ruletable(module)
    elif action == 'add_ruletable':
        result = adc_add_ruletable(module)
    elif action == 'delete_ruletable':
        result = adc_delete_ruletable(module)
    elif action == 'add_ruletable_entry':
        result = adc_add_ruletable_entry(module)
    elif action == 'delete_ruletable_entry':
        result = adc_delete_ruletable_entry(module)
    elif action == 'add_ruletable_string':
        result = adc_add_ruletable_string(module)
    elif action == 'delete_ruletable_string':
        result = adc_delete_ruletable_string(module)
    elif action == 'add_ruletable_dns':
        result = adc_add_ruletable_dns(module)
    elif action == 'delete_ruletable_dns':
        result = adc_delete_ruletable_dns(module)
    else:
        module.fail_json(msg="Unknown action: %s" % action)
    
    # 正确处理返回值 - 检查result是否成功
    if result.get('success', False):
        module.exit_json(changed=True, result=result)
    else:
        module.fail_json(msg="Operation failed: %s" % result.get('errmsg', 'Unknown error'), result=result)

if __name__ == '__main__':
    main()