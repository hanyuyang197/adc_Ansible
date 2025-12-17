# 新环境部署指南

当您将代码部署到新机器时，需要正确配置Ansible环境才能识别自定义模块。

## 1. 环境配置步骤

### 步骤1: 确保目录结构正确
确保您的项目目录结构如下：
```
/opt/adc_Ansible/
├── ansible.cfg
├── inventory
├── library/
│   ├── adc_login.py
│   ├── adc_logout.py
│   └── ... (所有模块文件)
└── playbooks/
    ├── waf_profile_list_example.yml
    └── ... (所有playbook文件)
```

### 步骤2: 验证ansible.cfg配置
确保ansible.cfg文件内容如下：
```ini
[defaults]
inventory = inventory
library = library
host_key_checking = False
```

### 步骤3: 验证inventory文件
确保inventory文件存在且配置正确：
```ini
[adc_servers]
192.168.1.100 ansible_connection=local

[adc_servers:vars]
adc_username=admin
adc_password=admin
```

## 2. 常见问题解决

### 问题1: Module not found错误
**错误信息**: `ERROR! couldn't resolve module/action 'adc_login'`

**根本原因**: Ansible未正确识别配置文件(ansible.cfg)和模块搜索路径

**解决方案**:
1. **确保在包含ansible.cfg文件的目录下运行ansible命令**
   - 这是最重要的一点，Ansible会自动在当前目录查找ansible.cfg
   
2. **验证ansible.cfg配置正确**
   - 检查ansible.cfg中的library路径是否正确指向模块目录
   - 确认模块文件存在于library目录中
   
3. **检查Ansible配置文件识别情况**
   - 运行 `ansible --version` 查看Configured module search path和Config file路径
   - 确保显示的路径指向正确的项目目录
   
4. **使用环境变量强制指定配置**
   - 设置 ANSIBLE_CONFIG 环境变量指向项目的ansible.cfg文件
   - 设置 ANSIBLE_LIBRARY 环境变量指向项目的library目录

### 问题2: Inventory not found错误
**错误信息**: `ERROR! Unable to parse /path/to/inventory as an inventory source`

**解决方案**:
1. 确保inventory文件存在
2. 验证ansible.cfg中的inventory路径正确
3. 检查inventory文件格式是否正确

## 3. 正确的运行方式

### 方式1: 在项目根目录运行（推荐）
```bash
cd /opt/adc_Ansible
ansible-playbook playbooks/waf_profile_list_example.yml
```

### 方式2: 使用增强环境变量脚本运行
为了确保Ansible正确识别配置文件和模块路径，我们提供了增强版环境变量设置脚本：

**Linux/macOS系统**:
```bash
# 运行增强环境设置脚本
source ./enhanced_setup_ansible_env.sh

# 使用便捷命令运行Ansible playbook
ansible_playbook_with_config playbooks/waf_profile_list_example.yml
```

**Windows系统**:
```cmd
# 运行增强环境设置脚本
enhanced_setup_ansible_env.bat

# 使用便捷命令运行Ansible playbook
ansible_playbook_with_config.bat playbooks/waf_profile_list_example.yml
```

### 方式3: 指定配置文件运行
```bash
ansible-playbook -c /opt/adc_Ansible/ansible.cfg playbooks/waf_profile_list_example.yml
```

### 方式4: 指定模块路径和inventory运行
```bash
ansible-playbook -M /opt/adc_Ansible/library -i /opt/adc_Ansible/inventory playbooks/waf_profile_list_example.yml
```

## 4. 验证配置是否正确

### 检查Ansible配置
```bash
cd /opt/adc_Ansible
ansible-config dump | grep DEFAULT_MODULE_PATH
ansible-config dump | grep DEFAULT_HOST_LIST
```

### 检查模块是否可见
```bash
cd /opt/adc_Ansible
ansible-doc -l | grep adc_
```

### 测试模块
```bash
cd /opt/adc_Ansible
ansible adc_servers -m adc_login -a "ip=192.168.1.100 username=admin password=admin"
```

## 5. 故障排除

### 如果仍然出现问题，请按以下步骤检查：

1. **检查当前工作目录**:
   ```bash
   pwd
   ls -la
   ```
   确保您在包含ansible.cfg的目录中

2. **检查模块文件权限**:
   ```bash
   ls -la library/
   ```
   确保模块文件具有可读权限

3. **检查Python环境**:
   ```bash
   python --version
   ansible --version
   ```

4. **启用详细输出进行调试**:
   ```bash
   ansible-playbook -vvv playbooks/waf_profile_list_example.yml
   ```

### 使用诊断工具

为帮助快速定位问题，我们提供了专门的诊断工具：

**Linux/macOS系统**:
```bash
# 运行诊断脚本
./diagnose_ansible_env.sh
```

**Windows系统**:
```cmd
# 运行诊断脚本
diagnose_ansible_env.bat
```

诊断工具会自动检查：
- 文件结构完整性
- 关键模块是否存在
- Ansible安装状态
- 环境变量配置
- 模块识别情况

并提供针对性的解决方案建议。

## 6. 最佳实践

1. **始终在项目根目录运行命令**
2. **不要移动或重命名关键配置文件**
3. **确保所有团队成员使用相同的目录结构**
4. **定期备份配置文件**
5. **使用环境变量脚本简化配置** - 推荐使用提供的环境变量设置脚本，避免路径配置问题

通过以上步骤，您应该能够成功在新环境中运行Ansible playbook。