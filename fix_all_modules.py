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
    
    # 检查是否已经修复过
    if '# Python 2/3兼容性处理' in content:
        print("文件已修复: %s" % file_path)
        return True
    
    # 修复导入问题
    if 'import urllib2' in content or 'import urllib.request as urllib2' in content:
        # 替换导入语句
        content = re.sub(
            r'try:\s*\n\s*import urllib2\s*\n\s*import json\s*\nexcept ImportError:\s*\n\s*pass',
            '# Python 2/3兼容性处理\ntry:\n    # Python 2\n    import urllib2 as urllib_request\n    import json\nexcept ImportError:\n    # Python 3\n    import urllib.request as urllib_request\n    import urllib.error as urllib_error\n    import json',
            content,
            count=1
        )
        
        # 替换urllib2为urllib_request
        content = re.sub(r'urllib2\.', 'urllib_request.', content)
        
        # 修复send_request函数
        def fix_send_request(match):
            func_content = match.group(0)
            # 修复json.dumps调用
            func_content = re.sub(r'data_json = json\.dumps\(data\)\s*\n\s*req = urllib_request\.Request\(url, data=data_json\)', 
                                r'data_json = json.dumps(data)\n        data_bytes = data_json.encode(\'utf-8\')\n        req = urllib_request.Request(url, data=data_bytes)', 
                                func_content)
            return func_content
            
        content = re.sub(r'def send_request\(.*?\):.*?return result\n\s*\n', fix_send_request, content, flags=re.DOTALL)
    
    # 修复main函数中的参数访问问题
    if 'module.params[\'action\']' in content:
        main_fix = '''    # 获取action参数并确保它是字符串类型
    if 'action' in module.params and module.params['action'] is not None:
        action = str(module.params['action'])
    else:
        action = '''''
        
        content = re.sub(
            r'action = module\.params\[\'action\'\] if \'action\' in module\.params else \'\'.*?\n\s+if hasattr\(action, \'__str__\'\):\n\s+action = str\(action\)',
            main_fix,
            content,
            flags=re.DOTALL
        )
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("已修复文件: %s" % file_path)
    return True

def fix_all_modules():
    """修复所有模块"""
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
    fix_all_modules()