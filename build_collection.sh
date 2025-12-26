#!/bin/bash
# Horizon Modules Ansible 集合包构建脚本 (Linux)

set -e  # 遇到错误时退出

# 定义变量
COLLECTION_NAMESPACE="horizon"
COLLECTION_NAME="modules"
COLLECTION_VERSION="1.0.0"
COLLECTION_PACKAGE_NAME="${COLLECTION_NAMESPACE}-${COLLECTION_NAME}-${COLLECTION_VERSION}.tar.gz"

# 创建临时目录
TEMP_DIR="temp_collection_build"
if [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi
mkdir -p "$TEMP_DIR"

# 设置集合目录（顶层目录）
COLLECTION_DIR="$TEMP_DIR"

# 创建必要的子目录
PLUGINS_DIR="$COLLECTION_DIR/plugins"
MODULES_DIR="$PLUGINS_DIR/modules"
META_DIR="$COLLECTION_DIR/meta"
DOCS_DIR="$COLLECTION_DIR/docs"

mkdir -p "$MODULES_DIR" "$META_DIR" "$DOCS_DIR"

# 检查并复制模块文件
if [ -d "library" ]; then
    MODULE_FILES=$(find library -name "*.py" -type f)
    if [ -n "$MODULE_FILES" ]; then
        for module_file in $MODULE_FILES; do
            cp "$module_file" "$MODULES_DIR/"
            echo "已添加模块: $(basename "$module_file")"
        done
    else
        echo "错误: library目录中未找到任何.py文件"
        rm -rf "$TEMP_DIR"
        exit 1
    fi
else
    echo "错误: 未找到library目录"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 创建meta/runtime.yml
cat > "$META_DIR/runtime.yml" << 'EOF'
---
requires_ansible: '>=2.9.10'
EOF

# 创建README.md
cat > "$COLLECTION_DIR/README.md" << EOF
# ${COLLECTION_NAMESPACE}.${COLLECTION_NAME}

An Ansible collection for ${COLLECTION_NAMESPACE} operations.
EOF

# 创建requirements.txt
cat > "$COLLECTION_DIR/requirements.txt" << 'EOF'
# Collection requirements
EOF

# 临时创建FILES.json（后面会用Python脚本来生成正确的FILES.json）
touch "$COLLECTION_DIR/FILES.json"

# 创建MANIFEST.json
cat > "$COLLECTION_DIR/MANIFEST.json" << EOF
{
  "collection_info": {
    "namespace": "${COLLECTION_NAMESPACE}",
    "name": "${COLLECTION_NAME}",
    "version": "${COLLECTION_VERSION}",
    "authors": ["Auto-generated"],
    "readme": "README.md",
    "tags": ["horizon", "hsm", "monitoring"],
    "description": "Ansible collection for ${COLLECTION_NAMESPACE} operations",
    "license": ["GPL-3.0-only"],
    "license_file": null,
    "dependencies": {},
    "repository": null,
    "documentation": null,
    "homepage": null,
    "issues": null
  },
  "file_manifest_file": {
    "name": "FILES.json",
    "ftype": "file",
    "chksum_type": "sha256",
    "chksum_sha256": "temp-placeholder",
    "format": 1
  },
  "format": 1
}
EOF

# 使用Python脚本重新生成正确的FILES.json和MANIFEST.json
# 由于shell难以处理复杂的JSON和校验和计算，我们使用Python脚本
python3 -c "
import os
import json
import hashlib
import sys
from pathlib import Path

collection_dir = '$COLLECTION_DIR'
files_info = []

def add_file_to_manifest(rel_path):
    full_path = Path(collection_dir) / rel_path
    if full_path.is_file():
        with open(full_path, 'rb') as f:
            content = f.read()
            chksum_sha256 = hashlib.sha256(content).hexdigest()
        files_info.append({
            'name': rel_path,
            'ftype': 'file',
            'chksum_type': 'sha256',
            'chksum_sha256': chksum_sha256,
            'format': 1
        })

def add_dir_to_manifest(rel_path):
    files_info.append({
        'name': rel_path,
        'ftype': 'dir',
        'chksum_type': None,
        'chksum_sha256': None,
        'format': 1
    })

# 添加所有文件和目录到清单
for root, dirs, files in os.walk(collection_dir):
    # 计算相对路径
    rel_root = os.path.relpath(root, collection_dir)
    if rel_root != '.':
        add_dir_to_manifest(rel_root.replace('\\\\', '/'))
    
    for file in files:
        if file not in ['FILES.json', 'MANIFEST.json']:  # 排除正在生成的文件
            file_path = os.path.join(rel_root, file) if rel_root != '.' else file
            file_path = file_path.replace('\\\\', '/')
            add_file_to_manifest(file_path)

# 生成FILES.json
files_json = Path(collection_dir) / 'FILES.json'
with open(files_json, 'w', encoding='utf-8') as f:
    json.dump({
        'files': files_info,
        'format': 1
    }, f, indent=2, ensure_ascii=False)

# 更新MANIFEST.json中的校验和
manifest_path = Path(collection_dir) / 'MANIFEST.json'
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest_data = json.load(f)

manifest_data['file_manifest_file']['chksum_sha256'] = hashlib.sha256(files_json.read_bytes()).hexdigest()

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest_data, f, indent=2, ensure_ascii=False)
"

# 创建tar.gz包 - 直接打包顶层目录的内容
tar -czf "$COLLECTION_PACKAGE_NAME" -C "$TEMP_DIR" .

echo "成功创建集合包: $COLLECTION_PACKAGE_NAME"
echo "包大小: $(stat -c%s "$COLLECTION_PACKAGE_NAME") bytes"

# 清理临时目录
rm -rf "$TEMP_DIR"

echo "构建完成: $COLLECTION_PACKAGE_NAME"