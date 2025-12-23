#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Horizon Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
import json
import sys
__metaclass__ = type

# ADC API响应解析函数


def format_adc_response_for_ansible(response_data, action="", changed_default=True):
    """
    格式化ADC响应为Ansible模块返回格式

    Args:
        response_data (str/dict): API响应数据
        action (str): 执行的操作名称
        changed_default (bool): 默认的changed状态

    Returns:
        tuple: (success, result_dict)
            - success (bool): 操作是否成功
            - result_dict (dict): Ansible模块返回字典
    """

    # 初始化返回结果
    result = {
        'success': False,
        'result': '',
        'errcode': '',
        'errmsg': '',
        'data': {}
    }

    try:
        # 如果是字符串，尝试解析为JSON
        if isinstance(response_data, str):
            parsed_data = json.loads(response_data)
        else:
            parsed_data = response_data

        result['data'] = parsed_data

        # 提取基本字段
        result['result'] = parsed_data.get('result', '')
        result['errcode'] = parsed_data.get('errcode', '')
        result['errmsg'] = parsed_data.get('errmsg', '')

        # 判断操作是否成功
        if result['result'].lower() == 'success':
            result['success'] = True
        else:
            # 处理幂等性问题 - 检查错误信息中是否包含"已存在"等表示已存在的关键词
            errmsg = result['errmsg'].lower() if isinstance(
                result['errmsg'], str) else str(result['errmsg']).lower()
            if any(keyword in errmsg for keyword in ['已存在', 'already exists', 'already exist', 'exists']):
                # 幂等性处理：如果是因为已存在而导致的"失败"，实际上算成功
                result['success'] = True
                result['result'] = 'success (already exists)'

    except json.JSONDecodeError as e:
        result['errmsg'] = "JSON解析失败: %s" % str(e)
        result['errcode'] = 'JSON_PARSE_ERROR'
    except Exception as e:
        result['errmsg'] = "响应解析异常: %s" % str(e)
        result['errcode'] = 'PARSE_EXCEPTION'

    # 格式化为Ansible返回格式
    if result['success']:
        # 操作成功
        result_dict = {
            'changed': changed_default,
            'msg': '%s操作成功' % action if action else '操作成功',
            'response': result['data']
        }

        # 如果是幂等性成功（已存在），调整消息
        if 'already exists' in result['result']:
            result_dict['changed'] = False
            result_dict['msg'] = '%s操作成功（资源已存在，无需更改）' % action if action else '操作成功（资源已存在，无需更改）'

        return True, result_dict
    else:
        # 操作失败
        result_dict = {
            'changed': False,
            'msg': '%s操作失败' % action if action else '操作失败',
            'error': {
                'result': result['result'],
                'errcode': result['errcode'],
                'errmsg': result['errmsg']
            },
            'response': result['data']
        }
        return False, result_dict


