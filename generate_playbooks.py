#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
根据library目录下的模块文件生成对应的YAML playbook文件
"""

import os
import re
from pathlib import Path

def extract_actions_from_module(module_file):
    """从模块文件中提取action信息"""
    with open(module_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找choices中的action列表
    choices_match = re.search(r'choices=\[(.*?)\]', content, re.DOTALL)
    if choices_match:
        choices_str = choices_match.group(1)
        # 提取action名称
        actions = re.findall(r'[\'"]([^\'"]+)[\'"]', choices_str)
        return actions
    return []

def get_function_api_action_mapping(module_file):
    """获取模块中函数名到API action的映射"""
    with open(module_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有函数定义和对应的API action
    mapping = {}
    
    # 查找所有函数定义
    func_matches = list(re.finditer(r'def\s+adc_(\w+)\s*\([^)]*\):', content))
    for i, match in enumerate(func_matches):
        function_name = match.group(1)  # 如 'arp_ipv4_list'
        
        # 在该函数定义和下一个函数定义之间查找API action
        func_start = match.end()
        if i < len(func_matches) - 1:
            # 如果不是最后一个函数，到下一个函数定义为止
            next_func_start = func_matches[i + 1].start()
            func_content = content[func_start:next_func_start]
        else:
            # 如果是最后一个函数，到文件末尾
            func_content = content[func_start:]
        
        # 直接查找特定的URL模式并提取API action
        search_str = 'url = "http://%s/adcapi/v2.0/?authkey=%s&action='
        start_pos = func_content.find(search_str)
        if start_pos != -1:
            # 找到匹配的字符串，提取后面的API action
            start_pos += len(search_str)  # 移动到action=后面
            # 找到引号结束的位置
            end_pos = func_content.find('"', start_pos)
            if end_pos != -1:
                api_action = func_content[start_pos:end_pos]
                mapping[function_name] = api_action
    
    return mapping

def get_action_to_api_action_mapping(module_file):
    """获取模块中action到API action的直接映射"""
    with open(module_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 首先获取函数名到API action的映射
    func_api_mapping = get_function_api_action_mapping(module_file)
    
    # 获取choices中的actions
    choices_match = re.search(r'choices=\[(.*?)\]', content, re.DOTALL)
    if not choices_match:
        return {}
    
    choices_str = choices_match.group(1)
    actions = re.findall(r'[\'"]([^\'"]+)[\'"]', choices_str)
    
    # 创建action到API action的映射
    action_mapping = {}
    
    for action in actions:
        matched_api_action = None
        
        # 策略1: 检查函数名是否包含action
        for func_name, api_action in func_api_mapping.items():
            if action in func_name or func_name.endswith(f"_{action}") or func_name.startswith(f"{action}_"):
                matched_api_action = api_action
                break
        
        # 策略2: 检查API action是否包含action
        if not matched_api_action:
            for func_name, api_action in func_api_mapping.items():
                if action in api_action or api_action.endswith(f".{action}"):
                    matched_api_action = api_action
                    break
        
        # 策略3: 检查API action的最后部分是否与action匹配
        if not matched_api_action:
            for func_name, api_action in func_api_mapping.items():
                if api_action.split('.')[-1] == action:
                    matched_api_action = api_action
                    break
        
        # 策略4: 检查是否存在部分匹配（更智能的匹配）
        if not matched_api_action:
            for func_name, api_action in func_api_mapping.items():
                # 尝试更智能的匹配 - 将action和函数名、API action分解成部分进行匹配
                api_parts = api_action.split('.')
                action_parts = action.split('_')
                
                # 检查action的各个部分是否在API的各个部分中
                if len(action_parts) > 0:
                    # 如果action是list_profiles，查找包含list和profiles的API
                    action_contains_list = 'list' in action
                    action_contains_get = 'get' in action
                    action_contains_add = 'add' in action
                    action_contains_edit = 'edit' in action
                    action_contains_delete = 'delete' in action or 'del' in action
                    
                    api_contains_list = 'list' in api_parts
                    api_contains_get = 'get' in api_parts
                    api_contains_add = 'add' in api_parts
                    api_contains_edit = 'edit' in api_parts
                    api_contains_del = 'del' in api_parts
                    
                    # 匹配操作类型
                    operation_match = (
                        (action_contains_list and api_contains_list) or
                        (action_contains_get and api_contains_get) or
                        (action_contains_add and api_contains_add) or
                        (action_contains_edit and api_contains_edit) or
                        (action_contains_delete and api_contains_del)
                    )
                    
                    # 检查是否包含相似的名词部分
                    noun_match = False
                    if '_' in action:
                        # 提取名词部分（非操作词部分）
                        noun_parts = [part for part in action_parts if part not in ['list', 'get', 'add', 'edit', 'delete', 'del']]
                        for noun in noun_parts:
                            if noun in api_action:
                                noun_match = True
                                break
                    
                    if operation_match and (noun_match or len([p for p in action_parts if p not in ['list', 'get', 'add', 'edit', 'delete', 'del']]) == 0):
                        matched_api_action = api_action
                        break
        
        # 策略5: 检查函数名和API action是否与模块名相关
        if not matched_api_action:
            module_name = Path(module_file).stem
            if module_name.startswith('adc_'):
                module_name = module_name[4:]
            
            for func_name, api_action in func_api_mapping.items():
                # 检查API action是否包含模块相关信息
                if module_name.replace('_', '.') in api_action and action in api_action:
                    matched_api_action = api_action
                    break
        
        # 策略6: 特殊处理 - 对于execute action，尝试从函数名推断实际操作
        if not matched_api_action and action == 'execute':
            for func_name, api_action in func_api_mapping.items():
                # 对于execute action，函数名通常包含实际操作类型
                # 比如 adc_interface_mgmt_set 对应 interface.mgmt.set
                # 从函数名中提取操作类型
                import re as regex
                # 查找函数名中最后一个下划线后的部分（通常是操作类型）
                match = regex.search(r'_(set|get|add|edit|del|delete|list|statis|clear|upload|download|match|execute)$', func_name)
                if match:
                    actual_operation = match.group(1)
                    # 检查API action是否包含这个操作类型
                    if actual_operation in api_action:
                        matched_api_action = api_action
                        break
        
        # 策略7: 特殊处理 - 对于通用action如list_profiles，尝试匹配模式
        if not matched_api_action and '_' in action:
            # 比如action是list_profiles，需要匹配list_*_profiles模式的函数
            action_parts = action.split('_')
            if 'list' in action_parts and 'profiles' in action_parts:
                # 查找包含list和profiles的函数，不管中间是什么
                for func_name, api_action in func_api_mapping.items():
                    if 'list' in func_name and 'profile' in func_name and 'list' in api_action and 'profile' in api_action:
                        # 检查API action的结构是否匹配
                        if 'list' in api_action.split('.') and ('profile' in api_action or 'profiles' in api_action):
                            matched_api_action = api_action
                            break
            elif 'add' in action_parts and 'profile' in action_parts:
                for func_name, api_action in func_api_mapping.items():
                    if 'add' in func_name and 'profile' in func_name and 'add' in api_action and 'profile' in api_action:
                        matched_api_action = api_action
                        break
            elif 'get' in action_parts and 'profile' in action_parts:
                for func_name, api_action in func_api_mapping.items():
                    if 'get' in func_name and 'profile' in func_name and 'get' in api_action and 'profile' in api_action:
                        matched_api_action = api_action
                        break
            elif 'edit' in action_parts and 'profile' in action_parts:
                for func_name, api_action in func_api_mapping.items():
                    if 'edit' in func_name and 'profile' in func_name and 'edit' in api_action and 'profile' in api_action:
                        matched_api_action = api_action
                        break
            elif 'delete' in action_parts and 'profile' in action_parts:
                for func_name, api_action in func_api_mapping.items():
                    if ('delete' in func_name or 'del' in func_name) and 'profile' in func_name and ('del' in api_action or 'delete' in api_action) and 'profile' in api_action:
                        matched_api_action = api_action
                        break
        
        action_mapping[action] = matched_api_action
    
    return action_mapping

def get_chinese_description_from_module(module_file, action):
    """从模块文件中获取对应action的中文描述"""
    with open(module_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取模块名（不含adc_前缀和.py后缀）
    module_name = Path(module_file).stem
    if module_name.startswith('adc_'):
        module_name = module_name[4:]  # 去掉'adc_'前缀
    
    # 将action转换为对应的函数名格式
    # 对于大多数模块，函数名是 adc_{action}，如 adc_add_node
    # 对于一些模块，函数名是 adc_{module}_{action}，如 adc_arp_ipv4_add
    possible_function_names = [
        f"adc_{action}",  # 标准格式
        f"adc_{module_name}_{action}"  # 模块特定格式
    ]
    
    for function_name in possible_function_names:
        # 查找函数定义
        func_pattern = f'def {function_name}('
        func_start_pos = content.find(func_pattern)
        if func_start_pos != -1:
            # 找到函数定义，查找函数定义后的文档字符串
            # 找到函数定义行的结束位置
            func_def_end = content.find(':', func_start_pos)
            if func_def_end != -1:
                # 查找函数体开始位置
                body_start = content.find('\n', func_def_end)
                if body_start != -1:
                    # 跳过可能的注释行，查找文档字符串
                    pos = body_start + 1
                    # 跳过空白行
                    while pos < len(content) and content[pos].isspace():
                        pos += 1
                    
                    # 查找 """ 或 ''' 开头的文档字符串
                    if content[pos:pos+3] == '"""':
                        doc_start = pos + 3
                        doc_end = content.find('"""', doc_start)
                        if doc_end != -1:
                            docstring = content[doc_start:doc_end]
                            return docstring.strip()
                    elif content[pos:pos+3] == "'''":
                        doc_start = pos + 3
                        doc_end = content.find("'''", doc_start)
                        if doc_end != -1:
                            docstring = content[doc_start:doc_end]
                            return docstring.strip()
    
    # 如果没找到，返回action的简单中文解释
    return action.replace('_', ' ')

