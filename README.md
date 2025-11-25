# ADC Ansible自动化管理项目

## 项目概述
本项目提供了一套完整的Ansible模块和Playbook，用于自动化管理ADC设备。通过这些模块，可以实现对ADC设备的节点、服务池、虚拟地址、虚拟服务和健康检查等资源的增删改查操作。

## 模块列表

### adc_login模块
- **功能**：登录ADC设备并获取authkey
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `username`：用户名（必需）
  - `password`：密码（必需）

### adc_logout模块
- **功能**：登出ADC设备，使authkey失效
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `authkey`：登录时获取的认证密钥（必需）

### adc_slb_node模块
- **功能**：管理ADC节点
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `authkey`：登录时获取的认证密钥（必需）
  - `action`：操作类型，可选值：`list_nodes`、`get_node`、`add_node`、`edit_node`、`delete_node`、`add_node_port`、`edit_node_port`、`delete_node_port`（必需）
  - `name`：节点名称（添加/编辑/删除节点时必需）
  - `host`：节点主机地址（添加节点时必需）
  - `weight`：节点权重（可选，默认为1）
  - `healthcheck`：健康检查名称（可选）
  - `status`：节点状态，1为启用，0为禁用（可选，默认为1）
  - `conn_limit`：连接限制（可选，默认为0）
  - `ports`：节点端口列表（添加节点时可选）
  - `port_port_number`：端口号（添加/编辑/删除节点端口时必需）
  - `port_protocol`：端口协议（添加/编辑/删除节点端口时必需）

### adc_slb_pool模块
- **功能**：管理ADC服务池
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `authkey`：登录时获取的认证密钥（必需）
  - `action`：操作类型，可选值：`list_pools`、`get_pool`、`add_pool`、`edit_pool`、`delete_pool`、`add_pool_node`、`edit_pool_node`、`delete_pool_node`（必需）
  - `name`：服务池名称（添加/编辑/删除服务池时必需）
  - `lb_method`：负载均衡方法（可选，默认为0）
  - `min_active_member`：最小活跃成员数（可选，默认为1）
  - `conn_limit`：连接限制（可选，默认为0）
  - `status`：服务池状态，1为启用，0为禁用（可选，默认为1）
  - `pool_name`：服务池名称（添加/编辑/删除服务池节点时必需）
  - `node`：节点名称（添加/编辑/删除服务池节点时必需）
  - `port`：端口号（添加/编辑/删除服务池节点时必需）
  - `protocol`：协议类型（添加/编辑/删除服务池节点时必需）

### adc_slb_va模块
- **功能**：管理ADC虚拟地址
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `authkey`：登录时获取的认证密钥（必需）
  - `action`：操作类型，可选值：`list_vas`、`get_va`、`add_va`、`edit_va`、`delete_va`、`list_va_stats`、`get_va_stat`（必需）
  - `name`：虚拟地址名称（添加/编辑/删除虚拟地址时必需）
  - `ip_address`：IP地址（添加虚拟地址时必需）
  - `status`：虚拟地址状态，1为启用，0为禁用（可选，默认为1）
  - `netmask`：子网掩码（可选）
  - `gateway`：网关（可选）
  - `vlan`：VLAN ID（可选）
  - `interface`：接口名称（可选）

### adc_slb_va_vs模块
- **功能**：管理ADC虚拟服务
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `authkey`：登录时获取的认证密钥（必需）
  - `action`：操作类型，可选值：`add_vs`、`edit_vs`、`delete_vs`、`get_vs`（必需）
  - `va_name`：虚拟地址名称（必需）
  - `name`：虚拟服务名称（必需）
  - `protocol`：协议类型（必需）
  - `port`：端口号（必需）
  - `pool`：服务池名称（可选）
  - `status`：虚拟服务状态，1为启用，0为禁用（可选，默认为1）