def send_request(url, data=None, method='GET'):
    """发送HTTP请求到ADC设备"""
    try:
        if method == 'POST' and data:
            data_json = json.dumps(data)
            data_bytes = data_json.encode('utf-8')

            if sys.version_info[0] >= 3:
                # Python 3
                import urllib.request as urllib_request
                req = urllib_request.Request(url, data=data_bytes)
                req.add_header('Content-Type', 'application/json')
            else:
                # Python 2
                import urllib2 as urllib_request
                req = urllib_request.Request(url, data=data_bytes)
                req.add_header('Content-Type', 'application/json')
        else:
            if sys.version_info[0] >= 3:
                # Python 3
                import urllib.request as urllib_request
                req = urllib_request.Request(url)
            else:
                # Python 2
                import urllib2 as urllib_request
                req = urllib_request.Request(url)

        response = urllib_request.urlopen(req)
        response_data = response.read()

        # 正确处理响应数据的编码
        if isinstance(response_data, bytes):
            # 尝试UTF-8解码，如果失败则使用latin1作为后备
            try:
                response_text = response_data.decode('utf-8')
            except UnicodeDecodeError:
                response_text = response_data.decode('latin1')
        else:
            response_text = response_data

        result = json.loads(response_text)

        # 标准化响应格式
        # 成功响应保持原样
        # 错误响应标准化为 {"result":"error","errcode":"REQUEST_ERROR","errmsg":"..."}
        if isinstance(result, dict) and 'status' in result and result['status'] is False:
            # 修复Unicode解码错误：确保错误消息正确处理中文字符
            error_msg = result.get('msg', '')
            if isinstance(error_msg, bytes):
                try:
                    error_msg = error_msg.decode('utf-8')
                except UnicodeDecodeError:
                    error_msg = error_msg.decode('latin1')

            return {
                'result': 'error',
                'errcode': 'REQUEST_ERROR',
                'errmsg': error_msg if error_msg else '请求失败'
            }
        else:
            return result
    except UnicodeDecodeError as e:
        # 如果JSON解析失败，直接返回原始响应数据
        return {
            'result': 'success',
            'data': str(response_data) if response_data is not None else '',
            'raw_response': True
        }
    except Exception as e:
        return {
            'result': 'error',
            'errcode': 'REQUEST_EXCEPTION',
            'errmsg': str(e)
        }


DOCUMENTATION = r'''
---
module: adc_system_ha_vrrp
short_description: Manage ADC system HA VRRP configuration
description:
  - Manage High Availability VRRP configuration for ADC devices.
  - Supports global configuration, groups, heartbeat interfaces, floating IPs, and more.
version_added: "1.0.0"
options:
  vrrp_component:
    description:
      - The VRRP component to manage.
    type: str
    required: true
    choices: [ global, group, heartbeat_eth, heartbeat_trunk, floating_ip, force_offline, gateway_track, route_track, pool_track, ethernet_track, trunk_track, vlan_track ]
  action:
    description:
      - The action to perform on the VRRP component.
    type: str
    required: true
    choices: [ get, set, add, list, edit, delete ]
  # Global configuration parameters
  enabled:
    description:
      - Enable VRRP (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  as_model:
    description:
      - Enable AS mode (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  unit_id:
    description:
      - Unit ID (0-8).
    type: int
  interval:
    description:
      - Heartbeat interval (1-255).
    type: int
  retry:
    description:
      - Retry count (2-200).
    type: int
  delay:
    description:
      - Delay (1-100).
    type: int
  cluster_id:
    description:
      - Cluster ID (0-7).
    type: int
  # Group parameters
  group_id:
    description:
      - Group ID (0-8).
    type: int
  priority:
    description:
      - Priority (1-200).
    type: int
  preempt_th:
    description:
      - Preempt threshold (0-100).
    type: int
  preempt_dis:
    description:
      - Disable preempt (0=enabled, 1=disabled).
    type: int
    choices: [0, 1]
  priority_threshold:
    description:
      - Priority threshold (1-200).
    type: int
  failback_first_device:
    description:
      - Failback to first device (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  order_list:
    description:
      - Order list (space-separated integers).
    type: str
  # Heartbeat interface parameters
  slot:
    description:
      - Ethernet interface slot (0-8).
    type: int
  port:
    description:
      - Ethernet interface port (0-7).
    type: int
  vlan_id:
    description:
      - VLAN ID (0-4094).
    type: int
  trunk_id:
    description:
      - Trunk ID (1-8).
    type: int
  # Floating IP parameters
  floating_ip:
    description:
      - Floating IP address (IPv4/IPv6).
    type: str
  # Force offline parameters
  force_offline:
    description:
      - Force offline (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  all_partitions:
    description:
      - Apply to all partitions (0=disabled, 1=enabled).
    type: int
    choices: [0, 1]
  # Track parameters
  ip:
    description:
      - IP address for tracking (IPv4/IPv6).
    type: str
  netmask:
    description:
      - Netmask or prefix for route tracking.
    type: str
  pool_name:
    description:
      - Pool name for pool tracking.
    type: str
  min_up_members:
    description:
      - Minimum up members for pool tracking.
    type: int
  member_priority:
    description:
      - Member priority for trunk tracking.
    type: int
  timeout:
    description:
      - Timeout for VLAN tracking.
    type: int
author:
  - Horizon Inc.
'''

