# ADC 网络管理 Ansible 模块

本文档介绍了为 ADC 设备网络管理功能开发的 Ansible 模块和示例 playbook。

## 已创建的模块

### 1. VLAN 管理模块

- **模块文件**: `library/adc_network_vlan.py`
- **功能**: VLAN 的增删改查操作
- **支持的操作**:
  - `list_vlans`: 获取 VLAN 列表
  - `get_vlan`: 获取 VLAN 详情
  - `add_vlan`: 添加 VLAN
  - `edit_vlan`: 编辑 VLAN
  - `delete_vlan`: 删除 VLAN

### 2. TRUNK 管理模块

- **模块文件**: `library/adc_network_trunk.py`
- **功能**: TRUNK 的增删改查操作
- **支持的操作**:
  - `list_trunks`: 获取 TRUNK 列表
  - `get_trunk`: 获取 TRUNK 详情
  - `add_trunk`: 添加 TRUNK
  - `edit_trunk`: 编辑 TRUNK
  - `delete_trunk`: 删除 TRUNK

### 3. IPv4 标准访问列表模块

- **模块文件**: `library/adc_network_acl_ipv4_std.py`
- **功能**: IPv4 标准访问列表的管理操作
- **支持的操作**:
  - `list_acls`: 获取 IPv4 标准访问列表
  - `get_acl`: 获取 IPv4 标准访问列表详情
  - `add_acl_item`: 添加 IPv4 标准访问列表条目
  - `edit_acl_item`: 编辑 IPv4 标准访问列表条目
  - `delete_acl_item`: 删除 IPv4 标准访问列表条目
  - `set_acl_description`: 设置 IPv4 标准访问列表描述

### 4. IPv4 扩展访问列表模块

- **模块文件**: `library/adc_network_acl_ipv4_ext.py`
- **功能**: IPv4 扩展访问列表的管理操作
- **支持的操作**:
  - `list_acls`: 获取 IPv4 扩展访问列表
  - `get_acl`: 获取 IPv4 扩展访问列表详情
  - `add_acl_item`: 添加 IPv4 扩展访问列表条目
  - `edit_acl_item`: 编辑 IPv4 扩展访问列表条目
  - `delete_acl_item`: 删除 IPv4 扩展访问列表条目
  - `set_acl_description`: 设置 IPv4 扩展访问列表描述

### 5. IPv6 访问列表模块

- **模块文件**: `library/adc_network_acl_ipv6.py`
- **功能**: IPv6 访问列表的管理操作
- **支持的操作**:
  - `list_acls`: 获取 IPv6 访问列表
  - `get_acl`: 获取 IPv6 访问列表详情
  - `add_acl_item`: 添加 IPv6 访问列表条目
  - `edit_acl_item`: 编辑 IPv6 访问列表条目
  - `delete_acl_item`: 删除 IPv6 访问列表条目
  - `set_acl_description`: 设置 IPv6 访问列表描述

### 6. 端口列表模板模块

- **模块文件**: `library/adc_network_port_list_profile.py`
- **功能**: 端口列表模板的管理操作
- **支持的操作**:
  - `list_profiles`: 获取端口列表模板
  - `get_profile`: 获取端口列表模板详情
  - `add_profile`: 添加端口列表模板
  - `add_profile_item`: 添加端口列表模板条目
  - `edit_profile`: 编辑端口列表模板
  - `delete_profile`: 删除端口列表模板
  - `delete_profile_item`: 删除端口列表模板条目

### 7. NAT 地址池模块

- **模块文件**: `library/adc_network_nat_pool.py`
- **功能**: NAT 地址池的管理操作
- **支持的操作**:
  - `list_pools`: 获取 NAT 地址池列表
  - `get_pool`: 获取 NAT 地址池详情
  - `add_pool`: 添加 NAT 地址池
  - `edit_pool`: 编辑 NAT 地址池
  - `delete_pool`: 删除 NAT 地址池

### 8. 网络 NAT 模块

