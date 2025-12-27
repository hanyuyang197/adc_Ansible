#!/usr/bin/env python3
"""
根据缺少api.txt文件生成缺失的API模块和对应的YML文件
"""

import os
import re
from pathlib import Path


def extract_apis_from_txt(file_path):
    """从txt文件中提取API列表"""
    apis = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 按行分割并提取API
    lines = content.split('\n')
    current_category = ""

    for line in lines:
        line = line.strip()
        if line and not line[0].isdigit():  # 类别标题行
            current_category = line
        elif line and line[0].isdigit():  # API行
            # 提取API格式: "序号.描述 ---api.action"
            match = re.match(r'\d+\.(.*?)---(.+)', line)
            if match:
                description = match.group(1).strip()
                api_action = match.group(2).strip()
                apis.append({
                    'category': current_category,
                    'description': description,
                    'action': api_action
                })

    return apis


def create_module_content(api_info):
    """创建模块文件内容"""
    # 从API动作中提取模块名称
    action_parts = api_info['action'].split('.')
    module_name = '_'.join(
        action_parts[:-1]) if len(action_parts) > 1 else action_parts[0]
    action_suffix = action_parts[-1] if action_parts else 'general'

    # 将模块名转换为Python兼容格式
    module_name = re.sub(r'[^a-zA-Z0-9_]', '_', module_name)
    action_suffix = re.sub(r'[^a-zA-Z0-9_]', '_', action_suffix)

    # 生成函数名
    func_name = f"adc_{module_name}_{action_suffix}"

    # 确定主要参数（通常在action中包含的名词）
    main_param = "name"  # 默认参数名
    if 'server' in api_info['action']:
        main_param = "server"
    elif 'ntp' in api_info['action']:
        main_param = "server"
    elif 'snmp' in api_info['action']:
        main_param = "name"
    elif 'user' in api_info['action']:
        main_param = "username"
    elif 'group' in api_info['action']:
        main_param = "group"
    elif 'view' in api_info['action']:
        main_param = "view"
    elif 'time' in api_info['action']:
        main_param = "name"
    elif 'arp' in api_info['action']:
        main_param = "ip"
    elif 'route' in api_info['action']:
        main_param = "destination"
    elif 'cert' in api_info['action']:
        main_param = "name"
    elif 'key' in api_info['action']:
        main_param = "name"
    elif 'profile' in api_info['action']:
        main_param = "name"

    module_content = f'''#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.horizon.modules.plugins.module_utils.adc_common import (
    make_adc_request,
    format_adc_response,
    check_adc_auth,
    handle_adc_error,
    build_adc_params,
    validate_adc_params,
    adc_result_check,

    format_adc_response_for_ansible
)
import json
import sys


def {func_name}(module):
    """{api_info['description']}"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action={api_info['action']}" % (ip, authkey)

    # 构造请求数据
    request_data = {{
        "ip": ip,
        "authkey": authkey
    }}
    
    # 定义可选参数列表（根据API具体需求调整）
    optional_params = [
        '{main_param}', 'description', 'status', 'config', 'setting'
        # 根据具体API需求添加更多参数
    ]
    
    # 添加可选参数
    for param in optional_params:
        if get_param_if_exists(module, param) is not None:
            request_data[param] = get_param_if_exists(module, param)

    # 转换为JSON格式
    post_data = json.dumps(request_data)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理编码
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={{
                                         'Content-Type': 'application/json'}})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={{
                                         'Content-Type': 'application/json'}})
            response = urllib_request.urlopen(req)
            response_data = response.read()

    except Exception as e:
        module.fail_json(msg="{api_info['description']}失败: %s" % str(e))

    # 使用通用响应解析函数
    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "{api_info['description']}", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=['execute']),
        {main_param}=dict(type='str', required=False),
        description=dict(type='str', required=False),
        status=dict(type='str', required=False),
        config=dict(type='dict', required=False),
        setting=dict(type='dict', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 执行操作
    {func_name}(module)


if __name__ == '__main__':
    main()
'''
    return module_content, f"adc_{module_name}.py"


def create_playbook_content(api_info, module_filename):
    """创建对应的playbook YML内容"""
    action_parts = api_info['action'].split('.')
    module_name = '_'.join(
        action_parts[:-1]) if len(action_parts) > 1 else action_parts[0]

    # 确定主要参数（通常在action中包含的名词）
    main_param = "name"  # 默认参数名
    if 'server' in api_info['action']:
        main_param = "server"
    elif 'ntp' in api_info['action']:
        main_param = "server"
    elif 'snmp' in api_info['action']:
        main_param = "name"
    elif 'user' in api_info['action']:
        main_param = "username"
    elif 'group' in api_info['action']:
        main_param = "group"
    elif 'view' in api_info['action']:
        main_param = "view"
    elif 'time' in api_info['action']:
        main_param = "name"
    elif 'arp' in api_info['action']:
        main_param = "ip"
    elif 'route' in api_info['action']:
        main_param = "destination"
    elif 'cert' in api_info['action']:
        main_param = "name"
    elif 'key' in api_info['action']:
        main_param = "name"
    elif 'profile' in api_info['action']:
        main_param = "name"

    yml_content = f'''---
- name: {api_info['description']}
  hosts: localhost
  gather_facts: no
  tasks:
    - name: Execute {api_info['description']}
      horizon.modules.adc_{module_name}:
        ip: "{{{{ target_ip }}}}"
        authkey: "{{{{ target_authkey }}}}"
        action: execute
        {main_param}: "example_value"
        # 根据实际需求添加更多参数
      register: result

    - name: Display result
      debug:
        var: result
'''
    return yml_content, f"{module_name}_{action_parts[-1] if action_parts else 'general'}.yml"


def main():
    # 读取API列表
    apis = extract_apis_from_txt('缺少api.txt')

    print(f"发现 {len(apis)} 个需要生成的API")

    # 创建library目录（如果不存在）
    library_dir = Path('library')
    library_dir.mkdir(exist_ok=True)

    # 创建playbooks目录（如果不存在）
    playbooks_dir = Path('playbooks')
    playbooks_dir.mkdir(exist_ok=True)

    # 为playbooks创建专门的子目录
    missing_apis_dir = playbooks_dir / 'missing_apis'
    missing_apis_dir.mkdir(exist_ok=True)

    generated_count = 0

    for api in apis:
        print(f"正在处理: {api['action']} - {api['description']}")

        # 生成模块内容
        module_content, module_filename = create_module_content(api)

        # 检查模块是否已存在
        module_path = library_dir / module_filename
        if module_path.exists():
            print(f"  模块已存在，跳过: {module_filename}")
            continue

        # 创建模块文件
        with open(module_path, 'w', encoding='utf-8') as f:
            f.write(module_content)

        print(f"  创建模块: {module_filename}")

        # 生成对应的playbook
        yml_content, yml_filename = create_playbook_content(
            api, module_filename)

        # 创建playbook文件
        yml_path = missing_apis_dir / yml_filename
        with open(yml_path, 'w', encoding='utf-8') as f:
            f.write(yml_content)

        print(f"  创建playbook: {yml_filename}")
        generated_count += 1

    print(f"\n完成! 生成了 {generated_count} 个API模块和对应的playbook文件")
    print(f"模块文件位置: {library_dir}/")
    print(f"Playbook文件位置: {missing_apis_dir}/")


if __name__ == "__main__":
    main()
