# ADC Ansible 模块功能概览

## 目录
1. [网络管理模块](#网络管理模块)
2. [系统管理模块](#系统管理模块)
3. [负载均衡模块](#负载均衡模块)
4. [安全模块](#安全模块)

## 网络管理模块

### VLAN管理 - adc_network_vlan
**功能**: VLAN的增删改查操作
- add_vlan: 添加VLAN
- edit_vlan: 编辑VLAN
- delete_vlan: 删除VLAN
- get_vlan: 获取VLAN详情
- list_vlans: 列出所有VLAN

**示例playbook**: `playbooks/vlan_*.yml`

### Trunk管理 - adc_network_trunk
**功能**: Trunk接口的增删改查操作
- add_trunk: 添加Trunk
- edit_trunk: 编辑Trunk
- delete_trunk: 删除Trunk
- get_trunk: 获取Trunk详情
- list_trunks: 列出所有Trunk

**示例playbook**: `playbooks/trunk_*.yml`

### ACL管理

#### IPv4标准ACL - adc_network_acl_ipv4_std
**功能**: IPv4标准访问控制列表管理
- add_acl_item: 添加ACL条目
- edit_acl_item: 编辑ACL条目
- delete_acl_item: 删除ACL条目
- get_acl: 获取ACL详情
- list_acls: 列出所有ACL

**示例playbook**: `playbooks/acl_ipv4_std_*.yml`

#### IPv4扩展ACL - adc_network_acl_ipv4_ext
**功能**: IPv4扩展访问控制列表管理
- add_acl_item: 添加ACL条目
- edit_acl_item: 编辑ACL条目
- delete_acl_item: 删除ACL条目
- get_acl: 获取ACL详情
- list_acls: 列出所有ACL

**示例playbook**: `playbooks/acl_ipv4_ext_*.yml`

#### IPv6 ACL - adc_network_acl_ipv6
**功能**: IPv6访问控制列表管理
- add_acl_item: 添加ACL条目
- edit_acl_item: 编辑ACL条目
- delete_acl_item: 删除ACL条目
- get_acl: 获取ACL详情
- list_acls: 列出所有ACL

**示例playbook**: `playbooks/acl_ipv6_*.yml`

### 路由管理

#### IPv4静态路由 - adc_network_route_static_ipv4
**功能**: IPv4静态路由管理
- add_route: 添加路由
- edit_route: 编辑路由
- delete_route: 删除路由
- get_route: 获取路由详情
- list_routes: 列出所有路由

**示例playbook**: `playbooks/route_static_ipv4_*.yml`

#### IPv6静态路由 - adc_network_route_static_ipv6
**功能**: IPv6静态路由管理
- add_route: 添加路由
- edit_route: 编辑路由
- delete_route: 删除路由
- get_route: 获取路由详情
- list_routes: 列出所有路由

**示例playbook**: `playbooks/route_static_ipv6_*.yml`

### NAT管理

#### NAT地址池 - adc_network_nat_pool
**功能**: NAT地址池管理
- add_pool: 添加地址池
- edit_pool: 编辑地址池
- delete_pool: 删除地址池
- get_pool: 获取地址池详情
- list_pools: 列出所有地址池

**示例playbook**: `playbooks/nat_pool_*.yml`

#### NAT策略 - adc_network_nat_policy
**功能**: NAT策略管理
- add_policy: 添加策略
- edit_policy: 编辑策略
- delete_policy: 删除策略
- get_policy: 获取策略详情
- list_policies: 列出所有策略

**示例playbook**: `playbooks/nat_policy_*.yml`

## 系统管理模块

### 用户管理 - adc_system_user
**功能**: 系统用户管理
- add_user: 添加用户
- edit_user: 编辑用户
- delete_user: 删除用户
- get_user: 获取用户详情
- list_users: 列出所有用户
- unlock_user: 解锁用户
- change_password: 修改密码

**示例playbook**: `playbooks/system/user/*.yml`

### 日志配置 - adc_system_log_config
**功能**: 系统日志配置管理
- get_service_log_config: 获取业务日志配置
- set_service_log_config: 设置业务日志配置
- get_audit_log_config: 获取审计日志配置
- set_audit_log_config: 设置审计日志配置

**示例playbook**: `playbooks/system/log/*.yml`

### SNMP管理 - adc_system_snmp
**功能**: SNMP配置管理
- add_snmp_community: 添加SNMP团体字
- delete_snmp_community: 删除SNMP团体字
- set_snmp_server: 设置SNMP服务
- get_snmp_server: 获取SNMP服务配置

**示例playbook**: `playbooks/system/snmp/*.yml`

### 时间配置 - adc_system_time
**功能**: 系统时间管理
- get_time: 获取系统时间配置
- set_time: 设置系统时间配置

**示例playbook**: `playbooks/system/time/*.yml`

## 负载均衡模块

### 节点管理 - adc_slb_node
**功能**: 负载均衡节点管理
- add_node: 添加节点
- edit_node: 编辑节点
- delete_node: 删除节点
- get_node: 获取节点详情
- list_nodes: 列出所有节点

**示例playbook**: `playbooks/node_*.yml`

### 池管理 - adc_slb_pool
**功能**: 负载均衡池管理
- add_pool: 添加池
- edit_pool: 编辑池
- delete_pool: 删除池
- get_pool: 获取池详情
- list_pools: 列出所有池

**示例playbook**: `playbooks/pool_*.yml`

### 虚拟服务模板 - adc_slb_profile_vs
**功能**: 虚拟服务模板管理
- add_profile: 添加模板
- edit_profile: 编辑模板
- delete_profile: 删除模板
- get_profile: 获取模板详情
- list_profiles: 列出所有模板

**示例playbook**: `playbooks/vs_profile_*.yml`

## 安全模块

### WAF模板 - adc_waf_profile
**功能**: WAF模板管理
- add_profile: 添加WAF模板
- edit_profile: 编辑WAF模板
- delete_profile: 删除WAF模板
- get_profile: 获取WAF模板详情
- list_profiles: 列出所有WAF模板

**示例playbook**: `playbooks/waf_profile_*.yml`

### DDoS防护 - adc_network_ddos
**功能**: DDoS防护配置
- get_ddos_config: 获取DDoS配置
- set_ddos_config: 设置DDoS配置

**示例playbook**: `playbooks/network/ddos_*.yml`