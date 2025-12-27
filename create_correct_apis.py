#!/usr/bin/env python3
"""
根据缺少api.txt文件生成缺失的API模块和对应的YML文件
这次正确处理API名称，不添加错误的符号
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

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        print(f"处理第{line_num}行: {repr(line)}")  # 调试输出
        if line and not line[0].isdigit() and not line.startswith('--') and line not in ['', 'ntp服务器api缺少', '域名解析', 'snmp', '认证', 'vrrp', '日志', 'LLDP', '时间对象', '地址解析', '安全', '流量控制', '接口', 'SSl', '端口列表模板', '静态路由']:
            current_category = line.strip()
            print(f"  设置类别: {current_category}")
        elif line and line[0].isdigit():  # API行
            print(f"  检测到API行，尝试解析...")
            # 使用更简单的解析方法
            # 找到第一个'.'的位置，这是序号和描述的分隔点
            dot_index = line.find('.')
            if dot_index != -1:
                # 提取序号后的描述和API动作
                rest = line[dot_index + 1:].strip()
                # 找到描述和API动作之间的分隔
                # 通常描述和API之间有多个空格
                import re
                # 使用正则表达式分割，按多个空格分割
                parts = re.split(r'\\s{2,}', rest)  # 至少2个空格作为分隔符
                if len(parts) >= 2:
                    description = parts[0].strip()
                    api_action = parts[1].split()[0] if parts[1].split(
                    ) else parts[1]  # 获取第一个词作为API动作
                    # 确保API action不包含错误的前缀符号
                    clean_api_action = api_action.lstrip('- ')
                    print(
                        f"  成功解析: 描述='{description}', 动作='{clean_api_action}'")
                    apis.append({
                        'category': current_category,
                        'description': description,
                        'action': clean_api_action
                    })
                else:
                    # 如果没有找到多个空格，尝试其他方法
                    # 查找描述和API动作的分隔
                    words = rest.split()
                    if len(words) >= 2:
                        # 假设第一个词是描述，其余是API动作
                        description = words[0]
                        api_action = ' '.join(words[1:])
                        # 确保API action不包含错误的前缀符号
                        clean_api_action = api_action.lstrip('- ')
                        print(
                            f"  成功解析(备用方法): 描述='{description}', 动作='{clean_api_action}'")
                        apis.append({
                            'category': current_category,
                            'description': description,
                            'action': clean_api_action
                        })
            else:
                print(f"  解析失败: 未找到序号分隔符")

    print(f"总共找到 {len(apis)} 个API")
    return apis


def create_module_content(api_info):
    """创建模块文件内容"""
    # 从API动作中提取模块名称
    action_parts = api_info['action'].split('.')

    # 提取模块名称部分（通常是前几个部分，不包括操作动词）
    module_name_parts = []
    for i, part in enumerate(action_parts):
        if part in ['add', 'get', 'list', 'edit', 'del', 'set', 'download', 'upload', 'clear', 'statis', 'stats']:
            break
        module_name_parts.append(part)

    if not module_name_parts:
        module_name_parts = action_parts[:-
                                         1] if len(action_parts) > 1 else action_parts

    module_name = '_'.join(module_name_parts)
    action_suffix = action_parts[-1] if action_parts else 'general'

    # 将模块名转换为Python兼容格式，移除特殊字符
    module_name = re.sub(r'[^a-zA-Z0-9_]', '_', module_name)
    action_suffix = re.sub(r'[^a-zA-Z0-9_]', '_', action_suffix)

    # 确保模块名不以数字开头
    if module_name and module_name[0].isdigit():
        module_name = f"api_{module_name}"

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
    elif 'time' in api_info['action'] or 'timerange' in api_info['action']:
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
    elif 'interface' in api_info['action'] or 'ethernet' in api_info['action'] or 'trunk' in api_info['action'] or 've' in api_info['action']:
        main_param = "interface"
    elif 'vrrp' in api_info['action']:
        main_param = "group"

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
        '{main_param}', 'description', 'status', 'config', 'setting', 'value', 'enable'
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
        setting=dict(type='dict', required=False),
        value=dict(type='str', required=False),
        enable=dict(type='bool', required=False)
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
    # 从文件名中提取模块名
    module_name = module_filename.replace('adc_', '').replace('.py', '')

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
    elif 'time' in api_info['action'] or 'timerange' in api_info['action']:
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
    elif 'interface' in api_info['action'] or 'ethernet' in api_info['action'] or 'trunk' in api_info['action'] or 've' in api_info['action']:
        main_param = "interface"
    elif 'vrrp' in api_info['action']:
        main_param = "group"

    yml_content = f'''---
- name: {api_info['description']}
  collections:
    - horizon.modules
  hosts: adc_servers
  gather_facts: no
  vars:
    # adc_ip变量已移除，使用inventory_hostname替代
    adc_username: "admin"
    adc_password: "admin"

  tasks:
    - name: 登录ADC设备
      adc_login:
        ip: "{{{{ inventory_hostname }}}}"
        username: "{{{{ adc_username }}}}"
        password: "{{{{ adc_password }}}}"
      register: login_result

    - name: 显示登录结果
      debug:
        var: login_result

    - name: 执行 {api_info['description']}
      horizon.modules.adc_{module_name}:
        ip: "{{{{ inventory_hostname }}}}"
        authkey: "{{{{ login_result.authkey }}}}"
        action: execute
        {main_param}: "example_value"
        # 根据实际需求添加更多参数
      register: result
      when: login_result is succeeded

    - name: 显示 {api_info['description']} 结果
      debug:
        var: result
      when: result is defined

    - name: 登出ADC设备
      adc_logout:
        ip: "{{{{ inventory_hostname }}}}"
        authkey: "{{{{ login_result.authkey }}}}"
      register: logout_result
      when: login_result is succeeded

    - name: 显示登出结果
      debug:
        var: logout_result
      when: logout_result is defined
'''
    return yml_content, f"{module_name}_{api_info['action'].split('.')[-1]}.yml"


def main():
    # 读取API列表
    apis = extract_apis_from_txt('缺少api.txt')

    print(f"发现 {len(apis)} 个需要生成的API")

    # 创建library目录（如果不存在）
    library_dir = Path('library')
    library_dir.mkdir(exist_ok=True)

    # 创建playbooks目录结构
    playbooks_dir = Path('playbooks')
    playbooks_dir.mkdir(exist_ok=True)

    # 根据API类别创建不同的playbook目录
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

        # 根据API类别确定playbook目录
        category = api['category'].lower()
        if 'ntp' in category or 'ntp' in api['action']:
            playbook_dir = playbooks_dir / 'system'
        elif 'snmp' in category or 'snmp' in api['action']:
            playbook_dir = playbooks_dir / 'system'
        elif 'aaa' in category or 'aaa' in api['action']:
            playbook_dir = playbooks_dir / 'system'
        elif 'vrrp' in category or 'vrrp' in api['action']:
            playbook_dir = playbooks_dir / 'system'
        elif 'log' in category or 'log' in api['action']:
            playbook_dir = playbooks_dir / 'system'
        elif 'lldp' in category or 'lldp' in api['action']:
            playbook_dir = playbooks_dir / 'network'
        elif 'arp' in category or 'arp' in api['action']:
            playbook_dir = playbooks_dir / 'network'
        elif 'route' in category or 'route' in api['action']:
            playbook_dir = playbooks_dir / 'network'
        elif 'interface' in category or 'interface' in api['action']:
            playbook_dir = playbooks_dir / 'network'
        elif 'slb' in api['action'] or 'ssl' in api['action'] or 'persist' in api['action'] or 'profile' in api['action']:
            playbook_dir = playbooks_dir / 'slbnew'
        elif 'security' in category or 'ddos' in api['action'] or 'syn' in api['action']:
            playbook_dir = playbooks_dir / 'network'
        elif 'tc' in api['action'] or 'flow' in category:  # 流量控制
            playbook_dir = playbooks_dir / 'network'
        else:
            # 根据action的第一个部分来判断
            first_part = api['action'].split(
                '.')[0] if '.' in api['action'] else api['action']
            if first_part in ['system', 'aaa', 'ntp', 'snmp', 'log', 'timerange']:
                playbook_dir = playbooks_dir / 'system'
            elif first_part in ['network', 'interface', 'arp', 'route', 'lldp', 'tc']:
                playbook_dir = playbooks_dir / 'network'
            elif first_part in ['slb', 'ssl', 'persist', 'profile']:
                playbook_dir = playbooks_dir / 'slbnew'
            else:
                playbook_dir = playbooks_dir / 'system'  # 默认放到system目录

        # 创建playbook目录
        playbook_dir.mkdir(exist_ok=True)

        # 生成对应的playbook
        yml_content, yml_filename = create_playbook_content(
            api, module_filename)

        # 创建playbook文件
        yml_path = playbook_dir / yml_filename
        with open(yml_path, 'w', encoding='utf-8') as f:
            f.write(yml_content)

        print(f"  创建playbook: {yml_path}")
        generated_count += 1

    print(f"\n完成! 生成了 {generated_count} 个API模块和对应的playbook文件")
    print(f"模块文件位置: {library_dir}/")
    print(f"Playbook文件位置: {playbooks_dir}/ 目录下按类别存放")


if __name__ == "__main__":
    main()
