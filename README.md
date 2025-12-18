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

### 8. 节点端口启用/禁用示例

```bash
ansible-playbook playbooks/node_port_onoff_example.yml
```

### 9. 服务池列表示例

```bash
ansible-playbook playbooks/pool_list_example.yml
```

### 10. 服务池添加示例

```bash
ansible-playbook playbooks/pool_add_example.yml
```

### 11. 服务池获取详情示例

```bash
ansible-playbook playbooks/pool_get_example.yml
```

### 12. 服务池编辑示例

```bash
ansible-playbook playbooks/pool_edit_example.yml
```

### 13. 服务池删除示例

```bash
ansible-playbook playbooks/pool_delete_example.yml
```

### 14. 虚拟地址列表示例

```bash
ansible-playbook playbooks/va_list_example.yml
```

### 15. 获取虚拟地址详情示例

```bash
ansible-playbook playbooks/va_get_example.yml
```

### 16. 添加 IPv4 类型虚拟地址示例

```bash
ansible-playbook playbooks/va_add_ipv4_example.yml
```

### 17. 添加子网类型虚拟地址示例

```bash
ansible-playbook playbooks/va_add_subnet_example.yml
```

### 18. 添加 IPv4 ACL 类型虚拟地址示例

```bash
ansible-playbook playbooks/va_add_acl_ipv4_example.yml
```

### 19. 添加 IPv6 ACL 类型虚拟地址示例

```bash
ansible-playbook playbooks/va_add_acl_ipv6_example.yml
```

### 20. 编辑虚拟地址示例

```bash
ansible-playbook playbooks/va_edit_example.yml
```

### 21. 删除虚拟地址示例

```bash
ansible-playbook playbooks/va_delete_example.yml
```

### 22. 虚拟地址状态列表示例

```bash
ansible-playbook playbooks/va_stat_list_example.yml
```

### 23. 获取虚拟地址状态详情示例

```bash
ansible-playbook playbooks/va_stat_get_example.yml
```

### 24. 添加 DNS 类型虚拟服务示例

```bash
ansible-playbook playbooks/vs_add_dns_example.yml
```

### 25. 添加 FTP 类型虚拟服务示例

```bash
ansible-playbook playbooks/vs_add_ftp_example.yml
```

### 26. 添加 HTTP 普通类型虚拟服务示例

```bash
ansible-playbook playbooks/vs_add_http_example.yml
```

### 27. 添加 HTTPS 类型虚拟服务示例

```bash
ansible-playbook playbooks/vs_add_https_example.yml
```

### 28. 添加 TCP 类型虚拟服务示例

```bash
ansible-playbook playbooks/vs_add_tcp_example.yml
```

### 29. 编辑虚拟服务示例

```bash
ansible-playbook playbooks/vs_edit_example.yml
```

### 30. 删除虚拟服务示例

```bash
ansible-playbook playbooks/vs_delete_example.yml
```

### 31. 获取虚拟服务详情示例

```bash
ansible-playbook playbooks/vs_get_example.yml
```

### 32. 获取虚拟服务状态示例

```bash
ansible-playbook playbooks/vs_stat_get_example.yml
```

### 33. 获取虚拟服务状态汇总示例

```bash
ansible-playbook playbooks/vs_stat_list_count_example.yml
```

### 34. 健康检查列表示例

```bash
ansible-playbook playbooks/healthcheck_list_example.yml
```

### 35. 获取健康检查详情示例

```bash
ansible-playbook playbooks/healthcheck_get_example.yml
```

### 36. 添加 ICMP 健康检查示例

```bash
ansible-playbook playbooks/healthcheck_add_icmp_example.yml
```

### 37. 添加 HTTP 健康检查示例

```bash
ansible-playbook playbooks/healthcheck_add_http_example.yml
```

### 38. 添加 HTTPS 健康检查示例

```bash
ansible-playbook playbooks/healthcheck_add_https_example.yml
```

### 39. 添加 TCP 健康检查示例

```bash
ansible-playbook playbooks/healthcheck_add_tcp_example.yml
```

### 40. 添加 Combo 健康检查示例

```bash
ansible-playbook playbooks/healthcheck_add_combo_example.yml
```

### 41. 编辑健康检查示例

```bash
ansible-playbook playbooks/healthcheck_edit_example.yml
```

### 42. 删除健康检查示例

```bash
ansible-playbook playbooks/healthcheck_delete_example.yml
```

### 43. 获取 SLB 状态列表示例

