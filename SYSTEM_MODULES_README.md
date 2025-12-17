# ADC 系统管理 Ansible 模块

本文档介绍了为 ADC 设备系统管理功能开发的 Ansible 模块和示例 playbook。

## 已创建的模块

### 1. 安全标识模块

- **模块文件**: `library/adc_system_security_banner.py`
- **功能**: 登录安全标识的获取和设置
- **支持的操作**:
  - `get_security_banner`: 获取登录安全标识
  - `set_security_banner`: 设置登录安全标识

### 2. 系统配置模块

- **模块文件**: `library/adc_system_dns.py`
- **功能**: DNS 服务器配置的设置和获取
- **支持的操作**:

  - `get_dns`: 获取 DNS 服务器配置
  - `set_dns`: 设置 DNS 服务器配置

- **模块文件**: `library/adc_system_hostname.py`
- **功能**: 主机名配置的设置和获取
- **支持的操作**:

  - `set_hostname`: 设置系统主机名
  - `get_hostname_ipv4`: 获取主机名 IPv4 地址
  - `set_hostname_ipv4`: 设置主机名 IPv4 地址
  - `get_hostname_ipv6`: 获取主机名 IPv6 地址
  - `set_hostname_ipv6`: 设置主机名 IPv6 地址

- **模块文件**: `library/adc_system_hosts.py`
- **功能**: Hosts 配置的管理
- **支持的操作**:

  - `list_hosts`: 获取 Hosts 列表
  - `add_host`: 添加 Hosts 记录
  - `delete_host`: 删除 Hosts 记录

- **模块文件**: `library/adc_system_banner.py`
- **功能**: 系统 Banner 信息获取
- **支持的操作**:

  - `get_system_banner`: 获取系统 Banner 信息

- **模块文件**: `library/adc_system_time.py`
- **功能**: 时间配置的设置和获取
- **支持的操作**:
  - `get_time`: 获取时间配置
  - `set_time`: 设置时间配置

### 3. SNMP 管理模块

- **模块文件**: `library/adc_system_snmp.py`
- **功能**: SNMP 配置的管理
- **支持的操作**:
  - `add_snmp_community`: 添加 SNMP 团体字
  - `list_snmp_communities`: 获取 SNMP 团体字列表
  - `delete_snmp_community`: 删除 SNMP 团体字
  - `set_snmp_server`: 设置 SNMP 服务配置
  - `get_snmp_server`: 获取 SNMP 服务配置
  - `add_snmp_trap`: 添加 SNMP TRAP
  - `list_snmp_traps`: 获取 SNMP TRAP 列表
  - `delete_snmp_trap`: 删除 SNMP TRAP
  - `set_snmp_trap`: 设置 SNMP TRAP 配置
  - `get_snmp_trap`: 获取 SNMP TRAP 配置

### 4. SNMPv3 管理模块

- **模块文件**: `library/adc_system_snmp_v3.py`
- **功能**: SNMPv3 配置的管理
- **支持的操作**:
  - `add_view`: 添加 SNMPv3 视图
  - `list_views`: 获取 SNMPv3 视图列表
  - `get_view`: 获取 SNMPv3 视图
  - `delete_view`: 删除 SNMPv3 视图
  - `edit_view`: 编辑 SNMPv3 视图
  - `add_group`: 添加 SNMPv3 组
  - `list_groups`: 获取 SNMPv3 组列表
  - `get_group`: 获取 SNMPv3 组
  - `delete_group`: 删除 SNMPv3 组
  - `edit_group`: 编辑 SNMPv3 组
  - `add_user`: 添加 SNMPv3 用户
  - `list_users`: 获取 SNMPv3 用户列表
  - `get_user`: 获取 SNMPv3 用户
  - `delete_user`: 删除 SNMPv3 用户
  - `edit_user`: 编辑 SNMPv3 用户
  - `add_trap`: 添加 SNMPv3 TRAP
  - `list_traps`: 获取 SNMPv3 TRAP 列表
  - `get_trap`: 获取 SNMPv3 TRAP
  - `delete_trap`: 删除 SNMPv3 TRAP
  - `edit_trap`: 编辑 SNMPv3 TRAP

