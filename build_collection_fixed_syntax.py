#!/usr/bin/env python3
"""
构建Ansible集合包的脚本 - 修复语法错误版
"""

import os
import json
import shutil
import tarfile
from pathlib import Path


def create_collection_structure():
    """创建Ansible集合包的标准目录结构（类似F5包结构）"""
    # 创建临时构建目录
    build_dir = Path("build_temp")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    build_dir.mkdir(exist_ok=True)

    # 直接在顶层创建结构，类似F5包
    # 顶层包含 MANIFEST.json, FILES.json, plugins/ 等
    plugins_dir = build_dir / "plugins"
    modules_dest = plugins_dir / "modules"
    modules_dest.mkdir(parents=True, exist_ok=True)

    # 复制library目录中的所有模块文件
    library_dir = Path("library")
    for module_file in library_dir.glob("*.py"):
        shutil.copy2(module_file, modules_dest)

    # 复制module_utils目录
    module_utils_dest = plugins_dir / "module_utils"
    module_utils_dest.mkdir(parents=True, exist_ok=True)

    # 创建adc_common.py文件，包含通用函数 - 使用兼容的字符串格式化
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


def format_adc_response_for_ansible(response_data, operation_name, success_expected=True):
    """格式化ADC响应以适应Ansible"""
    try:
        parsed_data = json.loads(response_data)
        if 'errmsg' in parsed_data and parsed_data['errmsg']:
            return False, {
                'failed': True,
                'msg': '%s失败: %s' % (operation_name, parsed_data['errmsg']),
                'response': parsed_data
            }
        else:
            return True, {
                'changed': True,
                'msg': '%s成功' % (operation_name,),
                'response': parsed_data
            }
    except json.JSONDecodeError as e:
        return False, {
            'failed': True,
            'msg': '解析响应失败: %s' % str(e),
            'raw_response': response_data
        }
'''
    with open(module_utils_dest / "adc_common.py", 'w', encoding='utf-8') as f:
        f.write(adc_common_content)

    # 创建meta目录和runtime.yml
    meta_dir = build_dir / "meta"
    meta_dir.mkdir(exist_ok=True)

    runtime_content = '''---
requires_ansible: '>=2.9.0'
'''
    with open(meta_dir / "runtime.yml", 'w', encoding='utf-8') as f:
        f.write(runtime_content)

    # 创建README.md
    readme_content = '''# Horizon ADC Modules Collection

This collection provides modules for managing Horizon ADC devices.
'''
    with open(build_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)

    return build_dir


def create_manifest_json(build_dir):
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

    manifest_path = build_dir / "MANIFEST.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_content, f, indent=4, ensure_ascii=False)

    return manifest_path


def create_files_json(build_dir):
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
    for root, dirs, files in os.walk(build_dir):
        for directory in dirs:
            dir_path = Path(root) / directory
            rel_path = dir_path.relative_to(build_dir)
            files_info["files"].append({
                "name": str(rel_path).replace("\\", "/"),
                "ftype": "dir",
                "chksum_type": None,
                "chksum_sha256": None,
                "format": 1
            })

        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(build_dir)

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

    files_json_path = build_dir / "FILES.json"
    with open(files_json_path, 'w', encoding='utf-8') as f:
        json.dump(files_info, f, indent=4)

    return files_json_path


def build_collection_package(build_dir):
    """构建集合包"""
    # 首先创建FILES.json
    create_files_json(build_dir)

    # 创建MANIFEST.json
    create_manifest_json(build_dir)

    # 更新FILES.json中的MANIFEST校验和
    import hashlib

    # 重新计算MANIFEST.json的校验和并更新FILES.json
    manifest_path = build_dir / "MANIFEST.json"
    with open(manifest_path, 'rb') as f:
        manifest_content = f.read()
        manifest_chksum = hashlib.sha256(manifest_content).hexdigest()

    # 读取FILES.json并更新MANIFEST.json的校验和
    files_json_path = build_dir / "FILES.json"
    with open(files_json_path, 'r', encoding='utf-8') as f:
        files_info = json.load(f)

    for file_info in files_info["files"]:
        if file_info["name"] == "MANIFEST.json":
            file_info["chksum_sha256"] = manifest_chksum
            break

    with open(files_json_path, 'w', encoding='utf-8') as f:
        json.dump(files_info, f, indent=4)

    # 创建tar.gz包 - 顶层直接包含所有文件，没有额外的命名空间目录
    package_name = "horizon-modules-1.0.0.tar.gz"
    with tarfile.open(package_name, "w:gz") as tar:
        # 将build_dir中的所有内容直接添加到tar包中
        for item in build_dir.iterdir():
            tar.add(item, arcname=item.name)

    print(f"集合包已创建: {package_name}")

    # 清理临时目录
    shutil.rmtree(build_dir)

    return package_name


def main():
    print("开始构建Ansible集合包 (horizon.modules) - 修复语法错误版...")

    # 创建目录结构
    build_dir = create_collection_structure()
    print(f"目录结构已创建: {build_dir}")

    # 构建包
    package_name = build_collection_package(build_dir)
    print(f"构建完成! 包文件: {package_name}")

    # 显示统计信息
    import tarfile
    with tarfile.open(package_name, "r:gz") as tar:
        names = tar.getnames()
        modules_count = len(
            [n for n in names if '/modules/' in n and n.endswith('.py')])
        utils_count = len(
            [n for n in names if '/module_utils/' in n and n.endswith('.py')])
        print(f"统计信息:")
        print(f"  模块数量: {modules_count}")
        print(f"  通用工具数量: {utils_count}")
        print(f"  命名空间: horizon.modules")


if __name__ == "__main__":
    main()
