#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re


def extract_actions_from_file(file_path):
    """从单个 Python 文件中提取模块名和对应的 action"""
    module_name = os.path.basename(file_path).replace('.py', '')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.read()
        except Exception as e:
            return module_name, None, str(e)

    actions = []
    note = ""

    # 方法1: 尝试从 action 参数的 choices 中提取
    pattern = r"action\s*=\s*dict\s*\(\s*type\s*=\s*['\"]str['\"],\s*required\s*=\s*True,\s*choices\s*=\s*\[(.*?)\]\s*\)"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        choices_str = match.group(1)
        # 提取所有单引号或双引号字符串
        action_pattern = r"['\"]([^'\"]+)['\"]"
        actions = re.findall(action_pattern, choices_str)
        if actions:
            return module_name, actions, ""
        else:
            note = "choices为空"
            return module_name, [], note

    # 方法2: 从 main 函数的 if-elif 语句中提取 action
    # 查找所有 "if action == 'xxx'" 或 "elif action == 'xxx'" 的模式
    action_pattern = r"(?:if|elif)\s+action\s*==\s*['\"]([^'\"]+)['\"]"
    actions = re.findall(action_pattern, content)

    if actions:
        # 去重
        actions = list(set(actions))
        return module_name, actions, ""

    # 方法3: 检查是否有 main 函数但没有找到 action
    if "def main():" in content or "def main (" in content:
        if 'action' in content:
            note = "找到action参数但未匹配到choices或if-elif语句"
        else:
            note = "没有找到action参数"
    else:
        note = "没有找到main函数"

    return module_name, [], note


def main():
    library_path = os.path.join(os.path.dirname(__file__), 'library')
    output_file = os.path.join(os.path.dirname(__file__), 'module_actions_mapping.txt')

    if not os.path.exists(library_path):
        print(f"Error: library directory not found at {library_path}")
        return

    # 存储所有模块的 action 映射
    all_modules = {}

    # 遍历 library 目录
    py_files = sorted([f for f in os.listdir(library_path) if f.endswith('.py') and not f.startswith('__')])

    print(f"Processing {len(py_files)} Python files...")

    for filename in py_files:
        file_path = os.path.join(library_path, filename)
        module_name, actions, note = extract_actions_from_file(file_path)

        all_modules[module_name] = {
            'actions': actions,
            'note': note
        }

        if actions:
            print(f"  {module_name}: {len(actions)} actions")
        else:
            print(f"  {module_name}: {note}")

    # 统计
    modules_with_actions = sum(1 for m in all_modules if all_modules[m]['actions'])
    total_actions = sum(len(all_modules[m]['actions']) for m in all_modules)
    modules_need_check = sum(1 for m in all_modules if not all_modules[m]['actions'])

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ADC Ansible Modules - Actions Mapping\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"总模块数: {len(all_modules)}\n")
        f.write(f"有action的模块数: {modules_with_actions}\n")
        f.write(f"需要人工检查的模块数: {modules_need_check}\n")
        f.write(f"总action数: {total_actions}\n\n")

        # 按模块名称排序输出
        for module_name in sorted(all_modules.keys()):
            f.write(f"{module_name}:\n")
            if all_modules[module_name]['actions']:
                for action in sorted(all_modules[module_name]['actions']):
                    f.write(f"  - {action}\n")
            else:
                f.write(f"  [需要人工检查] {all_modules[module_name]['note']}\n")
            f.write("\n")

        # 生成 JSON 格式的映射
        f.write("\n" + "=" * 80 + "\n")
        f.write("JSON Format Mapping\n")
        f.write("=" * 80 + "\n\n")
        f.write("{\n")
        module_list = []
        for module_name in sorted(all_modules.keys()):
            if all_modules[module_name]['actions']:
                module_list.append(f'  "{module_name}": {sorted(all_modules[module_name]["actions"])}')
            else:
                module_list.append(f'  "{module_name}": []  // {all_modules[module_name]["note"]}')
        f.write(",\n".join(module_list))
        f.write("\n}\n")

        # 生成 Markdown 表格格式
        f.write("\n" + "=" * 80 + "\n")
        f.write("Markdown Table Format\n")
        f.write("=" * 80 + "\n\n")
        f.write("| Module Name | Actions | Note |\n")
        f.write("|-------------|----------|------|\n")
        for module_name in sorted(all_modules.keys()):
            if all_modules[module_name]['actions']:
                actions_str = ", ".join(sorted(all_modules[module_name]['actions']))
                f.write(f"| {module_name} | {actions_str} | |\n")
            else:
                f.write(f"| {module_name} | | {all_modules[module_name]['note']} |\n")

        # 生成需要人工检查的模块列表
        f.write("\n" + "=" * 80 + "\n")
        f.write("Modules Need Manual Check\n")
        f.write("=" * 80 + "\n\n")
        need_check = [m for m in all_modules if not all_modules[m]['actions']]
        if need_check:
            for module_name in sorted(need_check):
                f.write(f"- {module_name}: {all_modules[module_name]['note']}\n")
        else:
            f.write("None\n")

    print(f"\nSuccessfully extracted actions to: {output_file}")
    print(f"Summary:")
    print(f"  Total modules: {len(all_modules)}")
    print(f"  Modules with actions: {modules_with_actions}")
    print(f"  Modules need manual check: {modules_need_check}")
    print(f"  Total actions: {total_actions}")


if __name__ == '__main__':
    main()
