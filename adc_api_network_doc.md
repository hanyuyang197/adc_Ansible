网络 8
接口 8
网络模式 8
管理口配置 10
以太网接口配置 13
虚拟接口配置 31
汇聚接口配置 37
LLDP 43
LLDP 配置获取 43
LLDP 邻居查询 43
LLDP 配置设置 44
VLAN 44
VLAN 配置列表 44
VLAN 配置获取 46
VLAN 配置增加 47
VLAN 配置编辑 48
VLAN 配置删除 49
汇聚(TRUNK) 49
TRUNK 配置列表 49
TRUNK 配置获取 50
TRUNK 配置增加 51
TRUNK 配置编辑 52
TRUNK 配置删除 52
IPv4 标准访问列表 53
IPv4 标准访问列表列表 53
IPv4 标准访问列表获取 54
IPv4 标准访问列表增加 54
IPv4 标准访问列表编辑 54
IPv4 标准访问列表删除 55
IPv4 标准访问列表描述设置 55
IPv4 扩展访问列表 56
IPv4 扩展访问列表列表 56
IPv4 扩展访问列表获取 57
IPv4 扩展访问列表增加 58
IPv4 扩展访问列表编辑 59
IPv4 扩展访问列表删除 60
IPv4 扩展访问列表描述设置 60
IPv6 访问列表 61
IPv6 访问列表列表 61
IPv6 访问列表获取 62
IPv6 访问列表增加 63
IPv6 访问列表编辑 64
IPv6 访问列表删除 65
IPv6 访问列表描述设置 66
时间对象 66
时间对象配置列表 66
时间对象配置获取 67
时间对象配置增加 68
时间对象配置编辑 69
时间对象配置删除 69
端口列表模板 70
端口列表模板列表 70
端口列表模板获取 70
端口列表模板增加 71
端口列表模板增加明细条目 72
端口列表模板编辑 72
端口列表模板删除 73
端口列表模板删除明细条目 73
NAT 地址转换 74
NAT 地址池 74
NAT 地址池统计信息 79
NAT 地址池组 82
静态 NAT(包括 PAT) 84
网络 NAT 93
NAT 映射 96
地址转换策略 98
NAT 全局配置 101
地址解析 104
IPv4 ARP 104
IPv6 Neigbor 108
静态路由 112
IPv4 静态路由配置列表 112
IPv4 静态路由配置获取 113
IPv4 静态路由配置增加 114
IPv4 静态路由配置编辑 114
IPv4 静态路由配置删除 115
IPv6 静态路由配置列表 115
IPv6 静态路由配置获取 116
IPv6 静态路由配置增加 117
IPv6 静态路由配置编辑 117
IPv6 静态路由配置删除 118
静态管理路由 118
IPv4 静态管理路由配置列表 118
IPv4 静态管理路由配置获取 119
IPv4 静态管理路由配置增加 120
IPv4 静态管理路由配置编辑 120
IPv4 静态管理路由配置删除 121
IPv6 静态管理路由配置列表 121
IPv6 静态管理路由配置获取 122
IPv6 静态路管理由配置增加 122
IPv6 静态管理路由配置编辑 123
IPv6 静态管理路由配置删除 123
静态业务路由 124
IPv4 静态业务路由配置列表 124
IPv4 静态业务路由配置获取 124
IPv4 静态业务路由配置增加 125
IPv4 静态业务路由配置编辑 126
IPv4 静态路业务由配置删除 127
IPv6 静态业务路由配置列表 127
IPv6 静态业务路由配置获取 128
IPv6 静态业务路由配置增加 129
IPv6 静态业务路由配置编辑 130
IPv6 静态业务路由配置删除 130
OSPF 131
OSPF 网络列表 131
OSPF 网络增加 131
OSPF 网络删除 132
OSPF 状态获取 132
OSPF 状态设置 132
BGP 133
BGP 网络列表 133
BGP 网络增加 133
BGP 网络删除 134
BGP 邻居列表 134
BGP 邻居增加 135
BGP 邻居删除 135
BGP 状态获取 135
BGP 状态设置 136
网络安全 DDOS 136
获取网络安全 DDOS 配置 136
设置网络安全 DDOS 配置 137
网络安全 SYN 攻击 137
获取全局 SYN Cookie 配置 137
设置全局 SYN Cookie 配置 138
获取每虚拟服务 SYN Cookie 配置 138
设置每虚拟服务 SYN Cookie 配置 139
流量控制 140
流量控制全局使能获取 140
流量控制全局使能设置 140
流量控制配置列表 140
流量控制配置获取 141
流量控制配置增加 142
流量控制配置编辑 142
流量控制配置删除 142
流量控制 RULE 配置列表 143
流量控制 RULE 配置获取 143
流量控制 RULE 配置增加 144
流量控制 RULE 配置编辑 145
流量控制 RULE 配置删除 145

网络
接口
网络模式
网络模式配置获取
Action：network.mode.get
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.mode.get
响应参数：
名称 类型 范围 含义
network_mode 整数 0-1 0：网关模式 1：桥模式
网关模式下全局 IP 地址配置必须为空，桥模式下全局 IP 地址必须配置
ipv4_addr Ipv4 address 全局 Ipv4 地址
ipv4_mask Ipv4 address 全局 Ipv4 掩码
ipv4_gw Ipv4 address 全局 Ipv4 网关
ipv6_addr Ipv6 address 全局 Ipv6 地址
ipv6_prefix 整数 1-128 全局 Ipv6 前缀
Ipv6_gw Ipv6 address 全局 IPV6 网关
响应举例：
{
"network_mode": 0,
"ipv4_addr": "0.0.0.0",
"ipv4_mask": "0.0.0.0",
"ipv4_gw": "0.0.0.0",
"ipv6_addr": "::",
"ipv6_prefix": 0,
"ipv6_gw": "::"
}
网络模式配置设置
Action：network.mode.set
请求参数：
名称 类型 范围 含义 必选 备注
network_mode 整数 0-1 网络模式 是 0：网关模式 1：桥模式
网关模式下全局 IP 地址配置必须为空，桥模式下全局 IP 地址必须配置
ipv4_addr Ipv4 address 全局 Ipv4 地址 是
ipv4_mask Ipv4 address 全局 Ipv4 掩码 是
ipv4_gw Ipv4 address 全局 Ipv4 网关 是
ipv6_addr Ipv6 address 全局 Ipv6 地址 否
ipv6_prefix 整数 1-128 全局 Ipv6 前缀 否
ipv6_gw Ipv6 address 全局 Ipv6 网关 否
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.mode.set
请求 body：
{
"network_mode": 1,
"ipv4_addr": "100.0.0.10",
"ipv4_mask": "255.0.0.0",
"ipv4_gw": "0.0.0.0",
"ipv6_addr": "::",
"ipv6_prefix": 0,
"ipv6_gw": "::"
}

    网络模式由网关模式改为桥模式时，所有接口需要清除所有配置

管理口配置
管理接口配置获取
Action：interface.mgmt.get
请求参数：无
请求举例：
GET
http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.mgmt.get
响应参数：
名称 类型 范围 含义
status 整数 0-1 接口状态
mac_addr 字符串 MAC 地址
dhcp_client 整数 0-1 启动 dhcp
management_services 数组 0-7 管理服务配置数组
service_type 整数 0-6 服务类型
service_ipv4_acl 整数 2-198，0 0 表示没有配置 ipv4 的 acl
service_ipv6_acl 字符串 0-10 空字符串表示没有配置 ipv6 的 acl
ipv4_acl 整数 2-198 Ipv4 访问列表
ipv6_acl 字符串 0-191 Ipv6 访问列表
ipv4_addr IP 地址 Ipv4 地址
ipv4_mask IP 地址 Ipv4 掩码
ipv4_gw IP 地址 Ipv4 网关
ipv6_addr IPV6 地址 Ipv6 地址
ipv6_prefix 整数 1-128 Ipv6 前缀
ipv6_gw IPV6 地址 Ipv6 网关
speed 整数 0-4 速度
duplexity 整数 0-2 模式
flow_control 整数 0-1 硬件流控控制
响应举例：
{
"status": 1,
"mac_addr": "00:0D:48:4F:03:58",
"dhcp_client": 0,
"ipv4_addr": "192.168.70.150",
"ipv4_mask": "255.255.255.0",
"ipv4_gw": "192.168.70.250",
"ipv4_acl": 0,
"ipv6_addr": "2000:192:168:70::150",
"ipv6_prefix": 64,
"ipv6_gw": "",
"ipv6_acl": "",
"management_services": [
{
"service_type": 0
},
{
"service_type": 1
},
{
"service_type": 2
},
{
"service_type": 3
},
{
"service_type": 4
},
{
"service_type": 5
}
],
"speed": 0,
"duplexity": 2,
"flow_control": 1
}
管理接口配置设置
Action：interface.mgmt.set
请求参数：
名称 类型 范围 含义 必选 备注
status 整数 0-1 接口状态 否 0:disable;1:enable;缺省值:不修改
dhcp_client 整数 0-1 启动 dhcp 否 0:disable;1:enable;缺省值:不修改
management_services 数组 0-7 管理服务配置数组 否
service_type 整数 0-6 服务类型 是 0 表示 http
1 表示 https
2 表示 ping
3 表示 snmp
4 表示 ssh
5 表示 telnet
6 表示 acl
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl 否
service_ipv6_acl 字符串 0-10 空字符串表示取消配置 ipv6 的 acl 否

ipv4_acl 整数 2-198 Ipv4 访问列表 否 0 表示没有配置
ipv6_acl 字符串 0-191 Ipv6 访问列表 否 “”表示没有配置
ipv4_addr IP 地址 Ipv4 地址 否 空表示没有配置，缺省值:不修改
ipv4_mask IP 地址 Ipv4 掩码 否 空表示没有配置，缺省值:不修改
ipv4_gw IP 地址 Ipv4 网关 否 空表示没有配置，缺省值:不修改
ipv6_addr IPV6 地址 Ipv6 地址 否 空表示没有配置，缺省值:不修改
ipv6_prefix 整数 1-128 Ipv6 前缀 否 空表示没有配置，缺省值:不修改
ipv6_gw IPV6 地址 Ipv6 网关 否 空表示没有配置，缺省值:不修改
speed 整数 0-4 速度 否 0: 10Mbit/s
1: 100Mbit/s
2: 1000Mbit/s
3: 10000Mbit/s
4: auto
缺省值:不修改
duplexity 整数 0-2 模式 否 0: full
1: half
2: auto
缺省值:不修改
flow_control 整数 0-1 硬件流控控制 否 0:disable;1:enable;缺省值:不修改
请求举例：
POST  
http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.mgmt.set
请求 body：
{
"status": 1,
"mac_addr": "00:0D:48:4F:03:58",
"dhcp_client": 0,
"ipv4_addr": "192.168.70.150",
"ipv4_mask": "255.255.255.0",
"ipv4_gw": "192.168.70.250",
"ipv4_acl": 0,
"ipv6_addr": "2000:192:168:70::150",
"ipv6_prefix": 64,
"ipv6_gw": "2000:192:168:70::1",
"ipv6_acl": "",
"management_services": [
{
"service_type": 0
},
{
"service_type": 1
},
{
"service_type": 2
},
{
"service_type": 3
},
{
"service_type": 4
},
{
"service_type": 5
}
],
"speed": 0,
"duplexity": 2,
"flow_control": 1
}
以太网接口配置

以太接口配置列表
Action：interface.ethernet.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.ethernet.list
响应参数：
名称 类型 范围 含义 必选 说明
slot 整数 0-8 槽位 是
port 整数 0-7
端口 是
status 整数 0-1 接口状态 否 0 表示 disable，1 表示 enable
description 字符串 0-191 接口描述 否
management_services 数组 0-7 管理服务配置数组 否
service_type 整数 0-6 服务类型 是 0 表示 http
1 表示 https
2 表示 ping
3 表示 snmp
4 表示 ssh
5 表示 telnet
6 表示 acl
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl 否
service_ipv6_acl 字符串 0-191 空字符串表示取消配置 ipv6 的 acl 否

ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
mac_addr 字符串 MAC 地址 否
ipv4_addr IP 地址 Ipv4 地址 否
ipv4_mask IP 地址 Ipv4 掩码 否
dhcp_client 整数 0-1 DHCP 启动 否 0 表示 disable，1 表示 enable
ipv4_acl 整数 2-198 Ipv4 访问列表 否 0 表示没有配置
ipv4_list 数组 0-16 Ipv4 地址列表 否
Ipv6_list 数组 0-16 Ipv6 地址列表 否
ipv6_addr IPV6 地址 Ipv6 地址 否 空表示没有配置
ipv6_prefix 整数 1-128 Ipv6 前缀 否 0 表示没有配置
ipv6_anycast 整数 0-1 Ipv6 多播 否 0 表示 disable，1 表示 enable
ipv6_local_auto 整数 0-1 Ipv6 自动配置 否 0 表示 disable，1 表示 enable
ipv6_local_addr IPV6 地址 Ipv6 本地地址 否
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀 否 0 表示没有配置
ipv6_local_anycast 整数 0-1 Ipv6 本地多播 否 0 表示 disable，1 表示 enable
ipv6_acl 字符串 0-191 Ipv6 访问列表 否 0 表示没有配置
speed 整数 0-4 速度 否 0: 10Mbit/s
1: 100Mbit/s
2: 1000Mbit/s
3: 10000Mbit/s
4: auto
duplexity 整数 0-2 模式 否 0: full
1: half
2: auto
flow_control 整数 0-1 硬件流控控制 否 0 表示 disable，1 表示 enable
permit_wildcard 整数 0-1 混杂模式 否 0 表示 disable，1 表示 enable
grat_arp 整数 0-1 免费 ARP 否 0 表示 disable，1 表示 enable
nat_dir 整数 0-3 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
no_vlan_forward 整数 0-1 禁止 VLAN 转发 否 0 表示关闭，1 表示开启
icmp_rate_limit 整数 1-65535 ICMP 速率限制值 否
icmp_lock_up_rate 整数 1-65535 ICMP 锁定门限值 否
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期 否
lldp_mode 整数 0-3 LLDP 状态 否 0 表示 Transmit and Receive
1 表示 Transmit Only
2 表示 Receive Only
3 表示 Disabled
lldp_attr
整数 LLDP 可选 TLV 否 空表示没有配置
0 表示 system-name
1 表示 system-description
2 表示 system-capability
3 表示 port-vlan-id
4 表示 port-description
6 表示 vlan-name
7 表示 protocol-identity
8 表示 mac-phy
9 表示 link-aggregation
10 表示 max-frame-size
12 表示 managenment-address
响应举例：
[
    {
        "slot": 1,
        "port": 0,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:E4:7D",
        "duplexity": 2,
        "hardware": "10G",
        "speed": 0,
        "flow_control": 0,
        "permit_wildcard": 0,
        "grat_arp": 0,
        "icmp_rate_limit": 0,
        "icmp_lock_up_rate": 0,
        "icmp_lock_up_time": 0,
        "no_vlan_forward": "0",
        "ipv4_acl": 0,
        "nat_dir": 0,
        "ipv6_nat_dir": 0,
        "dhcp_client": 0,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [],
        "ipv6_list": [],
        "ipv6_local_auto": 0,
        "ipv6_acl": "",
        "lldp_mode": 0,
        "lldp_attr": "0,1,2,3,4,6,7,8,9,10,12"
    },
    {
        "slot": 1,
        "port": 1,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:E4:7C",
        "duplexity": 2,
        "hardware": "10G",
        "speed": 0,
        "flow_control": 0,
        "permit_wildcard": 1,
        "grat_arp": 1,
        "icmp_rate_limit": 65535,
        "icmp_lock_up_rate": 65535,
        "icmp_lock_up_time": 16383,
        "no_vlan_forward": "0",
        "ipv4_acl": 0,
        "nat_dir": 3,
        "ipv6_nat_dir": 3,
        "dhcp_client": 1,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [],
        "ipv6_list": [
            {
                "ipv6_addr": "2000:172::1",
                "ipv6_prefix": 64,
                "ipv6_anycast": 0
            }
        ],
        "ipv6_local_auto": 1,
        "ipv6_acl": "",
        "lldp_mode": 0,
        "lldp_attr": "0,1,2,3,4,6,7,8,9,10,12"
    },
    {
        "slot": 4,
        "port": 0,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:B5:35",
        "duplexity": 2,
        "hardware": "10G",
        "speed": 0,
        "flow_control": 0,
        "permit_wildcard": 0,
        "grat_arp": 0,
        "icmp_rate_limit": 0,
        "icmp_lock_up_rate": 0,
        "icmp_lock_up_time": 0,
        "no_vlan_forward": "0",
        "ipv4_acl": 0,
        "nat_dir": 0,
        "ipv6_nat_dir": 0,
        "dhcp_client": 0,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [],
        "ipv6_list": [],
        "ipv6_local_auto": 0,
        "ipv6_acl": "",
        "lldp_mode": 0,
        "lldp_attr": "0,1,2,3,4,6,7,8,9,10,12"
    }]
备注：除其他分区独占接口外的所有接口
Action：interface.ethernet.list.withcommon
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.ethernet.list.withcommon
响应参数：
名称 类型 范围 含义 必选 说明
slot 整数 0-255 槽位 是
port 整数 0-255 端口 是
status 整数 0-1 接口状态 否 0 表示 disable，1 表示 enable
description 字符串 0-191 接口描述 否
management_services 数组 0-7 管理服务配置数组 否
service_type 整数 0-6 服务类型 是 0 表示 http
1 表示 https
2 表示 ping
3 表示 snmp
4 表示 ssh
5 表示 telnet
6 表示 acl
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl 否
service_ipv6_acl 字符串 0-128 空字符串表示取消配置 ipv6 的 acl 否

ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
mac_addr 字符串 Mac 地址 MAC 地址 否
ipv4_addr IP 地址 Ipv4 地址 否
ipv4_mask IP 地址 Ipv4 掩码 否
dhcp_client 整数 0-1 DHCP 启动 否 0 表示 disable，1 表示 enable
ipv4_acl 整数 2-198 Ipv4 访问列表 否 0 表示没有配置
ipv4_list 数组 0-16 Ipv4 地址列表 否
Ipv6_list 数组 0-16 Ipv6 地址列表 否
ipv6_addr IPV6 地址 Ipv6 地址 否 空表示没有配置
ipv6_prefix 整数 1-128 Ipv6 前缀 否 0 表示没有配置
ipv6_anycast 整数 0-1 Ipv6 多播 否 0 表示 disable，1 表示 enable
ipv6_local_auto 整数 0-1 Ipv6 自动配置 否 0 表示 disable，1 表示 enable
ipv6_local_addr IPV6 地址 Ipv6 本地地址 否
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀 否 0 表示没有配置
ipv6_local_anycast 整数 Ipv6 本地多播 否 0 表示 disable，1 表示 enable
ipv6_acl 字符串 0-15 Ipv6 访问列表 否 0 表示没有配置
speed 整数 0-4 速度 否 0: 10Mbit/s
1: 100Mbit/s
2: 1000Mbit/s
3: 10000Mbit/s
4: auto
duplexity 整数 0-2 模式 否 0: full
1: half
2: auto
flow_control 整数 0-1 硬件流控控制 否 0 表示 disable，1 表示 enable
permit_wildcard 整数 0-1 混杂模式 否 0 表示 disable，1 表示 enable
grat_arp 整数 0-1 免费 ARP 否 0 表示 disable，1 表示 enable
nat_dir 整数 0-3 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
no_vlan_forward 整数 0-1 禁止 VLAN 转发 否 0 表示关闭，1 表示开启
icmp_rate_limit 整数 1-65535 ICMP 速率限制值 否
icmp_lock_up_rate 整数 1-65535 ICMP 锁定门限值 否
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期 否
lldp_mode 整数 0-3 LLDP 状态 否 0 表示 Transmit and Receive
1 表示 Transmit Only
2 表示 Receive Only
3 表示 Disabled
lldp_attr
整数 0-12 LLDP 可选 TLV 否
响应举例：
[
    {
        "slot": 1,
        "port": 0,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:E4:7D",
        "duplexity": 2,
        "hardware": "10G",
        "speed": 0,
        "flow_control": 0,
        "permit_wildcard": 0,
        "grat_arp": 0,
        "icmp_rate_limit": 0,
        "icmp_lock_up_rate": 0,
        "icmp_lock_up_time": 0,
        "no_vlan_forward": "0",
        "ipv4_acl": 0,
        "nat_dir": 0,
        "ipv6_nat_dir": 0,
        "dhcp_client": 0,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [],
        "ipv6_list": [],
        "ipv6_local_auto": 0,
        "ipv6_acl": "",
        "lldp_mode": 0,
        "lldp_attr": "0,1,2,3,4,6,7,8,9,10,12"
    },
    {
        "slot": 1,
        "port": 1,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:E4:7C",
        "duplexity": 2,
        "hardware": "10G",
        "speed": 0,
        "flow_control": 0,
        "permit_wildcard": 1,
        "grat_arp": 1,
        "icmp_rate_limit": 65535,
        "icmp_lock_up_rate": 65535,
        "icmp_lock_up_time": 16383,
        "no_vlan_forward": "0",
        "ipv4_acl": 0,
        "nat_dir": 3,
        "ipv6_nat_dir": 3,
        "dhcp_client": 1,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [],
        "ipv6_list": [
            {
                "ipv6_addr": "2000:172::1",
                "ipv6_prefix": 64,
                "ipv6_anycast": 0
            }
        ],
        "ipv6_local_auto": 1,
        "ipv6_acl": "",
        "lldp_mode": 0,
        "lldp_attr": "0,1,2,3,4,6,7,8,9,10,12"
    }
]

