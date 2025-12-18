#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


def check_ansible_installation():
    """检查Ansible安装"""
    print("=== Ansible 安装检查 ===")
    try:
        result = subprocess.run(
            ['ansible', '--version'], capture_output=True, text=True)
        print("Ansible 版本:")
        print(result.stdout)
    except FileNotFoundError:
        print("❌ 未找到 Ansible 命令")
        print("请确保 Ansible 已正确安装")


def check_python_path():
    """检查Python路径"""
    print("\n=== Python 路径检查 ===")
    print("Python executable:", sys.executable)
    print("Python path:")
    for path in sys.path:
        print("  ", path)


def check_library_directory():
    """检查library目录"""
    print("\n=== Library 目录检查 ===")
    library_path = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'
    if os.path.exists(library_path):
        print("✅ Library 目录存在:", library_path)
        print("目录中的文件:")
        for file in os.listdir(library_path):
            if file.endswith('.py'):
                print("  ", file)
    else:
        print("❌ Library 目录不存在:", library_path)


def check_ansible_cfg():
    """检查ansible.cfg配置"""
    print("\n=== Ansible 配置检查 ===")
    cfg_paths = [
        r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\ansible.cfg',
        r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\.ansible.cfg',
        os.path.expanduser('~/.ansible.cfg')
    ]

    found = False
    for cfg_path in cfg_paths:
        if os.path.exists(cfg_path):
            print("✅ 配置文件存在:", cfg_path)
            with open(cfg_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print("配置内容:")
                print(content)
            found = True
            break

    if not found:
        print("⚠️  未找到 ansible.cfg 配置文件")
        print("建议创建一个配置文件来指定模块路径")


def check_environment_variables():
    """检查环境变量"""
    print("\n=== 环境变量检查 ===")
    ansible_vars = ['ANSIBLE_LIBRARY',
                    'ANSIBLE_MODULE_UTILS', 'ANSIBLE_COLLECTIONS_PATHS']
    for var in ansible_vars:
        value = os.environ.get(var, '未设置')
        print(f"{var}: {value}")


def create_ansible_cfg():
    """创建ansible.cfg配置文件"""
    print("\n=== 创建 Ansible 配置文件 ===")
    cfg_content = """[defaults]
library = ./library
module_utils = ./module_utils
host_key_checking = False
deprecation_warnings = False

[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml

[ssh_connection]
scp_if_ssh = True
"""

    cfg_path = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\ansible.cfg'
    try:
        with open(cfg_path, 'w', encoding='utf-8') as f:
            f.write(cfg_content)
        print("✅ 已创建 ansible.cfg 配置文件:", cfg_path)
        print("配置内容:")
        print(cfg_content)
    except Exception as e:
        print("❌ 创建配置文件失败:", str(e))


def test_module_import():
    """测试模块导入"""
    print("\n=== 模块导入测试 ===")
    library_path = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'

    if library_path not in sys.path:
        sys.path.insert(0, library_path)

    modules_to_test = ['adc_login', 'adc_logout', 'adc_base']

    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} 导入成功")
        except ImportError as e:
            print(f"❌ {module_name} 导入失败: {str(e)}")
        except SyntaxError as e:
            print(f"❌ {module_name} 语法错误: {str(e)}")
        except Exception as e:
            print(f"❌ {module_name} 其他错误: {str(e)}")


if __name__ == '__main__':
    check_ansible_installation()
    check_python_path()
    check_library_directory()
    check_ansible_cfg()
    check_environment_variables()
    create_ansible_cfg()
    test_module_import()  # !/usr/bin/env python
# -*- coding: utf-8 -*-


def check_ansible_installation():
    """检查Ansible安装"""
    print("=== Ansible 安装检查 ===")
    try:
        result = subprocess.run(
            ['ansible', '--version'], capture_output=True, text=True)
        print("Ansible 版本:")
        print(result.stdout)
    except FileNotFoundError:
        print("❌ 未找到 Ansible 命令")
        print("请确保 Ansible 已正确安装")


def check_python_path():
    """检查Python路径"""
    print("\n=== Python 路径检查 ===")
    print("Python executable:", sys.executable)
    print("Python path:")
    for path in sys.path:
        print("  ", path)


def check_library_directory():
    """检查library目录"""
    print("\n=== Library 目录检查 ===")
    library_path = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'
    if os.path.exists(library_path):
        print("✅ Library 目录存在:", library_path)
        print("目录中的文件:")
        for file in os.listdir(library_path):
            if file.endswith('.py'):
                print("  ", file)
    else:
        print("❌ Library 目录不存在:", library_path)


def check_ansible_cfg():
    """检查ansible.cfg配置"""
    print("\n=== Ansible 配置检查 ===")
    cfg_paths = [
        r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\ansible.cfg',
        r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\.ansible.cfg',
        os.path.expanduser('~/.ansible.cfg')
    ]

    found = False
    for cfg_path in cfg_paths:
        if os.path.exists(cfg_path):
            print("✅ 配置文件存在:", cfg_path)
            with open(cfg_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print("配置内容:")
                print(content)
            found = True
            break

    if not found:
        print("⚠️  未找到 ansible.cfg 配置文件")
        print("建议创建一个配置文件来指定模块路径")


def check_environment_variables():
    """检查环境变量"""
    print("\n=== 环境变量检查 ===")
    ansible_vars = ['ANSIBLE_LIBRARY',
                    'ANSIBLE_MODULE_UTILS', 'ANSIBLE_COLLECTIONS_PATHS']
    for var in ansible_vars:
        value = os.environ.get(var, '未设置')
        print(f"{var}: {value}")


def create_ansible_cfg():
    """创建ansible.cfg配置文件"""
    print("\n=== 创建 Ansible 配置文件 ===")
    cfg_content = """[defaults]
library = ./library
module_utils = ./module_utils
host_key_checking = False
deprecation_warnings = False

[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml

[ssh_connection]
scp_if_ssh = True
"""

    cfg_path = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\ansible.cfg'
    try:
        with open(cfg_path, 'w', encoding='utf-8') as f:
            f.write(cfg_content)
        print("✅ 已创建 ansible.cfg 配置文件:", cfg_path)
        print("配置内容:")
        print(cfg_content)
    except Exception as e:
        print("❌ 创建配置文件失败:", str(e))


def test_module_import():
    """测试模块导入"""
    print("\n=== 模块导入测试 ===")
    library_path = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'

    if library_path not in sys.path:
        sys.path.insert(0, library_path)

    modules_to_test = ['adc_login', 'adc_logout', 'adc_base']

    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} 导入成功")
        except ImportError as e:
            print(f"❌ {module_name} 导入失败: {str(e)}")
        except SyntaxError as e:
            print(f"❌ {module_name} 语法错误: {str(e)}")
        except Exception as e:
            print(f"❌ {module_name} 其他错误: {str(e)}")


if __name__ == '__main__':
    check_ansible_installation()
    check_python_path()
    check_library_directory()
    check_ansible_cfg()
    check_environment_variables()
    create_ansible_cfg()
    test_module_import()