EXAMPLES = r'''
- name: Get VRRP global configuration
  adc_system_ha_vrrp:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    vrrp_component: global
    action: get

- name: Enable VRRP
  adc_system_ha_vrrp:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    vrrp_component: global
    action: set
    enabled: 1
    unit_id: 1
    interval: 10
    retry: 3

- name: Add VRRP group
  adc_system_ha_vrrp:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    vrrp_component: group
    action: add
    group_id: 1
    priority: 150

- name: List VRRP groups
  adc_system_ha_vrrp:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    vrrp_component: group
    action: list

- name: Add Ethernet heartbeat interface
  adc_system_ha_vrrp:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    vrrp_component: heartbeat_eth
    action: add
    slot: 0
    port: 1
    vlan_id: 100

- name: Add floating IP
  adc_system_ha_vrrp:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    vrrp_component: floating_ip
    action: add
    group_id: 1
    floating_ip: "192.168.1.100"

- name: Set force offline
  adc_system_ha_vrrp:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    vrrp_component: force_offline
    action: set
    force_offline: 1

- name: Add gateway tracking
  adc_system_ha_vrrp:
    ip: "192.168.1.1"
    authkey: "your_auth_key"
    vrrp_component: gateway_track
    action: add
    group_id: 1
    priority: 50
    ip: "10.0.0.1"
'''

RETURN = r'''
global_config:
  description: VRRP global configuration when vrrp_component=global and action=get
  returned: when vrrp_component=global and action=get
  type: dict
  sample: {
    "enabled": 1,
    "as_mode": 0,
    "unit_id": 1,
    "interval": 10,
    "retry": 3
  }
groups:
  description: List of VRRP groups when vrrp_component=group and action=list
  returned: when vrrp_component=group and action=list
  type: list
  sample: [
    {
      "group_id": 1,
      "priority": 150,
      "preempt_th": 0
    }
  ]
msg:
  description: Result message
  returned: always
  type: str
  sample: "VRRP group added successfully"
'''


def adc_get_vrrp_global_config(module, adc_base):
    """Get VRRP global configuration"""
    # Make API call
    response = adc_base.make_request('GET', 'vrrp.global.get')

    if response.get('success'):
        return True, {'global_config': response.get('data', {})}
    else:
        return False, {'msg': response.get('msg', 'Failed to get VRRP global configuration')}


