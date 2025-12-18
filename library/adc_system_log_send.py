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
module: adc_system_log_send
short_description: Manage ADC system log sending configuration
description:
  - Manage syslog server configuration for ADC devices.
  - Supports adding, listing, getting, editing, and deleting syslog server configurations.
version_added: "1.0.0"
options:
  action:
    description:
      - The action to perform on syslog server configuration.
    type: str
    required: true
    choices: [ add, list, get, edit, delete ]
  # Parameters for add/edit actions
  host:
    description:
      - Syslog server address (hostname/IPv4/IPv6).
    type: str
  port:
    description:
      - Syslog server port.
    type: int
  log_code:
    description:
      - Code encoding status (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  facility:
    description:
      - Syslog facility number (0-7).
    type: int
    choices: [0, 1, 2, 3, 4, 5, 6, 7]
  nat_log:
    description:
      - Send NAT logs (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  audit_log:
    description:
      - Send audit logs (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  service_log:
    description:
      - Send service logs (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  dns_log:
    description:
      - Send DNS logs (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  match_type:
    description:
      - Filter matching type.
      - 0: Disable filtering
      - 1: Level/event/keyword/module OR operation
      - 2: Level/event/keyword/module AND operation
    type: int
    choices: [0, 1, 2]
  level_filter:
    description:
      - Log level filter (0-7).
    type: int
    choices: [0, 1, 2, 3, 4, 5, 6, 7]
  event_list:
    description:
      - Event list array.
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
  keyword_filter:
    description:
      - Keyword filter.
    type: str
  module_filter:
    description:
      - Module filter (comma-separated modules).
    type: str
  keyword_type:
    description:
      - Keyword type (string or regular).
    type: str
    choices: [string, regular]
author:
  - Horizon Inc.
'''

EXAMPLES = r'''
- name: Add syslog server
  adc_system_log_send:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: add
    host: "10.66.30.129"
    port: 514
    nat_log: 1
    audit_log: 1
    service_log: 1
    dns_log: 1

- name: List syslog servers
  adc_system_log_send:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: list

- name: Get specific syslog server
  adc_system_log_send:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: get
    host: "10.66.30.129"
    port: 514

- name: Edit syslog server
  adc_system_log_send:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: edit
    host: "10.66.30.129"
    port: 514
    level_filter: 5
    keyword_filter: "error"

- name: Delete syslog server
  adc_system_log_send:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    action: delete
    host: "10.66.30.129"
    port: 514
'''

RETURN = r'''
servers:
  description: List of syslog servers when action=list
  returned: when action=list
  type: list
  sample: [
    {
      "host": "10.66.30.129",
      "port": 514,
      "log_code": 0,
      "facility": 1,
      "nat_log": 1,
      "audit_log": 1,
      "service_log": 1,
      "dns_log": 1
    }
  ]
server:
  description: Specific syslog server when action=get
  returned: when action=get
  type: dict
  sample: {
    "host": "10.66.30.129",
    "port": 514,
    "log_code": 0,
    "facility": 1,
    "nat_log": 1,
    "audit_log": 1,
    "service_log": 1,
    "dns_log": 1
  }
msg:
  description: Result message
  returned: always
  type: str
  sample: "Syslog server added successfully"
'''


def adc_add_syslog_server(module, adc_base):
    """Add syslog server configuration"""
    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['host'] is not None:
        params['host'] = module.params['host']
    else:
        module.fail_json(msg="host is required for add action")

    if module.params['port'] is not None:
        params['port'] = module.params['port']
    else:
        module.fail_json(msg="port is required for add action")

    # Optional parameters
    if module.params['log_code'] is not None:
        params['log_code'] = module.params['log_code']
    if module.params['facility'] is not None:
        params['facility'] = module.params['facility']
    if module.params['nat_log'] is not None:
        params['nat_log'] = module.params['nat_log']
    if module.params['audit_log'] is not None:
        params['audit_log'] = module.params['audit_log']
    if module.params['service_log'] is not None:
        params['service_log'] = module.params['service_log']
    if module.params['dns_log'] is not None:
        params['dns_log'] = module.params['dns_log']
    if module.params['match_type'] is not None:
        params['match_type'] = module.params['match_type']
    if module.params['level_filter'] is not None:
        params['level_filter'] = module.params['level_filter']
    if module.params['event_list'] is not None:
        params['event_list'] = module.params['event_list']
    if module.params['keyword_filter'] is not None:
        params['keyword_filter'] = module.params['keyword_filter']
    if module.params['module_filter'] is not None:
        params['module_filter'] = module.params['module_filter']
    if module.params['keyword_type'] is not None:
        params['keyword_type'] = module.params['keyword_type']

    # Make API call
    response = adc_base.make_request(
        'POST', 'log.syslog.server.add', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Add syslog server", True)
    return success, result_dict


def adc_list_syslog_servers(module, adc_base):
    """List syslog server configurations"""
    # Make API call
    response = adc_base.make_request('GET', 'log.syslog.server.list')

    if response.get('success'):
        return True, {'servers': response.get('data', [])}
    else:
        return False, {'msg': response.get('msg', 'Failed to list syslog servers')}


def adc_get_syslog_server(module, adc_base):
    """Get specific syslog server configuration"""
    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['host'] is not None:
        params['host'] = module.params['host']
    else:
        module.fail_json(msg="host is required for get action")

    if module.params['port'] is not None:
        params['port'] = module.params['port']
    else:
        module.fail_json(msg="port is required for get action")

    # Make API call
    response = adc_base.make_request(
        'POST', 'log.syslog.server.get', data=params)

    if response.get('success'):
        return True, {'server': response.get('data', {})}
    else:
        return False, {'msg': response.get('msg', 'Failed to get syslog server')}


def adc_edit_syslog_server(module, adc_base):
    """Edit syslog server configuration"""
    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['host'] is not None:
        params['host'] = module.params['host']
    else:
        module.fail_json(msg="host is required for edit action")

    if module.params['port'] is not None:
        params['port'] = module.params['port']
    else:
        module.fail_json(msg="port is required for edit action")

    # Optional parameters
    if module.params['log_code'] is not None:
        params['log_code'] = module.params['log_code']
    if module.params['facility'] is not None:
        params['facility'] = module.params['facility']
    if module.params['nat_log'] is not None:
        params['nat_log'] = module.params['nat_log']
    if module.params['audit_log'] is not None:
        params['audit_log'] = module.params['audit_log']
    if module.params['service_log'] is not None:
        params['service_log'] = module.params['service_log']
    if module.params['dns_log'] is not None:
        params['dns_log'] = module.params['dns_log']
    if module.params['match_type'] is not None:
        params['match_type'] = module.params['match_type']
    if module.params['level_filter'] is not None:
        params['level_filter'] = module.params['level_filter']
    if module.params['event_list'] is not None:
        params['event_list'] = module.params['event_list']
    if module.params['keyword_filter'] is not None:
        params['keyword_filter'] = module.params['keyword_filter']
    if module.params['module_filter'] is not None:
        params['module_filter'] = module.params['module_filter']
    if module.params['keyword_type'] is not None:
        params['keyword_type'] = module.params['keyword_type']

    # Make API call
    response = adc_base.make_request(
        'POST', 'log.syslog.server.edit', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Edit syslog server", True)
    return success, result_dict


def adc_delete_syslog_server(module, adc_base):
    """Delete syslog server configuration"""
    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['host'] is not None:
        params['host'] = module.params['host']
    else:
        module.fail_json(msg="host is required for delete action")

    if module.params['port'] is not None:
        params['port'] = module.params['port']
    else:
        module.fail_json(msg="port is required for delete action")

    # Make API call
    response = adc_base.make_request(
        'POST', 'log.syslog.server.del', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Delete syslog server", True)
    return success, result_dict


def main():
    # Define module arguments
    argument_spec = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
                    'add', 'list', 'get', 'edit', 'delete']),
        # Parameters for add/edit actions
        host=dict(type='str'),
        port=dict(type='int'),
        log_code=dict(type='int', choices=[0, 1]),
        facility=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6, 7]),
        nat_log=dict(type='int', choices=[0, 1]),
        audit_log=dict(type='int', choices=[0, 1]),
        service_log=dict(type='int', choices=[0, 1]),
        dns_log=dict(type='int', choices=[0, 1]),
        match_type=dict(type='int', choices=[0, 1, 2]),
        level_filter=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6, 7]),
        event_list=dict(type='list', elements='int'),
        keyword_filter=dict(type='str'),
        module_filter=dict(type='str'),
        keyword_type=dict(type='str', choices=['string', 'regular']),
    )

    # Create Ansible module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ('action', 'add', ['host', 'port']),
            ('action', 'get', ['host', 'port']),
            ('action', 'edit', ['host', 'port']),
            ('action', 'delete', ['host', 'port']),
        ]
    )

    # Extract module parameters
    action = str(module.params['action'])

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(changed=False)

    # Create ADC base object
    adc_base = ADCBase(module)

    try:
        # Perform requested action
        if action == 'add':
            changed, result = adc_add_syslog_server(module, adc_base)
        elif action == 'list':
            changed, result = adc_list_syslog_servers(module, adc_base)
        elif action == 'get':
            changed, result = adc_get_syslog_server(module, adc_base)
        elif action == 'edit':
            changed, result = adc_edit_syslog_server(module, adc_base)
        elif action == 'delete':
            changed, result = adc_delete_syslog_server(module, adc_base)
        else:
            module.fail_json(msg="Unsupported action: %s" % action)

        # Exit with result
        if changed:
            module.exit_json(changed=True, **result)
        else:
            module.fail_json(msg=result.get('msg', 'Unknown error'))

    except Exception as e:
        module.fail_json(msg="An error occurred: %s" % str(e))


if __name__ == '__main__':
    main()
