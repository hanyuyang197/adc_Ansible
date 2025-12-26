#!/usr/bin/env python3
"""
Horizon Modules Ansible 集合包构建脚本
基于参考包结构创建符合Ansible标准的集合包
"""

import os
import json
import hashlib
import tarfile
from pathlib import Path
import shutil
import sys
import argparse


def create_horizon_collection(output_dir="."):
    """创建horizon模块集合包"""
    # 定义集合信息
    collection_namespace = "horizon"
    collection_name = "modules"
    collection_version = "1.0.0"

    # 创建临时目录用于构建集合
    temp_dir = Path("temp_collection_build")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(exist_ok=True)

    # 创建集合目录结构 - 直接在顶层目录创建
    collection_dir = temp_dir  # 不再创建命名格式为 namespace-collection-version 的目录

    # 创建必要的子目录
    plugins_dir = collection_dir / "plugins"
    modules_dir = plugins_dir / "modules"
    modules_dir.mkdir(parents=True, exist_ok=True)

    # 创建其他必要目录
    meta_dir = collection_dir / "meta"
    meta_dir.mkdir(exist_ok=True)
    docs_dir = collection_dir / "docs"
    docs_dir.mkdir(exist_ok=True)

    # 查找并复制现有的模块文件
    module_files = []
    source_modules_dir = Path("library")
    if source_modules_dir.exists():
        module_files = list(source_modules_dir.glob("*.py"))

    if not module_files:
        print("错误: 未找到任何模块文件 (library目录为空或不存在)")
        return None

    # 复制现有的模块文件
    for src_module in module_files:
        dest_module = modules_dir / src_module.name
        dest_module.write_text(src_module.read_text(
            encoding='utf-8'), encoding='utf-8')
        print(f"已添加模块: {src_module.name}")

    # 创建meta/runtime.yml
    runtime_yml = meta_dir / "runtime.yml"
    runtime_yml.write_text('''---
requires_ansible: '>=2.9.10'
''', encoding='utf-8')

    # 创建README.md
    readme_md = collection_dir / "README.md"
    readme_md.write_text(f'''# {collection_namespace}.{collection_name}

An Ansible collection for {collection_namespace} operations.
''', encoding='utf-8')

    # 创建requirements.txt
    requirements_txt = collection_dir / "requirements.txt"
    requirements_txt.write_text(
        "# Collection requirements\n", encoding='utf-8')

    # 计算所有文件的校验和并生成FILES.json
    files_info = []

    def add_file_to_manifest(rel_path):
        full_path = collection_dir / rel_path
        if full_path.is_file():
            with open(full_path, 'rb') as f:
                content = f.read()
                chksum_sha256 = hashlib.sha256(content).hexdigest()
            files_info.append({
                "name": rel_path,
                "ftype": "file",
                "chksum_type": "sha256",
                "chksum_sha256": chksum_sha256,
                "format": 1
            })

    def add_dir_to_manifest(rel_path):
        files_info.append({
            "name": rel_path,
            "ftype": "dir",
            "chksum_type": None,
            "chksum_sha256": None,
            "format": 1
        })

    # 添加所有文件和目录到清单
    for root, dirs, files in os.walk(collection_dir):
        # 计算相对路径
        rel_root = os.path.relpath(root, collection_dir)
        if rel_root != '.':
            add_dir_to_manifest(rel_root.replace('\\', '/'))

        for file in files:
            file_path = os.path.join(
                rel_root, file) if rel_root != '.' else file
            file_path = file_path.replace('\\', '/')
            add_file_to_manifest(file_path)

    # 生成FILES.json
    files_json = collection_dir / "FILES.json"
    with open(files_json, 'w', encoding='utf-8') as f:
        json.dump({
            "files": files_info,
            "format": 1
        }, f, indent=2, ensure_ascii=False)

    # 生成MANIFEST.json
    manifest_json = collection_dir / "MANIFEST.json"
    with open(manifest_json, 'w', encoding='utf-8') as f:
        json.dump({
            "collection_info": {
                "namespace": collection_namespace,
                "name": collection_name,
                "version": collection_version,
                "authors": ["Auto-generated"],
                "readme": "README.md",
                "tags": ["horizon", "hsm", "monitoring"],
                "description": f"Ansible collection for {collection_namespace} operations",
                "license": ["GPL-3.0-only"],
                "license_file": None,
                "dependencies": {},
                "repository": None,
                "documentation": None,
                "homepage": None,
                "issues": None
            },
            "file_manifest_file": {
                "name": "FILES.json",
                "ftype": "file",
                "chksum_type": "sha256",
                "chksum_sha256": hashlib.sha256(files_json.read_bytes()).hexdigest(),
                "format": 1
            },
            "format": 1
        }, f, indent=2, ensure_ascii=False)

    # 创建tar.gz包 - 直接打包顶层目录的内容
    collection_package_name = f"{collection_namespace}-{collection_name}-{collection_version}.tar.gz"
    output_path = Path(output_dir) / collection_package_name

    with tarfile.open(output_path, "w:gz") as tar:
        for file_path in collection_dir.iterdir():
            # 添加每个文件/目录到tar包中，保持顶层目录结构
            tar.add(file_path, arcname=file_path.name)

    print(f"成功创建集合包: {output_path}")
    print(f"包大小: {os.path.getsize(output_path)} bytes")

    # 清理临时目录
    shutil.rmtree(temp_dir)

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Horizon Modules Ansible 集合包构建工具')
    parser.add_argument('--output-dir', '-o', default='.',
                        help='输出目录 (默认为当前目录)')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

    args = parser.parse_args()

    if args.verbose:
        print("开始构建 Horizon Modules Ansible 集合包...")
        print(f"输出目录: {args.output_dir}")

    try:
        result = create_horizon_collection(output_dir=args.output_dir)
        if result:
            print(f"构建完成: {result}")
        else:
            print("构建失败")
            sys.exit(1)
    except Exception as e:
        print(f"构建过程中出现错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