### 5. 用户管理模块

- **模块文件**: `library/adc_system_user.py`
- **功能**: 用户配置的管理
- **支持的操作**:
  - `add_user`: 添加用户
  - `list_users`: 获取用户列表
  - `get_user`: 获取指定用户
  - `edit_user`: 编辑指定用户
  - `delete_user`: 删除指定用户
  - `set_user_config`: 设置用户锁定和密码配置
  - `get_user_config`: 获取用户锁定配置和密码配置
  - `unlock_user`: 解锁锁定用户
  - `change_password`: 修改当前用户密码

### 6. 系统时间范围模块

- **模块文件**: `library/adc_system_timerange.py`
- **功能**: 系统时间范围的管理
- **支持的操作**:
  - `list_timeranges`: 获取时间范围列表
  - `get_timerange`: 获取时间范围详情
  - `add_timerange`: 添加时间范围
  - `edit_timerange`: 编辑时间范围
  - `delete_timerange`: 删除时间范围

### 7. 分区管理模块

- **模块文件**: `library/adc_system_partition.py`
- **功能**: 分区的管理
- **支持的操作**:
  - `list_partitions`: 获取分区列表
  - `get_partition`: 获取指定分区
  - `add_partition`: 添加分区
  - `edit_partition`: 编辑指定分区
  - `delete_partition`: 删除指定分区
  - `switch_partition`: 切换不同分区

### 8. 客户端锁定模块

- **模块文件**: `library/adc_system_client_lock.py`
- **功能**: 客户端锁定配置的管理
- **支持的操作**:
  - `set_client_lock_config`: 设置客户端锁定配置
  - `get_client_lock_config`: 获取客户端锁定配置
  - `list_locked_clients`: 获取锁定客户端列表
  - `unlock_client`: 解锁锁定客户端

### 9. AAA 认证模块

- **模块文件**: `library/adc_system_aaa.py`
- **功能**: AAA 认证配置的管理
- **支持的操作**:
  - `set_aaa_general_config`: AAA 全局配置设置
  - `get_aaa_general_config`: AAA 全局配置获取
  - `set_radius_config`: Radius 认证配置设置
  - `get_radius_config`: Radius 认证配置获取
  - `set_tacacs_config`: TACACS+认证配置设置
  - `get_tacacs_config`: TACACS+认证配置获取

### 10. NTP 配置模块

- **模块文件**: `library/adc_system_ntp.py`
- **功能**: NTP 配置的管理
- **支持的操作**:
  - `add_ntp_config`: 添加 NTP 配置
  - `list_ntp_configs`: 获取 NTP 配置列表
  - `get_ntp_config`: 获取指定 NTP 配置
  - `edit_ntp_config`: 编辑 NTP 配置
  - `delete_ntp_config`: 删除指定 NTP 配置

### 11. WEB 会话模块

- **模块文件**: `library/adc_system_web_session.py`
- **功能**: WEB 会话配置的管理
- **支持的操作**:
  - `set_web_session_config`: 设置 WEB 会话超时时间及是否默认显示高级选项
  - `get_web_session_config`: 获取 WEB 会话超时时间及是否默认显示高级选项
  - `set_web_session_limit`: 设置 WEB 会话限制
  - `get_web_session_limit`: 获取 WEB 会话限制配置

### 12. WEB 证书管理模块

- **模块文件**: `library/adc_system_web_cert.py`
- **功能**: WEB 证书的管理
- **支持的操作**:
  - `list_web_certs`: 获取 web 证书列表
  - `delete_web_cert`: 删除 web 证书
  - `apply_web_cert`: 应用 web 证书
  - `upload_web_key`: 上传 web 私钥文件
  - `download_web_key`: 下载 web 私钥文件
  - `upload_web_cert`: 上传 web 证书文件
  - `download_web_cert`: 下载 web 证书文件

