# HORIZON Ansible 模块集合

此集合提供了用于管理 ADC（应用交付控制器）设备的 Ansible 模块。

## 安装

### 先决条件

- Ansible 2.9 或更高版本
- Python 2.7 或 Python 3.6+

### 安装方法

#### 方法 1：从 Galaxy 安装（推荐）

```bash
ansible-galaxy collection install horizon.modules.horizon_modules
```

#### 方法 2：从 tarball 安装

下载集合 tarball 并在本地安装：

```bash
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz
```

#### 方法 3：从本地构建安装

在本地构建集合并安装。项目提供三种构建方式：

#### Python 脚本方式（通用）

```bash
# 使用Python构建（推荐）
python build_collection.py

# 安装集合
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz
```

#### Shell 脚本方式（Linux/macOS）

```bash
# 构建集合（Linux/macOS）
chmod +x build_collection.sh
./build_collection.sh

# 安装集合
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz
```

#### 批处理脚本方式（Windows）

```cmd
REM 构建集合（Windows）
build_collection.bat

REM 安装集合
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz
```

## 使用方法

### 在 Playbook 中使用

要在 playbook 中使用此集合中的模块，请指定完整的命名空间路径：

```yaml
---
- name: 示例playbook
  hosts: adc_servers
  gather_facts: no

  tasks:
    - name: 添加节点
      horizon.modules.horizon_modules.adc_slb_node:
        ip: "192.168.1.100"
        authkey: "{{ login_result.authkey }}"
        action: "add_node"
        name: "test_node"
        addr: "10.0.0.1"
        status: 1
      register: result

    - name: 显示结果
      debug:
        var: result
```

### 可用模块

该集合包含以下模块：

- `adc_slb_node` - 节点管理
- `adc_slb_node_port` - 节点端口管理
- `adc_slb_pool` - 服务池管理
- `adc_slb_healthcheck` - 健康检查管理
- `adc_slb_va` - 虚拟地址管理
- `adc_slb_va_vs` - 虚拟服务管理
- `adc_slb_profile_*` - 配置文件管理（fastl4, tcp, udp, http 等）
- 以及更多模块...

## 配置

### Inventory 设置

将您的 ADC 设备添加到 Ansible inventory 中：

```ini
[adc_servers]
adc1 ansible_host=192.168.1.100
adc2 ansible_host=192.168.1.101
```

### 变量

模块通常需要以下变量：

- `ip`: ADC 设备的 IP 地址
- `authkey`: 从登录获得的认证密钥
- `action`: 要执行的操作（因模块而异）

## 构建集合

要从源代码构建集合：

1. 克隆仓库
2. 运行构建脚本：
   ```bash
   ./build_collection.sh
   ```

这将创建一个可以用 ansible-galaxy 安装的 tarball。

## 变更日志

### 1.0.0

- 初始版本
- 包含所有 ADC 管理模块
- 支持所有主要 ADC 功能
