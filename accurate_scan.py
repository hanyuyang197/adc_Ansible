#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import re
import glob

def scan_accurate_mappings():
    """准确扫描项目结构并建立映射关系"""
    
    # 读取Excel文件
    df = pd.read_excel('ansible_yml_path.xlsx')
    
    # 创建空列（如果不存在）
    if '模块文件相对路径' not in df.columns:
        df['模块文件相对路径'] = ''
    if '模块名' not in df.columns:
        df['模块名'] = ''
    if 'Action名' not in df.columns:
        df['Action名'] = ''
    
    # 扫描library目录
    module_files = {}
    for file in os.listdir('library'):
        if file.endswith('.py') and file.startswith('adc_'):
            module_name = file.replace('.py', '')
            module_files[module_name] = os.path.join('library', file)
    
    print(f"发现模块文件: {len(module_files)}个")
    
    # 扫描playbooksNew目录
    yaml_files = {}
    for file in os.listdir('playbooksNew'):
        if file.endswith('.yml'):
            yaml_name = file.replace('.yml', '')
            yaml_files[yaml_name] = os.path.join('playbooksNew', file)
    
    print(f"发现YAML文件: {len(yaml_files)}个")
    
    # API到模块的映射规则
    api_mappings = {
        # slb.node.*
        'slb.node.list': ('adc_slb_node', 'adc_list_nodes'),
        'slb.node.add': ('adc_slb_node', 'adc_add_node'),
        'slb.node.del': ('adc_slb_node', 'adc_delete_node'),
        'slb.node.get': ('adc_slb_node', 'adc_get_node'),
        'slb.node.edit': ('adc_slb_node', 'adc_edit_node'),
        
        # slb.pool.*
        'slb.pool.list': ('adc_slb_pool', 'adc_list_pools'),
        'slb.pool.add': ('adc_slb_pool', 'adc_add_pool'),
        'slb.pool.del': ('adc_slb_pool', 'adc_delete_pool'),
        'slb.pool.get': ('adc_slb_pool', 'adc_get_pool'),
        'slb.pool.edit': ('adc_slb_pool', 'adc_edit_pool'),
        
        # slb.healthcheck.*
        'slb.healthcheck.list': ('adc_slb_healthcheck', 'adc_list_healthchecks'),
        'slb.healthcheck.add': ('adc_slb_healthcheck', 'adc_add_healthcheck'),
        'slb.healthcheck.del': ('adc_slb_healthcheck', 'adc_delete_healthcheck'),
        'slb.healthcheck.get': ('adc_slb_healthcheck', 'adc_get_healthcheck'),
        'slb.healthcheck.edit': ('adc_slb_healthcheck', 'adc_edit_healthcheck'),
        
        # slb.ssl.*
        'slb.ssl.certificate.upload': ('adc_slb_ssl_certificate', 'adc_upload_certificate'),
        'slb.ssl.key.upload': ('adc_slb_ssl_key', 'adc_upload_key'),
        'slb.ssl.crl.upload': ('adc_slb_ssl_crl', 'adc_upload_crl'),
        
        # 其他模块...
    }
    
    # 检查每个API的映射关系
    updated_count = 0
    
    for idx, row in df.iterrows():
        api_name = row['api对应']
        if pd.isna(api_name):
            continue
        
        # 检查是否有预定义的映射
        if api_name in api_mappings:
            module_name, function_name = api_mappings[api_name]
            
            # 检查模块文件是否存在
            if module_name in module_files:
                module_path = module_files[module_name]
                
                # 检查函数是否存在
                with open(module_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    functions = re.findall(r'def (adc_.*?)\(', content)
                    
                    if function_name in functions:
                        # 更新Excel
                        df.at[idx, '模块文件相对路径'] = f"library/{module_name}"
                        df.at[idx, '模块名'] = module_name
                        df.at[idx, 'Action名'] = function_name
                        updated_count += 1
                        print(f"✓ 已更新: {api_name} -> {module_name}.{function_name}")
                    else:
                        print(f"✗ 函数不存在: {api_name} -> {function_name}")
                        print(f"  模块中存在的函数: {functions}")
            else:
                print(f"✗ 模块不存在: {api_name} -> {module_name}")
        else:
            print(f"? 未定义映射: {api_name}")
    
    # 保存Excel
    df.to_excel('ansible_yml_path.xlsx', index=False)
    
    print(f"\n更新完成！共更新了 {updated_count} 个API的映射关系")
    print(f"总API数量: {len(df)}")
    
    # 统计缺失情况
    missing_count = len(df[df['模块文件相对路径'].isna() | (df['模块文件相对路径'] == '')])
    print(f"缺失映射的API数量: {missing_count}")

if __name__ == "__main__":
    scan_accurate_mappings()