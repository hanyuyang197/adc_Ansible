#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys


def check_module_syntax(file_path):
    """检查单个模块的语法"""
    try:
        # 使用Python编译器检查语法
        result = subprocess.run([
            sys.executable, '-m', 'py_compile', file_path
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print("✅ %s: 语法正确" % os.path.basename(file_path))
            return True
        else:
            print("❌ %s: 语法错误 - %s" %
                  (os.path.basename(file_path), result.stderr.strip()))
            return False
    except subprocess.TimeoutExpired:
        print("⏰ %s: 检查超时" % os.path.basename(file_path))
        return False
    except Exception as e:
        print("💥 %s: 检查失败 - %s" % (os.path.basename(file_path), str(e)))
        return False


def check_all_modules():
    """检查所有模块的语法"""
    modules_dir = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'

    if not os.path.exists(modules_dir):
        print("目录不存在: %s" % modules_dir)
        return

    # 获取所有.py文件
    module_files = [f for f in os.listdir(
        modules_dir) if f.endswith('.py') and f != '__init__.py']

    print("开始检查 %d 个模块的语法..." % len(module_files))
    print("-" * 50)

    passed = 0
    failed = 0

    for module_file in module_files:
        file_path = os.path.join(modules_dir, module_file)
        try:
            if check_module_syntax(file_path):
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print("检查文件时出错 %s: %s" % (file_path, str(e)))
            failed += 1

    print("-" * 50)
    print("检查完成: %d 通过, %d 失败" % (passed, failed))

    if failed > 0:
        print("\n❌ 发现语法错误，请检查上述模块")
        return False
    else:
        print("\n✅ 所有模块语法正确")
        return True


if __name__ == '__main__':
    check_all_modules()