- **模块文件**: `library/adc_network_nat_network.py`
- **功能**: 网络 NAT 的管理操作
- **支持的操作**:
  - `list_networks`: 获取网络 NAT 列表
  - `get_network`: 获取网络 NAT 详情
  - `add_network`: 添加网络 NAT
  - `edit_network`: 编辑网络 NAT
  - `delete_network`: 删除网络 NAT

### 9. NAT 映射模块

- **模块文件**: `library/adc_network_nat_map.py`
- **功能**: NAT 映射的管理操作
- **支持的操作**:
  - `list_maps`: 获取 NAT 映射列表
  - `add_map`: 添加 NAT 映射
  - `delete_map`: 删除 NAT 映射
  - `list_ipv6_maps`: 获取 IPv6 NAT 映射列表
  - `add_ipv6_map`: 添加 IPv6 NAT 映射
  - `delete_ipv6_map`: 删除 IPv6 NAT 映射

### 10. NAT 策略模块

- **模块文件**: `library/adc_network_nat_policy.py`
- **功能**: NAT 策略的管理操作
- **支持的操作**:
  - `list_policies`: 获取 NAT 策略列表
  - `get_policy`: 获取 NAT 策略详情
  - `add_policy`: 添加 NAT 策略
  - `edit_policy`: 编辑 NAT 策略
  - `delete_policy`: 删除 NAT 策略

### 11. IPv4 静态路由模块

- **模块文件**: `library/adc_network_route_static_ipv4.py`
- **功能**: IPv4 静态路由的管理操作
- **支持的操作**:
  - `list_routes`: 获取 IPv4 静态路由列表
  - `get_route`: 获取 IPv4 静态路由详情
  - `add_route`: 添加 IPv4 静态路由
  - `edit_route`: 编辑 IPv4 静态路由
  - `delete_route`: 删除 IPv4 静态路由

### 12. IPv6 静态路由模块

- **模块文件**: `library/adc_network_route_static_ipv6.py`
- **功能**: IPv6 静态路由的管理操作
- **支持的操作**:
  - `list_routes`: 获取 IPv6 静态路由列表
  - `get_route`: 获取 IPv6 静态路由详情
  - `add_route`: 添加 IPv6 静态路由
  - `edit_route`: 编辑 IPv6 静态路由
  - `delete_route`: 删除 IPv6 静态路由

### 13. 网络模式管理模块

- **模块文件**: `library/adc_network_mode.py`
- **功能**: 网络模式配置的获取和设置
- **支持的操作**:
  - `get_network_mode`: 获取网络模式配置
  - `set_network_mode`: 设置网络模式配置

### 14. NAT 地址池统计信息模块

- **模块文件**: `library/adc_network_nat_pool_stats.py`
- **功能**: NAT 地址池统计信息的获取和清除
- **支持的操作**:
  - `list_stats`: 获取 NAT 地址池统计信息列表
  - `clear_stats`: 清除 NAT 地址池统计信息

### 15. NAT 地址池组模块

- **模块文件**: `library/adc_network_nat_pool_group.py`
- **功能**: NAT 地址池组的管理操作
- **支持的操作**:
  - `list_groups`: 获取 NAT 地址池组列表
  - `get_group`: 获取 NAT 地址池组详情
  - `add_group`: 添加 NAT 地址池组
  - `edit_group`: 编辑 NAT 地址池组
  - `delete_group`: 删除 NAT 地址池组

### 16. 静态 NAT 模块

- **模块文件**: `library/adc_network_nat_static.py`
- **功能**: 静态 NAT 的管理操作
- **支持的操作**:
  - `list_statics`: 获取静态 NAT 列表
  - `get_static`: 获取静态 NAT 详情
  - `add_static`: 添加静态 NAT
  - `edit_static`: 编辑静态 NAT
  - `delete_static`: 删除静态 NAT

### 17. NAT 超时配置模块

- **模块文件**: `library/adc_network_nat_timeout.py`
- **功能**: NAT 超时配置的获取和设置
- **支持的操作**:
  - `get_timeout`: 获取 NAT 超时配置
  - `set_timeout`: 设置 NAT 超时配置