def adc_set_vrrp_global_config(module, adc_base):
    """Set VRRP global configuration"""
    # Prepare parameters
    params = {}

    # Add optional parameters if provided
    if module.params['enabled'] is not None:
        params['enabled'] = module.params['enabled']
    if module.params['as_model'] is not None:
        params['as_model'] = module.params['as_model']
    if module.params['unit_id'] is not None:
        params['unit_id'] = module.params['unit_id']
    if module.params['interval'] is not None:
        params['interval'] = module.params['interval']
    if module.params['retry'] is not None:
        params['retry'] = module.params['retry']
    if module.params['delay'] is not None:
        params['delay'] = module.params['delay']
    if module.params['cluster_id'] is not None:
        params['cluster_id'] = module.params['cluster_id']

    # Make API call
    response = adc_base.make_request('POST', 'vrrp.global.set', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Set VRRP global configuration", True)
    return success, result_dict


def adc_add_vrrp_group(module, adc_base):
    """Add VRRP group"""
    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['group_id'] is not None:
        params['group_id'] = module.params['group_id']
    else:
        module.fail_json(msg="group_id is required for add group action")

    # Optional parameters
    if module.params['priority'] is not None:
        params['priority'] = module.params['priority']
    if module.params['preempt_th'] is not None:
        params['preempt_th'] = module.params['preempt_th']
    if module.params['preempt_dis'] is not None:
        params['preempt_dis'] = module.params['preempt_dis']
    if module.params['priority_threshold'] is not None:
        params['priority_threshold'] = module.params['priority_threshold']
    if module.params['failback_first_device'] is not None:
        params['failback_first_device'] = module.params['failback_first_device']
    if module.params['order_list'] is not None:
        params['order_list'] = module.params['order_list']

    # Make API call
    response = adc_base.make_request('POST', 'vrrp.group.add', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Add VRRP group", True)
    return success, result_dict


def adc_list_vrrp_groups(module, adc_base):
    """List VRRP groups"""
    # Make API call
    response = adc_base.make_request('GET', 'vrrp.group.list')

    if response.get('success'):
        return True, {'groups': response.get('data', [])}
    else:
        return False, {'msg': response.get('msg', 'Failed to list VRRP groups')}


def adc_add_heartbeat_eth(module, adc_base):
    """Add Ethernet heartbeat interface"""
    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['slot'] is not None:
        params['slot'] = module.params['slot']
    else:
        module.fail_json(msg="slot is required for add heartbeat_eth action")

    if module.params['port'] is not None:
        params['port'] = module.params['port']
    else:
        module.fail_json(msg="port is required for add heartbeat_eth action")

    if module.params['vlan_id'] is not None:
        params['vlan_id'] = module.params['vlan_id']
    else:
        module.fail_json(
            msg="vlan_id is required for add heartbeat_eth action")

    # Make API call
    response = adc_base.make_request('POST', 'vrrp.heart_eth.add', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Add Ethernet heartbeat interface", True)
    return success, result_dict


def adc_add_floating_ip(module, adc_base):
    """Add floating IP"""
    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['group_id'] is not None:
        params['group_id'] = module.params['group_id']
    else:
        module.fail_json(msg="group_id is required for add floating_ip action")

    if module.params['floating_ip'] is not None:
        params['floating_ip'] = module.params['floating_ip']
    else:
        module.fail_json(
            msg="floating_ip is required for add floating_ip action")

    # Make API call
    response = adc_base.make_request(
        'POST', 'vrrp.floating_ip.add', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Add floating IP", True)
    return success, result_dict


def adc_set_force_offline(module, adc_base):
    """Set force offline"""
    # Prepare parameters
    params = {}

    # Optional parameters
    if module.params['force_offline'] is not None:
        params['force_offline'] = module.params['force_offline']
    if module.params['all_partitions'] is not None:
        params['all_partitions'] = module.params['all_partitions']

    # Make API call
    response = adc_base.make_request(
        'POST', 'vrrp.force_offline.set', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Set force offline", True)
    return success, result_dict


def adc_add_gateway_track(module, adc_base):
    """Add gateway tracking"""
    # Prepare parameters
    params = {}

    # Required parameters
    if module.params['group_id'] is not None:
        params['group_id'] = module.params['group_id']
    else:
        module.fail_json(
            msg="group_id is required for add gateway_track action")

    if module.params['priority'] is not None:
        params['priority'] = module.params['priority']
    else:
        module.fail_json(
            msg="priority is required for add gateway_track action")

    if module.params['track_ip'] is not None:
        params['ip'] = module.params['track_ip']
    else:
        module.fail_json(
            msg="track_ip is required for add gateway_track action")

    # Make API call
    response = adc_base.make_request(
        'POST', 'vrrp.track.gateway.add', data=params)

    # Format response
    success, result_dict = adc_base.format_adc_response_for_ansible(
        response, "Add gateway tracking", True)
    return success, result_dict


def main():
    # Define module arguments
    argument_spec = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        vrrp_component=dict(type='str', required=True, choices=[
            'global', 'group', 'heartbeat_eth', 'heartbeat_trunk',
            'floating_ip', 'force_offline', 'gateway_track', 'route_track',
            'pool_track', 'ethernet_track', 'trunk_track', 'vlan_track'
        ]),
        action=dict(type='str', required=True, choices=[
                    'get', 'set', 'add', 'list', 'edit', 'delete']),
        # Global configuration parameters
        enabled=dict(type='int', choices=[0, 1]),
        as_model=dict(type='int', choices=[0, 1]),
        unit_id=dict(type='int'),
        interval=dict(type='int'),
        retry=dict(type='int'),
        delay=dict(type='int'),
        cluster_id=dict(type='int'),
        # Group parameters
        group_id=dict(type='int'),
        priority=dict(type='int'),
        preempt_th=dict(type='int'),
        preempt_dis=dict(type='int', choices=[0, 1]),
        priority_threshold=dict(type='int'),
        failback_first_device=dict(type='int', choices=[0, 1]),
        order_list=dict(type='str'),
        # Heartbeat interface parameters
        slot=dict(type='int'),
        port=dict(type='int'),
        vlan_id=dict(type='int'),
        trunk_id=dict(type='int'),
        # Floating IP parameters
        floating_ip=dict(type='str'),
        # Force offline parameters
        force_offline=dict(type='int', choices=[0, 1]),
        all_partitions=dict(type='int', choices=[0, 1]),
        # Track parameters
        track_ip=dict(type='str'),
        netmask=dict(type='str'),
        pool_name=dict(type='str'),
        min_up_members=dict(type='int'),
        member_priority=dict(type='int'),
        timeout=dict(type='int'),
    )

    # Create Ansible module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ('vrrp_component', 'group', ['action']),
            ('vrrp_component', 'heartbeat_eth', ['action']),
            ('vrrp_component', 'floating_ip', ['action']),
            ('vrrp_component', 'gateway_track', ['action']),
        ]
    )

    # Extract module parameters
    vrrp_component = str(module.params['vrrp_component'])
    action = str(module.params['action'])

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(changed=False)

    # Create ADC base object
    adc_base = ADCBase(module)

    try:
        # Perform requested action based on VRRP component
        if vrrp_component == 'global':
            if action == 'get':
                changed, result = adc_get_vrrp_global_config(module, adc_base)
            elif action == 'set':
                changed, result = adc_set_vrrp_global_config(module, adc_base)
            else:
                module.fail_json(
                    msg="Unsupported action for global: %s" % action)
        elif vrrp_component == 'group':
            if action == 'add':
                changed, result = adc_add_vrrp_group(module, adc_base)
            elif action == 'list':
                changed, result = adc_list_vrrp_groups(module, adc_base)
            else:
                module.fail_json(
                    msg="Unsupported action for group: %s" % action)
        elif vrrp_component == 'heartbeat_eth':
            if action == 'add':
                changed, result = adc_add_heartbeat_eth(module, adc_base)
            else:
                module.fail_json(
                    msg="Unsupported action for heartbeat_eth: %s" % action)
        elif vrrp_component == 'floating_ip':
            if action == 'add':
                changed, result = adc_add_floating_ip(module, adc_base)
            else:
                module.fail_json(
                    msg="Unsupported action for floating_ip: %s" % action)
        elif vrrp_component == 'force_offline':
            if action == 'set':
                changed, result = adc_set_force_offline(module, adc_base)
            else:
                module.fail_json(
                    msg="Unsupported action for force_offline: %s" % action)
        elif vrrp_component == 'gateway_track':
            if action == 'add':
                changed, result = adc_add_gateway_track(module, adc_base)
            else:
                module.fail_json(
                    msg="Unsupported action for gateway_track: %s" % action)
        else:
            module.fail_json(
                msg="Unsupported VRRP component: %s" % vrrp_component)

        # Exit with result
        if changed:
            module.exit_json(changed=True, **result)
        else:
            module.fail_json(msg=result.get('msg', 'Unknown error'))

    except Exception as e:
        module.fail_json(msg="An error occurred: %s" % str(e))


if __name__ == '__main__':
    main()
