#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Horizon Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.horizon.modules.plugins.module_utils.adc_common import (
    make_adc_request,
    format_adc_response,
    check_adc_auth,
    handle_adc_error,
    build_adc_params,
    validate_adc_params,
    adc_result_check,
    adc_format_output,
    build_params_with_optional,
    make_http_request,
    get_param_if_exists,
    create_adc_module_args,
    adc_response_to_ansible_result,
    format_adc_response_for_ansible
)
from ansible_collections.horizon.modules.plugins.module_utils.adc_common import (
    make_adc_request,
    format_adc_response,
    check_adc_auth,
    handle_adc_error,
    build_adc_params,
    validate_adc_params,
    adc_result_check,
    adc_format_output,
    build_params_with_optional,
    make_http_request,
    get_param_if_exists,
    create_adc_module_args,
    adc_response_to_ansible_result,
    format_adc_response_for_ansible
)
import json
import sys
__metaclass__ = type

# ADC API响应解析函数


def send_request(url, data=None, method='GET'):
    """发送HTTP请求到ADC设备"""
    import sys
    response_data = None
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

        # 安全地解析JSON响应
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # 如果不是有效的JSON格式，返回原始响应
            return {
                'result': 'error',
                'errcode': 'JSON_PARSE_ERROR',
                'errmsg': f'响应不是有效的JSON格式: {response_text}'
            }

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
        # 如果解码失败，直接返回错误信息
        return {
            'result': 'error',
            'errcode': 'UNICODE_DECODE_ERROR',
            'errmsg': f'响应解码失败: {str(e)}'
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


def adc_get_vrrp_global_config(module):
    """Get VRRP global configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.global.get" % (
        ip, authkey)

    # Make API call
    response = send_request(url, method='GET')

    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'global_config': response.get('data', {})}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "获取VRRP全局配置失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'global_config': response}
    else:
        return False, {'msg': '响应数据格式错误'}


def adc_set_vrrp_global_config(module):
    """Set VRRP global configuration"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.global.set" % (
        ip, authkey)

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
    response = send_request(url, params, method='POST')

    # Format response
    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': 'VRRP全局配置设置成功'}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "设置VRRP全局配置失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'response': response}
    else:
        return False, {'msg': '响应数据格式错误'}


def adc_add_vrrp_group(module):
    """Add VRRP group"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.group.add" % (
        ip, authkey)

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
    response = send_request(url, params, method='POST')

    # Format response
    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': 'VRRP组添加成功'}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "添加VRRP组失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'response': response}
    else:
        return False, {'msg': '响应数据格式错误'}


def adc_list_vrrp_groups(module):
    """List VRRP groups"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.group.list" % (
        ip, authkey)

    # Make API call
    response = send_request(url, method='GET')

    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'groups': response.get('data', [])}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "获取VRRP组列表失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'groups': response}
    else:
        return False, {'msg': '响应数据格式错误'}


def adc_add_heartbeat_eth(module):
    """Add Ethernet heartbeat interface"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.heart_eth.add" % (
        ip, authkey)

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
    response = send_request(url, params, method='POST')

    # Format response
    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': '以太网心跳接口添加成功'}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "添加以太网心跳接口失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'response': response}
    else:
        return False, {'msg': '响应数据格式错误'}


def adc_add_floating_ip(module):
    """Add floating IP"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.floating_ip.add" % (
        ip, authkey)

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
    response = send_request(url, params, method='POST')

    # Format response
    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': '浮动IP添加成功'}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "添加浮动IP失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'response': response}
    else:
        return False, {'msg': '响应数据格式错误'}


def adc_set_force_offline(module):
    """Set force offline"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.force_offline.set" % (
        ip, authkey)

    # Prepare parameters
    params = {}

    # Optional parameters
    if module.params['force_offline'] is not None:
        params['force_offline'] = module.params['force_offline']
    if module.params['all_partitions'] is not None:
        params['all_partitions'] = module.params['all_partitions']

    # Make API call
    response = send_request(url, params, method='POST')

    # Format response
    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': '强制离线设置成功'}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "设置强制离线失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'response': response}
    else:
        return False, {'msg': '响应数据格式错误'}


def adc_add_gateway_track(module):
    """Add gateway tracking"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action=vrrp.track.gateway.add" % (
        ip, authkey)

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
    response = send_request(url, params, method='POST')

    # Format response
    if isinstance(response, dict):
        if response.get('result', '').lower() == 'success':
            # 成功响应
            return True, {'msg': '网关跟踪添加成功'}
        elif 'errcode' in response and response['errcode']:
            # 错误响应
            return False, {'msg': "添加网关跟踪失败: %s" % response.get('errmsg', '未知错误')}
        else:
            # 直接返回数据
            return True, {'response': response}
    else:
        return False, {'msg': '响应数据格式错误'}


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

    try:
        # Perform requested action based on VRRP component
        if vrrp_component == 'global':
            if action == 'get':
                changed, result = adc_get_vrrp_global_config(module)
            elif action == 'set':
                changed, result = adc_set_vrrp_global_config(module)
            else:
                module.fail_json(
                    msg="Unsupported action for global: %s" % action)
        elif vrrp_component == 'group':
            if action == 'add':
                changed, result = adc_add_vrrp_group(module)
            elif action == 'list':
                changed, result = adc_list_vrrp_groups(module)
            else:
                module.fail_json(
                    msg="Unsupported action for group: %s" % action)
        elif vrrp_component == 'heartbeat_eth':
            if action == 'add':
                changed, result = adc_add_heartbeat_eth(module)
            else:
                module.fail_json(
                    msg="Unsupported action for heartbeat_eth: %s" % action)
        elif vrrp_component == 'floating_ip':
            if action == 'add':
                changed, result = adc_add_floating_ip(module)
            else:
                module.fail_json(
                    msg="Unsupported action for floating_ip: %s" % action)
        elif vrrp_component == 'force_offline':
            if action == 'set':
                changed, result = adc_set_force_offline(module)
            else:
                module.fail_json(
                    msg="Unsupported action for force_offline: %s" % action)
        elif vrrp_component == 'gateway_track':
            if action == 'add':
                changed, result = adc_add_gateway_track(module)
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