### 18. NAT 全局配置模块

- **模块文件**: `library/adc_network_nat_global.py`
- **功能**: NAT 全局配置的获取和设置
- **支持的操作**:
  - `get_global`: 获取 NAT 全局配置
  - `set_global`: 设置 NAT 全局配置

### 19. IPv4 静态管理路由模块

- **模块文件**: `library/adc_network_route_static_mgmt_ipv4.py`
- **功能**: IPv4 静态管理路由的管理操作
- **支持的操作**:
  - `list_routes`: 获取 IPv4 静态管理路由列表
  - `get_route`: 获取 IPv4 静态管理路由详情
  - `add_route`: 添加 IPv4 静态管理路由
  - `edit_route`: 编辑 IPv4 静态管理路由
  - `delete_route`: 删除 IPv4 静态管理路由

### 20. IPv6 静态管理路由模块

- **模块文件**: `library/adc_network_route_static_mgmt_ipv6.py`
- **功能**: IPv6 静态管理路由的管理操作
- **支持的操作**:
  - `list_routes`: 获取 IPv6 静态管理路由列表
  - `get_route`: 获取 IPv6 静态管理路由详情
  - `add_route`: 添加 IPv6 静态管理路由
  - `edit_route`: 编辑 IPv6 静态管理路由
  - `delete_route`: 删除 IPv6 静态管理路由

### 21. IPv4 静态控制路由模块

- **模块文件**: `library/adc_network_route_static_ctrl_ipv4.py`
- **功能**: IPv4 静态控制路由的管理操作
- **支持的操作**:
  - `list_routes`: 获取 IPv4 静态控制路由列表
  - `get_route`: 获取 IPv4 静态控制路由详情
  - `add_route`: 添加 IPv4 静态控制路由
  - `edit_route`: 编辑 IPv4 静态控制路由
  - `delete_route`: 删除 IPv4 静态控制路由

### 22. IPv6 静态控制路由模块

- **模块文件**: `library/adc_network_route_static_ctrl_ipv6.py`
- **功能**: IPv6 静态控制路由的管理操作
- **支持的操作**:
  - `list_routes`: 获取 IPv6 静态控制路由列表
  - `get_route`: 获取 IPv6 静态控制路由详情
  - `add_route`: 添加 IPv6 静态控制路由
  - `edit_route`: 编辑 IPv6 静态控制路由
  - `delete_route`: 删除 IPv6 静态控制路由

### 23. OSPF 模块

- **模块文件**: `library/adc_network_ospf.py`
- **功能**: OSPF 的管理操作
- **支持的操作**:
  - `list_networks`: 获取 OSPF 网络列表
  - `add_network`: 添加 OSPF 网络
  - `delete_network`: 删除 OSPF 网络
  - `get_status`: 获取 OSPF 状态
  - `set_status`: 设置 OSPF 状态

### 24. BGP 模块

- **模块文件**: `library/adc_network_bgp.py`
- **功能**: BGP 的管理操作
- **支持的操作**:
  - `list_networks`: 获取 BGP 网络列表
  - `add_network`: 添加 BGP 网络
  - `delete_network`: 删除 BGP 网络
  - `list_neighbors`: 获取 BGP 邻居列表
  - `add_neighbor`: 添加 BGP 邻居
  - `delete_neighbor`: 删除 BGP 邻居
  - `get_status`: 获取 BGP 状态
  - `set_status`: 设置 BGP 状态

### 25. SYN Cookie 模块

- **模块文件**: `library/adc_network_syn_cookie.py`
- **功能**: SYN Cookie 配置的获取和设置
- **支持的操作**:
  - `get_global_syn_cookie`: 获取全局 SYN Cookie 配置
  - `set_global_syn_cookie`: 设置全局 SYN Cookie 配置
  - `get_vs_syn_cookie`: 获取每虚拟服务 SYN Cookie 配置
  - `set_vs_syn_cookie`: 设置每虚拟服务 SYN Cookie 配置

### 26. 接口管理模块

