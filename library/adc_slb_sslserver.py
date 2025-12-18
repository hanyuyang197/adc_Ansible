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
module: adc_slb_sslserver
short_description: Manage ADC SLB Server SSL profiles
description:
    - Manage ADC SLB Server SSL profiles including add, edit, delete, list and get operations
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
            - The action to perform (list_profiles, list_profiles_withcommon, get_profile, add_profile, edit_profile, delete_profile)
        required: true
        choices: ['list_profiles', 'list_profiles_withcommon', 'get_profile', 'add_profile', 'edit_profile', 'delete_profile']
    name:
        description:
            - The name of the server SSL profile
        required: false
    cert:
        description:
            - Certificate name
        required: false
    key:
        description:
            - Private key name
        required: false
author:
    - Your Name
'''

EXAMPLES = '''
# List all server SSL profiles
- adc_slb_sslserver:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "list_profiles"

# Get a specific server SSL profile
- adc_slb_sslserver:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "get_profile"
    name: "my_ssl_profile"

# Add a server SSL profile
- adc_slb_sslserver:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "add_profile"
    name: "my_ssl_profile"
    cert: "my_cert"
    key: "my_key"

# Edit a server SSL profile
- adc_slb_sslserver:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "edit_profile"
    name: "my_ssl_profile"
    cert: "new_cert"

# Delete a server SSL profile
- adc_slb_sslserver:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "delete_profile"
    name: "my_ssl_profile"
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


def adc_list_sslserver_profiles(module):
    """List all server SSL profiles"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.list" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_list_sslserver_profiles_withcommon(module):
    """List all server SSL profiles including common partition"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.list.withcommon" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_get_sslserver_profile(module):
    """Get a specific server SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="获取服务端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.get" % (
        ip, authkey)

    data = {
        "name": name
    }

    result = send_request(url, data, method='POST')
    return result


def adc_add_sslserver_profile(module):
    """Add a new server SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="添加服务端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.add" % (
        ip, authkey)

    # Construct profile data
    profile_data = {
        "name": name
    }

    # Only include parameters that are explicitly defined in YAML
    optional_params = ['cert', 'key']

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # Send POST request
    result = send_request(url, profile_data, method='POST')
    return result


def adc_edit_sslserver_profile(module):
    """Edit an existing server SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="编辑服务端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.edit" % (
        ip, authkey)

    # Construct profile data
    profile_data = {
        "name": name
    }

    # Only include parameters that are explicitly defined in YAML
    optional_params = ['cert', 'key']

    for param in optional_params:
        if module.params[param] is not None:
            profile_data[param] = module.params[param]

    # Send POST request
    result = send_request(url, profile_data, method='POST')
    return result


def adc_delete_sslserver_profile(module):
    """Delete a server SSL profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    # Check required parameters
    if not name:
        module.fail_json(msg="删除服务端SSL卸载模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.sslserver.del" % (
        ip, authkey)

    # Construct profile data
    profile_data = {
        "name": name
    }

    # Send POST request
    result = send_request(url, profile_data, method='POST')
    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(type='str', required=True),
            authkey=dict(type='str', required=True),
            action=dict(type='str', required=True, choices=[
                'list_profiles', 'list_profiles_withcommon', 'get_profile',
                'add_profile', 'edit_profile', 'delete_profile'
            ]),
            name=dict(type='str', required=False),
            cert=dict(type='str', required=False),
            key=dict(type='str', required=False),
        ),
        supports_check_mode=False
    )

    action = module.params['action']

    if action == 'list_profiles':
        result = adc_list_sslserver_profiles(module)
    elif action == 'list_profiles_withcommon':
        result = adc_list_sslserver_profiles_withcommon(module)
    elif action == 'get_profile':
        result = adc_get_sslserver_profile(module)
    elif action == 'add_profile':
        result = adc_add_sslserver_profile(module)
    elif action == 'edit_profile':
        result = adc_edit_sslserver_profile(module)
    elif action == 'delete_profile':
        result = adc_delete_sslserver_profile(module)
    else:
        module.fail_json(msg="Unknown action: %s" % action)

    if result.get('status') is True:
        module.exit_json(changed=True, result=result)
    else:
        module.fail_json(msg="Operation failed", result=result)


if __name__ == '__main__':
    main()
