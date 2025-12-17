#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
try:
    import urllib2
    import json
except ImportError:
    pass

DOCUMENTATION = '''
---
module: adc_slb_policy
short_description: Manage ADC SLB Policy Templates
description:
    - Manage ADC SLB Policy Templates including add, edit, delete, list and get operations
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
            - The action to perform (list_policies, list_policies_withcommon, get_policy, add_policy, edit_policy, delete_policy)
        required: true
        choices: ['list_policies', 'list_policies_withcommon', 'get_policy', 'add_policy', 'edit_policy', 'delete_policy']
    name:
        description:
            - The name of the policy template
        required: false
    match_dst_ip:
        description:
            - Match destination IP address; 1: yes; 0: no
        required: false
    match_overlap:
        description:
            - Overlap match; 1: yes; 0: no
        required: false
    bwlist_name:
        description:
            - Black/white list name
        required: false
    ruletable_name:
        description:
            - Rule table name
        required: false
    match_client:
        description:
            - Client matching method; 0: source IP matching; 1: destination IP matching; 2: header name matching
        required: false
    header_name:
        description:
            - Header name
        required: false
    bwlists:
        description:
            - Black/white list policy rules array
        required: false
        type: list
    ruletables:
        description:
            - Rule table policy rules array
        required: false
        type: list
author:
    - Your Name
'''

EXAMPLES = '''
# List all policy templates
- adc_slb_policy:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "list_policies"

# Get a specific policy template
- adc_slb_policy:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "get_policy"
    name: "my_policy"

# Add a policy template
- adc_slb_policy:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_policy"
    name: "my_policy"
    match_dst_ip: 1
    match_overlap: 1
    bwlist_name: "bwl"
    ruletable_name: "rt0"
    match_client: 2
    header_name: "head"

# Edit a policy template
- adc_slb_policy:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "edit_policy"
    name: "my_policy"
    match_dst_ip: 0

# Delete a policy template
- adc_slb_policy:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_policy"
    name: "my_policy"
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
            req = urllib2.Request(url, data=data_json)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib2.Request(url)
        
        response = urllib2.urlopen(req)
        result = json.loads(response.read())
        return result
    except Exception as e:
        return {'status': False, 'msg': str(e)}

def adc_list_policies(module):
    """List all policy templates"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.list" % (ip, authkey)
    result = send_request(url)
    return result

def adc_list_policies_withcommon(module):
    """List all policy templates including common partition"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.list.withcommon" % (ip, authkey)
    result = send_request(url)
    return result

def adc_get_policy(module):
    """Get a specific policy template"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    
    if not name:
        module.fail_json(msg="获取策略模板需要提供name参数")
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.get" % (ip, authkey)
    
    data = {
        "name": name
    }
    
    result = send_request(url, data, method='POST')
    return result

def adc_add_policy(module):
    """Add a new policy template"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    
    # Check required parameters
    if not name:
        module.fail_json(msg="添加策略模板需要提供name参数")
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.add" % (ip, authkey)
    
    # Construct policy data
    policy_data = {
        "name": name
    }
    
    # Only include parameters that are explicitly defined in YAML
    optional_params = [
        'match_dst_ip', 'match_overlap', 'bwlist_name', 'ruletable_name',
        'match_client', 'header_name', 'bwlists', 'ruletables'
    ]
    
    for param in optional_params:
        if module.params[param] is not None:
            policy_data[param] = module.params[param]
    
    # Send POST request
    result = send_request(url, policy_data, method='POST')
    return result

def adc_edit_policy(module):
    """Edit an existing policy template"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    
    # Check required parameters
    if not name:
        module.fail_json(msg="编辑策略模板需要提供name参数")
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.edit" % (ip, authkey)
    
    # Construct policy data
    policy_data = {
        "name": name
    }
    
    # Only include parameters that are explicitly defined in YAML
    optional_params = [
        'match_dst_ip', 'match_overlap', 'bwlist_name', 'ruletable_name',
        'match_client', 'header_name', 'bwlists', 'ruletables'
    ]
    
    for param in optional_params:
        if module.params[param] is not None:
            policy_data[param] = module.params[param]
    
    # Send POST request
    result = send_request(url, policy_data, method='POST')
    return result

def adc_delete_policy(module):
    """Delete a policy template"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']
    
    # Check required parameters
    if not name:
        module.fail_json(msg="删除策略模板需要提供name参数")
    
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.policy.del" % (ip, authkey)
    
    # Construct policy data
    policy_data = {
        "name": name
    }
    
    # Send POST request
    result = send_request(url, policy_data, method='POST')
    return result

def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(type='str', required=True),
            authkey=dict(type='str', required=True),
            action=dict(type='str', required=True, choices=[
                'list_policies', 'list_policies_withcommon', 'get_policy', 
                'add_policy', 'edit_policy', 'delete_policy'
            ]),
            name=dict(type='str', required=False),
            match_dst_ip=dict(type='int', required=False),
            match_overlap=dict(type='int', required=False),
            bwlist_name=dict(type='str', required=False),
            ruletable_name=dict(type='str', required=False),
            match_client=dict(type='int', required=False),
            header_name=dict(type='str', required=False),
            bwlists=dict(type='list', required=False),
            ruletables=dict(type='list', required=False),
        ),
        supports_check_mode=False
    )

    action = module.params['action']
    
    if action == 'list_policies':
        result = adc_list_policies(module)
    elif action == 'list_policies_withcommon':
        result = adc_list_policies_withcommon(module)
    elif action == 'get_policy':
        result = adc_get_policy(module)
    elif action == 'add_policy':
        result = adc_add_policy(module)
    elif action == 'edit_policy':
        result = adc_edit_policy(module)
    elif action == 'delete_policy':
        result = adc_delete_policy(module)
    else:
        module.fail_json(msg="Unknown action: %s" % action)
    
    if result.get('status') is True:
        module.exit_json(changed=True, result=result)
    else:
        module.fail_json(msg="Operation failed", result=result)

if __name__ == '__main__':
    main()