- **模块文件**: `library/adc_network_interface.py`
- **功能**: 网络接口的管理操作
- **支持的操作**:
  - `get_mgmt_interface`: 获取管理接口配置
  - `set_mgmt_interface`: 设置管理接口配置
  - `list_ethernet_interfaces`: 获取以太网接口列表
  - `get_ethernet_interface`: 获取以太网接口详情
  - `edit_ethernet_interface`: 编辑以太网接口配置
  - `get_ethernet_statistics`: 获取以太网接口统计信息
  - `list_ve_interfaces`: 获取 VE 接口列表
  - `get_ve_interface`: 获取 VE 接口详情
  - `edit_ve_interface`: 编辑 VE 接口配置
  - `list_trunk_interfaces`: 获取 TRUNK 接口列表
  - `get_trunk_interface`: 获取 TRUNK 接口详情
  - `edit_trunk_interface`: 编辑 TRUNK 接口配置

### 27. LLDP 模块

- **模块文件**: `library/adc_network_lldp.py`
- **功能**: LLDP 协议的管理操作
- **支持的操作**:
  - `get_lldp_config`: 获取 LLDP 配置
  - `set_lldp_config`: 设置 LLDP 配置
  - `get_lldp_neighbors`: 获取 LLDP 邻居信息

### 28. ARP 模块

- **模块文件**: `library/adc_network_arp.py`
- **功能**: ARP 表项的管理操作
- **支持的操作**:
  - `list_ipv4_entries`: 获取 IPv4 ARP 条目列表
  - `get_ipv4_entry`: 获取 IPv4 ARP 条目详情
  - `add_ipv4_entry`: 添加 IPv4 ARP 条目
  - `edit_ipv4_entry`: 编辑 IPv4 ARP 条目
  - `delete_ipv4_entry`: 删除 IPv4 ARP 条目
  - `get_ipv4_statistics`: 获取 IPv4 ARP 统计信息
  - `clear_ipv4_statistics`: 清除 IPv4 ARP 统计信息
  - `list_ipv6_entries`: 获取 IPv6 ARP 条目列表
  - `get_ipv6_entry`: 获取 IPv6 ARP 条目详情
  - `add_ipv6_entry`: 添加 IPv6 ARP 条目
  - `edit_ipv6_entry`: 编辑 IPv6 ARP 条目
  - `delete_ipv6_entry`: 删除 IPv6 ARP 条目
  - `get_ipv6_statistics`: 获取 IPv6 ARP 统计信息
  - `clear_ipv6_statistics`: 清除 IPv6 ARP 统计信息

### 29. DDoS 防护模块

- **模块文件**: `library/adc_network_ddos.py`
- **功能**: DDoS 防护配置的获取和设置
- **支持的操作**:
  - `get_ddos_config`: 获取 DDoS 防护配置
  - `set_ddos_config`: 设置 DDoS 防护配置

### 30. 流量控制(TC)模块

- **模块文件**: `library/adc_network_tc.py`
- **功能**: 流量控制策略的管理操作
- **支持的操作**:
  - `get_global_tc_config`: 获取全局 TC 配置
  - `set_global_tc_config`: 设置全局 TC 配置
  - `list_tc_entries`: 获取 TC 条目列表
  - `get_tc_entry`: 获取 TC 条目详情
  - `add_tc_entry`: 添加 TC 条目
  - `edit_tc_entry`: 编辑 TC 条目
  - `delete_tc_entry`: 删除 TC 条目
  - `list_tc_rules`: 获取 TC 规则列表
  - `get_tc_rule`: 获取 TC 规则详情
  - `add_tc_rule`: 添加 TC 规则
  - `edit_tc_rule`: 编辑 TC 规则
  - `delete_tc_rule`: 删除 TC 规则

### 31. 系统时间范围模块

- **模块文件**: `library/adc_system_timerange.py`
- **功能**: 系统时间范围的管理操作
- **支持的操作**:
  - `list_timeranges`: 获取时间范围列表
  - `get_timerange`: 获取时间范围详情
  - `add_timerange`: 添加时间范围
  - `edit_timerange`: 编辑时间范围
  - `delete_timerange`: 删除时间范围

