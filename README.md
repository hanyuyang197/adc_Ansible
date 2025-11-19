# ADC Ansible 自动化管理工具

## 项目概述

本项目是一个基于Ansible的自动化工具集，用于管理ADC（Application Delivery Controller）设备。通过自定义Ansible模块，可以实现对ADC设备的登录、登出以及节点管理等操作。

## 目录结构

```
adc_Ansible/
├── ansible.cfg                 # Ansible配置文件
├── inventory                   # 主机清单文件
├── library/                    # 自定义Ansible模块
│   ├── adc_login.py           # 登录模块
│   ├── adc_logout.py          # 登出模块
│   └── adc_node.py            # 节点管理模块
└── playbooks/                 # Ansible剧本
    ├── login_logout_test.yml  # 登录登出测试剧本
    ├── node_add_example.yml   # 节点添加示例剧本
    ├── node_edit_example.yml  # 节点编辑示例剧本
    ├── node_management_test.yml # 节点管理测试剧本
```

## 环境要求

### Python环境
- Python 2.7 或 Python 3.6+
- Ansible 2.9+

### 安装Ansible

#### 在Linux/macOS上安装
```bash
# 使用pip安装
pip install ansible

# 或使用包管理器安装（Ubuntu/Debian）
sudo apt update
sudo apt install ansible

# 或使用包管理器安装（CentOS/RHEL）
sudo yum install ansible
```

#### 在Windows上安装
由于Windows原生环境对Ansible支持有限，推荐以下方案：
1. **WSL（推荐）**：安装Windows Subsystem for Linux，然后在WSL中安装Ansible
2. **Docker**：使用包含Ansible的Docker容器
3. **虚拟机**：在Linux虚拟机中安装Ansible

## 配置说明

### 1. 主机清单配置（inventory文件）

编辑inventory文件，配置目标ADC设备的IP地址：

```ini
[adc_servers]
10.5.116.35 ansible_connection=local

[adc_servers:vars]
adc_username=admin
adc_password=admin
```

### 2. Ansible配置（ansible.cfg文件）

```ini
[defaults]
inventory = inventory
library = library
host_key_checking = False
```

### 3. 环境变量设置

在Linux/WSL环境中运行时，可能需要设置以下环境变量：

```bash
# 设置Ansible库路径（如果需要）
export ANSIBLE_LIBRARY=./library

# 设置主机清单文件路径
export ANSIBLE_INVENTORY=./inventory

# 设置配置文件路径
export ANSIBLE_CONFIG=./ansible.cfg
```

## 使用方法

### 1. 测试登录登出功能

```bash
ansible-playbook playbooks/login_logout_test.yml
```

### 2. 添加节点示例

```bash
ansible-playbook playbooks/node_add_example.yml
```

### 3. 编辑节点示例

```bash
ansible-playbook playbooks/node_edit_example.yml
```

### 4. 节点管理测试

```bash
ansible-playbook playbooks/node_management_test.yml
```

### 5. 节点端口添加示例

```bash
ansible-playbook playbooks/node_port_add_example.yml
```

### 6. 节点端口编辑示例

```bash
ansible-playbook playbooks/node_port_edit_example.yml
```

### 7. 节点端口删除示例

```bash
ansible-playbook playbooks/node_port_delete_example.yml
```

### 8. 节点列表示例 (slb.node.list)

```bash
ansible-playbook playbooks/node_list_example.yml
```

### 9. 获取节点详情示例 (slb.node.get)

```bash
ansible-playbook playbooks/node_get_example.yml
```

### 10. 服务池列表示例

```bash
ansible-playbook playbooks/pool_list_example.yml
```

### 11. 服务池添加示例

```bash
ansible-playbook playbooks/pool_add_example.yml
```

### 12. 服务池获取详情示例

```bash
ansible-playbook playbooks/pool_get_example.yml
```

### 13. 服务池编辑示例

```bash
ansible-playbook playbooks/pool_edit_example.yml
```

### 14. 服务池删除示例

```bash
ansible-playbook playbooks/pool_delete_example.yml
```

## 模块说明

### adc_login模块
- **功能**：登录ADC设备并获取authkey
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `username`：用户名（必需）
  - `password`：密码（必需）
- **返回**：`authkey`

### adc_logout模块
- **功能**：登出ADC设备，使authkey失效
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `authkey`：登录时获取的认证密钥（必需）
- **返回**：登出结果

