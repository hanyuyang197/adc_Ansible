#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Horizon Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible_collections.horizon.adc.plugins.module_utils.adc_base import ADCBase
from ansible.module_utils.basic import AnsibleModule
import json
__metaclass__ = type

DOCUMENTATION = r'''
---
module: adc_system_log_get
short_description: Manage ADC system log retrieval
description:
  - Retrieve various types of logs from ADC devices.
  - Supports service logs, audit logs, NAT logs, DNS logs.
  - Supports listing, clearing, and downloading logs.
version_added: "1.0.0"
options:
  action:
    description:
      - The action to perform on logs.
      - C(list) to list logs.
      - C(clear) to clear logs.
      - C(download) to download logs.
    type: str
    required: true
    choices: [ list, clear, download ]
  log_type:
    description:
      - The type of log to operate on.
    type: str
    required: true
    choices: [ service, audit, nat, dns, coredump, system ]
  # Options for list action
  direct:
    description:
      - Log pagination direction.
      - 0:first, 1:prev, 2:next, 3:last
    type: int
    choices: [0, 1, 2, 3]
    default: 0
  index:
    description:
      - Log index for pagination.
    type: int
    default: 0
  limit:
    description:
      - Output limit for logs.
    type: int
    default: 30
  level:
    description:
      - Output logs at this level and above.
      - 0: emergency, 1: alert, 2: critical, 3: error, 4: warning, 5: notification, 6: information, 7: debugging
    type: int
    choices: [0, 1, 2, 3, 4, 5, 6, 7]
    default: 7
  # Options for audit log list
  start_time:
    description:
      - Filter logs by start time (seconds since epoch).
    type: int
    default: 0
  time_range:
    description:
      - Filter logs by time range (seconds).
    type: int
    default: 0
  user_name:
    description:
      - Filter audit logs by username.
    type: str
author:
  - Horizon Inc.
'''

EXAMPLES = r'''
- name: Get service logs
  adc_system_log_get:
    action: list
    log_type: service
    direct: 0
    index: 0
    limit: 10
    level: 7

- name: Get audit logs for user
  adc_system_log_get:
    action: list
    log_type: audit
    user_name: admin
    limit: 20

- name: Clear NAT logs
  adc_system_log_get:
    action: clear
    log_type: nat

- name: Download DNS logs
  adc_system_log_get:
    action: download
    log_type: dns
'''

RETURN = r'''
logs:
  description: List of logs when action=list
  returned: when action=list
  type: list
  sample: [
    {
      "index": 254,
      "item": "Oct 25 2024 14:48:58 local0.info Horizon/common/ lldp: add neighbor for Ethernet6/0..."
    }
  ]
result:
  description: Result message when action=clear
  returned: when action=clear
  type: str
  sample: "Logs cleared successfully"
file_path:
  description: Path to downloaded file when action=download
  returned: when action=download
  type: str
  sample: "/tmp/service_logs.txt"
'''


def list_logs(module, adc_base, log_type):
    """List logs of specified type"""
    # Prepare the action based on log type
    action_map = {
        'service': 'log.service.list',
        'audit': 'log.audit.list',
        'nat': 'log.nat.list',
        'dns': 'log.dns.list'
    }

    if log_type not in action_map:
        module.fail_json(
            msg="Unsupported log type for list action: %s" % log_type)

    # Prepare parameters
    params = {
        'direct': module.params['direct'],
        'index': module.params['index'],
        'limit': module.params['limit']
    }

    # Add type-specific parameters
    if log_type == 'service':
        params['level'] = module.params['level']
    elif log_type == 'audit':
        params['start_time'] = module.params['start_time']
        params['time_range'] = module.params['time_range']
        params['user_name'] = module.params['user_name']

    # Make API call
    response = adc_base.make_request('POST', action_map[log_type], data=params)

    if response.get('success'):
        return True, {'logs': response.get('data', [])}
    else:
        return False, {'msg': response.get('msg', 'Failed to list logs')}


def clear_logs(module, adc_base, log_type):
    """Clear logs of specified type"""
    # Prepare the action based on log type
    action_map = {
        'service': 'log.service.clear',
        'audit': 'log.audit.clear',
        'nat': 'log.nat.clear',
        'dns': 'log.dns.clear'
    }

    if log_type not in action_map:
        module.fail_json(
            msg="Unsupported log type for clear action: %s" % log_type)

    # Make API call
    response = adc_base.make_request('GET', action_map[log_type])

    if response.get('success'):
        return True, {'result': 'Logs cleared successfully'}
    else:
        return False, {'msg': response.get('msg', 'Failed to clear logs')}


def download_logs(module, adc_base, log_type):
    """Download logs of specified type"""
    # Prepare the action based on log type
    action_map = {
        'service': 'log.service.download',
        'audit': 'log.audit.download',
        'nat': 'log.nat.download',
        'dns': 'log.dns.download',
        'coredump': 'log.coredump.download',
        'system': 'log.system.download'
    }

    if log_type not in action_map:
        module.fail_json(
            msg="Unsupported log type for download action: %s" % log_type)

    # Make API call to download file
    file_path = "/tmp/%s_logs.txt" % log_type
    success = adc_base.download_file(action_map[log_type], file_path)

    if success:
        return True, {'file_path': file_path}
    else:
        return False, {'msg': 'Failed to download logs'}


def main():
    # Define module arguments
    argument_spec = dict(
        action=dict(type='str', required=True, choices=[
                    'list', 'clear', 'download']),
        log_type=dict(type='str', required=True, choices=[
                      'service', 'audit', 'nat', 'dns', 'coredump', 'system']),
        # Options for list action
        direct=dict(type='int', choices=[0, 1, 2, 3], default=0),
        index=dict(type='int', default=0),
        limit=dict(type='int', default=30),
        level=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6, 7], default=7),
        # Options for audit log list
        start_time=dict(type='int', default=0),
        time_range=dict(type='int', default=0),
        user_name=dict(type='str'),
    )

    # Create Ansible module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ('log_type', 'audit', ['user_name'], True),
        ]
    )

    # Extract module parameters
    action = module.params['action']
    log_type = module.params['log_type']

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(changed=False)

    # Create ADC base object
    adc_base = ADCBase(module)

    try:
        # Perform requested action
        if action == 'list':
            changed, result = list_logs(module, adc_base, log_type)
        elif action == 'clear':
            changed, result = clear_logs(module, adc_base, log_type)
        elif action == 'download':
            changed, result = download_logs(module, adc_base, log_type)
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
