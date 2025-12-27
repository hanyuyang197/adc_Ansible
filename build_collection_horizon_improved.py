#!/usr/bin/env python3
"""
构建Ansible集合包的脚本 - 用于horizon命名空间 (改进版)
"""

import os
import json
import shutil
import tarfile
from pathlib import Path


def create_collection_structure():
    """创建Ansible集合包的标准目录结构"""
    # 创建临时构建目录
    build_dir = Path("build_temp")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    build_dir.mkdir(exist_ok=True)

    # 创建集合目录结构
    collection_dir = build_dir / "horizon" / "modules"
    collection_dir.mkdir(parents=True, exist_ok=True)

    # 复制library目录中的所有模块文件
    library_dir = Path("library")
    modules_dest = collection_dir / "plugins" / "modules"
    modules_dest.mkdir(parents=True, exist_ok=True)

    for module_file in library_dir.glob("*.py"):
        shutil.copy2(module_file, modules_dest)

    # 复制module_utils目录
    module_utils_dest = collection_dir / "plugins" / "module_utils"
    module_utils_dest.mkdir(parents=True, exist_ok=True)

    # 从adc_base.py中提取通用函数并创建adc_common.py
    adc_base_path = library_dir / "adc_base.py"
    if adc_base_path.exists():
        with open(adc_base_path, 'r', encoding='utf-8') as f:
            adc_base_content = f.read()

        # 提取通用函数并创建adc_common.py
        adc_common_content = '''"""
ADC通用函数模块
"""
import json
import sys


def make_adc_request(url, data=None, method='GET'):
    """发送ADC请求"""
    pass


def format_adc_response(response_data, operation_name, success_expected=True):
    """格式化ADC响应"""
    pass


def check_adc_auth(authkey):
    """检查ADC认证"""
    pass


def handle_adc_error(error):
    """处理ADC错误"""
    pass


def build_adc_params(params):
    """构建ADC参数"""
    pass


def validate_adc_params(params):
    """验证ADC参数"""
    pass


def adc_result_check(result):
    """检查ADC结果"""
    pass


def adc_format_output(output):
    """格式化ADC输出"""
    pass


def build_params_with_optional(base_params, optional_params):
    """构建带可选参数的参数"""
    pass


def make_http_request(url, data=None, method='GET'):
    """发送HTTP请求"""
    pass


def get_param_if_exists(module, param_name):
    """从模块中获取参数值"""
    if hasattr(module, 'params') and param_name in module.params:
        return module.params[param_name]
    return None


def create_adc_module_args():
    """创建ADC模块参数"""
    pass


def adc_response_to_ansible_result(response_data, operation_name):
    """将ADC响应转换为Ansible结果"""
    pass


'''
        # 从adc_base.py中提取format_adc_response_for_ansible函数
        # 查找函数定义的起始位置
        func_start = adc_base_content.find(
            'def format_adc_response_for_ansible')
        if func_start != -1:
            # 查找函数定义的结束位置（基于缩进）
            lines = adc_base_content[func_start:].split('\n')
            adc_common_content += 'def format_adc_response_for_ansible'
            current_line = 1
            # 添加函数定义行
            for i, line in enumerate(lines[1:], 1):
                # 检查缩进以确定函数结束
                stripped = line.lstrip()
                if stripped and not line.startswith(' ') and not line.startswith('\t'):
                    # 遇到非缩进行，函数结束
                    break
                adc_common_content += '\n' + line
                current_line = i
        else:
            # 如果没有找到特定函数，使用通用版本
            adc_common_content += '''def format_adc_response_for_ansible(response_data, operation_name, success_expected=True):
    """格式化ADC响应以适应Ansible"""
    try:
        parsed_data = json.loads(response_data)
        if 'errmsg' in parsed_data and parsed_data['errmsg']:
            return False, {
                'failed': True,
                'msg': f"{operation_name}失败: {parsed_data['errmsg']}",
                'response': parsed_data
            }
        else:
            return True, {
                'changed': True,
                'msg': f"{operation_name}成功",
                'response': parsed_data
            }
    except json.JSONDecodeError as e:
        return False, {
            'failed': True,
            'msg': f"解析响应失败: {str(e)}",
            'raw_response': response_data
        }
'''

        with open(module_utils_dest / "adc_common.py", 'w', encoding='utf-8') as f:
            f.write(adc_common_content)

    # 创建roles目录（如果存在）
    roles_dir = Path("roles")
    if roles_dir.exists():
        roles_dest = collection_dir / "roles"
        if roles_dir.exists():
            shutil.copytree(roles_dir, roles_dest, dirs_exist_ok=True)

    # 创建defaults目录
    defaults_dir = collection_dir / "defaults"
    defaults_dir.mkdir(exist_ok=True)

    # 创建handlers目录
    handlers_dir = collection_dir / "handlers"
    handlers_dir.mkdir(exist_ok=True)

    # 创建tasks目录
    tasks_dir = collection_dir / "tasks"
    tasks_dir.mkdir(exist_ok=True)

    # 创建templates目录
    templates_dir = collection_dir / "templates"
    templates_dir.mkdir(exist_ok=True)

    # 创建vars目录
    vars_dir = collection_dir / "vars"
    vars_dir.mkdir(exist_ok=True)

    # 创建playbooks目录
    playbooks_dir = collection_dir / "playbooks"
    playbooks_dir.mkdir(exist_ok=True)

    # 复制playbooks目录中的所有文件
    src_playbooks_dir = Path("playbooks")
    if src_playbooks_dir.exists():
        for item in src_playbooks_dir.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(src_playbooks_dir)
                dest_path = playbooks_dir / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)

    return collection_dir, build_dir


