#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

def fix_single_module_imports(file_path):
    """修复单个模块的导入问题"""
    if not os.path.exists(file_path):
        print("文件不存在: %s" % file_path)
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复Python 2/3兼容性导入
    # 首先移除所有现有的urllib相关导入
    content = re.sub(r'import urllib2.*?\n', '', content)
    content = re.sub(r'import urllib\.request.*?\n', '', content)
    content = re.sub(r'import urllib\.error.*?\n', '', content)
    
    # 查找AnsibleModule导入的位置
    lines = content.split('\n')
    new_lines = []
    ansible_import_found = False
    json_import_found = False
    compat_block_added = False
    
    for line in lines:
        if 'from ansible.module_utils.basic import AnsibleModule' in line:
            new_lines.append(line)
            ansible_import_found = True
            # 在AnsibleModule导入后添加json导入（如果还没有的话）
            if not json_import_found:
                new_lines.append('import json')
                json_import_found = True
            # 添加Python 2/3兼容性处理
            if not compat_block_added:
                new_lines.extend([
                    '# Python 2/3兼容性处理',
                    'try:',
                    '    # Python 2',
                    '    import urllib2 as urllib_request',
                    'except ImportError:',
                    '    # Python 3',
                    '    import urllib.request as urllib_request',
                    '    import urllib.error as urllib_error'
                ])
                compat_block_added = True
        elif 'import json' in line and not json_import_found:
            # 如果已经有json导入，跳过（避免重复）
            new_lines.append(line)
            json_import_found = True
        elif '# Python 2/3兼容性处理' in line:
            # 如果已经有兼容性处理块，跳过整个块
            # 跳过直到找到except ImportError行之后
            continue
        elif 'import urllib2' in line or 'import urllib.request' in line or 'import urllib.error' in line:
            # 跳过其他urllib相关导入
            continue
        else:
            new_lines.append(line)
    
    # 如果没有找到AnsibleModule导入，添加到文件开头
    if not ansible_import_found:
        new_lines.insert(0, 'from ansible.module_utils.basic import AnsibleModule')
        new_lines.insert(1, 'import json')
        new_lines.insert(2, '# Python 2/3兼容性处理')
        new_lines.insert(3, 'try:')
        new_lines.insert(4, '    # Python 2')
        new_lines.insert(5, '    import urllib2 as urllib_request')
        new_lines.insert(6, 'except ImportError:')
        new_lines.insert(7, '    # Python 3')
        new_lines.insert(8, '    import urllib.request as urllib_request')
        new_lines.insert(9, '    import urllib.error as urllib_error')
    
    content = '\n'.join(new_lines)
    
    # 修复send_request函数中的urllib调用
    content = re.sub(r'urllib2\.', 'urllib_request.', content)
    content = re.sub(r'urllib\.request\.', 'urllib_request.', content)
    
    # 确保send_request函数使用正确的导入
    def fix_send_request_func(match):
        func_content = match.group(0)
        # 确保使用urllib_request而不是urllib2
        func_content = re.sub(r'urllib2\.', 'urllib_request.', func_content)
        func_content = re.sub(r'urllib\.request\.', 'urllib_request.', func_content)
        return func_content
    
    content = re.sub(r'def send_request\(.*?\):.*?return result\n\s*\n', fix_send_request_func, content, flags=re.DOTALL)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("已修复文件导入问题: %s" % file_path)
    return True

def fix_all_modules_imports_final():
    """最终修复所有模块的导入问题"""
    modules_dir = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'
    
    if not os.path.exists(modules_dir):
        print("目录不存在: %s" % modules_dir)
        return
    
    # 获取所有.py文件
    module_files = [f for f in os.listdir(modules_dir) if f.endswith('.py') and f != '__init__.py']
    
    for module_file in module_files:
        file_path = os.path.join(modules_dir, module_file)
        try:
            fix_single_module_imports(file_path)
        except Exception as e:
            print("修复文件时出错 %s: %s" % (file_path, str(e)))

if __name__ == '__main__':
    fix_all_modules_imports_final()