def generate_playbook_content(module_name, action, description, api_action=None):
    """生成playbook内容"""
    # 生成YAML内容
    yaml_content = f"""---
- name: {description}
  collections:
    - horizon.modules
  hosts: adc_servers
  gather_facts: no
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

    - name: 执行 {description}
      {module_name}:
        ip: "{{{{ inventory_hostname }}}}"
        authkey: "{{{{ login_result.authkey }}}}"
        action: "{action}"
        # API action: {api_action if api_action else 'N/A'}
        # 以下为可选参数
      register: result
      when: login_result is succeeded

    - name: 显示 {description} 结果
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
"""
    return yaml_content

def main():
    # 获取当前工作目录
    current_dir = Path('.')
    
    # 扫描library目录下的所有Python模块
    library_dir = current_dir / 'library'
    if not library_dir.exists():
        print(f"目录 {library_dir} 不存在")
        return
    
    for module_file in library_dir.glob('*.py'):
        print(f"处理模块: {module_file.name}")
        
        # 提取模块名（去掉.py后缀）
        module_name = module_file.stem
        if module_name.startswith('adc_'):
            module_display_name = module_name
        else:
            module_display_name = f"adc_{module_name}"
        
        # 从模块中提取action
        actions = extract_actions_from_module(module_file)
        
        if not actions:
            print(f"  未找到actions: {module_file.name}")
            continue
        
        print(f"  找到 {len(actions)} 个actions: {actions}")
        
        # 获取函数到API action的映射
        api_action_mapping = get_function_api_action_mapping(module_file)
        print(f"  函数API action映射: {api_action_mapping}")
        
        # 获取action到API action的直接映射
        action_to_api_mapping = get_action_to_api_action_mapping(module_file)
        print(f"  Action到API action映射: {action_to_api_mapping}")
        
        # 为每个action生成YAML文件
        for action in actions:
            # 从模块文件中获取中文描述
            description = get_chinese_description_from_module(module_file, action)
            
            # 获取对应的API action
            # 优先使用action到API action的直接映射
            api_action = action_to_api_mapping.get(action)
            
            # 如果直接映射没有找到，使用原来的逻辑
            if api_action is None:
                possible_function_names = [
                    action,  # 直接使用action作为函数名后缀 - adc_{action}
                    f"{module_name[4:]}_{action}" if module_name.startswith('adc_') else f"{module_name}_{action}",  # 模块名_action格式 - adc_{module}_{action}
                ]
                
                # 也尝试在映射中查找包含action的函数名
                for func_name, mapped_api_action in api_action_mapping.items():
                    # 如果映射中的函数名包含action，也考虑使用
                    if action in func_name or func_name.endswith(f"_{action}"):
                        api_action = mapped_api_action
                        break
                
                # 如果上述方法都没找到，尝试在可能的函数名中查找
                if api_action is None:
                    for func_name in possible_function_names:
                        if func_name in api_action_mapping:
                            api_action = api_action_mapping[func_name]
                            break
            
            # 生成YAML文件名，使用模块名+action名确保唯一性
            # 例如: adc_arp_ipv4_add.yml
            yaml_filename = f"{module_name}_{action}.yml"
            yaml_path = current_dir / 'playbooksNew' / yaml_filename
            
            # 生成YAML内容
            yaml_content = generate_playbook_content(module_display_name, action, description, api_action)
            
            # 写入YAML文件
            os.makedirs(yaml_path.parent, exist_ok=True)
            with open(yaml_path, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
            
            print(f"    生成: {yaml_path} - {description} (API: {api_action})")

if __name__ == '__main__':
    main()