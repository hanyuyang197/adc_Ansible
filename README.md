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
    └── node_management_test.yml # 节点管理测试剧本
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

### 3. 节点管理测试

```bash
ansible-playbook playbooks/node_management_test.yml
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

### adc_node模块
- **功能**：管理ADC节点
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `authkey`：登录时获取的认证密钥（必需）
  - `action`：操作类型，可选值：`get_nodes`、`add_node`、`remove_node`（必需）
  - `tc_name`：流量控制名称（可选）
  - `name`：节点名称（可选）
  - `host`：节点主机地址（可选）
  - `weight`：权重（可选，默认为1）
  - `status`：状态（可选，默认为1）
  - `ports`：端口列表（可选）
  - `node_id`：节点ID（删除节点时必需）

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