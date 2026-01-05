#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import re

def fix_all_mappings():
    """修复所有映射关系"""
    
    # 读取Excel文件
    df = pd.read_excel('ansible_yml_path.xlsx')
    
    print(f"Excel文件列名: {df.columns.tolist()}")
    print(f"总API数量: {len(df)}")
    
    # 检查特定API
    api_to_check = 'slb.node.list'
    row = df[df['api对应'] == api_to_check]
    
    if not row.empty:
        idx = row.index[0]
        print(f"\n检查 {api_to_check}:")
        print(f"H列: {df.at[idx, '模块文件相对路径'] if '模块文件相对路径' in df.columns else '列不存在'}")
        print(f"I列: {df.at[idx, '模块名'] if '模块名' in df.columns else '列不存在'}")
        print(f"J列: {df.at[idx, 'Action名'] if 'Action名' in df.columns else '列不存在'}")
    
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
    
    print(f"\n扫描到 {len(module_functions)} 个模块文件")
    
    # 更新所有API的映射关系
    updated_count = 0
    
    for idx, row in df.iterrows():
        api_name = row['api对应']
        if pd.isna(api_name):
            continue
        
        # 根据API名称确定模块
        module_name = None
        if api_name.startswith('slb.node.'):
            module_name = 'adc_slb_node'
        elif api_name.startswith('slb.pool.'):
            module_name = 'adc_slb_pool'
        elif api_name.startswith('slb.healthcheck.'):
            module_name = 'adc_slb_healthcheck'
        elif api_name.startswith('slb.healthtest.'):
            module_name = 'adc_slb_healthtest'
        elif api_name.startswith('slb.passive-health-check.'):
            module_name = 'adc_slb_passive_health_check'
        elif api_name.startswith('slb.session.'):
            module_name = 'adc_slb_session'
        elif api_name.startswith('slb.stat.'):
            module_name = 'adc_slb_stat'
        elif api_name.startswith('slb.ssl.certificate.'):
            module_name = 'adc_slb_ssl_certificate'
        elif api_name.startswith('slb.ssl.key.'):
            module_name = 'adc_slb_ssl_key'
        elif api_name.startswith('slb.ssl.crl.'):
            module_name = 'adc_slb_ssl_crl'
        
        if module_name and module_name in module_functions:
            # 从API名称提取action
            action = api_name.split('.')[-1]
            
            # 查找匹配的函数
            found_function = None
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
                
                if api_name == 'slb.node.list':
                    print(f"✓ 已修复: {api_name} -> {module_name}.{found_function}")
    
    # 保存Excel
    df.to_excel('ansible_yml_path.xlsx', index=False)
    
    print(f"\n更新完成！共更新了 {updated_count} 个API的映射关系")
    
    # 再次检查特定API
    row = df[df['api对应'] == 'slb.node.list']
    if not row.empty:
        idx = row.index[0]
        print(f"\n修复后检查:")
        print(f"H列: {df.at[idx, '模块文件相对路径']}")
        print(f"I列: {df.at[idx, '模块名']}")
        print(f"J列: {df.at[idx, 'Action名']}")

if __name__ == "__main__":
    fix_all_mappings()