#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import re
import glob

def scan_project_structure():
    """扫描项目结构，获取所有模块文件和YAML文件"""
    
    # 扫描library目录下的所有Python模块文件
    module_files = {}
    library_dir = 'library'
    if os.path.exists(library_dir):
        for file in os.listdir(library_dir):
            if file.endswith('.py') and file.startswith('adc_'):
                module_name = file.replace('.py', '')
                module_files[module_name] = os.path.join(library_dir, file)
    
    # 扫描playbooksNew目录下的所有YAML文件
    yaml_files = {}
    playbooks_dir = 'playbooksNew'
    if os.path.exists(playbooks_dir):
        for file in os.listdir(playbooks_dir):
            if file.endswith('.yml'):
                yaml_name = file.replace('.yml', '')
                yaml_files[yaml_name] = os.path.join(playbooks_dir, file)
    
    return module_files, yaml_files

def extract_functions_from_module(module_path):
    """从模块文件中提取所有函数名"""
    functions = []
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 使用正则表达式匹配函数定义
            function_pattern = r'def\s+(adc_[a-zA-Z_][a-zA-Z0-9_]*)\('
            functions = re.findall(function_pattern, content)
    except Exception as e:
        print(f"读取模块文件 {module_path} 时出错: {e}")
    
    return functions

def map_api_to_module(api_name):
    """将API名称映射到模块和函数名"""
    # API格式: slb.node.list -> adc_slb_node, adc_list_nodes
    parts = api_name.split('.')
    
    if len(parts) < 3:
        return None, None, None
    
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
    elif action == 'edit':
        function_name = f"adc_edit_{parts[1]}"
    elif action == 'clear':
        function_name = f"adc_clear_{parts[1]}"
    else:
        function_name = f"adc_{action}_{parts[1]}"
    
    # YAML文件名: adc_slb_node_list.yml
    yaml_name = f"{module_prefix}_{action}"
    
    return module_prefix, function_name, yaml_name

def main():
    """主函数"""
    
    # 读取Excel文件
    df = pd.read_excel('ansible_yml_path.xlsx')
    
    # 扫描项目结构
    module_files, yaml_files = scan_project_structure()
    
    print(f"发现模块文件: {len(module_files)} 个")
    print(f"发现YAML文件: {len(yaml_files)} 个")
    
    # 为每个API检查映射关系
    updated_count = 0
    
    for idx, row in df.iterrows():
        api_name = row['api对应']
        if pd.isna(api_name):
            continue
        
        # 获取预期的模块和函数名
        module_prefix, expected_function, expected_yaml = map_api_to_module(api_name)
        
        if not module_prefix:
            continue
        
        # 检查模块文件是否存在
        module_exists = False
        actual_module_name = None
        actual_function_name = None
        
        # 尝试匹配模块文件
        for module_name, module_path in module_files.items():
            if module_name.startswith(module_prefix):
                # 检查函数是否存在
                functions = extract_functions_from_module(module_path)
                
                # 首先尝试匹配预期的函数名
                if expected_function in functions:
                    module_exists = True
                    actual_module_name = module_name
                    actual_function_name = expected_function
                    break
                else:
                    # 如果没有精确匹配，尝试找到相似函数
                    for func in functions:
                        if func.startswith('adc_') and ('list' in func or 'get' in func or 'add' in func):
                            module_exists = True
                            actual_module_name = module_name
                            actual_function_name = func
                            break
        
        # 检查YAML文件是否存在
        yaml_exists = False
        actual_yaml_name = None
        
        for yaml_name, yaml_path in yaml_files.items():
            if expected_yaml and yaml_name == expected_yaml:
                yaml_exists = True
                actual_yaml_name = yaml_name
                break
            elif expected_yaml and expected_yaml in yaml_name:
                yaml_exists = True
                actual_yaml_name = yaml_name
                break
        
        # 如果模块和函数都存在，更新Excel
        if module_exists and actual_function_name:
            # 更新H列：模块文件相对路径
            df.at[idx, '模块文件相对路径'] = f"library/{actual_module_name}"
            # 更新I列：模块名
            df.at[idx, '模块名'] = actual_module_name
            # 更新J列：Action名
            df.at[idx, 'Action名'] = actual_function_name
            
            updated_count += 1
            print(f"✓ 已更新: {api_name} -> {actual_module_name}.{actual_function_name}")
        else:
            # 清空不存在的映射
            df.at[idx, '模块文件相对路径'] = ''
            df.at[idx, '模块名'] = ''
            df.at[idx, 'Action名'] = ''
            print(f"✗ 缺失: {api_name}")
    
    # 保存更新后的Excel文件
    df.to_excel('ansible_yml_path.xlsx', index=False)
    
    print(f"\n更新完成！共更新了 {updated_count} 个API的映射关系")
    print(f"总API数量: {len(df)}")
    
    # 统计缺失情况
    missing_count = len(df[df['模块文件相对路径'].isna() | (df['模块文件相对路径'] == '')])
    print(f"缺失映射的API数量: {missing_count}")

if __name__ == "__main__":
    main()