## 示例 Playbook

每个模块都配有相应的示例 playbook，位于`playbooks/`目录下：

### VLAN 相关示例

- `vlan_add_example.yml`: 添加 VLAN 示例
- `vlan_list_example.yml`: 获取 VLAN 列表示例
- `vlan_get_example.yml`: 获取 VLAN 详情示例
- `vlan_edit_example.yml`: 编辑 VLAN 示例
- `vlan_delete_example.yml`: 删除 VLAN 示例

### TRUNK 相关示例

- `trunk_add_example.yml`: 添加 TRUNK 示例
- `trunk_list_example.yml`: 获取 TRUNK 列表示例
- `trunk_get_example.yml`: 获取 TRUNK 详情示例
- `trunk_edit_example.yml`: 编辑 TRUNK 示例
- `trunk_delete_example.yml`: 删除 TRUNK 示例

### IPv4 标准访问列表相关示例

- `acl_ipv4_std_list_example.yml`: 获取 IPv4 标准访问列表示例
- `acl_ipv4_std_get_example.yml`: 获取 IPv4 标准访问列表详情示例
- `acl_ipv4_std_add_item_example.yml`: 添加 IPv4 标准访问列表条目示例
- `acl_ipv4_std_edit_item_example.yml`: 编辑 IPv4 标准访问列表条目示例
- `acl_ipv4_std_delete_item_example.yml`: 删除 IPv4 标准访问列表条目示例
- `acl_ipv4_std_set_description_example.yml`: 设置 IPv4 标准访问列表描述示例

### IPv4 扩展访问列表相关示例

- `acl_ipv4_ext_list_example.yml`: 获取 IPv4 扩展访问列表示例
- `acl_ipv4_ext_get_example.yml`: 获取 IPv4 扩展访问列表详情示例
- `acl_ipv4_ext_add_item_example.yml`: 添加 IPv4 扩展访问列表条目示例
- `acl_ipv4_ext_edit_item_example.yml`: 编辑 IPv4 扩展访问列表条目示例
- `acl_ipv4_ext_delete_item_example.yml`: 删除 IPv4 扩展访问列表条目示例
- `acl_ipv4_ext_set_description_example.yml`: 设置 IPv4 扩展访问列表描述示例

### IPv6 访问列表相关示例

- `acl_ipv6_list_example.yml`: 获取 IPv6 访问列表示例
- `acl_ipv6_get_example.yml`: 获取 IPv6 访问列表详情示例
- `acl_ipv6_add_item_example.yml`: 添加 IPv6 访问列表条目示例
- `acl_ipv6_edit_item_example.yml`: 编辑 IPv6 访问列表条目示例
- `acl_ipv6_delete_item_example.yml`: 删除 IPv6 访问列表条目示例
- `acl_ipv6_set_description_example.yml`: 设置 IPv6 访问列表描述示例

### 端口列表模板相关示例

- `port_list_profile_list_example.yml`: 获取端口列表模板示例
- `port_list_profile_get_example.yml`: 获取端口列表模板详情示例
- `port_list_profile_add_example.yml`: 添加端口列表模板示例
- `port_list_profile_add_item_example.yml`: 添加端口列表模板条目示例
- `port_list_profile_edit_example.yml`: 编辑端口列表模板示例
- `port_list_profile_delete_example.yml`: 删除端口列表模板示例
- `port_list_profile_delete_item_example.yml`: 删除端口列表模板条目示例

### NAT 地址池相关示例

- `nat_pool_list_example.yml`: 获取 NAT 地址池列表示例
- `nat_pool_get_example.yml`: 获取 NAT 地址池详情示例
- `nat_pool_add_example.yml`: 添加 NAT 地址池示例
- `nat_pool_edit_example.yml`: 编辑 NAT 地址池示例
- `nat_pool_delete_example.yml`: 删除 NAT 地址池示例

### 网络 NAT 相关示例

