#!/bin/bash

# HORIZON Ansible模块集合构建器
# 此脚本用于构建HORIZON Ansible集合包

set -e  # 遇到错误时退出

echo "正在构建HORIZON Ansible模块集合..."

# 定义变量
COLLECTION_NAME="horizon-modules"
COLLECTION_VERSION="1.0.0"
BUILD_DIR="build"
COLLECTION_DIR="${BUILD_DIR}/horizon/modules/horizon_modules"
TARBALL_NAME="${COLLECTION_NAME}-${COLLECTION_VERSION}.tar.gz"

# 清理之前的构建
echo "正在清理之前的构建..."
rm -rf "${BUILD_DIR}"
rm -f "${TARBALL_NAME}"

# 创建目录结构
echo "正在创建目录结构..."
mkdir -p "${COLLECTION_DIR}"

# 复制库模块
echo "正在复制库模块..."
mkdir -p "${COLLECTION_DIR}/plugins/modules"
cp -r library/*.py "${COLLECTION_DIR}/plugins/modules/"

# 创建模块工具目录（如果需要）
echo "正在创建模块工具目录..."
mkdir -p "${COLLECTION_DIR}/plugins/module_utils"

# 复制playbooks（作为示例）
echo "正在复制playbooks..."
mkdir -p "${COLLECTION_DIR}/examples"
cp -r playbooks/*.yml "${COLLECTION_DIR}/examples/"

# 创建galaxy.yml文件
echo "正在创建galaxy.yml..."
cat > "${COLLECTION_DIR}/galaxy.yml" << EOF
namespace: horizon
name: modules
version: ${COLLECTION_VERSION}
readme: README.md
authors:
  - Your Name <your.email@example.com>
description: 用于ADC（应用交付控制器）管理的Ansible模块
license_file: LICENSE
tags:
  - adc
  - loadbalancer
  - networking
  - infrastructure
dependencies:
  ansible_core: ">=2.9"
repository: https://github.com/your-org/horizon-ansible-modules
documentation: https://github.com/your-org/horizon-ansible-modules/blob/main/README.md
homepage: https://github.com/your-org/horizon-ansible-modules
issues: https://github.com/your-org/horizon-ansible-modules/issues
build_ignore:
  - "*.tar.gz"
  - "build"
EOF

# 为集合创建README.md
echo "正在创建README.md..."
cat > "${COLLECTION_DIR}/README.md" << EOF
# ADC Ansible模块集合

此集合提供了用于管理ADC（应用交付控制器）设备的Ansible模块。

## 包含的模块

- **节点管理**: adc_slb_node, adc_slb_node_port
- **服务池管理**: adc_slb_pool
- **健康检查管理**: adc_slb_healthcheck
- **虚拟地址管理**: adc_slb_va
- **虚拟服务管理**: adc_slb_va_vs
- **配置文件管理**: adc_slb_profile_* (fastl4, tcp, udp, http等)
- 以及更多模块...

## 安装

\`\`\`bash
ansible-galaxy collection install horizon.modules.horizon_modules
\`\`\`

## 使用方法

\`\`\`yaml
- name: 添加节点
  horizon.modules.horizon_modules.adc_slb_node:
    ip: "192.168.1.100"
    authkey: "{{ login_result.authkey }}"
    action: "add_node"
    name: "test_node"
    addr: "10.0.0.1"
    status: 1
  register: result
\`\`\`

请参考PACKAGING.md获取详细的安装和使用说明。
EOF

# 创建空的LICENSE文件
echo "正在创建LICENSE文件..."
touch "${COLLECTION_DIR}/LICENSE"

# 切换到构建目录
cd "${BUILD_DIR}"

# 创建tarball
echo "正在创建tarball..."
tar -czf "../${TARBALL_NAME}" .

# 返回原始目录
cd ..

# 清理构建目录
echo "正在清理..."
rm -rf "${BUILD_DIR}"

echo "构建完成！"
echo "集合包已创建: ${TARBALL_NAME}"
echo ""
echo "要安装集合，请运行:"
echo "ansible-galaxy collection install ${TARBALL_NAME}"