### 13. WEB 网页加密算法和版本模块

- **模块文件**: `library/adc_system_web_ciphers.py`
- **功能**: WEB 网页加密算法和版本的管理
- **支持的操作**:
  - `get_web_ciphers`: 获取 web 网页加密算法和版本
  - `set_web_ciphers`: 设置 web 网页加密算法和版本

### 14. 系统应用端口模块

- **模块文件**: `library/adc_system_ports.py`
- **功能**: 系统应用端口配置的管理
- **支持的操作**:
  - `set_system_ports`: 设置系统应用端口配置
  - `get_system_ports`: 获取系统应用端口配置

### 15. 系统操作模块

- **模块文件**: `library/adc_system_operations.py`
- **功能**: 系统操作的执行
- **支持的操作**:
  - `save_config`: 保存配置
  - `reboot_system`: 系统重启
  - `reload_config`: 重新加载配置
  - `shutdown_system`: 系统关机

### 16. 配置文件管理模块

- **模块文件**: `library/adc_system_config_file.py`
- **功能**: 配置文件的管理
- **支持的操作**:
  - `add_config_file`: 添加配置文件
  - `list_config_files`: 获取配置文件列表
  - `apply_config_file`: 指定配置文件
  - `delete_config_file`: 删除配置文件
  - `backup_config_file`: 配置文件导出
  - `restore_config_file`: 配置文件导入

### 17. 域名解析自定义管理模块

- **模块文件**: `library/adc_system_domain_table.py`
- **功能**: 域名解析自定义的管理
- **支持的操作**:
  - `list_domain_tables`: 获取域名解析自定义列表
  - `add_domain_table`: 添加域名解析自定义
  - `delete_domain_table`: 删除域名解析自定义
  - `list_domain_files`: 查看域名表文件列表
  - `upload_domain_file`: 上传域名表文件
  - `delete_domain_file`: 删除域名表文件

## 示例 Playbook

每个模块都配有相应的示例 playbook，位于`playbooks/system/`目录下：

### 安全标识相关示例

- `security_banner/get_security_banner.yml`: 获取登录安全标识示例
- `security_banner/set_security_banner.yml`: 设置登录安全标识示例

### 系统配置相关示例

- `dns/get_dns.yml`: 获取 DNS 服务器配置示例
- `dns/set_dns.yml`: 设置 DNS 服务器配置示例
- `hostname/set_hostname.yml`: 设置系统主机名示例
- `hostname/get_hostname_ipv4.yml`: 获取主机名 IPv4 地址示例
- `hostname/set_hostname_ipv4.yml`: 设置主机名 IPv4 地址示例
- `hostname/get_hostname_ipv6.yml`: 获取主机名 IPv6 地址示例
- `hostname/set_hostname_ipv6.yml`: 设置主机名 IPv6 地址示例
- `hosts/list_hosts.yml`: 获取 Hosts 列表示例
- `hosts/add_host.yml`: 添加 Hosts 记录示例
- `hosts/delete_host.yml`: 删除 Hosts 记录示例
- `banner/get_system_banner.yml`: 获取系统 Banner 信息示例
- `time/get_time.yml`: 获取时间配置示例
- `time/set_time.yml`: 设置时间配置示例

### SNMP 相关示例

- `snmp/add_snmp_community.yml`: 添加 SNMP 团体字示例
- `snmp/list_snmp_communities.yml`: 获取 SNMP 团体字列表示例
- `snmp/delete_snmp_community.yml`: 删除 SNMP 团体字示例
- `snmp/set_snmp_server.yml`: 设置 SNMP 服务配置示例
- `snmp/get_snmp_server.yml`: 获取 SNMP 服务配置示例
- `snmp/add_snmp_trap.yml`: 添加 SNMP TRAP 示例
- `snmp/list_snmp_traps.yml`: 获取 SNMP TRAP 列表示例
- `snmp/delete_snmp_trap.yml`: 删除 SNMP TRAP 示例
- `snmp/set_snmp_trap.yml`: 设置 SNMP TRAP 配置示例
- `snmp/get_snmp_trap.yml`: 获取 SNMP TRAP 配置示例