备注: 显示本分区已使用的接口
Action：interface.ethernet.list.withused
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.ethernet.list.withused
响应参数：
名称 类型 范围 含义 必选 说明
slot 整数 0-255 槽位 是
port 整数 0-255 端口 是
status 整数 0-1 接口状态 否 0 表示 disable，1 表示 enable
description 字符串 0-191 接口描述 否
management_services 数组 0-7 管理服务配置数组 否
service_type 整数 0-6 服务类型 是 0 表示 http
1 表示 http
2 表示 ping
3 表示 snmp
4 表示 ssh
5 表示 telnet
6 表示 acl
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl 否
service_ipv6_acl 字符串 0-128 空字符串表示取消配置 ipv6 的 acl 否

ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
mac_addr 字符串 Mac 地址 MAC 地址 否
ipv4_addr IP 地址 Ipv4 地址 否
ipv4_mask IP 地址 Ipv4 掩码 否
dhcp_client 整数 0-1 DHCP 启动 否 0 表示 disable，1 表示 enable
ipv4_acl 整数 2-198 Ipv4 访问列表 否 0 表示没有配置
ipv4_list 数组 0-16 Ipv4 地址列表 否
Ipv6_list 数组 0-16 Ipv6 地址列表 否
ipv6_addr IPV6 地址 Ipv6 地址 否 空表示没有配置
ipv6_prefix 整数 1-128 Ipv6 前缀 否 0 表示没有配置
ipv6_anycast 整数 0-1 Ipv6 多播 否 0 表示 disable，1 表示 enable
ipv6_local_auto 整数 0-1 Ipv6 自动配置 否 0 表示 disable，1 表示 enable
ipv6_local_addr IPV6 地址 Ipv6 本地地址 否
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀 否 0 表示没有配置
ipv6_local_anycast 整数 Ipv6 本地多播 否 0 表示 disable，1 表示 enable
ipv6_acl 字符串 0-15 Ipv6 访问列表 否 0 表示没有配置
speed 整数 0-4 速度 否 0: 10Mbit/s
1: 100Mbit/s
2: 1000Mbit/s
3: 10000Mbit/s
4: auto
duplexity 整数 0-2 模式 否 0: full
1: half
2: auto
flow_control 整数 0-1 硬件流控控制 否 0 表示 disable，1 表示 enable
permit_wildcard 整数 0-1 混杂模式 否 0 表示 disable，1 表示 enable
grat_arp 整数 0-1 免费 ARP 否 0 表示 disable，1 表示 enable
nat_dir 整数 0-3 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
no_vlan_forward 整数 0-1 禁止 VLAN 转发 否 0 表示关闭，1 表示开启
icmp_rate_limit 整数 1-65535 ICMP 速率限制值 否
icmp_lock_up_rate 整数 1-65535 ICMP 限制门限值 否
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期 否
lldp_mode 整数 0-3 LLDP 状态 否 0 表示 Transmit and Receive
1 表示 Transmit Only
2 表示 Receive Only
3 表示 Disabled
lldp_attr
整数 0-12 LLDP 可选 TLV 否
响应举例：
[
    {
        "slot": 1,
        "port": 0,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:E4:7D",
        "duplexity": 2,
        "hardware": "10G",
        "speed": 0,
        "flow_control": 0,
        "permit_wildcard": 0,
        "grat_arp": 0,
        "icmp_rate_limit": 0,
        "icmp_lock_up_rate": 0,
        "icmp_lock_up_time": 0,
        "no_vlan_forward": "0",
        "ipv4_acl": 0,
        "nat_dir": 0,
        "ipv6_nat_dir": 0,
        "dhcp_client": 0,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [],
        "ipv6_list": [],
        "ipv6_local_auto": 0,
        "ipv6_acl": "",
        "lldp_mode": 0,
        "lldp_attr": "0,1,2,3,4,6,7,8,9,10,12"
    },
    {
        "slot": 1,
        "port": 1,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:E4:7C",
        "duplexity": 2,
        "hardware": "10G",
        "speed": 0,
        "flow_control": 0,
        "permit_wildcard": 1,
        "grat_arp": 1,
        "icmp_rate_limit": 65535,
        "icmp_lock_up_rate": 65535,
        "icmp_lock_up_time": 16383,
        "no_vlan_forward": "0",
        "ipv4_acl": 0,
        "nat_dir": 3,
        "ipv6_nat_dir": 3,
        "dhcp_client": 1,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [],
        "ipv6_list": [
            {
                "ipv6_addr": "2000:172::1",
                "ipv6_prefix": 64,
                "ipv6_anycast": 0
            }
        ],
        "ipv6_local_auto": 1,
        "ipv6_acl": "",
        "lldp_mode": 0,
        "lldp_attr": "0,1,2,3,4,6,7,8,9,10,12"
    }
]

备注：显示本分区独占接口
Action：interface.ethernet.list.self
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.ethernet.list.self
响应参数：
名称 类型 范围 含义 必选 说明
slot 整数 0-255 槽位 是
port 整数 0-255 端口 是
status 整数 0-1 接口状态 否 0 表示 disable，1 表示 enable
description 字符串 0-191 接口描述 否
management_services 数组 0-7 管理服务配置数组 否
service_type 整数 0-6 服务类型 是 0 表示 http
1 表示 http
2 表示 ping
3 表示 snmp
4 表示 ssh
5 表示 telnet
6 表示 acl
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl 否
service_ipv6_acl 字符串 0-128 空字符串表示取消配置 ipv6 的 acl 否

ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
mac_addr 字符串 Mac 地址 MAC 地址 否
ipv4_addr IP 地址 Ipv4 地址 否
ipv4_mask IP 地址 Ipv4 掩码 否
dhcp_client 整数 0-1 DHCP 启动 否 0 表示 disable，1 表示 enable
ipv4_acl 整数 2-198 Ipv4 访问列表 否 0 表示没有配置
ipv4_list 数组 0-16 Ipv4 地址列表 否
Ipv6_list 数组 0-16 Ipv6 地址列表 否
ipv6_addr IPV6 地址 Ipv6 地址 否 空表示没有配置
ipv6_prefix 整数 1-128 Ipv6 前缀 否 0 表示没有配置
ipv6_anycast 整数 0-1 Ipv6 多播 否 0 表示 disable，1 表示 enable
ipv6_local_auto 整数 0-1 Ipv6 自动配置 否 0 表示 disable，1 表示 enable
ipv6_local_addr IPV6 地址 Ipv6 本地地址 否
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀 否 0 表示没有配置
ipv6_local_anycast 整数 Ipv6 本地多播 否 0 表示 disable，1 表示 enable
ipv6_acl 字符串 0-15 Ipv6 访问列表 否 0 表示没有配置
speed 整数 0-4 速度 否 0: 10Mbit/s
1: 100Mbit/s
2: 1000Mbit/s
3: 10000Mbit/s
4: auto
duplexity 整数 0-2 模式 否 0: full
1: half
2: auto
flow_control 整数 0-1 硬件流控控制 否 0 表示 disable，1 表示 enable
permit_wildcard 整数 0-1 混杂模式 否 0 表示 disable，1 表示 enable
grat_arp 整数 0-1 免费 ARP 否 0 表示 disable，1 表示 enable
nat_dir 整数 0-3 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
no_vlan_forward 整数 0-1 禁止 VLAN 转发 否 0 表示关闭，1 表示开启
icmp_rate_limit
整数 1-65535 ICMP 速率限制值 否
icmp_lock_up_rate 整数 1-65535 ICMP 限制门限值 否
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期 否
lldp_mode 整数 0-3 LLDP 状态 否 0 表示 Transmit and Receive
1 表示 Transmit Only
2 表示 Receive Only
3 表示 Disabled
lldp_attr
整数 0-12 LLDP 可选 TLV 否
响应举例：
    {
        "slot": 1,
        "port": 1,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:E4:7C",
        "duplexity": 2,
        "hardware": "10G",
        "speed": 0,
        "flow_control": 0,
        "permit_wildcard": 1,
        "grat_arp": 1,
        "icmp_rate_limit": 65535,
        "icmp_lock_up_rate": 65535,
        "icmp_lock_up_time": 16383,
        "no_vlan_forward": "0",
        "ipv4_acl": 0,
        "nat_dir": 3,
        "ipv6_nat_dir": 3,
        "dhcp_client": 1,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [],
        "ipv6_list": [
            {
                "ipv6_addr": "2000:172::1",
                "ipv6_prefix": 64,
                "ipv6_anycast": 0
            }
        ],
        "ipv6_local_auto": 1,
        "ipv6_acl": "",
        "lldp_mode": 0,
        "lldp_attr": "0,1,2,3,4,6,7,8,9,10,12"
    }
以太接口配置获取
Action: interface.ethernet.get
请求参数：
名称 类型 范围 含义 必选 备注
slot 整数 0-8 槽位 是
port 整数 0-7 端口 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.ethernet.get
请求 body：
{
"slot": 1,
"port": 1
}
响应参数：
名称 类型 范围 含义 必选 说明
slot 整数 0-8 槽位 是
port 整数 0-7 端口 是
status 整数 0-1 接口状态 否 0 表示 disable，1 表示 enable
description 字符串 0-191 接口描述 否
management_services 数组 0-7 管理服务配置数组 否
service_type 整数 0-6 服务类型 是 0 表示 http
1 表示 https
2 表示 ping
3 表示 snmp
4 表示 ssh
5 表示 telnet
6 表示 acl
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl 否
service_ipv6_acl 字符串 0-191 空字符串表示取消配置 ipv6 的 acl 否

ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
mac_addr 字符串 MAC 地址 否
ipv4_addr IP 地址 Ipv4 地址 否
ipv4_mask IP 地址 Ipv4 掩码 否
dhcp_client 整数 0-1 DHCP 启动 否 0 表示 disable，1 表示 enable
ipv4_acl 整数 2-198 Ipv4 访问列表 否 0 表示没有配置
ipv4_list 数组 0-16 Ipv4 地址列表 否
Ipv6_list 数组 0-16 Ipv6 地址列表 否
ipv6_addr IPV6 地址 Ipv6 地址 否 空表示没有配置
ipv6_prefix 整数 1-128 Ipv6 前缀 否 0 表示没有配置
ipv6_anycast 整数 0-1 Ipv6 多播 否 0 表示 disable，1 表示 enable
ipv6_local_auto 整数 0-1 Ipv6 自动配置 否 0 表示 disable，1 表示 enable
ipv6_local_addr IPV6 地址 Ipv6 本地地址 否
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀 否 0 表示没有配置
ipv6_local_anycast 整数 Ipv6 本地多播 否 0 表示 disable，1 表示 enable
ipv6_acl 字符串 0-191 Ipv6 访问列表 否 0 表示没有配置
speed 整数 0-4 速度 否 0: 10Mbit/s
1: 100Mbit/s
2: 1000Mbit/s
3: 10000Mbit/s
4: auto
duplexity 整数 0-2 模式 否 0: full
1: half
2: auto
flow_control 整数 0-1 硬件流控控制 否 0 表示 disable，1 表示 enable
permit_wildcard 整数 0-1 混杂模式 否 0 表示 disable，1 表示 enable
grat_arp 整数 0-1 免费 ARP 否 0 表示 disable，1 表示 enable
nat_dir 整数 0-3 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
no_vlan_forward 整数 0-1 禁止 VLAN 转发 否 0 表示关闭，1 表示开启
icmp_rate_limit 整数 1-65535 ICMP 速率限制值 否
icmp_lock_up_rate 整数 1-65535 ICMP 锁定门限值 否
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期 否
lldp_mode 整数 0-3 LLDP 状态 否 0 表示 Transmit and Receive
1 表示 Transmit Only
2 表示 Receive Only
3 表示 Disabled
lldp_attr
整数 LLDP 可选 TLV 否 空表示没有配置
0 表示 system-name
1 表示 system-description
2 表示 system-capability
3 表示 port-vlan-id
4 表示 port-description
6 表示 vlan-name
7 表示 protocol-identity
8 表示 mac-phy
9 表示 link-aggregation
10 表示 max-frame-size
12 表示 managenment-address
响应举例：
{
    "slot": 1,
    "port": 1,
    "description": "",
    "status": 1,
    "mac_addr": "00:0D:48:6D:E4:7C",
    "duplexity": 2,
    "hardware": "10G",
    "speed": 0,
    "flow_control": 0,
    "permit_wildcard": 1,
    "grat_arp": 1,
    "icmp_rate_limit": 65535,
    "icmp_lock_up_rate": 65535,
    "icmp_lock_up_time": 16383,
    "no_vlan_forward": "0",
    "ipv4_acl": 0,
    "nat_dir": 3,
    "ipv6_nat_dir": 3,
    "dhcp_client": 1,
    "management_services": [
        {
            "service_type": 2
        }
    ],
    "ipv4_list": [],
    "ipv6_list": [
        {
            "ipv6_addr": "2000:172::1",
            "ipv6_prefix": 64,
            "ipv6_anycast": 0
        }
    ],
    "ipv6_local_auto": 1,
    "ipv6_acl": "",
    "lldp_mode": 0,
    "lldp_attr": "0,1,2,3,4,6,7,8,9,10,12"
}
以太接口配置编辑
Action：interface.ethernet.edit
请求参数：
名称 类型 范围 含义 必选 说明
slot 整数 0-8 槽位 是
port 整数 0-7 端口 是
status 整数 0-1 接口状态 否 0:disable;1:enable;缺省值:不修改
description 字符串 0-191 接口描述 否 空表示没有配置;缺省值:不修改
management_services 数组 0-7 管理服务配置数组 否
service_type 整数 0-6 服务类型 是 0 表示 http
1 表示 https
2 表示 ping
3 表示 snmp
4 表示 ssh
5 表示 telnet
6 表示 acl
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl 否
service_ipv6_acl 字符串 0-191 空字符串表示取消配置 ipv6 的 acl 否

ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向 否 0 表示没有配置；缺省值：不修改
1 表示 inside
2 表示 outside
3 表示 bidirection
ipv4_addr Ipv4 address Ipv4 地址 否 空表示没有配置;缺省值:不修改
ipv4_mask Ipv4 address Ipv4 掩码 否 空表示没有配置;缺省值:不修改
dhcp_client 整数 0-1 DHCP 启动 否 0:disable;1:enable;缺省值:不修改
ipv4_acl 整数 2-198 Ipv4 访问列表 否 0 表示没有配置;缺省值:不修改
ipv4_list 数组 0-16 Ipv4 地址列表 否 空表示没有配置;缺省值:不修改
Ipv6_list 数组 0-16 Ipv6 地址列表 否 空表示没有配置;缺省值:不修改
ipv6_addr Ipv6 address Ipv6 地址 否 空表示没有配置;缺省值:不修改
ipv6_prefix 整数 1-128 Ipv6 前缀 否 0 表示没有配置;缺省值:不修改
ipv6_anycast 整数 0-1 Ipv6 多播 否 0:disable;1:enable;缺省值:不修改
ipv6_local_auto 整数 0-1 Ipv6 自动配置 否 0:disable;1:enable;缺省值:0
ipv6_local_addr Ipv6 address Ipv6 本地地址 否 空表示没有配置;缺省值: 空
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀 否 0 表示没有配置;缺省值:不修改
ipv6_local_anycast 整数 Ipv6 本地多播 否 0:disable;1:enable;缺省值:不修改
ipv6_acl 字符串 0-191 Ipv6 访问列表 否 0 表示没有配置;缺省值:不修改
speed 整数 0-4 速度 否 0: 10Mbit/s
1: 100Mbit/s
2: 1000Mbit/s
3: 10000Mbit/s
4: auto
;缺省值:不修改
duplexity 整数 0-2 模式 否 0: full
1: half
2: auto
;缺省值:不修改
flow_control 整数 0-1 硬件流控控制 否 0:disable;1:enable;缺省值:不修改
permit_wildcard 整数 0-1 混杂模式 否 0:disable;1:enable;缺省值:不修改
grat_arp 整数 0-1 免费 ARP 否 0:disable;1:enable;缺省值:不修改
nat_dir 整数 0-3 Nat 方向 否 0 表示没有配置;缺省值:不修改
1 表示 inside
2 表示 outside
3 表示 bidirection
no_vlan_forward 整数 0-1 禁止 VLAN 转发 否 0 表示关闭，1 表示开启
icmp_rate_limit 整数 1-65535 ICMP 速率限制值 否
icmp_lock_up_rate 整数 1-65535 ICMP 锁定门限值 否
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期 否
lldp_mode 整数 0-3 LLDP 状态 否 0 表示 Transmit and Receive
1 表示 Transmit Only
2 表示 Receive Only
3 表示 Disabled
lldp_attr
整数 0-12 LLDP 可选 TLV 否 空表示没有配置
0 表示 system-name
1 表示 system-description
2 表示 system-capability
3 表示 port-vlan-id
4 表示 port-description
6 表示 vlan-name
7 表示 protocol-identity
8 表示 mac-phy
9 表示 link-aggregation
10 表示 max-frame-size
12 表示 managenment-address
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.ethernet.edit
请求 body：
{
    "slot": 1,
    "port": 1,
    "description": "",
    "status": 1,
    "mac_addr": "00:0D:48:6D:E4:7C",
    "duplexity": 2,
    "hardware": "10G",
    "speed": 0,
    "flow_control": 0,
    "permit_wildcard": 1,
    "grat_arp": 1,
    "icmp_rate_limit": 65535,
    "icmp_lock_up_rate": 65535,
    "icmp_lock_up_time": 1638,
    "no_vlan_forward": "0",
    "ipv4_acl": 0,
    "nat_dir": 3,
    "ipv6_nat_dir": 3,
    "dhcp_client": 1,
    "management_services": [
        {
            "service_type": 2
        }
    ],
    "ipv4_list": [],
    "ipv6_list": [
        {
            "ipv6_addr": "2000:172::1",
            "ipv6_prefix": 64,
            "ipv6_anycast": 0
        }
    ],
    "ipv6_local_auto": 1,
    "ipv6_acl": "",
    "lldp_mode": 0,
    "lldp_attr": "0,1,2,3,4,6,7,8,9,10,12"
}
获取接口统计信息
Action：
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.ethernet.statis
响应参数：
名称 类型 范围 含义
slot 整数 0-8 接口插槽号
port 整数 0-7 接口端口号
mtu 整数 1-1500
speed 字符串 "10,000,000,000", 10G
"1,000,000,000",1G
"100,000,000",100M
"10,000,000",10M
"auto" 自动
description 字符串 接口描述信息
ipaddr 字符串 接口 IP 地址
status 整数 0-2 0：unknown;1:down;2:up
in_unicast_pkts 字符串 接收的单播报文数
out_unicast_pkts 字符串 发送的单播报文数
in_bytes 字符串 接收的字节数
out_bytes 字符串 发送的字节数
in_error_pkts 字符串 接收的错误报文数
out_error_pkts 字符串 发送的错误报文数
in_discard_pkts 字符串 接收后丢弃的报文数
out_discard_pkts 字符串 发送后丢弃的报文数
in_bit_rate 字符串 接收速率(bps)
out_bit_rate 字符串 发送速率(bps)
in_pkt_rate 字符串 接收报文速率(pps)
out_pkt_rate 字符串 发送报文速率(pps)
响应举例：
[
    {
        "slot": 1,
        "port": 0,
        "mtu": 1500,
        "speed": "10,000,000,000",
        "ipaddr": "",
        "description": "",
        "status": 2,
        "in_unicast_pkts": "326815630",
        "in_bytes": "312159388657",
        "in_error_pkts": "0",
        "in_discard_pkts": "0",
        "in_bit_rate": "1113524808",
        "in_pkt_rate": "145711",
        "out_unicast_pkts": "333518520",
        "out_bytes": "313500706220",
        "out_error_pkts": "0",
        "out_discard_pkts": "0",
        "out_bit_rate": "1118312624",
        "out_pkt_rate": "148700"
    },
    {
        "slot": 1,
        "port": 1,
        "mtu": 1500,
        "speed": "10,000,000,000",
        "ipaddr": "2000:172::1/64",
        "description": "",
        "status": 2,
        "in_unicast_pkts": "1602",
        "in_bytes": "842479",
        "in_error_pkts": "0",
        "in_discard_pkts": "0",
        "in_bit_rate": "2800",
        "in_pkt_rate": "0",
        "out_unicast_pkts": "837",
        "out_bytes": "804480",
        "out_error_pkts": "0",
        "out_discard_pkts": "0",
        "out_bit_rate": "2496",
        "out_pkt_rate": "0"
    }]
虚拟接口配置
虚拟接口配置列表
Action：interface.ve.list
请求参数：无
请求举例：
GET
http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.ve.list
响应参数：
名称 类型 范围 含义
port_num 整数 2-4094 端口
status 整数 0-1 接口状态
description 字符串 0-191 接口描述
management_services 数组 0-7 管理服务配置数组
service_type 整数 0-6 服务类型
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl
service_ipv6_acl 字符串 0-191 空字符串表示取消配置 ipv6 的 acl
ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向
mac_addr 字符串 MAC 地址
ipv4_addr Ipv4 address Ipv4 地址
ipv4_mask Ipv4 address Ipv4 掩码
ipv4_acl 整数 2-198 Ipv4 访问列表
ipv4_list 数组 0-16 Ipv4 地址列表
Ipv6_list 数组 0-16 Ipv6 地址列表
ipv6_addr Ipv6 address Ipv6 地址
ipv6_prefix 整数 1-128 Ipv6 前缀
ipv6_anycast 整数 0-1 Ipv6 多播
ipv6_local_auto 整数 0-1 Ipv6 自动配置
ipv6_local_addr Ipv6 address Ipv6 本地地址
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀
ipv6_local_anycast 整数 Ipv6 本地多播
ipv6_acl 字符串 0-191 Ipv6 访问列表
nat_dir 整数 0-3 Nat 方向
permit_wildcard 整数 0-1 混杂模式
grat_arp 整数 0-1 免费 ARP
no_vlan_forward 整数 0-1 禁止 VLAN 转发
icmp_rate_limit 整数 1-65535 ICMP 速率限制值
icmp_lock_up_rate 整数 1-65535 ICMP 锁定门限值
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期
响应举例：
[
    {
        "port_num": 1001,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:B5:32",
        "permit_wildcard": 0,
        "grat_arp": 0,
        "nat_dir": 0,
        "ipv6_nat_dir": 0,
        "no_vlan_forward": "0",
        "icmp_rate_limit": 0,
        "icmp_lock_up_rate": 0,
        "icmp_lock_up_time": 0,
        "ipv4_acl": 0,
        "management_services": [
            {
                "service_type": 2
            },
            {
                "service_type": 4
            }
        ],
        "ipv4_list": [
            {
                "ipv4_addr": "1.1.5.4",
                "ipv4_mask": "255.255.255.0"
            }
        ],
        "ipv6_list": [],
        "ipv6_local_auto": 0,
        "ipv6_acl": ""
    },
    {
        "port_num": 1801,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:63:E8:74",
        "permit_wildcard": 1,
        "grat_arp": 1,
        "nat_dir": 3,
        "ipv6_nat_dir": 3,
        "no_vlan_forward": "0",
        "icmp_rate_limit": 65535,
        "icmp_lock_up_rate": 65535,
        "icmp_lock_up_time": 16383,
        "ipv4_acl": 0,
        "management_services": [
            {
                "service_type": 0
            },
            {
                "service_type": 1
            },
            {
                "service_type": 2
            },
            {
                "service_type": 3
            },
            {
                "service_type": 4
            },
            {
                "service_type": 5
            }
        ],
        "ipv4_list": [
            {
                "ipv4_addr": "155.0.0.4",
                "ipv4_mask": "255.255.255.0"
            }
        ],
        "ipv6_list": [
            {
                "ipv6_addr": "2000:155:1::4",
                "ipv6_prefix": 64,
                "ipv6_anycast": 0
            }
        ],
        "ipv6_local_auto": 1,
        "ipv6_acl": ""
    }]
只有创建 vlan 开启虚拟接口才能对虚拟接口操作

