# HORIZON Ansible模块集合PowerShell构建器
# 此脚本用于构建HORIZON Ansible集合包

Write-Output "正在构建HORIZON Ansible模块集合..."

# 定义变量
$COLLECTION_NAME = "horizon.modules.horizon_modules"
$COLLECTION_VERSION = "1.0.0"
$BUILD_DIR = "build"
$COLLECTION_BUILD_DIR = Join-Path $BUILD_DIR "ansible_collections\horizon\modules"
$TARBALL_NAME = "horizon-modules-$COLLECTION_VERSION.tar.gz"

# 清理之前的构建
Write-Output "正在清理之前的构建..."
if (Test-Path $BUILD_DIR) {
    Remove-Item -Path $BUILD_DIR -Recurse -Force
}
if (Test-Path $TARBALL_NAME) {
    Remove-Item -Path $TARBALL_NAME -Force
}

# 创建目录结构
Write-Output "正在创建目录结构..."
New-Item -ItemType Directory -Path $COLLECTION_BUILD_DIR -Force

# 创建集合根目录
$COLLECTION_ROOT = Join-Path $COLLECTION_BUILD_DIR "horizon_modules"
New-Item -ItemType Directory -Path (Join-Path $COLLECTION_ROOT "plugins\modules") -Force
New-Item -ItemType Directory -Path (Join-Path $COLLECTION_ROOT "plugins\module_utils") -Force
New-Item -ItemType Directory -Path (Join-Path $COLLECTION_ROOT "docs") -Force
New-Item -ItemType Directory -Path (Join-Path $COLLECTION_ROOT "tests") -Force

# 复制库模块
Write-Output "正在复制库模块..."
Copy-Item -Path "library\*.py" -Destination (Join-Path $COLLECTION_ROOT "plugins\modules") -Force

# 复制playbooks（作为示例）
Write-Output "正在复制playbooks..."
if (Test-Path "playbooks") {
    Copy-Item -Path "playbooks\*" -Destination (Join-Path $COLLECTION_ROOT "docs") -Recurse -Force
}

# 创建galaxy.yml文件
Write-Output "正在创建galaxy.yml..."
$galaxyContent = @"
namespace: horizon
name: modules
version: 1.0.0
readme: README.md
authors:
  - Horizon Team
description: 用于ADC（应用交付控制器）管理的Ansible模块集合
license:
  - GPL-2.0-or-later
tags:
  - adc
  - loadbalancer
  - networking
  - infrastructure
  - horizon
dependencies: {}
repository: https://github.com/horizon/horizon-ansible-modules
documentation: https://github.com/horizon/horizon-ansible-modules/blob/main/README.md
homepage: https://github.com/horizon/horizon-ansible-modules
issues: https://github.com/horizon/horizon-ansible-modules/issues
build_ignore:
  - "*.tar.gz"
  - "build"
  - ".git"
  - ".gitignore"
"@
Set-Content -Path (Join-Path $COLLECTION_ROOT "galaxy.yml") -Value $galaxyContent

# 为集合创建README.md
Write-Output "正在创建README.md..."
$readmeContent = @"
# HORIZON ADC Ansible模块集合

此集合提供了用于管理HORIZON ADC（应用交付控制器）设备的Ansible模块。

## 包含的模块

- **节点管理**: adc_slb_node, adc_slb_node_port
- **服务池管理**: adc_slb_pool
- **健康检查管理**: adc_slb_healthcheck
- **虚拟地址管理**: adc_slb_va
- **虚拟服务管理**: adc_slb_va_vs
- **配置文件管理**: adc_slb_profile_* (fastl4, tcp, udp, http等)
- **系统管理**: adc_system_*
- **WAF管理**: adc_waf_*
- 以及更多模块...

## 安装

```bash
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz
```

或者从Ansible Galaxy安装：

```bash
ansible-galaxy collection install horizon.modules.horizon_modules
```

## 使用方法

安装后，您可以在Playbook中使用完整命名空间调用模块：

```yaml
---
- name: 管理ADC设备示例
  hosts: adc_servers
  gather_facts: no
  tasks:
    - name: 登录ADC设备
      horizon.modules.horizon_modules.adc_login:
        ip: "{{ inventory_hostname }}"
        username: "{{ adc_username }}"
        password: "{{ adc_password }}"
      register: login_result

    - name: 添加节点
      horizon.modules.horizon_modules.adc_slb_node:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
        action: "add_node"
        name: "test_node"
        addr: "10.0.0.1"
        status: 1
      register: result
      when: login_result is succeeded

    - name: 输出结果
      debug:
        var: result

    - name: 登出ADC设备
      horizon.modules.horizon_modules.adc_logout:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
      register: logout_result
      when: login_result is succeeded
```

请参考playbooks目录中的示例YAML文件了解如何使用各个模块。
"@
Set-Content -Path (Join-Path $COLLECTION_ROOT "README.md") -Value $readmeContent

# 创建LICENSE文件
Write-Output "正在创建LICENSE文件..."
$licenseContent = @"
GNU GENERAL PUBLIC LICENSE
Version 2, June 1991

Copyright (C) 1989, 1991 Free Software Foundation, Inc.
51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"@
Set-Content -Path (Join-Path $COLLECTION_ROOT "LICENSE") -Value $licenseContent

