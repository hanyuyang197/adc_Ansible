#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re


def fix_indentation(file_path):
    """修复单个文件的缩进错误"""
    if not os.path.exists(file_path):
        print("文件不存在: %s" % file_path)
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 修复缩进问题
        fixed_lines = []
        for line in lines:
            # 检查是否有异常缩进
            stripped = line.lstrip()
            if stripped:
                # 计算原始缩进
                original_indent = len(line) - len(stripped)
                # 确保缩进是4的倍数
                correct_indent = (original_indent // 4) * 4
                # 重新构造行
                fixed_line = ' ' * correct_indent + stripped
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)

        # 修复特定的语法错误（如不完整的赋值语句）
        content = ''.join(fixed_lines)

        # 修复不完整的action赋值语句
        content = re.sub(r'action =\s*$', 'action = \'\'', content)

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("已修复文件缩进: %s" % file_path)
        return True

    except Exception as e:
        print("修复文件时出错 %s: %s" % (file_path, str(e)))
        return False


def fix_all_indentation_errors():
    """修复所有模块的缩进错误"""
    modules_dir = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'

    if not os.path.exists(modules_dir):
        print("目录不存在: %s" % modules_dir)
        return

    # 获取所有.py文件
    module_files = [f for f in os.listdir(
        modules_dir) if f.endswith('.py') and f != '__init__.py']

    print("开始修复 %d 个模块的缩进错误..." % len(module_files))

    for module_file in module_files:
        file_path = os.path.join(modules_dir, module_file)
        try:
            fix_indentation(file_path)
        except Exception as e:
            print("处理文件时出错 %s: %s" % (file_path, str(e)))


if __name__ == '__main__':
    fix_all_indentation_errors()