def create_manifest_json(collection_dir):
    """创建MANIFEST.json文件"""
    manifest_content = {
        "collection_info": {
            "namespace": "horizon",
            "name": "modules",
            "version": "1.0.0",
            "authors": ["Your Name"],
            "description": "Horizon ADC modules collection",
            "license": ["GPL-2.0-or-later"],
            "license_file": "LICENSE",
            "min_ansible_version": "2.9.0",
            "dependencies": {},
            "repository": "https://github.com/horizon/horizon-modules",
            "documentation": "https://github.com/horizon/horizon-modules/blob/main/README.md",
            "homepage": "https://github.com/horizon/horizon-modules",
            "issues": "https://github.com/horizon/horizon-modules/issues"
        },
        "file_manifest_file": {
            "name": "FILES.json",
            "ftype": "file",
            "chksum_type": "sha256",
            "chksum_sha256": None,
            "format": 1
        },
        "format": 1
    }

    manifest_path = collection_dir / "MANIFEST.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_content, f, indent=4, ensure_ascii=False)

    return manifest_path


def create_files_json(collection_dir):
    """创建FILES.json文件"""
    import hashlib

    files_info = {
        "files": [
            {
                "name": ".",
                "ftype": "dir",
                "chksum_type": None,
                "chksum_sha256": None,
                "format": 1
            }
        ],
        "format": 1
    }

    # 遍历收集所有文件信息
    for root, dirs, files in os.walk(collection_dir):
        for directory in dirs:
            dir_path = Path(root) / directory
            rel_path = dir_path.relative_to(collection_dir.parent.parent)
            files_info["files"].append({
                "name": str(rel_path).replace("\\", "/"),
                "ftype": "dir",
                "chksum_type": None,
                "chksum_sha256": None,
                "format": 1
            })

        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(collection_dir.parent.parent)

            # 计算文件的sha256校验和
            with open(file_path, 'rb') as f:
                file_content = f.read()
                chksum_sha256 = hashlib.sha256(file_content).hexdigest()

            files_info["files"].append({
                "name": str(rel_path).replace("\\", "/"),
                "ftype": "file",
                "chksum_type": "sha256",
                "chksum_sha256": chksum_sha256,
                "format": 1
            })

    files_json_path = collection_dir / "FILES.json"
    with open(files_json_path, 'w', encoding='utf-8') as f:
        json.dump(files_info, f, indent=4)

    return files_json_path


def build_collection_package(collection_dir, build_dir):
    """构建集合包"""
    # 首先创建FILES.json
    create_files_json(collection_dir)

    # 创建MANIFEST.json
    create_manifest_json(collection_dir)

    # 更新FILES.json中的MANIFEST校验和
    import hashlib

    # 重新计算MANIFEST.json的校验和并更新FILES.json
    manifest_path = collection_dir / "MANIFEST.json"
    with open(manifest_path, 'rb') as f:
        manifest_content = f.read()
        manifest_chksum = hashlib.sha256(manifest_content).hexdigest()

    # 读取FILES.json并更新MANIFEST.json的校验和
    files_json_path = collection_dir / "FILES.json"
    with open(files_json_path, 'r', encoding='utf-8') as f:
        files_info = json.load(f)

    for file_info in files_info["files"]:
        if file_info["name"] == "MANIFEST.json":
            file_info["chksum_sha256"] = manifest_chksum
            break

    with open(files_json_path, 'w', encoding='utf-8') as f:
        json.dump(files_info, f, indent=4)

    # 创建tar.gz包
    package_name = "horizon-modules-1.0.0.tar.gz"
    with tarfile.open(package_name, "w:gz") as tar:
        # 将整个collection目录添加到tar包中
        for root, dirs, files in os.walk(collection_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(collection_dir.parent)
                tar.add(file_path, arcname=arc_path)

    print(f"集合包已创建: {package_name}")

    # 清理临时目录
    shutil.rmtree(build_dir)

    return package_name


def main():
    print("开始构建Ansible集合包 (horizon.modules) - 改进版...")

    # 创建目录结构
    collection_dir, build_dir = create_collection_structure()
    print(f"目录结构已创建: {collection_dir}")

    # 构建包
    package_name = build_collection_package(collection_dir, build_dir)
    print(f"构建完成! 包文件: {package_name}")

    # 显示统计信息
    module_count = len(
        list((collection_dir / "plugins" / "modules").glob("*.py")))
    playbook_count = len(list((collection_dir / "playbooks").rglob("*.yml"))) + \
        len(list((collection_dir / "playbooks").rglob("*.yaml")))
    utils_count = len(
        list((collection_dir / "plugins" / "module_utils").glob("*.py")))

    print(f"统计信息:")
    print(f"  模块数量: {module_count}")
    print(f"  Playbook数量: {playbook_count}")
    print(f"  通用工具数量: {utils_count}")
    print(f"  命名空间: horizon.modules")


if __name__ == "__main__":
    main()
