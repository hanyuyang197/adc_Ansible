# HORIZON ADC Ansible 模块集合 - 快速启动指南

## 1. 构建集合包

```bash
# 构建Ansible集合包
./build_collection.sh

# 预期输出：
# 正在构建HORIZON Ansible模块集合...
# 正在清理之前的构建...
# 正在创建目录结构...
# ...
# 构建完成！
# 集合包已创建: horizon-modules-1.0.0.tar.gz
```

## 2. 安装集合包

```bash
# 安装构建好的集合包
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz

# 预期输出：
# Starting galaxy collection install process
# Process install dependency map
# Starting collection install process
# Installing 'horizon.modules:1.0.0' to '/home/user/.ansible/collections/ansible_collections/horizon/modules'
```

## 3. 验证安装

```bash
# 检查集合是否安装成功
ansible-galaxy collection list | grep horizon

# 查看可用的模块
ansible-doc -l | grep horizon.modules.horizon_modules | head -10
```

## 4. 创建 Inventory 文件

创建 `inventory` 文件：

```ini
[adc_servers]
10.5.116.35 ansible_connection=local

[adc_servers:vars]
adc_username=admin
adc_password=admin
```

## 5. 创建示例 Playbook

创建 [test_connection.yml](file:///C:%5C%E4BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8%5C8%E3%80%81%E5%B7%A1%E6%A3%80%E8%84%9A%E6%9C%AC%E9%9B%86%E5%90%88%5C%E6%B8%AF%E4%BA%A4%E6%89%80%5Cadc_Ansible%5Cplaybooks%5Cnode_add_example.yml) 文件：

```yaml
---
- name: 测试ADC连接
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

    - name: 获取系统信息
      horizon.modules.horizon_modules.adc_system_global_config:
        ip: "{{ inventory_hostname }}"
        authkey: "{{ login_result.authkey }}"
        action: "get_system_info"
      register: system_info
      when: login_result is succeeded

    - name: 显示系统信息
      debug:
        var: system_info
      when: system_info is defined

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

## 6. 运行 Playbook

```bash
# 运行测试连接Playbook
ansible-playbook -i inventory test_connection.yml

# 预期输出：
# PLAY [测试ADC连接] **************************************************************
#
# TASK [登录ADC设备] **************************************************************
# ok: [10.5.116.35]
#
# TASK [显示登录结果] *************************************************************
# ok: [10.5.116.35] => {
#     "login_result": {...}
# }
# ...
```

## 7. 常用命令速查

```bash
# 列出所有已安装的集合
ansible-galaxy collection list

# 查看特定模块的文档
ansible-doc horizon.modules.horizon_modules.adc_slb_node

# 以详细模式运行Playbook（用于调试）
ansible-playbook -i inventory test_connection.yml -vvv

# 测试与ADC服务器的连接
ansible adc_servers -i inventory -m ping
```

## 8. 常见问题

### Q: 安装时提示 "does not contain the required file manifest.json"

A: 请确保使用更新后的 [build_collection.sh](file:///C:%5C%E4BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8%5C8%E3%80%81%E5%B7%A1%E6%A3%80%E8%84%9A%E6%9C%AC%E9%9B%86%E5%90%88%5C%E6%B8%AF%E4%BA%A4%E6%89%80%5Cadc_Ansible%5Cbuild_collection.sh) 脚本重新构建集合包。

### Q: 模块找不到

A: 检查集合是否正确安装，并验证模块名称是否使用完整命名空间（如 `horizon.modules.horizon_modules.adc_slb_node`）。

### Q: 连接超时

A: 确认 ADC 服务器 IP 地址正确，并检查网络连接。如果 ADC 服务器使用自签名证书，可能需要在模块中设置 `validate_certs: false`。