### SNMPv3 相关示例

- `snmp_v3/add_view.yml`: 添加 SNMPv3 视图示例
- `snmp_v3/list_views.yml`: 获取 SNMPv3 视图列表示例
- `snmp_v3/get_view.yml`: 获取 SNMPv3 视图示例
- `snmp_v3/delete_view.yml`: 删除 SNMPv3 视图示例
- `snmp_v3/edit_view.yml`: 编辑 SNMPv3 视图示例
- `snmp_v3/add_group.yml`: 添加 SNMPv3 组示例
- `snmp_v3/list_groups.yml`: 获取 SNMPv3 组列表示例
- `snmp_v3/get_group.yml`: 获取 SNMPv3 组示例
- `snmp_v3/delete_group.yml`: 删除 SNMPv3 组示例
- `snmp_v3/edit_group.yml`: 编辑 SNMPv3 组示例
- `snmp_v3/add_user.yml`: 添加 SNMPv3 用户示例
- `snmp_v3/list_users.yml`: 获取 SNMPv3 用户列表示例
- `snmp_v3/get_user.yml`: 获取 SNMPv3 用户示例
- `snmp_v3/delete_user.yml`: 删除 SNMPv3 用户示例
- `snmp_v3/edit_user.yml`: 编辑 SNMPv3 用户示例
- `snmp_v3/add_trap.yml`: 添加 SNMPv3 TRAP 示例
- `snmp_v3/list_traps.yml`: 获取 SNMPv3 TRAP 列表示例
- `snmp_v3/get_trap.yml`: 获取 SNMPv3 TRAP 示例
- `snmp_v3/delete_trap.yml`: 删除 SNMPv3 TRAP 示例
- `snmp_v3/edit_trap.yml`: 编辑 SNMPv3 TRAP 示例

### 用户管理相关示例

- `user/add_user.yml`: 添加用户示例
- `user/list_users.yml`: 获取用户列表示例
- `user/get_user.yml`: 获取指定用户示例
- `user/edit_user.yml`: 编辑指定用户示例
- `user/delete_user.yml`: 删除指定用户示例
- `user/set_user_config.yml`: 设置用户锁定和密码配置示例
- `user/get_user_config.yml`: 获取用户锁定配置和密码配置示例
- `user/unlock_user.yml`: 解锁锁定用户示例
- `user/change_password.yml`: 修改当前用户密码示例

### 系统时间范围相关示例

- `timerange/list_timeranges.yml`: 获取时间范围列表示例
- `timerange/get_timerange.yml`: 获取时间范围详情示例
- `timerange/add_timerange.yml`: 添加时间范围示例
- `timerange/edit_timerange.yml`: 编辑时间范围示例
- `timerange/delete_timerange.yml`: 删除时间范围示例

### 分区管理相关示例

- `partition/list_partitions.yml`: 获取分区列表示例
- `partition/get_partition.yml`: 获取指定分区示例
- `partition/add_partition.yml`: 添加分区示例
- `partition/edit_partition.yml`: 编辑指定分区示例
- `partition/delete_partition.yml`: 删除指定分区示例
- `partition/switch_partition.yml`: 切换不同分区示例

### 客户端锁定相关示例

- `client_lock/set_client_lock_config.yml`: 设置客户端锁定配置示例
- `client_lock/get_client_lock_config.yml`: 获取客户端锁定配置示例
- `client_lock/list_locked_clients.yml`: 获取锁定客户端列表示例
- `client_lock/unlock_client.yml`: 解锁锁定客户端示例

### AAA 认证相关示例

