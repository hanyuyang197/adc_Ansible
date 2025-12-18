#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re


def fix_module_imports(file_path):
    """修复单个模块的导入问题"""
    if not os.path.exists(file_path):
        print("文件不存在: %s" % file_path)
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 修复重复的导入语句
    # 查找并移除重复的Python 2/3兼容性处理
    pattern = r'# Python 2/3兼容性处理\s*try:\s*# Python 2\s*import urllib2 as urllib_request\s*except ImportError:\s*# Python 3\s*import urllib.request as urllib_request\s*import urllib.error as urllib_error\s*except ImportError:\s*# Python 3\s*import urllib.request as urllib_request\s*import urllib.error as urllib_error'

    replacement = '''# Python 2/3兼容性处理
try:
    # Python 2
    import urllib2 as urllib_request
except ImportError:
    # Python 3
    import urllib.request as urllib_request
    import urllib.error as urllib_error'''

    content = re.sub(pattern, replacement, content)

    # 确保只有一个Python 2/3兼容性处理块
    lines = content.split('\n')
    new_lines = []
    found_compat_block = False

    i = 0
    while i < len(lines):
        line = lines[i]
        if '# Python 2/3兼容性处理' in line:
            if not found_compat_block:
                # 保留第一个兼容性处理块
                new_lines.append(line)
                found_compat_block = True
                # 添加接下来的几行
                for j in range(1, 6):
                    if i + j < len(lines):
                        new_lines.append(lines[i + j])
                i += 6
            else:
                # 跳过重复的兼容性处理块
                # 跳过直到找到except ImportError行之后
                while i < len(lines) and 'import urllib.error as urllib_error' not in lines[i]:
                    i += 1
                if i < len(lines):
                    i += 1
                continue
        else:
            new_lines.append(line)
        i += 1

    content = '\n'.join(new_lines)

    # 修复send_request函数中的urllib调用
    content = re.sub(r'urllib2\.', 'urllib_request.', content)

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("已修复文件导入问题: %s" % file_path)
    return True


def fix_all_modules_imports():
    """修复所有模块的导入问题"""
    modules_dir = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'

    if not os.path.exists(modules_dir):
        print("目录不存在: %s" % modules_dir)
        return

    # 获取所有.py文件
    module_files = [f for f in os.listdir(modules_dir) if f.endswith('.py')]

    for module_file in module_files:
        file_path = os.path.join(modules_dir, module_file)
        try:
            fix_module_imports(file_path)
        except Exception as e:
            print("修复文件时出错 %s: %s" % (file_path, str(e)))


if __name__ == '__main__':
    fix_all_modules_imports()