虚拟接口配置获取
Action：interface.ve.get
请求参数：
名称 类型 范围 含义 必选 备注
port_num 整数 2-4094 端口 是
请求举例：
POST
http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.ve.get
请求 body：
{
"port_num": 1001
}
响应参数：
名称 类型 范围 含义
port_num 整数 2-4094 端口
status 整数 0-1 接口状态
description 字符串 0-191 接口描述
management_services 数组 0-7 管理服务配置数组
service_type 整数 0-6 服务类型
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl
service_ipv6_acl 字符串 0-128 空字符串表示取消配置 ipv6 的 acl
ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向
mac_addr 字符串 MAC 地址
ipv4_addr Ipv4 address Ipv4 地址
ipv4_mask Ipv4 address Ipv4 掩码
ipv4_acl 整数 2-198 Ipv4 访问列表
ipv4_list 数组 0-16 Ipv4 地址列表
Ipv6_list 数组 0-16 Ipv6 地址列表
ipv6_addr Ipv6 address Ipv6 地址
ipv6_prefix 整数 1-128 Ipv6 前缀
ipv6_anycast 整数 0-1 Ipv6 多播
ipv6_local_auto 整数 0-1 Ipv6 自动配置
ipv6_local_addr Ipv6 address Ipv6 本地地址
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀
ipv6_local_anycast 整数 Ipv6 本地多播
ipv6_acl 字符串 0-15 Ipv6 访问列表
nat_dir 整数 0-3 Nat 方向
permit_wildcard 整数 0-1 混杂模式
grat_arp 整数 0-1 免费 ARP
no_vlan_forward 整数 0-1 禁止 VLAN 转发
icmp_rate_limit 整数 1-65535 ICMP 速率限制值
icmp_lock_up_rate 整数 1-65535 ICMP 锁定门限值
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期
响应举例：
{
        "port_num": 1001,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:B5:32",
        "permit_wildcard": 0,
        "grat_arp": 0,
        "nat_dir": 0,
        "ipv6_nat_dir": 0,
        "no_vlan_forward": "0",
        "icmp_rate_limit": 0,
        "icmp_lock_up_rate": 0,
        "icmp_lock_up_time": 0,
        "ipv4_acl": 0,
        "management_services": [
            {
                "service_type": 2
            },
            {
                "service_type": 4
            }
        ],
        "ipv4_list": [
            {
                "ipv4_addr": "1.1.5.4",
                "ipv4_mask": "255.255.255.0"
            }
        ],
        "ipv6_list": [],
        "ipv6_local_auto": 0,
        "ipv6_acl": ""
}
虚拟接口配置编辑
Action：interface.ve.edit
请求参数：
名称 类型 范围 含义 必选 说明
port_num 整数 2-4094 端口 是 对应 ve 接口序号
status 整数 0-1 接口状态 否 0:disable;1:enable;缺省值:不修改
description 字符串 0-191 接口描述 否 缺省值:不修改
management_services 数组 0-7 管理服务配置数组 否
service_type 整数 0-6 服务类型 是 0 表示 http
1 表示 https
2 表示 ping
3 表示 snmp
4 表示 ssh
5 表示 telnet
6 表示 acl
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl 否
service_ipv6_acl 字符串 0-191 空字符串表示取消配置 ipv6 的 acl 否

ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向 否 0 表示没有配置；缺省值：不修改
1 表示 inside
2 表示 outside
3 表示 bidirection
ipv4_addr Ipv4 address Ipv4 地址 是
ipv4_mask Ipv4 address Ipv4 掩码 是
ipv4_acl 整数 2-198 Ipv4 访问列表 否 0 表示没有配置;缺省值:不修改
ipv4_list 数组 0-16 Ipv4 地址列表 否 缺省值:不修改
Ipv6_list 数组 0-16 Ipv6 地址列表 否 缺省值:不修改
ipv6_addr Ipv6 address Ipv6 地址 是 空表示没有配置;缺省值:不修改
ipv6_prefix 整数 1-128 Ipv6 前缀 是 0 表示没有配置;缺省值:不修改
ipv6_anycast 整数 0-1 Ipv6 多播 是 0:disable;1:enable;缺省值:不修改
ipv6_local_auto 整数 0-1 Ipv6 自动配置 否 0:disable;1:enable;缺省值:不修改
ipv6_local_addr Ipv6 address Ipv6 本地地址 否 默认值空字符串，配置该项 ipv6_local_auto 自动变成 disable;缺省值:0
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀 否 0 表示没有配置;缺省值:不修改
ipv6_local_anycast 整数 Ipv6 本地多播 否 0:disable;1:enable;缺省值:不修改
ipv6_acl 字符串 0-191 Ipv6 访问列表 否 0 表示没有配置;缺省值:不修改
nat_dir 整数 0-3 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
;缺省值:不修改
permit_wildcard 整数 0-1 混杂模式 否 0:disable;1:enable;缺省值:不修改
grat_arp 整数 0-1 免费 ARP 否 0:disable;1:enable;缺省值:不修改
no_vlan_forward 整数 0-1 禁止 VLAN 转发 否 0 表示关闭，1 表示开启
icmp_rate_limit 整数 1-65535 ICMP 速率限制值 否
icmp_lock_up_rate 整数 1-65535 ICMP 锁定门限值 否
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期 否
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.ve.edit

请求 body：
{
        "port_num": 1001,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:B5:32",
        "permit_wildcard": 0,
        "grat_arp": 0,
        "nat_dir": 0,
        "ipv6_nat_dir": 0,
        "no_vlan_forward": "0",
        "icmp_rate_limit": 0,
        "icmp_lock_up_rate": 0,
        "icmp_lock_up_time": 0,
        "ipv4_acl": 0,
        "management_services": [
            {
                "service_type": 2
            },
            {
                "service_type": 4
            }
        ],
        "ipv4_list": [
            {
                "ipv4_addr": "1.1.5.4",
                "ipv4_mask": "255.255.255.0"
            }
        ],
        "ipv6_list": [],
        "ipv6_local_auto": 0,
        "ipv6_acl": ""
}
汇聚接口配置
汇聚接口配置列表
Action：interface.trunk.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.trunk.list
响应参数：
名称 类型 范围 含义
port_num 整数 1-8 端口
status 整数 0-2 接口状态
description 字符串 0-191 接口描述
management_services 数组 0-7 管理服务配置数组
service_type 整数 0-6 服务类型
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl
service_ipv6_acl 字符串 0-191 空字符串表示取消配置 ipv6 的 acl
ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向
mac_addr 字符串 MAC 地址
ipv4_addr Ipv4 address Ipv4 地址
ipv4_mask Ipv4 address Ipv4 掩码
ipv4_acl 整数 2-198 Ipv4 访问列表
ipv4_list 数组 0-16 Ipv4 地址列表
Ipv6_list 数组 0-16 Ipv6 地址列表
ipv6_addr Ipv6 address Ipv6 地址
ipv6_prefix 整数 1-128 Ipv6 前缀
ipv6_anycast 整数 0-1 Ipv6 多播
ipv6_local_auto 整数 0-1 Ipv6 自动配置
ipv6_local_addr Ipv6 address Ipv6 本地地址
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀
ipv6_local_anycast 整数 0-1 Ipv6 本地多播
ipv6_acl 字符串 0-191 Ipv6 访问列表
nat_dir 整数 0-3 Nat 方向
permit_wildcard 整数 0-1 混杂模式
grat_arp 整数 0-1 免费 ARP
no_vlan_forward 整数 0-1 禁止 VLAN 转发
icmp_rate_limit 整数 1-65535 ICMP 速率限制值
icmp_lock_up_rate 整数 1-65535 ICMP 锁定门限值
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期
响应举例：
[
    {
        "port_num": 1,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:B5:35",
        "permit_wildcard": 1,
        "grat_arp": 1,
        "nat_dir": 3,
        "ipv6_nat_dir": 3,
        "no_vlan_forward": "0",
        "icmp_rate_limit": 65535,
        "icmp_lock_up_rate": 65535,
        "icmp_lock_up_time": 16383,
        "ipv4_acl": 0,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [
            {
                "ipv4_addr": "171.1.1.1",
                "ipv4_mask": "255.255.255.0"
            }
        ],
        "ipv6_list": [
            {
                "ipv6_addr": "2000:171:1::1",
                "ipv6_prefix": 64,
                "ipv6_anycast": 0
            }
        ],
        "ipv6_local_auto": 1,
        "ipv6_acl": ""
    }
]

    只有创建汇聚，汇聚没有被N引用的时才能对汇聚接口操作

汇聚接口配置获取
Action：interface.trunk.get
请求参数：
名称 类型 范围 含义 必选 备注
port_num 整数 1-8 端口 是 对应 trunk 接口序号
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.trunk.get
{
"port_num": 1
}
响应参数：
名称 类型 范围 含义
port_num 整数 2-4094 端口
status 整数 0-1 接口状态
description 字符串 0-191 接口描述
management_services 数组 0-7 管理服务配置数组
service_type 整数 0-6 服务类型
service_ipv4_acl 整数 2-198，0 0 表示取消配置 ipv4 的 acl
service_ipv6_acl 字符串 0-128 空字符串表示取消配置 ipv6 的 acl
ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向
mac_addr 字符串 MAC 地址
ipv4_addr Ipv4 address Ipv4 地址
ipv4_mask Ipv4 address Ipv4 掩码
ipv4_acl 整数 2-198 Ipv4 访问列表
ipv4_list 数组 0-16 Ipv4 地址列表
Ipv6_list 数组 0-16 Ipv6 地址列表
ipv6_addr Ipv6 address Ipv6 地址
ipv6_prefix 整数 1-128 Ipv6 前缀
ipv6_anycast 整数 0-1 Ipv6 多播
ipv6_local_auto 整数 0-1 Ipv6 自动配置
ipv6_local_addr Ipv6 address Ipv6 本地地址
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀
ipv6_local_anycast 整数 0-1 Ipv6 本地多播
ipv6_acl 字符串 0-15 Ipv6 访问列表
nat_dir 整数 0-3 Nat 方向
permit_wildcard 整数 0-1 混杂模式
grat_arp 整数 0-1 免费 ARP
no_vlan_forward 整数 0-1 禁止 VLAN 转发
icmp_rate_limit 整数 1-65535 ICMP 速率限制值
icmp_lock_up_rate 整数 1-65535 ICMP 锁定门限值
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期
响应举例：
 {
        "port_num": 1,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:B5:35",
        "permit_wildcard": 1,
        "grat_arp": 1,
        "nat_dir": 3,
        "ipv6_nat_dir": 3,
        "no_vlan_forward": "0",
        "icmp_rate_limit": 65535,
        "icmp_lock_up_rate": 65535,
        "icmp_lock_up_time": 16383,
        "ipv4_acl": 0,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [
            {
                "ipv4_addr": "171.1.1.1",
                "ipv4_mask": "255.255.255.0"
            }
        ],
        "ipv6_list": [
            {
                "ipv6_addr": "2000:171:1::1",
                "ipv6_prefix": 64,
                "ipv6_anycast": 0
            }
        ],
        "ipv6_local_auto": 1,
        "ipv6_acl": ""
    }
汇聚接口配置编辑
Action：interface.trunk.edit
请求参数：
名称 类型 范围 含义 必选 说明
port_num 整数 1-8 端口 是 对应 trunk 接口序号
status 整数 0-1 接口状态 否 0:disable;1:enable;缺省值:不修改
description 字符串 0-191 接口描述 否
management_services 数组 0-7 管理服务配置数组 否
service_type 整数 0-6 服务类型 是 0 表示 http
1 表示 https
2 表示 ping
3 表示 snmp
4 表示 ssh
5 表示 telnet
6 表示 acl
service_ipv4_acl 整数 2-198，0 配置 ipv4 的 acl 否 0 表示取消配置 ipv4 的 acl
service_ipv6_acl 字符串 0-191 配置 ipv6 的 acl 否
空字符串表示取消配置 ipv6 的 acl
ipv6_nat_dir 整数 0-3 IPv6 的 Nat 方向 否 0 表示没有配置；缺省值：不修改
1 表示 inside
2 表示 outside
3 表示 bidirection
ipv4_addr Ipv4 address Ipv4 地址 是
ipv4_mask Ipv4 address Ipv4 掩码 是
ipv4_acl 整数 2-198 Ipv4 访问列表 否 0 表示没有配置;缺省值:不修改
ipv4_list 数组 0-16 Ipv4 地址列表 否 空表示没有配置;缺省值:不修改
Ipv6_list 数组 0-16 Ipv6 地址列表 否 空表示没有配置;缺省值:不修改
ipv6_addr Ipv6 address Ipv6 地址 是 空表示没有配置;缺省值:不修改
ipv6_prefix 整数 1-128 Ipv6 前缀 是 0 表示没有配置;缺省值:不修改
ipv6_anycast 整数 0-1 Ipv6 多播 是 0:disable;1:enable;缺省值:不修改
ipv6_local_auto 整数 0-1 Ipv6 自动配置 否 0:disable;1:enable;缺省值:不修改
ipv6_local_addr Ipv6 address Ipv6 本地地址 否 空表示没有配置;缺省值:不修改
ipv6_local_prefix 整数 1-128 Ipv6 本地前缀 否 0 表示没有配置;缺省值:不修改
ipv6_local_anycast 整数 Ipv6 本地多播 否 0:disable;1:enable;缺省值:不修改
ipv6_acl 字符串 0-191 Ipv6 访问列表 否 0 表示没有配置;缺省值:不修改
nat_dir 整数 0-3 Nat 方向 否 0 表示没有配置
1 表示 inside
2 表示 outside
3 表示 bidirection
;缺省值:不修改
permit_wildcard 整数 0-1 混杂模式 否 0:disable;1:enable;缺省值:不修改
grat_arp 整数 0-1 免费 ARP 否 0:disable;1:enable;缺省值:不修改
no_vlan_forward 整数 0-1 禁止 VLAN 转发 否 0 表示关闭，1 表示开启
icmp_rate_limit 整数 1-65535 ICMP 速率限制值 否
icmp_lock_up_rate 整数 1-65535 ICMP 锁定门限值 否
icmp_lock_up_time 整数 1-16383 ICMP 锁定周期 否
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=interface.trunk.edit
请求 body：
{
        "port_num": 1,
        "description": "",
        "status": 1,
        "mac_addr": "00:0D:48:6D:B5:35",
        "permit_wildcard": 1,
        "grat_arp": 1,
        "nat_dir": 3,
        "ipv6_nat_dir": 3,
        "no_vlan_forward": "0",
        "icmp_rate_limit": 65535,
        "icmp_lock_up_rate": 65535,
        "icmp_lock_up_time": 16383,
        "ipv4_acl": 0,
        "management_services": [
            {
                "service_type": 2
            }
        ],
        "ipv4_list": [
            {
                "ipv4_addr": "171.1.1.1",
                "ipv4_mask": "255.255.255.0"
            }
        ],
        "ipv6_list": [
            {
                "ipv6_addr": "2000:171:1::1",
                "ipv6_prefix": 64,
                "ipv6_anycast": 0
            }
        ],
        "ipv6_local_auto": 1,
        "ipv6_acl": ""
    }

LLDP
LLDP 配置获取
Action：lldp.config.get
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=lldp.config.get
响应参数：
名称 类型 范围 含义
status 整数 0-1 0：关闭 1：开启
tx_hold 整数 2-10 消息保持倍数
tx_interva 整数 5-3600 消息发送周期
max_neighbors_per_port 整数 1-32 每接口最大邻居数
响应举例：
{
"status": 1,
"tx_hold": 2,
"tx_delay": 2,
"tx_interval": 5,
"reinit_delay": 2,
"max_neighbors_per_port": 1
}

LLDP 邻居查询
Action：lldp.neighbors.get
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=lldp.neighbors.get
响应参数：
名称 类型 范围 含义
local_name 整数 本地接口编号
ChassisID 字符串 对端接口 mac 地址
SysName 字符串 对端设备系统名称
MgmtIPv4 ipv4 address 管理口 Ipv4 地址
MgmtIPv6 ipv6 address 管理口 Ipv6 地址
PortID 字符串 对端接口 ID
PortDescr 字符串 对端物理接口描述
TTL 整数 存活时间
响应举例：
{
    "neighbors": [
        {
            "local_name": "Ethernet0/0",
            "ChassisID": "mac 00:0d:48:26:f2:94",
            "SysName": "dev-10.6.136.11",
            "MgmtIPv4": "10.6.136.11",
            "MgmtIPv6": "200a:0:0:1::1",
            "PortID": "local Ethernet0/0",
            "PortDescr": "Ethernet0/0",
            "TTL": "120"
        },
        {
            "local_name": "Ethernet0/2",
            "ChassisID": "mac 00:0d:48:26:f2:94",
            "SysName": "dev-10.6.136.11",
            "MgmtIPv4": "10.6.136.11",
            "MgmtIPv6": "200a:0:0:1::1",
            "PortID": "local Ethernet0/2",
            "PortDescr": "Ethernet0/2",
            "TTL": "120"
        }
    ]
}
LLDP 配置设置
Action：lldp.config.set
请求参数：无
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=lldp.config.set
请求参数：
名称 类型 范围 含义
status 整数 0-1 0：关闭 lldp 全局使能 1：开启 lldp 全局使能
tx_hold 整数 2-10 消息保持倍数
tx_interva 整数 5-3600 消息发送周期
max_neighbors_per_port 整数 1-32 每接口最大邻居数
请求举例：
{
"status": 1,
"tx_hold": 2,
"tx_interval": 5,
"max_neighbors_per_port": 1
}

VLAN
VLAN 配置列表
Action：network.vlan.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.vlan.list
响应参数：
名称 范围 类型 含义
id 1-4094 整数 VLANID
description 0-191 字符串 描述
l2_fwd_disable 0-1 整数 二层转发开关
path_persist 0-1 整数 路径保持
ve_if 0-1 整数 是否建立 ve 接口,0：disable，1：enable
slot 0-8 整数 槽位
port 0-7 整数 端口
tagged 0-1 整数 vlan 标签
trunk 1-8 整数 汇聚口
响应举例：
[{
        "id": 1,
        "description": "",
        "l2_fwd_disable": 1,
        "path_persist": 0,
        "ve_if": 0,
        "interface_list": [
            {
                "slot": 1,
                "port": 1,
                "tagged": 0
            },
            {
                "slot": 4,
                "port": 2,
                "tagged": 0
            },
            {
                "slot": 4,
                "port": 3,
                "tagged": 0
            },
            {
                "slot": 6,
                "port": 0,
                "tagged": 0
            },
            {
                "slot": 6,
                "port": 1,
                "tagged": 0
            },
            {
                "slot": 6,
                "port": 2,
                "tagged": 0
            },
            {
                "slot": 6,
                "port": 3,
                "tagged": 0
            },
            {
                "slot": 6,
                "port": 7,
                "tagged": 0
            }
        ],
        "trunk_list": [
            {
                "trunk": 1,
                "tagged": 0
            }
        ]
    },
    {
        "id": 1001,
        "description": "",
        "l2_fwd_disable": 1,
        "path_persist": 0,
        "ve_if": 1,
        "interface_list": [],
        "trunk_list": [
            {
                "trunk": 3,
                "tagged": 1
            }
        ]
}，
{
    "id": 1999,
    "description": "",
    "l2_fwd_disable": 1,
    "path_persist": 0,
    "ve_if": 1,
    "interface_list": [
        {
            "slot": 6,
            "port": 7,
            "tagged": 1
        }
    ],
    "trunk_list": [
        {
            "trunk": 2,
            "tagged": 1
        }
    ]
}]
VLAN 配置获取
Action：network.vlan.get
请求参数：
名称 类型 范围 含义 必选 备注
id 整数 2-4094 VLANID 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.vlan.get
请求 body：
{
"id": 1999
}
响应参数：
名称 范围 类型 含义
id 1-4094 整数 VLANID
description 0-191 字符串 描述
l2_fwd_disable 0-1 整数 二层转发开关
path_persist 0-1 整数 路径保持
ve_if 0-1 整数 是否建立 ve 接口
slot 0-8 整数 槽位
port 0-7 整数 端口
tagged 0-1 整数 vlan 标签
trunk 1-8 整数 汇聚口
响应举例：
{
    "id": 1999,
    "description": "",
    "l2_fwd_disable": 1,
    "path_persist": 0,
    "ve_if": 1,
    "interface_list": [
        {
            "slot": 6,
            "port": 7,
            "tagged": 1
        }
    ],
    "trunk_list": [
        {
            "trunk": 2,
            "tagged": 1
        }
    ]
}
VLAN 配置增加
Action：network.vlan.add
请求参数：
名称 范围 类型 含义 必选 备注
id 1-4094 整数 VLANID 是
description 0-63 字符串 描述 否
l2_fwd_disable 0-1 整数 二层转发开关 否 1 ： disable
0 ： enable
path_persist 0-1 整数 路径保持 否 0 ： disable
1 ： enable
ve_if 0-1 整数 是否开启 ve 接口 否 1 表示开启
0 表示关闭
slot 0-8 整数 槽位 是
port 0-7 整数 端口 是
tagged 0-1 整数 vlan 标签 是 1 表示打 vlan 标签
trunk 1-8 整数 汇聚口 否
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.vlan.add
请求 body：
{
"id": 100,
"description": "test",
"l2_fwd_disable": 1,
"path_persist": 0,
"mcast_limit": 5000,
"ve_if": 1,
"interface_list": [
        {
            "slot": 6,
            "port": 7,
            "tagged": 1
        }
    ],
    "trunk_list": [
        {
            "trunk": 2,
            "tagged": 1
        }
    ]

}
VLAN 配置编辑
Action：network.vlan.edit
请求参数：
名称 范围 类型 含义 必选 备注
id 1-4094 整数 VLANID 是
description 0-63 字符串 描述 否 缺省值:不修改
l2_fwd_disable 0-1 整数 二层转发开关 否 1:disable
0:enable
缺省值:不修改
path_persist 0-1 整数 路径保持 否 0 ： disable
1 ： enable
缺省值:0
ve_if 0-1 整数 是否建立 ve 接口 否 1 表示建立
缺省值:不修改
slot 0-255 整数 槽位 是
port 0-255 整数 端口 是
tagged 0-1 整数 vlan 标签 否 1 表示打 vlan 标签
缺省值:不修改
trunk 1-8 整数 汇聚口 否
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.vlan.edit
请求 body：
{
"id": 100,
"description": "test",
"l2_fwd_disable": 1,
"path_persist": 0,
"mcast_limit": 5000,
"ve_if": 1,
"interface_list": [
        {
            "slot": 6,
            "port": 6,
            "tagged": 1
        }
    ],
    "trunk_list": [
        {
            "trunk": 2,
            "tagged": 1
        }
  ]
}
VLAN 配置删除
Action：network.vlan.del
请求参数：
名称 类型 范围 含义 必选 备注
id 整数 2-4094 VLANID 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.vlan.del
请求 body：
{
"id": 100
}

汇聚(TRUNK)
TRUNK 配置列表
Action：network.trunk.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.trunk.list
响应参数：
名称 类型 范围 含义
id 整数 1-8 TRUNK id
type 整数 0-1 TRUNK 类型 0 静态 trunk， 1 动态 trunk（lacp）
status 整数 0-1 状态
slot 整数 0-8 接口插槽
port 整数 0-7 接口序号
enable 整数 0-1 Trunk 中接口的状态
mode 整数 0-1 接口模式
timeout 整数 0-1 超时模式
priority 整数 1-65535 接口优先级
interface_list 数组 trunk 成员接口列表
响应举例：
[{
"id": 1,
"type": 0,
"status": 1,
"interface_list": [{
"slot": 0,
"port": 2,
"enable": 0
}, {
"slot": 0,
"port": 3,
"enable": 1
}]
}, {
"id": 2,
"type": 1,
"status": 2,
"interface_list": [{
"slot": 0,
"port": 0,
"enable": 1,
"mode": 0,
"timeout": 0,
"priority": 32767
}, {
"slot": 0,
"port": 1,
"enable": 1,
"mode": 1,
"timeout": 1,
"priority": 32768
}]
}]
TRUNK 配置获取
Action：network.trunk.get
请求参数：
名称 类型 范围 含义 必选 备注
id 整数 1-8 TRUNK id 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.trunk.get
请求 body：
{
"id": 2
}
响应参数：
名称 类型 范围 含义
id 整数 1-8 TRUNK id
type 整数 0-1 TRUNK 类型 0 静态 trunk， 1 动态 trunk（lacp）
status 整数 0-1 状态
slot 整数 0-8 接口插槽
port 整数 0-7 接口序号
enable 整数 0-1 Trunk 中接口的状态
mode 整数 0-1 接口模式
timeout 整数 0-1 超时模式
priority 整数 1-65535 接口优先级
interface_list 数组 trunk 成员接口列表
响应举例：
{
"id": 2,
"type": 1,
"status": 1,
"interface_list": [{
"slot": 0,
"port": 0,
"enable": 1,
"mode": 0,
"timeout": 0,
"priority": 32767
}, {
"slot": 0,
"port": 1,
"enable": 1,
"mode": 1,
"timeout": 1,
"priority": 32768
}]
}
TRUNK 配置增加
Action：network.trunk.add
请求参数：
名称 类型 范围 含义 必选 说明
id 整数 1-8 TRUNK id 是
type 整数 0-1 TRUNK 类型 是 0 静态 trunk， 1 动态 trunk（lacp）
status 整数 0-1 状态 否 0: down 1:up
slot 整数 0-8 接口插槽 否
port 整数 0-7 接口序号 否
enable 整数 0-1 Trunk 中接口的状态 否 0: disable 1:enable
mode 整数 0-1 接口模式 否 0: passive 1：active
timeout 整数 0-1 超时模式 否 0：short 模式 1：long 模式
priority 整数 1-65535 接口优先级 否 默认 32768
interface_list 数组 trunk 成员接口列表 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.trunk.add
请求 body：
{
"id": 2,
"type": 1,
"interface_list": [{
"slot": 0,
"port": 0,
"enable": 1,
"mode": 0,
"timeout": 0,
"priority": 32766
}, {
"slot": 0,
"port": 1,
"enable": 1,
"mode": 0,
"timeout": 0,
"priority": 32765
}
]
}
TRUNK 配置编辑
Action：network.trunk.edit
请求参数：
名称 类型 范围 含义 必选 说明
id 整数 1-8 TRUNK id 是
type 整数 0-1 TRUNK 类型 是 0 静态 trunk， 1 动态 trunk（lacp）
status 整数 0-1 状态 否 0: down 1:up;缺省值:不修改
interface_list 数组 trunk 成员接口列表 是
slot 整数 0-8 接口插槽 是
port 整数 0-7 接口序号 是
enable 整数 0-1 Trunk 中接口的状态 否 0: disable 1:enable
mode 整数 0-1 接口模式 否 0: passive 1：active
timeout 整数 0-1 超时模式 否 0：short 模式 1：long 模式
priority 整数 1-65535 接口优先级 否 默认 32768
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.trunk.edit
请求 body：
{
"id": 2,
"type": 1,
"interface_list": [{
"slot": 0,
"port": 0,
"enable": 1,
"mode": 0,
"timeout": 0,
"priority": 32766
}, {
"slot": 0,
"port": 1,
"enable": 1,
"mode": 0,
"timeout": 0,
"priority": 32765
}
]
}
TRUNK 配置删除
Action：network.trunk.del
请求参数：
名称 类型 范围 含义 必选 备注
id 整数 1-8 TRUNK id 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.trunk.del
请求 body：
{
"id": 2
}