```bash
ansible-playbook playbooks/slb_states_list_example.yml
```

### 44. 清除 SLB 会话示例

```bash
ansible-playbook playbooks/slb_session_clear_example.yml
```

### 45. 完整测试场景 - HTTP

```bash
ansible-playbook playbooks/complete_test_http_scenario.yml
```

### 46. 完整测试场景 - HTTPS

```bash
ansible-playbook playbooks/complete_test_https_scenario.yml
```

### 47. 节点创建测试

```bash
ansible-playbook playbooks/test_node_creation.yml
```

### 48. TCP 代理模板列表示例

```bash
ansible-playbook playbooks/fastl4_profile_list_example.yml
```

### 49. 获取 TCP 代理模板详情示例

```bash
ansible-playbook playbooks/fastl4_profile_get_example.yml
```

### 50. 添加 TCP 代理模板示例

```bash
ansible-playbook playbooks/fastl4_profile_add_example.yml
```

### 51. 编辑 TCP 代理模板示例

```bash
ansible-playbook playbooks/fastl4_profile_edit_example.yml
```

### 52. 删除 TCP 代理模板示例

```bash
ansible-playbook playbooks/fastl4_profile_delete_example.yml
```

### 53. TCP 模板列表示例

```bash
ansible-playbook playbooks/tcp_profile_list_example.yml
```

### 54. 获取 TCP 模板详情示例

```bash
ansible-playbook playbooks/tcp_profile_get_example.yml
```

### 55. 添加 TCP 模板示例

```bash
ansible-playbook playbooks/tcp_profile_add_example.yml
```

### 56. 编辑 TCP 模板示例

```bash
ansible-playbook playbooks/tcp_profile_edit_example.yml
```

### 57. 删除 TCP 模板示例

```bash
ansible-playbook playbooks/tcp_profile_delete_example.yml
```

### 58. UDP 模板列表示例

```bash
ansible-playbook playbooks/udp_profile_list_example.yml
```

### 59. 获取 UDP 模板详情示例

```bash
ansible-playbook playbooks/udp_profile_get_example.yml
```

### 60. 添加 UDP 模板示例

```bash
ansible-playbook playbooks/udp_profile_add_example.yml
```

### 61. 编辑 UDP 模板示例

```bash
ansible-playbook playbooks/udp_profile_edit_example.yml
```

### 62. 删除 UDP 模板示例

```bash
ansible-playbook playbooks/udp_profile_delete_example.yml
```

### 63. HTTP 模板列表示例

```bash
ansible-playbook playbooks/http_profile_list_example.yml
```

### 64. 获取 HTTP 模板详情示例

```bash
ansible-playbook playbooks/http_profile_get_example.yml
```

### 65. 添加 HTTP 模板示例

```bash
ansible-playbook playbooks/http_profile_add_example.yml
```

### 66. 编辑 HTTP 模板示例

```bash
ansible-playbook playbooks/http_profile_edit_example.yml
```

### 67. 删除 HTTP 模板示例

```bash
ansible-playbook playbooks/http_profile_delete_example.yml
```

### 68. RTSP 模板列表示例

```bash
ansible-playbook playbooks/rtsp_profile_list_example.yml
```

### 69. 获取 RTSP 模板详情示例

```bash
ansible-playbook playbooks/rtsp_profile_get_example.yml
```

### 70. 添加 RTSP 模板示例

```bash
ansible-playbook playbooks/rtsp_profile_add_example.yml
```

### 71. 编辑 RTSP 模板示例

```bash
ansible-playbook playbooks/rtsp_profile_edit_example.yml
```

### 72. 删除 RTSP 模板示例

```bash
ansible-playbook playbooks/rtsp_profile_delete_example.yml
```

### 73. FTP 模板列表示例

```bash
ansible-playbook playbooks/ftp_profile_list_example.yml
```

### 74. 获取 FTP 模板详情示例

```bash
ansible-playbook playbooks/ftp_profile_get_example.yml
```

### 75. 添加 FTP 模板示例

```bash
ansible-playbook playbooks/ftp_profile_add_example.yml
```

### 76. 编辑 FTP 模板示例

```bash
ansible-playbook playbooks/ftp_profile_edit_example.yml
```

### 77. 删除 FTP 模板示例

```bash
ansible-playbook playbooks/ftp_profile_delete_example.yml
```

### 78. 请求日志模板列表示例

```bash
ansible-playbook playbooks/request_log_profile_list_example.yml
```

