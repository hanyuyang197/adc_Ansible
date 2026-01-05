#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

def update_excel_mapping():
    """更新Excel文件中nat.static相关的映射关系"""
    
    # 读取Excel文件
    df = pd.read_excel('ansible_yml_path.xlsx')
    
    # 确保列存在
    if '模块文件相对路径' not in df.columns:
        df['模块文件相对路径'] = ''
    if '模块名' not in df.columns:
        df['模块名'] = ''
    if 'Action名' not in df.columns:
        df['Action名'] = ''
    
    # 检查nat.static.statis是否存在
    if 'nat.static.statis' in df['api对应'].values:
        idx_statis = df[df['api对应'] == 'nat.static.statis'].index[0]
        df.at[idx_statis, '模块文件相对路径'] = 'library/adc_nat_static'
        df.at[idx_statis, '模块名'] = 'adc_nat_static'
        df.at[idx_statis, 'Action名'] = 'adc_get_nat_static_statistics'
        print("✓ 已更新 nat.static.statis 映射")
    
    # 检查nat.static.clear是否存在
    if 'nat.static.clear' in df['api对应'].values:
        idx_clear = df[df['api对应'] == 'nat.static.clear'].index[0]
        df.at[idx_clear, '模块文件相对路径'] = 'library/adc_nat_static'
        df.at[idx_clear, '模块名'] = 'adc_nat_static'
        df.at[idx_clear, 'Action名'] = 'adc_clear_nat_static_statistics'
        print("✓ 已更新 nat.static.clear 映射")
    
    # 保存Excel文件
    df.to_excel('ansible_yml_path.xlsx', index=False)
    print("✓ Excel文件已更新")
    
    # 检查更新结果
    print("\n更新后的映射关系:")
    nat_apis = ['nat.static.statis', 'nat.static.clear']
    for api in nat_apis:
        if api in df['api对应'].values:
            row = df[df['api对应'] == api].iloc[0]
            print(f"{api}:")
            print(f"  模块文件: {row['模块文件相对路径']}")
            print(f"  模块名: {row['模块名']}")
            print(f"  Action名: {row['Action名']}")

if __name__ == "__main__":
    update_excel_mapping()