### adc_slb_healthcheck模块
- **功能**：管理ADC健康检查
- **参数**：
  - `ip`：ADC设备IP地址（必需）
  - `authkey`：登录时获取的认证密钥（必需）
  - `action`：操作类型，可选值：`list_healthchecks`、`get_healthcheck`、`add_healthcheck`、`edit_healthcheck`、`delete_healthcheck`（必需）
  - `name`：健康检查名称（添加/编辑/删除/获取详情时必需）
  - `hc_type`：健康检查类型，可选值：`icmp`、`http`、`https`、`tcp`、`udp`、`combo`、`arp`、`database`、`dns`、`ftp`、`imap`、`ldap`、`ntp`、`pop3`、`radius`、`rtsp`、`sip`、`smtp`、`snmp`（添加时可选，默认为icmp）
  - `retry`：重试次数（可选，默认为3）
  - `interval`：间隔时间，单位秒（可选，默认为5）
  - `timeout`：超时时间，单位秒（可选，默认为5）
  - `description`：描述（可选）
  - `auto_disable`：自动禁用，0为禁用，1为启用（可选，默认为0）
  - `alias_ipv4_src`：源地址IPv4（可选）
  - `alias_ipv6_src`：源地址IPv6（可选）
  - `interface`：源接口（可选）
  - `alias_ipv4`：IPv4地址别名（可选）
  - `alias_ipv6`：IPv6地址别名（可选）
  - `alias_port`：端口别名（可选）
  - `port`：端口（可选）
  - `up_check_cnt`：检测对象up前最少检测成功的个数（可选，默认为1）
  - `wait_all_retry`：等待所有的retry尝试次数都失败了才会将检测对象标记为down，0为禁用，1为启用（可选，默认为0）
  - `http_version`：HTTP版本，可选值：`HTTP 0.9`、`HTTP 1.0`、`HTTP 1.1`（可选）
  - `mode`：透明模式，仅ICMP类型使用（可选）
  - `icmp_alias_addr`：透明模式下健康检查的目的地址，仅ICMP类型使用（可选）
  - `host`：HTTP头部host字段，仅HTTP/HTTPS类型使用（可选）
  - `url`：请求方法和URL，仅HTTP/HTTPS类型使用（可选）
  - `post_data`：发送body，当url中方法为POST时有效，仅HTTP/HTTPS类型使用（可选）
  - `post_file`：发送body文件名，当url中方法为POST时有效，仅HTTP/HTTPS类型使用（可选）
  - `username`：认证用户名，仅HTTP/HTTPS类型使用（可选）
  - `password`：认证密码，仅HTTP/HTTPS类型使用（可选）
  - `code`：HTTP返回码，仅HTTP/HTTPS类型使用（可选）
  - `pattern`：接收字符串，仅HTTP/HTTPS类型使用（可选）
  - `pattern_disable_str`：接收禁用字符串，仅HTTP/HTTPS类型使用（可选）
  - `server_fail_code`：进入维护模式的响应码，仅HTTP/HTTPS类型使用（可选）
  - `trans_mode`：透明模式开关，仅HTTP/HTTPS类型使用（可选）
  - `sslver`：SSL版本，仅HTTPS类型使用（可选）
  - `combo`：组合健康检查表达式，仅Combo类型使用（可选）

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

### 8. 服务池列表示例

```bash
ansible-playbook playbooks/pool_list_example.yml
```

### 9. 服务池添加示例

```bash
ansible-playbook playbooks/pool_add_example.yml
```

### 10. 服务池获取详情示例

```bash
ansible-playbook playbooks/pool_get_example.yml
```

### 11. 服务池编辑示例

```bash
ansible-playbook playbooks/pool_edit_example.yml
```

### 12. 服务池删除示例

```bash
ansible-playbook playbooks/pool_delete_example.yml
```

### 13. 虚拟地址列表示例

```bash
ansible-playbook playbooks/va_list_example.yml
```