### 79. 获取请求日志模板详情示例

```bash
ansible-playbook playbooks/request_log_profile_get_example.yml
```

### 80. 添加请求日志模板示例

```bash
ansible-playbook playbooks/request_log_profile_add_example.yml
```

### 81. 编辑请求日志模板示例

```bash
ansible-playbook playbooks/request_log_profile_edit_example.yml
```

### 82. 删除请求日志模板示例

```bash
ansible-playbook playbooks/request_log_profile_delete_example.yml
```

### 83. 虚拟服务模板列表示例

```bash
ansible-playbook playbooks/vs_profile_list_example.yml
```

### 84. 获取虚拟服务模板详情示例

```bash
ansible-playbook playbooks/vs_profile_get_example.yml
```

### 85. 添加虚拟服务模板示例

```bash
ansible-playbook playbooks/vs_profile_add_example.yml
```

### 86. 编辑虚拟服务模板示例

```bash
ansible-playbook playbooks/vs_profile_edit_example.yml
```

### 87. 删除虚拟服务模板示例

```bash
ansible-playbook playbooks/vs_profile_delete_example.yml
```

### 88. NAT 日志模板列表示例

```bash
ansible-playbook playbooks/natlog_profile_list_example.yml
```

### 89. 获取 NAT 日志模板详情示例

```bash
ansible-playbook playbooks/natlog_profile_get_example.yml
```

### 90. 添加 NAT 日志模板示例

```bash
ansible-playbook playbooks/natlog_profile_add_example.yml
```

### 91. 编辑 NAT 日志模板示例

```bash
ansible-playbook playbooks/natlog_profile_edit_example.yml
```

### 92. 删除 NAT 日志模板示例

```bash
ansible-playbook playbooks/natlog_profile_delete_example.yml
```

### 93. DNS 日志模板列表示例

```bash
ansible-playbook playbooks/dnslog_profile_list_example.yml
```

### 94. 获取 DNS 日志模板详情示例

```bash
ansible-playbook playbooks/dnslog_profile_get_example.yml
```

### 95. 添加 DNS 日志模板示例

```bash
ansible-playbook playbooks/dnslog_profile_add_example.yml
```

### 96. 编辑 DNS 日志模板示例

```bash
ansible-playbook playbooks/dnslog_profile_edit_example.yml
```

### 97. 删除 DNS 日志模板示例

```bash
ansible-playbook playbooks/dnslog_profile_delete_example.yml
```

### 98. SSL 连接保持模板列表示例

```bash
ansible-playbook playbooks/sslid_profile_list_example.yml
```

### 99. 获取 SSL 连接保持模板详情示例

```bash
ansible-playbook playbooks/sslid_profile_get_example.yml
```

### 100. 添加 SSL 连接保持模板示例

```bash
ansible-playbook playbooks/sslid_profile_add_example.yml
```

### 101. 编辑 SSL 连接保持模板示例

```bash
ansible-playbook playbooks/sslid_profile_edit_example.yml
```

### 102. 删除 SSL 连接保持模板示例

```bash
ansible-playbook playbooks/sslid_profile_delete_example.yml
```

### 103. 服务端 SSL 卸载模板列表示例

```bash
ansible-playbook playbooks/sslserver_profile_list_example.yml
```

### 104. 获取服务端 SSL 卸载模板详情示例

```bash
ansible-playbook playbooks/sslserver_profile_get_example.yml
```

### 105. 添加服务端 SSL 卸载模板示例

```bash
ansible-playbook playbooks/sslserver_profile_add_example.yml
```

### 106. 编辑服务端 SSL 卸载模板示例

```bash
ansible-playbook playbooks/sslserver_profile_edit_example.yml
```

### 107. 删除服务端 SSL 卸载模板示例

```bash
ansible-playbook playbooks/sslserver_profile_delete_example.yml
```

### 108. 客户端 SSL 卸载模板列表示例

```bash
ansible-playbook playbooks/sslclient_profile_list_example.yml
```

### 109. 获取客户端 SSL 卸载模板详情示例

```bash
ansible-playbook playbooks/sslclient_profile_get_example.yml
```

### 110. 添加客户端 SSL 卸载模板示例

```bash
ansible-playbook playbooks/sslclient_profile_add_example.yml
```

### 111. 编辑客户端 SSL 卸载模板示例

```bash
ansible-playbook playbooks/sslclient_profile_edit_example.yml
```

