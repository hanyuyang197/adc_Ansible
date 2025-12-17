# ADC Ansible 模块开发任务列表

## 已完成的任务

### 测试文档

- [x] 测试指南文档 (TEST_GUIDE.md)
- [x] 快速入门指南 (QUICK_START.md)
- [x] 模块功能概览 (MODULES_OVERVIEW.md)
- [x] 新环境部署指南 (DEPLOYMENT_GUIDE.md)
- [x] 环境变量设置脚本 (setup_ansible_env.sh, setup_ansible_env.bat)
- [x] 增强环境变量设置脚本 (enhanced_setup_ansible_env.sh, enhanced_setup_ansible_env.bat)
- [x] 环境诊断工具 (diagnose_ansible_env.sh, diagnose_ansible_env.bat)

### 网络模块

- [x] VLAN 管理模块 (adc_network_vlan.py)
- [x] TRUNK 管理模块 (adc_network_trunk.py)
- [x] IPv4 标准访问列表模块 (adc_network_acl_ipv4_std.py)
- [x] IPv4 扩展访问列表模块 (adc_network_acl_ipv4_ext.py)
- [x] IPv6 访问列表模块 (adc_network_acl_ipv6.py)
- [x] 端口列表模板模块 (adc_network_port_list_profile.py)
- [x] NAT 地址池模块 (adc_network_nat_pool.py)
- [x] 网络 NAT 模块 (adc_network_nat_network.py)
- [x] NAT 映射模块 (adc_network_nat_map.py)
- [x] NAT 策略模块 (adc_network_nat_policy.py)
- [x] IPv4 静态路由模块 (adc_network_route_static_ipv4.py)
- [x] IPv6 静态路由模块 (adc_network_route_static_ipv6.py)
- [x] 网络模式管理模块 (adc_network_mode.py)
- [x] NAT 地址池统计信息模块 (adc_network_nat_pool_stats.py)
- [x] NAT 地址池组模块 (adc_network_nat_pool_group.py)
- [x] 静态 NAT 模块 (adc_network_nat_static.py)
- [x] NAT 超时配置模块 (adc_network_nat_timeout.py)
- [x] NAT 全局配置模块 (adc_network_nat_global.py)
- [x] IPv4 静态管理路由模块 (adc_network_route_static_mgmt_ipv4.py)
- [x] IPv6 静态管理路由模块 (adc_network_route_static_mgmt_ipv6.py)
- [x] IPv4 静态控制路由模块 (adc_network_route_static_ctrl_ipv4.py)
- [x] IPv6 静态控制路由模块 (adc_network_route_static_ctrl_ipv6.py)
- [x] OSPF 模块 (adc_network_ospf.py)
- [x] BGP 模块 (adc_network_bgp.py)
- [x] SYN Cookie 模块 (adc_network_syn_cookie.py)
- [x] 接口管理模块 (adc_network_interface.py)
- [x] LLDP 模块 (adc_network_lldp.py)
- [x] ARP 模块 (adc_network_arp.py)
- [x] DDoS 防护模块 (adc_network_ddos.py)
- [x] 流量控制(TC)模块 (adc_network_tc.py)

### 系统模块

- [x] 安全标识模块 (adc_system_security_banner.py)
- [x] 系统配置模块 (adc_system_dns.py, adc_system_hostname.py, adc_system_hosts.py, adc_system_banner.py, adc_system_time.py)
- [x] SNMP 管理模块 (adc_system_snmp.py)
- [x] SNMPv3 管理模块 (adc_system_snmp_v3.py)
- [x] 用户管理模块 (adc_system_user.py)
- [x] 系统时间范围模块 (adc_system_timerange.py)
- [x] 分区管理模块 (adc_system_partition.py)
- [x] 客户端锁定模块 (adc_system_client_lock.py)
- [x] AAA 认证模块 (adc_system_aaa.py)
- [x] NTP 配置模块 (adc_system_ntp.py)
- [x] WEB 会话模块 (adc_system_web_session.py)
- [x] WEB 证书管理模块 (adc_system_web_cert.py)
- [x] WEB 网页加密算法和版本模块 (adc_system_web_ciphers.py)
- [x] 系统应用端口模块 (adc_system_ports.py)
- [x] 系统操作模块 (adc_system_operations.py)
- [x] 配置文件管理模块 (adc_system_config_file.py)
- [x] 域名解析自定义管理模块 (adc_system_domain_table.py)

## 待完成的任务

根据 adc_api_system_doc.md 文件和用户要求，需要检查是否还有其他系统模块需要开发，排除以下内容：

- 管理--》平台、会话、许可管理
- 维护：恢复出厂
- 调试
- 镜像
- 自动备份
- 诊断信息
- 系统报告
- 硬件检查
- 控制台

### 需要开发的系统模块

- [x] SMTP 配置模块 (adc_system_smtp.py)
- [x] 日志配置模块 (adc_system_log_config.py)
- [x] 日志获取模块 (adc_system_log_get.py)
- [x] 日志发送模块 (adc_system_log_send.py)
- [x] 日志告警模块 (adc_system_log_alarm.py)
- [x] 高可用性模块 (adc_system_ha_vrrp.py)
