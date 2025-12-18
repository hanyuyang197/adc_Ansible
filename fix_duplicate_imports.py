#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

def fix_duplicate_imports(file_path):
    """修复单个模块的重复导入问题"""
    if not os.path.exists(file_path):
        print("文件不存在: %s" % file_path)
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 将内容分割成行
    lines = content.split('\n')
    
    # 跟踪已见过的导入语句
    seen_imports = set()
    new_lines = []
    
    for line in lines:
        stripped_line = line.strip()
        
        # 检查是否是导入语句
        is_import_line = (
            stripped_line.startswith('import ') or 
            stripped_line.startswith('from ') and ' import ' in stripped_line
        )
        
        if is_import_line:
            # 如果已经见过这个导入语句，跳过
            if stripped_line in seen_imports:
                continue
            # 否则添加到已见过的集合中
            seen_imports.add(stripped_line)
        
        new_lines.append(line)
    
    # 重新组合内容
    content = '\n'.join(new_lines)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("已修复文件重复导入问题: %s" % file_path)
    return True

def fix_all_duplicate_imports():
    """修复所有模块的重复导入问题"""
    modules_dir = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'
    
    if not os.path.exists(modules_dir):
        print("目录不存在: %s" % modules_dir)
        return
    
    # 获取所有.py文件
    module_files = [f for f in os.listdir(modules_dir) if f.endswith('.py') and f != '__init__.py']
    
    for module_file in module_files:
        file_path = os.path.join(modules_dir, module_file)
        try:
            fix_duplicate_imports(file_path)
        except Exception as e:
            print("修复文件时出错 %s: %s" % (file_path, str(e)))

if __name__ == '__main__':
    fix_all_duplicate_imports()