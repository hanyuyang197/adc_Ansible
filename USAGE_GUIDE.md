# HORIZON ADC Ansible 模块集合使用指南

## 1. 构建集合包

运行以下命令构建 Ansible 集合包：

```bash
./build_collection.sh
```

构建完成后会生成 `horizon-modules-1.0.0.tar.gz` 文件。

## 2. 安装集合包

### 本地安装

```bash
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz
```

### 从 Galaxy 安装（如果已发布）

```bash
ansible-galaxy collection install horizon.modules.horizon_modules
```

## 3. 验证安装

验证集合是否安装成功：

```bash
ansible-galaxy collection list | grep horizon
```

或者查看可用模块：

```bash
ansible-doc -l | grep horizon.modules.horizon_modules
```

## 4. 配置 Inventory

创建 inventory 文件以定义目标 ADC 服务器：

```ini
[adc_servers]
10.5.116.35 ansible_connection=local

[adc_servers:vars]
adc_username=admin
adc_password=admin
```

## 5. 创建和使用 YAML Playbook

### 示例 Playbook: 添加节点

创建 [add_node.yml](file:///C:%5C%E4BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8%5C8%E3%80%81%E5%B7%A1%E6%A3%80%E8%84%9A%E6%9C%AC%E9%9B%86%E5%90%88%5C%E6%B8%AF%E4%BA%A4%E6%89%80%5Cadc_Ansible%5Cplaybooks%5Cnode_add_example.yml) 文件：

```yaml
---
- name: 添加ADC节点
  hosts: adc_servers
  gather_facts: no
  tasks:
    - name: 登录ADC设备
      horizon.modules.horizon_modules.adc_login:
        ip: "{{ inventory_hostname }}"
        username: "{{ adc_username }}"
        password: "{{ adc_password }}"
      register: login_result

    - name: 显示登录结果
      debug:
        var: login_result

    - name: 添加节点
      horizon.modules.horizon_modules.adc_slb_node:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
        action: "add_node"
        name: "test_node"
        addr: "192.168.1.100"
        status: 1
        weight: 1
      register: result
      when: login_result is succeeded

    - name: 输出结果
      debug:
        var: result
      when: result is defined

    - name: 登出ADC设备
      horizon.modules.horizon_modules.adc_logout:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
      register: logout_result
      when: login_result is succeeded

    - name: 显示登出结果
      debug:
        var: logout_result
      when: logout_result is defined
```

### 示例 Playbook: 管理服务池

创建 [manage_pool.yml](file:///C:%5C%E4BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8%5C8%E3%80%81%E5%B7%A1%E6%A3%80%E8%84%9A%E6%9C%AC%E9%9B%86%E5%90%88%5C%E6%B8%AF%E4%BA%A4%E6%89%80%5Cadc_Ansible%5Cplaybooks%5Cslb_pool_member_add.yml) 文件：

```yaml
---
- name: 管理ADC服务池
  hosts: adc_servers
  gather_facts: no
  tasks:
    - name: 登录ADC设备
      horizon.modules.horizon_modules.adc_login:
        ip: "{{ inventory_hostname }}"
        username: "{{ adc_username }}"
        password: "{{ adc_password }}"
      register: login_result

    - name: 添加服务池
      horizon.modules.horizon_modules.adc_slb_pool:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
        action: "pool_add"
        name: "test_pool"
        lb_method: 0
        status: 1
      register: pool_result
      when: login_result is succeeded

    - name: 输出服务池结果
      debug:
        var: pool_result
      when: pool_result is defined

    - name: 登出ADC设备
      horizon.modules.horizon_modules.adc_logout:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
      register: logout_result
      when: login_result is succeeded
```

## 6. 运行 Playbook

使用以下命令运行 Playbook：

```bash
# 运行添加节点的Playbook
ansible-playbook -i inventory add_node.yml

# 运行管理服务池的Playbook
ansible-playbook -i inventory manage_pool.yml

# 使用详细输出模式
ansible-playbook -i inventory add_node.yml -vvv
```

## 7. 模块列表

HORIZON ADC 模块集合包含以下模块：

### SLB（服务器负载均衡）模块

- `horizon.modules.horizon_modules.adc_slb_node` - 节点管理
- `horizon.modules.horizon_modules.adc_slb_pool` - 服务池管理
- `horizon.modules.horizon_modules.adc_slb_healthcheck` - 健康检查管理
- `horizon.modules.horizon_modules.adc_slb_va` - 虚拟地址管理
- `horizon.modules.horizon_modules.adc_slb_va_vs` - 虚拟服务管理
- `horizon.modules.horizon_modules.adc_slb_profile_*` - 各类协议模板管理

### 系统管理模块

- `horizon.modules.horizon_modules.adc_system_global_config` - 系统全局配置
- `horizon.modules.horizon_modules.adc_system_partition` - 分区管理
- `horizon.modules.horizon_modules.adc_system_ntp` - NTP 配置
- `horizon.modules.horizon_modules.adc_system_log_*` - 日志相关配置

### WAF 模块

- `horizon.modules.horizon_modules.adc_waf_*` - WAF 相关功能

### 认证模块

- `horizon.modules.horizon_modules.adc_login` - 登录
- `horizon.modules.horizon_modules.adc_logout` - 登出

## 8. 故障排除

### 检查模块路径

```bash
ansible-config dump | grep DEFAULT_MODULE_PATH
```

### 查看模块文档

```bash
ansible-doc horizon.modules.horizon_modules.adc_slb_node
```

### 测试连接

```bash
ansible adc_servers -i inventory -m ping
```

## 9. 最佳实践

1. 始终在 Playbook 中包含登录和登出步骤
2. 使用`when`条件确保在登录成功后才执行操作
3. 使用`register`捕获结果并进行调试
4. 将敏感信息存储在 inventory 或 vault 中，而不是硬编码在 Playbook 中
5. 使用版本控制管理 Playbook 文件