IPv4 标准访问列表
IPv4 标准访问列表列表
Action: acl.ipv4.std.list
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.std.list
响应参数:
名称 类型 范围 含义
description 字符串 0-191 访问列表描述
id 整数 2-99 访问列表号
item_list 列表 多个访问列表规则组成
访问列表规则：
名称 类型 范围 含义
sequence 整数 1-2000 访问列表号
acl_action 整数 0-2 匹配后动作 0：deny；1：permit；2：no-vlan-forward
sec_ip IP 地址 Ipv4 地址 源网络地址
sec_mask IP 掩码 Ipv4 掩码 源网络掩码
hits 整数 命中数
响应举例：
[{
"description": "",
"id": 3,
"item_list": [{
"sequence": 10,
"acl_action": 0,
"src_ip": "0.0.0.0",
"src_mask": "255.255.255.255",
"hits": "0"
}]
}]
IPv4 标准访问列表获取
Action: acl.ipv4.std.get
请求参数:
名称 类型 范围 含义 必选 备注
id 整数 2-99 访问列表号 是
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.std.get
请求 Body:
{
"id": 2
}
IPv4 标准访问列表增加
Action: acl.ipv4.std.item.add
请求参数:
名称 类型 范围 含义 必选 备注
id 整数 2-99 访问列表号 是
sequence 整数 1-2000 访问列表号 是
acl_action 整数 0-2 动作 否 缺省值：0，
0：deny；1：permit；2：no-vlan-forward
src_ip Ip 地址 Ipv4 地址 源网络地址 否 缺省值：0.0.0.0
src_mask Ip 掩码 Ipv4 掩码 源网络掩码 否 缺省值：255.255.255.255
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.std.item.add
请求 body：
{
"id": 3,
"sequence": 10,
"acl_action": 0,
"src_ip": "0.0.0.0",
"src_mask": "255.255.255.255"
}
IPv4 标准访问列表编辑
Action: acl.ipv4.std.item.edit
请求参数:
名称 类型 范围 含义 必选 备注
id 整数 2-99 访问列表号 是
sequence 整数 1-2000 访问列表号 是
acl_action 整数 0-2 动作 否 缺省值：0
0：deny；1：permit；2：no-vlan-forward
src_ip IP 地址 Ipv4 地址 源网络地址 否 缺省值：不修改
src_mask Ip 掩码 Ipv4 掩码 源网络掩码 否 缺省值：不修改
请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.std.item.edit
请求 body：
{
"id": 3,
"sequence": 10,
"acl_action": 0,
"src_ip": "0.0.0.0",
"src_mask": "255.255.255.255"
}
IPv4 标准访问列表删除
Action: acl.ipv4.std.item.del
请求参数:
名称 类型 范围 含义 必选 备注
id 整数 2-99 访问列表号 是
sequence 整数 1-2000 访问列表号 否 如果"sequence"缺失，删除所有表项
请求举例:
POST
http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.std.item.del
请求 body：
{
"id": 2,
"sequence": 2
}
IPv4 标准访问列表描述设置
Action: acl.ipv4.std.desc.set
请求参数:
名称 类型 范围 含义 必选 备注
id 整数 2-99 访问列表号 是
description 字符串 0-191 访问列表描述 是
请求举例:
post http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.std.desc.set
请求 body:
{
"id": "2",
"description": "adc"
}
IPv4 扩展访问列表
IPv4 扩展访问列表列表
Action: acl.ipv4.ext.list
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.ext.list
响应参数：
名称 类型 范围 含义
description 字符串 0-191 访问列表描述
id 整数 100-198 访问列表号
Item_list 列表 访问控制列表
访问控制列表：
名称 类型 范围 含义
sequence 整数 1-2000 访问列表号
acl_action 整数 0-2 动作 0：deny；1：permit；2：no-vlan-forward
protocol 整数 0-17 协议
src_ip Ip 地址 Ipv4 地址 源网络地址
icmp_type 整数 0-254 Icmp 报文类型
icmp_code 整数 0-254 Icmp code 码
src_port_min 整数 1-65535 源端口最小值
src_port_max 整数 1-65535 源端口最大值
src_mask Ip 地址 Ipv4 掩码 源网络掩码
dst_ip Ip 地址 Ipv4 地址 目的网络地址
dst_mask Ip 地址 Ipv4 掩码 目的网络掩码
dst_port_min 整数 1-65535 目的端口最小值
dst_port_max 整数 1-65535 目的端口最大值
ip_fragments 整数 0-1 IP 分片
vlan_id 整数 1-4094 vlan id
dscp 整数 1-63 DSCP 值
tcp_established 整数 0-1 TCP 会话建立
description 整数 1-191 访问列表描述
timerange 字符串 1-191 时间对象
hits 整数 命中数
响应举例：
[{
"description": "ip",
"id": 100,
"item_list": [{
"sequence": 20,
"acl_action": 1,
"protocol": 0,
"src_ip": "2.0.0.0",
"src_mask": "0.255.255.255",
"dst_ip": "0.0.0.0",
"dst_mask": "255.255.255.255",
"ip_fragments": 1,
"vlan_id": 2,
"dscp": 1,
"hits": "0"
}]
}]
IPv4 扩展访问列表获取
Action: acl.ipv4.ext.get
请求参数:
名称 类型 范围 含义 必选 备注
id 整数 100-198 访问列表号 是

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.ext.get
{
"id": 100
}

响应参数：
名称 类型 范围 含义
description 字符串 0-191 访问列表描述
id 整数 100-198 访问列表号
Item_list 列表 访问控制列表
访问控制列表：
名称 类型 范围 含义
sequence 整数 1-2000 访问列表号
acl_action 整数 0-2 动作 0：deny；1：permit；2：no-vlan-forward
protocol 整数 0-17 协议
src_ip Ip 地址 Ipv4 地址 源网络地址
icmp_type 整数 0-254 Icmp 报文类型
icmp_code 整数 0-254 Icmp code 码
src_port_min 整数 1-65535 源端口最小值
src_port_max 整数 1-65535 源端口最大值
src_mask Ip 地址 Ipv4 掩码 源网络掩码
dst_ip Ip 地址 Ipv4 地址 目的网络地址
dst_mask Ip 地址 Ipv4 掩码 目的网络掩码
dst_port_min 整数 1-65535 目的端口最小值
dst_port_max 整数 1-65535 目的端口最大值
ip_fragments 整数 0-1 IP 分片
vlan_id 整数 1-4094 vlan id
dscp 整数 1-63 DSCP 值
tcp_established 整数 0-1 TCP 会话建立
description 整数 1-191 访问列表描述
timerange 字符串 1-191 时间对象
hits 整数 命中数
响应举例：
{
"description": "ip",
"id": 100,
"item_list": [{
"sequence": 20,
"acl_action": 1,
"protocol": 0,
"src_ip": "2.0.0.0",
"src_mask": "0.255.255.255",
"dst_ip": "0.0.0.0",
"dst_mask": "255.255.255.255",
"ip_fragments": 1,
"vlan_id": 2,
"dscp": 1,
"hits": "0"
}]
}
IPv4 扩展访问列表增加
Action: acl.ipv4.ext.item.add
请求参数:
名称 类型 范围 含义 必选 备注
description 字符串 1-191 访问列表描述 否
id 整数 100-198 访问列表号 是
sequence 整数 1-2000 访问列表号 是
acl_action 整数 0-2 动作 否 动作 0：deny；1：permit；2：no-vlan-forward
protocol 整数 0/1/6/17 协议 否 0：ip；1：icmp；6：tcp；17:udp
src_ip Ip 地址 Ipv4 地址 源网络地址 否 缺省值："0.0.0.0"
全 0 表示匹配任何地址
src_mask Ip 地址 Ipv4 地址 源网络掩码 否 缺省值："255.255.255.255"
反掩码：全 1 表示匹配任何地址，全 0 表示主机地址
icmp_type 整数 0-254 Icmp 报文类型 否 协议 protocol 是 ICMP 的时候，才有效
icmp_code 整数 0-254 Icmp code 码 否 协议 protocol 是 ICMP 的时候，才有效
src_port_min 整数 1-65535 源端口最小值 否 协议 protocol 是 TCP/UDP 的时候，才有效
src_port_max 整数 1-65535 源端口最大值 否 协议 protocol 是 TCP/UDP 的时候，才有效
dst_ip Ip 地址 Ipv4 地址 目的网络地址 否 缺省值："0.0.0.0"
全 0 表示匹配任何地址
dst_mask Ip 地址 Ipv4 掩码 目的网络掩码 否 缺省值："255.255.255.255"
反掩码：全 1 表示匹配任何地址，全 0 表示主机地址
dst_port_min 整数 1-65535 目的端口最小值 否 协议 protocol 是 TCP/UDP 的时候，才有效
dst_port_max 整数 1-65535 目的端口最大值 否 协议 protocol 是 TCP/UDP 的时候，才有效
ip_fragments 整数 0-1 IP 分片 否
vlan_id 整数 1-4094 vlan id 否
dscp 整数 1-63 DSCP 值 否
tcp_established 整数 0-1 TCP 会话建立 否 协议 protocol 是 TCP 的时候，才有效
description 整数 1-191 访问列表描述 否
timerange 字符串 1-191 时间对象 否
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.ext.item.add
请求 body:
{
"description": "ip",
"id": 100,
"sequence": 20,
"acl_action": 1,
"protocol": 0,
"src_ip": "2.0.0.0",
"src_mask": "0.255.255.255",
"dst_ip": "0.0.0.0",
"dst_mask": "255.255.255.255",
"ip_fragments": 1,
"vlan_id": 2,
"dscp": 1
}
IPv4 扩展访问列表编辑
Action: acl.ipv4.ext.item.edit
请求参数：
名称 类型 范围 含义 必选 备注
description 字符串 1-191 访问列表描述 否
id 整数 100-198 访问列表号 是
sequence 整数 1-2000 访问列表号 是
acl_action 整数 0-2 动作 否 动作 0：deny；1：permit；2：no-vlan-forward
protocol 整数 0-17 协议 否
src_ip Ip 地址 Ipv4 地址 源网络地址 否 缺省值："0.0.0.0"
全 0 表示匹配任何地址
src_mask Ip 地址 Ipv4 地址 源网络掩码 否 缺省值："255.255.255.255"
反掩码：全 1 表示匹配任何地址，全 0 表示主机地址
icmp_type 整数 0-254 Icmp 报文类型 否 协议 protocol 是 ICMP 的时候，才有效
icmp_code 整数 0-254 Icmp code 码 否 协议 protocol 是 ICMP 的时候，才有效
src_port_min 整数 1-65535 源端口最小值 否 协议 protocol 是 TCP/UDP 的时候，才有效
src_port_max 整数 1-65535 源端口最大值 否 协议 protocol 是 TCP/UDP 的时候，才有效
dst_ip Ip 地址 Ipv4 地址 目的网络地址 否 缺省值："0.0.0.0"
全 0 表示匹配任何地址
dst_mask Ip 地址 Ipv4 掩码 目的网络掩码 否 缺省值："255.255.255.255"
反掩码：全 1 表示匹配任何地址，全 0 表示主机地址
dst_port_min 整数 1-65535 目的端口最小值 否 协议 protocol 是 TCP/UDP 的时候，才有效
dst_port_max 整数 1-65535 目的端口最大值 否 协议 protocol 是 TCP/UDP 的时候，才有效
ip_fragments 整数 0-1 IP 分片 否
vlan_id 整数 1-4094 vlan id 否
dscp 整数 1-63 DSCP 值 否
tcp_established 整数 0-1 TCP 会话建立 否 协议 protocol 是 TCP 的时候，才有效
description 整数 1-191 访问列表描述 否
timerange 字符串 1-191 时间对象 否
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.ext.item.edit
请求 body：
{
"description": "ip",
"id": 100,
"sequence": 20,
"acl_action": 1,
"protocol": 0,
"src_ip": "2.0.0.0",
"src_mask": "0.255.255.255",
"dst_ip": "0.0.0.0",
"dst_mask": "255.255.255.255",
"ip_fragments": 1,
"vlan_id": 2,
"dscp": 1
}
IPv4 扩展访问列表删除
Action: acl.ipv4.ext.item.del
请求参数：
名称 类型 范围 含义 必选 备注
id 整数 100-198 访问列表号 是
sequence 整数 1-2000 访问列表号 是 如果"sequence"缺失，删除所有表项；
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.ext.item.del
请求 body：
{
"id": 100,
"sequence": 20
}
IPv4 扩展访问列表描述设置
Action: acl.ipv4.ext.desc.set
请求参数：
名称 类型 范围 含义 必选 备注
id 整数 100-198 访问列表号 是
description 字符串 0-191 访问列表描述 是
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv4.ext.desc.set
请求 body：
{
"id": 100,
"description": "adc"
}

IPv6 访问列表
IPv6 访问列表列表
Action: acl.ipv6.ext.list
请求参数:无
请求举例：
GET http://10.2.20.35/adcapi/v2.0/?authkey=a209da70aa9e6dcdca81bb93c59cf0&action=acl.ipv6.ext.list
响应参数:

名称 类型 范围 含义
description 字符串 0-191 IPV6 访问列表描述
name 字符串 长度 1-191 IPV6 访问列表名
item_list 列表 多个访问列表规则组成
访问列表规则：
名称 类型 范围 含义
sequence 整数 1-2000 访问列表号
acl_action 整数 0-2 匹配后动作 0：deny；1：permit；2：no-vlan-forward
src_ip ipv6 地址 IpV6 地址 源网络地址
src_mask 整数 1-128 源网络掩码
hits 字符串 命中数
protocol 整数 协议类型，UDP:17；IPV6:41；ICMP:58；TCP:6
ip_fragments 整数 0-1 IP 分片；0：关闭；1：开启
dst_ip ipv6 地址 IPV6 地址 目的网络地址
dst_mask 整数 1-128 目的网络掩码
src_port_min 整数 1-65535 源端口最小值
src_port_max 整数 1-65535 源端口最大值
dst_port_min 整数 1-65535 目的端口最小值
dst_port_max 整数 1-65535 目的端口最大值
ip_fragments 整数 0-1 IP 分片
vlan_id 整数 1-4094 vlan id
dscp 整数 1-63 DSCP 值
tcp_established 整数 0-1 TCP 会话建立
description 整数 1-191 IPV6 访问列表描述
响应举例：
[
{
"description": "",
"name": "ipv6-acl",
"item_list": [
{
"sequence": 222,
"acl_action": 0,
"protocol": 6,
"src_ip": "::",
"src_mask": 0,
"src_port_min": 1,
"src_port_max": 65535,
"dst_ip": "::",
"dst_mask": 0,
"dst_port_min": 1,
"dst_port_max": 65535,
"ip_fragments": 1,
"tcp_established": 0,
"hits": "0"
}
]
}
]
IPv6 访问列表获取
Action: acl.ipv6.ext.get
请求参数:
名称 类型 范围 含义 必选 备注
name 字符串 长度 1-191 IPV6 访问列表名 是
请求举例：
POST http://10.2.20.35/adcapi/v2.0/?authkey={{authkey}}&action=acl.ipv6.ext.get
请求 Body:
{
"name":"ipv6-acl"
}
IPv6 访问列表增加
Action: acl.ipv6.ext.item.add
请求参数:
名称 类型 范围 含义 必选 备注
description 字符串 0-191 IPV6 访问列表描述 否
name 字符串 长度 1-191 IPV6 访问列表名 是
sequence 整数 1-2000 访问列表号 是
acl_action 整数 0-2 匹配后动作 否 动作 0：deny；1：permit；2：no-vlan-forward
src_ip 字符串 IpV6 地址 源网络地址 否
src_mask 整数 Ipv6 掩码 源网络掩码 否
protocol 整数 协议类型 否 UDP:17；IPV6:41；ICMP:58；TCP:6
ip_fragments 整数 0-1 IP 分片；0：关闭；1：开启 否 0：关闭；1：开启
dst_ip 字符串 IpV6 地址 目的网络地址 否
dst_mask 整数 Ipv6 掩码 目的网络掩码 否
src_port_min 整数 1-65535 源端口最小值 否 协议 protocol 是 TCP/UDP 的时候，才有效
src_port_max 整数 1-65535 源端口最大值 否 协议 protocol 是 TCP/UDP 的时候，才有效
dst_port_min 整数 1-65535 目的端口最小值 否 协议 protocol 是 TCP/UDP 的时候，才有效
dst_port_max 整数 1-65535 目的端口最大值 否 协议 protocol 是 TCP/UDP 的时候，才有效
ip_fragments 整数 0-1 IP 分片 否
vlan_id 整数 1-4094 vlan id 否
dscp 整数 1-63 DSCP 值 否
tcp_established 整数 0-1 TCP 会话建立 否 协议 protocol 是 TCP 的时候，才有效
description 整数 1-191 访问列表描述 否

请求举例：
POST http://10.2.20.35/adcapi/v2.0/?authkey={{authkey}}&action=acl.ipv6.ext.item.add
请求 body：
{
"name": "ipv6-acl",
"sequence": 222,
"acl_action": 0,
"protocol": 17,
"src_ip": "::",
"src_mask": 0,
"src_port_min": 1,
"src_port_max": 65535,
"dst_ip": "::",
"dst_mask": 0,
"dst_port_min": 1,
"dst_port_max": 65535,
"ip_fragments": 0,
"hits": "0"
}
IPv6 访问列表编辑
Action: acl.ipv6.ext.item.edit
请求参数:
名称 类型 范围 含义 必选 备注
name 字符串 长度 1-191 IPV6 访问列表名 是
description 字符串 0-191 访问列表描述 是
sequence 整数 1-2000 访问列表号 是
acl_action 整数 0-2 匹配后动作 否 动作 0：deny；1：permit；2：no-vlan-forward
src_ip 字符串 IpV6 地址 源网络地址 否
src_mask 整数 Ipv6 掩码 源网络掩码 否
protocol 整数 协议类型 否 UDP:17；IPV6:41；ICMP:58；TCP:6
ip_fragments 整数 0-1 IP 分片；0：关闭；1：开启 否 0：关闭；1：开启
dst_ip 字符串 IpV6 地址 目的网络地址 否
dst_mask 整数 Ipv6 掩码 目的网络掩码 否
src_port_min 整数 1-65535 源端口最小值 否 协议 protocol 是 TCP/UDP 的时候，才有效
src_port_max 整数 1-65535 源端口最大值 否 协议 protocol 是 TCP/UDP 的时候，才有效
dst_port_min 整数 1-65535 目的端口最小值 否 协议 protocol 是 TCP/UDP 的时候，才有效
dst_port_max 整数 1-65535 目的端口最大值 否 协议 protocol 是 TCP/UDP 的时候，才有效
ip_fragments 整数 0-1 IP 分片 否
vlan_id 整数 1-4094 vlan id 否
dscp 整数 1-63 DSCP 值 否
tcp_established 整数 0-1 TCP 会话建立 否 协议 protocol 是 TCP 的时候，才有效
description 整数 1-191 访问列表描述 否

请求举例:
POST http://10.2.20.35/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv6.ext.item.edit
请求 body：
{
"description": "",
"name": "ipv6-acl",
"sequence": 222,
"acl_action": 0,
"protocol": 17,
"src_ip": "::",
"src_mask": 0,
"src_port_min": 1,
"src_port_max": 65535,
"dst_ip": "::",
"dst_mask": 0,
"dst_port_min": 1,
"dst_port_max": 65535,
"ip_fragments": 0

}
IPv6 访问列表删除
Action: acl.ipv6.ext.item.del
请求参数:
名称 类型 范围 含义 必选 备注
name 字符串 长度 1-191 IPV6 访问列表名 是
sequence 整数 1-2000 访问列表号 是
请求举例:
POST
http://10.2.20.35/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv6.ext.item.del
请求 body：
{
"name":"ipv6-acl",
"sequence": 2
}
IPv6 访问列表描述设置
Action: acl.ipv6.ext.desc.set
请求参数:

名称 类型 范围 含义 必选 备注
name 字符串 长度 1-191 IPV6 访问列表名 是
description 字符串 0-191 访问列表描述 是
请求举例:
post http://10.2.20.35/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=acl.ipv6.ext.desc.set
请求 body:
{
"name": "ipv6-acl",
"description": "5555"
}
时间对象
时间对象配置列表
Action：system.timerange.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=system.timerange.list
响应参数：
名称 类型 范围 含义
name 字符串 1-191 时间对象名字
type 整数 0-2 时间类型
day_list 整数 0-6
1-31 天列表
time_list 时间列表
start 整数 0-86400 开始时间
end 整数 0-86400 结束时间
响应举例：
[{
"name": "daytest",
"type": 0,
"time_list": [{
"start": 0,
"end": 10800
}, {
"start": 14400,
"end": 14400
}, {
"start": 18000,
"end": 21600
}, {
"start": 43200,
"end": 86400
}]
}, {
"name": "weektest",
"type": 1,
"day_list": [0, 2, 3, 4, 5, 6],
"time_list": [{
"start": 3600,
"end": 10800
}, {
"start": 10800,
"end": 18000
}]
}, {
"name": "montest",
"type": 2,
"day_list": [1, 3, 4, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31],
"time_list": [{
"start": 3600,
"end": 10800
}, {
"start": 18000,
"end": 28800
}]
}]
时间对象配置获取
Action：system.timerange.get
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 时间对象名字 是 key
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=system.timerange.get
请求 body：
{
"name": "weektest"
}
响应参数：
名称 类型 范围 含义
name 字符串 1-191 时间对象名字
type 整数 0-2 时间类型
day_list 整数 0-6
1-31 天列表
time_list 时间列表
start 整数 0-86400 开始时间
end 整数 0-86400 结束时间
响应举例：
{
"name": "weektest",
"type": 1,
"day_list": [0, 2, 3, 4, 5, 6],
"time_list": [{
"start": 3600,
"end": 10800
}, {
"start": 10800,
"end": 18000
}]
时间对象配置增加
Action：system.timerange.add
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 时间对象名字 是 key
type 整数 0-2 时间类型 是 0：每天 1：每周 2： 每月
day_list 整数 0-6
1-31 天列表 是 如果 type=1，列表值 0-6，表示周日到周六
如果 type=2，列表值 1-31，表示 1 号到 31 号
time_list 时间列表 一天的时间段
start 整数 0-86400 开始时间 是 必须 3600 整数倍
end 整数 0-86400 结束时间 是 必须 3600 整数倍
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=system.timerange.add
请求 body：
{
"name": "weektest",
"type": 1,
"day_list": [0, 3, 4, 6],
"time_list": [{
"start": 3600,
"end": 10800
}, {
"start": 10800,
"end": 18000
}]
}
时间对象配置编辑
Action：system.timerange.edit
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 时间对象名字 是 key
type 整数 0-2 时间类型 是 0：每天 1：每周 2： 每月
day_list 整数 0-6
1-31 天列表 是 如果 type=1，列表值 0-6，表示周日到周六
如果 type=2，列表值 1-31，表示 1 号到 31 号
time_list 时间列表 一天的时间段
start 整数 0-86400 开始时间 是 必须 3600 整数倍
end 整数 0-86400 结束时间 是 必须 3600 整数倍
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=system.timerange.edit
请求 body：
{
"name": "weektest",
"type": 1,
"day_list": [0, 3, 4, 6],
"time_list": [{
"start": 3600,
"end": 10800
}, {
"start": 10800,
"end": 18000
}]
}
时间对象配置删除
Action：system.timerange.del
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 时间对象名字 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=system.timerange.del
请求 body：
{
"name": "weektest"
}

端口列表模板
端口列表模板列表
Action: port-list.profile.list
请求参数:无
请求举例：
GET http://10.2.20.35/adcapi/v2.0/?authkey=a209da70aa9e6dcdca81bb93c59cf0&action=port-list.profile.list
响应参数:

名称 类型 范围 含义
name 字符串 长度 1-191 端口列表模板名
port
端口 2048-65533 端口范围
start_port 端口 2048-65533 开始端口范围
end_port 端口 2048-65533 结束端口范围
响应举例：
{
    "port-list_profile": [
        {
            "name": "port_list_1",
            "port": [
                {
                    "start_port": 2548,
                    "end_port": 5500
                },
                {
                    "start_port": 2549,
                    "end_port": 5501
                }
            ]
        }
    ],
    "total": 1
}
端口列表模板获取
Action: port-list.profile.get
请求参数:
名称 类型 范围 含义
name 字符串 长度 1-191 端口列表模板名
请求举例：
GET http://10.2.20.35/adcapi/v2.0/?authkey=a209da70aa9e6dcdca81bb93c59cf0&action=port-list.profile.get
请求 body：
{
"name": "port_list_1"
}
响应参数:
名称 类型 范围 含义
name 字符串 长度 1-191 端口列表模板名
port
端口 2048-65533 端口范围
start_port 端口 2048-65533 开始端口范围
end_port 端口 2048-65533 结束端口范围

响应举例：
{
    "port-list_profile": [
        {
            "name": "port_list_1",
            "port": [
                {
                    "start_port": 2548,
                    "end_port": 5500
                },
                {
                    "start_port": 2549,
                    "end_port": 5501
                }
            ]
        }
    ],
    "total": 1
}

端口列表模板增加
Action: port-list.profile.add
请求参数:
名称 类型 范围 含义
name 字符串 长度 1-191 端口列表模板名
port
端口 2048-65533 端口范围:
start_port:开始端口范围 2048-65533
end_port:结束端口范围 2048-65533

请求举例：
POST http://10.2.20.35/adcapi/v2.0/?authkey=a209da70aa9e6dcdca81bb93c59cf0&action=port-list.profile.add
请求 body：
{
"name": "port_list_2",
"port": [
{
"start_port": 10001,
"end_port": 10002

                }
            ]
        }

端口列表模板增加明细条目
Action: port-list.profile.item.add
请求举例：
GET http://10.2.20.35/adcapi/v2.0/?authkey=a209da70aa9e6dcdca81bb93c59cf0&action=port-list.profile.item.add
请求参数：
名称 类型 范围 含义
name 字符串 长度 1-191 端口列表模板名
start_port 端口 2048-65533 开始端口范围
end_port 端口 2048-65533 结束端口范围

请求 body:
{
"name":"port_list_2",
"start_port":2048,
"end_port":60002
}
端口列表模板编辑
Action: port-list.profile.edit
请求参数:
名称 类型 范围 含义
name 字符串 长度 1-191 端口列表模板名
port
端口 2048-65533 端口范围
start_port:开始端口范围 2048-65533
end_port:结束端口范围 2048-65533

请求举例：
POST http://10.2.20.35/adcapi/v2.0/?authkey=a209da70aa9e6dcdca81bb93c59cf0&action=port-list.profile.edit
请求 body:
{
    "name": "port_list_2",
    "port": [
        {
            "start_port": 2548,
            "end_port": 5500
        },
        {
            "start_port": 2549,
            "end_port": 5501
        }
    ]
}
端口列表模板删除
Action: port-list.profile.del
请求参数:
名称 类型 范围 含义
name 字符串 长度 1-191 端口列表模板名

请求举例：
POST http://10.2.20.35/adcapi/v2.0/?authkey=a209da70aa9e6dcdca81bb93c59cf0&action=port-list.profile.del
请求 body：
{"name": "port_list_1"}
端口列表模板删除明细条目
Action: port-list.profile.edit
请求参数:
名称 类型 范围 含义
name 字符串 长度 1-191 端口列表模板名
start_port 端口 2048-65533 开始端口范围
end_port 端口 2048-65533 结束端口范围

请求举例：
POST http://10.2.20.35/adcapi/v2.0/?authkey=a209da70aa9e6dcdca81bb93c59cf0&action=port-list.profile.item.del
请求 body：
{
"name":"p1",
"start_port":2048,
"end_port":60002
}

NAT 地址转换
NAT 地址池
NAT 地址池列表
Action：nat.pool.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool.list
响应参数：
名称 类型 范围 含义
name 字符串 1-191 地址池名字
ip_type 整数 0-1 0:IPv4, 1:IPv6
global_gateway IPv4 网关 IP 地址
vrid 整数 0-8 VRRP 的 ID
ip_rr 整数 0-1 IP 选择轮询开关
member_list 数组 地址池成员列表
description 字符串 1-191 描述
start_ip_addr IPv4/IPv6 地址池成员起始 IP 地址
end_ip_addr IPv4/IPv6 地址池成员结束 IP 地址
netmask IPv4 掩码/IPv6 前缀长度 地址池成员掩码(IPv4)或前缀长度(IPv6)
gateway IPv4/IPv6 地址池成员网关 IP 地址
ipv6_global_gateway IPV6 网关 IPV6 地址
ipv6_member_list 数组 地址池成员列表
响应举例：
[
    {
        "name": "snat-pool",
        "ip_type": 0,
        "vrid": 0,
"description": "23",
        "ip_rr": 0,
        "global_gateway": "",
        "member_list": [
            {
                "start_ip_addr": "1.1.1.20",
                "end_ip_addr": "1.1.1.200",
                "netmask": "255.255.255.0",
                "gateway": ""
            }
        ],
        "ipv6_global_gateway": "",
        "ipv6_member_list": []
    },
    {
        "name": "1010:1::\_64",
        "ip_type": 0,
        "vrid": 0,
        "ip_rr": 0,
        "global_gateway": "",
        "member_list": [],
        "ipv6_global_gateway": "",
        "ipv6_member_list": []
    },
    {
        "name": "2.1.1.0_24",
        "ip_type": 0,
        "vrid": 0,
        "ip_rr": 0,
        "global_gateway": "",
        "member_list": [
            {
                "start_ip_addr": "2.1.1.20",
                "end_ip_addr": "2.1.1.200",
                "netmask": "255.255.255.0",
                "gateway": ""
            }
        ],
        "ipv6_global_gateway": "",
        "ipv6_member_list": []
    },
    {
        "name": "snatpool",
        "ip_type": 0,
        "vrid": 0,
        "ip_rr": 0,
        "global_gateway": "",
        "member_list": [
            {
                "start_ip_addr": "2.2.2.2",
                "end_ip_addr": "2.2.2.2",
                "netmask": "255.255.255.0",
                "gateway": ""
            }
        ],
        "ipv6_global_gateway": "",
        "ipv6_member_list": [
            {
                "start_ip_addr": "2020::1",
                "end_ip_addr": "2020::100",
                "netmask": "64",
                "gateway": ""
            }
        ]
    }
]
NAT 地址池获取
Action：nat.pool.get
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 地址池名字 是
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool.get
请求 body：
{
"name" : "ipv4pool"
}
响应参数：
名称 类型 范围 含义
name 字符串 1-191 地址池名字
ip_type 整数 0-1 0:IPv4, 1:IPv6
global_gateway IPv4 地址池全局网关 IP 地址
vrid 整数 0-8 VRRP 的 ID
ip_rr 整数 0-1 IP 选择轮询开关
member_list 数组 地址池成员列表
start_ip_addr IPv4/IPv6 地址池成员起始 IP 地址
end_ip_addr IPv4/IPv6 地址池成员结束 IP 地址
netmask IPv4 掩码/IPv6 前缀长度 地址池成员掩码(IPv4)或前缀长度(IPv6)
gateway IPv4/IPv6 地址池成员网关 IP 地址
description 字符串 1-191 描述
ipv6_global_gateway IPv6 地址池全局网关 IPv6 地址
ipv6_member_list 数组 地址池成员列表
响应举例：
{
    "pool": {
        "name": "snatpool",
        "ip_type": 0,
        "vrid": 0,
        "ip_rr": 0,
"description": "23",
        "global_gateway": "",
        "member_list": [
            {
                "start_ip_addr": "2.2.2.2",
                "end_ip_addr": "2.2.2.2",
                "netmask": "255.255.255.0",
                "gateway": ""
            }
        ],
        "ipv6_global_gateway": "",
        "ipv6_member_list": [
            {
                "start_ip_addr": "2020::1",
                "end_ip_addr": "2020::100",
                "netmask": "64",
                "gateway": ""
            }
        ]
    }
}
NAT 地址池增加
Action：nat.pool.add
请求参数：
名称 类型 范围 含义 必选 备注
pool object 地址池对象 是
name 字符串 1-191 地址池名字 是 地址池名字
ip_type 整数 0-1 0:IPv4, 1:IPv6 否 缺省为 0
global_gateway IPv4 地址池全局网关 IP 地址 否 缺省为空
vrid 整数 0-8 VRRP 的 ID 否 缺省为 0
ip_rr 整数 0-1 IP 选择轮询开关 否 0 表示关，1 表示开,缺省为 0
member_list 数组 地址池成员列表 否 缺省为空
start_ip_addr IPv4/IPv6 地址池成员起始 IP 地址 是
end_ip_addr IPv4/IPv6 地址池成员结束 IP 地址 是
netmask IPv4 掩码/IPv6 前缀长度 地址池成员掩码(IPv4)或前缀长度(IPv6) 是
gateway IPv4/IPv6 地址池成员网关 IP 地址 否 缺省为空
description 字符串 描述 否
ipv6_member_list 数组 地址池 IPV6 地址成员列表 否 缺省为空
ipv6_global_gateway IPv6 地址池全局网关 IPV6 地址 否 缺省为 0
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool.add
请求 body：
{
    "pool": {
        "name": "snatpool",
        "ip_type": 0,
        "vrid": 0,
        "ip_rr": 0,
"description": "23",
        "global_gateway": "",
        "member_list": [
            {
                "start_ip_addr": "2.2.2.2",
                "end_ip_addr": "2.2.2.2",
                "netmask": "255.255.255.0",
                "gateway": ""
            }
        ],
        "ipv6_global_gateway": "",
        "ipv6_member_list": [
            {
                "start_ip_addr": "2020::1",
                "end_ip_addr": "2020::100",
                "netmask": "64",
                "gateway": ""
            }
        ]
    }
}

NAT 地址池编辑
Action：nat.pool.edit
请求参数：
名称 类型 范围 含义 必选 备注
pool object 地址池对象 是
name 字符串 1-191 地址池名字 是 地址池名字
ip_type 整数 0-1 0:IPv4, 1:IPv6 否 缺省为不改变
global_gateway IPv4 地址池全局网关 IP 地址 否 缺省为不改变
vrid 整数 0-8 VRRP 的 ID 否 缺省为不改变
ip_rr 整数 0-1 IP 选择轮询开关 否 0 表示关，1 表示开,缺省为不改变
member_list 数组 地址池成员列表 否 缺省为不改变
start_ip_addr IPv4/IPv6 地址池成员起始 IP 地址 是
end_ip_addr IPv4/IPv6 地址池成员结束 IP 地址 是
netmask IPv4 掩码/IPv6 前缀长度 地址池成员掩码(IPv4)或前缀长度(IPv6) 是
gateway IPv4/IPv6 地址池成员网关 IP 地址 否 缺省为空
description 字符串 0-191 描述 否 缺省为空
ipv6_member_list 数组 地址池成员列表 否 缺省为不改变
ipv6_global_gateway IPv6 地址池全局网关 IPV6 地址 否 缺省为不改变
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool.edit
请求 body：
{
    "pool": {
        "name": "snatpool",
        "ip_type": 0,
        "vrid": 0,
        "ip_rr": 0,
"description": "23",
        "global_gateway": "",
        "member_list": [
            {
                "start_ip_addr": "2.2.2.2",
                "end_ip_addr": "2.2.2.2",
                "netmask": "255.255.255.0",
                "gateway": ""
            }
        ],
        "ipv6_global_gateway": "",
        "ipv6_member_list": [
            {
                "start_ip_addr": "2020::1",
                "end_ip_addr": "2020::100",
                "netmask": "64",
                "gateway": ""
            }
        ]
    }
}
NAT 地址池删除
Action：nat.pool.del
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 地址池名字 是 地址池名字
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool.del
请求 body：
{
"name":"snatpool"
}

NAT 地址池统计信息
NAT 地址池统计信息列表
Action：nat.pool.stats.list
请求参数：
名称 类型 范围 含义 必选 备注
ip_type 整数 0-1 0:IPv4, 1:IPv6 否 缺省为 0
start 整数 0-99999 开始返回数据的编号 否 缺省为 0
limit 整数 0-99999 最多返回数据的条数 否 缺省为 30；0 表示不限制
searchbk 字符串 0-127 过滤条件表达式 否 可选，默认""

请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool.stats.list
响应参数：
名称 类型 范围 含义
pool_num 整数 0-99999 地址池的数量（总数)
match_num 整数 0-99999 匹配过滤条件的数量
limit_num 整数 0-99999 限制返回的数量
total 整数 0-99999 地址池的数量（总数)
ip_type 整数 0-1 0:IPv4, 1:IPv6
data 数组 地址池统计信息数组
name 字符串 1-191 地址池名字
port 整数 地址池当前连接数量
used 整数 地址池累计连接数量
freed 整数 地址池累计释放连接数量
响应举例：
{
    "pool_num": 19,
    "match_num": 0,
    "limit_num": 3,
    "total": 19,
    "ip_type": 0,
    "data": [
        {
            "name": "pop3_nat",
            "port": 0,
            "used": 0,
            "freed": 0
        },
        {
            "name": "dx",
            "port": 0,
            "used": 1828408,
            "freed": 1828408
        },
        {
            "name": "lt",
            "port": 0,
            "used": 788268,
            "freed": 788268
        }
    ]
}

NAT 地址池统计信息获取
Action：nat.pool.stats.list
请求参数：
名称 类型 范围 含义 必选 备注
ip_type 整数 0-1 0:IPv4, 1:IPv6 否 缺省为 0
name 字符串 1-191 地址池名字 是
start 整数 0-99999 开始返回数据的编号 否 缺省为 0
limit 整数 0-99999 最多返回数据的条数 否 缺省为 30；0 表示不限制
searchbk 字符串 0-127 过滤条件表达式 否 可选，默认""

请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool.stats.list&ip_type=0&start=1&limit=3&name=dx
响应参数：
名称 类型 范围 含义
addr_num 整数 0-99999 地址的数量（总数)
match_num 整数 0-99999 匹配的数量
limit_num 整数 0-99999 限制返回的数量
total 整数 0-99999 地址的数量（总数)
ip_type 整数 0-1 0:IPv4, 1:IPv6
data 数组 地址统计信息数组
addr IPv4/IPv6 地址 1-191 IPv4/IPv6 地址
port 整数 地址当前连接数量
used 整数 地址累计连接数量
freed 整数 地址累计释放连接数量
响应举例：
{
    "addr_num": 6,
    "match_num": 0,
    "limit_num": 3,
    "total": 6,
    "ip_type": 0,
    "data": [
        {
            "addr": "192.168.17.2",
            "port": 0,
            "used": 305126,
            "freed": 305126
        },
        {
            "addr": "192.168.17.3",
            "port": 0,
            "used": 304953,
            "freed": 304953
        },
        {
            "addr": "192.168.17.4",
            "port": 0,
            "used": 304803,
            "freed": 304803
        }
    ]
}

NAT 地址池统计信息清除
Action：nat.pool.stats.clear
请求参数：
名称 类型 范围 含义 必选 备注
ip_type 整数 0-1 0:IPv4, 1:IPv6 否 缺省为 1
name 字符串 1-191 地址池名字 否 指定名称时清除指定地址池的统计信息，为指定时清除指定类型的所有地址池的统计信息

请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool.stats.clear&ip_type=0&name=dx
请求 body：

响应参数：无
NAT 地址池组
NAT 地址池组列表
Action：nat.pool_group.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool_group.list
响应参数：
名称 类型 范围 含义
name 字符串 1-191 地址池组名字
vrrp_id 整数 0-8 VRRP 的 ID
pool_list 字符串数组 1-25 地址池数组
响应举例：
[ {
"name" : "ipv6group",
"vrrp_id" : 0,
"pool_list" : [ "ipv6pool" ]
}, {
"name" : "ipv4group",
"vrrp_id" : 1,
"pool_list" : [ "ipv4pool", "ipv4pool2" ]
} ]
NAT 地址池组获取
Action：nat.pool_group.get
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool_group.get
响应参数：
名称 类型 范围 含义
name 字符串 1-191 地址池组名字
vrrp_id 整数 0-8 VRRP 的 ID
pool_list 字符串数组 1-25 地址池数组
响应举例：
{
"name" : "ipv4group",
"vrrp_id" : 1,
"pool_list" : [ "ipv4pool", "ipv4pool2" ]
}
NAT 地址池组增加
Action：nat.pool_group.add
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 地址池组名字 是
vrrp_id 整数 0-8 VRRP 的 ID 否
pool_list 字符串数组 1-25 地址池数组 否
pool_list 成员 字符串 1-31 地址池名字 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool_group.add
请求 body：
{
"name" : "ipv4group",
"vrrp_id" : 1,
"pool_list" : [ "ipv4pool", "ipv4pool2" ]
}
NAT 地址池组编辑
Action：nat.pool_group.edit
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 地址池组名字 是
vrrp_id 整数 0-8 VRRP 的 ID 否
pool_list 字符串数组 1-25 地址池数组 否
pool_list 成员 字符串 1-31 地址池名字 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool_group.edit
请求 body：
{
"name" : "ipv4group",
"vrrp_id" : 1,
"pool_list" : [ "ipv4pool", "ipv4pool2" ]
}
NAT 地址池组删除
Action：nat.pool_group.del
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 地址池组名字 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.pool_group.del
请求 body：
{
"name" : "ipv4group"
}

静态 NAT(包括 PAT)
静态 NAT 列表
Action：nat.static.list
请求参数：
名称 类型 范围 含义 必选 备注
type 整数 0-2 类型 否 可选, 默认 0
0：all 1：nat 2：pat
limit 整数 0-1000 读取数 否 可选，默认 0
0 表示读取所有配置
index 整数 0-9999 序号 否 可选，默认 0
searchbk 字符串 0-127 表达式 否 可选，默认""
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.static.list
请求 body：
{
"type": 0,
"limit": 0,
"index": 30,
"searchbk": ""
}
响应参数：
名称 类型 范围 含义
origin_ip IPv4 内网源地址
nat_ip IPv4 外网全局地址
protocol 枚举 0，1，6，17 协议
origin_port 整数 1-65535 内网源端口
nat_port 整数 1-65535 外网端口
port_num 整数 1-65535 映射端口数
vrrp_id 整数 0-8 VRRP 的 ID
application 整数 0-5 PAT 中表明应用协议
priority 整数 0-1 优先级
if_type 枚举 0-3

    接口类型

if_slot 整数 0-127 ETH 插槽
if_port 整数 0-127 ETH 接口
if_ve 整数 2-4094 VE 接口
if_trunk 整数 1-8 Trunk 接口
disable bool 0-1 使能
description 字符串 0-191 描述
index 整数 0-9999 序号
响应举例：
[ {
"origin_ip" : "10.0.0.1",
"nat_ip" : "20.0.0.100",
"protocol" : 6,
"origin_port" : 100,
"nat_port" : 200,
"port_num" : 1,
"vrrp_id" : 0,
"application" : 2,
"if_slot" : 0,
"if_port" : 1,
"if_type" : 1,
"disable" : 0,
"description" : "pattest",
"index" : 0
}, {
"origin_ip" : "30.1.1.1",
"nat_ip" : "40.1.1.1",
"protocol" : 17,
"origin_port" : 233,
"nat_port" : 233,
"port_num" : 2,
"vrrp_id" : 0,
"application" : 1,
"if_type" : 0,
"disable" : 1,
"description" : "nattest",
"index" : 1
}, {
"origin_ip" : "203.1.1.1",
"nat_ip" : "203.1.1.2",
"protocol" : 1,
"port_num" : 1,
"vrrp_id" : 0,
"if_ve" : 2,
"if_type" : 2,
"disable" : 0,
"description" : "paticmp",
"index" : 2
}, {
"origin_ip" : "102.1.1.1",
"nat_ip" : "103.1.1.1",
"protocol" : 0,
"port_num" : 1,
"vrrp_id" : 0,
"priority" : 0,
"if_slot" : 0,
"if_port" : 2,
"if_type" : 1,
"disable" : 0,
"description" : "nattest",
"index" : 3
}, {
"origin_ip" : "104.1.1.1",
"nat_ip" : "105.1.1.1",
"protocol" : 0,
"port_num" : 1,
"vrrp_id" : 0,
"priority" : 1,
"if_ve" : 2,
"if_type" : 2,
"disable" : 0,
"description" : "vetestnat",
"index" : 4
} ]
静态 NAT 获取
Action：nat.static.get
请求参数：
名称 类型 范围 含义 必选 备注
origin_ip IPv4 内网源地址 是
nat_ip IPv4 外网全局地址 是
protocol 枚举 0，1，6，17 协议 是 0 表示 NAT，非 0 表示 PAT ，PAT 中：1 表示 icmp 转换，6 表示 tcp 转换，17 表示 udp 转换，默认 0
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.static.get
静态 NAT 获取，当 protocol 为 0
请求 body：
{
"origin_ip" : "102.1.1.1",
"nat_ip" : "103.1.1.1",
"protocol" : 0
}
响应参数：
名称 类型 范围 含义 必选 备注
origin_ip IPv4 内网源地址 是
nat_ip IPv4 外网全局地址 是
protocol 枚举 0，1，6，17 协议 是 0 表示 NAT，非 0 表示 PAT ，PAT 中：1 表示 icmp 转换，6 表示 tcp 转换，17 表示 udp 转换，默认 0
if_type 枚举 0-3

    接口类型	否	0：不启动接口选择功能

