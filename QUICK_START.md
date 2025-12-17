# ADC Ansible 模块快速入门指南

## 1. 环境准备

### CentOS 7 安装 Ansible

```bash
sudo yum install epel-release
sudo yum install ansible
```

### 验证安装

```bash
ansible --version
```

## 2. 配置设备信息

编辑 `inventory` 文件：

```ini
[adc_servers]
192.168.1.100 ansible_connection=local

[adc_servers:vars]
adc_username=admin
adc_password=admin
```

## 3. 快速测试

### 测试登录功能

```bash
ansible-playbook playbooks/login_test.yml
```

### 查看 VLAN 列表

```bash
ansible-playbook playbooks/vlan_list_example.yml
```

### 查看 WAF 模板列表

```bash
ansible-playbook playbooks/waf_profile_list_example.yml
```

## 4. 常用模块分类

### 网络管理

- VLAN: `adc_network_vlan`
- Trunk: `adc_network_trunk`
- ACL: `adc_network_acl_ipv4_std`, `adc_network_acl_ipv4_ext`
- 路由: `adc_network_route_static_ipv4`, `adc_network_route_static_ipv6`

### 系统管理

- 用户: `adc_system_user`
- 日志: `adc_system_log_config`
- SNMP: `adc_system_snmp`

### 负载均衡

- 节点: `adc_slb_node`
- 池: `adc_slb_pool`
- 虚拟服务: `adc_slb_profile_vs`

### 安全

- WAF: `adc_waf_profile`

## 5. 基本使用模式

所有操作都遵循以下模式：

```yaml
---
- name: 操作示例
  hosts: adc_servers
  gather_facts: no
  tasks:
    - name: 登录
      adc_login:
        ip: "{{ inventory_hostname }}"
        username: "{{ adc_username }}"
        password: "{{ adc_password }}"
      register: login_result

    - name: 执行操作
      adc_模块名:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
        action: "操作类型"
        # 其他参数...
      register: result

    - name: 显示结果
      debug:
        var: result

    - name: 登出
      adc_logout:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
```
