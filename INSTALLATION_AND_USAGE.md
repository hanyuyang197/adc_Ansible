# HORIZON ADC Ansible 模块集合 - 安装与使用指南

## 1. 集合包安装

### 本地安装

```bash
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz
```

### 从 Galaxy 安装（如果已发布）

```bash
ansible-galaxy collection install horizon.modules.horizon_modules
```

## 2. 验证安装

### 检查集合是否已安装

```bash
ansible-galaxy collection list | grep horizon
```

### 查看集合中包含的模块

```bash
ansible-doc -l | grep horizon.modules.horizon_modules
```

### 查看特定模块的文档

```bash
ansible-doc horizon.modules.horizon_modules.adc_slb_node
```

## 3. 配置 Inventory

创建 inventory 文件以定义目标 ADC 服务器：

```ini
[adc_servers]
10.5.116.35 ansible_connection=local

[adc_servers:vars]
adc_username=admin
adc_password=admin
```

## 4. 使用集合中的模块

### 基本使用示例

创建 [adc_example.yml](file:///C:%5C%E4BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8%5C8%E3%80%81%E5%B7%A1%E6%A3%80%E8%84%9A%E6%9C%AC%E9%9B%86%E5%90%88%5C%E6%B8%AF%E4%BA%A4%E6%89%80%5Cadc_Ansible%5Cexample_usage.yml) 文件：

```yaml
---
- name: HORIZON ADC模块集合使用示例
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
        name: "example_node"
        addr: "192.168.1.100"
        status: 1
        weight: 1
      register: node_result
      when: login_result is succeeded

    - name: 显示节点操作结果
      debug:
        var: node_result
      when: node_result is defined

    - name: 添加服务池
      horizon.modules.horizon_modules.adc_slb_pool:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
        action: "pool_add"
        name: "example_pool"
        lb_method: 0
        status: 1
      register: pool_result
      when: login_result is succeeded

    - name: 显示服务池操作结果
      debug:
        var: pool_result
      when: pool_result is defined

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

### 运行 Playbook

```bash
ansible-playbook -i inventory adc_example.yml
```

## 5. 集合中包含的主要模块

### SLB（服务器负载均衡）模块

- `horizon.modules.horizon_modules.adc_slb_node` - 节点管理
- `horizon.modules.horizon_modules.adc_slb_pool` - 服务池管理
- `horizon.modules.horizon_modules.adc_slb_healthcheck` - 健康检查管理
- `horizon.modules.horizon_modules.adc_slb_va` - 虚拟地址管理
- `horizon.modules.horizon_modules.adc_slb_va_vs` - 虚拟服务管理
- `horizon.modules.horizon_modules.adc_slb_profile_*` - 各类协议模板管理

### 网络模块

- `horizon.modules.horizon_modules.adc_network_*` - 网络配置相关

### 系统管理模块

- `horizon.modules.horizon_modules.adc_system_*` - 系统配置相关

### WAF 模块

- `horizon.modules.horizon_modules.adc_waf_*` - WAF 相关功能

### 认证模块

- `horizon.modules.horizon_modules.adc_login` - 登录
- `horizon.modules.horizon_modules.adc_logout` - 登出

## 6. 常见问题

### Q: 安装时提示 "does not contain the required file manifest.json"

A: 这个问题是由于之前的构建脚本没有正确创建 Ansible 集合必需的 MANIFEST.json 文件。现在已修复，使用新生成的包即可。

### Q: 模块找不到

A: 确保使用完整命名空间引用模块，如 `horizon.modules.horizon_modules.adc_slb_node`。

### Q: 连接问题

A: 确保 ADC 服务器 IP 地址正确，网络可达，并且认证凭据正确。

## 7. 最佳实践

1. **始终包含登录/登出步骤**：确保在操作前后正确登录和登出 ADC 设备
2. **使用条件执行**：使用 `when: login_result is succeeded` 确保仅在登录成功后执行操作
3. **捕获和调试结果**：使用 `register` 和 `debug` 任务来查看操作结果
4. **使用 Inventory 变量**：将认证凭据存储在 inventory 文件中，而不是硬编码在 playbook 中
5. **错误处理**：为关键操作添加适当的错误处理逻辑

## 8. 故障排除

### 检查模块路径

```bash
ansible-config dump | grep DEFAULT_MODULE_PATH
```

### 详细模式运行

```bash
ansible-playbook -i inventory adc_example.yml -vvv
```

### 测试连接

```bash
ansible adc_servers -i inventory -m ping
```
