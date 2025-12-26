# 发布到 Ansible Galaxy 指南

## 概述

本文档介绍了如何将 Horizon Modules 集合包发布到 Ansible Galaxy，使其可供社区使用，类似于 F5 的 f5_modules 集合。

## 发布前准备

### 1. 创建 Ansible Galaxy 账户

- 访问 https://galaxy.ansible.com/
- 注册账户并登录

### 2. 生成 Ansible Galaxy API Token

- 登录后访问个人资料页面
- 生成 API Token，用于发布操作

### 3. 安装 Ansible

确保已安装 Ansible 2.9 或更高版本：

```bash
pip install ansible
```

## 集合包结构要求

当前项目已经符合 Ansible 集合包标准：

```
horizon-modules-1.0.0/
├── docs/
├── galaxy.yml          # 集合元数据
├── MANIFEST.json       # 构建时自动生成
├── FILES.json          # 构建时自动生成
├── meta/
│   └── runtime.yml
├── plugins/
│   └── modules/
│       ├── adc_*.py    # 所有模块文件
│       └── ...
├── README.md
└── requirements.txt
```

## 发布步骤

### 1. 构建集合包

使用项目提供的构建脚本：

```bash
# Python 方式（推荐）
python build_collection.py

# 或 Linux/macOS 方式
./build_collection.sh

# 或 Windows 方式
build_collection.bat
```

### 2. 验证集合包

安装并测试集合包：

```bash
# 本地安装测试
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz

# 列出已安装的集合
ansible-galaxy collection list | grep horizon
```

### 3. 配置 Ansible Galaxy API Token

```bash
ansible-galaxy login
```

或者手动配置：

```bash
# 创建或编辑 ~/.ansible/galaxy_token
[galaxy_server]
url = https://galaxy.ansible.com
token = YOUR_API_TOKEN_HERE
```

### 4. 发布到 Ansible Galaxy

```bash
ansible-galaxy collection publish horizon-modules-1.0.0.tar.gz
```

## Galaxy 配置文件说明

### galaxy.yml 详解

```yaml
namespace: horizon # 命名空间，需在 Galaxy 中唯一
name: modules # 集合名称
version: 1.0.0 # 版本号，遵循语义化版本
readme: README.md # 说明文档
authors: # 作者信息
  - "Horizon ADC Team"
description: >- # 集合描述
  Ansible collection for Horizon ADC device management
license: # 许可证
  - GPL-3.0-only
tags: # 标签，便于搜索
  - horizon
  - adc
  - networking
  - loadbalancer
  - slb
dependencies: {} # 依赖关系
repository: >- # 源码仓库地址
  https://github.com/horizon/horizon-ansible-modules
documentation: >- # 文档地址
  https://horizon.com/docs/ansible-modules
homepage: >- # 主页
  https://horizon.com
issues: >- # 问题跟踪地址
  https://github.com/horizon/horizon-ansible-modules/issues
```

## Galaxy 平台配置

### 1. 在 Galaxy 上创建命名空间

- 登录 Galaxy 后创建 "horizon" 命名空间
- 如果命名空间已被占用，需要选择其他名称

### 2. 关联 GitHub 仓库

- 在 Galaxy 设置中关联 GitHub 仓库
- 配置自动构建和发布

## 版本管理

### 版本号规范

- 遵循语义化版本控制 (SemVer)
- 格式: MAJOR.MINOR.PATCH
- 例如: 1.0.0, 1.0.1, 1.1.0, 2.0.0

### 发布新版本

1. 更新 `galaxy.yml` 中的版本号
2. 重新构建集合包
3. 发布到 Galaxy

## 最佳实践

### 1. 文档完善

- 提供详细的 README.md
- 为每个模块编写文档
- 提供使用示例

### 2. 测试覆盖

- 确保模块功能测试通过
- 提供完整的使用示例

### 3. 持续集成

- 配置 CI/CD 流水线
- 自动构建和发布新版本

## 参考示例

### F5 Modules 集合参考

- Galaxy 地址: https://galaxy.ansible.com/ui/repo/published/f5networks/f5_modules/
- GitHub 仓库: https://github.com/F5Networks/f5-ansible/
- 文档: https://docs.ansible.com/projects/ansible/latest/collections/f5networks/f5_modules/index.html#plugin-index

### 与 F5 集合的相似性

- 相同的目录结构
- 标准的 galaxy.yml 配置
- 完整的模块文档
- 版本管理

## 故障排除

### 常见问题

1. **命名空间冲突**

   - 如果 "horizon" 已被占用，选择其他命名空间

2. **API Token 问题**

   - 确保 Token 权限正确
   - 检查 Token 是否过期

3. **构建失败**
   - 验证 MANIFEST.json 和 FILES.json 格式
   - 确保所有必需文件存在

## 后续步骤

1. 准备 GitHub 仓库
2. 创建 Galaxy 命名空间
3. 配置 CI/CD 流水线
4. 发布初始版本
5. 推广和维护

## 注意事项

- 发布前确保代码质量
- 遵循 Ansible 集合开发最佳实践
- 提供充分的文档和示例
- 考虑用户反馈和持续改进