### 14. 获取虚拟地址详情示例

```bash
ansible-playbook playbooks/va_get_example.yml
```

### 15. 添加IPv4类型虚拟地址示例

```bash
ansible-playbook playbooks/va_add_ipv4_example.yml
```

### 16. 添加子网类型虚拟地址示例

```bash
ansible-playbook playbooks/va_add_subnet_example.yml
```

### 17. 添加IPv4 ACL类型虚拟地址示例

```bash
ansible-playbook playbooks/va_add_acl_ipv4_example.yml
```

### 18. 添加IPv6 ACL类型虚拟地址示例

```bash
ansible-playbook playbooks/va_add_acl_ipv6_example.yml
```

### 19. 编辑虚拟地址示例

```bash
ansible-playbook playbooks/va_edit_example.yml
```

### 20. 删除虚拟地址示例

```bash
ansible-playbook playbooks/va_delete_example.yml
```

### 21. 虚拟地址状态列表示例

```bash
ansible-playbook playbooks/va_stat_list_example.yml
```

### 22. 获取虚拟地址状态详情示例

```bash
ansible-playbook playbooks/va_stat_get_example.yml
```

### 23. 添加DNS类型虚拟服务示例

```bash
ansible-playbook playbooks/vs_add_dns_example.yml
```

### 24. 添加FTP类型虚拟服务示例

```bash
ansible-playbook playbooks/vs_add_ftp_example.yml
```

### 25. 添加HTTP普通类型虚拟服务示例

```bash
ansible-playbook playbooks/vs_add_http_example.yml
```

### 26. 添加HTTPS类型虚拟服务示例

```bash
ansible-playbook playbooks/vs_add_https_example.yml
```

### 27. 添加TCP类型虚拟服务示例

```bash
ansible-playbook playbooks/vs_add_tcp_example.yml
```

### 28. 编辑虚拟服务示例

```bash
ansible-playbook playbooks/vs_edit_example.yml
```

### 29. 删除虚拟服务示例

```bash
ansible-playbook playbooks/vs_delete_example.yml
```

### 30. 获取虚拟服务详情示例

```bash
ansible-playbook playbooks/vs_get_example.yml
```

### 31. 健康检查列表示例

```bash
ansible-playbook playbooks/healthcheck_list_example.yml
```

### 32. 获取健康检查详情示例

```bash
ansible-playbook playbooks/healthcheck_get_example.yml
```

### 33. 添加ICMP健康检查示例

```bash
ansible-playbook playbooks/healthcheck_add_icmp_example.yml
```

### 34. 添加HTTP健康检查示例

```bash
ansible-playbook playbooks/healthcheck_add_http_example.yml
```

### 35. 添加HTTPS健康检查示例

```bash
ansible-playbook playbooks/healthcheck_add_https_example.yml
```

### 36. 添加TCP健康检查示例

```bash
ansible-playbook playbooks/healthcheck_add_tcp_example.yml
```

### 37. 添加Combo健康检查示例

```bash
ansible-playbook playbooks/healthcheck_add_combo_example.yml
```

### 38. 编辑健康检查示例

```bash
ansible-playbook playbooks/healthcheck_edit_example.yml
```

### 39. 删除健康检查示例

```bash
ansible-playbook playbooks/healthcheck_delete_example.yml
```

### 40. 完整测试场景 - HTTP

```bash
ansible-playbook playbooks/complete_test_http_scenario.yml
```

### 41. 完整测试场景 - HTTPS

```bash
ansible-playbook playbooks/complete_test_https_scenario.yml
```

### 42. 节点创建测试

```bash
ansible-playbook playbooks/test_node_creation.yml
```

## 注意事项
1. 所有操作前请确保已正确配置ADC设备的IP地址和认证信息
2. 删除资源时请遵循依赖关系，先删除被依赖的资源
3. 建议在测试环境中验证所有操作后再在生产环境中使用