- `nat_network_list_example.yml`: 获取网络 NAT 列表示例
- `nat_network_get_example.yml`: 获取网络 NAT 详情示例
- `nat_network_add_example.yml`: 添加网络 NAT 示例
- `nat_network_edit_example.yml`: 编辑网络 NAT 示例
- `nat_network_delete_example.yml`: 删除网络 NAT 示例

### NAT 映射相关示例

- `nat_map_list_example.yml`: 获取 NAT 映射列表示例
- `nat_map_add_example.yml`: 添加 NAT 映射示例
- `nat_map_delete_example.yml`: 删除 NAT 映射示例
- `nat_ipv6_map_list_example.yml`: 获取 IPv6 NAT 映射列表示例
- `nat_ipv6_map_add_example.yml`: 添加 IPv6 NAT 映射示例
- `nat_ipv6_map_delete_example.yml`: 删除 IPv6 NAT 映射示例

### NAT 策略相关示例

- `nat_policy_list_example.yml`: 获取 NAT 策略列表示例
- `nat_policy_get_example.yml`: 获取 NAT 策略详情示例
- `nat_policy_add_example.yml`: 添加 NAT 策略示例
- `nat_policy_edit_example.yml`: 编辑 NAT 策略示例
- `nat_policy_delete_example.yml`: 删除 NAT 策略示例

### IPv4 静态路由相关示例

- `route_static_ipv4_list_example.yml`: 获取 IPv4 静态路由列表示例
- `route_static_ipv4_get_example.yml`: 获取 IPv4 静态路由详情示例
- `route_static_ipv4_add_example.yml`: 添加 IPv4 静态路由示例
- `route_static_ipv4_edit_example.yml`: 编辑 IPv4 静态路由示例
- `route_static_ipv4_delete_example.yml`: 删除 IPv4 静态路由示例

### IPv6 静态路由相关示例

- `route_static_ipv6_list_example.yml`: 获取 IPv6 静态路由列表示例
- `route_static_ipv6_get_example.yml`: 获取 IPv6 静态路由详情示例
- `route_static_ipv6_add_example.yml`: 添加 IPv6 静态路由示例
- `route_static_ipv6_edit_example.yml`: 编辑 IPv6 静态路由示例
- `route_static_ipv6_delete_example.yml`: 删除 IPv6 静态路由示例

### 网络模式相关示例

- `network_mode_get_example.yml`: 获取网络模式配置示例
- `network_mode_set_example.yml`: 设置网络模式配置示例

### NAT 地址池统计信息相关示例

- `nat_pool_stats_list_example.yml`: 获取 NAT 地址池统计信息列表示例
- `nat_pool_stats_clear_example.yml`: 清除 NAT 地址池统计信息示例

### NAT 地址池组相关示例

- `nat_pool_group_list_example.yml`: 获取 NAT 地址池组列表示例
- `nat_pool_group_get_example.yml`: 获取 NAT 地址池组详情示例
- `nat_pool_group_add_example.yml`: 添加 NAT 地址池组示例
- `nat_pool_group_edit_example.yml`: 编辑 NAT 地址池组示例
- `nat_pool_group_delete_example.yml`: 删除 NAT 地址池组示例

### 静态 NAT 相关示例

- `nat_static_list_example.yml`: 获取静态 NAT 列表示例
- `nat_static_get_example.yml`: 获取静态 NAT 详情示例
- `nat_static_add_example.yml`: 添加静态 NAT 示例
- `nat_static_edit_example.yml`: 编辑静态 NAT 示例
- `nat_static_delete_example.yml`: 删除静态 NAT 示例

### NAT 超时配置相关示例

- `nat_timeout_get_example.yml`: 获取 NAT 超时配置示例
- `nat_timeout_set_example.yml`: 设置 NAT 超时配置示例

### NAT 全局配置相关示例

- `nat_global_get_example.yml`: 获取 NAT 全局配置示例
- `nat_global_set_example.yml`: 设置 NAT 全局配置示例

### IPv4 静态管理路由相关示例

