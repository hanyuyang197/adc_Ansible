#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

def cleanup_module(file_path):
    """清理单个模块"""
    if not os.path.exists(file_path):
        print("文件不存在: %s" % file_path)
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复不完整的try-except块
    # 查找并移除不完整的try-except块
    pattern = r'try:\s*# Python 2\s*except ImportError:\s*# Python 3\s*'
    content = re.sub(pattern, '', content)
    
    # 确保send_request函数正确使用urllib_request
    content = re.sub(r'urllib2\.', 'urllib_request.', content)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("已清理文件: %s" % file_path)
    return True

def final_cleanup():
    """最终清理所有模块"""
    modules_dir = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'
    
    if not os.path.exists(modules_dir):
        print("目录不存在: %s" % modules_dir)
        return
    
    # 获取所有.py文件
    module_files = [f for f in os.listdir(modules_dir) if f.endswith('.py') and f != '__init__.py']
    
    for module_file in module_files:
        file_path = os.path.join(modules_dir, module_file)
        try:
            cleanup_module(file_path)
        except Exception as e:
            print("清理文件时出错 %s: %s" % (file_path, str(e)))

if __name__ == '__main__':
    final_cleanup()