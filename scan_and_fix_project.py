#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import pandas as pd
import json

print("=== 开始扫描整个项目目录 ===")

# 读取Excel文件
df = pd.read_excel('ansible_yml_path.xlsx')

# 清空D、E、F、G列的内容
df.iloc[:, 3:7] = ''  # D、E、F、G列（索引3-6）
print("已清空D、E、F、G列内容")

# 扫描library目录下的所有Python模块文件
library_dir = 'library'
playbooks_dir = 'playbooksNew'

# 获取所有Python模块文件
module_files = []
if os.path.exists(library_dir):
    for file in os.listdir(library_dir):
        if file.endswith('.py') and file.startswith('adc_'):
            module_files.append(file)

print(f"发现 {len(module_files)} 个模块文件")

# 获取所有YAML文件
yaml_files = []
if os.path.exists(playbooks_dir):
    for file in os.listdir(playbooks_dir):
        if file.endswith('.yml'):
            yaml_files.append(file)

print(f"发现 {len(yaml_files)} 个YAML文件")

# 构建模块函数字典
module_functions = {}
for module_file in module_files:
    module_path = os.path.join(library_dir, module_file)
    with open(module_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 提取所有函数定义
        functions = re.findall(r'def\s+(\w+)\(module\):', content)
        module_functions[module_file] = functions

print(f"\n模块函数统计:")
for module, funcs in module_functions.items():
    print(f"{module}: {len(funcs)} 个函数")

# 构建YAML文件映射
yaml_mapping = {}
for yaml_file in yaml_files:
    # 解析YAML文件名获取对应的action
    # 格式: adc_slb_node_add_node.yml -> add_node
    if yaml_file.startswith('adc_') and yaml_file.endswith('.yml'):
        parts = yaml_file[4:-4].split('_')  # 去掉adc_和.yml
        if len(parts) >= 2:
            action = parts[-1]  # 最后一个部分通常是action
            yaml_mapping[yaml_file] = action

print(f"\nYAML文件映射:")
for yaml, action in list(yaml_mapping.items())[:10]:
    print(f"{yaml} -> {action}")

# API到模块函数的映射规则
def api_to_module_function(api):
    """将API转换为可能的模块函数名"""
    parts = api.split('.')
    if len(parts) < 3:
        return [], [], []
    
    category = parts[0]  # slb
    subcategory = parts[1]  # node, healthcheck等
    
    if len(parts) == 3:
        # slb.node.add
        resource = parts[1]  # node
        action = parts[2]   # add
        
        possible_modules = [
            f'adc_{category}_{resource}.py',  # adc_slb_node.py
        ]
        
        possible_functions = [
            f'adc_{action}_{resource}',      # adc_add_node
            f'adc_{resource}_{action}',      # adc_node_add
            f'{action}_{resource}',          # add_node
            f'{resource}_{action}',          # node_add
        ]
        
        possible_yamls = [
            f'adc_{category}_{resource}_{action}_{resource}.yml',  # adc_slb_node_add_node.yml
            f'adc_{category}_{resource}_{action}.yml',             # adc_slb_node_add.yml
        ]
        
    elif len(parts) >= 4:
        # slb.healthcheck.script.list
        resource = parts[2]  # script
        action = parts[3]    # list
        
        possible_modules = [
            f'adc_{category}_{subcategory}.py',          # adc_slb_healthcheck.py
            f'adc_{category}_{subcategory}_{resource}.py', # adc_slb_healthcheck_script.py
        ]
        
        possible_functions = [
            f'adc_{resource}_{action}',                  # adc_script_list
            f'adc_{action}_{resource}',                  # adc_list_script
            f'adc_{subcategory}_{resource}_{action}',    # adc_healthcheck_script_list
            f'{resource}_{action}',                      # script_list
            f'{action}_{resource}',                      # list_script
        ]
        
        possible_yamls = [
            f'adc_{category}_{subcategory}_{resource}_{action}.yml',  # adc_slb_healthcheck_script_list.yml
            f'adc_{category}_{resource}_{action}.yml',                # adc_slb_script_list.yml
        ]
    else:
        return [], [], []
    
    # 过滤掉None值
    possible_functions = [f for f in possible_functions if f]
    possible_yamls = [f for f in possible_yamls if f]
    
    return possible_modules, possible_functions, possible_yamls

print("\n=== 开始分析每个API ===")

# 分析每个API
api_analysis = {}
for idx, row in df.iterrows():
    api = str(row.iloc[1]).strip()
    if not api or api == 'nan':
        continue
    
    possible_modules, possible_functions, possible_yamls = api_to_module_function(api)
    
    # 检查模块是否存在
    found_module = None
    found_function = None
    found_yaml = None
    
    for module in possible_modules:
        if module in module_files:
            # 检查模块中的函数
            for func in possible_functions:
                if func in module_functions.get(module, []):
                    found_module = module
                    found_function = func
                    break
            if found_module:
                break
    
    # 检查YAML文件是否存在
    for yaml_pattern in possible_yamls:
        for yaml_file in yaml_files:
            if yaml_file == yaml_pattern:
                found_yaml = yaml_file
                break
        if found_yaml:
            break
    
    api_analysis[api] = {
        'module': found_module,
        'function': found_function,
        'yaml': found_yaml,
        'possible_modules': possible_modules,
        'possible_functions': possible_functions,
        'possible_yamls': possible_yamls
    }

# 统计结果
found_count = sum(1 for info in api_analysis.values() if info['module'] and info['function'])
missing_count = len(api_analysis) - found_count

print(f"\n=== 分析结果 ===")
print(f"总API数量: {len(api_analysis)}")
print(f"找到完整模块函数的API: {found_count}")
print(f"缺失模块函数的API: {missing_count}")

# 显示一些缺失的API示例
print("\n缺失模块函数的API示例:")
missing_apis = [api for api, info in api_analysis.items() if not info['module'] or not info['function']]
for i, api in enumerate(missing_apis[:10]):
    info = api_analysis[api]
    print(f"{i+1}. {api}")
    print(f"   可能模块: {info['possible_modules']}")
    print(f"   可能函数: {info['possible_functions']}")
    print(f"   可能YAML: {info['possible_yamls']}")

# 更新Excel文件
print("\n=== 更新Excel文件 ===")

for idx, row in df.iterrows():
    api = str(row.iloc[1]).strip()
    if not api or api == 'nan' or api not in api_analysis:
        continue
    
    info = api_analysis[api]
    
    # 填充H、I、J列
    if info['module'] and info['function']:
        module_path = f"library/{info['module'][:-3]}"  # 去掉.py
        df.iloc[idx, 7] = module_path        # H列: 模块文件相对路径
        df.iloc[idx, 8] = info['module'][:-3] # I列: 模块名
        df.iloc[idx, 9] = info['function']   # J列: Action名
    else:
        # 留空
        df.iloc[idx, 7] = ''
        df.iloc[idx, 8] = ''
        df.iloc[idx, 9] = ''

# 保存Excel文件
df.to_excel('ansible_yml_path.xlsx', index=False)
print("已保存更新后的Excel文件")

# 显示最终的列结构
print("\n=== 最终Excel结构 ===")
print("列名:", df.columns.tolist())
print("总列数:", len(df.columns))

# 显示一些示例数据
print("\n示例数据:")
for i in range(min(5, len(df))):
    api = df.iloc[i, 1]
    h_col = df.iloc[i, 7]
    i_col = df.iloc[i, 8]
    j_col = df.iloc[i, 9]
    print(f"{api}: H={h_col}, I={i_col}, J={j_col}")

print("\n扫描完成！")