- `route_static_mgmt_ipv4_list_example.yml`: 获取 IPv4 静态管理路由列表示例
- `route_static_mgmt_ipv4_get_example.yml`: 获取 IPv4 静态管理路由详情示例
- `route_static_mgmt_ipv4_add_example.yml`: 添加 IPv4 静态管理路由示例
- `route_static_mgmt_ipv4_edit_example.yml`: 编辑 IPv4 静态管理路由示例
- `route_static_mgmt_ipv4_delete_example.yml`: 删除 IPv4 静态管理路由示例

### IPv6 静态管理路由相关示例

- `route_static_mgmt_ipv6_list_example.yml`: 获取 IPv6 静态管理路由列表示例
- `route_static_mgmt_ipv6_get_example.yml`: 获取 IPv6 静态管理路由详情示例
- `route_static_mgmt_ipv6_add_example.yml`: 添加 IPv6 静态管理路由示例
- `route_static_mgmt_ipv6_edit_example.yml`: 编辑 IPv6 静态管理路由示例
- `route_static_mgmt_ipv6_delete_example.yml`: 删除 IPv6 静态管理路由示例

### IPv4 静态控制路由相关示例

- `route_static_ctrl_ipv4_list_example.yml`: 获取 IPv4 静态控制路由列表示例
- `route_static_ctrl_ipv4_get_example.yml`: 获取 IPv4 静态控制路由详情示例
- `route_static_ctrl_ipv4_add_example.yml`: 添加 IPv4 静态控制路由示例
- `route_static_ctrl_ipv4_edit_example.yml`: 编辑 IPv4 静态控制路由示例
- `route_static_ctrl_ipv4_delete_example.yml`: 删除 IPv4 静态控制路由示例

### IPv6 静态控制路由相关示例

- `route_static_ctrl_ipv6_list_example.yml`: 获取 IPv6 静态控制路由列表示例
- `route_static_ctrl_ipv6_get_example.yml`: 获取 IPv6 静态控制路由详情示例
- `route_static_ctrl_ipv6_add_example.yml`: 添加 IPv6 静态控制路由示例
- `route_static_ctrl_ipv6_edit_example.yml`: 编辑 IPv6 静态控制路由示例
- `route_static_ctrl_ipv6_delete_example.yml`: 删除 IPv6 静态控制路由示例

### OSPF 相关示例

- `ospf_network_list_example.yml`: 获取 OSPF 网络列表示例
- `ospf_network_add_example.yml`: 添加 OSPF 网络示例
- `ospf_network_delete_example.yml`: 删除 OSPF 网络示例
- `ospf_status_get_example.yml`: 获取 OSPF 状态示例
- `ospf_status_set_example.yml`: 设置 OSPF 状态示例

### BGP 相关示例

- `bgp_network_list_example.yml`: 获取 BGP 网络列表示例
- `bgp_network_add_example.yml`: 添加 BGP 网络示例
- `bgp_network_delete_example.yml`: 删除 BGP 网络示例
- `bgp_neighbor_list_example.yml`: 获取 BGP 邻居列表示例
- `bgp_neighbor_add_example.yml`: 添加 BGP 邻居示例
- `bgp_neighbor_delete_example.yml`: 删除 BGP 邻居示例
- `bgp_status_get_example.yml`: 获取 BGP 状态示例
- `bgp_status_set_example.yml`: 设置 BGP 状态示例

### SYN Cookie 相关示例

- `syn_cookie_global_get_example.yml`: 获取全局 SYN Cookie 配置示例
- `syn_cookie_global_set_example.yml`: 设置全局 SYN Cookie 配置示例
- `syn_cookie_vs_get_example.yml`: 获取每虚拟服务 SYN Cookie 配置示例
- `syn_cookie_vs_set_example.yml`: 设置每虚拟服务 SYN Cookie 配置示例

### 接口管理相关示例