### 112. 删除客户端 SSL 卸载模板示例

```bash
ansible-playbook playbooks/sslclient_profile_delete_example.yml
```

### 113. 规则表列表示例

```bash
ansible-playbook playbooks/ruletable_list_example.yml
```

### 114. 获取规则表详情示例

```bash
ansible-playbook playbooks/ruletable_get_example.yml
```

### 115. 添加规则表示例

```bash
ansible-playbook playbooks/ruletable_add_example.yml
```

### 116. 编辑规则表示例

```bash
ansible-playbook playbooks/ruletable_edit_example.yml
```

### 117. 删除规则表示例

```bash
ansible-playbook playbooks/ruletable_delete_example.yml
```

### 118. 添加规则表条目示例

```bash
ansible-playbook playbooks/ruletable_add_entry_example.yml
```

### 119. 策略模板列表示例

```bash
ansible-playbook playbooks/policy_list_example.yml
```

### 120. 获取策略模板详情示例

```bash
ansible-playbook playbooks/policy_get_example.yml
```

### 121. 添加策略模板示例

```bash
ansible-playbook playbooks/policy_add_example.yml
```

### 122. 编辑策略模板示例

```bash
ansible-playbook playbooks/policy_edit_example.yml
```

### 123. 删除策略模板示例

```bash
ansible-playbook playbooks/policy_delete_example.yml
```

### 124. WAF 模板列表示例

```bash
ansible-playbook playbooks/waf_profile_list_example.yml
```

### 125. 获取 WAF 模板详情示例

```bash
ansible-playbook playbooks/waf_profile_get_example.yml
```

### 126. 添加 WAF 模板示例

```bash
ansible-playbook playbooks/waf_profile_add_example.yml
```

### 127. 编辑 WAF 模板示例

```bash
ansible-playbook playbooks/waf_profile_edit_example.yml
```

### 128. 删除 WAF 模板示例

```bash
ansible-playbook playbooks/waf_profile_delete_example.yml
```

### 129. 测试指南

详细测试说明请参考 [TEST_GUIDE.md](TEST_GUIDE.md) 文件。

## 打包和分发

此项目可以打包为 Ansible 集合，便于分发和安装。

### 打包方法

#### Linux/macOS 系统：

```bash
./build_collection.sh
```

#### Windows 系统：

```cmd
build_collection.bat
```

这将创建一个名为 `horizon-modules-1.0.0.tar.gz` 的集合包。

### 安装方法

1. 使用 ansible-galaxy 安装：

```bash
ansible-galaxy collection install horizon-modules-1.0.0.tar.gz
```

2. 或者直接从 Galaxy 安装（如果已发布）：

```bash
ansible-galaxy collection install horizon.modules.horizon_modules
```

### 使用打包后的模块

安装集合后，可以在 playbook 中使用完整命名空间引用模块：

```yaml
- name: 添加节点示例
  horizon.modules.horizon_modules.adc_slb_node:
    ip: "192.168.1.100"
    authkey: "{{ login_result.authkey }}"
    action: "add_node"
    name: "test_node"
    addr: "10.0.0.1"
    status: 1
  register: result
```

详细信息请参考 `PACKAGING.md` 文件。

### 新环境部署

在新环境中部署和运行请参考 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) 文件。

为方便使用，我们还提供了以下工具：

- 环境变量设置脚本：
  - 基础版: [setup_ansible_env.sh](setup_ansible_env.sh) (Linux/macOS), [setup_ansible_env.bat](setup_ansible_env.bat) (Windows)
  - 增强版: [enhanced_setup_ansible_env.sh](enhanced_setup_ansible_env.sh) (Linux/macOS), [enhanced_setup_ansible_env.bat](enhanced_setup_ansible_env.bat) (Windows)
- 环境诊断工具：
  - Linux/macOS: [diagnose_ansible_env.sh](diagnose_ansible_env.sh)
  - Windows: [diagnose_ansible_env.bat](diagnose_ansible_env.bat)

### 参数优化

所有模块均已优化参数处理逻辑，确保只发送 YAML 中明确指定的参数。详细说明请参考 [PARAMETER_OPTIMIZATION.md](PARAMETER_OPTIMIZATION.md)。

## 注意事项

1. 所有操作前请确保已正确配置 ADC 设备的 IP 地址和认证信息
2. 删除资源时请遵循依赖关系，先删除被依赖的资源
3. 建议在测试环境中验证所有操作后再在生产环境中使用