1：ETH
2：VE
3：TRUNK
默认 0
if_slot 整数 0-127 ETH 插槽 否 if_type 为 1 有效，默认 0
if_port 整数 0-127 ETH 接口 否 if_type 为 1 有效，默认 0
description 字符串 0-191 描述 否 默认空串
disable bool 0-1 使能 否 默认 0
vrrp_id 整数 0-8 VRRP 的 ID 否 默认 0
priority 整数 0-1 优先级 否 NAT 中有效，0 低优先级；1 高优先级，默认 0
响应举例：
{
"origin_ip" : "102.1.1.1",
"nat_ip" : "103.1.1.1",
"protocol" : 0,
"vrrp_id" : 0,
"priority" : 0,
"if_slot" : 0,
"if_port" : 2,
"if_type" : 1,
"disable" : 0,
"description" : "nattest"
}
静态 NAT 获取，当 protocol 为 1
请求参数：
名称 类型 范围 含义 必选 备注
origin_ip IPv4 内网源地址 是
nat_ip IPv4 外网全局地址 是
protocol 枚举 0，1，6，17 协议 是 0 表示 NAT，非 0 表示 PAT ，PAT 中：1 表示 icmp 转换，6 表示 tcp 转换，17 表示 udp 转换，默认 0
请求 body：
{
"origin_ip" : "203.1.1.1",
"nat_ip" : "203.1.1.2",
"protocol" : 1
}
响应参数：
名称 类型 范围 含义 必选 备注
origin_ip IPv4 内网源地址 是
nat_ip IPv4 外网全局地址 是
protocol 枚举 0，1，6，17 协议 是 0 表示 NAT，非 0 表示 PAT ，PAT 中：1 表示 icmp 转换，6 表示 tcp 转换，17 表示 udp 转换，默认 0
if_type 枚举 0-3

    接口类型	否	0：不启动接口选择功能

1：ETH
2：VE
3：TRUNK
默认 0
description 字符串 0-191 描述 否 默认空串
disable bool 0-1 使能 否 默认 0
vrrp_id 整数 0-8 VRRP 的 ID 否 默认 0
响应举例：
{
"origin_ip" : "203.1.1.1",
"nat_ip" : "203.1.1.2",
"protocol" : 1,
"vrrp_id" : 0,
"if_ve" : 2,
"if_type" : 2,
"disable" : 0,
"description" : "paticmp"
}
静态 NAT 获取，当 protocol 为 6 或 17
请求参数：
名称 类型 范围 含义 必选 备注
origin_ip IPv4 内网源地址 是
nat_ip IPv4 外网全局地址 是
protocol 枚举 0，1，6，17 协议 是 0 表示 NAT，非 0 表示 PAT ，PAT 中：1 表示 icmp 转换，6 表示 tcp 转换，17 表示 udp 转换，默认 0
origin_port 整数 1-65535 内网源端口 是(PAT) PAT 中有效，取值 1-65535
nat_port 整数 1-65535 外网端口 是(PAT) PAT 中有效，取值 1-65535
port_num 整数 1-65535 映射端口数 是(PAT) PAT 中有效，取值 1-65535
请求 body：
{
"origin_ip" : "30.1.1.1",
"nat_ip" : "40.1.1.1",
"protocol" : 17,
"origin_port" : 233,
"nat_port" : 233,
"port_num" : 2
}
响应参数：
名称 类型 范围 含义 必选 备注
origin_ip IPv4 内网源地址 是
nat_ip IPv4 外网全局地址 是
protocol 枚举 0，1，6，17 协议 是 0 表示 NAT，非 0 表示 PAT ，PAT 中：1 表示 icmp 转换，6 表示 tcp 转换，17 表示 udp 转换，默认 0
if_type 枚举 0-3

    接口类型	否	0：不启动接口选择功能

1：ETH
2：VE
3：TRUNK
默认 0
description 字符串 0-191 描述 否 默认空串
disable bool 0-1 使能 否 默认 0
vrrp_id 整数 0-8 VRRP 的 ID 否 默认 0
origin_port 整数 1-65535 内网源端口 是(PAT) PAT 中有效，取值 1-65535
nat_port 整数 1-65535 外网端口 是(PAT) PAT 中有效，取值 1-65535
port_num 整数 1-65535 映射端口数 是(PAT) PAT 中有效，取值 1-65535
响应举例：
{
"origin_ip" : "30.1.1.1",
"nat_ip" : "40.1.1.1",
"protocol" : 17,
"origin_port" : 233,
"nat_port" : 233,
"port_num" : 2,
"vrrp_id" : 0,
"application" : 1,
"if_type" : 0,
"disable" : 1,
"description" : "nattest"
}
静态 NAT 增加
Action：nat.static.add
请求参数：
名称 类型 范围 含义 必选 备注
origin_ip IPv4 内网源地址 是
nat_ip IPv4 外网全局地址 是
protocol 枚举 0，1，6，17 协议 是 0 表示 NAT，非 0 表示 PAT ，PAT 中：1 表示 icmp 转换，6 表示 tcp 转换，17 表示 udp 转换，默认 0
origin_port 整数 1-65535 内网源端口 是(PAT) PAT 中有效，取值 1-65535
nat_port 整数 1-65535 外网端口 是(PAT) PAT 中有效，取值 1-65535
port_num 整数 1-65535 映射端口数 是(PAT) PAT 中有效，取值 1-65535
vrrp_id 整数 0-8 VRRP 的 ID 否 默认 0
application 整数 0-6 PAT 中表明应用协议 否 PAT 中有效，1 表示 FTP；2 表示 RTSP；3 表示 PPTP；4 表示 MMS；6 表示 TFTP，默认 0
priority 整数 0-1 优先级 否 NAT 中有效，0 低优先级；1 高优先级，默认 0
if_type 枚举 0-3

    接口类型	否	0：不启动接口选择功能

1：ETH
2：VE
3：TRUNK
默认 0
if_slot 整数 0-127 ETH 插槽 否 if_type 为 1 有效，默认 0
if_port 整数 0-127 ETH 接口 否 if_type 为 1 有效，默认 0
if_ve 整数 2-4094 VE 接口 否 if_type 为 2 有效
if_trunk 整数 1-8 Trunk 接口 否 if_type 为 3 有效
disable bool 0-1 使能 否 默认 0
description 字符串 0-191 描述 否 默认空串
index 整数 0-9999 序号 否 翻页使用，默认 0
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.static.add
请求 body：
{
"origin_ip" : "30.1.1.1",
"nat_ip" : "40.1.1.1",
"protocol" : 17,
"origin_port" : 233,
"nat_port" : 233,
"port_num" : 2,
"vrrp_id" : 0,
"application" : 1,
"if_type" : 0,
"disable" : 1,
"description" : "nattest"
}
请求参数参考静态 NAT 获取
静态 NAT 编辑
Action：nat.static.edit
请求参数：
名称 类型 范围 含义 必选 备注
origin_ip IPv4 内网源地址 是
nat_ip IPv4 外网全局地址 是
protocol 枚举 0，1，6，17 协议 是 0 表示 NAT，非 0 表示 PAT ，PAT 中：1 表示 icmp 转换，6 表示 tcp 转换，17 表示 udp 转换，默认 0
origin_port 整数 1-65535 内网源端口 是(PAT) PAT 中有效，取值 1-65535
nat_port 整数 1-65535 外网端口 是(PAT) PAT 中有效，取值 1-65535
port_num 整数 1-65535 映射端口数 是(PAT) PAT 中有效，取值 1-65535
vrrp_id 整数 0-8 VRRP 的 ID 否 默认 0
application 整数 0-5 PAT 中表明应用协议 否 PAT 中有效，1 表示 FTP；2 表示 RTSP；3 表示 PPTP；4 表示 MMS；5 表示 SIP，默认 0
priority 整数 0-1 优先级 否 NAT 中有效，0 低优先级；1 高优先级，默认 0
if_type 枚举 0-3

    接口类型	否	0：不启动接口选择功能

1：ETH
2：VE
3：TRUNK
默认 0
if_slot 整数 0-127 ETH 插槽 否 if_type 为 1 有效，默认 0
if_port 整数 0-127 ETH 接口 否 if_type 为 1 有效，默认 0
if_ve 整数 2-4094 VE 接口 否 if_type 为 2 有效
if_trunk 整数 1-8 Trunk 接口 否 if_type 为 3 有效
disable bool 0-1 使能 否 默认 0
description 字符串 0-191 描述 否 默认空串
index 整数 0-9999 序号 否 翻页使用，默认 0
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.static.edit
请求 body：
{
"old_origin_ip": "30.1.1.1",
"origin_ip" : "30.1.1.2",
"old_nat_ip" : "40.1.1.1",
"nat_ip" : "40.1.1.2",
"old_protocol" : 17,
"protocol" : 17,
"old_origin_port" : 233,
"origin_port" : 233,
"old_nat_port" : 233,
"nat_port" : 233,
"old_port_num" : 2,
"port_num" : 2,
"old_vrrp_id" : 0,
"vrrp_id" : 0,
"application" : 1,
"if_type" : 0,
"disable" : 1,
"description" : "nattest"
}
静态 NAT 删除
Action：nat.static.del
请求参数：
名称 类型 范围 含义 必选 备注
origin_ip IPv4 内网源地址 是
nat_ip IPv4 外网全局地址 是
protocol 枚举 0，1，6，17 协议 是 0 表示 NAT，非 0 表示 PAT ，PAT 中：1 表示 icmp 转换，6 表示 tcp 转换，17 表示 udp 转换，默认 0
origin_port 整数 1-65535 内网源端口 是(PAT) PAT 中有效，取值 1-65535
nat_port 整数 1-65535 外网端口 是(PAT) PAT 中有效，取值 1-65535
port_num 整数 1-65535 映射端口数 是(PAT) PAT 中有效，取值 1-65535
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.static.del

1.  protocol 为 0
    请求 body：
    {
    "origin_ip" : "102.1.1.1",
    "nat_ip" : "103.1.1.1",
    "protocol" : 0
    }
2.  protocol 为 1
    请求 body：
    {
    "origin_ip" : "203.1.1.1",
    "nat_ip" : "203.1.1.2",
    "protocol" : 1
    }
    1)protocol 为 6 或 17
    请求 body：
    {
    "origin_ip" : "30.1.1.1",
    "nat_ip" : "40.1.1.1",
    "protocol" : 17,
    "origin_port" : 233,
    "nat_port" : 233,
    "port_num" : 2
    }
    静态 NAT 统计信息列表
    Action：nat.static.statis
    请求参数：
    名称 类型 范围 含义 必选 备注
    type 整数 0-2 类型 否 可选, 默认 0
    0：all 1：nat 2：pat
    limit 整数 0-1000 读取数 否 可选，默认 0
    0 表示读取所有配置
    index 整数 0-9999 序号 否 可选，默认 0
    searchbk 字符串 0-127 表达式 否 可选，默认""
    请求举例：
    POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.static.statis
    请求 body：
    {
    "type": 0,
    "limit": 1,
    "index": 30,
    "searchbk": "1"
    }
    响应参数：
    名称 类型 范围 含义
    origin_ip IPv4 内网源地址
    nat_ip IPv4 外网全局地址
    protocol 枚举 0，1，6，17 协议
    origin_port 整数 1-65535 内网源端口
    nat_port 整数 1-65535 外网端口
    port_num 整数 1-65535 映射端口数
    port_used 整数 0- 4294967295 端口使用量
    port_total_used 整数 0- 4294967295 端口使用累计量
    port_total_freed 整数 0- 4294967295 端口释放累计量
    port_total_hits 整数 0- 4294967295 端口命中累计量
    响应举例：
    {
    "static_nat_list" : [ {
    "origin_ip" : "1.1.1.12",
    "nat_ip" : "2.2.2.22",
    "protocol" : 0,
    "port_used" : 0,
    "port_total_used" : 0,
    "port_total_freed" : 0,
    "port_total_hits" : 0
    },{
    "origin_ip" : "100.1.1.1",
    "nat_ip" : "200.1.1.1",
    "protocol" : 6,
    "origin_port" : 22,
    "nat_port" : 22,
    "port_num" : 3,
    "port_used" : 0,
    "port_total_used" : 0,
    "port_total_freed" : 0,
    "port_total_hits" : 0
    } ],
    "total" : 2
    }
    静态 NAT 统计信息清除
    Action：nat.static.clear
    请求参数：无
    请求举例：
    GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.static.clear
    网络 NAT
    网络 NAT 列表
    Action：nat.network.list
    请求参数：无
    请求举例：
    GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.network.list
    响应参数：
    名称 类型 范围 含义
    name 字符串 1-191 网络 NAT 名称
    origin_ip IPv4 内网源地址
    origin_mask IPv4 内网源地址掩码
    nat_ip IPv4 外网全局地址
    nat_mask IPv4 外网全局地址掩码
    number 整数 1-180000 转换个数
    vrrp_id 整数 0-8 VRRP 的 ID
    响应举例：
    [ {
    "name" : "netnat",
    "origin_ip" : "10.0.1.0",
    "origin_mask" : "255.255.255.0",
    "nat_ip" : "220.22.22.0",
    "nat_mask" : "255.255.255.0",
    "number" : 10,
    "vrrp_id" : 1
    }, {
    "name" : "net2",
    "origin_ip" : "20.1.1.1",
    "origin_mask" : "255.255.255.0",
    "nat_ip" : "30.1.1.1",
    "nat_mask" : "255.255.255.0",
    "number" : 10,
    "vrrp_id" : 1
    } ]
    网络 NAT 获取
    Action：nat.network.get
    请求参数：
    名称 类型 范围 含义 必选 备注
    name 字符串 1-191 网络 NAT 名称 是
    请求举例：
    POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.network.get
    请求 body：
    {
    "name" : "netnat"
    }
    响应参数：
    名称 类型 范围 含义
    name 字符串 1-191 网络 NAT 名称
    origin_ip IPv4 内网源地址
    origin_mask IPv4 内网源地址掩码
    nat_ip IPv4 外网全局地址
    nat_mask IPv4 外网全局地址掩码
    number 整数 1-180000 转换个数
    vrrp_id 整数 0-8 VRRP 的 ID
    响应举例：
    {
    "name" : "netnat",
    "origin_ip" : "10.0.1.0",
    "origin_mask" : "255.255.255.0",
    "nat_ip" : "220.22.22.0",
    "nat_mask" : "255.255.255.0",
    "number" : 10,
    "vrrp_id" : 1
    }
    网络 NAT 增加
    Action：nat.network.add
    请求参数：
    名称 类型 范围 含义 必选 备注
    name 字符串 1-191 网络 NAT 名称 是 必选
    origin_ip IPv4 内网源地址 是 必选
    origin_mask IPv4 内网源地址掩码 是 必选
    nat_ip IPv4 外网全局地址 是 必选
    nat_mask IPv4 外网全局地址掩码 是 必选
    number 整数 1-180000 转换个数 是 必选，默认 1
    vrrp_id 整数 0-8 VRRP 的 ID 否 可选，默认 0
    请求举例：
    POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.network.add
    请求 body：
    {
    "name" : "netnat3",
    "origin_ip" : "50.0.1.0",
    "origin_mask" : "255.255.255.0",
    "nat_ip" : "215.22.22.0",
    "nat_mask" : "255.255.255.0",
    "number" : 20,
    "vrrp_id" : 1
    }
    网络 NAT 编辑
    Action：nat.network.edit
    请求参数：
    名称 类型 范围 含义 必选 备注
    name 字符串 1-191 网络 NAT 名称 是 必选
    origin_ip IPv4 内网源地址 是 必选
    origin_mask IPv4 内网源地址掩码 是 必选
    nat_ip IPv4 外网全局地址 是 必选
    nat_mask IPv4 外网全局地址掩码 是 必选
    number 整数 1-180000 转换个数 是 必选，默认 1
    vrrp_id 整数 0-8 VRRP 的 ID 否 可选，默认 0
    请求举例：
    POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.network.edit
    请求 body：
    {
    "name" : "netnat3",
    "origin_ip" : "50.0.1.0",
    "origin_mask" : "255.255.255.0",
    "nat_ip" : "215.22.22.0",
    "nat_mask" : "255.255.255.0",
    "number" : 20,
    "vrrp_id" : 1
    }
    网络 NAT 删除
    Action：nat.network.del
    请求参数：
    名称 类型 范围 含义 必选 备注
    name 字符串 1-191 网络 NAT 名称 是
    请求举例：
    POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.network.del
    请求 body：
    {
    "name" : "netnat3"
    }

NAT 映射
NAT 映射列表
Action：nat.map.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.map.list
响应参数：
名称 类型 范围 含义
acl 整数 2-198 Ipv4 访问列表
nat_pool 字符串 1-191 Nat 地址池
响应举例：
[ {
"acl" : 2,
"nat_pool" : "ipv4pool2"
}, {
"acl" : 3,
"nat_pool" : "ipv4pool"
} ]
NAT 映射增加
Action：nat.map.add
请求参数：
名称 类型 范围 含义 必选 备注
acl 整数 2-198 Ipv4 访问列表 是
nat_pool 字符串 1-191 Nat 地址池 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.map.add
请求 body：
{
"acl" : 3,
"nat_pool" : "ipv4pool"
}
NAT 映射删除
Action：nat.map.del
请求参数：
名称 类型 范围 含义 必选 备注
acl 整数 2-198 Ipv4 访问列表 是
nat_pool 字符串 1-191 Nat 地址池 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.map.del
请求 body：
{
"acl" : 3,
"nat_pool" : "ipv4pool"
}

IPv6 NAT 映射列表
Action：nat.ipv6.map.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.ipv6.map.list
响应参数：
名称 类型 范围 含义
acl_name 字符串 1-191 Ipv6 访问列表
nat_pool 字符串 1-191 Nat 地址池
响应举例：
[ {
"acl_name" : "mgmtacl",
"nat_pool" : "aclipv6"
} ]
IPv6 NAT 映射增加
Action：nat. ipv6.map.add
请求参数：
名称 类型 范围 含义 必选 备注
acl_name 字符串 1-191 Ipv6 访问列表 是
nat_pool 字符串 1-191 Nat 地址池 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.ipv6.map.add
请求 body：
{
"acl_name" : "mgmtacl",
"nat_pool" : "aclipv6"
}
IPv6 NAT 映射删除
Action：nat. ipv6.map.del
请求参数：
名称 类型 范围 含义 必选 备注
acl_name 字符串 1-191 Ipv6 访问列表 是
nat_pool 字符串 1-191 Nat 地址池 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat. ipv6.map.del
请求 body：
{
"acl_name" : "mgmtacl",
"nat_pool" : "aclipv6"
}
地址转换策略
地址转换策略列表
Action：nat.policy.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.policy.list
响应参数：
名称 类型 范围 含义
name 字符串 1-191 策略名
acl 整数 2-198 访问列表
nat_pool 字符串 1-191 地址池
pool_bind_list 数组 0-64 地址池绑定列表
member_acl 整数 2-198 访问列表
member_nat_pool 字符串 1-191 地址池
响应举例：
[{
"name": "123",
"acl": 2,
"nat_pool": "pool1",
"pool_bind_list": [{
"member_acl": 3,
"member_nat_pool": "pool2"
}, {
"member_acl": 4,
"member_nat_pool": "pool3"
}]
}, {
"name": "test",
"acl": 2,
"nat_pool": "pool2",
"pool_bind_list": [{
"member_acl": 3,
"member_nat_pool": "pool3"
}]
}]
地址转换策略获取
Action：nat.policy.get
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 策略名 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.policy.get
请求 body：
{
"name": "123"
}
响应参数：
名称 类型 范围 含义
name 字符串 1-191 策略名
acl 整数 2-198 访问列表
nat_pool 字符串 1-191 地址池
pool_bind_list 数组 0-64 地址池绑定列表
member_acl 整数 2-198 访问列表
member_nat_pool 字符串 1-191 地址池
响应举例：
{
"name": "123",
"acl": 2,
"nat_pool": "pool1",
"pool_bind_list": [{
"member_acl": 3,
"member_nat_pool": "pool2"
}, {
"member_acl": 4,
"member_nat_pool": "pool3"
}]
}
地址转换策略增加
Action：nat.policy.add
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 策略名 是
acl 整数 2-198 访问列表 否 0 表示没有配置
nat_pool 字符串 1-191 地址池 否 空字符串表示没有配置
pool_bind_list 数组 0-64 地址池绑定列表 否
member_acl 整数 2-198 访问列表 是
member_nat_pool 字符串 1-191 地址池 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.policy.add
请求 body：
{
"name": "new",
"acl": 2,
"nat_pool": "pool1",
"pool_bind_list": [{
"member_acl": 3,
"member_nat_pool": "pool2"
}, {
"member_acl": 4,
"member_nat_pool": "pool3"
}]
}
地址转换策略编辑
Action：nat.policy.edit
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 策略名 是
acl 整数 2-198 访问列表 否 0 表示没有配置
nat_pool 字符串 1-191 地址池 否 空字符串表示没有配置
pool_bind_list 数组 0-64 地址池绑定列表 否
member_acl 整数 2-198 访问列表 是
member_nat_pool 字符串 1-191 地址池 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.policy.edit
请求 body：
{
"name": "new",
"acl": 2,
"nat_pool": "pool1",
"pool_bind_list": [{
"member_acl": 3,
"member_nat_pool": "pool2"
}, {
"member_acl": 4,
"member_nat_pool": "pool3"
}]
}
地址转换策略删除
Action：nat.policy.del
请求参数：
名称 类型 范围 含义 必选 备注
name 字符串 1-191 策略名 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.policy.del
请求 body：
{
"name": "new"
}

NAT 全局配置
NAT 超时参数获取
Action：nat.timeout.get
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.timeout.get
响应参数：
名称 类型 范围 含义
syn 整数 60-300（秒） 半连接会话超时删除时间
tcp 整数 60-18000（秒） tcp 连接会话超时删除时间
udp 整数 60-18000（秒） udp 连接会话超时删除时间
icmp 整数 60-18000（秒） icmp 连接会话超时删除时间
service_list 数组 服务超时列表
protocol 整数 0-1 协议
port 整数 1-65535 端口
timeout 整数 0-18000（秒） 连接会话超时删除时间
响应举例：
{
"syn" : 180,
"tcp" : 180,
"udp" : 180,
"icmp" : 120,
"service_list" : [ {
"protocol" : 1,
"port" : 53,
"timeout" : 120
},
{
"protocol" : 1,
"port" : 54,
"timeout" : 180
}]
}
NAT 超时参数设置
Action：nat.timeout.set
请求参数：
名称 类型 范围 含义 必选 备注
syn 整数 60-300（秒） 半连接会话超时删除时间 否 可选，只能配置 60 的整倍数，缺省值:60
tcp 整数 60-18000（秒） tcp 连接会话超时删除时间 否 可选，只能配置 60 的整倍数，缺省值:300
udp 整数 60-18000（秒） udp 连接会话超时删除时间 否 可选，只能配置 60 的整倍数，缺省值:300
icmp 整数 60-18000（秒） icmp 连接会话超时删除时间 否 可选，只能配置 60 的整倍数，缺省值:60
service_list LIST 服务超时列表 否 缺省值:不可修改
protocol 整数 0-1 协议 是 必选，1 表示 udp 0 表示 tcp
port 整数 1-65535 端口 是 必选，协议端口
timeout 整数 0-18000（秒） 连接会话超时删除时间 是 必选，只能配置 60 的整倍数
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.timeout.set
请求 body：
{
"syn" : 180,
"tcp" : 180,
"udp" : 180,
"icmp" : 120,
"service_list" : [ {
"protocol" : 1,
"port" : 53,
"timeout" : 120
},
{
"protocol" : 1,
"port" : 54,
"timeout" : 180
}]
}

