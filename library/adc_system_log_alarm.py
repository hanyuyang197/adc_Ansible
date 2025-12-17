#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Horizon Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from adc_base import ADCBase
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

DOCUMENTATION = r'''
---
module: adc_system_log_alarm
short_description: Manage ADC system log alarm configuration
description:
  - Manage email and SMS log alarm configuration for ADC devices.
  - Supports getting and setting email/SMS alarm configurations.
version_added: "1.0.0"
options:
  alarm_type:
    description:
      - The type of alarm configuration to manage.
    type: str
    required: true
    choices: [ email, sms ]
  action:
    description:
      - The action to perform on alarm configuration.
    type: str
    required: true
    choices: [ get, set ]
  # Parameters for email alarm configuration
  delay_send_buff:
    description:
      - Delay send buffer length (16-256).
    type: int
  delay_send_time:
    description:
      - Delay send time in minutes (10-1440).
    type: int
  send_event:
    description:
      - Send events array.
      - 1: Interface status
      - 2: Device reboot
      - 3: Login event
      - 4: Health check failure
      - 5: Health check busy
      - 9: VM linkage
      - 11: GSLB log
      - 12: Erule log
    type: list
    elements: int
  send_level:
    description:
      - Log level filter (-1, 0, 1, 2, 5).
      - -1: Disable level filtering
    type: int
    choices: [-1, 0, 1, 2, 5]
  # Parameters for SMS alarm configuration
  url:
    description:
      - SMS platform URL.
    type: str
author:
  - Horizon Inc.
'''

EXAMPLES = r'''
- name: Get email alarm configuration
  adc_system_log_alarm:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    alarm_type: email
    action: get

- name: Set email alarm configuration
  adc_system_log_alarm:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    alarm_type: email
    action: set
    delay_send_buff: 120
    delay_send_time: 110
    send_event: [2, 4, 5]
    send_level: 5

- name: Get SMS alarm configuration
  adc_system_log_alarm:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    alarm_type: sms
    action: get

- name: Set SMS alarm configuration
  adc_system_log_alarm:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    alarm_type: sms
    action: set
    url: "h.163.com.cn"
    send_event: [1, 3]
    send_level: 2
'''

RETURN = r'''
email_config:
  description: Email alarm configuration when alarm_type=email and action=get
  returned: when alarm_type=email and action=get
  type: dict
  sample: {
    "delay_send_buff": 120,
    "delay_send_time": 110,
    "send_event": [2, 4, 5],
    "send_level": 5
  }
sms_config:
  description: SMS alarm configuration when alarm_type=sms and action=get
  returned: when alarm_type=sms and action=get
  type: dict
  sample: {
    "url": "h.163.com.cn",
    "send_event": [1, 3],
    "send_level": 2
  }
msg:
  description: Result message
  returned: always
  type: str
  sample: "Email alarm configuration updated successfully"
'''


def adc_get_email_alarm_config(module, adc_base):
    """Get email alarm configuration"""
    # Make API call
    response = adc_base.make_request('GET', 'log.alarm.email.get')

    if response.get('success'):
        return True, {'email_config': response.get('data', {})}
    else:
        return False, {'msg': response.get('msg', 'Failed to get email alarm configuration')}


def adc_set_email_alarm_config(module, adc_base):
    """Set email alarm configuration"""
    # Prepare parameters
    params = {}

    # Add optional parameters if provided
    if module.params['delay_send_buff'] is not None:
        params['delay_send_buff'] = module.params['delay_send_buff']
    if module.params['delay_send_time'] is not None:
        params['delay_send_time'] = module.params['delay_send_time']
    if module.params['send_event'] is not None:
        params['send_event'] = module.params['send_event']
    if module.params['send_level'] is not None:
        params['send_level'] = module.params['send_level']

    # Make API call
    response = adc_base.make_request(
        'POST', 'log.alarm.email.set', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Set email alarm configuration", True)
    return success, result_dict


def adc_get_sms_alarm_config(module, adc_base):
    """Get SMS alarm configuration"""
    # Make API call
    response = adc_base.make_request('GET', 'log.alarm.sms.get')

    if response.get('success'):
        return True, {'sms_config': response.get('data', {})}
    else:
        return False, {'msg': response.get('msg', 'Failed to get SMS alarm configuration')}


def adc_set_sms_alarm_config(module, adc_base):
    """Set SMS alarm configuration"""
    # Prepare parameters
    params = {}

    # Add optional parameters if provided
    if module.params['url'] is not None:
        params['url'] = module.params['url']
    if module.params['send_event'] is not None:
        params['send_event'] = module.params['send_event']
    if module.params['send_level'] is not None:
        params['send_level'] = module.params['send_level']

    # Make API call
    response = adc_base.make_request('POST', 'log.alarm.sms.set', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Set SMS alarm configuration", True)
    return success, result_dict


def main():
    # Define module arguments
    argument_spec = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        alarm_type=dict(type='str', required=True, choices=['email', 'sms']),
        action=dict(type='str', required=True, choices=['get', 'set']),
        # Parameters for email alarm configuration
        delay_send_buff=dict(type='int'),
        delay_send_time=dict(type='int'),
        send_event=dict(type='list', elements='int'),
        send_level=dict(type='int', choices=[-1, 0, 1, 2, 5]),
        # Parameters for SMS alarm configuration
        url=dict(type='str'),
    )

    # Create Ansible module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    # Extract module parameters
    alarm_type = str(module.params['alarm_type'])
    action = str(module.params['action'])

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(changed=False)

    # Create ADC base object
    adc_base = ADCBase(module)

    try:
        # Perform requested action based on alarm type
        if alarm_type == 'email':
            if action == 'get':
                changed, result = adc_get_email_alarm_config(module, adc_base)
            elif action == 'set':
                changed, result = adc_set_email_alarm_config(module, adc_base)
            else:
                module.fail_json(
                    msg="Unsupported action for email alarm: %s" % action)
        elif alarm_type == 'sms':
            if action == 'get':
                changed, result = adc_get_sms_alarm_config(module, adc_base)
            elif action == 'set':
                changed, result = adc_set_sms_alarm_config(module, adc_base)
            else:
                module.fail_json(
                    msg="Unsupported action for SMS alarm: %s" % action)
        else:
            module.fail_json(msg="Unsupported alarm type: %s" % alarm_type)

        # Exit with result
        if changed:
            module.exit_json(changed=True, **result)
        else:
            module.fail_json(msg=result.get('msg', 'Unknown error'))

    except Exception as e:
        module.fail_json(msg="An error occurred: %s" % str(e))


if __name__ == '__main__':
    main()
