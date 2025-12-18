#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

def fix_ruletable_module():
    """修复ruletable模块中的语法错误"""
    file_path = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library\adc_slb_ruletable.py'
    
    if not os.path.exists(file_path):
        print("文件不存在: %s" % file_path)
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复导入问题
    content = re.sub(
        r'import urllib2 as urllib_request',
        '# Python 2/3兼容性处理\ntry:\n    # Python 2\n    import urllib2 as urllib_request\nexcept ImportError:\n    # Python 3\n    import urllib.request as urllib_request\n    import urllib.error as urllib_error',
        content,
        count=1
    )
    
    # 修复send_request函数中的引用
    content = re.sub(
        r'urllib2\.Request',
        'urllib_request.Request',
        content
    )
    
    content = re.sub(
        r'urllib2\.urlopen',
        'urllib_request.urlopen',
        content
    )
    
    # 修复main函数中的参数访问
    main_fix = '''    # 获取action参数并确保它是字符串类型
    if 'action' in module.params and module.params['action'] is not None:
        action = str(module.params['action'])
    else:
        action = '''''
    
    content = re.sub(
        r'action = module\.params\[\'action\'\] if \'action\' in module\.params else \'\'\n\s+# 为了解决静态检查工具的问题，我们进行类型转换\n\s+if hasattr\(action, \'__str__\'\):\n\s+action = str\(action\)',
        main_fix,
        content
    )
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("已修复ruletable模块")

if __name__ == '__main__':
    fix_ruletable_module()