NAT 全局参数获取
Action：nat.global.get
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.global.get
响应参数：
名称 类型 范围 含义
pptp_alg 布尔型 0-1 开启 PPTP 算法
port_enable 布尔型 0-1 端口启动 NAT
gw_enable 布尔型 0-1 启动网管
nat_pool_log 布尔型 0-1 开启 snat 资源池使用率告警日志,，0 关闭，1 开启
nat_pool_log_warn_th 整数 1-100 告警门限，单位为百分比
nat_pool_log_warn_cth 整数 0-100 恢复告警门限日志，单位为百分比，0 为不恢复
nat_pool_log_warn_period 整数 5-86400 小于撤销告警门限打印恢复告警，恢复告警只打印一次
响应举例：
{
"pptp_alg" : 1,
"port_enable" : 0,
"gw_enable" : 1，
"nat_pool_log": 1,
"nat_pool_log_warn_th": 80,
"nat_pool_log_warn_cth": 1,
 "nat_pool_log_warn_period": 60

}
NAT 全局参数设置
Action：nat.global.set
请求参数：
名称 类型 范围 含义 必选 备注
pptp_alg 布尔型 0-1 开启 PPTP 算法 启动该功能，pptp 才能透传 nat，默认 1
port_enable 布尔型 0-1 端口启动 NAT 该参数为 1，接口 nat 命令才能工作，默认 0
gw_enable 布尔型 0-1 启动网管 默认 0
nat_pool_log 布尔型 0-1 开启 snat 资源池使用率告警日志 0 关闭，1 开启，默认 0
nat_pool_log_warn_th 整数 1-100 告警门限，单位为百分比 默认 80
nat_pool_log_warn_cth 整数 0-100 恢复告警门限日志，单位为百分比，0 为不恢复 默认 0
nat_pool_log_warn_period 整数 5-86400 按照周期提示告警信息，小于撤销告警门限打印恢复告警，恢复告警只打印一次 默认为 60
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=nat.global.set
请求 body：
{
    "pptp_alg": 1,
    "port_enable": 0,
    "gw_enable": 0,
    "nat_pool_log": 1,
    "nat_pool_log_warn_th": 80,
"nat_pool_log_warn_cth": 0,
"nat_pool_log_warn_period": 60
}
地址解析
IPv4 ARP
获取静态 ARP 配置列表
Action：arp.ipv4.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv4.list
响应参数：
名称 类型 范围 含义
ip_addr IPv4 地址 IP 地址
mac_addr MAC 地址 MAC 地址
port_type 整数 1,3 接口类型:1 以太网接口 3 trunk 接口
slot_num 整数 0-8 接口插槽号
port_num 整数 0-7 当 port_type 为 1 时表示以太网接口端口号
当 port_type 为 3 时表示 trunk 接口 ID

响应举例：
[{
"ip_addr": "192.168.220.229",
"mac_addr": "0000.0000.0001"
}, {
"ip_addr": "10.0.3.100",
"mac_addr": "0000.0003.0001"
}, {
"ip_addr": "10.0.2.100",
"mac_addr": "0000.0002.0001"
}, {
"ip_addr": "10.0.0.100",
"mac_addr": "0000.0001.0001",
"port_type": 1,
"slot_num": 0,
"port_num": 0
}]
获取指定静态 ARP 配置
Action：arp.ipv4.get
请求参数：
名称 类型 范围 含义 必选 备注
ip_addr IPv4 地址 IP 地址 是

请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv4.get
请求 body：
{"ip_addr":"10.0.3.100"}
响应参数：

名称 类型 范围 含义
ip_addr IPv4 地址 IP 地址
mac_addr MAC 地址 MAC 地址
port_type 整数 1 接口类型:1 以太网接口，3 trunk 接口
slot_num 整数 0-8 接口插槽号
port_num 整数 0-7 接口号
响应举例：
{
"ip_addr": "10.0.3.100",
"mac_addr": "0000.0003.0001"
}
增加静态 ARP 配置
Action：arp.ipv4.add
请求参数：
名称 类型 范围 含义 必选 备注
ip_addr IPv4 地址 IP 地址 是
mac_addr MAC 地址 MAC 地址 是
port_type 整数 0/1/3 接口类型 是 0:表示不指定接口(默认同网段的接口)
1：以太口,当 ARP 所在接口为 VE 接口时必须使用该参数,其它情况不需要
3:trunk 接口
缺省值:0

slot_num 整数 0-8 接口插槽号 否 当指定 port_type 为 1 时需要指定该参数
缺省值:无
port_num 整数 0-7 接口号 否 当指定 port_type 为 1 或者 3 时需要指定该参数
当 port_type 为 1 时表示以太网接口端口号
当 port_type 为 3 时表示 trunk 接口 ID
缺省值:无
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv4.add
举例 1:添加非 VE 接口的 ARP
请求 body：
{
"ip_addr":"192.168.70.100",
"mac_addr":"0000.0000.0001",
"port_type":0
}
举例 2：添加 VE 接口中（ETH0/0)的 ARP
{
"ip_addr":"192.168.10.100",
"mac_addr":"0000.0000.0001",
"port_type":1,
"slot_num":0,
"port_num":0
} 1.添加静态 ARP 时,IP 地址必须属于设备直连路由可达的范围 2.静态 ARP 对应直连路由属于 VE 接口时,必须指定其具体的以太网接口
编辑指定静态 ARP 配置
Action：arp.ipv4.edit
请求参数：
名称 类型 范围 含义 必选 备注
ip_addr IPv4 地址 IP 地址 是
mac_addr MAC 地址 MAC 地址 否 缺省值:不修改
port_type 整数 0/1/3 接口类型 是 0:表示不指定接口
1：以太口,当 ARP 所在接口为 VE 接口时必须使用该参数,其它情况不需要
3:trunk 接口
缺省值:0

slot_num 整数 0-8 接口插槽号 否 当指定 port_type 为 1 时需要指定该参数
缺省值:无
port_num 整数 0-7 接口号 否 当指定 port_type 为 1 或者 3 时需要指定该参数
当 port_type 为 1 时表示以太网接口端口号
当 port_type 为 3 时表示 trunk 接口 ID
缺省值:无
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv4.edit
请求 body：
{
"ip_addr":"192.168.70.100",
"mac_addr":"0000.0070.0001"
}
删除指定静态 ARP 配置
Action：arp.ipv4.del
请求参数：
名称 类型 范围 含义 必选 备注
ip_addr IPv4 地址 IP 地址 是

请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv4.del
{"ip_addr":"10.0.3.100"}

获取 ARP 状态信息列表
Action：arp.ipv4.statis
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv4.statis
响应参数：
名称 类型 范围 含义
ip_addr IPv4 地址 IP 地址
mac_addr MAC 地址 MAC 地址
port_type 整数 1-4 接口类型:1 以太网接口， 3 trunk 接口，4：管理口
slot_num 整数 0-8 接口插槽号
port_num 整数 0-7 当 port_type 为 1 时表示 以太网接口号
当 port_type 为 3 时表示 trunk 接口号

type 字符串 ARP 类型：Static：静态 ARP ，Dynamic：动态 ARP
age 整数 0-300 占用时间,单位秒
state 字符串 状态：
"Incomplete", 未完成的
"Reachable", 可达的
"Stale", 陈旧的/过期的
"Delay",延迟状态
"Probe",探测状态
"Failed",失败状态
"No ARP",不需要解析
"Permanent",永久的
"None"初始状态
响应举例：
[{
"ip_addr": "10.0.0.100",
"mac_addr": "0000.0001.0001",
"port_type": 1,
"slot_num": 0,
"port_num": 0,
"type": "Static",
"age": 0,
"state": "Permanent",
"vlan_id": 100
}, {
"ip_addr": "10.0.2.100",
"mac_addr": "0000.0003.0001",
"port_type": 3,
"port_num": 1,
"type": "Static",
"age": 0,
"state": "Permanent"
}, {
"ip_addr": "10.0.2.123",
"mac_addr": "000c.29c9.678e",
"port_type": 3,
"port_num": 1,
"type": "Dynamic",
"age": 223,
"state": "Stale"
}, {
"ip_addr": "10.0.3.100",
"mac_addr": "0000.0003.0001",
"port_type": 1,
"slot_num": 0,
"port_num": 2,
"type": "Static",
"age": 0,
"state": "Permanent"
}, {
"ip_addr": "192.168.220.1",
"mac_addr": "24b8.d200.840e",
"port_type": 4,
"type": "Dynamic",
"age": 74,
"state": "Reachable"
}]
清除动态 ARP
Action：arp.ipv4.clear
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv4.clear

IPv6 Neigbor
获取静态 IPv6 邻居(Neighbor)列表
Action：arp.ipv6.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv6.list
响应参数：
名称 类型 范围 含义
ip_addr IPv6 地址 IPv6 地址
mac_addr MAC 地址 MAC 地址
port_type 整数 1，3 接口类型:1 以太网接口，3 trunk 接口
slot_num 整数 0-8 接口插槽号
port_num 整数 0-7 接口号
响应举例：
[{
"ip_addr": "2000::2",
"mac_addr": "0021.0000.0002",
"port_type": 1,
"slot_num": 0,
"port_num": 0
}, {
"ip_addr": "2001::2",
"mac_addr": "0021.0000.0002",
"port_type": 1,
"slot_num": 0,
"port_num": 2
}, {
"ip_addr": "2004::2",
"mac_addr": "0024.0000.0002",
"port_type": 1,
"slot_num": 0,
"port_num": 4
}]
获取指定静态 IPv6 邻居(Neighbor)
Action：arp.ipv6.get
请求参数：
名称 类型 范围 含义 必选 备注
ip_addr IPv6 地址 IPv6 地址 是

请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv6.get
{"ip_addr": "2000::2"}
响应参数：
名称 类型 范围 含义
ip_addr IPv6 地址 IPv6 地址
mac_addr MAC 地址 MAC 地址
port_type 整数 1，3 接口类型: 1 以太网接口，3 trunk 接口
slot_num 整数 0-8 接口插槽号
port_num 整数 0-7 接口号
响应举例：
{
"ip_addr": "2000::2",
"mac_addr": "0021.0000.0002",
"port_type": 1,
"slot_num": 0,
"port_num": 0
}
增加静态 IPv6 邻居(Neighbor)
Action：arp.ipv6.add
请求参数：

名称 类型 范围 含义 必选 备注
ip_addr IPv6 地址 IPv6 地址 是
mac_addr MAC 地址 MAC 地址 是
port_type 整数 1，3 接口类型 是 1：以太口,3；trunk 口
slot_num 整数 0-8 接口插槽号 否 当指定 port_type 为 1 时需要指定该参数
缺省值:无
port_num 整数 0-7 接口号 是 当指定 port_type 为 1 时表示以太网接口号
当指定 port_type 为 3 时表示 trunk 号
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv6.add
举例 1:添添加以太接口的 Neighbor
请求 body：
{
"ip_addr":"2000::3",
"mac_addr":"0000.0000.0003",
"port_type":1,
"slot_num":0,
"port_num":1
}
举例 2：添加 TRUNK 口的 Neighbor
{
"ip_addr":"2002::2",
"mac_addr":"0000.0002.0002",
"port_type":3,
"port_num":1
} 1.添加静态 IPv6 Neighbor 时,IPv6 地址必须属于设备 IPv6 直连路由可达的范围 2.静态 IPv6 Neighbor 对应直连路由属于 VE 接口时,必须指定其具体的以太网接口
编辑指定静态 IPv6 邻居(Neighbor)
Action：arp.ipv6.edit
请求参数：
名称 类型 范围 含义 必选 备注
ip_addr IPv6 地址 IPv6 地址 是
mac_addr MAC 地址 MAC 地址 否
port_type 整数 1，3 接口类型 是 1：以太口,3；trunk 口
slot_num 整数 0-8 接口插槽号 否 当指定 port_type 为 1 时需要指定该参数
缺省值:无
port_num 整数 0-7 接口号 是 当指定 port_type 为 1 时表示以太网接口号
当指定 port_type 为 3 时表示 trunk 号
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv6.edit
请求 body：
{
"ip_addr": "2000::2",
"mac_addr": "0000.2000.0002",
"port_type": 1,
"slot_num": 0,
"port_num": 0
}
删除指定静态 IPv6 邻居(Neighbor)
Action：arp.ipv6.del
请求参数：
名称 类型 范围 含义 必选 备注
ip_addr IPv6 地址 IPv6 地址 是

请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv6.del
{"ip_addr": "2000::2"}

获取 IPV6 邻居状态信息列表
Action：arp.ipv6.statis
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv6.statis
响应参数：
名称 类型 范围 含义
ip_addr IPv6 地址 IPv6 地址
mac_addr MAC 地址 MAC 地址
port_type 整数 1，3，4 接口类型:1 以太网接口，2：VE 接口，3 trunk 接口
slot_num 整数 0-8 接口插槽号
port_num 整数 0-7 当 port_type 为 1 时表示 以太网接口号
当 port_type 为 3 时表示 trunk 接口号

type 字符串 ARP 类型：Static：静态 IPv6 邻居(Neighbor) ，Dynamic：动态 ARP
age 整数 0-300 占用时间,单位秒
state 字符串 状态：
"Incomplete", 未完成的
"Reachable", 可达的
"Stale", 陈旧的/过期的
"Delay",延迟状态
"Probe",探测状态
"Failed",失败状态
"No ARP",不需要解析
"Permanent",永久的
"None"初始状态
响应举例：
[{
"ip_addr": "2001::2",
"mac_addr": "0021.0000.0002",
"port_type": 2,
"port_num": 100,
"type": "Static",
"age": 0,
"state": "Permanent"
}, {
"ip_addr": "2004::3",
"mac_addr": "0004.0000.0003",
"port_type": 3,
"port_num": 1,
"type": "Static",
"age": 0,
"state": "Permanent"
}, {
"ip_addr": "2004::2",
"mac_addr": "0024.0000.0002",
"port_type": 3,
"port_num": 1,
"type": "Static",
"age": 0,
"state": "Permanent"
}, {
"ip_addr": "2000::2",
"mac_addr": "0021.0000.0002",
"port_type": 1,
"slot_num": 0,
"port_num": 0,
"type": "Static",
"age": 0,
"state": "Permanent"
}]
清除动态 IPv6 邻居(Neighbor)
Action：arp.ipv6.clear
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=arp.ipv6.clear

静态路由
IPv4 静态路由配置列表
Action：route.static.ipv4.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ipv4.list
响应参数：
名称 类型 范围 含义
destination IPV4 目的网段
netmask IPV4 掩码 掩码
gateway IPV4 网关
distance 整数 0-255 管理距离，默认为 0
description 字符串 0-191 描述
pool 字符串 1-191 下一跳池的 pool 名称
响应举例：
[{
"destination": "192.168.0.0",
"netmask": "255.255.0.0",
"gateway": "192.168.70.250",
"distance": 0,
"description": ""
}, {
"destination": "201.0.21.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62",
"distance": 1,
"description": ""
}]
配置路由的时候本机接口的网络地址需要跟路由的下一跳在相同网段

IPv4 静态路由配置获取
Action：route.static.ipv4.get
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 目的网段 是
netmask IPV4 掩码 掩码 是
gateway IPV4 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ipv4.get
请求 body：
{
"destination": "201.0.21.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62"
}
响应参数：
名称 类型 范围 含义
destination IPV4 - 目的网段
netmask IPV4 掩码 - 掩码
gateway IPV4 - 网关
distance 整数 0-255 管理距离，默认为 0
description 字符串 0-191 描述
响应举例：
{
"destination": "201.0.21.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62",
"distance": 1,
"description": ""
}
IPv4 静态路由配置增加
Action：route.static.ipv4.add
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 - 目的网段 是
netmask IPV4 掩码 - 掩码 是
gateway IPV4 - 网关 是
distance 整数 0-255 管理距离 否 默认值 0，1-255 可配
description 字符串 0-191 描述 否 默认空串
pool 字符串 1-191 下一跳池的 pool 名称 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ipv4.add
请求 body：
{
"destination": "201.0.22.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62"
}
IPv4 静态路由配置编辑
Action：route.static.ipv4.edit
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 - 目的网段 是
netmask IPV4 掩码 - 掩码 是
gateway IPV4 - 网关 是
distance 整数 0-255 管理距离 否 默认值 0，1-255 可配
description 字符串 0-191 描述 否 默认空串
pool 字符串 1-191 下一跳池的 pool 名称 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ipv4.edit
请求 body：
{
"destination": "201.0.22.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62",
"distance": 2,
"description": "test"
}
IPv4 静态路由配置删除
Action：route.static.ipv4.del
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 目的网段 是
netmask IPV4 掩码 掩码 是
gateway IPV4 网关 是
pool 字符串
1-191 下一跳池的 pool 名称 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ipv4.del
请求 body：
{
"destination": "201.0.22.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62"
}
IPv6 静态路由配置列表
Action：route.static.ipv6.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ipv6.list
响应参数：
名称 类型 范围 含义
destination IPV6 目的网段
prefix_len 掩码前缀 1-128 掩码
gateway IPV6 网关
distance 整数 0-255 管理距离
pool 字符串 1-191 下一跳池的 pool 名称
响应举例：
[{
"destination": "2002::",
"prefix_len": "64",
"gateway": "2001::62",
"distance": 1
}, {
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62",
"distance": 2
}]

    配置路由的时候本机接口的网络地址需要跟路由的下一跳在相同网段

IPv6 静态路由配置获取
Action：route.static.ipv6.get
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV6 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是

请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ipv6.get
请求 body：
{
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62"
}

响应参数：
名称 类型 范围 含义
destination IPV6 目的网段
prefix_len 掩码前缀 1-128 掩码
gateway IPV6 网关
distance 整数 0-255 管理距离。默认为 0，可配范围 1-255。
pool 字符串 1-191 服务池名称

响应举例：{
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62",
"distance": 1
}
IPv6 静态路由配置增加
Action：route.static.ipv6.add
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV6 - 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 - 网关 是
distance 整数 0-255 管理距离 否 默认值 0。可配范围 1-255。
pool 字符串 1-191 下一跳池的 pool 名称 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ipv6.add
请求 body：
{
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62",
"distance": 1
}
IPv6 静态路由配置编辑
Action：route.static.ipv6.edit
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV6 - 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 - 网关 是
distance 整数 0-255 管理距离 否 默认值 0。可配范围 1-255。
pool 字符串 1-191 下一跳池的 pool 名称 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ipv6.edit
请求 body：
{
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62",
"distance": 2
}
IPv6 静态路由配置删除
Action：route.static.ipv6.del
请求参数：
名称 类型 范围 含义 必选 说明
destination IPV6 - 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 - 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ipv6.del
请求 body：
{
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62"
}

静态管理路由
IPv4 静态管理路由配置列表
Action：route.static.mgmt.ipv4.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.mgmt.ipv4.list
响应参数：
名称 类型 范围 含义
destination IPV4 目的网段
netmask IPV4 掩码 掩码
gateway IPV4 网关
distance 整数 0-255 管理距离
description 字符串 0-191 描述
响应举例：
[{
"destination": "192.168.0.0",
"netmask": "255.255.0.0",
"gateway": "192.168.70.250",
"distance": 0,
"description": ""
}, {
"destination": "201.0.21.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62",
"distance": 1,
"description": ""
}]
配置路由的时候本机接口的网络地址需要跟路由的下一跳在相同网段

IPv4 静态管理路由配置获取
Action：route.static.mgmt.ipv4.get
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 目的网段 是
netmask IPV4 掩码 掩码 是
gateway IPV4 网关 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.mgmt.ipv4.get
请求 body：
{
"destination": "201.0.21.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62"
}
响应参数：
名称 类型 范围 含义
destination IPV4 目的网段
netmask IPV4 掩码 掩码
gateway IPV4 网关
distance 整数 0-255 管理距离
description 字符串 0-191 描述
响应举例：
{
"destination": "201.0.21.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62",
"distance": 1,
"description": ""
}
IPv4 静态管理路由配置增加
Action：route.static.mgmt.ipv4.add
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 目的网段 是
netmask IPV4 掩码 掩码 是
gateway IPV4 网关 是
distance 整数 0-255 管理距离 否 默认值 0，可配范围 1-255。
description 字符串 0-191 描述 否 默认空串
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.mgmt.ipv4.add
请求 body：
{
"destination": "201.0.22.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62"
}
IPv4 静态管理路由配置编辑
Action：route.static.mgmt.ipv4.edit
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 目的网段 是
netmask IPV4 掩码 掩码 是
gateway IPV4 网关 是
distance 整数 0-255 管理距离 否 默认值 0，可配范围 1-255。
description 字符串 0-191 描述 否 默认空串
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.mgmt.ipv4.edit
请求 body：
{
"destination": "201.0.22.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62",
"distance": 2,
"description": "test"
}
IPv4 静态管理路由配置删除
Action：route.static.mgmt.ipv4.del
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 目的网段 是
netmask IPV4 掩码 掩码 是
gateway IPV4 网关 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.mgmt.ipv4.del
请求 body：
{
"destination": "201.0.22.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62"
}
IPv6 静态管理路由配置列表
Action：route.static.mgmt.ipv6.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.mgmt.ipv6.list
响应参数：
名称 类型 范围 含义
destination IPV6 目的网段
prefix_len 掩码前缀 1-128 掩码
gateway IPV6 网关
distance 整数 0-255 管理距离
响应举例：
[{
"destination": "2002::",
"prefix_len": "64",
"gateway": "2001::62",
"distance": 1
}, {
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62",
"distance": 2
}]

    配置路由的时候本机接口的网络地址需要跟路由的下一跳在相同网段

IPv6 静态管理路由配置获取
Action：route.static.mgmt.ipv6.get
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV6 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 网关 是
distance 整数 0-255 管理距离 否 默认值 0

请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.mgmt.ipv6.get
{
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62"
}

响应参数：
名称 类型 范围 含义
destination IPV6 目的网段
prefix_len 掩码前缀 1-128 掩码
gateway IPV6 网关
distance 整数 0-255 管理距离

响应举例：{
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62",
"distance": 1
}
IPv6 静态路管理由配置增加
Action：route.static.mgmt.ipv6.add
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV6 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 网关 是
distance 整数 0-255 管理距离 否 默认值 0，可配范围 1-255。
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.mgmt.ipv6.add
请求 body：
{
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62",
"distance": 1
}
IPv6 静态管理路由配置编辑
Action：route.static.mgmt.ipv6.edit
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV6 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 网关 是
distance 整数 0-255 管理距离 否 默认值 0，可配范围 1-255。
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.mgmt.ipv6.edit
请求 body：
{
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62",
"distance": 2
}
IPv6 静态管理路由配置删除
Action：route.static.mgmt.ipv6.del
请求参数：
名称 类型 范围 含义 必选 说明
destination IPV6 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 网关 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.mgmt.ipv6.del
请求 body：
{
"destination": "2003::",
"prefix_len": "65",
"gateway": "2001::62"
}

静态业务路由
IPv4 静态业务路由配置列表
Action：route.static.ctrl.ipv4.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ctrl.ipv4.list
响应参数：
名称 类型 范围 含义
destination IPV4 - 目的网段
netmask IPV4 掩码 - 掩码
gateway IPV4 - 网关
pool 字符串 1-191 下一跳池的 pool 名称
distance 整数 0-255 管理距离
description 字符串 0-191 描述
响应举例：
[
    {
        "destination": "10.2.110.201",
        "netmask": "255.255.255.255",
        "gateway": "205.0.1.5",
        "distance": 0,
        "description": ""
    },
    {
        "destination": "208.0.0.0",
        "netmask": "255.0.0.0",
        "pool": "for_static_pool_server",
        "distance": 0,
        "description": ""
}
]
配置路由的时候本机接口的网络地址需要跟路由的下一跳在相同网段

IPv4 静态业务路由配置获取
Action：route.static.ctrl.ipv4.get
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 目的网段 是
netmask IPV4 掩码 掩码 是
gateway IPV4 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是 与 gateway 互斥
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ctrl.ipv4.get
请求 body（gateway）：
{
"destination": "201.0.21.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62"
}
请求 body（pool）：
{
"destination": "208.0.0.0",
"netmask": "255.0.0.0",
"pool": "for_static_pool_server"
}
响应参数：
名称 类型 范围 含义
destination IPV4 目的网段
netmask IPV4 掩码 掩码
gateway IPV4 网关
pool 字符串 1-191 下一跳池的 pool 名称
distance 整数 0-255 管理距离
description 字符串 0-191 描述
响应举例（gateway）：
{
"destination": "201.0.21.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62",
"distance": 1,
"description": ""
}
响应举例（pool）：
    {
        "destination": "208.0.0.0",
        "netmask": "255.0.0.0",
        "pool": "for_static_pool_server",
        "distance": 0,
        "description": ""
    }