- `aaa/set_aaa_general_config.yml`: AAA 全局配置设置示例
- `aaa/get_aaa_general_config.yml`: AAA 全局配置获取示例
- `aaa/set_radius_config.yml`: Radius 认证配置设置示例
- `aaa/get_radius_config.yml`: Radius 认证配置获取示例
- `aaa/set_tacacs_config.yml`: TACACS+认证配置设置示例
- `aaa/get_tacacs_config.yml`: TACACS+认证配置获取示例

### NTP 配置相关示例

- `ntp/add_ntp_config.yml`: 添加 NTP 配置示例
- `ntp/list_ntp_configs.yml`: 获取 NTP 配置列表示例
- `ntp/get_ntp_config.yml`: 获取指定 NTP 配置示例
- `ntp/edit_ntp_config.yml`: 编辑 NTP 配置示例
- `ntp/delete_ntp_config.yml`: 删除指定 NTP 配置示例

### WEB 会话相关示例

- `web_session/set_web_session_config.yml`: 设置 WEB 会话超时时间及是否默认显示高级选项示例
- `web_session/get_web_session_config.yml`: 获取 WEB 会话超时时间及是否默认显示高级选项示例
- `web_session/set_web_session_limit.yml`: 设置 WEB 会话限制示例
- `web_session/get_web_session_limit.yml`: 获取 WEB 会话限制配置示例

### WEB 证书管理相关示例

- `web_cert/list_web_certs.yml`: 获取 web 证书列表示例
- `web_cert/delete_web_cert.yml`: 删除 web 证书示例
- `web_cert/apply_web_cert.yml`: 应用 web 证书示例
- `web_cert/upload_web_key.yml`: 上传 web 私钥文件示例
- `web_cert/download_web_key.yml`: 下载 web 私钥文件示例
- `web_cert/upload_web_cert.yml`: 上传 web 证书文件示例
- `web_cert/download_web_cert.yml`: 下载 web 证书文件示例

### WEB 网页加密算法和版本相关示例

- `web_ciphers/get_web_ciphers.yml`: 获取 web 网页加密算法和版本示例
- `web_ciphers/set_web_ciphers.yml`: 设置 web 网页加密算法和版本示例

### 系统应用端口相关示例

- `ports/set_system_ports.yml`: 设置系统应用端口配置示例
- `ports/get_system_ports.yml`: 获取系统应用端口配置示例

### 系统操作相关示例

- `operations/save_config.yml`: 保存配置示例
- `operations/reboot_system.yml`: 系统重启示例
- `operations/reload_config.yml`: 重新加载配置示例
- `operations/shutdown_system.yml`: 系统关机示例

### 配置文件管理相关示例

- `config_file/add_config_file.yml`: 添加配置文件示例
- `config_file/list_config_files.yml`: 获取配置文件列表示例
- `config_file/apply_config_file.yml`: 指定配置文件示例
- `config_file/delete_config_file.yml`: 删除配置文件示例
- `config_file/backup_config_file.yml`: 配置文件导出示例
- `config_file/restore_config_file.yml`: 配置文件导入示例

### 域名解析自定义管理相关示例

- `domain_table/list_domain_tables.yml`: 获取域名解析自定义列表示例
- `domain_table/add_domain_table.yml`: 添加域名解析自定义示例
- `domain_table/delete_domain_table.yml`: 删除域名解析自定义示例
- `domain_table/list_domain_files.yml`: 查看域名表文件列表示例
- `domain_table/delete_domain_file.yml`: 删除域名表文件示例

## 使用方法

1. 确保 Ansible 环境已正确配置
2. 将模块文件放置在`library/`目录下
3. 根据需要修改 playbook 中的 IP 地址、用户名和密码等参数
4. 运行 playbook:
   ```bash
   ansible-playbook playbooks/system/user/list_users.yml
   ```

## 注意事项

1. 所有操作前请确保已正确配置 ADC 设备的 IP 地址和认证信息
2. 删除资源时请遵循依赖关系，先删除被依赖的资源
3. 建议在测试环境中验证所有操作后再在生产环境中使用
