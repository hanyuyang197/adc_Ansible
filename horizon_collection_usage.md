# Horizon Modules Ansible 集合包使用指南

## 概述

这是一个符合 Ansible 标准的集合包，名为 `horizon.modules`，包含用于 Horizon 系统操作的各种模块。

## 安装集合包

```bash
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz
```

或者安装到指定路径：

```bash
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz --collections-path ./collections
```

## 验证安装

```bash
ansible-galaxy collection list | grep horizon
```

## 使用示例

### 1. 基本用法

```yaml
---
- name: 使用Horizon模块示例
  hosts: localhost
  gather_facts: no
  collections:
    - horizon.modules

  tasks:
    - name: 执行ADC基础操作
      adc_base:
        state: present
      register: result

    - name: 显示结果
      debug:
        var: result
```

### 2. 网络配置示例

```yaml
---
- name: 配置网络设置
  hosts: adc_servers
  gather_facts: yes
  collections:
    - horizon.modules

  tasks:
    - name: 配置网络接口
      adc_network_interface:
        name: eth0
        ip: 192.168.1.100
        netmask: 255.255.255.0
      register: interface_result

    - name: 配置静态路由
      adc_network_route_static_ipv4:
        destination: 10.0.0.0
        gateway: 192.168.1.1
        metric: 1
```

### 3. 系统管理示例

```yaml
---
- name: 系统管理任务
  hosts: adc_servers
  gather_facts: yes
  collections:
    - horizon.modules

  tasks:
    - name: 配置系统时间
      adc_system_time:
        timezone: Asia/Shanghai
        ntp_servers:
          - 0.pool.ntp.org
          - 1.pool.ntp.org

    - name: 配置系统用户
      adc_system_user:
        username: admin
        password: "{{ vault_admin_password }}"
        role: administrator
```

## 可用模块列表

该集合包包含以下模块：

- `adc_base` - 基础 ADC 操作模块
- `adc_login` / `adc_logout` - 登录/登出模块
- `adc_network_*` - 网络相关模块（BGP, OSPF, VLAN, 接口等）
- `adc_slb_*` - 负载均衡相关模块（池、虚拟服务器、健康检查等）
- `adc_system_*` - 系统管理模块（用户、时间、日志等）
- `adc_waf_*` - WAF 配置模块
- 以及其他相关工具模块

## 高级用法

### 使用变量文件

创建 `vars.yml`:

```yaml
adc_config:
  server: "https://adc.example.com"
  username: "admin"
  password: "{{ vault_adc_password }}"
  validate_certs: false
```

在 playbook 中使用：

```yaml
---
- name: 使用变量文件的示例
  hosts: localhost
  gather_facts: no
  collections:
    - horizon.modules
  vars_files:
    - vars.yml

  tasks:
    - name: 使用配置变量
      adc_network_interface:
        <<: *adc_config
        name: eth0
        ip: "{{ target_ip }}"
```

## 故障排除

如果遇到安装问题，请确保：

1. Ansible 版本兼容（建议使用 2.9 或更高版本）
2. 集合包文件完整且未损坏
3. 正确的文件权限

验证命令：

```bash
ansible --version
ansible-galaxy collection list
```