IPv4 静态业务路由配置增加
Action：route.static.ctrl.ipv4.add
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 目的网段 是
netmask IPV4 掩码 掩码 是
gateway IPV4 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是 与 gateway 互斥
distance 整数 0-255 管理距离 否 默认值 0，可配范围 1-255。
description 字符串 0-191 描述 否 默认空串
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ctrl.ipv4.add
请求 body（gateway）：
{
"destination": "201.0.22.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62"
}
请求 body（pool）：
    {
        "destination": "208.0.0.0",
        "netmask": "255.0.0.0",
        "pool": "for_static_pool_server",
        "distance": 0,
        "description": ""
    }

IPv4 静态业务路由配置编辑
Action：route.static.ctrl.ipv4.edit
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 目的网段 是
netmask IPV4 掩码 掩码 是
gateway IPV4 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是 与 gateway 互斥
distance 整数 0-255 管理距离 否 默认值 0，可配范围 1-255。
description 字符串 0-191 描述 否 默认空串
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ctrl.ipv4.edit
请求 body（gateway）：
{
"destination": "201.0.22.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62",
"distance": 2,
"description": "test"
}
请求 body（pool）：
    {
        "destination": "208.0.0.0",
        "netmask": "255.0.0.0",
        "pool": "for_static_pool_server",
        "distance": 2,
        "description": ""
    }

IPv4 静态路业务由配置删除
Action：route.static.ctrl.ipv4.del
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV4 目的网段 是
netmask IPV4 掩码 掩码 是
gateway IPV4 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是 与 gateway 互斥
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ctrl.ipv4.del
请求 body（gateway）：
{
"destination": "201.0.22.0",
"netmask": "255.255.255.0",
"gateway": "30.0.0.62"
}
请求 body（pool）：
{
"destination": "208.0.0.0",
"netmask": "255.0.0.0",
"pool": "for_static_pool_server"
}
IPv6 静态业务路由配置列表
Action：route.static.ctrl.ipv6.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ctrl.ipv6.list
响应参数：
名称 类型 范围 含义
destination IPV6 目的网段
prefix_len 掩码前缀 1-128 掩码
gateway IPV6 网关
pool 字符串 1-191 下一跳池的 pool 名称
distance 整数 0-255 管理距离
响应举例：
[{
"destination": "2002::",
"prefix_len": "64",
"gateway": "2001::62",
"distance": 1
}, {
"destination": "2003::",
"prefix_len": "65",
"pool": "for_static_pool_server",
"distance": 2
}]

    配置路由的时候本机接口的网络地址需要跟路由的下一跳在相同网段

IPv6 静态业务路由配置获取
Action：route.static.ctrl.ipv6.get
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV6 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是 与 gateway 互斥
distance 整数 0-255 管理距离 否 默认值 1

请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ctrl.ipv6.get
请求 body（gateway）：
{
"destination": "2002::",
"prefix_len": "64",
"gateway": "2001::62"
}
请求 body（pool）：
{
"destination": "2003::",
"prefix_len": "65",
"pool": "for_static_pool_server"
}

响应参数：
名称 类型 范围 含义
destination IPV6 目的网段
prefix_len 掩码前缀 1-128 掩码
gateway IPV6 网关
pool 字符串 1-191 下一跳池的 pool 名称
distance 整数 1-255 管理距离

响应举例（gateway）：
{
    "destination": "2002::",
    "prefix_len": 64,
    "gateway": "2001::62",
    "distance": 1
}
响应举例（pool）：
{
    "destination": "2003::",
    "prefix_len": 65,
    "pool": "for_static_pool_server",
    "distance": 0
}

IPv6 静态业务路由配置增加
Action：route.static.ctrl.ipv6.add
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV6 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是 与 gateway 互斥
distance 整数 0-255 管理距离 否 默认值 0，可配范围 1-255。
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ctrl.ipv6.add
请求 body（gateway）：
{
"destination":"2002::",
"prefix_len":64,
"gateway":"2001::62",
"distance":1
}
请求 body（pool）：
{
"destination":"2003::",
"prefix_len":65,
"pool":"for_static_pool_server",
"distance":0
}
IPv6 静态业务路由配置编辑
Action：route.static.ctrl.ipv6.edit
请求参数：
名称 类型 范围 含义 必选 备注
destination IPV6 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是 与 gateway 互斥
distance 整数 0-255 管理距离 否 默认值 0，可配范围 1-255。
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ctrl.ipv6.edit
请求 body（gateway）：
{
"destination":"2002::",
"prefix_len":64,
"gateway":"2001::62",
"distance":1
}
请求 body（pool）：
{
"destination":"2003::",
"prefix_len":65,
"pool":"for_static_pool_server",
"distance":2
}
IPv6 静态业务路由配置删除
Action：route.static.ctrl.ipv6.del
请求参数：
名称 类型 范围 含义 必选 说明
destination IPV6 目的网段 是
prefix_len 掩码前缀 1-128 掩码 是
gateway IPV6 网关 是
pool 字符串 1-191 下一跳池的 pool 名称 是 与 gateway 互斥
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=route.static.ctrl.ipv6.del
请求 body（gateway）：
{
"destination": "2002::",
"prefix_len": "64",
"gateway": "2001::62"
}
请求 body（pool）：
{
"destination": "2003::",
"prefix_len": "65",
"pool": "for_static_pool_server"
}
OSPF
OSPF 网络列表
Action: ospf.network.list
请求参数：无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=a5c149123abf65d3f6407bd95f88dd&action=ospf.network.list
响应参数：
名称 类型 范围 含义
srcaddr 字符串 Ipv4 地址 网络 ip
netmask 字符串 Ipv4 掩码 网络掩码
areaid 整数 0-4294967295 区域 id
响应举例：
[{
"srcaddr": "120.120.120.0",
"netmask": "255.255.255.0",
"areaid": "1"
}]
OSPF 网络增加
Action：ospf.network.add
请求参数：
名称 类型 范围 含义 必选 备注
srcaddr 字符串 Ipv4 地址 网络 ip 是
netmask 字符串 Ipv4 掩码 网络掩码 是
areaid 整数 0-4294967295 区域 id 是
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=a5c149123abf65d3f6407bd95f88dd&action=ospf.network.add
请求 body：
{
"srcaddr": "120.120.120.0",
"netmask": "255.255.255.0",
"areaid": "1"
}
OSPF 网络删除
Action：ospf.network.del
请求参数：
名称 类型 范围 含义 必选 备注
srcaddr 字符串 Ipv4 地址 网络 ip 是
netmask 字符串 Ipv4 掩码 网络掩码 是
areaid 整数 0-4294967295 区域 id 是
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=a5c149123abf65d3f6407bd95f88dd&action=ospf.network.del
请求 body：
{
"srcaddr": "122.121.121.0",
"netmask": "255.255.255.0",
"areaid": "1"
}
OSPF 状态获取
Action：ospf.status.get
请求参数：无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=a5c149123abf65d3f6407bd95f88dd&action=ospf.status.get
响应参数：
名称 类型 范围 含义
status 整数 0-1 状态
redistribute_static 整数 0-1 静态路由重分发
redistribute_connected 整数 0-1 直连路由重分发
redistribute_vip 整数 0-1 SLB 虚拟服务地址重分发
redistribute_default 整数 0-1 缺省路由重分发
metric_standby 整数 0-65535 备机路由度量
响应举例：
{
"status": 1,
"redistribute_static": 1,
"redistribute_connected": 0,
"redistribute_vip": 1,
"redistribute_default": 0,
"metric_standby": 100
}
OSPF 状态设置
Action：ospf.status.set
请求参数：
名称 类型 范围 含义 必选 备注
status 整数 0-1 状态 是
redistribute_static 整数 0-1 静态路由重分发 否 默认 0
redistribute_connected 整数 0-1 直连路由重分发 否 默认 0
redistribute_vip 整数 0-1 SLB 虚拟服务地址重分发 否 默认 0
redistribute_default 整数 0-1 缺省路由重分发 否 默认 0
metric_standby 整数 0-65535 备机路由度量 否 默认 0，0：关闭故障倒换触发功能；1-65535：开启故障倒换触发功能后的备机路由度量值
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=a5c149123abf65d3f6407bd95f88dd&action=ospf.status.set
请求 body：
{
"status": 1,
"redistribute_static": 1,
"redistribute_connected": 0,
"redistribute_vip": 1,
"redistribute_default": 0,
"metric_standby": 100
}
BGP
BGP 网络列表
Action：bgp.network.list
请求参数：无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=bgp.network.list
响应参数：
名称 类型 范围 含义
srcaddr 字符串 Ipv4/Ipv6 地址 网络 ip
netmask 字符串 Ipv4 掩码地址， 或者 1-128 的整数 网络掩码
响应举例：
[{
"srcaddr": "120.120.120.0",
"netmask": "255.255.255.0",
}]
BGP 网络增加
Action：bgp.network.add
请求参数：
名称 类型 范围 含义 必选 备注
srcaddr 字符串 Ipv4 地址 Ipv4/Ipv6 地址 是
netmask 字符串 Ipv4 掩码 Ipv4 掩码地址， 或者 1-128 的整数 是
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=bgp.network.add
请求 body:
{
"srcaddr": "120.120.120.0",
"netmask": "255.255.255.0"
}
BGP 网络删除
Action: bgp.network.del
请求参数：
名称 类型 范围 含义 必选 备注
srcaddr 字符串 Ipv4 地址 Ipv4/Ipv6 地址 是
netmask 字符串 Ipv4 掩码 Ipv4 掩码地址， 或者 1-128 的整数 是
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=bgp.network.del
请求 body：
{
"srcaddr": "122.121.121.0",
"netmask": "255.255.255.0"
}
BGP 邻居列表
Action：bgp.neighbor.list
请求参数：无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=bgp.neighbor.list
响应参数：
名称 类型 范围 含义
neighbor_id 字符串 Ipv4/Ipv6 地址 邻居
remote_as_id 整数 1-4294967295 邻居 id
响应举例：
{
"neighbor_id": "13.14.15.16",
"remote_as_id": 2
}
BGP 邻居增加
Action：bgp.neighbor.add
请求参数：
名称 类型 范围 含义 必选 备注
neighbor_id 字符串 Ipv4 地址 邻居 是
remote_as_id 整数 1-4294967295 邻居 id 是
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=bgp.neighbor.add
请求 body：
{
"neighbor_id": "13.14.15.16",
"remote_as_id": 2
}
BGP 邻居删除
Action：bgp.neighbor.del
请求参数：
名称 类型 范围 含义 必选 备注
neighbor_id 字符串 Ipv4/Ipv6 地址 邻居 是
remote_as_id 整数 1-4294967295 邻居 id 是
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=436406305dc37d81c09a75740d4253&action=bgp.neighbor.del
请求 body：
{
"neighbor_id": "13.14.15.16",
"remote_as_id": 2
}
BGP 状态获取
Action: bgp.status.get
请求参数：无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=a5c149123abf65d3f6407bd95f88dd&action=bgp.status.get
响应参数：
名称 类型 范围 含义
status 整数 0-1 状态
as-id 整数 1-4294967295 AS-ID
redistribute_static 整数 0-1 静态路由重分发
redistribute_connected 整数 0-1 直连路由重分发
redistribute_vip 整数 0-1 SLB 虚拟服务地址重分发
redistribute_ospf 整数 0-1 OSPF 路由重分发
响应举例：
{
"status": 1,
"as-id": 1,
"redistribute_static": 1,
"redistribute_connected": 0,
"redistribute_ospf": 0,
"redistribute_vip": 1
}
BGP 状态设置
Action：bgp.status.set
请求参数：
名称 类型 范围 含义 必选 备注
status 整数 0-1 状态 是
as-id 整数 1-4294967295 AS-ID 是
redistribute_static 整数 0-1 静态路由重分发 否 缺省值:0
redistribute_connected 整数 0-1 直连路由重分发 否 缺省值:0
redistribute_vip 整数 0-1 SLB 虚拟服务地址重分发 否 缺省值:0
redistribute_ospf 整数 0-1 OSPF 路由重分发 否 缺省值:0
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=a5c149123abf65d3f6407bd95f88dd&action=bgp.status.set
请求 body：
{
"status": 1,
"as-id": 1,
"redistribute_static": 1,
"redistribute_connected": 0,
"redistribute_ospf": 0,
"redistribute_vip": 1
}

网络安全 DDOS
获取网络安全 DDOS 配置
Action：network.ddos.get
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.ddos.get
响应参数：
名称 类型 范围 含义
ip_option 整数 0-1 阻断含有 ip 的 option 报文
land_attack 整数 0-1 Land 攻击
dead_ping 整数 0-1 死 ping
fragment 整数 0-1 阻断分片报文
tcp_no_flag 整数 0-1 阻断没有 flag 的 tcp 报文
tcp_fault_flag 整数 0-1 阻断错误 flag 的 tcp 报文
tcp_syn_frag 整数 0-1 阻断对 tcp 的 syn 报文分了片的报文
响应举例：
{
"ip_option" : 0,
"land_attack" : 1,
"dead_ping" : 0,
"fragment" : 1,
"tcp_no_flag" : 1,
"tcp_fault_flag" : 1,
"tcp_syn_frag" : 1
}

    Tcp攻击包含三种攻击方式tcp_syn_frag，tcp_fault_flag，tcp_no_flag

设置网络安全 DDOS 配置
Action：network.ddos.set
请求参数：
名称 类型 范围 含义 必选 备注
ip_option 整数 0-1 阻断含有 ip 的 option 报文 否 缺省值:0
land_attack 整数 0-1 Land 攻击 否 缺省值:0
dead_ping 整数 0-1 死 ping 否 缺省值:0
fragment 整数 0-1 阻断分片报文 否 缺省值:0
tcp_no_flag 整数 0-1 阻断没有 flag 的 tcp 报文 否 缺省值:0
tcp_fault_flag 整数 0-1 阻断错误 flag 的 tcp 报文 否 缺省值:0
tcp_syn_frag 整数 0-1 阻断对 tcp 的 syn 报文分了片的报文 否 缺省值:0
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.ddos.set
请求 body：
{
"ip_option" : 0,
"land_attack" : 1,
"dead_ping" : 0,
"fragment" : 1,
"tcp_no_flag" : 1,
"tcp_fault_flag" : 1,
"tcp_syn_frag" : 1
}

网络安全 SYN 攻击
获取全局 SYN Cookie 配置
Action: slb.syn_cookie.get
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.syn_cookie.get
响应参数:
名称 类型 范围 含义
sfnum_cfg 整数 0,1 0 表示开启全局 SYN Cookie，0 表示关闭
sfnum_enable 整数 1-10000000 开启记录门限值
sfnum_relieve 整数 1-10000000 关闭记录门限值
响应举例：
{
"synflood": {
"sfnum_cfg": 1,
"sfnum_enable": 1000,
"sfnum_relieve": 100
}
}

设置全局 SYN Cookie 配置
Action: slb.syn_cookie.edit
请求参数:
名称 类型 范围 含义
sfnum_cfg 整数 0,1 0 表示开启全局 SYN Cookie，0 表示关闭
sfnum_enable 整数 1-10000000 开启记录门限值
sfnum_relieve 整数 1-10000000 关闭记录门限值

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.syn_cookie.edit
请求 Body:
{
"synflood": {
"sfnum_cfg": 1,
"sfnum_enable": 1000,
"sfnum_relieve": 100
}
}
获取每虚拟服务 SYN Cookie 配置
Action: slb.vs.syn_cookie.get
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.vs.syn_cookie.get
响应参数:
名称 类型 范围 含义
sfnum_cfg 整数 0,1 0 表示开启全局 SYN Cookie，0 表示关闭
sfnum_enable 整数 1-10000000 开启记录门限值
sfnum_relieve 整数 1-10000000 关闭记录门限值
sfnum_interval 整数 1-10 检测间隔，1 代表 100ms
响应举例：
{
"synflood": {
"sfnum_cfg": 1,
"sfnum_enable": 1000,
"sfnum_relieve": 100,
"sfnum_interval": 10
}
}
设置每虚拟服务 SYN Cookie 配置
Action: slb.vs.syn_cookie.edit
请求参数:
名称 类型 范围 含义
sfnum_cfg 整数 0,1 0 表示开启全局 SYN Cookie，0 表示关闭
sfnum_enable 整数 1-10000000 开启记录门限值
sfnum_relieve 整数 1-10000000 关闭记录门限值
sfnum_interval 整数 1-10 检测间隔，1 代表 100ms
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.vs.syn_cookie.edit
请求 Body:
{
"vs_synflood": {
"sfnum_cfg": 1,
"sfnum_enable": 1000,
"sfnum_relieve": 100,
"sfnum_interval": 10
}
}
流量控制
流量控制全局使能获取
Action：network.tc.global.get
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.global.get
响应参数：
名称 类型 范围 含义
enable 整数 0-1 流控使能
响应举例：
{
"enable": 0
}
流量控制全局使能设置
Action：network.tc.global.set
请求参数：
名称 类型 范围 含义 必选 备注
enable 整数 0-1 流控使能 是 0 表示全局关闭流控，1 表示全局开启流控;缺省值:0
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.global.set
请求 body：
{
"enable": 0
}
流量控制配置列表
Action：network.tc.list
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.list
响应参数：
名称 类型 范围 含义
tc_name 字符串 1-191 流控名称
fw_bandwidth 整数 1-100000000 上行带宽
rev_bandwidth 整数 1-100000000 下行带宽
响应举例：
[{
"tc_name": "bwall",
"fw_bandwidth": 100000,
"rev_bandwidth": 120000
}, {
"tc_name": "bwone",
"fw_bandwidth": 400000,
"rev_bandwidth": 500000
}]
Partition 中获取 common 中的流量控制列表
Action：network.tc.list.withcommon
请求参数：无
请求举例：
GET http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.list.withcommon
响应参数：
名称 类型 范围 含义
tc_name 字符串 1-191 流控名字
fw_bandwidth 整数 1-100000000 上行带宽
rev_bandwidth 整数 1-100000000 下行带宽
响应举例：
[{
"tc_name": "bwall",
"fw_bandwidth": 100000,
"rev_bandwidth": 120000
}, {
"tc_name": "bwone",
"fw_bandwidth": 400000,
"rev_bandwidth": 500000
},{
         "tc_name": "common/traffice_001",
         "fw_bandwidth": 1000,
         "rev_bandwidth": 20000
    }]
流量控制配置获取
Action：network.tc.get
请求参数：
名称 类型 范围 含义 必选 备注
tc_name 字符串 1-191 流控名字 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.get
请求 body：
{
"tc_name": "bwall"
}
响应参数：
名称 类型 范围 含义
tc_name 字符串 1-191 流控名字
fw_bandwidth 整数 1-100000000 上行带宽
rev_bandwidth 整数 1-100000000 下行带宽
响应举例：
{
"tc_name": "bwall",
"fw_bandwidth": 100000,
"rev_bandwidth": 120000
}
流量控制配置增加
Action：network.tc.add
请求参数：
名称 类型 范围 含义 必选 备注
tc_name 字符串 1-191 流控名字 是
fw_bandwidth 整数 1-100000000 上行带宽 是 单位 Kbps
rev_bandwidth 整数 1-100000000 下行带宽 是 单位 Kbps
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.add
请求 body：
{
"tc_name": "addbwall",
"fw_bandwidth": 100000,
"rev_bandwidth": 120000
}
流量控制配置编辑
Action：network.tc.edit
请求参数：
名称 类型 范围 含义 必选 备注
tc_name 字符串 1-191 流控名字 是
fw_bandwidth 整数 1-100000000 上行带宽 是 单位 Kbps
rev_bandwidth 整数 1-100000000 下行带宽 是 单位 Kbps
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.edit
请求 body：
{
"tc_name": "addbwall",
"fw_bandwidth": 200000,
"rev_bandwidth": 220000
}
流量控制配置删除
Action：network.tc.del
请求参数：
名称 类型 范围 含义 必选 备注
tc_name 字符串 1-191 流控名字 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.del
请求 body：
{
"tc_name": "addbwall"
}
流量控制 RULE 配置列表
Action：network.tc.rule.list
请求参数：
名称 类型 范围 含义 必选 备注
tc_name 字符串 1-191 流控名字 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.rule.list
请求 body：
{
"tc_name": "addbwall"
}
响应参数：
名称 类型 范围 含义
tc_name 字符串 1-191 流控名字
fw_bandwidth 整数 1-100000000 规则上行带宽
rev_bandwidth 整数 1-100000000 规则下行带宽
rule_name 字符串 1-191 规则名字
acl 整数 2-198 访问列表
acl_name 字符串 1-191 IPV6 访问列表
响应举例：
[{
"rule_name": "manager",
"fw_bandwidth": 50000,
"rev_bandwidth": 50000,
"acl": 2
}, {
"rule_name": "employee",
"fw_bandwidth": 20000,
"rev_bandwidth": 30000,
"acl": 3
}]

    创建rule规则时需要在已创建的流控中创建

流量控制 RULE 配置获取
Action：network.tc.rule.get
请求参数：
名称 类型 范围 含义 必选 备注
tc_name 字符串 1-191 流控名字 是 Key
rule_name 字符串 1-191 规则名字 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.rule.get
请求 body：
{
"tc_name": "bwall",
"rule_name": "manager"
}
响应参数：
名称 类型 范围 含义
tc_name 字符串 1-191 流控名字
fw_bandwidth 整数 1-100000000 规则上行带宽
rev_bandwidth 整数 1-100000000 规则下行带宽
rule_name 字符串 1-191 规则名字
acl 整数 2-198 访问列表
acl_name 字符串 1-191 IPV6 访问列表
响应举例：
{
"rule_name": "manager",
"fw_bandwidth": 50000,
"rev_bandwidth": 50000,
"acl": 2
}
流量控制 RULE 配置增加
Action：network.tc.rule.add
请求参数：
名称 类型 范围 含义 必选 备注
tc_name 字符串 1-191 流控名字 是 Key
fw_bandwidth 整数 1-100000000 规则上行带宽 是 单位 Kbps
rev_bandwidth 整数 1-100000000 规则下行带宽 是 单位 Kbps
rule_name 字符串 1-191 规则名字 是 Key
acl 整数 2-198 访问列表 是 必须存在
acl_name 字符串 1-191 IPV6 访问列表 是
basename 字符串 1-191 规则名 否 若不为空,必须存在
pos 整数 0-1 插入位置 否 如果 basename 不为空，pos 为 0，表示该规则插入 basename 之前，如果 pos 为 1，表示插入 basename 之后
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.rule.add
请求 body：
{
"tc_name": "bwall",
"rule_name": "inszero",
"fw_bandwidth": 600000,
"rev_bandwidth": 600000,
"acl": 2,
"basename": "manager",
"pos": 0
}
流量控制 RULE 配置编辑
Action：network.tc.rule.edit
请求参数：
名称 类型 范围 含义 必选 备注
tc_name 字符串 1-191 流控名字 是 Key
fw_bandwidth 整数 1-100000000 规则上行带宽 是 单位 Kbps
rev_bandwidth 整数 1-100000000 规则下行带宽 是 单位 Kbps
rule_name 字符串 1-191 规则名字 是 Key
acl 整数 2-198 访问列表 是
acl_name 字符串 1-191 IPV6 访问列表 是
basename 字符串 1-191 规则名 否
pos 整数 0-1 插入位置 否 如果 basename 不为空，pos 为 0，表示该规则插入 basename 之前，如果 pos 为 1，表示插入 basename 之后
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.rule.edit
请求 body：
{
"tc_name": "bwall",
"rule_name": "inszero",
"fw_bandwidth": 600000,
"rev_bandwidth": 600000,
"acl": 2,
"basename": "manager",
"pos": 1
}
流量控制 RULE 配置删除
Action：network.tc.rule.del
请求参数：
名称 类型 范围 含义 必选 备注
tc_name 字符串 1-191 流控名字 是
rule_name 字符串 1-191 规则名字 是
请求举例：
POST http://192.168.70.63/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=network.tc.rule.del
请求 body：
{
"tc_name": "bwall",
"rule_name": "inszero"
}