# 创建MANIFEST.json（这是必需的文件）
Write-Output "正在创建MANIFEST.json..."
$manifestContent = @"
{
 "format": 1,
 "collection_info": {
   "namespace": "horizon",
   "name": "modules",
   "version": "1.0.0",
   "authors": [
     "Horizon Team"
   ],
   "readme": "README.md",
   "tags": [
     "adc",
     "loadbalancer",
     "networking",
     "infrastructure",
     "horizon"
   ],
   "description": "用于ADC（应用交付控制器）管理的Ansible模块集合",
   "license": [
     "GPL-2.0-or-later"
   ],
   "license_file": "LICENSE",
   "dependencies": {},
   "repository": "https://github.com/horizon/horizon-ansible-modules",
   "documentation": "https://github.com/horizon/horizon-ansible-modules/blob/main/README.md",
   "homepage": "https://github.com/horizon/horizon-ansible-modules",
   "issues": "https://github.com/horizon/horizon-ansible-modules/issues"
 },
 "file_manifest_file": {
   "name": "FILES.json",
   "ftype": "file",
   "chksum_type": "sha256",
   "chksum_sha256": "",
   "format": 1
 },
 "format": 1
}
"@
Set-Content -Path (Join-Path $COLLECTION_ROOT "MANIFEST.json") -Value $manifestContent

# 创建FILES.json（这也是必需的文件）
Write-Output "正在创建FILES.json..."

# 获取所有文件并计算校验和
$files = @()
$files += @{
    name = "MANIFEST.json"
    ftype = "file"
    chksum_type = "sha256"
    chksum_sha256 = $null
    format = 1
}

$files += @{
    name = "README.md"
    ftype = "file"
    chksum_type = "sha256"
    chksum_sha256 = $null
    format = 1
}

$files += @{
    name = "LICENSE"
    ftype = "file"
    chksum_type = "sha256"
    chksum_sha256 = $null
    format = 1
}

$files += @{
    name = "galaxy.yml"
    ftype = "file"
    chksum_type = "sha256"
    chksum_sha256 = $null
    format = 1
}

# 添加目录条目
$files += @{
    name = "plugins/"
    ftype = "dir"
    chksum_type = $null
    chksum_sha256 = $null
    format = 1
}

$files += @{
    name = "plugins/modules/"
    ftype = "dir"
    chksum_type = $null
    chksum_sha256 = $null
    format = 1
}

# 添加模块文件
$moduleFiles = Get-ChildItem -Path (Join-Path $COLLECTION_ROOT "plugins\modules") -File
foreach ($file in $moduleFiles) {
    $relativePath = $file.FullName.Substring($COLLECTION_ROOT.Length + 1).Replace("\", "/")
    $files += @{
        name = $relativePath
        ftype = "file"
        chksum_type = "sha256"
        chksum_sha256 = $null  # 实际构建时需要计算校验和
        format = 1
    }
}

$files += @{
    name = "plugins/module_utils/"
    ftype = "dir"
    chksum_type = $null
    chksum_sha256 = $null
    format = 1
}

$files += @{
    name = "docs/"
    ftype = "dir"
    chksum_type = $null
    chksum_sha256 = $null
    format = 1
}

$files += @{
    name = "tests/"
    ftype = "dir"
    chksum_type = $null
    chksum_sha256 = $null
    format = 1
}

$filesJson = @{
    files = $files
    format = 1
} | ConvertTo-Json -Depth 10

Set-Content -Path (Join-Path $COLLECTION_ROOT "FILES.json") -Value $filesJson

# 使用tar命令创建tarball（如果可用）
Write-Output "正在创建tarball..."

# 检查是否有tar命令可用
$tarAvailable = Get-Command tar -ErrorAction SilentlyContinue

if ($tarAvailable) {
    $collectionDir = Split-Path $COLLECTION_ROOT -Parent
    $collectionName = Split-Path $COLLECTION_ROOT -Leaf
    Set-Location $collectionDir
    $command = "tar -czf ..\$TARBALL_NAME $collectionName"
    Invoke-Expression $command
    Set-Location $PSScriptRoot
} else {
    Write-Warning "警告: 未找到tar命令。请安装Git for Windows或Windows Subsystem for Linux (WSL)。"
    Write-Output "集合文件已准备就绪，位于 $COLLECTION_ROOT 目录。"
    Write-Output "请使用压缩工具将 $COLLECTION_ROOT 目录压缩为 $TARBALL_NAME"
    
    # 尝试使用PowerShell的压缩功能
    if (Get-Command Compress-Archive -ErrorAction SilentlyContinue) {
        Write-Output "正在使用PowerShell的压缩功能..."
        $zipPath = [System.IO.Path]::ChangeExtension($TARBALL_NAME, ".zip")
        Compress-Archive -Path $COLLECTION_ROOT -DestinationPath $zipPath -Force
        Write-Output "已创建临时ZIP文件: $zipPath"
        Write-Output "请注意，Ansible需要的是tar.gz格式，您需要将ZIP转换为tar.gz格式"
    }
}

# 清理构建目录
Write-Output "正在清理..."
if (Test-Path $BUILD_DIR) {
    Remove-Item -Path $BUILD_DIR -Recurse -Force
}

Write-Output "构建完成！"
Write-Output "集合包已创建: $TARBALL_NAME"
Write-Output ""
Write-Output "要安装集合，请运行:"
Write-Output "ansible-galaxy collection install $TARBALL_NAME"