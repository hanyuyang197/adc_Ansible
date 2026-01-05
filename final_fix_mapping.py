#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import re

def scan_all_modules_and_functions():
    """扫描所有模块和函数"""
    
    # 读取Excel文件
    df = pd.read_excel('ansible_yml_path.xlsx')
    
    # 确保列存在
    if '模块文件相对路径' not in df.columns:
        df['模块文件相对路径'] = ''
    if '模块名' not in df.columns:
        df['模块名'] = ''
    if 'Action名' not in df.columns:
        df['Action名'] = ''
    
    # 扫描library目录
    module_functions = {}
    for file in os.listdir('library'):
        if file.endswith('.py') and file.startswith('adc_'):
            module_name = file.replace('.py', '')
            module_path = os.path.join('library', file)
            
            # 读取模块文件，提取所有函数
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
                functions = re.findall(r'def\s+(adc_[a-zA-Z_][a-zA-Z0-9_]*)\(', content)
                module_functions[module_name] = functions
    
    print(f"扫描到 {len(module_functions)} 个模块文件")
    
    # API到模块的映射规则
    api_to_module_patterns = {
        'slb.node.': 'adc_slb_node',
        'slb.pool.': 'adc_slb_pool',
        'slb.healthcheck.': 'adc_slb_healthcheck',
        'slb.healthtest.': 'adc_slb_healthtest',
        'slb.passive-health-check.': 'adc_slb_passive_health_check',
        'slb.session.': 'adc_slb_session',
        'slb.stat.': 'adc_slb_stat',
        'slb.ssl.certificate.': 'adc_slb_ssl_certificate',
        'slb.ssl.key.': 'adc_slb_ssl_key',
        'slb.ssl.crl.': 'adc_slb_ssl_crl',
    }
    
    # 检查每个API
    updated_count = 0
    
    for idx, row in df.iterrows():
        api_name = row['api对应']
        if pd.isna(api_name):
            continue
        
        # 找到对应的模块
        module_name = None
        for pattern, mod_name in api_to_module_patterns.items():
            if api_name.startswith(pattern):
                module_name = mod_name
                break
        
        if not module_name:
            continue
        
        # 检查模块是否存在
        if module_name in module_functions:
            # 从API名称提取action
            action = api_name.split('.')[-1]
            
            # 构建预期的函数名
            if action == 'list':
                expected_functions = [
                    f"adc_list_{module_name.split('_')[-1]}s",
                    f"adc_get_{module_name.split('_')[-1]}s"
                ]
            elif action == 'add':
                expected_functions = [f"adc_add_{module_name.split('_')[-1]}"]
            elif action == 'del':
                expected_functions = [f"adc_delete_{module_name.split('_')[-1]}"]
            elif action == 'get':
                expected_functions = [f"adc_get_{module_name.split('_')[-1]}"]
            elif action == 'edit':
                expected_functions = [f"adc_edit_{module_name.split('_')[-1]}"]
            elif action == 'clear':
                expected_functions = [f"adc_clear_{module_name.split('_')[-1]}"]
            else:
                expected_functions = [f"adc_{action}_{module_name.split('_')[-1]}"]
            
            # 检查是否存在预期的函数
            found_function = None
            for func in expected_functions:
                if func in module_functions[module_name]:
                    found_function = func
                    break
            
            # 如果没有精确匹配，尝试模糊匹配
            if not found_function:
                for func in module_functions[module_name]:
                    if action in func:
                        found_function = func
                        break
            
            if found_function:
                # 更新Excel
                df.at[idx, '模块文件相对路径'] = f"library/{module_name}"
                df.at[idx, '模块名'] = module_name
                df.at[idx, 'Action名'] = found_function
                updated_count += 1
                print(f"✓ {api_name} -> {module_name}.{found_function}")
            else:
                print(f"✗ {api_name}: 模块中存在函数 {module_functions[module_name]}")
        else:
            print(f"✗ {api_name}: 模块 {module_name} 不存在")
    
    # 保存Excel
    df.to_excel('ansible_yml_path.xlsx', index=False)
    
    print(f"\n更新完成！共更新了 {updated_count} 个API的映射关系")
    print(f"总API数量: {len(df)}")
    
    # 统计缺失情况
    missing_count = len(df[df['模块文件相对路径'].isna() | (df['模块文件相对路径'] == '')])
    print(f"缺失映射的API数量: {missing_count}")

if __name__ == "__main__":
    scan_all_modules_and_functions()