- `interface_mgmt_get_example.yml`: 获取管理接口配置示例
- `interface_mgmt_set_example.yml`: 设置管理接口配置示例
- `interface_ethernet_list_example.yml`: 获取以太网接口列表示例
- `interface_ethernet_get_example.yml`: 获取以太网接口详情示例
- `interface_ethernet_edit_example.yml`: 编辑以太网接口配置示例
- `interface_ethernet_statistics_example.yml`: 获取以太网接口统计信息示例
- `interface_ve_list_example.yml`: 获取 VE 接口列表示例
- `interface_ve_get_example.yml`: 获取 VE 接口详情示例
- `interface_ve_edit_example.yml`: 编辑 VE 接口配置示例
- `interface_trunk_list_example.yml`: 获取 TRUNK 接口列表示例
- `interface_trunk_get_example.yml`: 获取 TRUNK 接口详情示例
- `interface_trunk_edit_example.yml`: 编辑 TRUNK 接口配置示例

### LLDP 相关示例

- `lldp_config_get_example.yml`: 获取 LLDP 配置示例
- `lldp_config_set_example.yml`: 设置 LLDP 配置示例
- `lldp_neighbors_get_example.yml`: 获取 LLDP 邻居信息示例

### ARP 相关示例

- `arp_ipv4_list_example.yml`: 获取 IPv4 ARP 条目列表示例
- `arp_ipv4_get_example.yml`: 获取 IPv4 ARP 条目详情示例
- `arp_ipv4_add_example.yml`: 添加 IPv4 ARP 条目示例
- `arp_ipv4_edit_example.yml`: 编辑 IPv4 ARP 条目示例
- `arp_ipv4_delete_example.yml`: 删除 IPv4 ARP 条目示例
- `arp_ipv4_statistics_get_example.yml`: 获取 IPv4 ARP 统计信息示例
- `arp_ipv4_statistics_clear_example.yml`: 清除 IPv4 ARP 统计信息示例
- `arp_ipv6_list_example.yml`: 获取 IPv6 ARP 条目列表示例
- `arp_ipv6_get_example.yml`: 获取 IPv6 ARP 条目详情示例
- `arp_ipv6_add_example.yml`: 添加 IPv6 ARP 条目示例
- `arp_ipv6_edit_example.yml`: 编辑 IPv6 ARP 条目示例
- `arp_ipv6_delete_example.yml`: 删除 IPv6 ARP 条目示例
- `arp_ipv6_statistics_get_example.yml`: 获取 IPv6 ARP 统计信息示例
- `arp_ipv6_statistics_clear_example.yml`: 清除 IPv6 ARP 统计信息示例

### DDoS 防护相关示例

- `ddos_config_get_example.yml`: 获取 DDoS 防护配置示例
- `ddos_config_set_example.yml`: 设置 DDoS 防护配置示例

### 流量控制(TC)相关示例

- `tc_global_config_get_example.yml`: 获取全局 TC 配置示例
- `tc_global_config_set_example.yml`: 设置全局 TC 配置示例
- `tc_entry_list_example.yml`: 获取 TC 条目列表示例
- `tc_entry_get_example.yml`: 获取 TC 条目详情示例
- `tc_entry_add_example.yml`: 添加 TC 条目示例
- `tc_entry_edit_example.yml`: 编辑 TC 条目示例
- `tc_entry_delete_example.yml`: 删除 TC 条目示例
- `tc_rule_list_example.yml`: 获取 TC 规则列表示例
- `tc_rule_get_example.yml`: 获取 TC 规则详情示例
- `tc_rule_add_example.yml`: 添加 TC 规则示例
- `tc_rule_edit_example.yml`: 编辑 TC 规则示例
- `tc_rule_delete_example.yml`: 删除 TC 规则示例

## 使用方法

1. 确保 Ansible 环境已正确配置
2. 将模块文件放置在`library/`目录下
3. 根据需要修改 playbook 中的 IP 地址、用户名和密码等参数
4. 运行 playbook:
   ```bash
   ansible-playbook playbooks/vlan_add_example.yml
   ```

## 注意事项

1. 所有操作前请确保已正确配置 ADC 设备的 IP 地址和认证信息
2. 删除资源时请遵循依赖关系，先删除被依赖的资源
3. 建议在测试环境中验证所有操作后再在生产环境中使用
