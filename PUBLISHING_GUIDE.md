# 发布 Horizon Modules 到 Ansible Galaxy 完整指南

## 概述

本文档提供了将 Horizon Modules 集合包发布到 Ansible Galaxy 的完整指南，参考 F5 f5_modules 的成功案例。

## 为什么发布到 Galaxy

1. **社区可见性** - 让更多用户发现和使用您的模块
2. **易于安装** - 用户可以通过简单命令安装
3. **版本管理** - Galaxy 提供版本控制和依赖管理
4. **标准化** - 遵循 Ansible 社区标准

## 与 F5 f5_modules 的对比

| 特性        | F5 f5_modules                                                                                              | Horizon Modules                                                        |
| ----------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Galaxy 地址 | https://galaxy.ansible.com/ui/repo/published/f5networks/f5_modules/                                        | https://galaxy.ansible.com/ui/repo/published/horizon/modules/ (待发布) |
| GitHub 仓库 | https://github.com/F5Networks/f5-ansible/                                                                  | https://github.com/horizon/horizon-ansible-modules (待创建)            |
| 文档        | https://docs.ansible.com/projects/ansible/latest/collections/f5networks/f5_modules/index.html#plugin-index | https://horizon.com/docs/ansible-modules (待配置)                      |

## 准备工作

### 1. 创建 GitHub 仓库

创建一个新的 GitHub 仓库：

```bash
# 创建仓库结构
horizon-ansible-modules/
├── README.md
├── galaxy.yml
├── meta/
│   └── runtime.yml
├── plugins/
│   └── modules/
│       └── adc_*.py
├── docs/
├── changelogs/
├── tests/
└── .github/
    └── workflows/
        └── publish.yml
```

### 2. 配置项目元数据

在 `galaxy.yml` 中配置：

```yaml
namespace: horizon
name: modules
version: 1.0.0
readme: README.md
authors:
  - "Horizon ADC Team"
description: Ansible collection for Horizon ADC device management
license:
  - GPL-3.0-only
tags:
  - horizon
  - adc
  - networking
  - loadbalancer
  - slb
dependencies: {}
repository: "https://github.com/horizon/horizon-ansible-modules"
documentation: "https://horizon.com/docs/ansible-modules"
homepage: "https://horizon.com"
issues: "https://github.com/horizon/horizon-ansible-modules/issues"
```

### 3. 创建完整的 README.md

````markdown
# Horizon Modules

Ansible 集合，用于管理 Horizon ADC 设备。

## 安装

```bash
ansible-galaxy collection install horizon.modules
```
````

## 使用

```yaml
---
- name: 管理 Horizon ADC 设备
  hosts: adc_servers
  collections:
    - horizon.modules

  tasks:
    - name: 添加节点
      adc_slb_node:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
        action: "add_node"
        name: "test_node"
        addr: "10.0.0.1"
        status: 1
      register: result
```

## 模块列表

- `adc_slb_node` - 节点管理
- `adc_slb_pool` - 服务池管理
- `adc_slb_va` - 虚拟地址管理
- ... (所有 ADC 模块)

## 许可证

GPL-3.0-only

````

## 发布流程

### 1. 注册 Galaxy 账户

1. 访问 https://galaxy.ansible.com/
2. 注册并登录
3. 创建命名空间 "horizon"（如果可用）

### 2. 生成 API Token

1. 登录 Galaxy
2. 访问 Profile > API Token
3. 生成新的 API Token

### 3. 配置本地环境

```bash
# 配置 Galaxy Token
ansible-galaxy login
# 或者手动配置
ansible-galaxy config set token YOUR_API_TOKEN
````

### 4. 构建和测试

```bash
# 构建集合包
python build_collection.py

# 本地安装测试
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz

# 验证安装
ansible-galaxy collection list | grep horizon
```

### 5. 创建 GitHub 仓库

1. 在 GitHub 上创建新仓库 `horizon-ansible-modules`
2. 推送代码
3. 创建初始版本标签

### 6. 发布到 Galaxy

```bash
# 发布到 Galaxy
ansible-galaxy collection publish horizon-modules-1.0.0.tar.gz
```

## 自动化发布

### GitHub Actions 配置

`.github/workflows/publish.yml`:

```yaml
name: Publish Collection to Ansible Galaxy

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"

      - name: Install Ansible
        run: pip install ansible-core

      - name: Build Collection
        run: |
          python build_collection.py

      - name: Publish to Galaxy
        run: |
          ansible-galaxy collection publish horizon-modules-1.0.0.tar.gz --api-key ${{ secrets.GALAXY_API_KEY }}
        env:
          GALAXY_API_KEY: ${{ secrets.GALAXY_API_KEY }}
```

## 版本管理策略

### 版本号规范

- 主版本号：重大变更，不兼容的 API 更改
- 次版本号：向后兼容的功能添加
- 修订号：向后兼容的问题修正

### 发布流程

1. 更新 `galaxy.yml` 中的版本号
2. 提交代码并创建 Git 标签
3. 创建 GitHub Release
4. 自动发布到 Galaxy

## 文档和示例

### 为每个模块创建文档

在 `docs/` 目录下为每个模块创建文档：

```
docs/
├── adc_slb_node.md
├── adc_slb_pool.md
├── adc_system_user.md
└── ...
```

### 提供使用示例

在 `playbooks/` 目录下提供完整示例，这些示例已经准备好了。

## 社区支持

### 问题跟踪

- GitHub Issues: https://github.com/horizon/horizon-ansible-modules/issues
- 问题响应时间: 24-48 小时

### 贡献指南

创建 `CONTRIBUTING.md`:

```markdown
# 贡献指南

欢迎贡献代码！

## 开发环境

1. 克隆仓库
2. 安装依赖: `pip install ansible`
3. 运行测试

## 代码规范

- 遵循 Ansible 模块开发最佳实践
- 提供完整文档
- 包含测试用例
```

## 维护计划

### 定期维护

- 月度版本更新
- 安全漏洞修复
- 新功能开发

### 长期支持

- 为重要版本提供长期支持
- 向后兼容性保证
- 文档持续更新

## 成功案例参考

### F5 f5_modules 的成功要素

1. **完整文档** - 详细的模块文档和使用示例
2. **活跃维护** - 定期更新和问题修复
3. **社区支持** - 积极响应用户反馈
4. **质量保证** - 充分的测试和验证

### 我们的优势

1. **专业领域** - 专注 ADC 设备管理
2. **完整功能** - 覆盖所有 ADC 管理功能
3. **标准化** - 符合 Ansible 最佳实践
4. **易用性** - 简单的安装和使用方式

## 后续步骤

1. [ ] 创建 GitHub 仓库
2. [ ] 配置命名空间
3. [ ] 准备完整文档
4. [ ] 发布初始版本
5. [ ] 推广和宣传
6. [ ] 收集用户反馈
7. [ ] 持续改进

## 联系方式

- 项目维护者: Horizon ADC Team
- 邮箱: support@horizon.com
- GitHub: https://github.com/horizon/horizon-ansible-modules
