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
module: adc_waf_profile
short_description: Manage ADC WAF Profiles
description:
    - Manage ADC WAF Profiles including list and get operations
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
            - The action to perform (list_profiles, get_profile)
        required: true
        choices: ['list_profiles', 'get_profile']
    name:
        description:
            - The name of the WAF profile
        required: false
author:
    - Your Name
'''

EXAMPLES = '''
# List all WAF profiles
- adc_waf_profile:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "list_profiles"

# Get a specific WAF profile
- adc_waf_profile:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: "get_profile"
    name: "my_waf_profile"
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


def adc_list_waf_profiles(module):
    """List all WAF profiles"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.list" % (
        ip, authkey)
    result = send_request(url)
    return result


def adc_get_waf_profile(module):
    """Get a specific WAF profile"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="获取WAF模板需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=waf.profile.get" % (
        ip, authkey)

    data = {
        "name": name
    }

    result = send_request(url, data, method='POST')
    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(type='str', required=True),
            authkey=dict(type='str', required=True),
            action=dict(type='str', required=True, choices=[
                'list_profiles', 'get_profile'
            ]),
            name=dict(type='str', required=False),
        ),
        supports_check_mode=False
    )

    action = module.params['action']

    if action == 'list_profiles':
        result = adc_list_waf_profiles(module)
    elif action == 'get_profile':
        result = adc_get_waf_profile(module)
    else:
        module.fail_json(msg="Unknown action: %s" % action)

    if result.get('status') is True:
        module.exit_json(changed=True, result=result)
    else:
        module.fail_json(msg="Operation failed", result=result)


if __name__ == '__main__':
    main()
