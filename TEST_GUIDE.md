# ADC Ansible 模块测试指南

## 目录

1. [项目概述](#项目概述)
2. [环境准备](#环境准备)
3. [安装指南](#安装指南)
4. [框架介绍](#框架介绍)
5. [模块使用指南](#模块使用指南)
6. [常见问题](#常见问题)

## 项目概述

本项目是一套针对 ADC（应用交付控制器）设备的 Ansible 自动化模块集合，提供了完整的网络管理和系统管理功能，包括：

- VLAN、Trunk、ACL、路由等网络配置管理
- 用户、认证、日志、SNMP 等系统配置管理
- 负载均衡、虚拟服务、健康检查等 SLB 功能
- WAF、DDoS 防护等安全功能

## 环境准备

### 支持的操作系统

- CentOS 7.x/8.x
- RHEL 7.x/8.x
- Ubuntu 18.04/20.04

### 必需软件

- Python 2.7 或 Python 3.6+
- Ansible 2.9+
- SSH 客户端

## 安装指南

### 1. 安装 Ansible (CentOS/RHEL)

```bash
# CentOS 7
sudo yum install epel-release
sudo yum install ansible

# CentOS 8/RHEL 8
sudo dnf install epel-release
sudo dnf install ansible
```

### 2. 验证 Ansible 安装

```bash
ansible --version
```

### 3. 克隆项目代码

```bash
git clone <项目仓库地址>
cd adc_Ansible
```

### 4. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 5. 配置 Inventory 文件

编辑 `inventory` 文件，配置目标 ADC 设备信息：

```ini
[adc_servers]
192.168.1.100 ansible_connection=local

[adc_servers:vars]
adc_username=admin
adc_password=admin
```

## 框架介绍

### 项目结构

```
adc_Ansible/
├── library/              # 自定义Ansible模块
│   ├── adc_network_*.py   # 网络管理模块
│   ├── adc_system_*.py    # 系统管理模块
│   ├── adc_slb_*.py       # 负载均衡模块
│   └── adc_waf_profile.py # WAF模板模块
├── playbooks/            # 示例playbook
│   ├── network/          # 网络相关playbook
│   ├── system/           # 系统相关playbook
│   └── slb/              # SLB相关playbook
├── inventory             # 主机清单文件
└── README.md             # 项目说明文档
```

### 模块分类

1. **网络管理模块**

   - VLAN 管理: `adc_network_vlan`
   - Trunk 管理: `adc_network_trunk`
   - ACL 管理: `adc_network_acl_ipv4_std`, `adc_network_acl_ipv4_ext`, `adc_network_acl_ipv6`
   - 路由管理: `adc_network_route_static_ipv4`, `adc_network_route_static_ipv6`
   - NAT 管理: `adc_network_nat_pool`, `adc_network_nat_policy`等

2. **系统管理模块**

   - 用户管理: `adc_system_user`
   - 认证配置: `adc_system_aaa`
   - 日志配置: `adc_system_log_config`, `adc_system_log_send`
   - SNMP 管理: `adc_system_snmp`, `adc_system_snmp_v3`

3. **SLB 模块**

   - 节点管理: `adc_slb_node`
   - 池管理: `adc_slb_pool`
   - 虚拟服务: `adc_slb_profile_vs`
   - 健康检查: `adc_slb_healthcheck`

4. **安全模块**
   - WAF 模板: `adc_waf_profile`
   - DDoS 防护: `adc_network_ddos`

## 模块使用指南

### 基本使用流程

所有操作都遵循以下流程：

1. 登录设备获取 authkey
2. 执行具体操作
3. 登出设备释放会话

### 示例 1: 创建 VLAN

```yaml
---
- name: 创建VLAN示例
  hosts: adc_servers
  gather_facts: no
  vars:
    # 变量从inventory文件获取
  tasks:
    - name: 登录ADC设备
      adc_login:
        ip: "{{ inventory_hostname }}"
        username: "{{ adc_username }}"
        password: "{{ adc_password }}"
      register: login_result

    - name: 创建VLAN
      adc_network_vlan:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
        action: "add_vlan"
        id: 100
        name: "test_vlan"
        status: 1
      register: result

    - name: 显示结果
      debug:
        var: result

    - name: 登出ADC设备
      adc_logout:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
```

执行命令：

```bash
ansible-playbook playbooks/vlan_add_example.yml
```

### 示例 2: 管理 WAF 模板

```yaml
---
- name: WAF模板管理示例
  hosts: adc_servers
  gather_facts: no
  vars:
  tasks:
    - name: 登录ADC设备
      adc_login:
        ip: "{{ inventory_hostname }}"
        username: "{{ adc_username }}"
        password: "{{ adc_password }}"
      register: login_result

    - name: 添加WAF模板
      adc_waf_profile:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
        action: add_profile
        name: "test_waf_profile"
        rule_name: "wrule_123.txt"
        mode: 2
        enable: 1
      register: result

    - name: 显示结果
      debug:
        var: result

    - name: 登出ADC设备
      adc_logout:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
```

### 常用操作示例

#### 网络操作

- 查看 VLAN 列表: `ansible-playbook playbooks/vlan_list_example.yml`
- 创建 Trunk: `ansible-playbook playbooks/trunk_add_example.yml`
- 配置静态路由: `ansible-playbook playbooks/route_static_ipv4_add_example.yml`

#### 系统操作

- 添加用户: `ansible-playbook playbooks/system/user/add_user.yml`
- 配置 SNMP: `ansible-playbook playbooks/system/snmp/set_snmp_server.yml`
- 配置日志: `ansible-playbook playbooks/system/log/set_service_log_config.yml`

#### SLB 操作

- 添加节点: `ansible-playbook playbooks/node_add_example.yml`
- 创建池: `ansible-playbook playbooks/pool_add_example.yml`
- 配置虚拟服务: `ansible-playbook playbooks/vs_add_http_example.yml`

## 常见问题

### 1. "authkey 未定义"错误

**问题**: `The task includes an option with an undefined variable. The error was: 'authkey' is undefined`

**解决方法**: 确保 playbook 中包含登录步骤，并正确使用`login_result.authkey`

### 2. "list object has no attribute get"错误

**问题**: `AttributeError: 'list' object has no attribute 'get'`

**解决方法**: 这是模块内部处理结果类型的 bug，已在最新版本中修复

### 3. 连接超时

**问题**: `Connection timed out`

**解决方法**:

- 检查 ADC 设备 IP 地址是否正确
- 确认网络连通性
- 检查设备是否正常运行

### 4. 认证失败

**问题**: `Authentication failed`

**解决方法**:

- 检查用户名和密码是否正确
- 确认用户具有相应权限
- 检查设备认证配置

### 5. 模块找不到

**问题**: `ERROR! couldn't resolve module action`

**解决方法**:

- 确认在正确的目录下执行 playbook
- 检查 library 目录是否存在相应模块文件

## 测试建议

1. **测试环境**: 建议使用测试环境的 ADC 设备进行测试
2. **备份配置**: 测试前备份设备配置
3. **逐步测试**: 从简单操作开始，逐步测试复杂功能
4. **日志记录**: 启用详细日志记录便于问题排查
5. **清理测试**: 测试完成后清理测试数据

## 联系方式

如有问题，请联系开发团队：

- 开发负责人: [您的姓名]
- 技术支持邮箱: [技术支持邮箱]
