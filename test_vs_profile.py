#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# 添加library目录到Python路径
library_path = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'
if library_path not in sys.path:
    sys.path.insert(0, library_path)


def test_module_import():
    """测试模块导入"""
    print("测试adc_slb_profile_vs模块导入...")

    try:
        import adc_slb_profile_vs
        print("✅ 模块导入成功")

        # 检查主要函数是否存在
        functions_to_check = [
            'adc_list_vs_profiles',
            'adc_list_vs_profiles_withcommon',
            'adc_get_vs_profile',
            'adc_add_vs_profile',
            'adc_edit_vs_profile',
            'adc_delete_vs_profile',
            'main'
        ]

        for func_name in functions_to_check:
            if hasattr(adc_slb_profile_vs, func_name):
                print(f"✅ 函数 {func_name} 存在")
            else:
                print(f"❌ 函数 {func_name} 不存在")

    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


def test_syntax_errors():
    """测试语法错误"""
    print("\n测试语法错误...")

    try:
        # 尝试编译模块
        import py_compile
        py_compile.compile(
            r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library\adc_slb_profile_vs.py', doraise=True)
        print("✅ 语法检查通过")
    except py_compile.PyCompileError as e:
        print(f"❌ 语法错误: {e}")
    except Exception as e:
        print(f"❌ 语法检查过程中出现错误: {e}")


if __name__ == '__main__':
    test_syntax_errors()
    test_module_import()
