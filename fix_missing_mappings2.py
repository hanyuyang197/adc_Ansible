#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import re
import glob

def scan_project_structure():
    """扫描项目结构"""
    
    # 扫描library目录
    module_files = {}
    if os.path.exists('library'):
        for file in os.listdir('library'):
            if file.endswith('.py') and file.startswith('adc_'):
                module_name = file.replace('.py', '')
                module_files[module_name] = os.path.join('library', file)
    
    # 扫描playbooksNew目录
    yaml_files = {}
    if os.path.exists('playbooksNew'):
        for file in os.listdir('playbooksNew'):
            if file.endswith('.yml'):
                yaml_name = file.replace('.yml', '')
                yaml_files[yaml_name] = os.path.join('playbooksNew', file)
    
    return module_files, yaml_files

def extract_functions_from_module(module_path):
    """从模块文件中提取函数名"""
    functions = []
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 匹配函数定义
            pattern = r'def\s+(adc_[a-zA-Z_][a-zA-Z0-9_]*)\('
            functions = re.findall(pattern, content)
    except:
        pass
    
    return functions

def map_api_to_module(api_name):
    """将API映射到模块"""
    parts = api_name.split('.')
    
    if len(parts) < 3:
        return None, None
    
    # 模块名: slb.node -> adc_slb_node
    module_prefix = f"adc_{parts[0]}_{parts[1]}"
    
    # 函数名: list -> adc_list_nodes
    action = parts[2]
    if action == 'list':
        function_name = f"adc_list_{parts[1]}s"
    elif action == 'add':
        function_name = f"adc_add_{parts[1]}"
    elif action == 'del':
        function_name = f"adc_delete_{parts[1]}"
    elif action == 'get':
        function_name = f"adc_get_{parts[1]}"
    else:
        function_name = f"adc_{action}_{parts[1]}"
    
    return module_prefix, function_name

def main():
    # 读取Excel
    df = pd.read_excel('ansible_yml_path.xlsx')
    
    # 扫描项目
    module_files, yaml_files = scan_project_structure()
    
    print(f"模块文件: {len(module_files)}个")
    print(f"YAML文件: {len(yaml_files)}个")
    
    # 检查特定API
    api_to_check = 'slb.node.list'
    row = df[df['api对应'] == api_to_check]
    
    if not row.empty:
        idx = row.index[0]
        print(f"\n检查 {api_to_check}:")
        
        # 检查模块
        module_prefix, expected_function = map_api_to_module(api_to_check)
        print(f"预期模块: {module_prefix}")
        print(f"预期函数: {expected_function}")
        
        # 检查模块文件是否存在
        if module_prefix in module_files:
            print(f"模块文件存在: {module_files[module_prefix]}")
            functions = extract_functions_from_module(module_files[module_prefix])
            print(f"模块中的函数: {functions}")
            
            if expected_function in functions:
                print(f"函数 {expected_function} 存在")
                # 更新Excel
                df.at[idx, '模块文件相对路径'] = f"library/{module_prefix}"
                df.at[idx, '模块名'] = module_prefix
                df.at[idx, 'Action名'] = expected_function
                print("已更新Excel")
            else:
                print(f"函数 {expected_function} 不存在")
        else:
            print("模块文件不存在")
    
    # 保存
    df.to_excel('ansible_yml_path.xlsx', index=False)
    print("\nExcel文件已保存")

if __name__ == "__main__":
    main()