### adc_slb_node模块
- **功能**：管理ADC节点
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `authkey`：登录时获取的认证密钥（必需）
  - `action`：操作类型，可选值：`get_nodes`、`list_nodes`、`get_node`、`add_node`、`edit_node`、`delete_node`、`add_node_port`、`edit_node_port`、`delete_node_port`（必需）
  - `name`：节点名称（添加/编辑/删除节点及端口操作时必需）
  - `host`：节点主机地址（可选）
  - `weight`：权重（可选，默认为1）
  - `status`：状态（可选，默认为1）
  - `conn_limit`：连接限制（可选）
  - `healthcheck`：健康检查名称（可选）
  - `template`：模板名称（可选）
  - `conn_rate_limit`：连接速率限制（可选）
  - `desc_rserver`：节点描述（可选）
  - `graceful_time`：软关机超时时间（可选）
  - `graceful_delete`：删除节点触发软关机（可选）
  - `graceful_disable`：禁用节点触发软关机（可选）
  - `graceful_persist`：禁用节点触发软关机后会话保持表有效（可选）
  - `slow_start_type`：暖启动类型（可选）
  - `slow_start_recover`：暖启动恢复时间（可选）
  - `slow_start_rate`：暖启动变化规则（可选）
  - `slow_start_from`：暖启动初始量（可选）
  - `slow_start_step`：暖启动增量（可选）
  - `slow_start_interval`：暖启动间隔（可选）
  - `slow_start_interval_num`：暖启动间隔数（可选）
  - `slow_start_tail`：暖启动结束量（可选）
  - `request_rate_limit`：请求速率限制（可选）
  - `ports`：端口列表（可选）
  - `port_port_number`：端口端口号（可选）
  - `port_protocol`：端口协议类型（可选）
  - `port_status`：端口使能状态（可选）
  - `port_weight`：端口权重（可选）
  - `port_graceful_time`：软关机超时单位秒（可选）
  - `port_graceful_delete`：删除节点触发软关机（可选）
  - `port_graceful_disable`：禁用节点触发软关机（可选）
  - `port_graceful_persist`：禁用节点触发软关机后会话保持表有效（可选）
  - `port_conn_limit`：端口连接限制（可选）
  - `port_phm_profile`：被动健康检查名称（可选）
  - `port_healthcheck`：主动健康检查名称（可选）
  - `port_upnum`：可用性要求（可选）
  - `port_nat_strategy`：NAT策略名（可选）

### adc_slb_pool模块
- **功能**：管理ADC服务池
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `authkey`：登录时获取的认证密钥（必需）
  - `action`：操作类型，可选值：`get_pools`、`get_pool`、`add_pool`、`edit_pool`、`delete_pool`（必需）
  - `name`：服务池名称（添加/编辑/删除/获取详情时必需）
  - `protocol`：服务池协议，0为TCP，1为UDP（可选，默认为0）
  - `lb_method`：负载均衡算法（可选，默认为0）
  - `upnum`：可用性要求（可选，默认为0）
  - `healthcheck`：健康检查名称（可选，默认为空字符串）
  - `desc_pool`：服务池描述（可选，默认为空字符串）
  - `action_on_service_down`：服务池故障重置（可选，默认为0）
  - `aux_node_log`：优先级日志（可选，默认为0）
  - `up_members_at_least_status`：优先级规则状态（可选）
  - `up_members_at_least_num`：最少正常成员数（可选）
  - `up_members_at_least_type`：优先级规则类型（可选）

## 常见问题及解决方案

### 1. "skipping: no hosts matched" 错误

**问题原因**：Ansible无法匹配到inventory中定义的主机。

**解决方案**：
- 检查inventory文件中的主机地址是否正确
- 确保Ansible能够通过SSH或winrm连接到目标主机
- 验证ansible.cfg配置文件是否正确指向了inventory文件

### 2. 模块导入错误

**问题原因**：Ansible无法找到自定义模块。

**解决方案**：
- 确保自定义模块放置在library目录下
- 检查ansible.cfg中的library配置是否正确
- 设置ANSIBLE_LIBRARY环境变量显式指定模块路径

### 3. SSL证书验证错误

**问题原因**：目标服务器使用自签名证书。

**解决方案**：
- 在模块调用中设置`validate_certs: false`跳过证书验证
- 或在ansible.cfg中配置忽略主机密钥检查

### 4. Windows环境下运行问题

**问题原因**：Windows原生环境对Ansible支持有限。

**解决方案**：
- 推荐使用WSL环境运行
- 或使用Docker容器化运行
- 或在Linux服务器上直接运行

## 运行目录要求

1. **路径规范**：避免使用包含空格或中文等特殊字符的路径
2. **权限要求**：确保运行用户对项目目录有读写权限
3. **工作目录**：运行Ansible命令时应在项目根目录下执行

## 调试和测试

### 查看详细输出
使用`-v`参数查看详细输出：
```bash
ansible-playbook -v playbooks/login_logout_test.yml
```

### 检查语法
检查playbook语法是否正确：
```bash
ansible-playbook --syntax-check playbooks/login_logout_test.yml
```

### 列出主机
查看匹配的主机列表：
```bash
ansible-playbook --list-hosts playbooks/login_logout_test.yml
```

## 注意事项

1. **IP地址配置**：默认使用10.5.116.35作为测试IP，请根据实际情况修改inventory文件
2. **认证信息**：默认用户名和密码为admin/admin，请根据实际情况修改
3. **模块兼容性**：自定义模块兼容Python 2.7和Python 3.x环境
4. **安全性**：在生产环境中，请使用安全的方式管理密码，避免明文存储

## 版本信息

- Ansible版本：2.9+
- Python版本：2.7 或 3.6+
- 最后更新：2025年

## 许可证

本项目仅供内部使用。