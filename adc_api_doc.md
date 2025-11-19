







应用交付产品
API手册_SLB







上海弘积信息科技有限公司
弘积科技®
上海市浦东新区新金桥路36号上海国际财富中心南塔
电话：+021-61649161
服务热线：+400-100-8186
https://www.horizon-adn.com

版权声明
本手册中的所有内容及格式的版权属于上海弘积信息科技有限公司（以下简称弘积科技）所有，未经弘积科技许可，任何人不得仿制、拷贝、转译或任意引用。
版权所有 不得翻印 © 2014-2024 上海弘积信息科技有限公司
商标声明
本手册中所谈及的产品名称仅做识别之用。手册中涉及的其他公司的注册商标或是版权属各商标注册人所有，恕不逐一列明。
HORIZON® 上海弘积信息科技有限公司
目录
总则	5
Authkey 认证密钥	5
URL  API使用的URL	5
Method API使用的HTTP method	5
文件上传	5
必选参数	5
可选参数	5
响应内容	5
登陆和登出	6
登陆	6
登出	6
概括_资源统计	7
SLB服务器负载均衡	13
虚拟服务	13
SLB会话清除	13
节点	14
服务池	36
虚拟地址	57
虚拟服务	87
模板	112
TCP模板	120
健康检查	227
健康检查添加	227
健康检查列表	254
健康检查编辑	262
健康检查获取	263
健康检查删除	263
健康检查脚本列表	264
健康检查脚本上传	264
健康检查脚本删除	264
健康检查POST文件列表	265
健康检查POST文件上传	265
健康检查POST文件删除	266
健康检查检测	266
健康检查测试列表	266
添加健康检查测试	266
获取健康检查测试	267
删除健康检查测试	268
被动健康检查	268
添加被动健康检查配置	268
获取被动健康检查配置列表	269
获取指定被动健康检查配置	270
编辑指定被动健康检查配置	271
删除指定被动健康检查配置	272
ERULE	272
erule上传	272
erule在线编辑	272
erule删除	273
erule列表	273
erule服务器文件上传	274
erule服务器文件删除	274
erule服务器文件列表	274
连接保持	275
Cookie连接保持	275
源地址连接保持	279
目的地址连接保持	283
SSL连接保持	287
加速	290
缓存	290
连接复用	297
SSL卸载	300
策略	342
黑白名单	342
规则表	343
策略	351
Web安全	362
WAF模板	362
WAF规则	369
全局选项	373
SLB全局混杂设置	373
SLB全局软关机设置	374
SLB全局ICMP速率限制	375
SLB全局TCP新建保护	376
SLB全局VLAN一致性检查	376
SLB全局连接镜像	377
SLB全局路径保持	378
SLB全局地址转换	379
SLB全局虚拟MAC	380







总则
Authkey 认证密钥
除登陆API以外的API,都需要使用登陆API获取的authkey,authkey默认超时时间为10分钟,当超时或者登出以后,authkey立即失效。
URL  API使用的URL
除特殊说明的情况之外,所有API的URL格式都为
<protocol>://<host>:<port>/adcapi/v2.0/?authkey=<authkey>&action=<action>
其中参数说明如下：
名称	含义
<protocol>	使用API的协议,HTTP 或者HTTPS
<host>	目标设备的IP地址
<port>	目标设备的IP地址HTTP/HTTPS 端口,
当为该协议默认端口(HTTP:80,HTTPS:443)可以省略
<authkey>	通过login API获取的authkey
<action>	API的action字段,具体见各个API
Method API使用的HTTP method
若未特殊说明,当无请求参数时使用GET,有请求参数时使用POST
文件上传
文件上传时,使用form-data的方式上传,此时如果有请求参数,需要在URL中携带参数,具体请查看对应API
必选参数
执行API时,对于必选参数,必须明确指定该参数。
可选参数
执行API时,对于可选参数,不指定可选参数时,会使用缺省值。
当一个API全是可选参数时,至少需要指定其中一个参数。
响应内容
对于获取信息类的API,包括所有以(.get/.list/.stats/.statis)结尾的action的API,响应内容为标准JSON格式内容
具体内容请查看对于API说明
对于配置类的API,包括所有以(.add/.edit/.del/.set/.apply)结尾的action的API,响应内容为{"result":"success"}，不再在每个API中进行描述
登出的API(logout)的响应内容同配置类API的响应内容，为{"result":"success"}
对于文件下载类的API, 响应内容为文件内容 (application/octet-stream)
对于文件上传类的API, 响应内容同配置类API的响应内容,为{"result":"success"}
其它所有未对响应内容做特殊说明的API, 响应内容为{"result":"success"}
对于出错的情况, 响应内容为{"result":"error","errcode":<errcode>,"errmsg":<errmsg>}
其中参数说明如下：
名称	含义
<errcode>	错误码,为一个数字
<errmsg>	错误消息,为一个字符串


登陆和登出
登陆
Action:  login
请求参数:
名称	类型	范围	含义	必选	备注
username	字符串	长度1-63	用户名	是	
password	字符串	长度1-63	密码	是	

请求举例：
POST  http://192.168.70.73/adcapi/v2.0/?action=login
Body:{"username":"admin","password":"admin"}
 响应参数:
名称	类型	范围	含义
authkey	字符串		认证密钥,后续其它所有API请求需要在URL中携带该值
响应举例：
{
  "authkey": "dbc121e55cc33c67911a99ce4829db" 
}
	每次login会生成一个authkey,设备能同时支持的authkey的数量是有限的,
因此在使用完成后需要使用logout使该authkey失效

登出
Action:  logout
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=logout
	登出后该authkey不再有效.
概括_资源统计
获取服务器负载均衡资源列表

Action:slb.resource_statistics.list

响应参数: 
名称	类型	范围	含义
type
	类型	无	获取的类型
in_total
	整数	根据参数规格限制	统计的资源总数
up
	整数	根据参数规格限制	正常的资源统计数
down	整数	根据参数规格限制	故障的资源统计数
some-up	整数	根据参数规格限制	部分正常的资源统计数
disable	整数	根据参数规格限制	禁用的的资源统计数
请求举例：
POST 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.resource_statistics.list
[
    {
        "type": "Virtual-Address",
        "in_total": 103,
        "up": 2,
        "down": 99,
        "some_up": 2,
        "disable": 0
    },
    {
        "type": "Virtual-Server",
        "in_total": 205,
        "up": 5,
        "down": 200,
        "some_up": 0,
        "disable": 0
    },
    {
        "type": "Pool",
        "in_total": 341,
        "up": 127,
        "down": 214,
        "some_up": 0,
        "disable": 0
    },
    {
        "type": "Node",
        "in_total": 567,
        "up": 567,
        "down": 0,
        "some_up": 0,
        "disable": 0
    },
    {
        "type": "Node-Port",
        "in_total": 1520,
        "up": 1520,
        "down": 0,
        "some_up": 0,
        "disable": 0
    }
]

获取网络服务资源列表

Action:network.resource_statistics.list

响应参数: 
名称	类型	范围	含义
part
	区域	字符串	分区名称
snatpool
	整数	根据参数规格限制	统计的snat pool资源数
nat_address	整数	根据参数规格限制	统计的nat地址资源总数
static_nat	整数	根据参数规格限制	统计的静态nat资源数
vlan	整数	根据参数规格限制	统计的vlan资源数
ve	整数	根据参数规格限制	统计的虚拟接口的资源数
Trunk
	整数	根据参数规格限制	统计的汇聚接口的资源数
ipv4_acl
	整数	根据参数规格限制	统计的ipv4标准访问列表的资源数
ipv4_acl
	整数	根据参数规格限制	统计的ipv6标准访问列表的资源数
请求举例：
POST 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=network.resource_statistics.list

[
    {
        "part": "common",
        "snatpool": 110,
        "nat_address": 1314,
        "static_nat": 105,
        "vlan": 4,
        "ve": 3,
        "trunk": 1,
        "ipv4_acl": 2,
        "ipv6_acl": 2
    }
]

获取全部分区网络服务资源列表
Action:network.resource_statistics.list.all_partition

响应参数: 
名称	类型	范围	含义
part
	区域	字符串	分区名称
snatpool
	整数	根据参数规格限制	统计的snat pool资源数
nat_address	整数	根据参数规格限制	统计的nat地址资源总数
static_nat	整数	根据参数规格限制	统计的静态nat资源数
vlan	整数	根据参数规格限制	统计的vlan资源数
ve	整数	根据参数规格限制	统计的虚拟接口的资源数
Trunk
	整数	根据参数规格限制	统计的汇聚接口的资源数
ipv4_acl
	整数	根据参数规格限制	统计的ipv4标准访问列表的资源数
ipv4_acl
	整数	根据参数规格限制	统计的ipv6标准访问列表的资源数
请求举例：
POST 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=network.resource_statistics.list.all_partition


[
    {
        "part": "common",
        "snatpool": 110,
        "nat_address": 1314,
        "static_nat": 105,
        "vlan": 4,
        "ve": 3,
        "trunk": 1,
        "ipv4_acl": 2,
        "ipv6_acl": 2
    },
    {
        "part": "partition_1",
        "snatpool": 0,
        "nat_address": 102,
        "static_nat": 101,
        "vlan": 2,
        "ve": 2,
        "trunk": 0,
        "ipv4_acl": 0,
        "ipv6_acl": 0
    },
    {
        "part": "ALL-Partition-Total",
        "snatpool": 110,
        "nat_address": 1416,
        "static_nat": 206,
        "ipv6_acl": 2,
        "ipv4_acl": 2,
        "trunk": 1,
        "ve": 5,
        "vlan": 6
    }
]
获取模板资源统计列表
Action:profile.resource_statistics.list

响应参数: 
名称	类型	范围	含义
type	类型	字符串	模板类型
in_total
	整数	根据参数规格限制	统计的模板资源数

请求举例：
POST 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=profile.resource_statistics.list

[
    {
        "type": "TCP-Agent",
        "in_total": 1
    },
    {
        "type": "UDP",
        "in_total": 0
    },
    {
        "type": "TCP",
        "in_total": 4
    },
    {
        "type": "HTTP",
        "in_total": 3
    },
    {
        "type": "HTTP2",
        "in_total": 2
    },
    {
        "type": "SIP",
        "in_total": 2
    },
    {
        "type": "DNS",
        "in_total": 1
    },
    {
        "type": "SMTP",
        "in_total": 0
    },
    {
        "type": "RTSP",
        "in_total": 1
    },
    {
        "type": "FTP",
        "in_total": 1
    },
    {
        "type": "Request-Log",
        "in_total": 3
    },
    {
        "type": "Virtual-Server",
        "in_total": 1
    },
    {
        "type": "nat-Log",
        "in_total": 2
    },
    {
        "type": "DNS-Log",
        "in_total": 3
    },
    {
        "type": "SSL-Client",
        "in_total": 6
    },
    {
        "type": "SSL-Server",
        "in_total": 1
    },
    {
        "type": "Cookie",
        "in_total": 2
    },
    {
        "type": "Source-Address",
        "in_total": 0
    },
    {
        "type": "Dest-Address",
        "in_total": 2
    },
    {
        "type": "SSL-Session-ID",
        "in_total": 1
    },
    {
        "type": "BW-List",
        "in_total": 1
    },
    {
        "type": "RuleTable",
        "in_total": 3
    },
    {
        "type": "Policy",
        "in_total": 2
    },
    {
        "type": "WAF",
        "in_total": 1
    },
    {
        "type": "Conn-Multiplex",
        "in_total": 1
    },
    {
        "type": "Cache",
        "in_total": 0
    },
    {
        "type": "Traffic-Control",
        "in_total": 0
    }
]


获取SSL资源统计列表
Action:ssl.resource_statistics.list
响应参数: 
名称	类型	范围	含义
part
	区域	字符串	分区名称
cert	证书	根据参数规格限制	统计的证书资源数
key	私钥	根据参数规格限制	统计的私钥资源数
crl	证书吊销列表	根据参数规格限制	统计的证书吊销列表资源数

请求举例：
POST 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=ssl.resource_statistics.list

[
    {
        "part": "common",
        "cert": 4,
        "key": 3,
        "crl": 0
    }
]

SLB服务器负载均衡
虚拟服务
SLB资源数量
Action:  slb.states.list
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.states.list
请求body ：
    {
        "vs":1,
        "pool": 1,
        "node": 1
}
响应参数:
名称	类型	范围	含义
vs	整数	0,1	设备虚拟服务信息，字段的值为1，则获取虚拟地址对应的所有状态，字段的值为0，则不获取虚拟地址的状态
由以下信息组成的vs数组：
vs > total：
类型：整数；  
含义：字段代表总的个数,字段的值是其它字段值之和；
范围：最小为256，最大为4096，默认是1024个，
vs > up：
类型：整数；  
含义：全部正常的个数；
范围：0-4096，
vs > down：
类型：整数；  
含义：故障&&禁用的个数；
范围：0-4096，
vs > ：some_up
类型：整数；  
含义：代表部分正常的个数；
范围：0-4096，
pool	整数	0-1	设备服务池信息,字段的值为1，则获取服务池对应的所有状态，字段的值为0，则不获取服务池的状态
由以下信息组成的pool数组：
pool > total：
类型：整数；  
含义：字段代表总的个数,字段的值是其它字段值之和；
范围：最小为512，最大为4096，默认是1024个，
pool  > up：
类型：整数；  
含义：全部正常的个数；
范围：0-4096，
pool  > down：
类型：整数；  
含义：故障&&禁用的个数；
范围：0-4096，
pool  > ：some_up
类型：整数；  
含义：代表部分正常的个数；
范围：0-4096，
node	整数	0-1	设备节点信息,字段的值为1，则获取节点对应的所有状态，字段的值为0，则不获取节点的状态
由以下信息组成的node数组：
node > total：
类型：整数；  
含义：字段代表总的个数,字段的值是其它字段值之和；
范围：最小为512，最大为4096，默认是1024个，
node  > up：
类型：整数；  
含义：全部正常的个数；
范围：0-4096，
node  > down：
类型：整数；  
含义：故障&&禁用的个数；
范围：0-4096，
node  > ：some_up
类型：整数；  
含义：代表部分正常的个数；
范围：0-4096，
响应举例：
    {
        "vs": {
            "total": 3,
            "up": 1,
            "down": 1,
            "some_up": 1
        }，
        "pool": {
            "total": 3,
            "up": 2,
            "down": 0,
            "some_up": 1
        }
        "node": {
            "total": 3,
            "up": 3,
            "down": 0,
            "some_up": 0
        }
}
	注意：现在只显示total 、up 、down、 someup。其他的状态不显示（暖启动显示为up，其他显示为故障）


SLB会话清除
Action:  slb.session.clear
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.session.clear

	清除会话会导致当前会话中断,请谨慎操作
节点
节点(node)列表
Action:  slb.node.list
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.list
响应参数:
名称	类型	范围	含义
tc_name	字符串	长度1-191	流量控制模版名称
graceful_time	整数	0-65535	软关机超时，单位秒
由软关机信息组成的数组，支持参数如下：
graceful_time > graceful_delete：
类型：整数；  
范围：0-1；
含义：删除节点触发软关机，1启用，0禁用，
graceful_time > graceful_disable：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机，1启用，0禁用，
graceful_time > graceful_persist：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机后会话保持表有效，1启用，0禁用

name	字符串	长度1-191	节点名称
host	字符串	长度1-191	节点主机名或IP地址
weight	整数	1-100	节点权重，
healthcheck	字符串	长度0-191	节点关联的健康检查名
status	整数	0,1	节点使能状态，1:启用，0禁用，
conn_limit	整数	0-8000000	节点连接限制, 8000000表示不限制,0表示不配置
desc_rserver	字符串	长度1-191	描述
ports	数组	不涉及	节点端口列表
由节点端口信息组成的数组，支持参数如下：
ports > port_number：
类型：整数；  
范围：0-65534；
含义：端口号，
ports > protocol：
类型：整数；  
范围：0,1；
含义：协议类型，
ports > status：
类型：整数；  
范围：0,1；
含义：端口使能状态，
ports >weight：
类型：整数；  
范围：1-100；
含义：端口权重，
ports >gracefule_time：
类型：整数；  
范围：0-65535；
含义：软关机超时单位秒，
ports > graceful_delete：
类型：整数；  
范围：0-1；
含义：删除节点触发软关机，1启用，0禁用，
ports > graceful_disable：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机，1启用，0禁用，
ports > graceful_persist：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机后会话保持表有效，1启用，0禁用
ports >conn_limit：
类型：整数；  
范围：0-8000000；
含义：端口连接限制，
ports >phm_profile：
类型：字符串；  
范围：0-191；
含义：被动健康检查名称，
ports >healthcheck：
类型：字符串；  
范围：0-191；
含义：动健康检查名称，
ports >upnum：
类型：整数；  
范围：0-15；
含义：可用性要求  0 代表所有，
ports >nat_strategy：
类型：字符串；  
范围：0-191；
含义：nat策略名，
slow_start_type	整数	0,1	暖启动类型；0表示连接限制，1表示连接速率限制
slow_start_recover	整数	0-3600	暖启动恢复时间
slow_start_rate	整数	0,1	暖启动变化规则；0表示倍数增加，1表示线性增加
slow_start_from	整数	1-65535	暖启动初始量
slow_start_step	整数	2-10	暖启动增量
slow_start_interval	整数	1-60	暖启动间隔，单位为秒
slow_start_interval_num	整数	1-100	暖启动间隔数
slow_start_tail	整数	1-65535	暖启动结束量
cl-log	字符串	0,1	连接限制日志
request_rate_limit	整数	0-1048575	请求速率限制，0表示不配置
conn_rate_limit	整数	1-1000000	连接速率限制
template	字符串	长度0-191	与速率限制关联使用，创建新的节点模板对该ip进行速率限制
响应举例：
[
  {
    "tc_name": ""，
    "graceful_time":	50,
"graceful_delete":	1,
"graceful_disable":	1,
"graceful_persist":	1, 
    "name": "192.168.1.100",  
    "host": "192.168.1.100",   
    "weight": 2,            
    "healthcheck": "ping",      
    "status": 1,               
"conn_limit": 123, 
"template": "192.168.1.100",
"conn_rate_limit": 2011,
"request_rate_limit": 123123,      
    "desc_rserver": "iamnode1",   
    "ports": [               
      {
        "port_number": 80,  
        "protocol": 0,       
        "status": 1,  
        "weight": 12,          
        "conn_limit": 8000000,   
        "phm_profile": "default",  
        "healthcheck": "ping"    
      }
    ]
  }
]
分区中获取common分区和自己分区的节点列表
Action:  slb.node.list.withcommon
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.list.withcommon
响应参数：

响应举例：
 {
        "tc_name": "",
        "graceful_time": 0,
        "graceful_delete": 0,
        "graceful_disable": 0,
        "graceful_persist": 0,
        "name": "common/192.168.1.102",
        "host": "192.168.1.102",
        "weight": 1,
        "healthcheck": "",
        "upnum": 0,
        "status": 1,
"request_rate_limit": 123123,
        "desc_rserver": "",
        "template": "default",
        "ports": [
            {
                "port_number": 80,
                "protocol": 0,
                "status": 1,
                "weight": 1,
                "graceful_time": 0,
                "graceful_delete": 0,
                "graceful_disable": 0,
                "graceful_persist": 0,
                "phm_profile": "",
                "healthcheck": "",
                "upnum": 0,
                "nat_strategy": ""
            }
        ]
    },
    {
        "tc_name": "",
        "graceful_time": 0,
        "graceful_delete": 0,
        "graceful_disable": 0,
        "graceful_persist": 0,
        "name": "117.255.255.23",
        "host": "117.255.255.23",
        "weight": 1,
        "healthcheck": "",
        "upnum": 0,
        "status": 1,
        "desc_rserver": "",
        "template": "default",
        "ports": [
            {
                "port_number": 80,
                "protocol": 0,
                "status": 1,
                "graceful_time": 0,
                "graceful_delete": 0,
                "graceful_disable": 0,
                "graceful_persist": 0,
                "phm_profile": "",
                "healthcheck": "",
                "upnum": 0,
                "nat_strategy": ""
            }
        ]
    }
]

节点(node)获取
Action:  slb.node.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	节点名称	是	


请求举例：
POST 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.get
请求body
{
    "name": "192.168.1.100"    
}
响应参数:
名称	类型	范围	含义
tc_name	字符串	长度1-191	流量控制模版名称
graceful_time	整数	0-65535	软关机超时，单位秒
由软关机信息组成的数组，支持参数如下：
graceful_time > graceful_delete：
类型：整数；  
范围：0-1；
含义：删除节点触发软关机，1启用，0禁用，
graceful_time > graceful_disable：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机，1启用，0禁用，
graceful_time > graceful_persist：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机后会话保持表有效，1启用，0禁用
name	字符串	长度1-191	节点名称
host	字符串	长度1-191	节点主机名或IP地址
weight	整数	1-100	节点权重，
healthcheck	字符串	长度0-191	节点关联的健康检查名
status	整数	0,1	节点使能状态，1:启用，0禁用，
conn_limit	整数	0-8000000	节点连接限制, 8000000表示不限制,0表示不配置
desc_rserver	字符串	长度1-191	描述
ports	数组	不涉及	节点端口列表
由节点端口信息组成的数组，支持参数如下：
ports > port_number：
类型：整数；  
范围：0-65534；
含义：端口号，
ports > protocol：
类型：整数；  
范围：0,1；
含义：协议类型，
ports > status：
类型：整数；  
范围：0,1；
含义：端口使能状态，
ports >weight：
类型：整数；  
范围：1-100；
含义：端口权重，
ports >gracefule_time：
类型：整数；  
范围：0-65535；
含义：软关机超时单位秒，
ports > graceful_delete：
类型：整数；  
范围：0-1；
含义：删除节点触发软关机，1启用，0禁用，
ports > graceful_disable：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机，1启用，0禁用，
ports > graceful_persist：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机后会话保持表有效，1启用，0禁用
ports >conn_limit：
类型：整数；  
范围：0-8000000；
含义：端口连接限制，
ports >phm_profile：
类型：字符串；  
范围：0-191；
含义：被动健康检查名称，
ports >healthcheck：
类型：字符串；  
范围：0-191；
含义：动健康检查名称，
ports >upnum：
类型：整数；  
范围：0-15；
含义：可用性要求  0 代表所有，
ports >nat_strategy：
类型：字符串；  
范围：0-191；
含义：nat策略名，
ports >nat_strategy：
类型：数组；  
范围：不涉及；
含义：可用性，
ports > availability >status ：
类型：整数；  
范围：0-1；
含义：服务池成员是否启用，
ports > availability >hc_reason ：
类型：对象；  
范围：不涉及；
含义：健康检查结果集合，
ports > availability >hc_reason > reasons：
类型：数组；  
范围：不涉及；
含义：健康检查结果，
ports > availability >hc_reason > reasons > wiyhhc：
类型：整数；  
范围：0-1及；
含义：健康检查状态，
ports > availability >hc_reason > reasons > state：
类型：字符串；  
范围：不涉及；
含义：健康检查状态，up或down，
ports > availability >hc_reason > reasons > hcname：
类型：字符串；  
范围：1-191；
含义：健康检查名字，
ports > availability >hc_reason > reasons >reason：
类型：字符串；  
范围：1-191；
含义：健康检查失败原因，
slow_start_type	整数	0,1	暖启动类型；0表示连接限制，1表示连接速率限制
slow_start_recover	整数	0-3600	暖启动恢复时间
slow_start_rate	整数	0,1	暖启动变化规则；0表示倍数增加，1表示线性增加
slow_start_from	整数	1-65535	暖启动初始量
slow_start_step	整数	2-10	暖启动增量
slow_start_interval	整数	1-60	暖启动间隔，单位为秒
slow_start_interval_num	整数	1-100	暖启动间隔数
slow_start_tail	整数	1-65535	暖启动结束量
upnum	整数	0-15	可用性要求  0 代表所有
cl-log	字符串	0,1	连接限制日志
request_rate_limit	整数	0-1048575	请求速率限制，0表示不配置
conn_rate_limit	整数	1-1000000	连接速率限制
template	字符串	长度0-191	与速率限制关联使用，创建新的节点模板对该ip进行速率限制
响应举例：
{
       "tc_name": "",
       "graceful_time": 0,
       "graceful_delete": 0,
       "graceful_disable": 0,
       "graceful_persist": 0,
       "name": "192.168.1.100",
       "host": "192.168.1.100",
       "weight": 1,
       "healthcheck": "dns https sip",
       "upnum": 0,
       "status": 1,
       "conn_limit": 0,
"template": "192.168.1.100",
        "conn_rate_limit": 2011,
"request_rate_limit": 123123,
       "cl_log": 1,
       "desc_rserver": "",
       "template": "default",
       "ports": [
              {
                     "port_number": 81,
                     "protocol": 0,
                     "status": 1,

                     "weight": 1,
                     "conn_limit": 0,
                     "conn_limit_log": 1,
                     "graceful_time": 0,
                     "graceful_delete": 0,
                     "graceful_disable": 0,
                     "graceful_persist": 0,
                     "phm_profile": "",
                     "healthcheck": "",
                     "upnum": 0,
                     "nat_strategy": "default",
                     "availability": {
                            "status": "Down",
                            "hc_reason": {
                                   "reasons": [
                                          {
                                                 "withhc": 0,
                                                 "state": "down",
                                                 "reason": "Node Down"
                                          }
                                   ]
                            }
                     }
              }
       ],
       "availability": {
              "status": "Down",
              "hc_reason": {
                     "reasons": [
                            {
                                   "withhc": 1,
                                   "state": "down",
                                   "hcname": "dns",
                                   "reason": "DNS timeout"
                            },
                            {
                                   "withhc": 1,
                                   "state": "down",
                                   "hcname": "https",
                                   "reason": "HTTPS timeout"
                            },
                            {
                                   "withhc": 1,
                                   "state": "down",
                                   "hcname": "sip",
                                   "reason": "SIP timeout"
                            }
                     ]
              }
       }
}

节点(node)添加
Action:  slb.node.add
请求参数:
名称	类型	范围	含义
tc_name	字符串	长度1-191	流量控制模版名称
graceful_delete	整数	0,1	删除节点触发软关机，1启用，0禁用，
graceful_disable	整数	0,1	禁用节点触发软关机，1启用，0禁用，
graceful_persist	整数	0,1	禁用节点触发软关机后会话保持表有效，1启用，0禁用，
graceful_time	整数	0-65535	软关机超时，单位秒
name	字符串	长度1-191	节点名称
host	字符串	长度1-191	节点主机名或IP地址
weight	整数	1-100	节点权重，
healthcheck	字符串	长度0-191	节点关联的健康检查名
status	整数	0,1	节点使能状态，1:启用，0禁用，
conn_limit	整数	0-8000000	节点连接限制, 8000000表示不限制,0表示不配置
desc_rserver	字符串	长度1-191	描述
ports	数组	不涉及	节点端口列表
由节点端口信息组成的数组，支持参数如下：
ports > port_number：
类型：整数；  
范围：0-65534；
含义：端口号，
ports > protocol：
类型：整数；  
范围：0,1；
含义：协议类型，
ports > status：
类型：整数；  
范围：0,1；
含义：端口使能状态，
ports >weight：
类型：整数；  
范围：1-100；
含义：端口权重，
ports >gracefule_time：
类型：整数；  
范围：0-65535；
含义：软关机超时单位秒，
ports > graceful_delete：
类型：整数；  
范围：0-1；
含义：删除节点触发软关机，1启用，0禁用，
ports > graceful_disable：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机，1启用，0禁用，
ports > graceful_persist：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机后会话保持表有效，1启用，0禁用
ports >conn_limit：
类型：整数；  
范围：0-8000000；
含义：端口连接限制，
ports >phm_profile：
类型：字符串；  
范围：0-191；
含义：被动健康检查名称，
ports >healthcheck：
类型：字符串；  
范围：0-191；
含义：动健康检查名称，
ports >upnum：
类型：整数；  
范围：0-15；
含义：可用性要求  0 代表所有，
ports >nat_strategy：
类型：字符串；  
范围：0-191；
含义：nat策略名，
slow_start_type	整数	0,1	暖启动类型；0表示连接限制，1表示连接速率限制
slow_start_recover	整数	0-3600	暖启动恢复时间
slow_start_rate	整数	0,1	暖启动变化规则；0表示倍数增加，1表示线性增加
slow_start_from	整数	1-65535	暖启动初始量
slow_start_step	整数	2-10	暖启动增量
slow_start_interval	整数	1-60	暖启动间隔，单位为秒
slow_start_interval_num	整数	1-100	暖启动间隔数
slow_start_tail	整数	1-65535	暖启动结束量
upnum	整数	0-15	可用性要求  0 代表所有
cl-log	字符串	0,1	连接限制日志
request_rate_limit	整数	0-1048575	请求速率限制，0表示不配置
conn_rate_limit	整数	1-1000000	连接速率限制
template	字符串	长度0-191	与速率限制关联使用，创建新的节点模板对该ip进行速率限制

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.add
请求body
{
    "node": {
        "tc_name": "",
        "graceful_time": 0,  
        "graceful_delete": 0,
        "graceful_disable": 0,
        "graceful_persist": 0,
        "name": "192.168.1.123",
        "host": "192.168.1.123",
        "domain_ip_version": 0,
        "weight": 1,
        "healthcheck": "",
        "upnum": 0,
        "status": 1,
        "conn_limit": 123,
"template":"192.168.1.123",
        "conn_rate_limit":2011,
        "cl_log": 1,
        "desc_rserver": "",
        "ports": [
            {
                "port_number": 80,
                "protocol": 0,
                "status": 1,
                "weight": 1,
                "conn_limit": 0,
                "conn_limit_log": 1,
                "graceful_time": 0,
                "graceful_delete": 0,
                "graceful_disable": 0,
                "graceful_persist": 0,
                "phm_profile": "",
                "healthcheck": "",
                "upnum": 0,
                "nat_strategy": ""
            }
        ]
    }
}

节点(node)编辑
Action:  slb.node.edit
请求参数:
名称	类型	范围	含义	必选	备注
node	对象	不涉及	节点对象	是	
tc_name	字符串	长度1-191	流量控制模版名称	否	缺省值 空字符串"",表示没有流控
graceful_delete	整数	0,1	删除节点触发软关机	否	1启用，0禁用，缺省值 0
graceful_disable	整数	0,1	禁用节点触发软关机	否	1启用，0禁用，缺省值 0
graceful_persist	整数	0,1	禁用节点触发软关机后会话保持表有效	否	1启用，0禁用，缺省值 0
graceful_time	整数	0-65535	软关机超时，单位秒	否	缺省值 0，0表示永远不超时
name	字符串	长度1-191	节点名称	是	节点必须存在
host	字符串	长度1-191	节点主机名或IP地址	是	
weight	整数	1-100	节点权重	否	缺省值 1
healthcheck	字符串	长度0-191	节点关联的健康检查名	否	缺省值 空字符串"",表示没有检查
status	整数	0,1	节点使能状态，	否	1:启用，0禁用，缺省值1
conn_limit	整数	0-8000000	节点连接限制,	否	缺省值8000000表示不限制，0表示不配置
desc_rserver	字符串	长度1-191	描述	否	缺省值 空字符串""
slow_start_type	整数	0,1	暖启动类型	否	0表示连接限制，1表示连接速率限制；缺省值：0
slow_start_recover	整数	0-3600	暖启动恢复时间	否	缺省值：15
slow_start_rate	整数	0,1	暖启动变化规则	否	0表示倍数增加，1表示线性增加；缺省值：0
slow_start_from	整数	1-65535	暖启动初始量	否	缺省值：128
slow_start_step	整数	2-10	暖启动增量	否	缺省值：2
slow_start_interval	整数	1-60	暖启动间隔，单位为秒	否	缺省值：10
slow_start_interval_num	整数	1-100	暖启动间隔数	否	缺省值：6
slow_start_tail	整数	1-65535	暖启动结束量	否	缺省值：4096
request_rate_limit	整数	0-1048575	请求速率限制	否	缺省值 0，0表示不配置
conn_rate_limit	整数	1-1000000	连接速率限制		
template	字符串	长度0-191	与速率限制关联使用，创建新的节点模板对该ip进行速率限制	否	

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.edit
请求body
{
    "node":{                
		"tc_name":"",
		"graceful_time":50,
		"graceful_delete":1,
		"graceful_disable":1,
		"graceful_persist":1,
		"name":"192.168.1.123",
		"host":"192.168.1.123",
		"weight":2,
		"healthcheck":"ping",
		"status":1,
        "request_rate_limit":123123,
		"conn_limit":123,
        "template":"192.168.1.123",
        "conn_rate_limit":2011,
		"desc_rserver":"iamnode1"
    }
}
节点(node)编辑针对operator用户
Action:  slb.node.onoff
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	节点名称	是	节点必须存在
host	字符串	长度1-191	节点主机名或IP地址	是	
status	整数	0,1	节点使能状态，	否	1:启用，0禁用，缺省值1

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.onoff
请求body
{
    "node":{                
		"name": "120.1.129.100",
		"host": "120.1.129.100",
		"status": 1

    }
}


节点(node)删除
Action:  slb.node.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	节点名称	是	节点必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.del
请求body
{
    "name":"192.168.1.123"
}

节点端口(node.port)添加
Action:  slb.node.port.add
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	节点名称	是	节点必须存在
port	对象	不涉及	节点对象	是	节点端口列表
由节点端口信息组成的数组，支持参数如下：
ports > port_number：
类型：整数；  
范围：0-65534；
含义：端口号，
ports > protocol：
类型：整数；  
范围：0,1；
含义：协议类型，
ports > status：
类型：整数；  
范围：0,1；
含义：端口使能状态，
ports >weight：
类型：整数；  
范围：1-100；
含义：端口权重，
ports >gracefule_time：
类型：整数；  
范围：0-65535；
含义：软关机超时单位秒，
ports > graceful_delete：
类型：整数；  
范围：0-1；
含义：删除节点触发软关机，1启用，0禁用，
ports > graceful_disable：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机，1启用，0禁用，
ports > graceful_persist：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机后会话保持表有效，1启用，0禁用
ports >conn_limit：
类型：整数；  
范围：0-8000000；
含义：端口连接限制，
ports >phm_profile：
类型：字符串；  
范围：0-191；
含义：被动健康检查名称，
ports >healthcheck：
类型：字符串；  
范围：0-191；
含义：动健康检查名称，
ports >upnum：
类型：整数；  
范围：0-15；
含义：可用性要求  0 代表所有，
ports >nat_strategy：
类型：字符串；  
范围：0-191；
含义：nat策略名，

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.port.add
请求body
{
    "name" : "192.168.1.123",
    "port" : {
        "port_number" : 890,
        "protocol" : 0,
        "status" : 1,
        "weight" : 1,
        "conn_limit" : 8000000,
        "graceful_time" : 0,
        "graceful_delete" : 0,
        "graceful_disable" : 0,
        "graceful_persist" : 0,
        "phm_profile" : "",
        "healthcheck" :  "",
        "nat_strategy" : ""
    }
}
节点端口(node.port)编辑
Action:  slb.node.port.edit
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	节点名称	是	节点必须存在
port	对象	不涉及	节点对象	是	节点端口列表
由节点端口信息组成的数组，支持参数如下：
ports > port_number：
类型：整数；  
范围：0-65534；
含义：端口号，
ports > protocol：
类型：整数；  
范围：0,1；
含义：协议类型，
ports > status：
类型：整数；  
范围：0,1；
含义：端口使能状态，
ports >weight：
类型：整数；  
范围：1-100；
含义：端口权重，
ports >gracefule_time：
类型：整数；  
范围：0-65535；
含义：软关机超时单位秒，
ports > graceful_delete：
类型：整数；  
范围：0-1；
含义：删除节点触发软关机，1启用，0禁用，
ports > graceful_disable：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机，1启用，0禁用，
ports > graceful_persist：
类型：整数；  
范围：0-1；
含义：禁用节点触发软关机后会话保持表有效，1启用，0禁用
ports >conn_limit：
类型：整数；  
范围：0-8000000；
含义：端口连接限制，
ports >phm_profile：
类型：字符串；  
范围：0-191；
含义：被动健康检查名称，
ports >healthcheck：
类型：字符串；  
范围：0-191；
含义：动健康检查名称，
ports >upnum：
类型：整数；  
范围：0-15；
含义：可用性要求  0 代表所有，
ports >nat_strategy：
类型：字符串；  
范围：0-191；
含义：nat策略名，

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.port.edit
请求body
{
    "name" : "192.168.1.123",
    "port" : {
        "port_number" : 890,
        "protocol" : 0,
        "status" : 1,
        "weight" : 1,
        "conn_limit" : 8000000,
        "graceful_time" : 0,
        "graceful_delete" : 0,
        "graceful_disable" : 0,
        "graceful_persist" : 0,
        "phm_profile" : "",
        "healthcheck" :  "",
        "nat_strategy" : ""
    }
}
节点端口(node.port)编辑针对operator用户
Action:  slb.node.port.onoff
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	节点名称	是	节点必须存在
host	字符串	长度1-191	节点主机名或IP地址	是	
status	整数	0,1	节点端口使能状态，	否	1:启用，0禁用，缺省值1
protocol	整数	0,1	节点端口协议	是	1：udp,0：tcp

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.port.onoff
请求body
{
    "name" : "192.168.1.123",
    "port" : {
        "port_number" : 80,
        "protocol" : 0,
        "status" : 1
        
    }
}

节点端口(node.port)删除
Action:  slb.node.port.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	节点名称	是	节点必须存在
port	对象	不涉及	节点对象	是	节点端口列表
由节点端口信息组成的数组，支持参数如下：
ports > port_number：
类型：整数；  
范围：0-65534；
含义：端口号，
ports > protocol：
类型：整数；  
范围：0,1；
含义：协议类型，

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.port.del
请求body
{
	"name": "192.168.1.123",
"port": {
		"port_number": 80,
		"protocol": 0
	}
}



节点(node)状态列表
Action:  slb.node.stat.list
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.stat.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	节点名称
host	字符串	长度1-191	节点主机名或IP地址
status	整数	0-4	节点状态：0禁用，1正常，2 故障
desc_rserver	字符串	长度1-191	节点描述
current_conns	整数	>=0	节点当前并发连接数
total_conns	整数	>=0	节点累计连接连接数
send_packets	整数	>=0	节点发送包数
receive_packets	整数	>=0	节点接收包数
send_bytes	整数	>=0	节点发送字节数
receive_bytes	整数	>=0	节点接收字节数
send_rate	整数	>=0	节点发送速率（bps）
receive_rate	整数	>=0	节点接收速率（bps）
conn_rate	整数	>=0	节点新建连接速率（conn/s）
current_request	整数	>=0	节点当前请求
total_request	整数	>=0	节点累计请求
total_request_succ	整数	>=0	节点累计成功请求
node_ports_stat	数组	不涉及	节点端口列表
由节点端口信息组成的数组，支持参数如下：
node_ports_stat > port_number：
类型：整数；  
范围：0-65534；
含义：端口号，
node_ports_stat > protocol：
类型：整数；  
范围：0,1；
含义：协议类型，
node_ports_stat > status：
类型：整数；  
范围：0,1；
含义：节点端口状态：0禁用，1正常，2故障，3软关机，4暖启动，5软关机(服务器)，6维护，7软关机(故障)，8未知，9软关机(服务器)(故障)
node_ports_stat > current_conns：
类型：整数；  
范围：>=0；
含义：节点端口当前并发连接数，
node_ports_stat > total_conns：
类型：整数；  
范围：>=0；
含义：节点端口累计连接连接数，
node_ports_stat > send_packets：
类型：整数；  
范围：>=0；
含义：节点端口发送包数，
node_ports_stat > receive_packets：
类型：整数；  
范围：>=0；
含义：节点端口接收包数，
node_ports_stat > send_bytes：
类型：整数；  
范围：>=0；
含义：节点端口发送字节数，
node_ports_stat > receive_bytes：
类型：整数；  
范围：>=0；
含义：节点端口接收字节数，
node_ports_stat > send_rate：
类型：整数；  
范围：>=0；
含义：节点端口发送速率（bps），
node_ports_stat > receive_rate：
类型：整数；  
范围：>=0；
含义：节点端口接收速率（bps），
node_ports_stat > conn_rate：
类型：整数；  
范围：>=0；
含义：节点端口新建连接速率（conn/s），
node_ports_stat > current_request：
类型：整数；  
范围：>=0；
含义：节点端口当前请求，
node_ports_stat > total_request：
类型：整数；  
范围：>=0；
含义：节节点端口累计请求，
node_ports_stat >total_request_succ：
类型：整数；  
范围：>=0；
含义：节点端口累计成功请求，
响应举例：
[{ 
"name": "192.168.1.100",
 "host": "192.168.1.100", 
"status": 1, 
"desc_rserver": "", 
"current_conns": 0, 
"total_conns": 0, 
"send_packets": 0, 
"receive_packets": 0, 
"send_bytes": 0, 
"receive_bytes": 0, 
"send_rate": 0, 
"receive_rate": 0, 
"conn_rate": 0, 
"current_request": 0,
 "total_request": 0, 
"total_request_succ": 0, 
"node_ports_stat": [{ 
"port_number": 80, 
"protocol": 0, 
"status": 1, 
"current_conns": 0, 
"total_conns": 0, 
"send_rate": 0, 
"receive_rate": 0, 
"send_packets": 0,
 "receive_packets": 0, 
"send_bytes": 0, 
"receive_bytes": 0, 
"current_request": 0, 
"total_request": 0,
"total_request_succ": 0 
}] 
}, 
{ 
"name": "192.168.1.101",
 "host": "192.168.1.101", 
"status": 1, 
"desc_rserver": "", 
"current_conns": 0,
 "total_conns": 0, 
"send_packets": 0, 
"receive_packets": 0, 
"send_bytes": 0, 
"receive_bytes": 0, 
"send_rate": 0, 
"receive_rate": 0, 
"conn_rate": 0, 
"current_request": 0, 
"total_request": 0, 
"total_request_succ": 0, 
"node_ports_stat": [{ 
"port_number": 80,
 "protocol": 0, 
"status": 1, 
"current_conns": 0, 
"total_conns": 0, 
"send_rate": 0, 
"receive_rate": 0,
 "send_packets": 0, 
"receive_packets": 0, 
"send_bytes": 0, 
"receive_bytes": 0, 
"current_request": 0, 
"total_request": 0, 
"total_request_succ": 0 
}] 
}
]


节点(node)状态获取
Action:  slb.node.stat.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	节点名称	是	节点必须存在


请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.node.stat.get
请求body:
{
    "name": "192.168.1.100"
}
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	节点名称
host	字符串	长度1-191	节点主机名或IP地址
status	整数	0-4	节点状态：0禁用，1正常，2 故障
desc_rserver	字符串	长度1-191	节点描述
current_conns	整数	>=0	节点当前并发连接数
total_conns	整数	>=0	节点累计连接连接数
send_packets	整数	>=0	节点发送包数
receive_packets	整数	>=0	节点接收包数
send_bytes	整数	>=0	节点发送字节数
receive_bytes	整数	>=0	节点接收字节数
send_rate	整数	>=0	节点发送速率（bps）
receive_rate	整数	>=0	节点接收速率（bps）
conn_rate	整数	>=0	节点新建连接速率（conn/s）
current_request	整数	>=0	节点当前请求
total_request	整数	>=0	节点累计请求
total_request_succ	整数	>=0	节点累计成功请求
node_ports_stat	数组	不涉及	节点端口列表
由节点端口信息组成的数组，支持参数如下：
node_ports_stat > port_number：
类型：整数；  
范围：0-65534；
含义：端口号，
node_ports_stat > protocol：
类型：整数；  
范围：0,1；
含义：协议类型，
node_ports_stat > status：
类型：整数；  
范围：0,1；
含义：节点端口状态：0禁用，1正常，2故障，3软关机，4暖启动，5软关机(服务器)，6维护，7软关机(故障)，8未知，9软关机(服务器)(故障)
node_ports_stat > current_conns：
类型：整数；  
范围：>=0；
含义：节点端口当前并发连接数，
node_ports_stat > total_conns：
类型：整数；  
范围：>=0；
含义：节点端口累计连接连接数，
node_ports_stat > send_packets：
类型：整数；  
范围：>=0；
含义：节点端口发送包数，
node_ports_stat > receive_packets：
类型：整数；  
范围：>=0；
含义：节点端口接收包数，
node_ports_stat > send_bytes：
类型：整数；  
范围：>=0；
含义：节点端口发送字节数，
node_ports_stat > receive_bytes：
类型：整数；  
范围：>=0；
含义：节点端口接收字节数，
node_ports_stat > send_rate：
类型：整数；  
范围：>=0；
含义：节点端口发送速率（bps），
node_ports_stat > receive_rate：
类型：整数；  
范围：>=0；
含义：节点端口接收速率（bps），
node_ports_stat > conn_rate：
类型：整数；  
范围：>=0；
含义：节点端口新建连接速率（conn/s），
node_ports_stat > current_request：
类型：整数；  
范围：>=0；
含义：节点端口当前请求，
node_ports_stat > total_request：
类型：整数；  
范围：>=0；
含义：节节点端口累计请求，
node_ports_stat >total_request_succ：
类型：整数；  
范围：>=0；
含义：节点端口累计成功请求，


响应举例：
{
 "name": "192.168.1.100",
 "host": "192.168.1.100", 
"status": 1, 
"desc_rserver": "", 
"current_conns": 0,
 "total_conns": 0,
 "send_packets": 0,
 "receive_packets": 0, 
"send_bytes": 0, 
"receive_bytes": 0,
 "send_rate": 0, 
"receive_rate": 0,
 "conn_rate": 0,
 "current_request": 0,
 "total_request": 0, 
"total_request_succ": 0,
 "node_ports_stat": [{
 "port_number": 80,
 "protocol": 0, 
"status": 1, 
"current_conns": 0,
 "total_conns": 0, 
"send_rate": 0,
 "receive_rate": 0,
 "send_packets": 0, 
"receive_packets": 0, 
"send_bytes": 0,
 "receive_bytes": 0, 
"current_request": 0, 
"total_request": 0,
 "total_request_succ": 0
 }]
 }
节点状态清除
Action:  slb.node.stat.clear
请求参数:无
请求举例:
GET http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.node.stat.clear

	此API会清除所有节点的统计信息

服务池
服务池(pool)列表
Action:  slb.pool.list
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
protocol	整数	0,1	服务池的协议，0 tcp，1 udp
lb_method	整数	0-18，20，22-25	服务池关联算法：
0：轮询；
1：加权轮询；
2：节点最少连接；
3：加权节点最少连接；
4：服务最少连接 
5：加权服务最少连接；
6：最快响应 
7：最少请求；
8：精确轮询；
9：无状态源IP端口哈希；
10：无状态源IP哈希；
11：无状态目的IP端口哈希；
12：无状态源IP和目的IP端口哈希；
13：无状态每包轮询；
14：最小带宽；
15：源地址哈希； 
16：源地址和端口哈希；
17：目的地址哈希；
18：目的地址和端口哈希；
20：随机；
22：基于IPList；
23：无状态加权每包轮询；
24：严格加权轮询；
25：服务加权轮询
healthcheck	字符串	长度1-63	服务池关联的健康检查名称
up-num	整数	1-15	可用性要求，健康检查的最少正常个数
desc_pool	字符串	长度1-191	服务池描述
action_on_service_down	整数	0,1	服务池故障重置1开始，0关闭
slow_ramp_time	整数	0-65535	服务池暖启动的维持时间，单位为秒
up_members_at_least	对象	不涉及	最少正常成员数及成员优先级规则，详细参数如下:
up_members_at_least > status:
类型：整数串；  
范围：0-1；
含义：优先级规则状态，
up_members_at_least > num:
类型：整数串；  
范围：0-1；
含义：最少正常成员数，
up_members_at_least > type:
类型：整数串；  
范围：0-2；
含义：优先级规则，整数，0禁用，1仅使用低优先级成员，2动态使用低优先级成员，
aux_node_log	整数	0,1	1开启优先级日志，0关闭
node-select-fail-send-rst	整数	0,1	算法失败重置开关，0关闭，1开启
members	数组	不涉及	服务池成员对象组成的数组，详细参数如下：
members > nodename:
类型：字符串；  
范围：1-191；
含义：服务池成员使用的节点名称，
members > server:
类型：字符串；  
范围：1-63；
含义：服务池成员使用的节点主机名或者IP地址，
members > port:
类型：整数；  
范围：0-65534；
含义：服务池成员使用的节点端口，
members > priority:
类型：整数；  
范围：1-16；
含义：服务池成员的优先级，
members > availability:
类型：数组；  
范围：1-16；
含义：可用性，
members > status:
类型：整数；  
范围：0-1；
含义：服务池成员是否启用，
members > hc_reason:
类型：对象；  
范围：不涉及；
含义：健康检查结果集合，
members > reason:
类型：数组；  
范围：不涉及；
含义：健康检查结果，
members > withhc:
类型：整数；  
范围：0-1；
含义：健康检查状态，
members > state:
类型：字符串；  
范围：up或down；
含义：健康检查状态，
members > hcname:
类型：字符串；  
范围：1-191；
含义：健康检查名字，
members > reason:
类型：字符串；  
范围： 1-191；
含义：健康检查失败原因，
members > cookie:
类型：字符串；  
范围： 1-191；
含义：携带cookie参数，


响应举例：
[
  {
    "name": "pool",
    "protocol": 0,
    "lb_method": 0,
    "healthcheck": "ping",
    "desc_pool": "iampool",
    "action_on_service_down": 1,
    "up-members-at-least": {
        "status": 1,
        "num": 32,
        "type": 2
    },
    "aux-node-log": 1,
    "node-select-fail-send-rst": 0,
    "members": [
        {
        "nodename": "192.168.1.100",
        "server": "192.168.1.100",
        "port": 80,
        "priority": 5,
        "status": 1
      }
    ]
  }
]
分区中获取common分区和自己分区的服务池列表
Action:  slb.pool.list.withcommon
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.list.withcommon
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
protocol	整数	0,1	服务池关联协议，0 tcp，1 udp
lb_method	整数	0-18，20，22-25	服务池关联算法：
0：轮询；
1：加权轮询；
2：节点最少连接；
3：加权节点最少连接；
4：服务最少连接 
5：加权服务最少连接；
6：最快响应 
7：最少请求；
8：精确轮询；
9：无状态源IP端口哈希；
10：无状态源IP哈希；
11：无状态目的IP端口哈希；
12：无状态源IP和目的IP端口哈希；
13：无状态每包轮询；
14：最小带宽；
15：源地址哈希； 
16：源地址和端口哈希；
17：目的地址哈希；
18：目的地址和端口哈希；
20：随机；
22：基于IPList；
23：无状态加权每包轮询；
24：严格加权轮询；
25：服务加权轮询
healthcheck	字符串	长度1-63	服务池关联的健康检查名称
desc_pool	字符串	长度1-191	描述
action_on_service_down	整数	0,1	服务池故障重置；1开始，0关闭
up-members-at-least	对象		最少正常成员数及成员优先级规则，详细参数如下:
up_members_at_least > status:
类型：整数串；  
范围：0-1；
含义：优先级规则状态，
up_members_at_least > num:
类型：整数串；  
范围：0-1；
含义：最少正常成员数，
up_members_at_least > type:
类型：整数串；  
范围：0-2；
含义：优先级规则，整数，0禁用，1仅使用低优先级成员，2动态使用低优先级成员，
status	整数	0,1	num大于0时为1，num等于0时为0
num	整数	0-63	最少正常成员
type	整数	0-2	0禁用，1仅使用低优先级成员，2动态使用低优先级成员
aux-node-log	整数	0,1	1开启优先级日志，0关闭
members	数组		服务池成员对象组成的数组，详细参数如下：
members > nodename:
类型：字符串；  
范围：1-191；
含义：服务池成员使用的节点名称，
members > server:
类型：字符串；  
范围：1-63；
含义：服务池成员使用的节点主机名或者IP地址，
members > port:
类型：整数；  
范围：0-65534；
含义：服务池成员使用的节点端口，
members > priority:
类型：整数；  
范围：1-16；
含义：服务池成员的优先级，
members > availability:
类型：数组；  
范围：1-16；
含义：可用性，
members > status:
类型：整数；  
范围：0-1；
含义：服务池成员是否启用，
members > hc_reason:
类型：对象；  
范围：不涉及；
含义：健康检查结果集合，
members > reason:
类型：数组；  
范围：不涉及；
含义：健康检查结果，
members > withhc:
类型：整数；  
范围：0-1；
含义：健康检查状态，
members > state:
类型：字符串；  
范围：up或down；
含义：健康检查状态，
members > hcname:
类型：字符串；  
范围：1-191；
含义：健康检查名字，
members > reason:
类型：字符串；  
范围： 1-191；
含义：健康检查失败原因，
members > cookie:
类型：字符串；  
范围： 1-191；
含义：携带cookie参数，
members > cookie:
类型：整数；  
范围： 1-16；
含义：成员优先级，


响应举例：
[
{
    "name": "pool",
    "protocol": 0,
    "lb_method": 0,
    "healthcheck": "ping",
    "desc_pool": "iampool",
    "action_on_service_down": 1,
    "up-members-at-least": {  
        "status": 1,
        "num": 32,
        "type": 2
    },
    "aux-node-log": 1,
    "members": [
        {
            "nodename": "192.168.1.100",
            "server": "192.168.1.100",
            "port": 80,
            "priority": 5,
            "status": 1
        }
    ]
}
]

服务池(pool)获取
Action:  slb.pool.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	服务池名称	是	服务池必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.get
请求body
{
    "name": "pool"
}
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
protocol	整数	0,1	服务池的协议，0 tcp，1 udp
lb_method	整数	0-18，20，22-25	服务池关联算法：
0：轮询；
1：加权轮询；
2：节点最少连接；
3：加权节点最少连接；
4：服务最少连接 
5：加权服务最少连接；
6：最快响应 
7：最少请求；
8：精确轮询；
9：无状态源IP端口哈希；
10：无状态源IP哈希；
11：无状态目的IP端口哈希；
12：无状态源IP和目的IP端口哈希；
13：无状态每包轮询；
14：最小带宽；
15：源地址哈希； 
16：源地址和端口哈希；
17：目的地址哈希；
18：目的地址和端口哈希；
20：随机；
22：基于IPList；
23：无状态加权每包轮询；
24：严格加权轮询；
25：服务加权轮询
healthcheck	字符串	长度1-63	服务池关联的健康检查名称
upnum	整数	1-15	可用性要求,健康检查至少正常数量
desc_pool	字符串	长度1-191	服务池描述
action_on_service_down	整数	0,1	服务池故障重置1开始，0关闭
up_members_at_least	对象	不涉及	最少正常成员数及成员优先级规则，详细参数如下:
up_members_at_least > status:
类型：整数串；  
范围：0-1；
含义：优先级规则状态，
up_members_at_least > num:
类型：整数串；  
范围：0-1；
含义：最少正常成员数，
up_members_at_least > type:
类型：整数串；  
范围：0-2；
含义：优先级规则，整数，0禁用，1仅使用低优先级成员，2动态使用低优先级成员，
aux_node_log	整数	0,1	1开启优先级日志，0关闭
members	数组	不涉及	服务池成员对象组成的数组，详细参数如下：
members > nodename:
类型：字符串；  
范围：1-191；
含义：服务池成员使用的节点名称，
members > server:
类型：字符串；  
范围：1-63；
含义：服务池成员使用的节点主机名或者IP地址，
members > port:
类型：整数；  
范围：0-65534；
含义：服务池成员使用的节点端口，
members > priority:
类型：整数；  
范围：1-16；
含义：服务池成员的优先级，
members > availability:
类型：数组；  
范围：1-16；
含义：可用性，
members > status:
类型：整数；  
范围：0-1；
含义：服务池成员是否启用，
members > hc_reason:
类型：对象；  
范围：不涉及；
含义：健康检查结果集合，
members > reason:
类型：数组；  
范围：不涉及；
含义：健康检查结果，
members > withhc:
类型：整数；  
范围：0-1；
含义：健康检查状态，
members > state:
类型：字符串；  
范围：up或down；
含义：健康检查状态，
members > hcname:
类型：字符串；  
范围：1-191；
含义：健康检查名字，
members > reason:
类型：字符串；  
范围： 1-191；
含义：健康检查失败原因，
members > cookie:
类型：字符串；  
范围： 1-191；
含义：携带cookie参数，



响应举例：
{
  "name": "pool",
  "protocol": 0,
  "lb_method": 0,
  "healthcheck": "tcp ping dns",
  "upnum": 2,
  "desc_pool": "",
  "action_on_service_down": 1,
  "slow_ramp_time": 20,
  "up-members-at-least": {
    "status": 1,
    "num": 2,
    "type": 1
  },
  "aux-node-log": 1,
  "members": [
    {
      "nodename": "102.0.1.4",
      "server": "102.0.1.4",
      "port": 80,
      "priority": 1,
      "status": 1,
      "cookie": "",
      "availability": {
        "status": "Up",
        "hc_reason": {
          "reasons": [
            {
              "withhc": 1,
              "state": "up",
              "hcname": "tcp"
            },
            {
              "withhc": 1,
              "state": "up",
              "hcname": "ping"
            },
            {
              "withhc": 1,
              "state": "down",
              "hcname": "dns",
              "reason": "UDP service error"
            }
          ]
        }
      }
    }
  ]
}
分区中获取common分区和自己分区的服务池列表
Action:  slb.pool.list.withcommon
请求参数:无
请求举例：
GET 
http://{{host}}/adcapi/v2.0/?authkey={{authkey}}&action=slb.pool.list.withcommon
响应参数：

响应举例：
{
        "name": "common/pool3",
        "protocol": 0,
        "lb_method": 7,
        "healthcheck": "common/ping",
        "upnum": 0,
        "desc_pool": "iampool",
        "action_on_service_down": 0,
        "up-members-at-least": {
            "status": 1,
            "num": 32,
            "type": 2
        },
        "aux-node-log": 1,
        "members": []
    },
    {
        "name": "no-net",
        "protocol": 0,
        "lb_method": 0,
        "healthcheck": "",
        "upnum": 0,
        "desc_pool": "",
        "action_on_service_down": 0,
        "up-members-at-least": {
            "status": 0,
            "type": 0
        },
        "aux-node-log": 0,
        "members": [
            {
                "nodename": "117.255.255.23",
                "server": "117.255.255.23",
                "port": 80,
                "priority": 1,
                "status": 1,
                "cookie": ""
            }
        ]
    }
]
服务池(pool)添加
Action:  slb.pool.add
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	服务池名称	是	唯一
protocol	整数	0,1	服务池协议，	是	0 tcp，1 udp，缺省值：0
lb_method	整数	0-18，20，22-25	服务池算法：
	否	服务池关联算法：
0：轮询；
1：加权轮询；
2：节点最少连接；
3：加权节点最少连接；
4：服务最少连接 
5：加权服务最少连接；
6：最快响应 
7：最少请求；
8：精确轮询；
9：无状态源IP端口哈希；
10：无状态源IP哈希；
11：无状态目的IP端口哈希；
12：无状态源IP和目的IP端口哈希；
13：无状态每包轮询；
14：最小带宽；
15：源地址哈希； 
16：源地址和端口哈希；
17：目的地址哈希；
18：目的地址和端口哈希；
20：随机；
22：基于IPList；
23：无状态加权每包轮询；
24：严格加权轮询；
25：服务加权轮询
upnum	整数	0-15	可用性要求	否	缺省值  所有 0代表所有
healthcheck	字符串	长度1-63	健康检查名称	否	缺省值为空字符串"",表示没有检查
desc_pool	字符串	长度1-191	描述	否	缺省值为空字符串""
action_on_service_down	整数	0,1	服务池故障重置	否	0表示关闭，1表示开启；缺省值：0
up-members-at-least	对象	不涉及	优先级规则配置	否	最少正常成员数及成员优先级规则，详细参数如下:
up_members_at_least > status:
类型：整数串；  
范围：0-1；
含义：优先级规则状态，
up_members_at_least > num:
类型：整数串；  
范围：0-1；
含义：最少正常成员数，
up_members_at_least > type:
类型：整数串；  
范围：0-2；
含义：优先级规则，整数，0禁用，1仅使用低优先级成员，2动态使用低优先级成员，
aux-node-log	整数	0,1	1开启优先级日志，0关闭	否	缺省值：0

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.add
请求body
{
    "pool":{
        "name": "test_api_srvpool",
        "protocol": 0,
        "lb_method": 0,
        "healthcheck": "",
        "upnum": 0,
        "desc_pool": "",
        "action_on_service_down": 0,
        "up-members-at-least": {
            "status": 0,
            "type": 0
        },
        "aux-node-log": 0
    }
}
服务池(pool)编辑
Action:  slb.pool.edit
请求参数:
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
protocol	整数	0,1	服务池的协议，0 tcp，1 udp
lb_method	整数	0-18，20，22-25	服务池关联算法：
0：轮询；
1：加权轮询；
2：节点最少连接；
3：加权节点最少连接；
4：服务最少连接 
5：加权服务最少连接；
6：最快响应 
7：最少请求；
8：精确轮询；
9：无状态源IP端口哈希；
10：无状态源IP哈希；
11：无状态目的IP端口哈希；
12：无状态源IP和目的IP端口哈希；
13：无状态每包轮询；
14：最小带宽；
15：源地址哈希； 
16：源地址和端口哈希；
17：目的地址哈希；
18：目的地址和端口哈希；
20：随机；
22：基于IPList；
23：无状态加权每包轮询；
24：严格加权轮询；
25：服务加权轮询
healthcheck	字符串	长度1-63	服务池关联的健康检查名称
desc_pool	字符串	长度1-191	服务池描述
action_on_service_down	整数	0,1	服务池故障重置1开始，0关闭
up_members_at_least	对象	不涉及	最少正常成员数及成员优先级规则，详细参数如下:
up_members_at_least > status:
类型：整数串；  
范围：0-1；
含义：优先级规则状态，
up_members_at_least > num:
类型：整数串；  
范围：0-1；
含义：最少正常成员数，
up_members_at_least > type:
类型：整数串；  
范围：0-2；
含义：优先级规则，整数，0禁用，1仅使用低优先级成员，2动态使用低优先级成员，
aux_node_log	整数	0,1	1开启优先级日志，0关闭
members	数组	不涉及	服务池成员对象组成的数组，详细参数如下：
members > nodename:
类型：字符串；  
范围：1-191；
含义：服务池成员使用的节点名称，
members > server:
类型：字符串；  
范围：1-63；
含义：服务池成员使用的节点主机名或者IP地址，
members > port:
类型：整数；  
范围：0-65534；
含义：服务池成员使用的节点端口，
members > priority:
类型：整数；  
范围：1-16；
含义：服务池成员的优先级，
members > availability:
类型：数组；  
范围：1-16；
含义：可用性，
members > status:
类型：整数；  
范围：0-1；
含义：服务池成员是否启用，
members > hc_reason:
类型：对象；  
范围：不涉及；
含义：健康检查结果集合，
members > reason:
类型：数组；  
范围：不涉及；
含义：健康检查结果，
members > withhc:
类型：整数；  
范围：0-1；
含义：健康检查状态，
members > state:
类型：字符串；  
范围：up或down；
含义：健康检查状态，
members > hcname:
类型：字符串；  
范围：1-191；
含义：健康检查名字，
members > reason:
类型：字符串；  
范围： 1-191；
含义：健康检查失败原因，
members > cookie:
类型：字符串；  
范围： 1-191；
含义：携带cookie参数，
members > cookie:
类型：整数；  
范围： 1-16；
含义：成员优先级，
upnum	整数	1-15	可用性要求,健康检查至少正常数量

请求举例：
POST 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.edit
请求body
{
    "pool":{
      "name": "test_api_srvpool",
      "protocol": 0,
      "lb_method": 24,
      "healthcheck": "ping",
      "desc_pool": "",
      "up-members-at-least": {
        "status": 1,
        "num": 63,
        "type": 2
      },
      "aux-node-log": 1,
      "members": [
        {
            "nodename": "36.3.30.2",
            "server": "36.3.30.2",
            "port": 80,
       "priority": 1,
            "status": 1,
            "cookie": ""
        },
        {
            "nodename": "120.21.1.31",
            "server": "120.21.1.31",
            "port": 80,
            "priority": 1,
            "status": 1,
            "cookie": ""
        }
    ]
    }
}


服务池(pool)删除
Action:  slb.pool.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	服务池名称	是	服务池必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.del
请求body
{
    "name": "test_api_srvpool"
}


服务池成员(pool.member)添加
Action:  slb.pool.member.add
请求参数:
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
members	数组	不涉及	服务池成员对象组成的数组，详细参数如下：
members > nodename:
类型：字符串；  
范围：1-191；
含义：服务池成员使用的节点名称，
members > server:
类型：字符串；  
范围：1-63；
含义：服务池成员使用的节点主机名或者IP地址，
members > port:
类型：整数；  
范围：0-65534；
含义：服务池成员使用的节点端口，
members > priority:
类型：整数；  
范围：1-16；
含义：服务池成员的优先级，
members > state:
类型：字符串；  
范围：up或down；
含义：健康检查状态，

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.member.add
请求body
{
"name": "test_api_srvpool",
"member": 
        {
          "server": "16.1.3.18",
"port": 81,
          "priority": 15,
          "status": 1
        }
}

服务池成员(pool.member)编辑
Action:  slb.pool.member.edit
请求参数:
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
members	数组	不涉及	服务池成员对象组成的数组，详细参数如下：
members > server:
类型：字符串；  
范围：1-63；
含义：服务池成员使用的节点主机名或者IP地址，
members > port:
类型：整数；  
范围：0-65534；
含义：服务池成员使用的节点端口，
members > priority:
类型：整数；  
范围：1-16；
含义：服务池成员的优先级，
members > state:
类型：字符串；  
范围：up或down；
含义：健康检查状态，

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.member.edit
请求body
{
"name": "test_api_srvpool",
"member": 
        {
          "server": "16.1.3.18",
"port": 81,
          "priority": 10,
          "status": 1
        }
}
服务池成员(pool.member)编辑针对operator角色
Action:  slb.pool.member.onoff
请求参数:
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
status	整数	0,1	节点端口使能状态

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.member.onoff
请求body
{
"name": "test_api_srvpool",
"member": 
        {
          "server": "16.1.3.18",
"port": 81,
          "priority": 10,
          "status": 1
        }
}
服务池成员(pool.member)删除
Action:  slb.pool.member.del
请求参数:
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
members	数组	不涉及	服务池成员对象组成的数组，详细参数如下：
members > nodename:
类型：字符串；  
范围：1-191；
含义：服务池成员使用的节点名称，
members > server:
类型：字符串；  
范围：1-63；
含义：服务池成员使用的节点主机名或者IP地址，
members > port:
类型：整数；  
范围：0-65534；
含义：服务池成员使用的节点端口，

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.member.del
请求body
{
    "name": "test_api_srvpool",
    "member": 
    {
        "server": "16.1.3.18",
        "port": 81
    }
}

服务池(pool)状态列表
Action:  slb.pool.stat.list
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.stat.list
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
protocol	整数	0,1	服务池关联协议，0 tcp，1 udp
status	整数	0-4	服务池的状态：0禁用，1正常，2部分正常，3故障，4 unknown
desc_pool	字符串	长度1-191	描述
current_conns	整数	>=0	服务池当前并发连接数
total_conns	整数	>=0	服务池累计连接连接数
send_packets	整数	>=0	服务池发送包数
receive_packets	整数	>=0	服务池接收包数
send_bytes	整数	>=0	服务池发送字节数
receive_bytes	整数	>=0	服务池接收字节数
request_current	整数	>=0	服务池当前请求
request_total	整数	>=0	服务池累计请求
request_success	整数	>=0	服务池累计成功请求
members_stat	数组	不涉及	由服务池成员状态统计信息对象组成的数组，详细参数如下：
members_stat > server:	
类型：字符串	
范围：长度1-63	
含义：服务池成员使用的节点主机名或IP地址
members_stat > mem_nodename：	
类型：字符串	
范围：长度1-191	
含义：服务池成员使用的节点名称
members_stat > port：	
类型：整数	
范围：0-65534	
含义：服务池成员使用的节点端口
members_stat > status：
	类型：整数	
范围：0-2	
含义：服务池成员状态：0禁用，1正常，2故障
members_stat > response_time_hc：	
类型：整数	
范围 ：>=0	
含义：服务池成员健康检查响应时间
members_stat > response_time_http：	
类型：整数	
范围：>=0	
含义：服务池成员http协议响应时间
members_stat > current_conns：	
类型：整数	
范围：>=0	
含义：服务池成员当前并发连接数
members_stat > total_conns：
	类型：整数	
范围：>=0	
含义：服务池成员累计连接连接数
members_stat > send_packets	：
类型：整数	
范围：>=0	
含义：服务池成员发送包数
members_stat > receive_packets：	
类型：整数	
范围：>=0	
含义：服务池成员接收包数
members_stat > send_bytes：	
类型：整数	
范围：>=0	
含义：服务池成员发送字节数
members_stat > receive_bytes：	
类型：整数	
范围：>=0	
含义：服务池成员接收字节数
members_stat > request_current：	
类型：整数	
范围：>=0	
含义：服务池成员当前请求
members_stat > request_total：	
类型：整数	
范围：>=0	
含义：服务池成员累计请求
members_stat > request_success：	
类型：整数	
范围：>=0	
含义：服务池成员累计成功请求

响应参数:
响应举例：
[
  {
    "name": "pool",
    "protocol": 0,
    "status": 1,               
    "desc_pool": "iampool",
    "current_conns": 0,
    "total_conns": 0,
    "send_packets": 0,
    "receive_packets": 0,
    "send_bytes": 0,
    "receive_bytes": 0,
    "request_current": 0,
    "request_total": 0,
    "request_success": 0,
    "members_stat": [
      {
        "server": "192.168.1.100",
        "port": 80,
        "status": 1,                
        "current_conns": 0,
        "total_conns": 0,
        "mem_nodename": "192.168.1.100",
        "send_packets": 0,
        "receive_packets": 0,
        "response_time_hc": 112000,
        "response_time_http": 0,
        "send_bytes": 0,
        "receive_bytes": 0,
        "request_current": 0,
        "request_total": 0,
        "request_success": 0
      }
    ]
  }
]

服务池(pool)状态获取
Action:  slb.pool.stat.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	服务池名称	是	服务池必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.stat.get
请求body
{
    "name": "pool"
}

响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
protocol	整数	0,1	服务池关联协议，0 tcp，1 udp
status	整数	0-4	服务池的状态：0禁用，1全部正常，2部分正常，3故障，4 未知
desc_pool	字符串	长度1-191	描述
current_conns	整数	>=0	服务池当前并发连接数
total_conns	整数	>=0	服务池累计连接连接数
send_packets	整数	>=0	服务池发送包数
receive_packets	整数	>=0	服务池接收包数
send_bytes	整数	>=0	服务池发送字节数
receive_bytes	整数	>=0	服务池接收字节数
request_current	整数	>=0	服务池当前请求
request_total	整数	>=0	服务池累计请求
request_success	整数	>=0	服务池累计成功请求
members_stat	数组	不涉及	由服务池成员状态统计信息对象组成的数组，详细参数如下：
members_stat > server:	
类型：字符串	
范围：长度1-63	
含义：服务池成员使用的节点主机名或IP地址
members_stat > mem_nodename：	
类型：字符串	
范围：长度1-191	
含义：服务池成员使用的节点名称
members_stat > port：	
类型：整数	
范围：0-65534	
含义：服务池成员使用的节点端口
members_stat > status：
	类型：整数	
范围：0-2	
含义：服务池成员状态：0禁用，1正常，2故障，3维护
members_stat > response_time_hc：	
类型：整数	
范围 ：>=0	
含义：服务池成员健康检查响应时间
members_stat > response_time_http：	
类型：整数	
范围：>=0	
含义：服务池成员http协议响应时间
members_stat > current_conns：	
类型：整数	
范围：>=0	
含义：服务池成员当前并发连接数
members_stat > total_conns：
	类型：整数	
范围：>=0	
含义：服务池成员累计连接连接数
members_stat > send_packets	：
类型：整数	
范围：>=0	
含义：服务池成员发送包数
members_stat > receive_packets：	
类型：整数	
范围：>=0	
含义：服务池成员接收包数
members_stat > send_bytes：	
类型：整数	
范围：>=0	
含义：服务池成员发送字节数
members_stat > receive_bytes：	
类型：整数	
范围：>=0	
含义：服务池成员接收字节数
members_stat > request_current：	
类型：整数	
范围：>=0	
含义：服务池成员当前请求
members_stat > request_total：	
类型：整数	
范围：>=0	
含义：服务池成员累计请求
members_stat > request_success：	
类型：整数	
范围：>=0	
含义：服务池成员累计成功请求



响应举例：
{
    "name": "pool",
    "protocol": 0,
"status": 1,               
"desc_pool": "iampool",
    "current_conns": 0,
    "total_conns": 0,
    "send_packets": 0,
    "receive_packets": 0,
    "send_bytes": 0,
    "receive_bytes": 0,
    "request_current": 0,
    "request_total": 0,
    "request_success": 0,
    "members_stat": [
      {
        "server": "192.168.1.100",
        "port": 80,
        "status": 1,                 
        "current_conns": 0,
        "total_conns": 0,
        "mem_nodename": "192.168.1.100",
        "send_packets": 0,
        "receive_packets": 0,
        "response_time_hc": 112000,
        "response_time_http": 0,
        "send_bytes": 0,
        "receive_bytes": 0,
        "request_current": 0,
        "request_total": 0,
        "request_success": 0
      }
    ]
}

服务池成员(pool.member)禁用/启用
Action:  slb.pool.member.onoff
请求参数:
名称	类型	范围	含义
name	字符串	长度1-191	服务池名称
members	数组	不涉及	服务池成员对象组成的数组，详细参数如下：
members > nodename:
类型：字符串；  
范围：1-191；
含义：服务池成员使用的节点名称，
members > server:
类型：字符串；  
范围：1-63；
含义：服务池成员使用的节点主机名或者IP地址，
members > port:
类型：整数；  
范围：0-65534；
含义：服务池成员使用的节点端口，
members > priority:
类型：整数；  
范围：1-16；
含义：服务池成员的优先级，
members > status:
类型：整数；  
范围：0-1；
含义：服务池成员是否启用，

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.pool.member.onoff
请求body
{
      "name": "test",
      "member":
        {
          "server": "20.20.20.20",
          "port": 80,
          "status": 1
        }
}



服务池状态清除
Action:  slb.pool.stat.clear
请求参数:无
请求举例:
GET http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.pool.stat.clear

	此API会清除所有pool的统计信息
获取服务池名称列表
Action:  slb.pool.names.list
请求参数:无
请求举例:
GET http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.pool.names.list
响应参数:
名称	类型	范围	含义
items
	数组	不涉及	由以下数组组成的项目集合：
items > name：
类型：字符串
范围：1-191
含义：服务池名称
items > protocol：
类型：整数
范围：0，1
含义：服务池协议，0 tcp，1 udp，缺省值：0

 
响应举例：
{
    "items": [
        {
            "name": "test_1",
            "protocol": 0
        },
        {
            "name": "test_2",
            "protocol": 0
        },
        {
            "name": "test_3",
            "protocol": 0
        }
]
}
虚拟地址
虚拟地址列表
Action:  slb.va.list
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.list
响应参数:
名称	类型	范围	含义
tc_name	字符串	长度1-191	虚拟地址关联的流量控制
name	字符串	长度1-191	虚拟地址名称
address	字符串	长度1-63	ipv4/v6类型的虚拟地址才有此参数
subnet	对象	不涉及	子网类型的虚拟地址才有此参数
address	IP	不涉及	子网类型的虚拟地址的子网地址
mask_len	整数	16-32	子网类型的虚拟地址的子网掩码长度
acl_id	整数	1-199	ipv4 acl类型的虚拟地址才有此参数
acl_name	字符串	长度1-191	ipv6 acl类型的虚拟地址才有此参数
status	整数	0,1	虚拟地址状态:1:启用；0:禁用
arp_status	整数	0,1	arp状态1:启用；0:禁用
icmp_probe	整数	0-3	ping  vip地址0:always；1:disable；2:all；3:any
vrid	整数	0-8	vrrp组id，
redistribution	整数	0-3	类型：整数
范围：0-3
含义：路由联动
0:禁用；
1:启用；
2:all；
3:any
policy_profile	字符串	长度1-191	策略模版
virtual_services	数组	不涉及	该虚拟地址下的虚拟服务列表
虚拟地址成员对象组成的数组，详细参数如下：
virtual_services > name:
        类型：字符串
范围：1-63
含义：虚拟服务名称
virtual_services > protocol:
类型：整数
范围：不涉及
含义：虚拟服务类型含义
2：TCP
3：UDP
5：OTHER
8：RTSP
9：FTP
11：SIP
12：FAST_HTTP  (HTTP普通)
14：HTTP(HTTP增强)
15：HTTPS
16：SSL_AGENT
17：SMTP
18：SIP-TCP
20：TCP_AGENT
21：DIAMETER
22：DNS
23：TFTP
25：TCP-EXCHANGE
26：MBLB
28：RADIUS
virtual_services > port:
类型：整数
范围：0-65534
含义：虚拟服务端口
virtual_services > connection_limit:
类型：对象
范围：不涉及
含义：虚拟服务的并发连接限制对象
virtual_services > connection_limit > status:
类型：整数
范围：0-1
含义：虚拟服务的并发连接限制开关:1:启用；0:禁用
virtual_services>connection_limit>connection_limit_number:
类型：整数
范围：1-8000000
含义：虚拟服务的并发连接接限制数值，仅当开启虚拟服务的并发连接限制开关为1时有效
pool	字符串	长度1-63	虚拟服务的服务池
vs_enable_intf	字符串	长度1-63	使能接口号,eth开头，逗号分隔
path_persist	整数	0,1	路径保持:1:启用；0:禁用
status	整数	0,1	虚拟服务状态:1:启用；0:禁用
desc_vport	字符串	长度1-191	虚拟服务描述
snat_on_vip	整数	0,1	使能全局snat映射:1:启用；0:禁用
auto_snat	整数	0,1	接口snat:1:启用；0:禁用
snat_port_preserve_enable	整数	0,1	源端口保持:1:启用；0:禁用
snat_port_preserve_type	整数	0,1	源端口保持类型:1:强制；0:尝试，仅当snat_port_preserve_enable参数为1时有效
vs_acl_id	整数	0-199	访问列表,1-199表示对应acl，0表示没有配置
aclnamev6	字符串	长度1-191	ipv6访问列表名称
erules	数组	不涉及	关联的erule名称组成的列表
send_reset	整数	0,1	选择节点失败发送rst:1:启用；0:禁用
source_nat	字符串	长度1-63	源snat地址池
srcip_persist	字符串	长度1-191	源地址保持模版,一个虚拟服务只能有一种连接保持模板
dstip_persist	字符串	长度1-191	目的地址保持模版,一个虚拟服务只能有一种连接保持模板
cookie_persist	字符串	长度1-191	cookie保持模版,一个虚拟服务只能有一种连接保持模板
sslid_persis	字符串	长度1-191	ssl连接保持模版,一个虚拟服务只能有一种连接保持模板
policy_profile	字符串	长度1-191	策略模版
aclsnats	数组		策略地址转换
组成的数组，详细参数如下：
aclsnats > acl_id:
类型：整数
范围：1-199
含义：策略地址转换-acl id，
aclsnats > nat_pool:
类型：整数
范围：长度1-63
含义：策略地址转换-snat池，
connection_mirror	整数	0,1	连接镜像:1:启用；0:禁用
no_dest_nat	整数	0,1	直接转发:1:启用；0:禁用
syncookie	整数	0,1	syn cookie:1:启用；0:禁用
udp_profile	字符串	长度1-191	udp模版
dns_profile	字符串	长度1-191	dns模版
dns_log_profile	字符串	长度1-191	dns日志模版
tcp_profile	字符串	长度1-191	tcp模版
waf_profile	字符串	长度1-191	waf模版
http_profile	字符串	长度1-191	http模版
connmulti_profile	字符串	长度1-191	连接复用模版
cache_profile	字符串	长度1-191	缓存模版
tcp_agent	字符串	长度1-191	TCP代理模版
serverssl_profile	字符串	长度1-191	服务器ssl模版
connmulti_profile	字符串	长度1-191	连接复用模版
clientssl_profile	字符串	长度1-191	客户端ssl模版
rtsp_profile	字符串	长度1-191	rtsp模版
smtp_profile	字符串	长度1-191	smtp模版
sip_profile	字符串	长度1-191	sip模版
udp_profile	字符串	长度1-191	udp模版
l4_profile_type	整数	2,3	运输层协议，2 tcp，3 udp，
natlog_profile	字符串	长度1-191	nat日志模板

响应举例：
[
  {
    "tc_name": "",                  
    "name": "1.1.1.1_va",             
    "address": "1.1.1.1",               
    "status": 1,
"arp_status": 1,              
"icmp_disable": 0,              
    "vrid": 0,                   
    "redistribution": 0,          
    "policy_profile": "",        
    "virtual_services": [          
      {
        "name": "dnsvs",        
        "protocol": 22,           
        "port": 53,                                   
        "pool": "",              	       
 "connection_limit": {      
          "status": 0,             
          "connection_limit_number": 8000000    
        },
        "vs_enable_intf": "ETH0/1,ETH0/3",  
        "path_persist": 1,           
        "status": 1,
        "desc_vport": "",          
        "snat_on_vip": 0,                
        "auto_snat": 0,                 
        "snat_port_preserve_enable": 0,
"snat_port_preserve_type": 0,
        "vs_acl_id": 101,            
        "aclnamev6": "aclv6",        
        "erules": [                        
          "erule-empty.txt"        
        ],
        "send_reset": 0,         
        "source_nat": "",            
        "udp_profile": "",       
        "srcip_persist": "",  
        "dns_profile": "", 
"dns_log_profile": "",        
        "policy_profile": "",     
        "aclsnats": [           
           {
            "acl_id": 101,             
            "nat_pool": "snatpool"     
            }
        ]
      }
    ]
  },
  {
    "tc_name": "",
    "name": "2.2.2.2_va",
    "address": "2.2.2.2",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "ftpvs",
        "protocol": 9,
        "port": 21,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "connection_mirror": 0,
        "no_dest_nat": 0,      
        "syncookie": {
          "syncookie": 0        
        },
        "source_nat": "",
        "tcp_profile": "",             
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "3.3.3.3_24_va",
    "subnet": {
      "address": "3.3.3.3",
      "mask_len": 24
    },
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "httpvs",
        "protocol": 14,
        "port": 80,
        "pool": "pool",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "snat_port_preserve_enable": 0,
        "snat_port_preserve_type": 0,        
        "aclnamev6": "",
        "erules": [
          "erule-empty.txt"
        ],
        "send_reset": 0,
        "source_nat": "",
        "no_dest_nat": 0,
        "waf_profile": "",         
        "http_profile": "",         
        "tcp_profile": "",
        "connmulti_profile": "",     
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "ACL_ID_101_va",
    "acl_id": 101,
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "httpenvs",
        "protocol": 12,
        "port": 80,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "1,2",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "snat_port_preserve_enable": 0,
        "snat_port_preserve_type": 0,        
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "no_dest_nat": 0,
        "waf_profile": "",
        "http_profile": "",
        "cache_profile": "",          
        "tcpagent_profile": "",        
        "serverssl_profile": "",       
        "connmulti_profile": "",      
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "ACL_ID_aclv6_va",
    "acl_name": "aclv6",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "httpsvs",
        "protocol": 15,
        "port": 443,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "aclv6",
        "erules": [],
        "send_reset": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "no_dest_nat": 0,
        "waf_profile": "",
        "http_profile": "",
        "cache_profile": "",
        "tcpagent_profile": "",
        "clientssl_profile": "",      
        "serverssl_profile": "",
        "connmulti_profile": "",
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "0.0.0.0_va",
    "address": "0.0.0.0",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "rtspvs",
        "protocol": 8,
        "port": 554,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "2",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "no_dest_nat": 0,
        "syncookie": {
          "syncookie": 0
        },
        "tcp_profile": "",
        "rtsp_profile": "",             
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "6.6.6.6_va",
    "address": "6.6.6.6",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "smtpvs",
        "protocol": 17,
        "port": 25,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "tcpagent_profile": "",
        "clientssl_profile": "",
        "smtp_profile": "",          
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "7.7.7.7_va",
    "address": "7.7.7.7",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "sipvs",
        "protocol": 11,
        "port": 5060,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "connection_mirror": 0,
        "udp_profile": "",
        "srcip_persist": "",
        "sip_profile": "",             
        "dns_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "4.4.4.4_va",
    "address": "4.4.4.4",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "siptcpvs",
        "protocol": 18,
        "port": 5060,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "serverssl_profile": "",
        "connmulti_profile": "",
        "tcpagent_profile": "",
        "srcip_persist": "",
        "sip_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "5.5.5.5_va",
    "address": "5.5.5.5",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "SSLAGENTvs",
        "protocol":16,
        "port": 443,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "tcpagent_profile": "",
        "clientssl_profile": "",
        "serverssl_profile": "",
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "8.8.8.8_va",
    "address": "8.8.8.8",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "tcpvs",
        "protocol": 2,
        "port": 80,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "snat_port_preserve_enable": 0,
        "snat_port_preserve_type": 0,        
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "connection_mirror": 0,
        "no_dest_nat": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "tcp_profile": "",
        "srcip_persist": "",
        "sslid_persis": ""
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "9.9.9.9_va",
    "address": "9.9.9.9",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "TCPAGENTvs",
        "protocol":20,
        "port": 80,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "snat_port_preserve_enable": 0,
        "snat_port_preserve_type": 0,        
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "fixup_ftp": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "tcpagent_profile": "",
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "10.10.10.10_va",
    "address": "10.10.10.10",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "TCP-EXCHANGEvs",
        "protocol": 25,
        "port": 80,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "source_nat": "",
        "connmulti_profile": "",
        "tcpagent_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "12.12.12.12_va",
    "address": "12.12.12.12",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "mblbvs",
        "protocol": 26,
        "port": 80,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "source_nat": "",
        "connmulti_profile": "",
        "tcpagent_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "13.13.13.13_va",
    "address": "13.13.13.13",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "tftpvs",
        "protocol": 23,
        "port": 69,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "connection_mirror": 0,
        "no_dest_nat": 0,
        "source_nat": "",
        "udp_profile": "",
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "14.14.14.14_va",
    "address": "14.14.14.14",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "radiusvs",
        "protocol": 28,
        "port": 1813,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
       "aclnamev6": "",
        "erules": [],
        "connection_mirror": 0,
        "no_dest_nat": 0,
        "source_nat": "",
        "udp_profile": "",
        "srcip_persist": "",
        "dns_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "15.15.15.15_va",
    "address": "15.15.15.15",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "udpvs",
        "protocol": 3,
        "port": 8000,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "snat_port_preserve_enable": 0,
        "snat_port_preserve_type": 0,        
        "aclnamev6": "",
        "erules": [],
        "connection_mirror": 0,
        "no_dest_nat": 0,
        "source_nat": "",
        "udp_profile": "",           
        "srcip_persist": "",
        "dns_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  },
  {
    "tc_name": "",
    "name": "16.16.16.16_va",
    "address": "16.16.16.16",
    "status": 1,
"arp_status": 1,
"icmp_disable": 0,
    "vrid": 0,
    "redistribution": 0,
    "policy_profile": "",
    "virtual_services": [
      {
        "name": "othervs",
        "protocol": 5,
        "port": 0,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "no_dest_nat": 0,
        "source_nat": "",
        "srcip_persist": "",
        "l4_profile_type": 3,     
        "udp_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
    ]
  }
]

虚拟地址获取
Action:  slb.va.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟地址名称	是	虚拟地址名称必须存在

请求举例：
POST 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.get
请求body
{
    "name": "11.11.11.11_va"         
}
响应参数:
参考虚拟地址列表响应参数
响应举例：
{ 
"tc_name": "", 
"name": "11.11.11.11_va", 
"address": "11.11.11.11", 
"status": 1, 
"arp_status": 1, 
"icmp_disable": 0,
"vrid": 0, 
"redistribution": 0, 
"policy_profile": "", 
"virtual_services": 
[{ 
"name": 
"11.11.11.11", 
"protocol": 9, 
"port": 80, 
"pool": "pool", 
"connection_limit": {
"status": 0, 
"connection_limit_number": 8000000 }, 
"vs_enable_intf": "", 
"path_persist": 1, 
"status": 1, 
"desc_vport": "", 
"snat_on_vip": 0, 
"aclnamev6": "", 
"erules": [], 
"send_reset": 0, 
"source_nat": "", 
"no_dest_nat": 0, 
"auto_snat": 0, 
"waf_profile": "12345", 
"http_profile": "", 
"tcp_profile": "", 
"snat_port_preserve_enable": 0, 
"snat_port_preserve_type": 0,
 "connmulti_profile": "", 
"srcip_persist": "", 
"policy_profile": "", 
"aclsnats": [] }] 
}


虚拟地址添加
虚拟地址有四种类型，分别为：IPv4/IPv6地址类型、子网类型、IPv4 ACL类型和IPv6 ACL类型。
添加IPv4/IPv6类型的虚拟地址
Action:  slb.va.add
请求参数:
名称	类型	范围	含义	必选	备注
virtual_address	不涉及	不涉及	虚拟地址
由虚拟地址成员组成的数组：
virtual_address > tc_name:
类型：字符串
范围：1-191
含义：流量控制
virtual_address > name:
类型：字符串
范围：1-191
含义：虚拟地址名称
virtual_address > address:
类型：字符串
范围：1-63
含义：ipv4/v6类型的虚拟地址才有此参数
备注：address/network/acl三选一，具体使用方法请参考web用户手册
virtual_address > name:
类型：字符串
范围：1-191
含义：虚拟地址名称
virtual_address > status:
类型：整数
范围：0-1，1:启用；0:禁用;缺省值:1
含义：虚拟地址状态
virtual_address > arp_status:
类型：整数
范围：0-1
含义：ARP状态1:启用；0:禁用
virtual_address > icmp_probe:
类型：整数
范围：0-3
含义：ping vip地址0:always；1:disable；2:all；3:any
virtual_address > vird:
类型：整数
范围：0-8
含义：vrrp组id，
virtual_address > vird:
类型：整数
范围：0-8
含义：vrrp组id，
virtual_address > redistribution:
类型：整数
范围：0-3
含义：路由联动
0:禁用；
1:启用；
2:all；
3:any
virtual_address > policy_profile:
类型：字符串
范围：1-191
含义：策略模版，
virtual_address > :natlog_profile
类型：字符串
范围：1-191
含义：nat日志模板	是	

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.add
请求body

{
  "virtual_address":
        {
        "tc_name": "",
        "name": "test_api_vsaddrip",
        "address": "192.168.254.23",
        "status": 1,
        "arp_status": 1,
        "vrid": 0,
        "redistribution": 0,
        "policy_profile": "",
        "icmp_probe": 0,
        "natlog_profile": "",
        "virtual_services": [
        ]
    }
}

添加子网类型的虚拟地址
Action:  slb.va.add
请求参数:
名称	类型	范围	含义	必选	备注
virtual_address	字符串	长度1-191	虚拟地址
由虚拟地址成员组成的数组：
virtual_address > tc_name:
类型：字符串
范围：1-191
含义：流量控制
virtual_address > name:
类型：字符串
范围：1-191
含义：虚拟地址名称
virtual_address > address:
类型：字符串
范围：1-63
含义：ipv4/v6类型的虚拟地址才有此参数
备注：Address/network/acl三选一，具体使用方法请参考web用户手册
virtual_address > name:
类型：字符串
范围：1-191
含义：虚拟地址名称
virtual_address > status:
类型：整数
范围：0-1，1:启用；0:禁用;缺省值:1
含义：虚拟地址状态
virtual_address > arp_status:
类型：整数
范围：0-1
含义：arp状态1:启用；0:禁用
virtual_address > icmp_probe:
类型：整数
范围：0-3
含义：ping vip地址
0:always；
1:disable；
2:all；
3:any
virtual_address > vird:
类型：整数
范围：0-8
含义：vrrp组id，
virtual_address > vird:
类型：整数
范围：0-8
含义：vrrp组id，
virtual_address > redistribution:
类型：整数
范围：0-3
含义：路由联动
0:禁用；
1:启用；
2:all；
3:any
virtual_address > policy_profile:
类型：字符串
范围：1-191
含义：策略模版，
virtual_address > :natlog_profile
类型：字符串
范围：1-191
含义：nat日志模板，

	是	唯一

请求举例：
POST  http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.add
请求body
{
  "virtual_address":
    {
        "tc_name": "",
        "name": "192.168.123.2_24_va",
        "subnet": {
            "address": "192.168.123.2",
            "mask_len": 24
        },
        "status": 1,
        "arp_status": 1,
        "vrid": 0,
        "redistribution": 0,
        "policy_profile": "",
        "icmp_probe": 0,
        "natlog_profile": ""
    }
}

添加IPv4 ACL类型的虚拟地址
Action:  slb.va.add
请求参数:
名称	类型	范围	含义	必选	备注
virtual_address	字符串	长度1-191	虚拟地址
由虚拟地址成员组成的数组：
virtual_address > tc_name:
类型：字符串
范围：1-191
含义：流量控制
virtual_address > name:
类型：字符串
范围：1-191
含义：虚拟地址名称
virtual_address > address:
类型：字符串
范围：1-63
含义：ipv4/v6类型的虚拟地址才有此参数
备注：address/network/acl三选一，具体使用方法请参考web用户手册
virtual_address > name:
类型：字符串
范围：1-191
含义：虚拟地址名称
virtual_address > status:
类型：整数
范围：0-1，1:启用；0:禁用;缺省值:1
含义：虚拟地址状态
virtual_address > arp_status:
类型：整数
范围：0-1
含义：ARP状态1:启用；0:禁用
virtual_address > icmp_probe:
类型：整数
范围：0-3
含义：ping vip地址0:always；
1:disable；
2:all；
3:any
virtual_address > vird:
类型：整数
范围：0-8
含义：vrrp组id，
virtual_address > vird:
类型：整数
范围：0-8
含义：vrrp组id，
virtual_address > redistribution:
类型：整数
范围：0-3
含义：路由联动
0:禁用；
1:启用；
2:all；
3:any
virtual_address > policy_profile:
类型：字符串
范围：1-191
含义：策略模版，
virtual_address > :natlog_profile
类型：字符串
范围：1-191
含义：nat日志模板，	是	唯一


请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.add
请求body
{
  "virtual_address":
   {
        "tc_name": "",
        "name": "ACL_ID_101_va",
        "acl_id": 101,
        "status": 1,
        "arp_status": 1,
        "vrid": 0,
        "redistribution": 0,
        "policy_profile": "",
        "icmp_probe": 0,
        "natlog_profile": "",
        "virtual_services": [
        ]
    }
}

添加IPv6 ACL类型的虚拟地址
Action:  slb.va.add
请求参数:
名称	类型	范围	含义	必选	备注
virtual_address	数组	不涉及	虚拟地址
由虚拟地址成员组成的数组：
virtual_address > tc_name:
类型：字符串
范围：1-191
含义：流量控制
virtual_address > name:
类型：字符串
范围：1-191
含义：虚拟地址名称
virtual_address > address:
类型：字符串
范围：1-63
含义：ipv4/v6类型的虚拟地址才有此参数
备注：Address/network/acl三选一，具体使用方法请参考web用户手册
virtual_address > name:
类型：字符串
范围：1-191
含义：虚拟地址名称
virtual_address > status:
类型：整数
范围：0-1，1:启用；0:禁用;缺省值:1
含义：虚拟地址状态
virtual_address > arp_status:
类型：整数
范围：0-1
含义：arp状态1:启用；0:禁用
virtual_address > icmp_probe:
类型：整数
范围：0-3
含义：ping vip地址0:always；1:disable；2:all；3:any
virtual_address > vird:
类型：整数
范围：0-8
含义：vrrp组id，
virtual_address > vird:
类型：整数
范围：0-8
含义：vrrp组id，
virtual_address > redistribution:
类型：整数
范围：0-3
含义：路由联动
0:禁用；
1:启用；
2:all；
3:any
virtual_address > policy_profile:
类型：字符串
范围：1-191
含义：策略模版，
virtual_address > :natlog_profile
类型：字符串
范围：1-191
含义：nat日志模板，	是	唯一


请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.add
请求body

{
  "virtual_address":
    {
      "tc_name": "",
      "name": "test_aclv6_va",
      "acl_name": "test_aclv6",  
      "status": 1,
      "arp_status": 1,
      "icmp_disable": 0,
      "vrid": 0,
      "redistribution": 0,
      "policy_profile": ""
    }
}

虚拟地址编辑
Action:  slb.va.edit
请求参数:
虚拟地址编辑的参数与虚拟地址添加的请求参数完全相同
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.edit

{
  "virtual_address":
    {
        "tc_name": "",
        "name": "test_api_vsaddrip",
        "address": "192.168.254.23",
        "status": 1,
        "arp_status": 1,
        "vrid": 0,
        "redistribution": 0,
        "policy_profile": "",
        "icmp_probe": 0,
        "natlog_profile": ""
}}
}	编辑和添加格式完全相同，只是action不同

虚拟地址删除
Action:  slb.va.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟地址名称	是	虚拟地址必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.del
{
    "name": "4.5.6.7_va"
}
虚拟地址状态列表
Action:  slb.va.stat.list
请求参数:无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.va.stat.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	虚拟地址名称
address	字符串	长度1-63	虚拟地址的地址
status	整数	0-4	虚拟地址状态：0禁用，1全部正常，2部分正常，3故障，4 未知
current_conns	整数	>=0	虚拟地址当前并发连接数
total_conns	整数	>=0	虚拟地址累计连接连接数
send_packets	整数	>=0	虚拟地址发送包数
receive_packets	整数	>=0	虚拟地址接收包数
send_bytes	整数	>=0	虚拟地址发送字节数
由以下数组组成的虚拟地址发送字节数：
receive_bytes > receive_bytes:
        类型：整数
范围：>=0
含义：虚拟地址接收字节数
receive_bytes > receive_rate:
        类型：整数
范围：>=0
含义：虚拟地址接收接受速率，单位bps
receive_bytes > send_rate:
        类型：整数
范围：>=0
含义：虚拟地址接发送速率，单位bps
request_current	整数	>=0	虚拟地址当前请求
request_total	整数	>=0	虚拟地址累计请求
request_success	整数	>=0	虚拟地址累计成功请求
virtual_services_stat	数组		由虚拟服务状态统计信息对象组成的数组详细参数如下：
virtual_services_stat > name:
        类型：字符串
范围：1-63
含义：虚拟服务名称
virtual_services_stat > protocol:
类型：整数
范围：不涉及
含义：虚拟服务类型含义
2：TCP
3：UDP
5：OTHER
8：RTSP
9：FTP
11：SIP
12：FAST_HTTP  (HTTP普通)
14：HTTP(HTTP增强)
15：HTTPS
16：SSL_AGENT
17：SMTP
18：SIP-TCP
20：TCP_AGENT
21：DIAMETER
22：DNS
23：TFTP
25：TCP-EXCHANGE
26：MBLB
28：RADIUS
virtual_services_stat  > port:
类型：整数
范围：0-65534
含义：虚拟服务端口
virtual_services_stat  > status:
类型：整数
范围：0-2
含义：虚拟服务状态：0禁用，1全部正常，2部分正常，3故障，4未知
virtual_services_stat > current_conns:
类型：对象
范围：>=0
含义：虚拟服务当前并发连接数
virtual_services_stat  >total_connst:
类型：整数
范围：>=0
含义：虚拟服务累计连接连接数
virtual_services_stat  >send_packets:
类型：整数
范围：>=0
含义：虚拟服务发送包数
virtual_services_stat  >receive_packets:
类型：整数
范围：>=0
含义：虚拟服务接收包数
virtual_services_stat  >send_bytes:
类型：整数
范围：>=0
含义：虚拟服务发送字节数
virtual_services_stat  >receive_bytes:
类型：整数
范围：>=0
含义：虚拟服务接收字节数
virtual_services_stat  >request_current:
类型：整数
范围：>=0
含义：虚拟服务当前请求
virtual_services_stat  >request_total:
类型：整数
范围：>=0
含义：虚拟服务累计请求
virtual_services_stat  >request_success:
类型：整数
范围：>=0
含义：虚拟服务累计成功请求

响应举例：
[
  {
    "name": "1.2.3.4_va",
    "address": "1.2.3.4",
    "status": 1,               
    "current_conns": 0,
    "total_conns": 0,
    "send_packets": 0,
    "receive_packets": 0,
    "send_bytes": 0,
"receive_bytes": 0,
"receive_rate": 0,
"send_rate": 0,
    "request_current": 0,
    "request_total": 0,
    "request_success": 0,
    "virtual_services_stat": [
      {
        "name": "vs",
        "port": 443,
        "protocol": 15,
        "status": 1,            
        "current_conns": 0,
        "total_conns": 0,
        "send_packets": 0,
        "receive_packets": 0,
        "send_bytes": 0,
        "receive_bytes": 0,
        "request_current": 0,
        "request_total": 0,
        "request_success": 0
      }
    ]
  }
]
虚拟地址状态获取
Action:  slb.va.stat.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟地址名称	是	虚拟地址必须存在

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.va.stat.get
请求body:
{
    "name": "1.2.3.4_va"
}
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	虚拟地址名称
address	字符串	长度1-63	虚拟地址的地址
status	整数	0-4	虚拟地址的状态：0禁用，1全部正常，2部分正常，3故障，4未知
current_conns	整数	>=0	虚拟地址当前并发连接数
total_conns	整数	>=0	虚拟地址累计连接连接数
send_packets	整数	>=0	虚拟地址发送包数
receive_packets	整数	>=0	虚拟地址接收包数
send_bytes	整数	>=0	虚拟地址发送字节数
由以下数组组成的虚拟地址发送字节数：
receive_bytes > receive_bytes:
        类型：整数
范围：>=0
含义：虚拟地址接收字节数
receive_bytes > receive_rate:
        类型：整数
范围：>=0
含义：虚拟地址接收接受速率，单位bps
receive_bytes > send_rate:
        类型：整数
范围：>=0
含义：虚拟地址接发送速率，单位bps
request_current	整数	>=0	虚拟地址当前请求
request_total	整数	>=0	虚拟地址累计请求
request_success	整数	>=0	虚拟地址累计成功请求
virtual_services_stat	数组		由虚拟服务状态统计信息对象组成的数组详细参数如下：
virtual_services_stat > name:
        类型：字符串
范围：1-63
含义：虚拟服务名称
virtual_services_stat > protocol:
类型：整数
范围：不涉及
含义：虚拟服务类型含义
2：TCP
3：UDP
5：OTHER
8：RTSP
9：FTP
11：SIP
12：FAST_HTTP  (HTTP普通)
14：HTTP(HTTP增强)
15：HTTPS
16：SSL_AGENT
17：SMTP
18：SIP-TCP
20：TCP_AGENT
21：DIAMETER
22：DNS
23：TFTP
25：TCP-EXCHANGE
26：MBLB
28：RADIUS
virtual_services_stat  > port:
类型：整数
范围：0-65534
含义：虚拟服务端口
virtual_services_stat  > status:
类型：整数
范围：0，1，3
含义：虚拟服务状态：0禁用，1全部正常，2部分正常，3故障，4未知
virtual_services_stat > current_conns:
类型：对象
范围：>=0
含义：虚拟服务当前并发连接数
virtual_services_stat  >total_connst:
类型：整数
范围：>=0
含义：虚拟服务累计连接连接数
virtual_services_stat  >send_packets:
类型：整数
范围：>=0
含义：虚拟服务发送包数
virtual_services_stat  >receive_packets:
类型：整数
范围：>=0
含义：虚拟服务接收包数
virtual_services_stat  >send_bytes:
类型：整数
范围：>=0
含义：虚拟服务发送字节数
virtual_services_stat  >receive_bytes:
类型：整数
范围：>=0
含义：虚拟服务接收字节数
virtual_services_stat  >request_current:
类型：整数
范围：>=0
含义：虚拟服务当前请求
virtual_services_stat  >request_total:
类型：整数
范围：>=0
含义：虚拟服务累计请求
virtual_services_stat  >request_success:
类型：整数
范围：>=0
含义：虚拟服务累计成功请求

响应举例： 
  {
    "name": "1.2.3.4_va",
    "address": "1.2.3.4",
    "status": 1,               
    "current_conns": 0,
    "total_conns": 0,
    "send_packets": 0,
    "receive_packets": 0,
    "send_bytes": 0,
"receive_bytes": 0,
"receive_rate": 0,
"send_rate": 0,
    "request_current": 0,
    "request_total": 0,
    "request_success": 0,
    "virtual_services_stat": [
      {
        "name": "vs",
        "port": 443,
        "protocol": 15,
        "status": 1,            
        "current_conns": 0,
        "total_conns": 0,
        "send_packets": 0,
        "receive_packets": 0,
        "send_bytes": 0,
        "receive_bytes": 0,
"receive_rate": 0,
"send_rate": 0,
        "request_current": 0,
        "request_total": 0,
        "request_success": 0
      }
    ]
  }
虚拟地址状态清除
Action:  slb.va.stat.clear
请求参数:无
请求举例:
GET http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.va.stat.clear
	此API会清除所有虚拟地址的统计信息

虚拟服务
添加虚拟服务
	添加虚拟服务之前需要先添加虚拟地址。


Action:  slb.va.vs.add
公共请求参数:所有类型的虚拟服务都具有的参数,后续各种虚拟服务不再列举这些参数
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟服务使用过的虚拟地址名称	是	必须存在
virtual_service	对象	不涉及	所有虚拟服务的参数都在此对象中
由虚拟服务状态统计信息对象组成的数组详细参数如下：
virtual_services > name:
        类型：字符串
范围：1-63
含义：虚拟服务名称
virtual_services > protocol:
类型：整数
范围：不涉及
含义：虚拟服务类型含义
2：TCP
3：UDP
5：OTHER
8：RTSP
9：FTP
11：SIP
12：FAST_HTTP  (HTTP普通)
14：HTTP(HTTP增强)
15：HTTPS
16：SSL_AGENT
17：SMTP
18：SIP-TCP
20：TCP_AGENT
21：DIAMETER
22：DNS
23：TFTP
25：TCP-EXCHANGE
26：MBLB
28：RADIUS
virtual_services  > port:
类型：整数
范围：0-65534
含义：虚拟服务端口
virtual_services_stat  > status:
类型：整数
范围：0，1，3
含义：虚拟服务状态：0禁用，1全部正常，2部分正常，3故障，4未知
virtual_services_stat  > pool:
类型：字符串
范围：1-63
含义：虚拟服务使用的服务池的名称
virtual_services_stat  > connection_limit:
类型：对象
范围：不涉及
含义：虚拟服务的并发连接限制对象
virtual_services_stat>connection_limit_number:
类型：整数
范围：1-8000000
含义：虚拟服务的并发连接接限制数值，仅当开启虚拟服务的并发连接限制开关是有效
	是	
vs_enable_intf	字符串	长度1-63	使能接口号,eth开头，逗号分隔	否	缺省值:空
status	整数	0,1	虚拟服务的并发连接限制开关:	否	1:启用；0:禁用;缺省值:0
syncookie	对象	不涉及	虚拟服务启用syn cookie功能	否	
syncookie	整数	0,1	syn cookie	否	1:启用；0:禁用;缺省值:0
path_persist	整数	0,1	路径保持:	否	1:启用；0:禁用;缺省值:1
status	整数	0,1	虚拟服务状态	否	1:启用；0:禁用;缺省值:1
desc_vport	字符串	长度1-191	虚拟服务描述	否	缺省值:空
snat_on_vip	整数	0,1	使能全局snat映射:1:启用；0:禁用	否	1:启用；0:禁用;缺省值:0
auto_snat	整数	0,1	接口snat:1:启用；0:禁用	否	1:启用；0:禁用;缺省值:0
snat_port_preserve_enable	整数	0,1	源端口保持:1:启用；0:禁用	否	1:启用；0:禁用;缺省值:0
snat_port_preserve_type	整数	0,1	源端口保持类型:1:强制；0:尝试	否	1:启用；0:禁用;缺省值:0
vs_acl_id	整数	0-199	访问列表,1-199表示对应acl，0表示没有配置	否	缺省值:0
aclnamev6	字符串	长度1-191	ipv6访问列表名称	否	缺省值:空
erules	数组	不涉及	关联的erule名称组成的列表	否	缺省值:空
send_reset	整数	0,1	选择节点失败发送rst:1:启用；0:禁用	否	缺省值:0
source_nat	字符串	长度1-63	源snat地址池	否	缺省值:空
srcip_persist	字符串	长度1-191	源地址保持模版,一个虚拟服务只能有一种连接保持模板	否	缺省值:空
dstip_persist	字符串	长度1-191	目的地址保持模版,一个虚拟服务只能有一种连接保持模板	否	缺省值:空
cookie_persist	字符串	长度1-191	cookie保持模版,一个虚拟服务只能有一种连接保持模板	否	缺省值:空
sslid_persis	字符串	长度1-191	SSL连接保持模版,一个虚拟服务只能有一种连接保持模板	否	缺省值:空
policy_profile	字符串	长度1-191	策略模版	否	缺省值:0
aclsnats	数组		策略地址转换
组成的数组，详细参数如下：
aclsnats > acl_id:
类型：整数
范围：1-199
含义：策略地址转换-acl id，
aclsnats > nat_pool:
类型：整数
范围：长度1-63
含义：策略地址转换-snat池	否	缺省值:空
acl_name	字符串	长度1-191	策略地址转换-ipv6 acl name	否	缺省值：空
connection_mirror	整数	0,1	连接镜像:1:启用；0:禁用	否	缺省值:0
no_dest_nat	整数	0,1	直接转发:1:启用；0:禁用	否	缺省值:0
immediate_action_on_service_down 	整数	范围0-2	服务down时的新建连接处理方式
	是	0 代表 默认无，
1代表丢弃，
2代表重置
vport_template_name	整数	范围1-191	虚拟服务模板	是	默认值为default
traffic_control	字符串	长度1-191	流量控制	否	
service_last_hop	字符串	长度1-191	路径保持服务池	否	
force_update_mac	整数	范围0-1	强制更新mac:1:启用；0:禁用	否	

添加DNS类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
udp_profile	字符串	长度1-191	虚拟服务使用的UDP模板名称	否	必须存在
dns_profile	字符串	长度1-191	虚拟服务使用的DNS模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{                   
    "name": "test_api_vsaddrip",       
    "virtual_service":          
      {
        "name": "dns",        
        "protocol": 22,          
        "port": 53,                                   
        "pool": "pool_dns",              
        "connection_limit": {      
          "status": 0,          
          "connection_limit_number": 8000000    
        },
        "vs_enable_intf": "",  
        "path_persist": 1,                
        "status": 1,
        "desc_vport": "",                
        "snat_on_vip": 0,                
        "auto_snat": 0,           
        "aclnamev6": "",      
        "erules": [                        
          ""     
        ],
        "send_reset": 0,       
        "source_nat": "",         
        "udp_profile": "",              
        "srcip_persist": "",
        "traffic_control": "",
       "force_update_mac": 1,    
        "dstip_persist": "",         
        "cookie_persist": "",         
        "sslid_persis": "",                                                   
        "dns_profile": "",             
        "policy_profile": "",         
        "aclsnats": [                
          
        ]
      }
  }

添加FTP类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
tcp_profile	字符串	长度1-191	虚拟服务使用的TCP模板名称	否	必须存在
ftp_profile	字符串	长度1-191	ftp模板	是	
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
      "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "ftpvs",
        "protocol": 9,
        "port": 21,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "connection_mirror": 0,  
        "no_dest_nat": 0,
        "traffic_control": "",
       "force_update_mac": 1,        
        "syncookie": {
          "syncookie": 0        
        },
        "source_nat": "",
        "tcp_profile": "",           
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }}

添加HTTP普通类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
tcp_profile	字符串	长度1-191	虚拟服务使用的TCP模板名称	否	必须存在
http_profile	字符串	长度1-191	虚拟服务使用的HTTP模板名称	否	必须存在
connmulti_profile	字符串	长度1-191	虚拟服务使用的连接复用模板名称	否	必须存在
waf_profile	字符串	长度1-191	虚拟服务使用的HTTP模板名称	否	必须存在
request_log_profile	字符串	长度1-191	虚拟服务使用的请求日志名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
 请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "httpvs",
        "protocol": 12,
        "port": 80,
        "pool": "pool",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "snat_port_preserve_enable": 0,    
        "snat_port_preserve_type": 0,          
        "aclnamev6": "",
        "erules": [
          "erule-empty.txt"
        ],
        "send_reset": 0,
        "source_nat": "",
        "no_dest_nat": 0,
        "waf_profile": "",    
        "http_profile": "",      
        "tcp_profile": "",
        "connmulti_profile": "",
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    
  }

添加HTTP增强类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
tcpagent_profile	字符串	长度1-191	虚拟服务使用的TCP代理模板名称	否	必须存在
http_profile	字符串	长度1-191	虚拟服务使用的HTTP模板名称	否	必须存在
connmulti_profile	字符串	长度1-191	虚拟服务使用的连接复用模板名称	否	必须存在
waf_profile	字符串	长度1-191	虚拟服务使用的waf模板名称	否	必须存在
cache_profile	字符串	长度1-191	虚拟服务使用的缓存模板名称	否	必须存在
serverssl_profile	字符串	长度1-191	虚拟服务使用的服务端SSL卸载模板名称	否	必须存在
request_log_profile	字符串	长度1-191	虚拟服务使用的请求日志名称	否	必须存在
fallback_persist_srcip	字符串	长度1-191	虚拟服务使用的备份源地址保持模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
"name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "httpvs",
        "protocol": 14,
        "port": 80,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "traffic_control": "",
       "force_update_mac": 1, 
        "snat_port_preserve_enable": 0,
        "snat_port_preserve_type": 0,        
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "no_dest_nat": 0,
        "waf_profile": "",
        "http_profile": "",
        "cache_profile": "",          
        "tcpagent_profile": "",        
        "serverssl_profile": "",       
        "connmulti_profile": "",      
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }

}
添加HTTPS类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
tcpagent_profile	字符串	长度1-191	虚拟服务使用的TCP代理模板名称	否	必须存在
http_profile	字符串	长度1-191	虚拟服务使用的HTTP模板名称	否	必须存在
connmulti_profile	字符串	长度1-191	虚拟服务使用的连接复用模板名称	否	必须存在
waf_profile	字符串	长度1-191	虚拟服务使用的HTTP模板名称	否	必须存在
cache_profile	字符串	长度1-191	虚拟服务使用的缓存模板名称	否	必须存在
serverssl_profile	字符串	长度1-191	虚拟服务使用的服务端SSL卸载模板名称	否	必须存在
clientssl_profile	字符串	长度1-191	虚拟服务使用的客户端SSL卸载模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
   "name": "test_api_vsaddrip",
    "virtual_service": 
        {
    "name": "https_2",
    "protocol": 15,
    "port": 449,
    "pool": "",
    "connection_limit": {
        "status": 0,
        "connection_limit_number": 8000000
    },
    "vs_enable_intf": "",
    "path_persist": 1,
    "status": 1,
    "desc_vport": "",
    "snat_on_vip": 0,
    "service_last_hop": "",
    "aclnamev6": "",
    "traffic_control": "",
    "vport_template_name": "",
    "immediate_action_on_service_down": 0,
    "traffic_control": "",
    "force_update_mac": 1, 
    "erules": [],
    "send_reset": 0,
    "syncookie": {
        "syncookie": 0
    },
    "source_nat": "",
    "no_dest_nat": 0,
    "auto_snat": 0,
    "waf_profile": "",
    "request_log_profile": "",
    "http_profile": "",
    "http2_profile": "",
    "cache_profile": "",
    "tcpagent_profile": "",
    "clientssl_profile": "",
    "serverssl_profile": "",
    "connmulti_profile": "",
    "srcip_persist": "",
    "fallback_persist_srcip": "",
    "policy_profile": "",
    "aclsnats": []
}
}

添加RTSP类型的虚拟服务
Action:  slb.va.vs.add
请求参数
名称	类型	范围	含义	必选	备注
tcp_profile	字符串	长度1-191	虚拟服务使用的TCP模板名称	否	必须存在
rtsp_profile	字符串	长度1-191	虚拟服务使用的RTSP模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "rtspvs",
        "protocol": 8,
        "port": 554,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "no_dest_nat": 0,
    "traffic_control": "",
        "force_update_mac": 1, 
        "syncookie": {
          "syncookie": 0
        },
        "tcp_profile": "",
        "rtsp_profile": "",             
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    
  }

添加SMTP类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
tcpagent_profile	字符串	长度1-191	虚拟服务使用的TCP代理模板名称	否	必须存在
smtp_profile	字符串	长度1-191	虚拟服务使用的SMTP模板名称	否	必须存在
clientssl_profile	字符串	长度1-191	虚拟服务使用的客户端SSL卸载模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "smtpvs",
        "protocol": 17,
        "port": 25,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0, 
        "aclnamev6": "",
       "traffic_control": "",
       "force_update_mac": 1, 
        "erules": [],
        "send_reset": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "tcpagent_profile": "",
        "clientssl_profile": "",
        "smtp_profile": "",          
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    
  }
添加SIP类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
udp_profile	字符串	长度1-191	虚拟服务使用的UDP模板名称	否	必须存在
sip_profile	字符串	长度1-191	虚拟服务使用的SIP模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body

{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "sip_vs",
        "protocol": 11,
        "port": 5060,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
    "traffic_control": "",
       "force_update_mac": 1, 
        "snat_on_vip": 0,
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "connection_mirror": 0,
        "udp_profile": "",
        "srcip_persist": "",
        "sip_profile": "",             
        "policy_profile": "",
        "aclsnats": []
      }
}
添加SIP-TCP类型的虚拟服务
Action:  slb.va.vs.add
请求参数
名称	类型	范围	含义	必选	备注
sip_profile	字符串	长度1-191	虚拟服务使用的SIP模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "sip_vs",
        "protocol": 11,
        "port": 5060,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
    "traffic_control": "",
       "force_update_mac": 1, 
        "snat_on_vip": 0,
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "connection_mirror": 0,
        "udp_profile": "",
        "srcip_persist": "",
        "sip_profile": "",             
        "policy_profile": "",
        "aclsnats": []
      }
}
添加SSLAGENT类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
tcpagent_profile	字符串	长度1-191	虚拟服务使用的TCP代理模板名称	否	必须存在
serverssl_profile	字符串	长度1-191	虚拟服务使用的服务端SSL卸载模板名称	否	必须存在
clientssl_profile	字符串	长度1-191	虚拟服务使用的客户端SSL卸载模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "SSLAGENTvs",
        "protocol": 16,
        "port": 443,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "traffic_control": "",
        "force_update_mac": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "snat_port_preserve_enable": 0,    
        "snat_port_preserve_type": 0,  
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "tcpagent_profile": "",
        "clientssl_profile": "",
        "serverssl_profile": "",
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    
  }

添加TCP类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
tcp_profile	字符串	长度1-191	虚拟服务使用的TCP模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.v
a.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "tcpvs",
        "protocol": 2,
        "port": 8000,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "traffic_control": "",
        "force_update_mac": 1,
               "snat_on_vip": 0,
        "auto_snat": 0,
        "snat_port_preserve_enable": 0,
        "snat_port_preserve_type": 0,        
        "aclnamev6": "",
        "erules": [],
        "send_reset": 0,
        "connection_mirror": 0,
        "no_dest_nat": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "tcp_profile": "",
        "srcip_persist": "",
        "sslid_persis": ""
      }
  }

添加TCP_AGENT类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
tcpagent_profile	字符串	长度1-191	虚拟服务使用的TCP代理模板名称	否	必须存在
fixup_ftp	整数	0，1	FTP协议修正,1:开启;0:关闭;	否	缺省值:0
serverssl_profile	字符串	长度1-191	配置SSL服务端模板得名称	否	
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "TCPAGENTvs",
        "protocol": 20,
        "port": 8001,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "snat_port_preserve_enable": 0,
        "snat_port_preserve_type": 0,        
        "aclnamev6": "",
        "erules": [],
        "traffic_control": "",
        "force_update_mac": 1,
        "send_reset": 0,
        "fixup_ftp": 0,
        "syncookie": {
          "syncookie": 0
        },
        "source_nat": "",
        "tcpagent_profile": "",
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    
  }
添加TCP-EXCHANGE类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
tcpagent_profile	字符串	长度1-191	虚拟服务使用的TCP代理模板名称	否	必须存在
connmulti_profile	字符串	长度1-191	虚拟服务使用的连接复用模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "TCP-EXCHANGEvs",
        "protocol": 25,
        "port": 8002,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0, 
        "aclnamev6": "",
        "traffic_control": "",
        "force_update_mac": 1,
        "erules": [],
        "source_nat": "",
        "connmulti_profile": "",
        "tcpagent_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
  }
添加MBLB类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
tcpagent_profile	字符串	长度1-191	虚拟服务使用的TCP代理模板名称	否	必须存在
connmulti_profile	字符串	长度1-191	虚拟服务使用的连接复用模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "mblbvs",
        "protocol": 26,
        "port": 8003,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "traffic_control": "",
        "force_update_mac": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0, 
        "aclnamev6": "",
        "erules": [],
        "source_nat": "",
        "connmulti_profile": "",
        "tcpagent_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
    
  }
添加TFTP类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
udp_profile	字符串	长度1-191	虚拟服务使用的UDP模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "tftpvs",
        "protocol": 23,
        "port": 69,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "traffic_control": "",
        "force_update_mac": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0, 
        "aclnamev6": "",
        "erules": [],
        "connection_mirror": 0,
        "no_dest_nat": 0,
        "source_nat": "",
        "udp_profile": "",
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
    
  }

添加RADIUS类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
udp_profile	字符串	长度1-191	虚拟服务使用的UDP模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": {
        "name": "radiusvs",
        "protocol": 28,
        "port": 1813,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
          "traffic_control": "",
        "force_update_mac": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0, 
        "aclnamev6": "",
        "erules": [],
        "no_dest_nat": 0,
        "source_nat": "",
        "udp_profile": "",
        "srcip_persist": "",
        "policy_profile": "",
        "aclsnats": []
      }
  }
添加UDP类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
udp_profile	字符串	长度1-191	虚拟服务使用的UDP模板名称	否	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "udpvs",
        "protocol": 3,
        "port": 8000,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "traffic_control": "",
        "force_update_mac": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0,
        "snat_port_preserve_enable": 0,
        "snat_port_preserve_type": 0,        
        "aclnamev6": "",
        "erules": [],
        "connection_mirror": 0,
        "no_dest_nat": 0,
        "source_nat": "",
        "udp_profile": "",           
        "srcip_persist": "",
        "dns_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
    
  }

添加OTHER类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
l4_profile_type	整数	2,3	运输层协议	否	2:TCP;3:UDP;缺省值2
tcp_profile	字符串	长度1-191	虚拟服务使用的TCP模板名称	否	当l4_profile_type为2时有效
udp_profile	字符串	长度1-191	虚拟服务使用的UDP模板名称	否	当l4_profile_type为3时有效

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
        "name": "othervs",
        "protocol": 5,
        "port": 0,
        "pool": "",
        "connection_limit": {
          "status": 0,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "traffic_control": "",
        "force_update_mac": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "auto_snat": 0, 
        "aclnamev6": "",
        "erules": [],
        "no_dest_nat": 0,
        "source_nat": "",
        "srcip_persist": "",
        "l4_profile_type": 3,       
        "udp_profile": "",
        "policy_profile": "",
        "aclsnats": []
      }
    
  }

添加DNS_TCP类型的虚拟服务
Action:  slb.va.vs.add
请求参数:
名称	类型	范围	含义	必选	备注
dns_profile	字符串	长度1-191	虚拟服务使用的DNS模板名称	否	
send_reset	整数	0，1	节点选择失败发送rst报文	否	
tcpagent_profile	字符串	长度1-191	TCP代理模板	否	

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.add
请求body
{    "name": "test_api_vsaddrip",
    "virtual_service": 
      {
    "name": "dns_tcp",
    "protocol": 6,
    "port": 53,
    "pool": "",
    "connection_limit": {
        "status": 0,
        "connection_limit_number": 8000000
    },
    "vs_enable_intf": "",
    "path_persist": 1,
    "status": 1,
    "desc_vport": "",
    "usertag": "",
    "snat_on_vip": 0,
    "service_last_hop": "",
    "aclnamev6": "",
    "security_policy_profile": "",
    "traffic_control": "",
    "force_update_mac": 0,
    "no_dest_nat_port_change": 0,
    "vport_template_name": "",
    "immediate_action_on_service_down": 0,
    "erules": [],
    "send_reset": 0,
    "syncookie": {
        "syncookie": 0
    },
    "source_nat": "",
    "tcpagent_profile": "",
    "srcip_persist": "",
    "dns_profile": "",
    "auto_snat": 0,
    "dns_log_profile": "",
    "policy_profile": "",
    "aclsnats": []
}}

虚拟服务获取
Action:  slb.va.vs.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟地址名称	是	必须存在
virtual_service	对象	不涉及	虚拟服务对象
由虚拟服务状态统计信息对象组成的数组详细参数如下：
virtual_services > protocol:
类型：整数
范围：不涉及
含义：虚拟服务类型含义
2：TCP
3：UDP
5：OTHER
8：RTSP
9：FTP
11：SIP
12：FAST_HTTP  (HTTP普通)
14：HTTP(HTTP增强)
15：HTTPS
16：SSL_AGENT
17：SMTP
18：SIP-TCP
20：TCP_AGENT
21：DIAMETER
22：DNS
23：TFTP
25：TCP-EXCHANGE
26：MBLB
28：RADIUS
virtual_services  > port:
类型：整数
范围：0-65534
含义：虚拟服务端口
	是	

请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.get
请求body
{
  "name": "1.2.3.4_va",         
  "virtual_service": 
    {
      "protocol": 12,
      "port": 444
    }
}

响应参数:slb.va.list响应参数列表中一个虚拟地址中virtual_services中的一个
响应举例：
{
    "name": "vs2",
    "protocol": 12,
    "port": 444,
    "pool": "pool",
    "connection_limit": {
        "status": 0,
        "connection_limit_number": 8000000
    },
    "vs_enable_intf": "",
    "path_persist": 1,
    "status": 1,
    "desc_vport": "",
    "snat_on_vip": 0,
    "aclnamev6": "",
    "erules": [],
    "send_reset": 0,
    "syncookie": {
        "syncookie": 0
    },
    "source_nat": "",
    "no_dest_nat": 0,
    "auto_snat": 0,
    "waf_profile": "",
    "http_profile": "",
    "cache_profile": "",
    "tcpagent_profile": "",
    "clientssl_profile": "",
    "serverssl_profile": "",
    "connmulti_profile": "",
    "srcip_persist": "",
    "policy_profile": "",
    "aclsnats": []
}

虚拟服务编辑
Action:  slb.va.vs.edit
请求参数:参考虚拟服务添加部分
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.edit
请求body
{
    "name": "test_api_vsaddrip",
    "virtual_service": 
    {
        "name": "VS_NAME_1",
        "protocol": 14,
        "port": 8000,
        "pool": "pool_http_1",
        "connection_limit": {
          "status": 1,
          "connection_limit_number": 8000000
        },
        "vs_enable_intf": "",
        "path_persist": 1,
        "status": 1,
        "desc_vport": "",
        "snat_on_vip": 0,
        "vs_acl_id": 52,
        "service_last_hop": "path_persist_pool_1",
        "aclnamev6": "",
        "traffic_control": "",
        "vport_template_name": "default",
        "immediate_action_on_service_down": 0,
        "erules": [],
        "send_reset": 0,
        "syncookie": {
          "syncookie": 0        
        },
        "source_nat": "",
        "no_dest_nat": 0,
        "auto_snat": 0,
        "waf_profile": "",
        "request_log_profile": "",
        "http_profile": "http-profile-1",
        "cache_profile": "",
        "tcpagent_profile": "",
        "snat_port_preserve_enable": 0,
        "snat_port_preserve_type": 0,
        "serverssl_profile": "",
        "connmulti_profile": "",
        "srcip_persist": "",
        "fallback_persist_srcip": "",
        "policy_profile": "",
        "aclsnats": []
    }
  }

	虚拟服务编辑和添加请求body相同，action不同，其他协议类型编辑参考添加


虚拟服务删除
Action:  slb.va.vs.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟地址名称	是	必须存在
virtual_service	对象	不涉及	虚拟服务对象
由虚拟服务状态统计信息对象组成的数组详细参数如下：
virtual_services > protocol:
类型：整数
范围：不涉及
含义：虚拟服务类型含义
2：TCP
3：UDP
5：OTHER
8：RTSP
9：FTP
11：SIP
12：FAST_HTTP  (HTTP普通)
14：HTTP(HTTP增强)
15：HTTPS
16：SSL_AGENT
17：SMTP
18：SIP-TCP
20：TCP_AGENT
21：DIAMETER
22：DNS
23：TFTP
25：TCP-EXCHANGE
26：MBLB
28：RADIUS
virtual_services  > port:
类型：整数
范围：0-65534
含义：虚拟服务端口
	是	

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.va.vs.del
请求body
{
  "name": "1.2.3.4_va",         
  "virtual_service": 
    {
      "protocol": 12,
      "port": 444
    }
}

虚拟服务状态获取
Action:  slb.va.vs.stat.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟地址名称	是	必须存在
virtual_service	对象	不涉及	虚拟服务对象
由虚拟服务状态统计信息对象组成的数组详细参数如下：
virtual_services > protocol:
类型：整数
范围：不涉及
含义：虚拟服务类型含义
2：TCP
3：UDP
5：OTHER
8：RTSP
9：FTP
11：SIP
12：FAST_HTTP  (HTTP普通)
14：HTTP(HTTP增强)
15：HTTPS
16：SSL_AGENT
17：SMTP
18：SIP-TCP
20：TCP_AGENT
21：DIAMETER
22：DNS
23：TFTP
25：TCP-EXCHANGE
26：MBLB
28：RADIUS
virtual_services  > port:
类型：整数
范围：0-65534
含义：虚拟服务端口
	是	

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.va.vs.stat.get
请求body
{
  "name": "1.2.3.4_va",         
  "virtual_service": 
    {
      "protocol": 12,
      "port": 444
    }
}
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	虚拟服务的名称
protocol	字符串	长度1-63	虚拟服务的类型，2：TCP
3：UDP
5：OTHER
6：DNS_TCP
8：RTSP
9：FTP
11：SIP
12：FAST_HTTP  (HTTP普通)
14：HTTP(HTTP增强)
15：HTTPS
16：SSL_AGENT
17：SMTP
18：SIP-TCP
20：TCP_AGENT
21：DIAMETER
22：DNS
23：TFTP
25：TCP-EXCHANGE
26：MBLB
28：RADIUS
port	整数	0-65534	虚拟服务的端口
status	整数	0-2	虚拟服务状态：0禁用，1全部正常，2部分正常，3故障，4未知
current_conns	整数	>=0	虚拟服务当前并发连接数
total_conns	整数	>=0	虚拟服务累计连接连接数
send_packets	整数	>=0	虚拟服务发送包数
receive_packets	整数	>=0	虚拟服务接收包数
send_bytes	整数	>=0	虚拟服务发送字节数
receive_bytes	整数	>=0	虚拟服务接收字节数
receive_rate	整数	>=0	虚拟地址接收接受速率，单位Bps
send_rate	整数	>=0	虚拟地址接发送速率，单位Bps
request_current	整数	>=0	虚拟服务当前请求
request_total	整数	>=0	虚拟服务累计请求
request_success	整数	>=0	虚拟服务累计成功请求
响应举例:
{
    "name": "vs2",
    "port": 444,
    "protocol": 12,
    "status": 1,
    "current_conns": 0,
    "total_conns": 0,
    "receive_packets": 0,
    "send_packets": 0,
    "receive_bytes": 0,
"send_bytes": 0,
"receive_rate": 0,
"send_rate": 0,
    "request_current": 0,
    "request_total": 0,
    "request_success": 0
}

虚拟服务状态汇总
Action:  slb.va.vs.stat.count.list
请求参数:无
请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.va.vs.stat.count.list
响应参数:
名称	类型	范围	含义
disabled	整数	>=0	虚拟服务状态为禁用的总个数
all_up	整数	>=0	虚拟服务状态为全部正常的总个数
some_up	整数	>=0	虚拟服务状态为部分正常的总个数
down	整数	>=0	虚拟服务状态为故障的总个数
响应举例:
{
    "disabled": 2,
    "all_up": 13,
    "some_up": 15,
    "down": 246
}



模板
TCP代理模板
TCP代理模板列表
Action：slb.profile.fastl4.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.fastl4.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
description	字符串	长度1-191	描述
fin_timeout	整数	1-60	fin超时
timeout	整数	60-100000	空闲超时
reset_timeout	整数	0-31	超时重置
half_close_timeout	整数	0,60-15000	fin等待
retransmit_number	整数	1-16	最大重传
syn_retransmit_number	整数	1-16	最大syn重传
time_wait	整数	0-600000	等待时间，单位为ms
receive_buff	整数	1-2000000000	接收缓冲区
send_buffer	整数	1-2000000000	发送缓冲区
start_win_size	整数	0-65535	接收窗口
nagle	整数	0-1	nagle算法;0禁用，1使能
window_scale	整数	0-14	tcp窗口比例
keep_alive_interval	整数	0,60-12000	keep-alive报文发送间隔，0关闭此功能
keep_alive_retry	整数	0,2-10	keep-alive报文重试次数，0关闭此功能
optts	整数	0-1	tcp时间戳;0禁用，1使能
tcp_accelerate_client	整数	0-1	tcp加速;0禁用，1使能
tcp_accelerate_client_cnwd	整数	1-10	网络冲突初始化窗口
tcp_accelerate_server	整数	0-1	服务器慢路径;0禁用，1使能
tcp_accelerate_server_cnwd	整数	1-10	服务器冲突初始化窗口
mss	整数	0,128-4312	最大分段
rstnode	整数	0-1	服务器rst;0禁用，1使能
rstclient	整数	0-1	客户端rst;0禁用，1使能
zero_window_timeout	整数	0-65535	零窗口超时
syn_rto_base	整数	0,1000-5000	syn重试超时，单位为ms，0关闭此功能
响应举例：
[
    {
        "name": "profile_tcp_agent_1",
        "description": "",
        "fin_timeout": 56,
        "timeout": 1201,
        "reset_timeout": 21,
        "half_close_timeout": 67,
        "retransmit_number": 7,
        "syn_retransmit_number": 8,
        "time_wait": 80001,
        "receive_buff": 512002,
        "send_buffer": 512002,
        "start_win_size": 2223,
        "nagle": 1,
        "window_scale": 4,
        "keep_alive_interval": 61,
        "keep_alive_retry": 8,
        "optts": 1,
        "tcp_accelerate_client": 1,
        "tcp_accelerate_client_cnwd": 8,
        "tcp_accelerate_server": 1,
        "tcp_accelerate_server_cnwd": 8,
        "mss": 1281,
        "rstnode": 1,
        "rstclient": 1,
        "zero_window_timeout": 1235,
        "syn_rto_base": 2346
    }
]

分区中获取common分区和自己分区的TCP代理模板列表
Action：slb.profile.fastl4.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.fastl4.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
description	字符串	长度1-191	描述
fin_timeout	整数	1-60	fin超时
timeout	整数	60-100000	空闲超时
reset_timeout	整数	0-31	超时重置
half_close_timeout	整数	0,60-15000	fin等待
retransmit_number	整数	1-16	最大重传
syn_retransmit_number	整数	1-16	最大syn重传
time_wait	整数	0-600000	等待时间，单位为ms
receive_buff	整数	1-2000000000	接收缓冲区
send_buffer	整数	1-2000000000	发送缓冲区
start_win_size	整数	0-65535	接收窗口
nagle	整数	0-1	nagle算法;0禁用，1使能
window_scale	整数	0-14	tcp窗口比例
keep_alive_interval	整数	0,60-12000	keep-alive报文发送间隔，0关闭此功能
keep_alive_retry	整数	0,2-10	keep-alive报文重试次数，0关闭此功能
optts	整数	0-1	tcp时间戳;0禁用，1使能
tcp_accelerate_client	整数	0-1	tcp加速;0禁用，1使能
tcp_accelerate_client_cnwd	整数	1-10	网络冲突初始化窗口
tcp_accelerate_server	整数	0-1	服务器慢路径;0禁用，1使能
tcp_accelerate_server_cnwd	整数	1-10	服务器冲突初始化窗口
mss	整数	0,128-4312	最大分段
rstnode	整数	0-1	服务器rst;0禁用，1使能
rstclient	整数	0-1	客户端rst;0禁用，1使能
zero_window_timeout	整数	0-65535	零窗口超时
syn_rto_base	整数	0,1000-5000	syn重试超时，单位为ms，0关闭此功能

响应举例：
[
    {
        "name": "partition_profile_tcpagent_2",
        "description": "partition_pro_tcpagent2",
        "fin_timeout": 30,
        "timeout": 1800,
        "reset_timeout": 15,
        "half_close_timeout": 120,
        "retransmit_number": 5,
        "syn_retransmit_number": 3,
        "time_wait": 8000,
        "receive_buff": 51200,
        "send_buffer": 51200,
        "start_win_size": 65530,
        "nagle": 1,
        "window_scale": 4,
        "keep_alive_interval": 61,
        "keep_alive_retry": 8,
        "optts": 1,
        "tcp_accelerate_client": 1,
        "tcp_accelerate_client_cnwd": 8,
        "tcp_accelerate_server": 1,
        "tcp_accelerate_server_cnwd": 8,
        "mss": 512,
        "rstnode": 1,
        "rstclient": 1,
        "zero_window_timeout": 1024,
        "syn_rto_base": 2346
    }
]

TCP代理模板获取
Action：slb.profile.fastl4.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.fastl4.get
请求body：
{
    "name": "profile_tcpagent_1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
description	字符串	长度1-191	描述
fin_timeout	整数	1-60	fin超时
timeout	整数	60-100000	空闲超时
reset_timeout	整数	0-31	超时重置
half_close_timeout	整数	0,60-15000	fin等待
retransmit_number	整数	1-16	最大重传
syn_retransmit_number	整数	1-16	最大syn重传
time_wait	整数	0-600000	等待时间，单位为ms
receive_buff	整数	1-2000000000	接收缓冲区
send_buffer	整数	1-2000000000	发送缓冲区
start_win_size	整数	0-65535	接收窗口
nagle	整数	0-1	nagle算法;0禁用，1使能
window_scale	整数	0-14	tcp窗口比例
keep_alive_interval	整数	0,60-12000	keep-alive报文发送间隔，0关闭此功能
keep_alive_retry	整数	0,2-10	keep-alive报文重试次数，0关闭此功能
optts	整数	0-1	tcp时间戳;0禁用，1使能
tcp_accelerate_client	整数	0-1	tcp加速;0禁用，1使能
tcp_accelerate_client_cnwd	整数	1-10	网络冲突初始化窗口
tcp_accelerate_server	整数	0-1	服务器慢路径;0禁用，1使能
tcp_accelerate_server_cnwd	整数	1-10	服务器冲突初始化窗口
mss	整数	0,128-4312	最大分段
rstnode	整数	0-1	服务器rst;0禁用，1使能
rstclient	整数	0-1	客户端rst;0禁用，1使能
zero_window_timeout	整数	0-65535	零窗口超时
syn_rto_base	整数	0,1000-5000	syn重试超时，单位为ms，0关闭此功能

响应举例：
{
    "name": "profile_tcpagent_1",
    "description": "",
    "fin_timeout": 56,
    "timeout": 1201,
    "reset_timeout": 21,
    "half_close_timeout": 67,
    "retransmit_number": 7,
    "syn_retransmit_number": 8,
    "time_wait": 80001,
    "receive_buff": 512002,
    "send_buffer": 512002,
    "start_win_size": 2223,
    "nagle": 1,
    "window_scale": 4,
    "keep_alive_interval": 61,
    "keep_alive_retry": 8,
    "optts": 1,
    "tcp_accelerate_client": 1,
    "tcp_accelerate_client_cnwd": 8,
    "tcp_accelerate_server": 1,
    "tcp_accelerate_server_cnwd": 8,
    "mss": 1281,
    "rstnode": 1,
    "rstclient": 1,
    "zero_window_timeout": 1235,
    "syn_rto_base": 2346
}
TCP代理模板增加
Action：slb.profile.fastl4.add
请求参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
description	字符串	长度1-191	描述
fin_timeout	整数	1-60	fin超时
timeout	整数	60-100000	空闲超时
reset_timeout	整数	0-31	超时重置
half_close_timeout	整数	0,60-15000	fin等待
retransmit_number	整数	1-16	最大重传
syn_retransmit_number	整数	1-16	最大syn重传
time_wait	整数	0-600000	等待时间，单位为ms
receive_buff	整数	1-2000000000	接收缓冲区
send_buffer	整数	1-2000000000	发送缓冲区
start_win_size	整数	0-65535	接收窗口
nagle	整数	0-1	nagle算法;0禁用，1使能
window_scale	整数	0-14	tcp窗口比例
keep_alive_interval	整数	0,60-12000	keep-alive报文发送间隔，0关闭此功能
keep_alive_retry	整数	0,2-10	keep-alive报文重试次数，0关闭此功能
optts	整数	0-1	tcp时间戳;0禁用，1使能
tcp_accelerate_client	整数	0-1	tcp加速;0禁用，1使能
tcp_accelerate_client_cnwd	整数	1-10	网络冲突初始化窗口
tcp_accelerate_server	整数	0-1	服务器慢路径;0禁用，1使能
tcp_accelerate_server_cnwd	整数	1-10	服务器冲突初始化窗口
mss	整数	0,128-4312	最大分段
rstnode	整数	0-1	服务器rst;0禁用，1使能
rstclient	整数	0-1	客户端rst;0禁用，1使能
zero_window_timeout	整数	0-65535	零窗口超时
syn_rto_base	整数	0,1000-5000	syn重试超时，单位为ms，0关闭此功能

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.fastl4.add
请求body：
{
    "name": "profile_tcpagent_1",
    "description": "",
    "fin_timeout": 56,
    "timeout": 1201,
    "reset_timeout": 21,
    "half_close_timeout": 67,
    "retransmit_number": 7,
    "syn_retransmit_number": 8,
    "time_wait": 80001,
    "receive_buff": 512002,
    "send_buffer": 512002,
    "start_win_size": 2223,
    "nagle": 1,
    "window_scale": 4,
    "keep_alive_interval": 61,
    "keep_alive_retry": 8,
    "optts": 1,
    "tcp_accelerate_client": 1,
    "tcp_accelerate_client_cnwd": 8,
    "tcp_accelerate_server": 1,
    "tcp_accelerate_server_cnwd": 8,
    "mss": 1281,
    "rstnode": 1,
    "rstclient": 1,
    "zero_window_timeout": 1235,
    "syn_rto_base": 2346
}
TCP代理模板编辑
Action：slb.profile.fastl4.edit
请求参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
description	字符串	长度1-191	描述
fin_timeout	整数	1-60	fin超时
timeout	整数	60-100000	空闲超时
reset_timeout	整数	0-31	超时重置
half_close_timeout	整数	0,60-15000	fin等待
retransmit_number	整数	1-16	最大重传
syn_retransmit_number	整数	1-16	最大syn重传
time_wait	整数	0-600000	等待时间，单位为ms
receive_buff	整数	1-2000000000	接收缓冲区
send_buffer	整数	1-2000000000	发送缓冲区
start_win_size	整数	0-65535	接收窗口
nagle	整数	0-1	nagle算法;0禁用，1使能
window_scale	整数	0-14	tcp窗口比例
keep_alive_interval	整数	0,60-12000	keep-alive报文发送间隔，0关闭此功能
keep_alive_retry	整数	0,2-10	keep-alive报文重试次数，0关闭此功能
optts	整数	0-1	tcp时间戳;0禁用，1使能
tcp_accelerate_client	整数	0-1	tcp加速;0禁用，1使能
tcp_accelerate_client_cnwd	整数	1-10	网络冲突初始化窗口
tcp_accelerate_server	整数	0-1	服务器慢路径;0禁用，1使能
tcp_accelerate_server_cnwd	整数	1-10	服务器冲突初始化窗口
mss	整数	0,128-4312	最大分段
rstnode	整数	0-1	服务器rst;0禁用，1使能
rstclient	整数	0-1	客户端rst;0禁用，1使能
zero_window_timeout	整数	0-65535	零窗口超时
syn_rto_base	整数	0,1000-5000	syn重试超时，单位为ms，0关闭此功能

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.fastl4.edit
请求body：
{
    "name": "profile_tcpagent_1",
    "description": "",
    "fin_timeout": 56,
    "timeout": 1202,
    "reset_timeout": 22,
    "half_close_timeout": 68,
    "retransmit_number": 8,
    "syn_retransmit_number": 9,
    "time_wait": 80002,
    "receive_buff": 512003,
    "send_buffer": 512003,
    "start_win_size": 2224,
    "nagle": 1,
    "window_scale": 5,
    "keep_alive_interval": 62,
    "keep_alive_retry": 8,
    "optts": 1,
    "tcp_accelerate_client": 1,
    "tcp_accelerate_client_cnwd": 8,
    "tcp_accelerate_server": 1,
    "tcp_accelerate_server_cnwd": 8,
    "mss": 1281,
    "rstnode": 1,
    "rstclient": 1,
    "zero_window_timeout": 1235,
    "syn_rto_base": 2346
}
TCP代理模板删除
Action：slb.profile.fastl4.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.fastl4.del
请求body：
{
    "name": "profile_tcpagent_1"
}
TCP模板
TCP模板列表
Action：slb.profile.tcp.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.tcp.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
description	字符串	长度1-191	描述
timeout	整数	60-2097000	空闲超时
reset_timeout	整数	0-31	超时重置
start_win_size	整数	0-65535	接收窗口
half_close_timeout	整数	0,60-12000	fin等待
insertcip	整数	0-1	插入客户端ip；0禁用，1使能
generate_isn	整数	0-1	初始序列号；0禁用，1使能
rstnode	整数	0-1	服务器rst；0禁用，1使能
rstclient	整数	0-1	客户端rst；0禁用，1使能
timestamp	整数	0-2	时间戳；0不指定动作，1删除，2重写，3保持
loose_initiation	整数	0-1	非syn新建连接；0禁用，1使能
loose_close	整数	0-1	fin删除连接；0禁用，1使能
time_wait	整数	0-128000	等待时间，单位为ms
响应举例：
[
    {
        "name": "profile_tcp_1",
        "description": "",
        "timeout": 600,
        "reset_timeout": 6,
        "start_win_size": 1024,
        "half_close_timeout": 120,
        "insertcip": 1,
        "generate_isn": 1,
        "rstnode": 1,
        "rstclient": 1,
        "timestamp": 2,
        "loose_initiation": 1,
        "loose_close": 1,
        "time_wait": 1000
    }
]
分区中获取common分区和自己分区的tcp模板列表
Action：slb.profile.tcp.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.tcp.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
description	字符串	长度1-191	描述
timeout	整数	60-2097000	空闲超时
reset_timeout	整数	0-31	超时重置
start_win_size	整数	0-65535	接收窗口
half_close_timeout	整数	0,60-12000	fin等待
insertcip	整数	0-1	插入客户端ip；0禁用，1使能
generate_isn	整数	0-1	初始序列号，0禁用，1使能
rstnode	整数	0-1	服务器rst；0禁用，1使能
rstclient	整数	0-1	客户端rst；0禁用，1使能
timestamp	整数	0-2	时间戳；0不指定动作，1删除，2重写，3保持
loose_initiation	整数	0-1	非syn新建连接；0禁用，1使能
loose_close	整数	0-1	fin删除连接；0禁用，1使能
time_wait	整数	0-128000	等待时间，单位为ms
响应举例：
[
    {
        "name": "partition_profile_tcp_1",
        "description": "",
        "timeout": 600,
        "reset_timeout": 12,
        "start_win_size": 5120,
        "half_close_timeout": 0,
        "insertcip": 1,
        "generate_isn": 1,
        "rstnode": 1,
        "rstclient": 1,
        "timestamp": 1,
        "loose_initiation": 0,
        "loose_close": 0,
        "time_wait": 2000
    }
]
TCP模板获取
Action：slb.profile.tcp.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.tcp.get
请求body：
{
    "name": "profile_tcp_1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
description	字符串	长度1-191	描述
timeout	整数	60-2097000	空闲超时
reset_timeout	整数	0-31	超时重置
start_win_size	整数	0-65535	接收窗口
half_close_timeout	整数	0,60-12000	fin等待
insertcip	整数	0-1	插入客户端ip；0禁用，1使能
generate_isn	整数	0-1	初始序列号，0禁用，1使能
rstnode	整数	0-1	服务器rst；0禁用，1使能
rstclient	整数	0-1	客户端rst；0禁用，1使能
timestamp	整数	0-2	时间戳；0不指定动作，1删除，2重写，3保持
loose_initiation	整数	0-1	非syn新建连接；0禁用，1使能
loose_close	整数	0-1	fin删除连接；0禁用，1使能
time_wait	整数	0-128000	等待时间，单位为ms

响应举例：
{
    "name": "profile_tcp_2",
    "description": "",
    "timeout": 125,
    "reset_timeout": 25,
    "start_win_size": 34,
    "half_close_timeout": 68,
    "insertcip": 1,
    "generate_isn": 1,
    "rstnode": 1,
    "rstclient": 1,
    "timestamp": 3,
    "loose_initiation": 0,
    "loose_close": 1,
    "time_wait": 78
}
TCP模板增加
Action：slb.profile.tcp.add
请求参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
description	字符串	长度1-191	描述
timeout	整数	60-2097000	空闲超时
reset_timeout	整数	0-31	超时重置
start_win_size	整数	0-65535	接收窗口
half_close_timeout	整数	0,60-12000	fin等待
insertcip	整数	0-1	插入客户端ip；0禁用，1使能
generate_isn	整数	0-1	初始序列号，0禁用，1使能
rstnode	整数	0-1	服务器rst；0禁用，1使能
rstclient	整数	0-1	客户端rst；0禁用，1使能
timestamp	整数	0-2	时间戳；0不指定动作，1删除，2重写，3保持
loose_initiation	整数	0-1	非syn新建连接；0禁用，1使能
loose_close	整数	0-1	fin删除连接；0禁用，1使能
time_wait	整数	0-128000	等待时间，单位为ms
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.tcp.add
请求body：
{
    "name": "profile_tcp_1",
    "description": "",
    "timeout": 126,
    "reset_timeout": 26,
    "start_win_size": 33,
    "half_close_timeout": 90,
    "insertcip": 1,
    "generate_isn": 1,
    "rstnode": 1,
    "rstclient": 1,
    "timestamp": 1,
    "loose_initiation": 1,
    "loose_close": 1,
    "time_wait": 900
}
TCP模板编辑
Action：slb.profile.tcp.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	
timeout	整数	60-2097000	空闲超时	否	缺省值:不修改
reset_timeout	整数	0-31	超时重置	否	缺省值:不修改
half_close_timeout	整数	0,60-12000	fin等待	否	缺省值:不修改
insertcip	整数	0-1	插入客户端ip	否	1使能，0禁用，缺省值:不修改
rstnode	整数	0-1	服务器rst	否	1使能，0禁用，缺省值:不修改
rstclient	整数	0-1	客户端rst	否	1使能，0禁用，缺省值:不修改
start_win_size	整数	0-65535	接收窗口	否	缺省值:不修改
time_wait	整数	0-128000	等待时间，单位为ms	否	默认0
timestamp
	整数	0-3	时间戳	否	默认 0 删除 1 重写 2 保持3
loose_initiation
	整数	0,1	非syn新建连接	否	默认 0 使能 1 禁用0
loose_close
	整数	0,1	fin删除连接	否	默认 0 使能 1 禁用0
description	字符串
	长度1-191	描述	否	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.tcp.edit
请求body：
{
    "name": "profile_tcp_1",
    "description": "pro_tcp_1",
    "timeout": 127,
    "reset_timeout": 27,
    "start_win_size": 34,
    "half_close_timeout": 120,
    "insertcip": 0,
    "generate_isn": 0,
    "rstnode": 0,
    "rstclient": 0,
    "timestamp": 2,
    "loose_initiation": 0,
    "loose_close": 0,
    "time_wait": 1200
}
TCP模板删除
Action：slb.profile.tcp.del
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
请求参数：




请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.tcp.del
请求body：
{
    "name": "profile_tcp_5"
}
UDP模板
UDP模板列表
Action：slb.profile.udp.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.udp.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
description	字符串	长度1-191	描述
timeout	整数	60-100000	空闲超时
aging	字符串	长度1-63	快速老化选项：fast立即老化，delayed延迟老化
空表示不快速老化
delayed_timeout	整数	1-31	快速老化超时:只有在aging 参数为delayed时生效
node_reselect	整数	0-1	服务器重选；1使能，0禁用
响应举例:
[
    {
   	 "name": "profile-udp-1",
    	"description": "udp_profile",
    	"timeout": 120,
    	"aging": "delayed",
    	"delayed_timeout": 31,
     	"node_reselect": 0
}
]
分区中获取common分区的udp模板列表
Action：slb.profile.udp.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.udp.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
timeout	整数	60-100000	空闲超时
description	字符串	长度1-191	描述
aging	字符串	长度1-63	快速老化选项：fast立即老化，delayed延迟老化
空表示不快速老化
delayed_timeout	整数	1-31	快速老化超时:只有在aging 参数为delayed时生效
node_reselect	整数	0-1	服务器重选；1使能，0禁用
响应举例:
[
    {
        "name": "net_udp_profile",
        "description": "",
        "timeout": 120,
        "aging": "",
        "delayed_timeout": 0,
        "node_reselect": 0
    },
    {
        "name": "common/profile-udp-1",
        "description": "udp_profile",
        "timeout": 120,
        "aging": "delayed",
        "delayed_timeout": 31,
        "node_reselect": 0
    } 
]

UDP模板获取
Action：slb.profile.udp.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.udp.get
请求body：
{
    "name": "profile-udp-1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
timeout	整数	60-100000	空闲超时
description	字符串	长度1-191	描述
aging	字符串	长度1-63	快速老化选项：fast立即老化，delayed延迟老化
空表示不快速老化
delayed_timeout	整数	1-31	快速老化超时:只有在aging 参数为delayed时生效
node_reselect	整数	0-1	服务器重选；1使能，0禁用

响应举例:
{
    "name": "profile-udp-1",
    "description": "udp_profile",
    "timeout": 120,
    "aging": "delayed",
    "delayed_timeout": 31,
    "node_reselect": 0

}
UDP模板增加
Action：slb.profile.udp.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	
timeout	整数	60-100000	空闲超时	否	缺省值:120
description	字符串	长度1-191	描述	否	
aging	字符串	长度1-63	快速老化选项	否	fast立即老化，delayed延迟老化，
空表示不快速老化
缺省值:空
delayed_timeout	整数	1-31	快速老化超时:	否	只有在aging 参数为delayed时生效
缺省值:空
node_reselect	整数	0-1	服务器重选	否	0禁用，1使能，缺省值:0

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.udp.add
请求body：
{
 	"name": "profile-udp-1",
    	"description": "udp_profile",
    	"timeout": 120,
    	"aging": "delayed",
    	"delayed_timeout": 31,
     	"node_reselect": 0
}
UDP模板编辑
Action：slb.profile.udp.edit
请求参数：
name	字符串	长度1-191	模版名称	是	
timeout	整数	60-100000	空闲超时	否	缺省值:120
description	字符串	长度1-191	描述	否	
aging	字符串	长度1-63	快速老化选项	否	fast立即老化，delayed延迟老化，
空表示不快速老化
缺省值:空
delayed_timeout	整数	1-31	快速老化超时:	否	只有在aging 参数为delayed时生效
缺省值:空
node_reselect	整数	0-1	服务器重选	否	0禁用，1使能，缺省值:0

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.udp.edit
请求body：
{
 	"name": "profile-udp-1",
    	"description": "udp_profile",
    	"timeout": 120,
    	"aging": "delayed",
    	"delayed_timeout": 31,
     	"node_reselect": 0
}
UDP模板删除
Action：slb.profile.udp.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.udp.del
请求body：
{
    "name": "profile-udp-1"
}



HTTP模板
HTTP模板列表
Action: slb.profile.http.list
请求参数:无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
fallback_url	字符串	长度1-127	回退url
force_reselect	整数	0-1	强制重选；1:是;0:否
clientip_insert	字符串	长度1-63	插入客户端IP头名称,空表示不插入
clientip_insert_replace	整数	0-1	替换插入客户端IP头；1:是;0:否
retry_503	整数	0-3	http被动健康检查收到5xx次数
websocket	整数	0，1	websocket按开关
cookie_encrypt_name	字符串	1-63	Cookie加密的名称
cookie_encrypt_password	字符串	1-63	Cookie加密密码
req_header_del	数组	不涉及	请求头删除列表,由多个请求头部名称组成
rsp_header_del	数组	不涉及	响应头删除列表,由多个响应头部名称组成
req_header_insert	数组	不涉及	请求头插入数组：
req_header_insert > value:
类型：字符串，
范围：长度1-63，
含义：插入请求头,key:value格式
req_header_insert > type:
类型：整数，
范围：0-2
含义：插入模式:0:替换;1:强制;2:尝试
rsp_header_insert	数组	不涉及	响应头插入数组：
rsp_header_insert > value:
类型：字符串，
范围：长度1-63，
含义：插入响应求头,key:value格式
rsp_header_insert > type:
类型：整数，
范围：0-2
含义：插入模式:0:替换;1:强制;2:尝试
url_class	数组	不涉及	http-url分类数组--http-url分类和host分类只能选一种
url_class > url:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配url
url_class > pool:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配后发送到服务池名称
url_class > type:
类型：整数；
范围：0-3，
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
url_class > action：
类型：整数，
范围：1或32，
含义：url匹配后行为：1：指定到服务池；2：url限速
url_class > limitaction：
类型：整数，
范围：2，4，8，16，
含义：url限速的操作：2：本地文件；4：重定向；8：丢弃：16：重置
url_class > ruletable：
类型：字符串，
范围：不涉及
含义：已有规则表，url限速的源ip匹配规则表id，使限速生效
url_class > ruletableid：
类型：整数，
范围：0-30，
含义：规则表id
url_class > reqrps： 
类型：整数，
范围：0-8000000，
含义：Max-rps
url_class > path_or_url： 
类型：字符串，
范围：1-63，
含义：本地文件或重定向可以配置
host_class	数组	不涉及	host_class > pool:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配后发送到服务池名称
host_class > type:
类型：整数；
范围：0-3，
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
host_class > host:
类型：字符串，
范围：1-63，
含义:http-host分类--配匹host
url_hash	整数	0-2	URL哈希; 0:禁用;1:头部HASH；尾部HASH 
url_hash_len	整数	4-128	url哈希字节长度
url_hash_offset	整数	0-255	url哈希偏移量
redirect_modify	数组	不涉及	URL重定向动作列表
redirect_modify > match：
类型：字符串，
范围：1-63，	
含义：重定向--匹配URL
redirect_modify > to：
类型：字符串，
范围：1-63，
含义:重定向--重定向目标
redirect_modify_https	整数	0-1	重定向更改https;1:启用；0:禁用
redirect_modify_https_port	整数	1-65535	重定向更改https到端口
compress	整数	0-1	压缩1:启用；0:禁用
compress_keep_header	整数	0-1	压缩时保持accept头部
compress_level	整数	1-9	压缩级别;1:最快;5:标准;9:最好;
compress_min_len	整数	0-2147483647	最小内容长度
compress_content_type	数组	不涉及	包含内容，字符串，长度1-31，最大10条
compress_content_type_exclude	数组	不涉及	排除内容，字符串，长度1-31，最大10条
compress_url_exclude	数组	不涉及	排除url，字符串，长度1-31，最大10条
description	字符串
	长度1-191	描述
client-cert-code	数组	不涉及	证书错误码显示，详细参数如下：
client-cert-code > errno:
        类型：数组
含义：错误码，
证书范围0-79、901-906（但不包含902）、other 
client-cert-code > localpage：
含义：本地页面，
类型：整数，
范围：0-63
req_header_insert_cert	数组	不涉及	插入证书到请求头处，详细参数如下:
req_header_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_header_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称
req_url_insert_cert	数组	不涉及	插入证书到url中，详细参数如下:
req_url_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_url_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称
req_cookie_insert_cert	数组	不涉及	插入证书到请求头cookie中，详细参数如下:

req_cookie_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_cookie_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称
cookie_select	整数	0，1	cookie自定义保持过期类型，1，.过期时间，0，会话cookie
cookie_expire	整数	1-30000000	cookie自定义保持过期时间
cookie_expire_enable	整数	0，1	cookie自定义保持开关
chunking_request	整数	0，1	请求chunked编码开关
chunking_response	整数	0，1	响应chunked编码开关
websocket	整数	0，1	websocket按开关
node_select_fail_response_504	整数	0，1	算法失败响应504开关，1为开启，0为关闭
响应举例：
[
    {
        "name": "http",
        "description": "",
        "fallback_url": "",
        "force_reselect": 0,
        "clientip_insert": "",
        "clientip_insert_replace": 0,
        "retry_503": 0,
        "websocket": 0,
        "node_select_fail_response_504": 1,
        "cookie_encrypt_name": "",
        "cookie_encrypt_password": "********",
        "req_header_del": [],
        "rsp_header_del": [],
        "req_header_insert_cert": [
            {
                "type": 0,
                "value": "key"
            }
        ],
        "req_url_insert_cert": [
            {
                "type": 5,
                "value": "cert"
            }
        ],
        "req_cookie_insert_cert": [
            {
                "type": 6,
                "value": "csr"
            }
        ],
        "client_cert_code": [
            {
                "errno": "903",
                "localpage": "/index.html"
            }
        ],
        "req_header_insert": [],
        "rsp_header_insert": [],
        "url_class_log_interval": 0,
        "url_hash": 0,
        "url_hash_len": 0,
        "url_hash_offset": 0,
        "redirect_modify": [],
        "redirect_modify_https": 0,
        "redirect_modify_https_port": 0,
        "cookie_select": 0,
        "cookie_expire": 0,
        "cookie_expire_enable": 0,
        "compress": 0,
        "compress_keep_header": 0,
        "compress_level": 1,
        "compress_min_len": 0,
        "chunking_request": 0,
        "chunking_response": 0,
        "compress_content_type": [],
        "compress_content_type_exclude": [],
        "compress_url_exclude": []
    }
]

分区中获取common分区和自己分区的http模板列表
Action: slb.profile.http.list.withcommon
请求参数:无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http.list.withcommon
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
fallback_url	字符串	长度1-127	回退url
force_reselect	整数	0-1	强制重选；1:是;0:否
clientip_insert	字符串	长度1-63	插入客户端IP头名称,空表示不插入
clientip_insert_replace	整数	0-1	替换插入客户端IP头；1:是;0:否
retry_503	整数	0-3	http被动健康检查收到5xx次数
req_header_del	数组	不涉及	请求头删除列表,由多个请求头部名称组成
rsp_header_del	数组	不涉及	响应头删除列表,由多个响应头部名称组成
websocket	整数	0，1	websocket按开关
cookie_encrypt_name	字符串	1-63	cookie加密的名称
cookie_encrypt_password	字符串	1-63	cookie加密密码
req_header_insert	数组	不涉及	请求头插入数组
value	字符串	长度1-63	插入请求头,key:value格式
type	整数	0-2	插入模式:0:替换;1:强制;2:尝试;
rsp_header_insert	数组	不涉及	响应头插入数组
value	字符串	长度1-63	插入响应头,key:value格式
type	整数	0-2	插入模式:0:替换;1:强制;2:尝试;
url_class	数组	不涉及	http-url分类数组--http-url分类和host分类只能选一种
详细参数见以下数组：
url_class > url:
含义：http-url分类--匹配url
范围：1-63
类型：字符串
url_class > pool:
含义：http-url分类--匹配后发送到服务池名称
范围：1-63
类型：字符串
url_class > type:
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
范围：0-3
类型：数组
url_class > action:
含义：url匹配后行为：1：指定到服务池；2：url限速
范围：1或32
类型：整数

limitaction	整数	2，4，8，16	url限速的操作：2：本地文件；4：重定向；8：丢弃：16：重置；
ruletable	字符串	已有规则表	url限速的源ip匹配规则表id，使限速生效
ruletableid	整数	0-30	规则表的id
reqrps	整数	0-8000000	Max-rps
path_or_url	字符串	长度1-63	本地文件或重定向可以配置
host_class	数组	不涉及	http-host分类数组--http-url分类和host分类只能选一种
host	字符串	长度1-63	http-host分类--配匹host
pool	字符串	长度1-63	http-host分类--匹配后发送到服务池名称
type	整数	0-2	http-host分类--匹配方法:0:包含;1:头;2:尾;
url_hash	整数	0-2	URL哈希; 0:禁用;1:头部HASH；尾部HASH 
url_hash_len	整数	4-128	url哈希字节长度
url_hash_offset	整数	0-255	url哈希偏移量
redirect_modify	数组	不涉及	重URL定向动作列表
match	字符串	长度1-63	重定向--匹配URL
to	字符串	长度1-63	重定向--重定向目标
redirect_modify_https	整数	0-1	重定向更改https;1:启用；0:禁用
redirect_modify_https_port	整数	1-65535	重定向更改https到端口
compress	整数	0-1	压缩1:启用；0:禁用
compress_keep_header	整数	0-1	压缩时保持accept头部
compress_level	整数	1-9	压缩级别;1:最快;5:标准;9:最好;
compress_min_len	整数	0-2147483647	最小内容长度
compress_content_type	数组	1-31	包含内容
compress_content_type_exclude	数组	1-31	排除内容
compress_url_exclude	数组	1-31	排除uri
client-cert-code	字符串	不涉及	证书错误码显示
req_header_insert_cert	字符串	不涉及	插入指定证书字段到请求头中的header字段中
req_url_insert_cert	字符串	不涉及	插入指定证书字段到请求头中的url中
req_cookie_insert_cert	字符串	不涉及	插入证书字段到请求头的cookie中
响应举例：
[
	{
        "name": "http_test1",
        "fallback_url": "",
        "force_reselect": 0,
        "clientip_insert": "",
        "clientip_insert_replace": 0,
        "retry_503": 0,
        "websocket": 0,
        "node_select_fail_response_504": 1,
        "cookie_encrypt_name": "",
        "cookie_encrypt_password": "",
        "connlimit_action": {
            "action": 0,
            "path_or_url": ""
        },
        "req_header_del": [],
        "rsp_header_del": [],
        "req_header_insert": [],
        "rsp_header_insert": [],
        "url_class_log_interval": 0,
        "url_class": [
            {
                "url": "url",
                "pool": "pool_1",
                "type": 0,
                "action": 1
            }
        ],
        "url_hash": 0,
        "url_hash_len": 0,
        "url_hash_offset": 0,
        "redirect_modify": [],
        "redirect_modify_https": 0,
        "redirect_modify_https_port": 0,
        "cookie_select": 0,
        "cookie_expire": 0,
        "cookie_expire_enable": 0,
        "compress": 0,
        "compress_keep_header": 0,
        "compress_level": 1,
        "compress_min_len": 128,
        "chunking_request": 0,
        "chunking_response": 0,
        "compress_content_type": [],
        "compress_content_type_exclude": [],
        "compress_url_exclude": []
    },
    {
        "name": "common/http_test2",
        "fallback_url": "",
        "fallback_page": "",
        "force_reselect": 0,
        "clientip_insert": "X-Forwarded-For",
        "clientip_insert_replace": 0,
        "retry_503": 0,
        "websocket": 0,
        "cookie_encrypt_name": "",
        "cookie_encrypt_password": "********",
        "response_code_actions": [],
        "req_header_del": [],
        "rsp_header_del": [],
        "req_header_insert": [],
        "rsp_header_insert": [],
        "url_class_log_interval": 0,
        "url_hash": 0,
        "url_hash_len": 0,
        "url_hash_offset": 0,
        "redirect_modify": [],
        "redirect_modify_https": 0,
        "redirect_modify_https_port": 0,
        "cookie_select": 0,
        "cookie_expire": 0,
        "cookie_expire_enable": 0,
        "compress": 0,
        "compress_keep_header": 0,
        "compress_level": 1,
        "compress_min_len": 128,
        "chunking_request": 0,
        "chunking_response": 0,
        "compress_content_type": [],
        "compress_content_type_exclude": [],
        "compress_url_exclude": []
    }
]
HTTP模板获取
Action: slb.profile.http.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http.get
请求Body:
{
    "name": "profile_http_1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
fallback_url	字符串	长度1-127	回退url
force_reselect	整数	0-1	强制重选；1:是;0:否
clientip_insert	字符串	长度1-63	插入客户端IP头名称,空表示不插入
clientip_insert_replace	整数	0-1	替换插入客户端IP头；1:是;0:否
retry_503	整数	0-3	http被动健康检查收到5xx次数
req_header_del	数组	不涉及	请求头删除列表,由多个请求头部名称组成
rsp_header_del	数组	不涉及	响应头删除列表,由多个响应头部名称组成
req_header_insert	数组	不涉及	请求头插入数组：
req_header_insert > value:
类型：字符串，
范围：长度1-63，
含义：插入请求头,key:value格式
req_header_insert > type:
类型：整数，
范围：0-2
含义：插入模式:0:替换;1:强制;2:尝试
rsp_header_insert	数组	不涉及	响应头插入数组：
rsp_header_insert > value:
类型：字符串，
范围：长度1-63，
含义：插入响应求头,key:value格式
rsp_header_insert > type:
类型：整数，
范围：0-2
含义：插入模式:0:替换;1:强制;2:尝试
url_class	数组	不涉及	http-url分类数组--http-url分类和host分类只能选一种
url_class > url:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配url
url_class > pool:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配后发送到服务池名称
url_class > type:
类型：整数；
范围：0-3，
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
url_class > action：
类型：整数，
范围：1或32，
含义：url匹配后行为：1：指定到服务池；2：url限速
url_class > limitaction：
类型：整数，
范围：2，4，8，16，
含义：url限速的操作：2：本地文件；4：重定向；8：丢弃：16：重置
url_class > ruletable：
类型：字符串，
范围：不涉及
含义：已有规则表，url限速的源ip匹配规则表id，使限速生效
url_class > ruletableid：
类型：整数，
范围：0-30，
含义：规则表id
url_class > reqrps： 
类型：整数，
范围：0-8000000，
含义：Max-rps
url_class > path_or_url： 
类型：字符串，
范围：1-63，
含义：本地文件或重定向可以配置
host_class	数组	不涉及	host_class > pool:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配后发送到服务池名称
host_class > type:
类型：整数；
范围：0-3，
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
host_class > host:
类型：字符串，
范围：1-63，
含义:http-host分类--配匹host
url_hash	整数	0-2	url哈希; 0:禁用;1:头部HASH；尾部HASH 
url_hash_len	整数	4-128	url哈希字节长度
url_hash_offset	整数	0-255	url哈希偏移量
redirect_modify	数组	不涉及	URL重定向动作列表
match：字符串，长度1-63，	重定向--匹配URL
to：字符串，长度1-63，重定向--重定向目标
redirect_modify_https	整数	0-1	重定向更改https;1:启用；0:禁用
redirect_modify_https_port	整数	1-65535	重定向更改https到端口
compress	整数	0-1	压缩1:启用；0:禁用
compress_keep_header	整数	0-1	压缩时保持accept头部
compress_level	整数	1-9	压缩级别;1:最快;5:标准;9:最好;
compress_min_len	整数	0-2147483647	最小内容长度
compress_content_type	数组	不涉及	包含内容，字符串，长度1-31，最大10条
compress_content_type_exclude	数组	不涉及	排除内容，字符串，长度1-31，最大10条
compress_url_exclude	数组	不涉及	排除url，字符串，长度1-31，最大10条
cookie_encrypt_name	字符串	1-63	Cookie加密的名称
cookie_encrypt_password	字符串	1-63	Cookie加密密码
description	字符串
	长度1-191	描述
client-cert-code	数组	不涉及	证书错误码显示，详细参数如下：
client-cert-code > errno:
        类型：数组
含义：错误码，
证书范围0-79、901-906（但不包含902）、other 
client-cert-code > localpage：
含义：本地页面，
类型：整数，
范围：0-63
req_header_insert_cert	数组	不涉及	插入证书到请求头处，详细参数如下:
req_header_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_header_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称
req_url_insert_cert	数组	不涉及	插入证书到url中，详细参数如下:
req_url_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_url_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称
req_cookie_insert_cert	数组	不涉及	插入证书到请求头cookie中，详细参数如下:

req_cookie_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_cookie_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称
cookie_select	整数	0，1	cookie自定义保持过期类型，1，.过期时间，0，会话cookie
cookie_expire	整数	1-30000000	cookie自定义保持过期时间
cookie_expire_enable	整数	0，1	cookie自定义保持开关
chunking_request	整数	0，1	请求chunked编码开关
chunking_response	整数	0，1	响应chunked编码开关
websocket	整数	0，1	websocket按开关
node_select_fail_response_504	整数	0，1	算法失败响应504开关，1为开启，0为关闭
响应举例：
{
    "name": "profile_http_1",
    "description": "",
    "fallback_url": "",
    "force_reselect": 0,
    "clientip_insert": "",
    "clientip_insert_replace": 0,
    "retry_503": 0,
    "websocket": 0,
    "node_select_fail_response_504": 1,
    "cookie_encrypt_name": "",
    "cookie_encrypt_password": "********",
    "req_header_del": [],
    "rsp_header_del": [],
    "req_header_insert_cert": [
        {
            "type": 0,
            "value": "key"
        }
    ],
    "req_url_insert_cert": [
        {
            "type": 5,
            "value": "cert"
        }
    ],
    "req_cookie_insert_cert": [
        {
            "type": 6,
            "value": "csr"
        }
    ],
    "client_cert_code": [
        {
            "errno": "903",
            "localpage": "/index.html"
        }
    ],
    "req_header_insert": [],
    "rsp_header_insert": [],
    "url_class_log_interval": 0,
    "url_hash": 0,
    "url_hash_len": 0,
    "url_hash_offset": 0,
    "redirect_modify": [],
    "redirect_modify_https": 0,
    "redirect_modify_https_port": 0,
    "cookie_select": 0,
    "cookie_expire": 0,
    "cookie_expire_enable": 0,
    "compress": 0,
    "compress_keep_header": 0,
    "compress_level": 1,
    "compress_min_len": 0,
    "chunking_request": 0,
    "chunking_response": 0,
    "compress_content_type": [],
    "compress_content_type_exclude": [],
    "compress_url_exclude": []
}
HTTP模板增加
Action: slb.profile.http.add
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
fallback_url	字符串	长度1-127	回退url	否	
force_reselect	整数	0-1	强制重选；1:是;0:否	否	1:是;0:否，缺省值:0
clientip_insert	字符串	长度1-63	插入客户端IP头名称	否	空表示不插入
clientip_insert_replace
	整数	0-1	替换插入客户端IP头；1:是;0:否	否	1:是;0:否，缺省值:0
retry_503	整数	0-3	http被动健康检查收到5xx次数	否	缺省值:0，0表示禁用被动健康检查
req_header_del	数组	长度0-8	请求头删除列表,由多个请求头部名称组成	否	缺省值:空
rsp_header_del	数组	长度0-8	响应头删除列表,由多个响应头部名称组成	否	缺省值:空
req_header_insert	数组	不涉及	请求头插入数组：
req_header_insert > value:
类型：字符串，
范围：长度1-63，
含义：插入请求头,key:value格式
req_header_insert > type:
类型：整数，
范围：0-2
含义：插入模式:0:替换;1:强制;2:尝试	否	缺省值:空
rsp_header_insert	数组	不涉及	响应头插入数组：
rsp_header_insert > value:
类型：字符串，
范围：长度1-63，
含义：插入响应求头,key:value格式
rsp_header_insert > type:
类型：整数，
范围：0-2
含义：插入模式:0:替换;1:强制;2:尝试	否	缺省值:空
url_class	数组	不涉及	http-url分类数组--http-url分类和host分类只能选一种
url_class > url:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配url
url_class > pool:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配后发送到服务池名称
url_class > type:
类型：整数；
范围：0-3，
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
url_class > action：
类型：整数，
范围：1或32，
含义：url匹配后行为：1：指定到服务池；2：url限速
url_class > limitaction：
类型：整数，
范围：2，4，8，16，
含义：url限速的操作：2：本地文件；4：重定向；8：丢弃：16：重置
url_class > ruletable：
类型：字符串，
范围：不涉及
含义：已有规则表，url限速的源ip匹配规则表id，使限速生效
url_class > ruletableid：
类型：整数，
范围：0-30，
含义：规则表id
url_class > reqrps： 
类型：整数，
范围：0-8000000，
含义：Max-rps
url_class > path_or_url： 
类型：字符串，
范围：1-63，
含义：本地文件或重定向可以配置	是	缺省值:空
host_class	数组	不涉及	host_class > pool:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配后发送到服务池名称
host_class > type:
类型：整数；
范围：0-3，
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
host_class > host:
类型：字符串，
范围：1-63，
含义:http-host分类--配匹host	否	缺省值:空
url_hash	整数	0-2	URL哈希; 0:禁用;1:头部HASH；尾部HASH 	否	0:禁用;1:头部HASH；尾部HASH 
缺省值:0
url_hash_len	整数	4-128	url哈希字节长度	否	缺省值:0
url_hash_offset	整数	0-255	url哈希偏移量	否	缺省值:0
redirect_modify	数组		URL重定向动作列表
match：字符串，长度1-63，	重定向--匹配URL
to：字符串，长度1-63，重定向--重定向目标	否	缺省值:空
redirect_modify_https	整数	0-1	重定向更改https;1:启用；0:禁用	否	1:启用；0:禁用；缺省值:0
redirect_modify_https_port	整数	1-65535	重定向更改https到端口	否	缺省值:0
compress	整数	0-1	压缩1:启用；0:禁用	否	缺省值:0
compress_keep_header	整数	0-1	压缩时保持accept头部	否	缺省值:0
compress_level	整数	1-9	压缩级别;1:最快;5:标准;9:最好;	否	1:最快;5:标准;9:最好;缺省值:1
compress_min_len	整数	0-2147483647	最小内容长度	否	缺省值:0
compress_content_type	数组	不涉及	包含内容，字符串，长度1-31，最大10条	否	缺省值:空
compress_content_type_exclude	数组	不涉及	排除内容，字符串，长度1-31，最大10条	否	缺省值:空
compress_url_exclude	数组	不涉及	排除url，字符串，长度1-31，最大10条	否	缺省值:空
cookie_encrypt_name	字符串	1-63	cookie加密的名称	否	缺省值:空
cookie_encrypt_password	字符串	1-63	cookie加密密码	否	缺省值:空
description	字符串
	长度1-191	描述	否	
client-cert-code	数组	不涉及	证书错误码显示，详细参数如下：
client-cert-code > errno:
        类型：数组
含义：错误码，
证书范围0-79、901-906（但不包含902）、other 
client-cert-code > localpage：
含义：本地页面，
类型：整数，
范围：0-63	否	缺省值:空
req_header_insert_cert	数组	不涉及	插入证书到请求头处，详细参数如下:
req_header_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_header_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称	否	缺省值:空
req_url_insert_cert	数组	不涉及	插入证书到url中，详细参数如下:
req_url_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_url_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称	否	缺省值:空
req_cookie_insert_cert	数组	不涉及	插入证书到请求头cookie中，详细参数如下:

req_cookie_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_cookie_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称	否	缺省值:空
cookie_select	整数	0，1	cookie自定义保持过期类型，1，.过期时间，0，会话cookie	否	缺省值:空
cookie_expire	整数	1-30000000	cookie自定义保持过期时间	否	缺省值:空
cookie_expire_enable	整数	0，1	cookie自定义保持开关	否	缺省值:空
chunking_request	整数	0，1	请求chunked编码开关	否	缺省值:空
chunking_response	整数	0，1	响应chunked编码开关	否	缺省值:空
websocket	整数	0，1	websocket按开关	否	缺省值:空
node_select_fail_response_504	整数	0，1	算法失败响应504开关，1为开启，0为关闭	否	缺省值:0
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http.add
请求body：
{
    "name": "profile_http_1",
    "description": "",
    "fallback_url": "",
    "force_reselect": 0,
    "clientip_insert": "",
    "clientip_insert_replace": 0,
    "retry_503": 0,
    "websocket": 0,
    "node_select_fail_response_504": 1,
    "cookie_encrypt_name": "",
    "cookie_encrypt_password": "123456",
    "req_header_del": [],
    "rsp_header_del": [],
    "req_header_insert_cert": [
        {
            "type":0,
            "value":"key"
        }
    ],
    "req_url_insert_cert": [
        {
            "type": 5,
            "value": "cert"
        }
    ],
    "req_cookie_insert_cert": [
        {
            "type": 6,
            "value": "csr"
        }
    ],
    "client_cert_code": [
        {
            "errno": "903",
            "localpage": "/index.html"
        }
    ],
    "req_header_insert": [],
    "rsp_header_insert": [],
    "url_class_log_interval": 0,
    "url_hash": 0,
    "url_hash_len": 0,
    "url_hash_offset": 0,
    "redirect_modify": [],
    "redirect_modify_https": 0,
    "redirect_modify_https_port": 0,
    "cookie_select": 0,
    "cookie_expire": 0,
    "cookie_expire_enable": 0,
    "compress": 0,
    "compress_keep_header": 0,
    "compress_level": 1,
    "compress_min_len": 0,
    "chunking_request": 0,
    "chunking_response": 0,
    "compress_content_type": [],
    "compress_content_type_exclude": [],
    "compress_url_exclude": []
}
HTTP模板编辑
Action: slb.profile.http.edit
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
fallback_url	字符串	长度1-127	回退url	否	
force_reselect	整数	0-1	强制重选；1:是;0:否	否	1:是;0:否，缺省值:0
clientip_insert	字符串	长度1-63	插入客户端IP头名称	否	空表示不插入
clientip_insert_replace
	整数	0-1	替换插入客户端IP头；1:是;0:否	否	1:是;0:否，缺省值:0
retry_503	整数	0-3	http被动健康检查收到5xx次数	否	缺省值:0，0表示禁用被动健康检查
req_header_del	数组	长度0-8	请求头删除列表,由多个请求头部名称组成	否	缺省值:空
rsp_header_del	数组	长度0-8	响应头删除列表,由多个响应头部名称组成	否	缺省值:空
req_header_insert	数组	不涉及	请求头插入数组：
req_header_insert > value:
类型：字符串，
范围：长度1-63，
含义：插入请求头,key:value格式
req_header_insert > type:
类型：整数，
范围：0-2
含义：插入模式:0:替换;1:强制;2:尝试	否	缺省值:空
rsp_header_insert	数组	不涉及	响应头插入数组：
rsp_header_insert > value:
类型：字符串，
范围：长度1-63，
含义：插入响应求头,key:value格式
rsp_header_insert > type:
类型：整数，
范围：0-2
含义：插入模式:0:替换;1:强制;2:尝试	否	缺省值:空
url_class	数组	不涉及	http-url分类数组--http-url分类和host分类只能选一种
url_class > url:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配url
url_class > pool:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配后发送到服务池名称
url_class > type:
类型：整数；
范围：0-3，
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
url_class > action：
类型：整数，
范围：1或32，
含义：url匹配后行为：1：指定到服务池；2：url限速
url_class > limitaction：
类型：整数，
范围：2，4，8，16，
含义：url限速的操作：2：本地文件；4：重定向；8：丢弃：16：重置
url_class > ruletable：
类型：字符串，
范围：不涉及
含义：已有规则表，url限速的源ip匹配规则表id，使限速生效
url_class > ruletableid：
类型：整数，
范围：0-30，
含义：规则表id
url_class > reqrps： 
类型：整数，
范围：0-8000000，
含义：Max-rps
url_class > path_or_url： 
类型：字符串，
范围：1-63，
含义：本地文件或重定向可以配置	是	缺省值:空
host_class	数组	不涉及	host_class > pool:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配后发送到服务池名称
host_class > type:
类型：整数；
范围：0-3，
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
host_class > host:
类型：字符串，
范围：1-63，
含义:http-host分类--配匹host	否	缺省值:空
url_hash	整数	0-2	URL哈希; 0:禁用;1:头部HASH；尾部HASH 	否	0:禁用;1:头部HASH；尾部HASH 
缺省值:0
url_hash_len	整数	4-128	url哈希字节长度	否	缺省值:0
url_hash_offset	整数	0-255	url哈希偏移量	否	缺省值:0
redirect_modify	数组		URL重定向动作列表
match：字符串，长度1-63，	重定向--匹配URL
to：字符串，长度1-63，重定向--重定向目标	否	缺省值:空
redirect_modify_https	整数	0-1	重定向更改https;1:启用；0:禁用	否	1:启用；0:禁用；缺省值:0
redirect_modify_https_port	整数	1-65535	重定向更改https到端口	否	缺省值:0
compress	整数	0-1	压缩1:启用；0:禁用	否	缺省值:0
compress_keep_header	整数	0-1	压缩时保持accept头部	否	缺省值:0
compress_level	整数	1-9	压缩级别;1:最快;5:标准;9:最好;	否	1:最快;5:标准;9:最好;缺省值:1
compress_min_len	整数	0-2147483647	最小内容长度	否	缺省值:0
compress_content_type	数组	不涉及	包含内容，字符串，长度1-31，最大10条	否	缺省值:空
compress_content_type_exclude	数组	不涉及	排除内容，字符串，长度1-31，最大10条	否	缺省值:空
compress_url_exclude	数组	不涉及	排除url，字符串，长度1-31，最大10条	否	缺省值:空
cookie_encrypt_name	字符串	1-63	cookie加密的名称	否	缺省值:空
cookie_encrypt_password	字符串	1-63	cookie加密密码	否	缺省值:空
description	字符串
	长度1-191	描述	否	
client-cert-code	数组	不涉及	证书错误码显示，详细参数如下：
client-cert-code > errno:
        类型：数组
含义：错误码，
证书范围0-79、901-906（但不包含902）、other 
client-cert-code > localpage：
含义：本地页面，
类型：整数，
范围：0-63	否	缺省值:空
req_header_insert_cert	数组	不涉及	插入证书到请求头处，详细参数如下:
req_header_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_header_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称	否	缺省值:空
req_url_insert_cert	数组	不涉及	插入证书到url中，详细参数如下:
req_url_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_url_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称	否	缺省值:空
req_cookie_insert_cert	数组	不涉及	插入证书到请求头cookie中，详细参数如下:

req_cookie_insert_cert > type：
类型：整数，
范围：0-11，
含义：指定证书的内容，其中各参数的含义为：
（0:all;1:dn;2:issuer;3:sn;4:hash;5:subject;6:vaildity;7:notbefore;8:notafter;9:commonname;10:publickey;11:rdn）
req_cookie_insert_cert > value ：
类型：字符串，
范围：1-63
含义：请求头名称	否	缺省值:空
cookie_select	整数	0，1	cookie自定义保持过期类型，1，.过期时间，0，会话cookie	否	缺省值:空
cookie_expire	整数	1-30000000	cookie自定义保持过期时间	否	缺省值:空
cookie_expire_enable	整数	0，1	cookie自定义保持开关	否	缺省值:空
chunking_request	整数	0，1	请求chunked编码开关	否	缺省值:空
chunking_response	整数	0，1	响应chunked编码开关	否	缺省值:空
websocket	整数	0，1	websocket按开关	否	缺省值:空
node_select_fail_response_504	整数	0，1	算法失败响应504开关，1为开启，0为关闭	否	缺省值:0

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http.add
请求body：
{
    "name": "profile_http_1",
    "description": "123456789",
    "fallback_url": "",
    "force_reselect": 0,
    "clientip_insert": "",
    "clientip_insert_replace": 0,
    "retry_503": 0,
    "websocket": 0,
    "node_select_fail_response_504": 1,
    "cookie_encrypt_name": "",
    "cookie_encrypt_password": "123456",
    "req_header_del": [],
    "rsp_header_del": [],
    "req_header_insert_cert": [
        {
            "type":0,
            "value":"key"
        }
    ],
    "req_url_insert_cert": [
        {
            "type": 5,
            "value": "cert"
        }
    ],
    "req_cookie_insert_cert": [
        {
            "type": 6,
            "value": "csr"
        }
    ],
    "client_cert_code": [
        {
            "errno": "903",
            "localpage": "/index.html"
        }
    ],
    "req_header_insert": [],
    "rsp_header_insert": [],
    "url_class_log_interval": 0,
    "url_hash": 0,
    "url_hash_len": 0,
    "url_hash_offset": 0,
    "redirect_modify": [],
    "redirect_modify_https": 0,
    "redirect_modify_https_port": 0,
    "cookie_select": 0,
    "cookie_expire": 0,
    "cookie_expire_enable": 0,
    "compress": 0,
    "compress_keep_header": 0,
    "compress_level": 1,
    "compress_min_len": 0,
    "chunking_request": 0,
    "chunking_response": 0,
    "compress_content_type": [],
    "compress_content_type_exclude": [],
    "compress_url_exclude": []
}

HTTP模板删除
Action: slb.profile.http.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
请求举例:
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http.del
请求body：
{
    "name": "profile_http_1"
}
HTTP模板增加主机动作配置
Action: slb.profile.http.hostswitch.add
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
host_class	数组	不涉及	http模板头操作
由以下数组组成：
host_class > pool:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配后发送到服务池名称
host_class > type:
类型：整数；
范围：0-3，
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
host_class > host:
类型：字符串，
范围：1-63，
含义:http-host分类--配匹host	否	缺省值:空
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http.hostswitch.add
请求body：
{
"name": "profile_http_1",
"host_class": [
{
  "host": "adc",
  "pool": "pool_tcp",
  "type": 0
},
{
  "host": "adc_1",
  "pool": "pool_tcp",
  "type": 1
},
{
  "host": "adc_2",
  "pool": "pool_tcp",
  "type": 2
}
]
}
HTTP模板删除主机动作配置
Action: slb.profile.http.hostswitch.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
host_class	数组	不涉及	http模板头操作
由以下数组组成：
host_class > pool:
类型：字符串，
范围：1-63，
含义：http-url分类--匹配后发送到服务池名称
host_class > type:
类型：整数；
范围：0-3，
含义：http-url分类--匹配方法:0:包含;1:头;2:尾;3:相同;
host_class > host:
类型：字符串，
范围：1-63，
含义:http-host分类--配匹host	否	缺省值:空
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http.hostswitch.del
请求body：
{
"name": "profile_http_1",
"host_class": [
{
  "host": "adc",
  "pool": "pool_tcp",
  "type": 0
},
{
  "host": "adc_1",
  "pool": "pool_tcp",
  "type": 1
},
{
  "host": "adc_2",
  "pool": "pool_tcp",
  "type": 2
}
]
}

HTTP2模板
HTTP2模板列表
Action：slb.profile.http2.list
请求参数：无
请求举例：
GET：
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http2.list
响应参数
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
Insert_x_header	字符串	长度1-63	插入头内容
description	字符串
	长度1-191	描述
响应举例：
[
    {
        "name": "profile_http2",
        "insert_x_header": "",
       
    }
]


分区中获取common分区和自己分区的http2模板列表

Action：slb.profile.http2.list.withcommon
请求参数：无
请求举例：
GET：
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http2.list.withcommon
响应参数
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
Insert_x_header	字符串	长度1-63	插入头内容
description	字符串
	长度1-191	描述
响应举例：
[
    {
        "name": "p1_http2",
        "insert_x_header": "",
"description": "123"

}
]

HTTP2模板获取
Action：slb.profile.http2.get
请求参数
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
请求举例：
POST：
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http2.get
请求body：
{
        "name": "p1"
}
响应参数
名称	类型	范围	含义
name	字符串	长度1-191	模版名称
Insert_x_header	字符串	长度1-63	插入头内容
响应举例：
{
    "name": "p1",
    "insert_x_header": ""
}


HTTP2模板增加
Action：slb.profile.http2.add
请求参数
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	
Insert_x_header	字符串	长度1-63	插入头内容	否	缺省值：空
请求举例：
POST：
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http2.add
请求body:
{
        "name": "p1",
        "insert_x_header": ""
}
HTTP2模板编辑
Action：slb.profile.http2.edit
请求参数
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	
Insert_x_header	字符串	长度1-63	插入头内容	否	
description	字符串
	长度1-191	描述	否	
请求举例：
POST：
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http2.edit
请求body:
 {
        "name": "p1",
        "insert_x_header": "",
        "description":"123"
}

HTTP2模板删除
Action：slb.profile.http2.del
请求参数
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	
Insert_x_header	字符串	长度1-63	插入头内容	否	
请求举例：
POST：
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.http2.del
请求body：
{
    "name": "p1",
    "insert_x_header": ""
}

SIP模板
SIP模板列表
Action：slb.profile.sip.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.sip.list
响应参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	
timeout	字符串	长度1-250	注册会话超时时间	否	缺省值:10
registrar_pool	字符串	长度1-191	sip注册服务池	否	缺省值:空
client_keepalive	整数	长度0-1	客户端保活关闭，开启	否	缺省值:0
call_id_persist	整数	长度0-1	call-id连接保持关闭，开启	否	缺省值:0
action_for_selclient_err	整数	长度0-1	客户端选择失败后丢包关闭，开启	否	缺省值:0
action_for_selserver_err	整数	长度0-1	服务端选择失败后丢包关闭，开启	否	缺省值:0
message_for_selclient_err	字符串	长度0-63	客户端选择失败后自定义状态码	否	缺省值:空
message_for_selserver_err	字符串	长度0-63	服务端选择失败后自定义状态码	否	缺省值:空
insert_client_ip	整数	长度0-1	插入客户端客户端ip关闭，开启	否	缺省值:0
dnat_alg	整数	长度0-1	内网到外网sdp端口ip替换关闭，开启	否	缺省值:1
snat_alg	整数	长度0-1	外网到内网sdp端口ip替换关闭，开启	否	缺省值:1
start_line_trans	整数	长度0-1	不转换sip报文起始行关闭，开启	否	缺省值:0
headers_trans	整数	长度0-1	不转换sip报文起始消息头，开启	否	缺省值:0
body_trans	整数	长度0-1	不转换sip报文起始消息体，开启	否	缺省值:0
nonat_match_acl	整数	长度100-199	匹配上ipv4 acl不做nat转换	否	缺省值:空
nonat_match_acl6	整数	长度100-199	匹配上ipv6 acl不做nat转换	否	缺省值:空
header_trans_list	字符串	长度1-63	该头字段的值不进行nat转换	否	缺省值:空
sdp_dnat_pool	字符串	长度1-191	sdp目的地址转换的服务池	否	缺省值:空
sdp_snat_pool	字符串	长度1-191	sdp源地址转换的服务池	否	缺省值:空
client_request_header_add_list	字符串	长度1-253	客户端请求头插入，详细参数如下：
client_request_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
client_request_header_add_list > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
client_response_header_add_list	字符串	长度1-253	客户端响应头插入，详细参数如下：
client_response_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
client_response_header_add_list > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
server_request_header_add_list	字符串	长度1-253	服务端请求头插入，详细参数如下：
server_request_header_add_listt > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
server_request_header_add_listt > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
server_response_header_add_list	字符串	长度1-253	服务端响应头插入，详细参数如下：
server_response_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
server_response_header_add_list > key: 
含义：插入头字段的值，
类型：字符串 
范围：1-190	否	缺省值:空
client_request_header_del_list	字符串	长度1-253	客户端请求头删除，详细参数如下：
client_request_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
client_response_header_del_list	字符串	长度1-253	客户端响应头删除，详细参数如下：
client_response_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
server_request_header_del_list	字符串	长度1-253	服务端请求头删除，详细参数如下：
server_request_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
server_response_header_del_list	字符串	长度1-253	服务端响应头删除，详细参数如下：
server_response_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
modify_header_list	字符串	长度1-253	头字段替换
modify_header_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
modify_header_list > key: 
含义：插入头字段的值，
类型：字符串 
范围：1-190	否	缺省值:空


响应举例：
{
  "name": "slb_profile_sip",
  "timeout": 10,
  "registrar_pool": "sip_registrar_pool",
  "client_keepalive": 1,
  "server_keepalive": 30,
  "call_id_persist": 1,
  "action_for_selclient_err": 0,
  "action_for_selserver_err": 0,
  "message_for_selclient_err": "403 SelectFailed",
  "message_for_selserver_err": "403 SelectFailed",
  "insert_client_ip": 0,
  "dnat_alg": 1,
  "snat_alg": 1,
  "start_line_trans": 0,
  "headers_trans": 0,
  "body_trans": 0,
  "nonat_match_acl": 100,
  "nonat_match_acl6": "200",
  "header_trans_list": [],
  "sdp_dnat_pool": "snat_pool_alg_v4",
  "sdp_snat_pool": "snat_pool_alg_v4",
  "client_request_header_add_list": [
    {
      "header": "ClientHeader1: 100",
      "type": 0
    }
  ],
  "client_response_header_add_list": [
    {
      "header": "ClientHeader2: 100",
      "type": 0
    }
  ],
  "server_request_header_add_list": [
    {
      "header": "ServerHeader1: 100",
      "type": 0
    }
  ],
  "server_response_header_add_list": [
    {
      "header": "ServerHeader2: 100",
      "type": 0
    }
  ],
  "client_request_header_del_list": [
    {
      "key": "DelClientHeader1"
    }
  ],
  "client_response_header_del_list": [
    {
      "key": "DelClientHeader2"
    }
  ],
  "server_request_header_del_list": [
    {
      "key": "DelServerHeader1"
    }
  ],
  "server_response_header_del_list": [
    {
      "key": "DelServerHeader2"
    }
  ],
  "modify_header_list": [
    {
      "key": "ClienderRequestHeader1",
      "val": "ClienderRequestValue1"
    }
  ]
}





分区中获取common和自己分区的sip模板列表
Action：slb.profile.sip.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.sip.list.withcommon
响应参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	
timeout	字符串	长度1-250	注册会话超时时间	否	缺省值:10
registrar_pool	字符串	长度1-191	sip注册服务池	否	缺省值:空
client_keepalive	整数	长度0-1	客户端保活关闭，开启	否	缺省值:0
call_id_persist	整数	长度0-1	call-id连接保持关闭，开启	否	缺省值:0
action_for_selclient_err	整数	长度0-1	客户端选择失败后丢包关闭，开启	否	缺省值:0
action_for_selserver_err	整数	长度0-1	服务端选择失败后丢包关闭，开启	否	缺省值:0
message_for_selclient_err	字符串	长度0-63	客户端选择失败后自定义状态码	否	缺省值:空
message_for_selserver_err	字符串	长度0-63	服务端选择失败后自定义状态码	否	缺省值:空
insert_client_ip	整数	长度0-1	插入客户端客户端ip关闭，开启	否	缺省值:0
dnat_alg	整数	长度0-1	内网到外网sdp端口ip替换关闭，开启	否	缺省值:1
snat_alg	整数	长度0-1	外网到内网sdp端口ip替换关闭，开启	否	缺省值:1
start_line_trans	整数	长度0-1	不转换sip报文起始行关闭，开启	否	缺省值:0
headers_trans	整数	长度0-1	不转换sip报文起始消息头，开启	否	缺省值:0
body_trans	整数	长度0-1	不转换sip报文起始消息体，开启	否	缺省值:0
nonat_match_acl	整数	长度100-199	匹配上ipv4 acl不做nat转换	否	缺省值:空
nonat_match_acl6	整数	长度100-199	匹配ipv6 acl不做nat转换	否	缺省值:空
header_trans_list	字符串	长度1-63	该头字段的值不进行nat转换	否	缺省值:空
sdp_dnat_pool	字符串	长度1-191	sdp目的地址转换的服务池	否	缺省值:空
sdp_snat_pool	字符串	长度1-191	sdp源地址转换的服务池	否	缺省值:空
client_request_header_add_list	字符串	长度1-253	客户端请求头插入	否	缺省值:空
client_response_header_add_list	字符串	长度1-253	客户端响应头插入	否	缺省值:空
server_request_header_add_list	字符串	长度1-253	服务端请求头插入	否	缺省值:空
server_response_header_add_list	字符串	长度1-253	服务端响应头插入	否	缺省值:空
client_request_header_del_list	字符串	长度1-253	客户端请求头删除	否	缺省值:空
client_response_header_del_list	字符串	长度1-253	客户端响应头删除	否	缺省值:空
server_request_header_del_list	字符串	长度1-253	服务端请求头删除	否	缺省值:空
server_response_header_del_list	字符串	长度1-253	服务端响应头删除	否	缺省值:空
modify_header_list	字符串	长度1-253	头字段替换	否	缺省值:空
响应举例：

[
  {
    "name": "profile_sip",
    "timeout": 10,
    "registrar_pool": "common/",
    "client_keepalive": 0,
    "server_keepalive": 30,
    "call_id_persist": 1,
    "action_for_selclient_err": 0,
    "action_for_selserver_err": 0,
    "message_for_selclient_err": "",
    "message_for_selserver_err": "",
    "insert_client_ip": 0,
    "dnat_alg": 1,
    "snat_alg": 1,
    "start_line_trans": 0,
    "headers_trans": 0,
    "body_trans": 0,
    "nonat_match_acl": 0,
    "nonat_match_acl6": "",
    "header_trans_list": [
      {
        "key": "HEADER1"
      },
      {
        "key": "HEADER2"
      }
    ],
    "sdp_dnat_pool": "",
    "sdp_snat_pool": "",
    "client_request_header_add_list": [],
    "client_response_header_add_list": [],
    "server_request_header_add_list": [],
    "server_response_header_add_list": [],
    "client_request_header_del_list": [],
    "client_response_header_del_list": [],
    "server_request_header_del_list": [],
    "server_response_header_del_list": [],
    "modify_header_list": []
  },
  {
    "name": "slb_profile_sip",
    "timeout": 10,
    "registrar_pool": "sip_registrar_pool",
    "client_keepalive": 1,
    "server_keepalive": 30,
    "call_id_persist": 1,
    "action_for_selclient_err": 0,
    "action_for_selserver_err": 0,
    "message_for_selclient_err": "403 SelectFailed",
    "message_for_selserver_err": "403 SelectFailed",
    "insert_client_ip": 0,
    "dnat_alg": 1,
    "snat_alg": 1,
    "start_line_trans": 0,
    "headers_trans": 0,
    "body_trans": 0,
    "nonat_match_acl": 100,
    "nonat_match_acl6": "200",
    "header_trans_list": [],
    "sdp_dnat_pool": "snat_pool_alg_v4",
    "sdp_snat_pool": "snat_pool_alg_v4",
    "client_request_header_add_list": [
      {
        "header": "ClientHeader1: 100",
        "type": 0
      }
    ],
    "client_response_header_add_list": [
      {
        "header": "ClientHeader2: 100",
        "type": 0
      }
    ],
    "server_request_header_add_list": [
      {
        "header": "ServerHeader1: 100",
        "type": 0
      }
    ],
    "server_response_header_add_list": [
      {
        "header": "ServerHeader2: 100",
        "type": 0
      }
    ],
    "client_request_header_del_list": [
      {
        "key": "DelClientHeader1"
      }
    ],
    "client_response_header_del_list": [
      {
        "key": "DelClientHeader2"
      }
    ],
    "server_request_header_del_list": [
      {
        "key": "DelServerHeader1"
      }
    ],
    "server_response_header_del_list": [
      {
        "key": "DelServerHeader2"
      }
    ],
    "modify_header_list": [
      {
        "key": "ClienderRequestHeader1",
        "val": "ClienderRequestValue1"
      }
    ]
  },
  {
    "name": "common/sip_profile_v4",
    "timeout": 10,
    "registrar_pool": "",
    "client_keepalive": 0,
    "server_keepalive": 30,
    "call_id_persist": 1,
    "action_for_selclient_err": 0,
    "action_for_selserver_err": 0,
    "message_for_selclient_err": "",
    "message_for_selserver_err": "",
    "insert_client_ip": 0,
    "dnat_alg": 1,
    "snat_alg": 1,
    "start_line_trans": 0,
    "headers_trans": 0,
    "body_trans": 0,
    "nonat_match_acl": 0,
    "nonat_match_acl6": "",
    "header_trans_list": [],
    "sdp_dnat_pool": "",
    "sdp_snat_pool": "",
    "client_request_header_add_list": [],
    "client_response_header_add_list": [],
    "server_request_header_add_list": [],
    "server_response_header_add_list": [],
    "client_request_header_del_list": [],
    "client_response_header_del_list": [],
    "server_request_header_del_list": [],
    "server_response_header_del_list": [],
    "modify_header_list": []
  },
  {
    "name": "common/sip_profile_v6",
    "timeout": 10,
    "registrar_pool": "",
    "client_keepalive": 0,
    "server_keepalive": 30,
    "call_id_persist": 1,
    "action_for_selclient_err": 0,
    "action_for_selserver_err": 0,
    "message_for_selclient_err": "",
    "message_for_selserver_err": "",
    "insert_client_ip": 0,
    "dnat_alg": 1,
    "snat_alg": 1,
    "start_line_trans": 0,
    "headers_trans": 0,
    "body_trans": 0,
    "nonat_match_acl": 0,
    "nonat_match_acl6": "",
    "header_trans_list": [],
    "sdp_dnat_pool": "",
    "sdp_snat_pool": "",
    "client_request_header_add_list": [],
    "client_response_header_add_list": [],
    "server_request_header_add_list": [],
    "server_response_header_add_list": [],
    "client_request_header_del_list": [],
    "client_response_header_del_list": [],
    "server_request_header_del_list": [],
    "server_response_header_del_list": [],
    "modify_header_list": []
  }
]
SIP模板获取
Action：slb.profile.sip.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.sip.get
请求body：
{
    "name": "slb_profile_sip"
}
响应参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	
timeout	字符串	长度1-250	注册会话超时时间	否	缺省值:10
registrar_pool	字符串	长度1-191	sip注册服务池	否	缺省值:空
client_keepalive	整数	长度0-1	客户端保活关闭，开启	否	缺省值:0
call_id_persist	整数	长度0-1	call-id连接保持关闭，开启	否	缺省值:0
action_for_selclient_err	整数	长度0-1	客户端选择失败后丢包关闭，开启	否	缺省值:0
action_for_selserver_err	整数	长度0-1	服务端选择失败后丢包关闭，开启	否	缺省值:0
message_for_selclient_err	字符串	长度0-63	客户端选择失败后自定义状态码	否	缺省值:空
message_for_selserver_err	字符串	长度0-63	服务端选择失败后自定义状态码	否	缺省值:空
insert_client_ip	整数	长度0-1	插入客户端客户端ip关闭，开启	否	缺省值:0
dnat_alg	整数	长度0-1	内网到外网sdp端口ip替换关闭，开启	否	缺省值:1
snat_alg	整数	长度0-1	外网到内网sdp端口ip替换关闭，开启	否	缺省值:1
start_line_trans	整数	长度0-1	不转换sip报文起始行关闭，开启	否	缺省值:0
headers_trans	整数	长度0-1	不转换sip报文起始消息头，开启	否	缺省值:0
body_trans	整数	长度0-1	不转换sip报文起始消息体，开启	否	缺省值:0
nonat_match_acl	整数	长度100-199	匹配上ipv4 acl不做nat转换	否	缺省值:空
nonat_match_acl6	整数	长度100-199	匹配上ipv6 acl不做nat转换	否	缺省值:空
header_trans_list	字符串	长度1-63	该头字段的值不进行nat转换	否	缺省值:空
sdp_dnat_pool	字符串	长度1-191	sdp目的地址转换的服务池	否	缺省值:空
sdp_snat_pool	字符串	长度1-191	sdp源地址转换的服务池	否	缺省值:空
client_request_header_add_list	字符串	长度1-253	客户端请求头插入，详细参数如下：
client_request_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
client_request_header_add_list > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
client_response_header_add_list	字符串	长度1-253	客户端响应头插入，详细参数如下：
client_response_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
client_response_header_add_list > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
server_request_header_add_list	字符串	长度1-253	服务端请求头插入，详细参数如下：
server_request_header_add_listt > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
server_request_header_add_listt > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
server_response_header_add_list	字符串	长度1-253	服务端响应头插入，详细参数如下：
server_response_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
server_response_header_add_list > key: 
含义：插入头字段的值，
类型：字符串 
范围：1-190	否	缺省值:空
client_request_header_del_list	字符串	长度1-253	客户端请求头删除，详细参数如下：
client_request_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
client_response_header_del_list	字符串	长度1-253	客户端响应头删除，详细参数如下：
client_response_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
server_request_header_del_list	字符串	长度1-253	服务端请求头删除，详细参数如下：
server_request_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
server_response_header_del_list	字符串	长度1-253	服务端响应头删除，详细参数如下：
server_response_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
modify_header_list	字符串	长度1-253	头字段替换
modify_header_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
modify_header_list > key: 
含义：插入头字段的值，
类型：字符串 
范围：1-190	否	缺省值:空



响应举例：

{
  "name": "slb_profile_sip",
  "timeout": 10,
  "registrar_pool": "sip_registrar_pool",
  "client_keepalive": 1,
  "server_keepalive": 30,
  "call_id_persist": 1,
  "action_for_selclient_err": 0,
  "action_for_selserver_err": 0,
  "message_for_selclient_err": "403 SelectFailed",
  "message_for_selserver_err": "403 SelectFailed",
  "insert_client_ip": 0,
  "dnat_alg": 1,
  "snat_alg": 1,
  "start_line_trans": 0,
  "headers_trans": 0,
  "body_trans": 0,
  "nonat_match_acl": 100,
  "nonat_match_acl6": "200",
  "header_trans_list": [],
  "sdp_dnat_pool": "snat_pool_alg_v4",
  "sdp_snat_pool": "snat_pool_alg_v4",
  "client_request_header_add_list": [
    {
      "header": "ClientHeader1: 100",
      "type": 0
    }
  ],
  "client_response_header_add_list": [
    {
      "header": "ClientHeader2: 100",
      "type": 0
    }
  ],
  "server_request_header_add_list": [
    {
      "header": "ServerHeader1: 100",
      "type": 0
    }
  ],
  "server_response_header_add_list": [
    {
      "header": "ServerHeader2: 100",
      "type": 0
    }
  ],
  "client_request_header_del_list": [
    {
      "key": "DelClientHeader1"
    }
  ],
  "client_response_header_del_list": [
    {
      "key": "DelClientHeader2"
    }
  ],
  "server_request_header_del_list": [
    {
      "key": "DelServerHeader1"
    }
  ],
  "server_response_header_del_list": [
    {
      "key": "DelServerHeader2"
    }
  ],
  "modify_header_list": [
    {
      "key": "ClienderRequestHeader1",
      "val": "ClienderRequestValue1"
    }
  ]
}
SIP模板增加
Action：slb.profile.sip.add
请求参数：

名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	
timeout	字符串	长度1-250	注册会话超时时间	否	缺省值:10
registrar_pool	字符串	长度1-191	sip注册服务池	否	缺省值:空
client_keepalive	整数	长度0-1	客户端保活关闭，开启	否	缺省值:0
call_id_persist	整数	长度0-1	call-id连接保持关闭，开启	否	缺省值:0
action_for_selclient_err	整数	长度0-1	客户端选择失败后丢包关闭，开启	否	缺省值:0
action_for_selserver_err	整数	长度0-1	服务端选择失败后丢包关闭，开启	否	缺省值:0
message_for_selclient_err	字符串	长度0-63	客户端选择失败后自定义状态码	否	缺省值:空
message_for_selserver_err	字符串	长度0-63	服务端选择失败后自定义状态码	否	缺省值:空
insert_client_ip	整数	长度0-1	插入客户端客户端ip关闭，开启	否	缺省值:0
dnat_alg	整数	长度0-1	内网到外网sdp端口ip替换关闭，开启	否	缺省值:1
snat_alg	整数	长度0-1	外网到内网sdp端口ip替换关闭，开启	否	缺省值:1
start_line_trans	整数	长度0-1	不转换sip报文起始行关闭，开启	否	缺省值:0
headers_trans	整数	长度0-1	不转换sip报文起始消息头，开启	否	缺省值:0
body_trans	整数	长度0-1	不转换SIP报文起始消息体，开启	否	缺省值:0
nonat_match_acl	整数	长度100-199	匹配上ipv4 acl不做nat转换	否	缺省值:空
nonat_match_acl6	整数	长度100-199	匹配上ipv6 acl不做nat转换	否	缺省值:空
header_trans_list	字符串	长度1-63	该头字段的值不进行nat转换	否	缺省值:空
sdp_dnat_pool	字符串	长度1-191	sdp目的地址转换的服务池	否	缺省值:空
sdp_snat_pool	字符串	长度1-191	sdp源地址转换的服务池	否	缺省值:空
client_request_header_add_list	字符串	长度1-253	客户端请求头插入，详细参数如下：
client_request_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
client_request_header_add_list > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
client_response_header_add_list	字符串	长度1-253	客户端响应头插入，详细参数如下：
client_response_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
client_response_header_add_list > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
server_request_header_add_list	字符串	长度1-253	服务端请求头插入，详细参数如下：
server_request_header_add_listt > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
server_request_header_add_listt > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
server_response_header_add_list	字符串	长度1-253	服务端响应头插入，详细参数如下：
server_response_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
server_response_header_add_list > key: 
含义：插入头字段的值，
类型：字符串 
范围：1-190	否	缺省值:空
client_request_header_del_list	字符串	长度1-253	客户端请求头删除，详细参数如下：
client_request_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
client_response_header_del_list	字符串	长度1-253	客户端响应头删除，详细参数如下：
client_response_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
server_request_header_del_list	字符串	长度1-253	服务端请求头删除，详细参数如下：
server_request_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
server_response_header_del_list	字符串	长度1-253	服务端响应头删除，详细参数如下：
server_response_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
modify_header_list	字符串	长度1-253	头字段替换
modify_header_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
modify_header_list > key: 
含义：插入头字段的值，
类型：字符串 
范围：1-190	否	缺省值:空





请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.sip.add
请求body：
{
  "name": "slb_profile_sip",
  "timeout": 10,
  "registrar_pool": "sip_registrar_pool",
  "client_keepalive": 1,
  "server_keepalive": 30,
  "call_id_persist": 1,
  "action_for_selclient_err": 0,
  "action_for_selserver_err": 0,
  "message_for_selclient_err": "403 SelectFailed",
  "message_for_selserver_err": "403 SelectFailed",
  "insert_client_ip": 0,
  "dnat_alg": 1,
  "snat_alg": 1,
  "start_line_trans": 0,
  "headers_trans": 0,
  "body_trans": 0,
  "nonat_match_acl": 100,
  "nonat_match_acl6": "200",
  "header_trans_list": [],
  "sdp_dnat_pool": "snat_pool_alg_v4",
  "sdp_snat_pool": "snat_pool_alg_v4",
  "client_request_header_add_list": [
    {
      "header": "ClientHeader1: 100",
      "type": 0
    }
  ],
  "client_response_header_add_list": [
    {
      "header": "ClientHeader2: 100",
      "type": 0
    }
  ],
  "server_request_header_add_list": [
    {
      "header": "ServerHeader1: 100",
      "type": 0
    }
  ],
  "server_response_header_add_list": [
    {
      "header": "ServerHeader2: 100",
      "type": 0
    }
  ],
  "client_request_header_del_list": [
    {
      "key": "DelClientHeader1"
    }
  ],
  "client_response_header_del_list": [
    {
      "key": "DelClientHeader2"
    }
  ],
  "server_request_header_del_list": [
    {
      "key": "DelServerHeader1"
    }
  ],
  "server_response_header_del_list": [
    {
      "key": "DelServerHeader2"
    }
  ],
  "modify_header_list": [
    {
      "key": "ClienderRequestHeader1",
      "val": "ClienderRequestValue1"
    }
  ]
}

SIP模板编辑
Action：slb.profile.sip.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	
timeout	字符串	长度1-250	注册会话超时时间	否	缺省值:10
registrar_pool	字符串	长度1-191	sip注册服务池	否	缺省值:空
client_keepalive	整数	长度0-1	客户端保活关闭，开启	否	缺省值:0
call_id_persist	整数	长度0-1	call-id连接保持关闭，开启	否	缺省值:0
action_for_selclient_err	整数	长度0-1	客户端选择失败后丢包关闭，开启	否	缺省值:0
action_for_selserver_err	整数	长度0-1	服务端选择失败后丢包关闭，开启	否	缺省值:0
message_for_selclient_err	字符串	长度0-63	客户端选择失败后自定义状态码	否	缺省值:空
message_for_selserver_err	字符串	长度0-63	服务端选择失败后自定义状态码	否	缺省值:空
insert_client_ip	整数	长度0-1	插入客户端客户端ip关闭，开启	否	缺省值:0
dnat_alg	整数	长度0-1	内网到外网sdp端口ip替换关闭，开启	否	缺省值:1
snat_alg	整数	长度0-1	外网到内网sdp端口ip替换关闭，开启	否	缺省值:1
start_line_trans	整数	长度0-1	不转换sip报文起始行关闭，开启	否	缺省值:0
headers_trans	整数	长度0-1	不转换sip报文起始消息头，开启	否	缺省值:0
body_trans	整数	长度0-1	不转换sip报文起始消息体，开启	否	缺省值:0
nonat_match_acl	整数	长度100-199	匹配上ipv4 acl不做nat转换	否	缺省值:空
nonat_match_acl6	整数	长度100-199	匹配上ipv6 acl不做nat转换	否	缺省值:空
header_trans_list	字符串	长度1-63	该头字段的值不进行nat转换	否	缺省值:空
sdp_dnat_pool	字符串	长度1-191	sdp目的地址转换的服务池	否	缺省值:空
sdp_snat_pool	字符串	长度1-191	sdp源地址转换的服务池	否	缺省值:空
client_request_header_add_list	字符串	长度1-253	客户端请求头插入，详细参数如下：
client_request_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
client_request_header_add_list > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
client_response_header_add_list	字符串	长度1-253	客户端响应头插入，详细参数如下：
client_response_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
client_response_header_add_list > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
server_request_header_add_list	字符串	长度1-253	服务端请求头插入，详细参数如下：
server_request_header_add_listt > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
server_request_header_add_listt > key: 
含义：插入头字段的值，
类型：字符串
范围：1-190	否	缺省值:空
server_response_header_add_list	字符串	长度1-253	服务端响应头插入，详细参数如下：
server_response_header_add_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
server_response_header_add_list > key: 
含义：插入头字段的值，
类型：字符串 
范围：1-190	否	缺省值:空
client_request_header_del_list	字符串	长度1-253	客户端请求头删除，详细参数如下：
client_request_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
client_response_header_del_list	字符串	长度1-253	客户端响应头删除，详细参数如下：
client_response_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
server_request_header_del_list	字符串	长度1-253	服务端请求头删除，详细参数如下：
server_request_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
server_response_header_del_list	字符串	长度1-253	服务端响应头删除，详细参数如下：
server_response_header_del_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63	否	缺省值:空
modify_header_list	字符串	长度1-253	头字段替换
modify_header_list > key: 
含义：插入的头字段，
类型：字符串
范围：1-63
modify_header_list > key: 
含义：插入头字段的值，
类型：字符串 
范围：1-190	否	缺省值:空

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.sip.edit
请求body：
{
  "name": "slb_profile_sip",
  "timeout": 10,
  "registrar_pool": "sip_registrar_pool",
  "client_keepalive": 1,
  "server_keepalive": 30,
  "call_id_persist": 1,
  "action_for_selclient_err": 0,
  "action_for_selserver_err": 0,
  "message_for_selclient_err": "403 SelectFailed",
  "message_for_selserver_err": "403 SelectFailed",
  "insert_client_ip": 0,
  "dnat_alg": 1,
  "snat_alg": 1,
  "start_line_trans": 0,
  "headers_trans": 0,
  "body_trans": 0,
  "nonat_match_acl": 100,
  "nonat_match_acl6": "200",
  "header_trans_list": [],
  "sdp_dnat_pool": "snat_pool_alg_v4",
  "sdp_snat_pool": "snat_pool_alg_v4",
  "client_request_header_add_list": [
    {
      "header": "ClientHeader1: 100",
      "type": 0
    }
  ],
  "client_response_header_add_list": [
    {
      "header": "ClientHeader2: 100",
      "type": 0
    }
  ],
  "server_request_header_add_list": [
    {
      "header": "ServerHeader1: 100",
      "type": 0
    }
  ],
  "server_response_header_add_list": [
    {
      "header": "ServerHeader2: 100",
      "type": 0
    }
  ],
  "client_request_header_del_list": [
    {
      "key": "DelClientHeader1"
    }
  ],
  "client_response_header_del_list": [
    {
      "key": "DelClientHeader2"
    }
  ],
  "server_request_header_del_list": [
    {
      "key": "DelServerHeader1"
    }
  ],
  "server_response_header_del_list": [
    {
      "key": "DelServerHeader2"
    }
  ],
  "modify_header_list": [
    {
      "key": "ClienderRequestHeader1",
      "val": "ClienderRequestValue1"
    }
  ]
}
SIP模板删除
Action：slb.profile.sip.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.sip.del
请求body：
{
    "name": "slb_profile_sip"
}

DNS模板
DNS模板列表
Action：slb.profile.dns.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.dns.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
enabled	整数	0-1	状态；1：开启；0：禁用
description	字符串	长度1-191	描述
drop_bad_req	整数	0-1	安全策略；1：开启；0：禁用
default_to_cache	整数	0-1	默认cache；1：开启；0：禁用
cache_size	整数	0-2000000	最大cache数，最大规格与设备内存有关，(0,4g]:64k;(4,16g]:500k;(16,∞]:2M
insert_client_ip	整数	0-1	插入客户端地址；1：开启；0：禁用
netmask	整数	1-128	插入的客户端地址掩码位数
ruletable_name	字符串	长度1-191	规则表名称
ruletables	数组	不涉及	规则表成员对象组成的数组，详细参数如下：
ruletables > id：
含义：规则表id，
类型：整数，
范围：1-30
ruletables > conn_rate_limit：
含义：连接限制值，
类型：整数，
范围：1-2147483647
ruletables > type：
含义：算法类型，0：丢弃；1：重置
范围：0-1
类型：整数
ruletables > lock_time：
含义：会话锁定时间，
类型：整数，
范围：1-1023
ruletables > log：
含义：日志打印间隔时间，
类型：整数，
范围：1-255
conn_rate_limit_interval：请求速率间隔，单位为100ms，整数，范围1-65535
ruletables > dns_ttl：
含义：DNS缓存的ttl值，
类型：整数，
范围：1-65535
ruletables > dns_weight：
含义：DNS缓存的weight值，
类型：整数，
范围：1-7
ruletables > cache_enable：
含义：是否生成dns缓存，0：关闭；1：开启
类型：整数
范围：1-0
响应举例：
  [
{
   		 "name": "dns",
    		"description": "",
    		"enabled": 1,
   		 "drop_bad_req": 1,
    		"default_to_cache": 1,
    		"cache_size": 5000,
    		"insert_client_ip": 1,
    		"netmask": 24,
    		"ruletable_name": "gh",
    		"ruletables": [
        	{
            		"id": 1,
            		"conn_rate_limit": 100,
            		"type": 0,
            		"lock_time": 1,
           		 "log": 1,
            		"conn_rate_limit_interval": 10,
            		"dns_ttl": 300,
            		"dns_weight": 1,
            		"cache_enable": 0
        	}
    		]
}
]


分区中获取common和自己分区的dns模板列表
Action：slb.profile.dns.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.dns.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
enabled	整数	0-1	状态；1：开启；0：禁用
description	字符串	长度1-191	描述
drop_bad_req	整数	0-1	安全策略；1：开启；0：禁用
default_to_cache	整数	0-1	默认cache；1：开启；0：禁用
cache_size	整数	0-2000000	最大cache数，最大规格与设备内存有关，(0,4g]:64k;(4,16g]:500k;(16,∞]:2M
insert_client_ip	整数	0-1	插入客户端地址；1：开启；0：禁用
netmask	整数	1-128	插入的客户端地址掩码位数
ruletable_name	字符串	长度1-191	规则表名称
ruletables	数组	不涉及	规则表成员对象组成的数组，详细参数如下：
ruletables > id：
含义：规则表id，
类型：整数，
范围：1-30
ruletables > conn_rate_limit：
含义：连接限制值，
类型：整数，
范围：1-2147483647
ruletables > type：
含义：算法类型，0：丢弃；1：重置
范围：0-1
类型：整数
ruletables > lock_time：
含义：会话锁定时间，
类型：整数，
范围：1-1023
ruletables > log：
含义：日志打印间隔时间，
类型：整数，
范围：1-255
conn_rate_limit_interval：请求速率间隔，单位为100ms，整数，范围1-65535
ruletables > dns_ttl：
含义：DNS缓存的ttl值，
类型：整数，
范围：1-65535
ruletables > dns_weight：
含义：DNS缓存的weight值，
类型：整数，
范围：1-7
ruletables > cache_enable：
含义：是否生成dns缓存，0：关闭；1：开启
类型：整数
范围：1-0
响应举例：
[
    {
   		 "name": "net_dns",
    		"description": "",
    		"enabled": 1,
   		 "drop_bad_req": 1,
    		"default_to_cache": 1,
    		"cache_size": 5000,
    		"insert_client_ip": 1,
    		"netmask": 24,
    		"ruletable_name": "gh",
    		"ruletables": [
        	{
            		"id": 1,
            		"conn_rate_limit": 100,
            		"type": 0,
            		"lock_time": 1,
           		 "log": 1,
            		"conn_rate_limit_interval": 10,
            		"dns_ttl": 300,
            		"dns_weight": 1,
            		"cache_enable": 0
        	}
    		]
},
{
   		 "name": "common/dns",
    		"description": "",
    		"enabled": 1,
   		 "drop_bad_req": 1,
    		"default_to_cache": 1,
    		"cache_size": 5000,
    		"insert_client_ip": 1,
    		"netmask": 24,
    		"ruletable_name": "gh",
    		"ruletables": [
        	{
            		"id": 1,
            		"conn_rate_limit": 100,
            		"type": 0,
            		"lock_time": 1,
           		 "log": 1,
            		"conn_rate_limit_interval": 10,
            		"dns_ttl": 300,
            		"dns_weight": 1,
            		"cache_enable": 0
        	}
    		]
}

]

DNS模板获取
Action：slb.profile.dns.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.dns.get
请求body：
{
	"name": "dns"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-63	模板名称
enabled	整数	0-1	状态；1：开启；0：禁用
description	字符串	长度1-191	描述
drop_bad_req	整数	0-1	安全策略；1：开启；0：禁用
default_to_cache	整数	0-1	默认cache；1：开启；0：禁用
cache_size	整数	0-2000000	最大cache数，最大规格与设备内存有关，(0,4g]:64k;(4,16g]:500k;(16,∞]:2M
insert_client_ip	整数	0-1	插入客户端地址；1：开启；0：禁用
netmask	整数	1-128	插入的客户端地址掩码位数
ruletable_name	字符串	长度1-191	规则表名称
ruletables	数组	不涉及	规则表成员对象组成的数组，详细参数如下：
ruletables > id：
含义：规则表id，
类型：整数，
范围：1-30
ruletables > conn_rate_limit：
含义：连接限制值，
类型：整数，
范围：1-2147483647
ruletables > type：
含义：算法类型，0：丢弃；1：重置
范围：0-1
类型：整数
ruletables > lock_time：
含义：会话锁定时间，
类型：整数，
范围：1-1023
ruletables > log：
含义：日志打印间隔时间，
类型：整数，
范围：1-255
conn_rate_limit_interval：请求速率间隔，单位为100ms，整数，范围1-65535
ruletables > dns_ttl：
含义：dns缓存的ttl值，
类型：整数，
范围：1-65535
ruletables > dns_weight：
含义：dns缓存的weight值，
类型：整数，
范围：1-7
ruletables > cache_enable：
含义：是否生成DNS缓存，0：关闭；1：开启
类型：整数
范围：1-0

响应举例：
{
   		 "name": "dns",
    		"description": "",
    		"enabled": 1,
   		 "drop_bad_req": 1,
    		"default_to_cache": 1,
    		"cache_size": 5000,
    		"insert_client_ip": 1,
    		"netmask": 24,
    		"ruletable_name": "gh",
    		"ruletables": [
        	{
            		"id": 1,
            		"conn_rate_limit": 100,
            		"type": 0,
            		"lock_time": 1,
           		 "log": 1,
            		"conn_rate_limit_interval": 10,
            		"dns_ttl": 300,
            		"dns_weight": 1,
            		"cache_enable": 0
        	}
    		]
}
DNS模板增加
Action：slb.profile.dns.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
description	字符串	长度1-191	描述	否	
enabled	整数	0-1	状态	否	1开启，0禁用，缺省值:1
drop_bad_req	整数	0-1	安全策略	否	1开启，0禁用，缺省值:0
default_to_cache	整数	0-1	默认cache	否	1开启，0禁用，缺省值:0
cache_size	整数	0-2000000	最大cache数
最大规格与设备内存有关，(0,4g]:64k;(4,16g]:500k;(16,∞]:2M	否	缺省值:0
insert_client_ip	整数	0-1	插入客户端地址；1：开启；0：禁用	否	缺省值:0
netmask	整数	1-128	插入的客户端地址掩码位数	否	
ruletable_name	字符串	长度1-191	规则表名称	否	
ruletables	数组	不涉及	规则表成员对象组成的数组，详细参数如下：
ruletables > id：
含义：规则表id，
类型：整数，
范围：1-30
ruletables > conn_rate_limit：
含义：连接限制值，
类型：整数，
范围：1-2147483647
ruletables > type：
含义：算法类型，0：丢弃；1：重置
范围：0-1
类型：整数
ruletables > lock_time：
含义：会话锁定时间，
类型：整数，
范围：1-1023
ruletables > log：
含义：日志打印间隔时间，
类型：整数，
范围：1-255
conn_rate_limit_interval：请求速率间隔，单位为100ms，整数，范围1-65535
ruletables > dns缓存的ttl值，
类型：整数，
范围：1-65535
ruletables > dns_weight：
含义：dns缓存的weight值，
类型：整数，
范围：1-7
ruletables > cache_enable：
含义：是否生成dns缓存，0：关闭；1：开启
类型：整数
范围：1-0	是	
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.dns.add
请求body：
 {
        "name": "dns_proflie_1",
        "description": "",
        "enabled": 1,
        "drop_bad_req": 1,
        "default_to_cache": 1,
        "cache_size": 20000,
        "insert_client_ip": 1,
        "netmask": 128,
        "ruletable_name": "",
        "ruletables": []
    }

DNS模板编辑
Action：slb.profile.dns.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
description	字符串	长度1-191	描述	否	
enabled	整数	0-1	状态	否	1开启，0禁用，缺省值:1
drop_bad_req	整数	0-1	安全策略	否	1开启，0禁用，缺省值:0
default_to_cache	整数	0-1	默认cache	否	1开启，0禁用，缺省值:0
cache_size	整数	0-2000000	最大cache数，最大规格与设备内存有关，(0,4g]:64k;(4,16g]:500k;(16,∞]:2M	否	缺省值:0
insert_client_ip	整数	0-1	插入客户端地址；1：开启；0：禁用	否	缺省值:0
netmask	整数	1-128	插入的客户端地址掩码位数	否	
ruletable_name	字符串	长度1-191	规则表名称	否	
ruletables	数组	不涉及	规则表成员对象组成的数组，详细参数如下：
ruletables > id：
含义：规则表id，
类型：整数，
范围：1-30
ruletables > conn_rate_limit：
含义：连接限制值，
类型：整数，
范围：1-2147483647
ruletables > type：
含义：算法类型，0：丢弃；1：重置
范围：0-1
类型：整数
ruletables > lock_time：
含义：会话锁定时间，
类型：整数，
范围：1-1023
ruletables > log：
含义：日志打印间隔时间，
类型：整数，
范围：1-255
conn_rate_limit_interval：请求速率间隔，单位为100ms，整数，范围1-65535
ruletables > dns_ttl：
含义：dns缓存的ttl值，
类型：整数，
范围：1-65535
ruletables > dns_weight：
含义：dns缓存的weight值，
类型：整数，
范围：1-7
ruletables > cache_enable：
含义：是否生成dns缓存，0：关闭；1：开启
类型：整数
范围：1-0	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.dns.edit
请求body：
 {
        "name": "dns_proflie_1",
        "description": "",
        "enabled": 1,
        "drop_bad_req": 1,
        "default_to_cache": 1,
        "cache_size": 5000,
        "insert_client_ip": 1,
        "netmask": 128,
        "ruletable_name": "rule_1",
        "ruletables": [
            {
                "id": 1,
                "conn_rate_limit": 0,
                "type": 0,
                "lock_time": 0,
                "log": 0,
                "log_interval": 0,
                "conn_rate_limit_interval": 10,
                "dns_ttl": 300,
                "dns_weight": 1,
                "cache_enable": 0
            }
        ]
    }    

DNS模板删除
Action：slb.profile.dns.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.dns.del
请求body：
{"name": "dns_proflie_1"}

SMTP模板
SMTP模板列表
Action：slb.profile.smtp.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.smtp.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
starttls	整数	0-2	starttls需求；0禁止，1可选，2强制
expn	整数	0，1	禁止命令turn；0不禁止，1禁止
turn	整数	0，1	禁止命令expn；0不禁止，1禁止
vrfy	整数	0，1	禁止命令vrfy；0不禁止，1禁止
description	字符串
	长度1-191	描述
email_server_domain	字符串	长度1-63	email服务器域
server_ready_message	字符串	长度1-63	服务器就绪消息
client_switch	数组	不涉及	服务池选择
详细参数如下：
client_switch > client_domain：
含义：客户端域
类型：字符串
范围：1-63
client_switch >pool：
含义：服务池
类型：字符串
范围：1-63
client_switch >match_method：
含义：匹配方法:0:包含;1:头;2:尾;
类型：整数
范围：0-2
响应举例：
[{
  "name": "p1",
  "starttls": 0,
  "expn": 1,
"description": "23",
  "turn": 0,
  "vrfy": 0,
  "email_server_domain": "dom",
  "server_ready_message": "rdy",
  "client_switch": [
    {
      "client_domain": "client",
      "pool": "pool",
      "match_method": 0
    },
    {
      "client_domain": "client2",
      "pool": "pool",
      "match_method": 1
    },
    {
      "client_domain": "client3",
      "pool": "pool",
      "match_method": 2
    }
  ]
}]

分区获取common和自己分区的smtp模板列表
Action：slb.profile.smtp.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.smtp.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
starttls	整数	0-2	starttls需求；0禁止，1可选，2强制
expn	整数	0，1	禁止命令turn；0不禁止，1禁止
turn	整数	0，1	禁止命令expn；0不禁止，1禁止
vrfy	整数	0，1	禁止命令vrfy；0不禁止，1禁止
description	字符串
	长度1-191	描述
email_server_domain	字符串	长度1-63	email服务器域
server_ready_message	字符串	长度1-63	服务器就绪消息
client_switch	数组	不涉及	服务池选择
详细参数如下：
client_switch > client_domain：
含义：客户端域
类型：字符串
范围：1-63
client_switch >pool：
含义：服务池
类型：字符串
范围：1-63
client_switch >match_method：
含义：匹配方法:0:包含;1:头;2:尾;
类型：整数
范围：0-2
响应举例：
[
    {
        "name": "p1_smtp1",
        "starttls": 0,
        "expn": 1,
"description": "23", 
        "turn": 1,
        "vrfy": 1,
        "email_server_domain": "",
        "server_ready_message": "",
        "client_switch": []
    },
    {
        "name": "common/co_profile_smtp",
        "starttls": 0,
        "expn": 0,
        "turn": 0,
        "vrfy": 0,
        "email_server_domain": "aaa",
        "server_ready_message": "bbb",
        "client_switch": [
            {
                "client_domain": "client",
                "pool": "common/pool_ftp_2000:203:3::100_2000:203:3::107_8365",
                "match_method": 0
            }
        ]
    },
]
SMTP模板获取
Action：slb.profile.smtp.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.smtp.get
请求body：
{
    "name": "p1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
starttls	整数	0-2	starttls需求；0禁止，1可选，2强制
expn	整数	0，1	禁止命令turn；0不禁止，1禁止
turn	整数	0，1	禁止命令expn；0不禁止，1禁止
vrfy	整数	0，1	禁止命令vrfy；0不禁止，1禁止
description	字符串
	长度1-191	描述
email_server_domain	字符串	长度1-63	email服务器域
server_ready_message	字符串	长度1-63	服务器就绪消息
client_switch	数组	不涉及	服务池选择
详细参数如下：
client_switch > client_domain：
含义：客户端域
类型：字符串
范围：1-63
client_switch >pool：
含义：服务池
类型：字符串
范围：1-63
client_switch >match_method：
含义：匹配方法:0:包含;1:头;2:尾;
类型：整数
范围：0-2

响应举例：
{
  "name": "p1",
  "starttls": 0,
  "expn": 1,
  "turn": 0,
  "vrfy": 0,
"description": "23", 
  "email_server_domain": "dom",
  "server_ready_message": "rdy",
  "client_switch": [
    {
      "client_domain": "client",
      "pool": "pool",
      "match_method": 0
    },
    {
      "client_domain": "client2",
      "pool": "pool",
      "match_method": 1
    },
    {
      "client_domain": "client3",
      "pool": "pool",
      "match_method": 2
    }
  ]
}
SMTP模板增加
Action：slb.profile.smtp.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
starttls	整数	0-2	starttls需求；0禁止，1可选，2强制	否	0禁止;1可选;2强制；缺省值:0
expn	整数	0，1	禁止命令turn；0不禁止，1禁止	否	0不禁止，1禁止；缺省值:0
turn	整数	0，1	禁止命令expn；0不禁止，1禁止	否	0不禁止，1禁止；缺省值:0
vrfy	整数	0，1	禁止命令vrfy；0不禁止，1禁止	否	0不禁止，1禁止，缺省值:0
description	字符串
	长度1-191	描述	否	缺省值:空
email_server_domain	字符串	长度1-63	email服务器域	否	缺省值:空
server_ready_message	字符串	长度1-63	服务器就绪消息	否	缺省值:空
client_switch	数组	不涉及	服务池选择
详细参数如下：
client_switch > client_domain：
含义：客户端域
类型：字符串
范围：1-63
client_switch >pool：
含义：服务池
类型：字符串
范围：1-63
client_switch >match_method：
含义：匹配方法:0:包含;1:头;2:尾;
类型：整数
范围：0-2	否	
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.smtp.add
请求body：
{
        "name": "smtp_1",
        "description": "",
        "starttls": 0,
        "expn": 1,
        "turn": 1,
        "vrfy": 1,
        "email_server_domain": "www.123.con",
        "server_ready_message": "aaaaa",
        "client_switch": [
            {
                "client_domain": "client",
                "pool": "smtp_pool_v4",
                "match_method": 0
            }
        ]
    }

SMTP模板编辑
Action：slb.profile.smtp.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
starttls	整数	0-2	starttls需求；0禁止，1可选，2强制	否	0禁止;1可选;2强制；缺省值:0
expn	整数	0，1	禁止命令turn；0不禁止，1禁止	否	0不禁止，1禁止；缺省值:0
turn	整数	0，1	禁止命令expn；0不禁止，1禁止	否	0不禁止，1禁止；缺省值:0
vrfy	整数	0，1	禁止命令vrfy；0不禁止，1禁止	否	0不禁止，1禁止，缺省值:0
description	字符串
	长度1-191	描述	否	缺省值:空
email_server_domain	字符串	长度1-63	email服务器域	否	缺省值:空
server_ready_message	字符串	长度1-63	服务器就绪消息	否	缺省值:空
client_switch	数组	不涉及	服务池选择
详细参数如下：
client_switch > client_domain：
含义：客户端域
类型：字符串
范围：1-63
client_switch >pool：
含义：服务池
类型：字符串
范围：1-63
client_switch >match_method：
含义：匹配方法:0:包含;1:头;2:尾;
类型：整数
范围：0-2	否	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.smtp.edit
请求body：
 {
        "name": "smtp_1",
        "description": "",
        "starttls": 0,
        "expn": 1,
        "turn": 1,
        "vrfy": 1,
        "email_server_domain": "www.123.con",
        "server_ready_message": "aaaaaaaaaaa",
        "client_switch": [
            {
                "client_domain": "client",
                "pool": "smtp_pool_v4",
                "match_method": 0
            }
        ]
    }

SMTP模板删除
Action：slb.profile.smtp.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.smtp.del
请求body：
{
    "name": "smtp_1"
}

RTSP模板
RTSP模板列表
Action:  slb.profile.rtsp.list
请求参数:无
请求举例:
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.rtsp.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
uri_switch	数组	不涉及	策略列表，详细参数如下
uri_switch > uri:
类型：字符串	
范围：1-63	
含义：策略--匹配uri
uri_switch > pool：
类型：字符串	
范围：1-63	
含义：策略--匹配uri后选择服务池名称
uri_switch > description：	
类型：字符串	
范围：1-191	
含义：描述
响应举例：
[
  {
    "name": "p1", 
    "uri_switch": [
      {
        "uri": "/aaa", 
     "description": "23", 
        "pool": "pool0" 
      }
    ]
  }
]


分区获取common和自己分区的rtsp模板列表
Action:  slb.profile.rtsp.list.withcommon
请求参数:无
请求举例:
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.rtsp.list.withcommon
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
uri_switch	数组	不涉及	策略列表，详细参数如下
uri_switch > uri:
类型：字符串	
范围：1-63	
含义：策略--匹配uri
uri_switch > pool：
类型：字符串	
范围：1-63	
含义：策略--匹配uri后选择服务池名称
uri_switch > description：	
类型：字符串	
范围：1-191	
含义：描述


响应举例：
[
    {
        "name": "partition_pro_rtsp",
        "uri_switch": [
            {
                "uri": "uri",
"description": "23", 
                "pool": "common/pool1"
            }
        ]
    },
    {
        "name": "common/pro_rtsp",
        "uri_switch": [
            {
                "uri": "/",
                "pool": "common/pool2"
            }
        ]
    }
]


RTSP模板获取
Action: slb.profile.rtsp.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.rtsp.get
请求body：
{
    "name": "p1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
uri_switch	数组	不涉及	策略列表，详细参数如下
uri_switch > uri:
类型：字符串	
范围：1-63	
含义：策略--匹配uri
uri_switch > pool：
类型：字符串	
范围：1-63	
含义：策略--匹配uri后选择服务池名称
uri_switch > description：	
类型：字符串	
范围：1-191	
含义：描述

响应举例：
  {
    "name": "p1", 
    "uri_switch": [
      {
        "uri": "/aaa", 
        "pool": "pool0" 
      }
    ]
  }
RTSP模板增加
Action:  slb.profile.rtsp.add
请求参数:
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
uri_switch	数组	不涉及	策略列表，详细参数如下
uri_switch > uri:
类型：字符串	
范围：1-63	
含义：策略--匹配uri
uri_switch > pool：
类型：字符串	
范围：1-63	
含义：策略--匹配uri后选择服务池名称
uri_switch > description：	
类型：字符串	
范围：1-191	
含义：描述
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.rtsp.add
请求body：
{
        "name": "rtsp_1",
        "description": "",
        "uri_switch": [
            {
                "uri": "uri",
                "pool": "pool"
            },
            {
                "uri": "uri1",
                "pool": "pool"
            }
        ]
    }  
RTSP模板编辑
Action:  slb.profile.rtsp.edit
请求参数:
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
uri_switch	数组	不涉及	策略列表，详细参数如下
uri_switch > url:
类型：字符串	
范围：1-63	
含义：策略--匹配uri
uri_switch > pool：
类型：字符串	
范围：1-63	
含义：策略--匹配uri后选择服务池名称
uri_switch > description：	
类型：字符串	
范围：1-191	
含义：描述

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.rtsp.edit
请求body：
{
        "name": "rtsp_1",
        "description": "123456",
        "uri_switch": [
            {
                "uri": "uri",
                "pool": "pool"
            },
            {
                "uri": "uri1",
                "pool": "pool"
            }
        ]
    }  
RTSP模板删除
Action：slb.profile.rtsp.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.rtsp.del
请求body：
{
    "name": "rtsp_1"
}

FTP模板
FTP模板列表
Action：slb.profile.ftp.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.ftp.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
active_mode_port	整数	1-65535	主动模式端口
disable_active_mode	整数	0-1	禁用主动模式：0不禁用，1禁用
disable_passive_mode	整数	0-1	禁用被动模式：0不禁用，1禁用
description	字符串
	长度1-191	描述
响应举例：
[
{
    		"name": "pro_ftp",                
 "active_mode_port": 20,       
"description": "23",           
 "disable_active_mode": 0,           
"disable_passive_mode": 0         
}
]


Action：slb.profile.ftp.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.ftp.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	模板名称
active_mode_port	整数	1-65535	主动模式端口
disable_active_mode	整数	0-1	禁用主动模式：0不禁用，1禁用
disable_passive_mode	整数	0-1	禁用被动模式：0不禁用，1禁用
description	字符串
	长度1-191	描述
响应举例：
[
    {
        "name": "partition_pro_ftp",
        "active_mode_port": 20,
"description": "23", 
        "disable_active_mode": 0,
        "disable_passive_mode": 0
    },
    {
        "name": "common/pro_ftp",
        "active_mode_port": 20,
        "disable_active_mode": 0,
        "disable_passive_mode": 0
    }
]
FTP模板获取
Action：slb.profile.ftp.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.ftp.get
请求body：
{
	"name": "p1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-63	模板名称
active_mode_port	整数	1-65535	主动模式端口
disable_active_mode	整数	0-1	禁用主动模式：0不禁用，1禁用
disable_passive_mode	整数	0-1	禁用被动模式：0不禁用，1禁用
description	字符串
	长度1-191	描述

响应举例：
  {
    "name": "p1",                
"active_mode_port": 20,   
"description": "23",               
    "disable_active_mode": 0,           
"disable_passive_mode": 0         
  }
FTP模板增加
Action：slb.profile.ftp.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
active_mode_port	整数	1-65535	主动模式端口	否	缺省值：20
disable_active_mode	整数	0-1	禁用主动模式	否	0不禁用，1禁用，缺省值:0
disable_passive_mode	整数	0-1	禁用被动模式	否	0不禁用，1禁用，缺省值:0
description	字符串
	长度1-191	描述	否	
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.ftp.add
请求body：
{
    "name": "ftp_1",                
    "active_mode_port": 4444,                 
    "disable_active_mode": 0,           
    "disable_passive_mode": 0         
  } 
FTP模板编辑
Action：slb.profile.ftp.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
active_mode_port	整数	1-65535	主动模式端口	否	缺省值：：不修改
disable_active_mode	整数	0-1	禁用主动模式	否	0不禁用，1禁用，缺省值:0
disable_passive_mode	整数	0-1	禁用被动模式	否	0不禁用，1禁用，缺省值:0
description	字符串
	长度1-191	描述	否	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.ftp.edit
请求body：
{
    "name": "ftp_1",                
    "active_mode_port": 44,                 
    "disable_active_mode": 0,           
    "disable_passive_mode": 0         
  } 

FTP模板删除
Action：slb.profile.ftp.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.ftp.del
请求body：
{
"name": "ftp_1"
}


请求日志模板
请求日志模板列表
Action：slb.profile.request_log.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.request_log.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	请求日志模板名称
request_log	整数	0,1	请求日志模板开关，0：关闭，1：开启
log_source_port_mode	整数	0,1	日志发送源端口，0：轮询，1：随机
request_log_error_response
	整数	0,1	请求错误响应日志模板开关，0：关闭，1：开启
request_log_error_close	整数	0,1	错误关闭会话开关，0：关闭，1：开启
request_log_error_log_enable
	整数	0,1	错误日志模板开关，0：关闭，1：开启
response_log
	整数	0,1	响应日志模板开关，0：关闭，1：开启
response_log_error_log_enable
	整数	0,1	错误响应日志模板开关，0：关闭，1：开启
request_log_pool
	字符串	1-191	请求日志发送服务池
request_log_error_log_pool
	字符串	1-191	请求错误日志发送服务池
response_log_pool
	字符串	1-191	响应日志发送服务池
response_log_error_log_pool
	字符串	1-191	响应错误日志发送服务池
request_log_template
	字符串	长度1-4095	请求日志发送模板
request_log_error_response_content
	字符串	1-1023	请求错误响应自定义内容
request_log_error_log_template
	字符串	1-4095	请求错误日志模板
response_log_template
	字符串	1-4095	响应日志模板
response_log_error_log_template
	字符串	1-4095	响应错误日志模板

响应举例：
[
    {
        "name": "log_all",
        "request_log": 1,
       		   "log_source_port": 0,
                "log_source_port_mode": 1,
        "request_log_error_response": 1,
        "request_log_error_close": 1,
        "request_log_error_log_enable": 1,
        "response_log": 1,
        "response_log_error_log_enable": 1,
        "request_log_pool": "syslog",
        "request_log_error_log_pool": "syslog",
        "response_log_pool": "syslog",
        "response_log_error_log_pool": "syslog",
        "request_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME",
        "request_log_error_response_content": "server:nginx",
        "request_log_error_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME",
        "response_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME",
        "response_log_error_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME"
    }
]

分区中获取common分区的请求日志模板列表
Action：slb.profile.request_log.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.request_log.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	请求日志模板名称
log_source_port_mode	整数	0,1	日志发送源端口，0：轮询，1：随机
request_log	整数	0,1	请求日志模板开关，0：关闭，1：开启
request_log_error_response
	整数	0,1	请求错误响应日志模板开关，0：关闭，1：开启
request_log_error_close	整数	0,1	错误关闭会话开关，0：关闭，1：开启
request_log_error_log_enable
	整数	0,1	错误日志模板开关，0：关闭，1：开启
response_log
	整数	0,1	响应日志模板开关，0：关闭，1：开启
response_log_error_log_enable
	整数	0,1	错误响应日志模板开关，0：关闭，1：开启
request_log_pool
	字符串	1-191	请求日志发送服务池
request_log_error_log_pool
	字符串	1-191	请求错误日志发送服务池
response_log_pool
	字符串	1-191	响应日志发送服务池
response_log_error_log_pool
	字符串	1-191	响应错误日志发送服务池
request_log_template
	字符串	长度1-65520	请求日志发送模板
request_log_error_response_content
	字符串	长度1-65520	请求错误响应自定义内容
request_log_error_log_template
	字符串	长度1-65520	请求错误日志模板
response_log_template
	字符串	长度1-65520	响应日志模板
response_log_error_log_template
	字符串	长度1-65520	响应错误日志模板
响应举例：
[
    {
        "name": "common/log_all",
        "request_log": 1,
       		   "log_source_port": 0,
                "log_source_port_mode": 1,
        "request_log_error_response": 1,
        "request_log_error_close": 1,
        "request_log_error_log_enable": 1,
        "response_log": 1,
        "response_log_error_log_enable": 1,
        "request_log_pool": "syslog",
        "request_log_error_log_pool": "syslog",
        "response_log_pool": "syslog",
        "response_log_error_log_pool": "syslog",
        "request_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME",
        "request_log_error_response_content": "server:nginx",
        "request_log_error_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME",
        "response_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME",
        "response_log_error_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME"
    }
]



请求日志模板获取
Action：slb.profile.request_log.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	请求日志模版名称	是	必须存在
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.request_log.get
请求body:
{
    "name": "log_all"
}


响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	请求日志模板名称
request_log	整数	0,1	请求日志模板开关，0：关闭，1：开启
log_source_port_mode	整数	0,1	日志发送源端口，0：轮询，1：随机
request_log_error_response
	整数	0,1	请求错误响应日志模板开关，0：关闭，1：开启
request_log_error_close	整数	0,1	错误关闭会话开关，0：关闭，1：开启
request_log_error_log_enable
	整数	0,1	错误日志模板开关，0：关闭，1：开启
response_log
	整数	0,1	响应日志模板开关，0：关闭，1：开启
response_log_error_log_enable
	整数	0,1	错误响应日志模板开关，0：关闭，1：开启
request_log_pool
	字符串	1-191	请求日志发送服务池
request_log_error_log_pool
	字符串	1-191	请求错误日志发送服务池
response_log_pool
	字符串	1-191	响应日志发送服务池
response_log_error_log_pool
	字符串	1-191	响应错误日志发送服务池
request_log_template
	字符串	长度1-4095	请求日志发送模板
request_log_error_response_content
	字符串	1-1023	请求错误响应自定义内容
request_log_error_log_template
	字符串	1-4095	请求错误日志模板
response_log_template
	字符串	1-4095	响应日志模板
response_log_error_log_template
	字符串	1-4095	响应错误日志模板
响应举例：
[
    {
        "name": "log_all",
        "request_log": 1,
       		   "log_source_port": 0,
                "log_source_port_mode": 1,
        "request_log_error_response": 1,
        "request_log_error_close": 1,
        "request_log_error_log_enable": 1,
        "response_log": 1,
        "response_log_error_log_enable": 1,
        "request_log_pool": "syslog",
        "request_log_error_log_pool": "syslog",
        "response_log_pool": "syslog",
        "response_log_error_log_pool": "syslog",
        "request_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME",
        "request_log_error_response_content": "server:nginx",
        "request_log_error_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME",
        "response_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME",
        "response_log_error_log_template": "CLIENT_IP:$CLIENT_IP,CLIENT_PORT:$CLIENT_PORT,DATE_D:$DATE_D,DATE_DAY:$DATE_DAY,DATE_DD:$DATE_DD.DATE_DY:$DATE_DY,DATE_HTTP:$DATE_HTTP,DATE_MM:$DATE_MM,DATE_MON:$DATE_MON,DATE_MONTH:$DATE_MONTH,DATE_NCSA$DATE_NCSA,DATE_YY:$DATE_YY,DATE_YYYY:$DATE_YYYY,HTTP_KEEPALIVE:$HTTP_KEEPALIVE,HTTP_METHOD:$HTTP_METHOD,HTTP_PATH:$HTTP_PATH,HTTP_QUERY:$HTTP_QUERY,HTTP_REQUEST:$HTTP_REQUEST,HTTP_URI:$HTTP_URI,HTTP_VERSION:$HTTP_VERSION,TIME_AMPM:$TIME_AMPM,TIME_H12:$TIME_H12,TIME_HRS:$TIME_HRS,TIME_HH12:$TIME_HH12,TIME_HMS:$TIME_HMS,TIME_HH24:$TIME_HH24,TIME_MM:$TIME_MM,TIME_MSECS:$TIME_MSECS,TIME_OFFSET:$TIME_OFFSET,TIME_SS:$TIME_SS,TIME_UNIX:$TIME_UNIX,TIME_USECS:$TIME_USECS,abTIME_ZONE:$TIME_ZONE:$TIME_ZONE,abVIRTUAL_IP:$VIRTUAL_IP,VIRTUAL_NAME:$VIRTUAL_NAME,VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME,VIRTUAL_PORT:$VIRTUAL_PORT,VIRTUAL_SnatPOOL_NAME:$VIRTUAL_SnatPOOL_NAME"
    }

请求日志模板增加
Action：slb.profile.request_log.add
请求参数：


名称	类型	范围	含义
name	字符串	长度1-191	请求日志模板名称
request_log	整数	0,1	请求日志模板开关，0：关闭，1：开启
log_source_port_mode	整数	0,1	日志发送源端口，0：轮询，1：随机
request_log_error_response
	整数	0,1	请求错误响应日志模板开关，0：关闭，1：开启
request_log_error_close	整数	0,1	错误关闭会话开关，0：关闭，1：开启
request_log_error_log_enable
	整数	0,1	错误日志模板开关，0：关闭，1：开启
response_log
	整数	0,1	响应日志模板开关，0：关闭，1：开启
response_log_error_log_enable
	整数	0,1	错误响应日志模板开关，0：关闭，1：开启
request_log_pool
	字符串	1-191	请求日志发送服务池
request_log_error_log_pool
	字符串	1-191	请求错误日志发送服务池
response_log_pool
	字符串	1-191	响应日志发送服务池
response_log_error_log_pool
	字符串	1-191	响应错误日志发送服务池
request_log_template
	字符串	长度1-4095	请求日志发送模板
request_log_error_response_content
	字符串	1-1023	请求错误响应自定义内容
request_log_error_log_template
	字符串	1-4095	请求错误日志模板
response_log_template
	字符串	1-4095	响应日志模板
response_log_error_log_template
	字符串	1-4095	响应错误日志模板

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.request_log.add
请求body:
{
        "name": "request_1",
        "description": "",
        "log_source_port_mode": 0,
        "request_log": 1,
        "request_log_error_response": 0,
        "request_log_error_close": 0,
        "request_log_error_log_enable": 0,
        "response_log": 0,
        "response_log_error_log_enable": 0,
        "request_log_pool": "",
        "request_log_error_log_pool": "",
        "response_log_pool": "",
        "response_log_error_log_pool": "",
        "request_log_template": "ADC_CACHED:$ADC_CACHED===ADC_HOSTNAME:$ADC_HOSTNAME===CLIENT_IP:$CLIENT_IP===CLIENT_PORT:$CLIENT_PORT===DATE_D:$DATE_D===DATE_DAY:$DATE_DAY===DATE_DD:$DATE_DD===DATE_DY:$DATE_DY===DATE_HTTP:$DATE_HTTP===DATE_MM:$DATE_MM===DATE_MON:$DATE_MON===DATE_MONTH:$DATE_MONTH===DATE_NCSA:$DATE_NCSA===DATE_YY:$DATE_YY===DATE_YYYY:$DATE_YYYY===HTTP_KEEPALIVE:$HTTP_KEEPALIVE===HTTP_METHOD:$HTTP_METHOD===HTTP_PATH:$HTTP_PATH===HTTP_QUERY:$HTTP_QUERY===HTTP_REQUEST:$HTTP_REQUEST===HTTP_STATCODE:$HTTP_STATCODE===HTTP_STATUS:$HTTP_STATUS===HTTP_URI:$HTTP_URI===HTTP_VERSION:$HTTP_VERSION===NCSA_COMBINED:$NCSA_COMBINED===NCSA_COMMON:$NCSA_COMMON===RESPONSE_MSECS:$RESPONSE_MSECS===RESPONSE_SIZE:$RESPONSE_SIZE===RESPONSE_USECS:$RESPONSE_USECS===SERVER_IP:$SERVER_IP===SERVER_PORT:$SERVER_PORT===SNAT_IP:$SNAT_IP===SNAT_PORT:$SNAT_PORT===TIME_AMPM:$TIME_AMPM===TIME_H12:$TIME_H12===TIME_HRS:$TIME_HRS===TIME_HH12:$TIME_HH12===TIME_HMS:$TIME_HMS===TIME_HH24:$TIME_HH24===TIME_MM:$TIME_MM===TIME_MSECS:$TIME_MSECS===TIME_OFFSET:$TIME_OFFSET===TIME_SS:$TIME_SS===TIME_UNIX:$TIME_UNIX===TIME_USECS:$TIME_USECS===TIME_ZONE:$TIME_ZONE===VIRTUAL_IP:$VIRTUAL_IP===VIRTUAL_NAME:$VIRTUAL_NAME===VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME===VIRTUAL_PORT:$VIRTUAL_PORT===VIRTUAL_SNATPOOL_NAME:$VIRTUAL_SNATPOOL_NAME===NULL:$NULL===",
        "request_log_error_response_content": "",
        "request_log_error_log_template": "",
        "response_log_template": "",
        "response_log_error_log_template": ""
    }
 
请求日志模板编辑
Action：action=slb.profile.request_log.edit
请求参数：

名称	类型	范围	含义
name	字符串	长度1-191	请求日志模板名称
request_log	整数	0,1	请求日志模板开关，0：关闭，1：开启
log_source_port_mode	整数	0,1	日志发送源端口，0：轮询，1：随机
request_log_error_response
	整数	0,1	请求错误响应日志模板开关，0：关闭，1：开启
request_log_error_close	整数	0,1	错误关闭会话开关，0：关闭，1：开启
request_log_error_log_enable
	整数	0,1	错误日志模板开关，0：关闭，1：开启
response_log
	整数	0,1	响应日志模板开关，0：关闭，1：开启
response_log_error_log_enable
	整数	0,1	错误响应日志模板开关，0：关闭，1：开启
request_log_pool
	字符串	1-191	请求日志发送服务池
request_log_error_log_pool
	字符串	1-191	请求错误日志发送服务池
response_log_pool
	字符串	1-191	响应日志发送服务池
response_log_error_log_pool
	字符串	1-191	响应错误日志发送服务池
request_log_template
	字符串	长度1-4095	请求日志发送模板
request_log_error_response_content
	字符串	1-1023	请求错误响应自定义内容
request_log_error_log_template
	字符串	1-4095	请求错误日志模板
response_log_template
	字符串	1-4095	响应日志模板
response_log_error_log_template
	字符串	1-4095	响应错误日志模板
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.request_log.edit

请求body:
{
        "name": "request_1",
        "description": "",
        "log_source_port_mode": 0,
        "request_log": 1,
        "request_log_error_response": 0,
        "request_log_error_close": 0,
        "request_log_error_log_enable": 0,
        "response_log": 0,
        "response_log_error_log_enable": 0,
        "request_log_pool": "",
        "request_log_error_log_pool": "",
        "response_log_pool": "",
        "response_log_error_log_pool": "",
        "request_log_template": "ADC_CACHED:$ADC_CACHED===ADC_HOSTNAME:$ADC_HOSTNAME===CLIENT_IP:$CLIENT_IP===CLIENT_PORT:$CLIENT_PORT===DATE_D:$DATE_D===DATE_DAY:$DATE_DAY===DATE_DD:$DATE_DD===DATE_DY:$DATE_DY===DATE_HTTP:$DATE_HTTP===DATE_MM:$DATE_MM===DATE_MON:$DATE_MON===DATE_MONTH:$DATE_MONTH===DATE_NCSA:$DATE_NCSA===DATE_YY:$DATE_YY===DATE_YYYY:$DATE_YYYY===HTTP_KEEPALIVE:$HTTP_KEEPALIVE===HTTP_METHOD:$HTTP_METHOD===HTTP_PATH:$HTTP_PATH===HTTP_QUERY:$HTTP_QUERY===HTTP_REQUEST:$HTTP_REQUEST===HTTP_STATCODE:$HTTP_STATCODE===HTTP_STATUS:$HTTP_STATUS===HTTP_URI:$HTTP_URI===HTTP_VERSION:$HTTP_VERSION===NCSA_COMBINED:$NCSA_COMBINED===NCSA_COMMON:$NCSA_COMMON===RESPONSE_MSECS:$RESPONSE_MSECS===RESPONSE_SIZE:$RESPONSE_SIZE===RESPONSE_USECS:$RESPONSE_USECS===SERVER_IP:$SERVER_IP===SERVER_PORT:$SERVER_PORT===SNAT_IP:$SNAT_IP===SNAT_PORT:$SNAT_PORT===TIME_AMPM:$TIME_AMPM===TIME_H12:$TIME_H12===TIME_HRS:$TIME_HRS===TIME_HH12:$TIME_HH12===TIME_HMS:$TIME_HMS===TIME_HH24:$TIME_HH24===TIME_MM:$TIME_MM===TIME_MSECS:$TIME_MSECS===TIME_OFFSET:$TIME_OFFSET===TIME_SS:$TIME_SS===TIME_UNIX:$TIME_UNIX===TIME_USECS:$TIME_USECS===TIME_ZONE:$TIME_ZONE===VIRTUAL_IP:$VIRTUAL_IP===VIRTUAL_NAME:$VIRTUAL_NAME===VIRTUAL_POOL_NAME:$VIRTUAL_POOL_NAME===VIRTUAL_PORT:$VIRTUAL_PORT===VIRTUAL_SNATPOOL_NAME:$VIRTUAL_SNATPOOL_NAME===NULL:$NULL===",
        "request_log_error_response_content": "",
        "request_log_error_log_template": "",
        "response_log_template": "",
        "response_log_error_log_template": ""
    }

请求日志模板删除
Action：slb.profile.request_log.del

请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	服务端SSL卸载模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.profile.request_log.del

请求body:
{
    "name": "request_1"
}




请求日志模板参数
参数	通讯方式
	描述
ADC_CACHED	Response	请求是否命中缓存
ADC_HOSTNAME	Request and Response	设备主机名称
CLIENT_IP	Request and Response	客户端IP地址, 例如, 192.168.1.164
CLIENT_PORT	Request and Response	客户端端口, 例如： 80
DATE_D	Request and Response	日期中的某天，范围1-31
DATE_DAY	Request and Response	全写英文星期
DATE_DD	Request and Response	日期中的某天，范围01-31
DATE_DY	Request and Response	简写英文星期，例如, Mon
DATE_HTTP	Request and Response	HTTP 格式的日期和时间条目，
,  例如：Tue, 5 Apr 2011 02:15:31 UTC .
DATE_MM	Request and Response	日期月份，范围01-12
DATE_MON	Request and Response	月份英文简写，例如：APR

DATE_MONTH	Request and Response	月份英文全写

DATE_NCSA	Request and Response	NCSA 格式的日期时间, 例如, dd/mm/yy:hh:mm:ss ZNE.
DATE_YY	Request and Response	年份, 范围 00-99.
DATE_YYYY	Request and Response	完整年份
HTTP_KEEPALIVE	Request and Response	HTTP1.1 状态

HTTP_METHOD	Request and Response	HTTP请求方法, 例如, GET, PUT, HEAD, POST, DELETE, TRACE, or CONNECT
HTTP_PATH	Request and Response	HTTP 路径

HTTP_QUERY	Request and Response	URL中“?”后的URI
HTTP_REQUEST	Request and Response	完整的请求 $METHOD $URI $VERSION.
HTTP_STATCODE	Response	数字响应状态码，即不包含响应文本的状态响应码

HTTP_STATUS	Response	完整的状态响应
HTTP_URI	Request and Response	HTTP URI
HTTP_VERSION	Request and Response	HTTP version
NCSA_COMBINED	Response	NCSA 组合格式的日志字符串
, 例如, $NCSA_COMMON $Referer ${User-agent} $cookie.
NCSA_COMMON	Response	NCSA 通用格式的日志字符串
, 例如, $CLIENT_IP - - $DATE_NCSA $HTTP_REQUEST $HTTP_STATCODE $RESPONSE_SIZE.
RESPONSE_MSECS	Response	接收请求和发送响应之间经过的时间（以毫秒 
(ms) 为单位）。

RESPONSE_SIZE	Response	响应大小的条目（以字节为单位）。

RESPONSE_USECS	Response	接收请求和发送响应之间经过的时间（以微秒 (µs) 
为单位）
SERVER_IP	Response	向其发送 HTTP 请求的服务池成员的 IP 地址，例如：
10.10.0.1.

SERVER_PORT	Response	HTTP 请求发送到的服务池成员的端口，例如：80.

SNAT_IP	Response	SNAT转换地址， SNAT未启用时输出客户端地址.
SNAT_PORT	Response	SNAT转换端口， SNAT未启用时输出客户端端口  .
TIME_AMPM	Request and Response	12小时格式时间, 例如: AM or PM.
TIME_H12	Request and Response	12小时时间, 范围 1-12
TIME_HRS	Request and Response	12小时时间, 例如:12 AM
TIME_HH12	Request and Response	12小时时间 范围 01-12
TIME_HMS	Request and Response	 H:M:S格式时间, 例如：12:10:49.
TIME_HH24	Request and Response	24小时格式时间 范围00-23
TIME_MM	Request and Response	分钟 范围00-59
TIME_MSECS	Request and Response	请求时间，以毫秒 (ms) 为单位。

TIME_OFFSET	Request and Response	时区，与 GMT 相差小时数，例如： -8

TIME_SS	Request and Response	两位数时间秒 范围00-59
TIME_UNIX	Request and Response	 UNIX 时间戳
TIME_USECS	Request and Response	请求时间分数的条目，以微秒 (µs) 为单位

TIME_ZONE	Request and Response	时区
VIRTUAL_IP	Request and Response	虚拟服务器IP
VIRTUAL_NAME	Request and Response	虚拟服务器名称
VIRTUAL_POOL_NAME	Request and Response	服务池名称
VIRTUAL_PORT	Request and Response	虚拟服务端口
VIRTUAL_SnatPOOL_NAME	Request and Response	虚拟服务端，Snat服务池名称
NULL		输出HTTP LOG未定义参数的header名称，例如:${User-agent}

虚拟服务模板
虚拟服务模板列表
Action: slb.profile.vs.list
请求参数:无
请求举例：
Get
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.vs.list
响应参数：  
名称	类型	范围	含义
name	字符串	长度1-191	虚拟服务模板名称
ignored_tcp_msl	整数	0-1	忽略MSL；0关闭，1开启
reset_unknown_conn	整数	0-1	忽略非法连接；0关闭，1开启
reset_l7_on_failover	整数	0-1	节点选择失败重置；0关闭，1开启
syn_otherflags	整数	0-1	非Syn新建连接；0关闭，1开启
conn_limit_switch	整数	0-1	连接限制；0关闭，1开启
conn_limit	整数	1-8000000	连接数
conn_over_limit_action	整数	0-1	连接数超限重置；0关闭，1开启
log_conn_limit_exceed	整数	0-1	连接数超限日志；0关闭，1开启
conn_rate_limit_switch	整数	0-1	连接速率限制；0关闭，1开启
conn_rate_limit	整数	1-1048575	连接速率值
conn_rate_over_limit_action	整数	0-1	连接速率超限重置；0关闭，1开启
conn_rate_unit	整数	0-1	连接速率计算间隔；0代表second，1代表100ms
log_conn_rate_limit_exceed	整数	0-1	连接速率超限日志；0关闭，1开启
description	字符串
	长度1-191	描述
响应举例：
[
    {
        "name": "pro_vs_1",
        "ignored_tcp_msl": 1,
        "reset_unknown_conn": 1,
       "description": "23",    
        "reset_l7_on_failover": 1,
"description": "23",  
        "syn_otherflags": 1,
        "conn_limit_switch": 1,
        "conn_limit": 8000000,
        "conn_over_limit_action": 1,
        "log_conn_limit_exceed": 1,
        "conn_rate_limit_switch": 1,
        "conn_rate_limit": 1048575,
        "conn_rate_over_limit_action": 1,
        "conn_rate_unit": 0,
        "log_conn_rate_limit_exceed": 1
    }
]



分区获取common和自己分区的虚拟服务模板列表

Action: slb.profile.vs.list.withcommon
请求参数:无
请求举例：
Get
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.vs.list.withcommon
响应参数：  
名称	类型	范围	含义
name	字符串	长度1-191	虚拟服务模板名称
ignored_tcp_msl	整数	0-1	忽略MSL；0关闭，1开启
reset_unknown_conn	整数	0-1	忽略非法连接；0关闭，1开启
reset_l7_on_failover	整数	0-1	节点选择失败重置；0关闭，1开启
syn_otherflags	整数	0-1	非Syn新建连接；0关闭，1开启
conn_limit_switch	整数	0-1	连接限制；0关闭，1开启
conn_limit	整数	1-8000000	连接数
conn_over_limit_action	整数	0-1	连接数超限重置；0关闭，1开启
log_conn_limit_exceed	整数	0-1	连接数超限日志；0关闭，1开启
conn_rate_limit_switch	整数	0-1	连接速率限制；0关闭，1开启
conn_rate_limit	整数	1-1048575	连接速率值
conn_rate_over_limit_action	整数	0-1	连接速率超限重置；0关闭，1开启
conn_rate_unit	整数	0-1	连接速率计算间隔；0代表second，1代表100ms
log_conn_rate_limit_exceed	整数	0-1	连接速率超限日志；0关闭，1开启
description	字符串
	长度1-191	描述
响应举例：
[
    {
        "name": "partition_pro_vs_1",
        "ignored_tcp_msl": 1,
        "reset_unknown_conn": 0,
        "reset_l7_on_failover": 0,
"description": "23",    
        "syn_otherflags": 0,
        "conn_limit_switch": 0,
        "conn_limit": 8000000,
        "conn_over_limit_action": 0,
        "log_conn_limit_exceed": 1,
        "conn_rate_limit_switch": 0,
        "conn_rate_limit": 1048575,
        "conn_rate_over_limit_action": 1,
        "conn_rate_unit": 0,
        "log_conn_rate_limit_exceed": 1
    },
    {
        "name": "common/pro_vs_1",
        "ignored_tcp_msl": 1,
        "reset_unknown_conn": 0,
        "reset_l7_on_failover": 0,
        "syn_otherflags": 0,
        "conn_limit_switch": 0,
        "conn_limit": 8000000,
        "conn_over_limit_action": 0,
        "log_conn_limit_exceed": 1,
        "conn_rate_limit_switch": 0,
        "conn_rate_limit": 1048575,
        "conn_rate_over_limit_action": 1,
        "conn_rate_unit": 0,
        "log_conn_rate_limit_exceed": 1
    }
]
虚拟服务模板获取
Action: slb.profile.vs.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟服务模板名称	是	
请求举例：
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.vs.get
请求Body:
{
    "name": "p1"
}
响应参数：  
名称	类型	范围	含义
name	字符串	长度1-191	虚拟服务模板名称
ignored_tcp_msl	整数	0-1	忽略MSL；0关闭，1开启
reset_unknown_conn	整数	0-1	忽略非法连接；0关闭，1开启
reset_l7_on_failover	整数	0-1	节点选择失败重置；0关闭，1开启
syn_otherflags	整数	0-1	非Syn新建连接；0关闭，1开启
conn_limit_switch	整数	0-1	连接限制；0关闭，1开启
conn_limit	整数	1-8000000	连接数
conn_over_limit_action	整数	0-1	连接数超限重置；0关闭，1开启
log_conn_limit_exceed	整数	0-1	连接数超限日志；0关闭，1开启
conn_rate_limit_switch	整数	0-1	连接速率限制；0关闭，1开启
conn_rate_limit	整数	1-1048575	连接速率值
conn_rate_over_limit_action	整数	0-1	连接速率超限重置；0关闭，1开启
conn_rate_unit	整数	0-1	连接速率计算间隔；0代表second，1代表100ms
log_conn_rate_limit_exceed	整数	0-1	连接速率超限日志；0关闭，1开启
description	字符串
	长度1-191	描述

响应举例：
{
        "name": "p1",
        "ignored_tcp_msl": 1,
        "reset_unknown_conn": 1,
        "reset_l7_on_failover": 1,
"description": "23",  
        "syn_otherflags": 1,
        "conn_limit_switch": 1,
        "conn_limit": 8000000,
        "conn_over_limit_action": 1,
        "log_conn_limit_exceed": 1,
        "conn_rate_limit_switch": 1,
        "conn_rate_limit": 1048575,
        "conn_rate_over_limit_action": 1,
        "conn_rate_unit": 0,
        "log_conn_rate_limit_exceed": 1
  }
虚拟服务模板增加
Action: slb.profile.vs.add
请求参数
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟服务模板名称	是	
ignored_tcp_msl	整数	0-1	忽略MSL；0关闭，1开启	是	0关闭，1开启
reset_unknown_conn	整数	0-1	忽略非法连接；0关闭，1开启	是	0关闭，1开启
reset_l7_on_failover	整数	0-1	节点选择失败重置；0关闭，1开启	是	0关闭，1开启
syn_otherflags	整数	0-1	非Syn新建连接；0关闭，1开启	是	0关闭，1开启
conn_limit_switch	整数	0-1	连接限制；0关闭，1开启	是	0关闭，1开启
conn_limit	整数	1-8000000	连接数	是	
conn_over_limit_action	整数	0-1	连接数超限重置；0关闭，1开启	是	0关闭，1开启
log_conn_limit_exceed	整数	0-1	连接数超限日志；0关闭，1开启	是	0关闭，1开启
conn_rate_limit_switch	整数	0-1	连接速率限制；0关闭，1开启	是	0关闭，1开启
conn_rate_limit	整数	1-1048575	连接速率值	是	
conn_rate_over_limit_action	整数	0-1	连接速率超限重置；0关闭，1开启	是	0关闭，1开启
conn_rate_unit	整数	0-1	连接速率计算间隔；0代表second，1代表100ms	是	0代表second，1代表100ms
log_conn_rate_limit_exceed	整数	0-1	连接速率超限日志；0关闭，1开启	是	0关闭，1开启
description	字符串
	长度1-191	描述	否
	
请求举例
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.vs.add
请求body：
{
        "name": "p1",
        "ignored_tcp_msl": 1,
        "reset_unknown_conn": 1,
        "reset_l7_on_failover": 1,
        "syn_otherflags": 1,
        "conn_limit_switch": 1,
        "conn_limit": 8000000,
        "conn_over_limit_action": 1,
        "log_conn_limit_exceed": 1,
        "conn_rate_limit_switch": 1,
        "conn_rate_limit": 1048575,
        "conn_rate_over_limit_action": 1,
        "conn_rate_unit": 1,
        "log_conn_rate_limit_exceed": 1
  }
虚拟服务模板编辑
Action:  slb.profile.vs.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟服务模板名称	是	
ignored_tcp_msl	整数	0-1	忽略msl；0关闭，1开启	是	0关闭，1开启
reset_unknown_conn	整数	0-1	忽略非法连接；0关闭，1开启	是	0关闭，1开启
reset_l7_on_failover	整数	0-1	节点选择失败重置；0关闭，1开启	是	0关闭，1开启
syn_otherflags	整数	0-1	非syn新建连接；0关闭，1开启	是	0关闭，1开启
conn_limit_switch	整数	0-1	连接限制；0关闭，1开启	是	0关闭，1开启
conn_limit	整数	1-8000000	连接数	是	
conn_over_limit_action	整数	0-1	连接数超限重置；0关闭，1开启	是	0关闭，1开启
log_conn_limit_exceed	整数	0-1	连接数超限日志；0关闭，1开启	是	0关闭，1开启
conn_rate_limit_switch	整数	0-1	连接速率限制；0关闭，1开启	是	0关闭，1开启
conn_rate_limit	整数	1-1048575	连接速率值	是	
conn_rate_over_limit_action	整数	0-1	连接速率超限重置；0关闭，1开启	是	0关闭，1开启
conn_rate_unit	整数	0-1	连接速率计算间隔；0代表second，1代表100ms	是	0代表second，1代表100ms
log_conn_rate_limit_exceed	整数	0-1	连接速率超限日志；0关闭，1开启	是	0关闭，1开启
description	字符串
	长度1-191	描述	否
	
请求举例：
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.vs.edit
请求body：
{
        "name": "p1",
        "ignored_tcp_msl": 1,
        "reset_unknown_conn": 1,
        "reset_l7_on_failover": 1,
        "syn_otherflags": 1,
        "conn_limit_switch": 1,
        "conn_limit": 6000000,
        "conn_over_limit_action": 1,
        "log_conn_limit_exceed": 1,
        "conn_rate_limit_switch": 1,
        "conn_rate_limit": 1048575,
        "conn_rate_over_limit_action": 1,
        "conn_rate_unit": 1,
        "log_conn_rate_limit_exceed": 1
 }

虚拟服务模板删除
Action: slb.profile.vs.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	虚拟服务模板名称	是	
请求举例：
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.vs.del
请求body：
{
    "name": "p1"
}

NAT日志模板
NAT日志模板列表
Action: slb.profile.natlog.list
请求参数:无
请求举例：
Get
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.natlog.list
响应参数： 
名称	类型	范围	含义
name	字符串	长度1-191	nat日志模板名称
pool	整数	0-1	服务器地址为服务池类型
host	ipv4/ipv6地址	0-1	服务器地址为主机类型
facility	整数	0-1	类别
  1.kernel  2.user   3.mail    
  4.daemon  5.authorization         
  6.syslog  7.line-printer          
  8.news    9.uucp  10.cron                   
  11.private-authorization  
  12.ftp   13.0ntp 14.audit                 
  15.alert 16.clock 17.local0                 
  18.local1  19.local2   20.local3                 
  21.local5  22.local6   23.local7                 
severity	整数	0-1	级别
  emergency  0: Emergency
  alert      1: Alert
  crit       2: Critical
  error      3: Error
  warning    4: Warning
  notice     5: Notice
  info       6: Informational
  debugging  7: Debugging
src_port	整数	1-65535	源端口 1-65535 any:使用任何端口
enable_local_record	整数	0-1	0:关闭本地记录 1：开启本地记录
dst_port	整数	1-65535	目的端口
inc_dst	整数	0-1	包含虚拟服务 0:不包含 1:包含
inc_lip_lport	整数	0-1	包含服务器成员 0:不包含 1:包含
log-type	整数	1-1048575	日志类型 1:会话连接删除2.会话连接
 
响应举例：
  [
    {
        "name": "ftp",
        "pool": "",
        "host": "",
        "facility": 14,
        "severity": 4,
        "src_port": 514,
        "enable_local_record": 1,
        "dst_port": 514,
        "inc_dst": 1,
        "inc_lip_lport": 1,
        "log_type": 2
    }
]
partition分区获取common分区nat日志模板列表
Action: slb.profile.natlog.list.withcommon
请求参数:无
请求举例：
Get
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.natlog.list.withcommon
响应参数： 
名称	类型	范围	含义
name	字符串	长度1-191	nat日志模板名称
pool	整数	0-1	服务器地址为服务池类型
host	ipv4/ipv6地址	0-1	服务器地址为主机类型
facility	整数	0-1	类别
  1.kernel  2.user   3.mail    
  4.daemon  5.authorization         
  6.syslog  7.line-printer          
  8.news    9.uucp  10.cron                   
  11.private-authorization  
  12.ftp   13.0ntp 14.audit                 
  15.alert 16.clock 17.local0                 
  18.local1  19.local2   20.local3                 
  21.local5  22.local6   23.local7                 
severity	整数	0-1	级别
  emergency  0: Emergency
  alert      1: Alert
  crit       2: Critical
  error      3: Error
  warning    4: Warning
  notice     5: Notice
  info       6: Informational
  debugging  7: Debugging
Src-port	整数	1-65535	源端口 1-65535 any:使用任何端口
Enable-local-record	整数	0-1	0:关闭本地记录 1：开启本地记录
Dst-port	整数	1-65535	目的端口
inc-dst	整数	0-1	包含虚拟服务 0:不包含 1:包含
inc_lip_lport	整数	0-1	包含服务器成员 0:不包含 1:包含
Log-type	整数	1-1048575	日志类型 1:会话连接删除2.会话连接
 
响应举例：
  [
    {
        "name": "ftp",
        "pool": "",
        "host": "",
        "facility": 14,
        "severity": 4,
        "src_port": 514,
        "enable_local_record": 1,
        "dst_port": 514,
        "inc_dst": 1,
        "inc_lip_lport": 1,
        "log_type": 2
},
 {
        "name": "common/11",
        "pool": "",
        "host": "",
        "facility": 16,
        "severity": 7,
        "src_port": 514,
        "enable_local_record": 0,
        "dst_port": 514,
        "inc_dst": 1,
        "inc_lip_lport": 1,
        "log_type": 2
    },
]


NAT日志模板获取
Action: slb.profile.natlog.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	nat日志模板名称	是	 
请求举例：
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.natlog.get
请求Body:
{
    "name": "default"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	nat日志模板名称
pool	整数	0-1	服务器地址为服务池类型
host	ipv4/ipv6地址	0-1	服务器地址为主机类型
facility	整数	0-1	类别
  1.kernel  2.user   3.mail    
  4.daemon  5.authorization         
  6.syslog  7.line-printer          
  8.news    9.uucp  10.cron                   
  11.private-authorization  
  12.ftp   13.0ntp 14.audit                 
  15.alert 16.clock 17.local0                 
  18.local1  19.local2   20.local3                 
  21.local5  22.local6   23.local7                 
severity	整数	0-1	级别
  emergency  0: Emergency
  alert      1: Alert
  crit       2: Critical
  error      3: Error
  warning    4: Warning
  notice     5: Notice
  info       6: Informational
  debugging  7: Debugging
Src_port	整数	1-65535	源端口 1-65535 any:使用任何端口
Enable_local_record	整数	0-1	0:关闭本地记录 1：开启本地记录
Dst_port	整数	1-65535	目的端口
Inc_dst	整数	0-1	包含虚拟服务 0:不包含 1:包含
inc_lip_lport	整数	0-1	包含服务器成员 0:不包含 1:包含
Log_type	整数	1-1048575	日志类型 1:会话连接删除2.会话连接
  
响应举例：
{
    "name": "default",
    "pool": "",
    "host": "66.2.2.88",
    "facility": 10,
    "severity": 3,
    "src_port": 514,
    "enable_local_record": 1,
    "dst_port": 514,
    "inc_dst": 1,
    "inc_lip_lport": 1,
    "log_type": 2
}

NAT日志模板增加
Action: slb.profile.natlog.add
请求参数

名称	类型	范围	含义
name	字符串	长度1-191	nat日志模板名称
pool	整数	0-1	服务器地址为服务池类型
host	ipv4/ipv6地址	0-1	服务器地址为主机类型
facility	整数	0-1	类别
  1.kernel  2.user   3.mail    
  4.daemon  5.authorization         
  6.syslog  7.line-printer          
  8.news    9.uucp  10.cron                   
  11.private-authorization  
  12.ftp   13.0ntp 14.audit                 
  15.alert 16.clock 17.local0                 
  18.local1  19.local2   20.local3                 
  21.local5  22.local6   23.local7                 
severity	整数	0-1	级别
  emergency  0: Emergency
  alert      1: Alert
  crit       2: Critical
  error      3: Error
  warning    4: Warning
  notice     5: Notice
  info       6: Informational
  debugging  7: Debugging
src_port	整数	1-65535	源端口 1-65535 any:使用任何端口
enable_local_record	整数	0-1	0:关闭本地记录 1：开启本地记录
dst_port	整数	1-65535	目的端口
inc_dst	整数	0-1	包含虚拟服务 0:不包含 1:包含
inc_lip_lport	整数	0-1	包含服务器成员 0:不包含 1:包含
log-type	整数	1-1048575	日志类型 1:会话连接删除2.会话连接

POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.natlog.add
请求body：
{
              "name": "nat-log",
              "pool": "",
              "host": "152.1.1.100",
              "facility": 16,
              "severity": 7,
              "src_port": 514,
              "enable_local_record": 1,
              "dst_port": 514,
              "inc_dst": 1,
              "inc_lip_lport": 1,
              "log_type": 2
       }

NAT日志模板编辑
Action: slb.profile.natlog.edit
请求参数：
名称	类型	范围	含义
name	字符串	长度1-191	nat日志模板名称
pool	整数	0-1	服务器地址为服务池类型
host	ipv4/ipv6地址	0-1	服务器地址为主机类型
facility	整数	0-1	类别
  1.kernel  2.user   3.mail    
  4.daemon  5.authorization         
  6.syslog  7.line-printer          
  8.news    9.uucp  10.cron                   
  11.private-authorization  
  12.ftp   13.0ntp 14.audit                 
  15.alert 16.clock 17.local0                 
  18.local1  19.local2   20.local3                 
  21.local5  22.local6   23.local7                 
severity	整数	0-1	级别
  emergency  0: Emergency
  alert      1: Alert
  crit       2: Critical
  error      3: Error
  warning    4: Warning
  notice     5: Notice
  info       6: Informational
  debugging  7: Debugging
src_port	整数	1-65535	源端口 1-65535 any:使用任何端口
enable_local_record	整数	0-1	0:关闭本地记录 1：开启本地记录
dst_port	整数	1-65535	目的端口
inc_dst	整数	0-1	包含虚拟服务 0:不包含 1:包含
inc_lip_lport	整数	0-1	包含服务器成员 0:不包含 1:包含
log-type	整数	1-1048575	日志类型 1:会话连接删除2.会话连接
请求举例：
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.natlog.edit
请求body：
 {
              "name": "nat-log",
              "pool": "",
              "host": "152.1.1.10",
              "facility": 16,
              "severity": 7,
              "src_port": 514,
              "enable_local_record": 1,
              "dst_port": 514,
              "inc_dst": 1,
              "inc_lip_lport": 1,
              "log_type": 2
       }
NAT日志模板删除
nat日志模板删除
Action: slb.profile.natlog.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	nat模板名称	是	 
请求举例：
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.natlog.del
请求body：
{
	"name": "nat-log"
}
DNS日志模板
DNS日志模板列表
Action: slb.profile.dnslog.list
请求参数:无
请求举例：
Get
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.dnslog.list
响应参数： 
名称	类型	范围	含义
name	字符串	长度1-191	dns日志模板名称
description	字符串	长度1-191	描述
pool	字符串	长度1-191	服务器地址为服务池类型时服务池名称
host	ipv4/ipv6地址	不涉及	服务器地址为主机类型时主机地址
facility	整数	0-23	类别
  0:kernel  1:user   2:mail    
  3:daemon  4:authorization         
  5:syslog  6:line-printer          
  7:news    8:uucp  9:cron                   
  10:private-authorization  
  11:ftp   12:ntp 13:audit                 
  14:alert 15:clock 16:local0                 
  17:local1  18:local2   19:local3                 
  20:local4 21:local5 22:local6  23:local7               
severity	整数	0-7	级别
  emergency  0: Emergency
  alert      1: Alert
  crit       2: Critical
  error      3: Error
  warning    4: Warning
  notice     5: Notice
  info       6: Informational
  debugging  7: Debugging
src-port	整数	0-65535	源端口， 0:即any，使用任意端口
enable_local_record	整数	0-1	0:关闭本地记录 1：开启本地记录
dst_port	整数	1-65535	目的端口
query	整数	0-1	dns请求 0:不包含 1:包含
response	整数	0-1	dns响应 0:不包含 1:包含
 
响应举例：
[
{
    		"name": "dnslog",
    		"description": "",
    		"pool": "",
    		"host": "3.6.6.6",
    		"facility": 16,
    		"severity": 7,
    		"src_port": 514,
    		"enable_local_record": 1,
    		"dst_port": 514,
    		"query": 1,
    		"response": 1
}
]

分区获取common中DNS日志模板列表
Action: slb.profile.dnslog.list.withcommon
请求参数:无
请求举例：
Get
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.dnslog.list.withcommon
响应参数： 
名称	类型	范围	含义
name	字符串	长度1-191	dns日志模板名称
description	字符串	长度1-191	描述
pool	字符串	长度1-191	服务器地址为服务池类型时服务池名称
host	ipv4/ipv6地址	不涉及	服务器地址为主机类型时主机地址
facility	整数	0-23	类别
  0:kernel  1:user   2:mail    
  3:daemon  4:authorization         
  5:syslog  6:line-printer          
  7:news    8:uucp  9:cron                   
  10:private-authorization  
  11:ftp   12:ntp 13:audit                 
  14:alert 15:clock 16:local0                 
  17:local1  18:local2   19:local3                 
  20:local4 21:local5 22:local6  23:local7               
severity	整数	0-7	级别
  emergency  0: Emergency
  alert      1: Alert
  crit       2: Critical
  error      3: Error
  warning    4: Warning
  notice     5: Notice
  info       6: Informational
  debugging  7: Debugging
src-port	整数	0-65535	源端口， 0:即any，使用任意端口
enable_local_record	整数	0-1	0:关闭本地记录 1：开启本地记录
dst_port	整数	1-65535	目的端口
query	整数	0-1	dns请求 0:不包含 1:包含
response	整数	0-1	dns响应 0:不包含 1:包含

响应举例：
[
    {
        "name": "net_dnslog",
        "description": "",
        "pool": "",
        "host": "10.3.3.3",
        "facility": 16,
        "severity": 7,
        "src_port": 514,
        "enable_local_record": 0,
        "dst_port": 514,
        "query": 1,
        "response": 1
    },
    {
        "name": "common/dnslog",
        "description": "",
        "pool": "",
        "host": "3.6.6.6",
        "facility": 16,
        "severity": 7,
        "src_port": 514,
        "enable_local_record": 1,
        "dst_port": 514,
        "query": 1,
        "response": 1
    }
]
DNS日志模板获取
Action: slb.profile.dnslog.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	dns模板名称	是	

请求举例：
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.dnslog.get
请求Body:
{
    "name": "dnslog"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	DNS日志模板名称
description	字符串	长度1-191	描述
pool	字符串	长度1-191	服务器地址为服务池类型时服务池名称
host	ipv4/ipv6地址	不涉及	服务器地址为主机类型时主机地址
facility	整数	0-23	类别
  0:kernel  1:user   2:mail    
  3:daemon  4:authorization         
  5:syslog  6:line-printer          
  7:news    8:uucp  9:cron                   
  10:private-authorization  
  11:ftp   12:ntp 13:audit                 
  14:alert 15:clock 16:local0                 
  17:local1  18:local2   19:local3                 
  20:local4 21:local5 22:local6  23:local7               
severity	整数	0-7	级别
  emergency  0: Emergency
  alert      1: Alert
  crit       2: Critical
  error      3: Error
  warning    4: Warning
  notice     5: Notice
  info       6: Informational
  debugging  7: Debugging
src-port	整数	0-65535	源端口，0:即any，使用任意端口
enable_local_record	整数	0-1	0:关闭本地记录 1：开启本地记录
dst_port	整数	1-65535	目的端口
query	整数	0-1	dns请求 0:不包含 1:包含
response	整数	0-1	dns响应 0:不包含 1:包含
 
响应举例：
{
    "name": "dnslog",
    "description": "",
    "pool": "",
    "host": "3.6.6.6",
    "facility": 16,
    "severity": 7,
    "src_port": 514,
    "enable_local_record": 1,
    "dst_port": 514,
    "query": 1,
    "response": 1
}
DNS日志模板增加
Action: slb.profile.dnslog.add
请求参数
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	DNS日志模板名称	是	
description	字符串	长度1-191	描述	否	
pool	字符串	长度1-191	服务器地址为服务池类型时服务池名称	是	不能与host一起配置
host	IPV4/IPV6地址	不涉及	服务器地址为主机类型时主机地址	是	不能与pool一起配置
facility	整数	0-23	类别
             	否	0:kernel 1:user 2:mail    
3:daemon 4:authorization         
5:syslog 6:line-printer          
7:news   8:uucp  9:cron                   
10:private-authorization  
11:ftp   12:ntp 13:audit                 
14:alert 15:clock 16:local0            17:local1 18:local2   19:local3                 
20:local4 21:local5 22:local6 23:local7 ；
缺省值为16  
severity	整数	0-7	级别	否	emergency  0: Emergency
alert      1: Alert
crit       2: Critical
error      3: Error
warning    4: Warning
notice     5: Notice
info     6: Informational
debugging 7: Debugging ；
缺省值为7 
src-port	整数	0-65535	源端口，0:即any，使用任意端口	否	缺省值为514
enable_local_record	整数	0-1	0:关闭本地记录 1：开启本地记录	否	缺省值为0
dst_port	整数	1-65535	目的端口	否	缺省值为514
query	整数	0-1	dns请求 0:不包含 1:包含	否	缺省值为1
response	整数	0-1	dns响应 0:不包含 1:包含	否	缺省值为1

请求举例
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.dnslog.add
请求body：
{
    "name": "dnslog",
    "description": "",
    "pool": "",
    "host": "3.6.6.6",
    "facility": 16,
    "severity": 7,
    "src_port": 514,
    "enable_local_record": 1,
    "dst_port": 514,
    "query": 1,
    "response": 1
}

DNS日志模板编辑
Action: slb.profile.dnslog.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	DNS日志模板名称	是	
description	字符串	长度1-191	描述	否	
pool	字符串	长度1-191	服务器地址为服务池类型时服务池名称	是	不能与host一起配置
host	IPV4/IPV6地址	不涉及	服务器地址为主机类型时主机地址	是	不能与pool一起配置
facility	整数	0-23	类别
             	否	0:kernel 1:user 2:mail    
3:daemon 4:authorization         
5:syslog 6:line-printer          
7:news   8:uucp  9:cron                   
10:private-authorization  
11:ftp   12:ntp 13:audit                 
14:alert 15:clock 16:local0            17:local1 18:local2   19:local3                 
20:local4 21:local5 22:local6 23:local7 ；
缺省值为16  
severity	整数	0-7	级别	否	emergency  0: Emergency
alert      1: Alert
crit       2: Critical
error      3: Error
warning    4: Warning
notice     5: Notice
info     6: Informational
debugging 7: Debugging ；
缺省值为7 
src-port	整数	0-65535	源端口，0:即any，使用任意端口	否	缺省值为514
enable_local_record	整数	0-1	0:关闭本地记录 1：开启本地记录	否	缺省值为0
dst_port	整数	1-65535	目的端口	否	缺省值为514
query	整数	0-1	dns请求 0:不包含 1:包含	否	缺省值为1
response	整数	0-1	dns响应 0:不包含 1:包含	否	缺省值为1

请求举例：
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.dnslog.edit
请求body：
{
    "name": "dnslog",
    "description": "",
    "pool": "",
    "host": "3.6.6.6",
    "facility": 16,
    "severity": 7,
    "src_port": 514,
    "enable_local_record": 1,
    "dst_port": 514,
    "query": 1,
    "response": 1
}

DNS日志模板删除
Action: slb.profile.dnslog.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模板名称	是	
请求举例：
POST
http://10.2.120.21/adcapi/v2.0/?authkey=1021a0c521314f602f77749a662a0b&action=slb.profile.dnslog.del
请求body：
{
	"name": "dnslog"
}


健康检查
健康检查添加
Action:  slb.healthcheck.add
公共请求参数:所有种类的健康检查都具有的参数,后续各种健康检查不再列举这些参数
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	健康检查名称	是	唯一
retry	整数	一般健康检查：1-5
pro类型：0	重试次数	否	缺省值：3
pro类型必须为0
interval	整数	1-180	间隔时间,单位秒	否	缺省值：5
timeout	整数	一般健康检查：1-12
pro类型：1-1800	超时时间,单位秒	否	缺省值：5
pro类型的值必须大于interval
type	字符串		健康检查类型，	否	缺省值：icmp
支持字段:
icmp:icmp健康检查
http:http康检查
http-pro:http-pro健康检查
arp:arp健康检查
database:数据库健康检查
dns:dns健康检查
ftp:ftp健康检查
https:https健康检查
imap:imap健康检查
ladp:ladp健康检查
ntp:ntp健康检查
pop3:pop3健康检查
radius:rudius健康检查
rtsp:rtsp健康检查
sip:sip健康检查
smtp:smtp健康检查
snmp:snmp健康检查
tcp:tcp健康检查
tcp-pro:tcp-pro健康检查
udp:udpP健康检查
udp-pro:udp-pro健康检查
script:自定义脚本健康检查
combo:组合健康检查
auto_disable	整数	0,1	自动禁用	否	未配置此项时,获取配置也无此项；0不开启，1开启。缺省值：0
alias_ipv4_src	ipv4地址	不涉及	源地址,指定该参数后,检查时以该地址作为源地址	否	未配置此项时,获取配置也无此项；缺省值：无
alias_ipv6_src	ipv6地址	不涉及	源地址,指定该参数后,检查时以该地址作为源地址	否	未配置此项时,获取配置也无此项；缺省值：无
interface	字符串	不涉及	源接口,指定该参数后,检查时以该接口作为出接口	否	未配置此项时,获取配置也无此项；缺省值：无
alias_ipv4	ipv4地址	不涉及	ipv4地址别名,指定该参数后,检查时以该地址作为目的地址	否	未配置此项时,获取配置也无此项；缺省值：无
alias_ipv6	ipv6地址	不涉及	ipv6地址别名,指定该参数后,检查时以该地址作为目的地址	否	未配置此项时,获取配置也无此项；缺省值：无
alias_port	整数	1-65535	端口别名, 指定该参数后,检查时以该端口作为目的端口	否	未配置此项时,获取配置也无此项；
仅对TCP/UDP协议或基于TCP/UDP之上的协议有效
缺省值：无
port	整数	1-65535	在关联到节点时,使用该端口作为目的端口检查,其他情况使用关联的端口做检查	否	仅对TCP/UDP协议或基于TCP/UDP之上的协议有效
缺省值:各应用协议的默认端口
up_check_cnt	整数	1-10	对应命令行的up-check-cnt，表示检测对象up前最少检测成功的个数	否	默认参数为1，即只要有一次健康检查成功，就认为检查对象是up的
wait_all_retry	整数	0,1	对应命令行的wait-all-retry，表示等待所有的retry尝试次数都失败了，才会将检测对象标记为down	否	默认为0：表示不开启，1：表示开启
http_version	字符串	HTTP 0.9，HTTP 1.0，HTTP 1.1	健康检查算法为http、http-pro、https时使用的http的版本	否	默认值：HTTP 1.1；
HTTP 1.0：http版本为1.0；
HTTP 0.9：http版本为0.9；

由于各种类型的健康检查支持的参数不一样,下面分类型说明：
ICMP健康检查添加
Action:  slb.healthcheck.add
请求参数:
名称	类型	范围	含义	必选	备注
description	字符串
	长度1-191	描述	否	
mode	字符串	Transparent	表明设备是属于透明模式下	否	
icmp_alias_addr	ipv4地址	不涉及	透明模式下健康检查的目的地址	否	
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "ping1",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "interface": "ve158",
    "alias_ipv4": "2.2.2.2",
    "alias_ipv6": "3000::1",
    "description": "icmp",
    "type": "icmp",
    "mode": "transparent",
    "icmp_alias_addr": "2.2.2.2"
}
HTTP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	http	对于http健康检查类型，固定为http	是	
host	字符串	长度1-63	http 头部host字段	否	缺省值:自动
url	字符串	长度1-127	请求方法和url
	否	请求方法支持GET/POST
缺省值: GET /
post_data	字符串	长度1-255	发送body，当url中方法为POST时有效，和post_data两者只能配置一个	否	缺省值:空
post_file	字符串	长度1-31	发送body文件名，当url中方法为POST时有效，和post_data两者只能配置一个	否	缺省值:空
username	字符串	长度1-31	认证用户名,当http需要登录认证时使用	否	缺省值:空
password	字符串	长度1-31	认证密码,当http需要登录认证时使用	否	缺省值:空
code	字符串	长度1-31	http返回码,code和pattern 只能使用一个	否	格式为100-899之间的数字组成的字符串,可以使用逗号(,)或者连接符(-)连接；缺省值:200
pattern	字符串	长度1-255	接收字符串,code和pattern 只能使用一个	否	缺省值:空
pattern_disable_str	字符串	长度1-256	接收禁用字符串，没有收到pattern 字符串但是收到该字符串之后，对健康检查目标执行软关机操作。必须配合pattern 参数使用	否	缺省值:空
server_fail_code	字符串	长度1-31	进入维护模式的响应码	否	格式为100-899之间的数字组成的字符串,可以使用逗号(,)或者连接符(-)连接；添加时缺省为空，
编辑时缺省不修改
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
http_version	字符串	HTTP 0.9，HTTP 1.0，HTTP 1.1	健康检查的http的版本	否	默认值：HTTP 1.1
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "http",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "interface": "Ethernet 0/1",
    "alias_ipv4": "1.2.3.4",
    "alias_port": 889,
    "alias_ipv6": "2001::1",
    "type": "http",
    "port": 80,
    "host": "ahost",
    "url": "POST /index",
    "post_data": "mybodystring",
    "trans_mode": 0,
    "username": "username",
    "password": "pass",
    "code": "202"
}
HTTP2健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	http	对于http健康检查类型，固定为http	是	
host	字符串	长度1-63	http 头部host字段	否	缺省值:自动
url	字符串	长度1-127	请求方法和url
	否	请求方法支持GET/POST
缺省值: GET /
post_data	字符串	长度1-255	发送body，当url中方法为POST时有效，和post_data两者只能配置一个	否	缺省值:空
post_file	字符串	长度1-31	发送body文件名，当url中方法为POST时有效，和post_data两者只能配置一个	否	缺省值:空
username	字符串	长度1-31	认证用户名,当http需要登录认证时使用	否	缺省值:空
password	字符串	长度1-31	认证密码,当http需要登录认证时使用	否	缺省值:空
code	字符串	长度1-31	http返回码,code和pattern 只能使用一个	否	格式为100-899之间的数字组成的字符串,可以使用逗号(,)或者连接符(-)连接；缺省值:200
pattern	字符串	长度1-255	接收字符串,code和pattern 只能使用一个	否	缺省值:空
pattern_disable_str	字符串	长度1-256	接收禁用字符串，没有收到pattern 字符串但是收到该字符串之后，对健康检查目标执行软关机操作。必须配合pattern 参数使用	否	缺省值:空
server_fail_code	字符串	长度1-31	进入维护模式的响应码	否	格式为100-899之间的数字组成的字符串,可以使用逗号(,)或者连接符(-)连接；添加时缺省为空，
编辑时缺省不修改
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
auto_disable	整数	0，1	自动禁用开关	否	缺省：关闭
alias_ipv4_src	字符串	不涉及	健康检查源地址	否	缺省值:空
interface	字符	不涉及	健康检查接口	否	
alias_ipv4	字符	不涉及	别名地址ipv4	否	缺省值:空
alias_ipv6	字符	不涉及	别名地址ipv6	否	缺省值:空
alias_port	整数	1-65535	别名端口	否	缺省值:空
contenttype	字符串	不涉及	post文本类型	否	
retry	整数	0-5	重试次数	否	缺省值：3
interval	整数	1-180	检查间隔	否	缺省值：5
timeout	整数	1-1800	检查超时时间	否	缺省值：5
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "http2-test",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 0,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "trans_mode": 0,
   "alias_ipv4_src": "6.156.1.31",
   "alias_ipv6_src": "3000:6:156:1::31",
    "interface": "Ethernet2/0",
    "alias_ipv4": "1.2.3.4",
    "alias_ipv6": "2001::1",
    "alias_port": 889,
    "type": "http2",
    "port": 80,
    "host": "ahost",
    "url": "POST /index",
    "post_data": "mybodystring",
    "contenttype": "x-www-form-urlencoded",
    "pattern": "str1",
    "pattern_disable_str": "str2"
}

HTTP-PRO健康检查添加
Action:  slb.healthcheck-pro.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	http-pro	对于http健康检查类型，固定为http-pro	是	
retry	整数	Pro类型：0	重试次数	是	pro类型必须设为0
interval	整数	1-180	间隔时间,单位秒	是	缺省值：5
timeout	整数	Pro类型：1-1800	超时时间,单位秒	是	缺省值：5
pro类型的值必须大于interval
host	字符串	长度1-63	http头部host字段	否	缺省值:自动
url	字符串	长度1-127	请求方法和url
	否	请求方法支持GET/POST
缺省值: GET /
post_data	字符串	长度1-255	发送body，当url中方法为post时有效，和post_data两者只能配置一个	否	缺省值:空
post_file	字符串	长度1-31	发送body文件名，当url中方法为POST时有效，和post_data两者只能配置一个	否	缺省值:空
code	字符串	长度1-31	http返回码,code和pattern 只能使用一个	否	格式为100-899之间的数字组成的字符串,可以使用逗号(,)或者连接符(-)连接；缺省值:200
pattern	字符串	长度1-255	接收字符串,code和pattern 只能使用一个	否	缺省值:空
pattern_disable_str	字符串	长度1-256	接收禁用字符串，没有收到pattern 字符串但是收到该字符串之后，对健康检查目标执行软关机操作。必须配合pattern 参数使用	否	缺省值:空
server_fail_code	字符串	长度1-31	进入维护模式的响应码	否	格式为100-899之间的数字组成的字符串,可以使用逗号(,)或者连接符(-)连接；添加时缺省为空，
编辑时缺省不修改
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
auto_disable	整数	0，1	自动禁用开关	否	缺省：关闭
alias_ipv4_src	字符串	不涉及	健康检查源地址	否	缺省值:空
interface	字符	不涉及	健康检查接口	否	
alias_ipv4	字符	不涉及	别名地址ipv4	否	缺省值:空
alias_ipv6	字符	不涉及	别名地址ipv6	否	缺省值:空
alias_port	整数	1-65535	别名端口	否	缺省值:空
contenttype	字符串	不涉及	post文本类型	否	
retry	整数	0-5	重试次数	否	缺省值：3
interval	整数	1-180	检查间隔	否	缺省值：5
timeout	整数	1-1800	检查超时时间	否	缺省值：16
http_version	字符串	HTTP 0.9，HTTP 1.0，HTTP 1.1	健康检查时使用的http的版本	否	默认值：HTTP 1.1；
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "httppro-test",
    "retry": 0,
    "up_check_cnt": 1,
    "wait_all_retry": 0,
    "interval": 5,
    "timeout": 6,
    "auto_disable": 0,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
   "alias_ipv6_src": "3000:6:156:1::31",
    "interface": "Ethernet2/0",
    "alias_ipv4": "1.2.3.4",
    "alias_ipv6": "2001::1",
    "alias_port": 889,
    "type": "http-pro",
    "port": 80,
    "host": "ahost",
    "url": "POST /index",
    "post_data": "mybodystring",
    "contenttype": "x-www-form-urlencoded",
    "pattern": "str1",
    "pattern_disable_str": "str2",
    "server_fail_code": "502"
}
ARP健康检查添加

Action:  slb.healthcheck.add
请求参数:
名称	类型	范围	含义	必选	备注
type	字符串	arp	对于arp健康检查类型，固定为arp	是	
description	字符串
	长度1-191	描述	否	

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "arp",
    "type": "arp"
}

数据库健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	arp	检查类型	是	对于arp健康检查类型，固定为arp
database_name	字符串	长度1-31	数据库名称	是	
username	字符串	长度1-31	认证用户名	是	
password	字符串	长度1-31	认证密码	是	
query	字符串	不涉及	发送字符串	否	缺省值:空
response_str	字符串	不涉及	接收字符串	否	缺省值:空
row	整数	1-10	接收行	否	缺省值:1
column	整数	1-10	接收列	否	缺省值:1
database_type	整数	1-9	数据库类型	否	1:mssql;2: mysql;3:oracle;4:postgre
5:db2;6: gaussdb;7:oceandb;8:tidb;9:tdsql
缺省值:2
description	字符串
	长度1-191	描述	否	
retry	整数	0-5	重试次数	否	缺省值：3
interval	整数	1-180	检查间隔	否	缺省值：5
timeout	整数	1-1800	检查超时时间	否	缺省值：16
auto_disable	整数	0，1	自动禁用开关	否	缺省：关闭
alias_ipv4	字符	不涉及	别名地址ipv4	否	缺省值:空
alias_ipv6	字符	不涉及	别名地址ipv6	否	缺省值:空
alias_port	整数	1-65535	别名端口	否	缺省值:空
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "mysql",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "trans_mode": 0,
   "alias_ipv4_src": "6.156.1.31",
   "alias_ipv6_src": "3000:6:156:1::31",
    "interface": "Ethernet2/0",
    "alias_ipv4": "192.168.1.2",
    "alias_ipv6": "5001::2",
    "alias_port": 3301,
    "description": "test",
    "type": "database",
    "database_name": "test",
    "username": "root",
    "password": "123456",
    "query": "aaa",
    "response_str": "test",
    "row": 2,
    "column": 2,
    "database_type": 2
}

DNS健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	dns	检查类型	是	对于dns健康检查类型，固定为dns
domain	字符串	长度1-63	请求域名	否	缺省值:www.baidu.com
record_type	字符串	不涉及	记录类型	否	A/CNAME/SOA/PTR/MX/TXT/AAAA
缺省值:A
wantreturn	字符串	不涉及	返回code	否	可以接收多种code，code范围0-15
例如 "0,1,3-5"；缺省值:空
want_ipv4	ipv4地址	不涉及	期望返回ipv4地址	否	ipv4地址格式字符串,缺省值:空
want_ipv6	Ipv6地址	不涉及	期望返回ipv6地址	否	ipv6地址格式字符串,缺省值:空
ip_addr	ipv4地址	不涉及	反向解析域名的ip地址	否	与domain互斥，二者必选其一
dns_over_tcp	整数	0-1	通过tcp进行dns解析	否	0:关闭;1:开启;缺省值为0
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "health-dns",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 0,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "trans_mode": 0,
     "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "description": "health-dns",
    "dns_over_tcp": 0,
    "type": "dns",
    "port": 53,
    "domain": "www.baidu.com",
    "record_type": "A",
    "wantreturn": ""
}
FTP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	ftp	检查类型	是	对于ftp健康检查类型，固定为ftp
username	字符串	1-31	用户名	否	缺省值:空
password	字符串	1-31	密码	否	缺省值:空
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "ftp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "ftp",
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "port": 21,
    "username": "",
    "password": ""
}
HTTPS健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	https	对于http健康检查类型，固定为https	是	
port	整数	1-65534	端口,在关联到节点时,使用该端口作为目的端口检查,其他情况使用关联的端口做检查	否	缺省值:80
host	字符串	长度1-63	http头部host字段	否	缺省值:自动
header	数组	不涉及	响应头插入数组：
header > key:value
类型：字符串，
范围：1-127	否	缺省值:空
url	字符串	长度1-127	请求方法和url
	否	请求方法支持GET/POST/HEAD
缺省值: GET /index
post_data	字符串	长度1-255	发送body，当url中方法为POST时有效
	否	缺省值:空
username	字符串	长度1-31	认证用户名,当http需要登录认证时使用	否	缺省值:空
password	字符串	长度1-31	认证密码,当http需要登录认证时使用	否	缺省值:空
code	字符串	长度1-31	http返回码,code和pattern 只能使用一个	否	格式为100-899之间的数字组成的字符串,可以使用逗号(,)或者连接符(-)连接；缺省值:200
pattern	字符串	长度1-255	接收字符串,code和pattern 只能使用一个	否	缺省值:空
pattern_disable_str	字符串	长度1-256	接收禁用字符串，没有收到pattern 字符串但是收到该字符串之后，对健康检查目标执行软关机操作。必须配合pattern 参数使用	否	缺省值:空
server_fail_code	字符串	长度1-31	进入维护模式的响应码	否	格式为100-899之间的数字组成的字符串,可以使用逗号(,)或者连接符(-)连接；添加时缺省为空，
编辑时缺省不修改
sni	字符串	长度1-127		sni名称	否	缺省值:空
sslver	字符串	Default, SSL v3.0, TLS v1.0, TLS v1.1, TLS v1.2,
TLS v1.3,
GMTLS v1.1
	ssl协商时使用的ssl版本	否	缺省值是：Default 表示支持 SSL v3.0, TLS v1.0, TLS v1.1, TLS v1.2,TLS1.3,GMTLS v1.1的协商
https_ca	字符串	长度1-255	https健康检查的CA证书	否	缺省值:空
https_cert	字符串	长度1-255	https健康检查的client证书或GM签名证书	否	缺省值:空
https_key	字符串	长度1-255	https健康检查的client证书私钥或GM签名证书的私钥	否	缺省值:空
https_key_password	字符串	长度1-46	https健康检查的client私钥的密码或GM签名证书的私钥的密码	否	缺省值:空
https_ecert	字符串	长度1-255	https健康检查的GM加密证书	否	缺省值:空
https_ekey	字符串	长度1-255	https健康检查的GM加密证书的私钥	否	缺省值:空
https_ekey_password	字符串	长度1-46	https健康检查的GM加密证书的私钥的密码	否	缺省值:空
cipher_list	字符串		算法套件	否	缺省值：空
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
http_version	字符串	HTTP 1.0，HTTP 1.1	健康检查时使用的http的版本	否	默认值：HTTP 1.1；
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "https",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
   "alias_ipv4_src": "6.156.1.31",
   "alias_ipv6_src": "3000:6:156:1::31",
    "type": "https",
    "port": 5443,
    "host": "",
    "url": "GET /",
    "trans_mode": 0,
    "username": "",
    "password": "",
    "code": "",
    "sslver": "Default",
    "https_ca": "",
    "https_cert": "rsa",
    "https_key": "rsa",
    "cipher_list": [
        "TLS1_RSA_AES_128_SHA",
        "TLS1_RSA_AES_256_SHA"
    ]
}

国密健康检查添加例子：
请求body
{
    "name": "https",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
   "alias_ipv4_src": "6.156.1.31",
   "alias_ipv6_src": "3000:6:156:1::31",
    "type": "https",
    "port": 5443,
    "host": "",
    "url": "GET /",
    "username": "",
    "password": "",
    "code": "",
    "sslver": "GMTLS v1.1",
    "https_ca": "",
    "https_cert": "GM_sign",
    "https_key": "GM_sign",
    "https_ecert": "GM_enc",
    "https_ekey": "GM_enc",
    "cipher_list": [
        "GM1_ECC_SM4_SM3"
    ]
}
HTTP2S健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	https	对于http健康检查类型，固定为https	是	
port	整数	1-65534	端口,在关联到节点时,使用该端口作为目的端口检查,其他情况使用关联的端口做检查	否	缺省值:80
host	字符串	长度1-63	http头部host字段	否	缺省值:自动
url	字符串	长度1-127	请求方法和url
	否	请求方法支持GET/POST/HEAD
缺省值: GET /index
post_data	字符串	长度1-255	发送body，当url中方法为POST时有效
	否	缺省值:空
code	字符串	长度1-31	http返回码,code和pattern 只能使用一个	否	格式为100-899之间的数字组成的字符串,可以使用逗号(,)或者连接符(-)连接；缺省值:200
pattern	字符串	长度1-255	接收字符串,code和pattern 只能使用一个	否	缺省值:空
pattern_disable_str	字符串	长度1-256	接收禁用字符串，没有收到pattern 字符串但是收到该字符串之后，对健康检查目标执行软关机操作。必须配合pattern 参数使用	否	缺省值:空
server_fail_code	字符串	长度1-31	进入维护模式的响应码	否	格式为100-899之间的数字组成的字符串,可以使用逗号(,)或者连接符(-)连接；添加时缺省为空，
编辑时缺省不修改
sni	字符串	长度1-127		sni名称	否	缺省值:空
sslver	字符串	Default, SSL v3.0, TLS v1.0, TLS v1.1, TLS v1.2,
TLS v1.3,
GMTLS v1.1
	ssl协商时使用的ssl版本	否	缺省值是：Default 表示支持 SSL v3.0, TLS v1.0, TLS v1.1, TLS v1.2,TLS1.3,GMTLS v1.1的协商
https_ca	字符串	长度1-255	https健康检查的CA证书	否	缺省值:空
https_cert	字符串	长度1-255	https健康检查的client证书或GM签名证书	否	缺省值:空
https_key	字符串	长度1-255	https健康检查的client证书私钥或GM签名证书的私钥	否	缺省值:空
https_key_password	字符串	长度1-46	https健康检查的client私钥的密码或GM签名证书的私钥的密码	否	缺省值:空
https_ecert	字符串	长度1-255	https健康检查的GM加密证书	否	缺省值:空
https_ekey	字符串	长度1-255	https健康检查的GM加密证书的私钥	否	缺省值:空
https_ekey_password	字符串	长度1-46	https健康检查的GM加密证书的私钥的密码	否	缺省值:空
cipher_list	字符串		算法套件	否	缺省值：空
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "http2s",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 1,
    "trans_mode": 1,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "type": "http2s",
    "port": 5443,
    "host": "",
    "url": "GET /",
    "code": "",
    "sni": "",
    "sslver": "Default",
    "https_ca": "",
    "https_cert": "rsa",
    "https_key": "rsa",
    "cipher_list": []
}
国密健康检查添加例子：
请求body
{
    "name":"http2s",
    "retry":3,
    "up_check_cnt":1,
    "wait_all_retry":1,
    "interval":5,
    "timeout":5,
    "auto_disable":1,
    "trans_mode":1,
    "alias_ipv4_src":"6.156.1.31",
    "alias_ipv6_src":"3000:6:156:1::31",
    "type":"http2s",
    "port":5443,
    "host":"",
    "url":"GET /",
    "code":"",
    "sni":"",
    "sslver":"GMTLS v1.1",
    "https_ca":"",
    "https_cert":"GM_sign",
    "https_key":"GM_sign",
    "https_ecert":"GM_enc",
    "https_ekey":"GM_enc",
    "cipher_list":[
        "GM1_ECC_SM4_SM3"
    ]
}
SSL健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	https	对于http健康检查类型，固定为https	是	
port	整数	1-65534	端口,在关联到节点时,使用该端口作为目的端口检查,其他情况使用关联的端口做检查	否	缺省值:80
send_str		长度1-256	发送字符串	否	缺省值:空
response_str	字符串	长度1-256	接收字符串	否	缺省值:空
pattern_disable_str	字符串	长度1-256	接收禁用字符串，没有收到pattern 字符串但是收到该字符串之后，对健康检查目标执行软关机操作。必须配合pattern 参数使用	否	缺省值:空
sslver	字符串	Default, SSL v3.0, TLS v1.0, TLS v1.1, TLS v1.2,
TLS v1.3,
GMTLS v1.1
	ssl协商时使用的ssl版本	否	缺省值是：Default 表示支持 SSL v3.0, TLS v1.0, TLS v1.1, TLS v1.2,TLS1.3,GMTLS v1.1的协商
https_ca	字符串	长度1-255	https健康检查的CA证书	否	缺省值:空
https_cert	字符串	长度1-255	https健康检查的client证书或GM签名证书	否	缺省值:空
https_key	字符串	长度1-255	https健康检查的client证书私钥或GM签名证书的私钥	否	缺省值:空
https_key_password	字符串	长度1-46	https健康检查的client私钥的密码或GM签名证书的私钥的密码	否	缺省值:空
https_ecert	字符串	长度1-255	https健康检查的GM加密证书	否	缺省值:空
https_ekey	字符串	长度1-255	https健康检查的GM加密证书的私钥	否	缺省值:空
https_ekey_password	字符串	长度1-46	https健康检查的GM加密证书的私钥的密码	否	缺省值:空
cipher_list	字符串		算法套件	否	缺省值：空
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name":"SSL",
    "retry":3,
    "up_check_cnt":1,
    "wait_all_retry":1,
    "interval":5,
    "timeout":5,
    "auto_disable":0,
    "trans_mode":0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "type":"ssl",
    "port":5443,
    "send_str":"",
    "response_str":"",
    "response_disable_str":"",
    "sslver":"Default",
    "https_ca":"",
    "https_cert":"client.crt",
    "https_key":"client.key",
    "cipher_list":[
        "TLS1_RSA_AES_256_SHA",
        "TLS1_RSA_AES_128_SHA256",
        "TLS1_RSA_AES_128_SHA"
    ]
}
国密健康检查添加例子：
请求body
{
    "name": "SSL",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "type": "ssl",
    "port": 5443,
    "send_str": "",
    "response_str": "",
    "response_disable_str": "",
    "sslver": "GMTLS v1.1",
    "https_ca": "",
    "https_cert": "GM_sign",
    "https_key": "GM_sign",
    "https_ecert": "GM_enc",
    "https_ekey": "GM_enc",
    "cipher_list": [
        "GM1_ECC_SM4_SM3"
    ]
}

LDAP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	ldap	检查类型	是	对于ldap健康检查类型，固定为ldap
username	字符串	1-31	用户名	否	缺省值:空
password	字符串	1-31	密码	否	缺省值:空
ssl	整数	0,1	使用ssl	否	1:是;0:否；缺省值:0
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
auto_disable	整数	0，1	自动禁用开关	否	缺省：关闭
alias_ipv4_src	字符串	不涉及	健康检查源地址	否	缺省值:空
interface	字符	不涉及	健康检查接口	否	
alias_ipv4	字符	不涉及	别名地址ipv4	否	缺省值:空
alias_ipv6	字符	不涉及	别名地址ipv6	否	缺省值:空
alias_port	整数	1-65535	别名端口	否	缺省值:空
retry	整数	0-5	重试次数	否	缺省值：3
interval	整数	1-180	检查间隔	否	缺省值：5
timeout	整数	1-1800	检查超时时间	否	缺省值：5
base	字符串	0-127	基本DN	否	缺省值:空
filter	字符串	0-127	筛选过滤语句	否	缺省值:空
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "hc_locust_ldap_1",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "interface": "Ethernet2/0",
    "alias_ipv4": "192.168.2.2",
    "alias_ipv6": "2003::1",
    "alias_port": 389,
    "type": "ldap",
    "port": 636,
    "ssl": 1,
    "username": "cn=Manager,dc=walkingcloud,dc=cn",
    "password": "123456",
    "base": "ou=Group,dc=walkingcloud,dc=cn",
    "filter": "(&(cn=user1)(description=test)(gidNumber=1000))"
}
NTP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	ntp	检查类型	是	对于ntp健康检查类型，固定为ntp
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
auto_disable	整数	0，1	自动禁用开关	否	缺省：关闭
alias_ipv4_src	字符串	不涉及	健康检查源地址	否	缺省值:空
interface	字符	不涉及	健康检查接口	否	
alias_ipv4	字符	不涉及	别名地址ipv4	否	缺省值:空
alias_ipv6	字符	不涉及	别名地址ipv6	否	缺省值:空
alias_port	整数	1-65535	别名端口	否	缺省值:空
retry	整数	0-5	重试次数	否	缺省值：3
interval	整数	1-180	检查间隔	否	缺省值：5
timeout	整数	1-1800	检查超时时间	否	缺省值：5
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "ntp",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "alias_port": 123,
    "description": "a",
    "type": "ntp",
    "port": 123
}
IMAP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	imap	检查类型	是	对于imap健康检查类型，固定为imap
username	字符串	1-31	用户名	否	缺省值:空
password	字符串	1-31	密码	否	缺省值:空
plain_text	整数	0,1		否	0禁用，1使能，缺省值:0
login	整数	0,1		否	0禁用，1使能，缺省值:0
cram_md5	整数	0,1		否	0禁用，1使能，缺省值:0
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭

POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "imap",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "imap",
    "port": 143,
    "plain_text": 0,
    "login": 0,
    "cram_md5": 0,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "username": "",
    "password": ""
}
POP3健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	pop3	检查类型	是	对于pop3健康检查类型，固定为pop3
username	字符串	1-31	用户名	否	缺省值:空
password	字符串	1-31	密码	否	缺省值:空
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "pop3",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "pop3",
     "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "port": 110,
    "username": "aas",
    "password": "dww"
}
RADIUS健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	radius	检查类型	是	对于radius健康检查类型，固定为radius
username	字符串	1-31	用户名	否	缺省值:空
password	字符串	1-31	密码	否	缺省值:空
secret	字符串	1-31	共享密码	否	缺省值:adc
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "radius",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "radius",
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "port": 1812,
    "username": "",
    "password": "",
    "secret": "secret"
}
RTSP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	rtsp	检查类型	是	对于rtsp健康检查类型，固定为rtsp
url	字符串	长度1-63	url	否	缺省值:/music.mp3
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "rtsp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "type": "rtsp",
    "port": 554,
    "url": "/music.mp3"
}
SIP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	sip	检查类型	是	对于sip健康检查类型，固定为sip
register	整数	0,1	使用register	否	1:是;0:否;缺省值:0
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "sip",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "sip",
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "port": 5060,
    "register": 0
}
SMTP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	smtp	检查类型	是	对smtp健康检查类型，固定为smtp
domain	字符串	长度1-63	域名	否	缺省值:adc
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "smtp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "type": "smtp",
    "port": 25,
    "domain": "mail"
}
SNMP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
trans_mode	字符串	0,1	透明模式开关	否	缺省：关闭
operation	字符串	长度1-63	操作	否	get/get_next；缺省值:get
oid	字符串	长度1-63	oid，会自动加上前缀1.3.6.1	否	缺省值:.2.1.1.1.0
community	字符串	长度1-63	团体字	否	缺省值:public
description	字符串
	长度1-191	描述	否	

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "snmp1",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 1,
    "trans_mode": 1,
    "alias_ipv4_src": "3.3.3.3",
    "alias_ipv6_src": "3000::3",
    "interface": "ve158",
    "alias_ipv4": "2.2.2.2",
    "alias_ipv6": "3000::2",
    "alias_port": 2222,
    "type": "snmp",
    "port": 161,
    "operation": "get",
    "oid": "2.1.1.1.0",
    "community": "public"
}
TCP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
trans_mode	字符串	0,1	透明模式开关	否	缺省：关闭
send_rst	整数	0，1	发送reset	否	1:是;0:否;缺省值:0
send_str	字符串	长度1-1023	发送字符串	否	缺省值:空
response_str	字符串	长度1-1023	接收字符串	否	缺省值:空
response_disable_str	字符串	长度1-1023

	接收禁用字符串，没有收到response字符串但是收到该字符串之后，对健康检查目标执行软关机操作。必须配合response参数使用	否	缺省值:空
description	字符串
	长度1-191	描述	否	

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "tcp1",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 1,
    "trans_mode": 1,
    "alias_ipv4_src": "3.3.3.3",
    "alias_ipv6_src": "3000::3",
    "interface": "ve158",
    "alias_ipv4": "2.2.2.2",
    "alias_ipv6": "3000::2",
    "alias_port": 2222,
    "type": "tcp",
    "port": 80,
    "send_rst": 0,
    "send_str": "",
    "response_str": "",
    "response_disable_str": ""
}
TCP-PRO健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
trans_mode	字符串	0,1	透明模式开关	否	缺省：关闭
send_rst	整数	0，1	发送reset	否	1:是;0:否;缺省值:0
send_str	字符串	长度1-1023	发送字符串	否	缺省值:空
response_str	字符串	长度1-1023	接收字符串	否	缺省值:空
response_disable_str	字符串	长度1-1023

	接收禁用字符串，没有收到response字符串但是收到该字符串之后，对健康检查目标执行软关机操作。必须配合response参数使用	否	缺省值:空
description	字符串
	长度1-191	描述	否	

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "tcppro1",
    "retry": 0,
    "up_check_cnt": 1,
    "wait_all_retry": 0,
    "interval": 5,
    "timeout": 16,
    "auto_disable": 1,
    "trans_mode": 1,
    "alias_ipv4_src": "3.3.3.3",
    "alias_ipv6_src": "3000::3",
    "interface": "ve1522",
    "alias_ipv4": "2.2.2.2",
    "alias_ipv6": "3000::2",
    "alias_port": 2222,
    "type": "tcp-pro",
    "port": 80,
    "send_rst": 0,
    "send_str": "",
    "response_str": "",
    "response_disable_str": ""
}

UDP健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	udp	检查类型	是	对于udp健康检查类型，固定为udp
send_str	字符串	长度1-256	发送字符串	否	缺省值:空
response_str	字符串	长度1-256	接收字符串	否	缺省值:空
response_disable_str	字符串	长度1-256	接收禁用字符串，没有收到response字符串但是收到该字符串之后，对健康检查目标执行软关机操作。必须配合response参数使用	否	缺省值:空
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "udp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "type": "udp",
    "port": 8000
}
UDP-PRO健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	udp-pro	检查类型	是	对于udp-pro健康检查类型，固定为udp-pro
retry	整数	pro类型：0	重试次数	是	pro类型必须设为0
interval	整数	1-180	间隔时间,单位秒	是	缺省值：5
timeout	整数	pro类型：1-1800	超时时间,单位秒	是	缺省值：5
pro类型的值必须大于interval
send_str	字符串	长度1-256	发送字符串	否	缺省值:空
response_str	字符串	长度1-256	接收字符串	否	缺省值:空
response_disable_str	字符串	长度1-256	接收禁用字符串，没有收到response字符串但是收到该字符串之后，对健康检查目标执行软关机操作。必须配合response参数使用	否	缺省值:空
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "udp-pro",
    "retry": 0,
    "interval": 3,
    "timeout": 5,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
    "alias_ipv6_src": "3000:6:156:1::31",
    "type": "udp-pro",
    "port": 8000
}

自定义脚本健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
type	字符串	script	检查类型	是	对于自定义脚本健康检查类型，固定为script
script	字符串	长度1-191	脚本名称	是	需要先上传脚本
retry	整数	pro类型：0	重试次数	是	pro类型必须设为0
interval	整数	1-180	间隔时间,单位秒	是	缺省值：5
timeout	整数	pro类型：1-1800	超时时间,单位秒	是	缺省值：5
pro类型的值必须大于interval
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
auto_disable	整数	0，1	自动禁用开关	否	缺省：关闭
alias_ipv4_src	字符串	不涉及	健康检查源地址	否	缺省值:空
interface	字符	不涉及	健康检查接口	否	
alias_ipv4	字符	不涉及	别名地址ipv4	否	缺省值:空
alias_ipv6	字符	不涉及	别名地址ipv6	否	缺省值:空
alias_port	整数	1-65535	别名端口	否	缺省值:空
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "sc_test_001",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "trans_mode": 0,
    "alias_ipv4_src": "6.156.1.31",
   "alias_ipv6_src": "3000:6:156:1::31",
    "interface": "Ethernet2/0",
    "alias_ipv4": "192.168.2.2",
    "alias_ipv6": "5005::2",
    "type": "script",
    "script": "hc_transp_tcp.py",
    "port": 80
}
组合健康检查添加
Action:  slb.healthcheck.add
请求参数：
名称	类型	范围	含义	必选	备注
description	字符串
	长度1-191	描述	否	
trans_mode	整数	0，1	透明模式开关	否	缺省：关闭
combo	字符串	长度1-63	组合健康检查表达式	是	hck关键字表示健康检查名称
and 表示与
or 表示 或
not 表示非
使用后缀表达式

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.add
请求body
{
    "name": "combo",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 1,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 1,
    "trans_mode": 0,
    "alias_ipv4_src": "3.3.3.3",
    "alias_ipv6_src": "3000::3",
    "interface": "ve158",
    "alias_ipv4": "2.2.2.2",
    "alias_ipv6": "3000::2",
    "alias_port": 2222,
    "type": "combo",
    "combo": "hck tcp1 hck ping1 and "
}
健康检查列表
Action:  slb.healthcheck.list
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.list
响应参数:
响应参数参考健康检查添加中各种类型健康检查的相应参数
响应举例：
[
  {
    "name": "ping",    
    "retry": 3,       
    "interval": 5,       
    "timeout": 5,   
    "type": "icmp"   
  },
  {
    "name": "http",
    "retry": 3,
    "interval": 5,
"timeout": 5,
"auto_disable": 0,          
                       
    "alias_ipv4_src": "192.168.1.1", 
"interface": "Ethernet 0/1",    
                        
    "alias_ipv4": "1.2.3.4",       
    "alias_port": 889,      
    "alias_ipv6": "2001::1",  
    "type": "http"
    "port": 80,                      
    "host": "ahost",                 
    "url": "GET /index",            
    "post_data": "mybodystring",     
    "username": "username",       
    "password": "/+mboU9rpJM8EIy41dsA5zwQjLjV2wDnPBCMuNXbAOc8EIy41dsA5zwQjLjV2wDn",          
    "code": "202",             
    "pattern": "rvstring"         
  },
  {
    "name": "arp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "arp"
  },
  {
    "name": "database",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "database",
    "database_name": "db",      
    "username": "aaa",
    "password": "/+mboU9rpJM8EIy41dsA5zwQjLjV2wDnPBCMuNXbAOc8EIy41dsA5zwQjLjV2wDn",
    "query": "",                
    "response_str": "",          
    "row": 1,                      
    "column": 1,                
    "database_type": 4       
  },
  {
    "name": "dns",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
"type": "dns",
"dns_over_tcp": 0,
    "port": 53,
    "domain": "www.baidu.com",  
    "record_type": "A",       
    "wantreturn": "1,2,3",         
    "want_ipv4": "4.3.2.1"      
  },

  {
    "name": "ftp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "ftp",
    "port": 21,
    "username": "",           
    "password": ""             
  },
  {
    "name": "https",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "https",
    "port": 443,                  
    "host": "ahost",             
    "url": "GET /index",              
    "post_data": "mybodystring",    
    "username": "username",        
    "password": "/+mboU9rpJM8EIy41dsA5zwQjLjV2wDnPBCMuNXbAOc8EIy41dsA5zwQjLjV2wDn",          
"code": "202",
"sslver": "tlsv12",                 
    "pattern": "rvstring"       
  },
  {
    "name": "imap",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "imap",
"port": 143,
"plain_text": 0,   
"login": 0,      
"cram_md5": 0, 
    "username": "",  
    "password": ""   
  },
  {
    "name": "ldap",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "ldap",
    "port": 389,
    "ssl": 0,                
    "distinguished_name": "",  
    "password": ""           
  },
  {
    "name": "ntp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "ntp",
    "port": 123
  },
  {
    "name": "pop3",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "pop3",
    "port": 110,
    "username": "aas",       
    "password": "/+mboU9rpJM8EIy41dsA5zwQjLjV2wDnPBCMuNXbAOc8EIy41dsA5zwQjLjV2wDn"       
  },
  {
    "name": "radius",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "radius",
    "port": 1812,
    "username": "",     
    "password": "",        
    "secret": "secret"       
  },
  {
    "name": "rtsp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "rtsp",
    "port": 554,
    "url": "/music.mp3"     
  },
  {
    "name": "sip",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "sip",
    "port": 5060,
    "register": 0    
  },
  {
    "name": "smtp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "smtp",
    "port": 25,
    "domain": "mail"           
  },
  {
    "name": "snmp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "snmp",
    "port": 161,
    "operation": "get",      
    "oid": "2.1.1.1.0",      
    "community": "public"   
  },
  {
    "name": "tcp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "tcp",
    "port": 80,
    "send_rst": 0,      
    "send_str": "aaaaa",        
    "response_str": "bbbbb"   
  },
  {
    "name": "udp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "udp",
    "port": 8000
  },
  {
    "name": "script",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "script",
    "script": "checkbody.py",    
    "port": 80
  },
  {
    "name": "combo",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "combo",
    "combo": "hck ping not "       
  }
]
分区中获取common 健康检查列表
Action:  slb.healthcheck.list.withcommon
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.list.withcommon
响应参数:
响应参数参考健康检查添加中各种类型健康检查的相应参数
响应举例：
[
  {
    "name": "common/ping",    
    "retry": 3,       
    "interval": 5,       
    "timeout": 5,   
    "type": "icmp"   
  },
  {
    "name": "common/http",
    "retry": 3,
    "interval": 5,
"timeout": 5,
"auto_disable": 0,          
                       
    "alias_ipv4_src": "192.168.1.1", 
"interface": "Ethernet 0/1",    
                        
    "alias_ipv4": "1.2.3.4",       
    "alias_port": 889,      
    "alias_ipv6": "2001::1",  
    "type": "http"
    "port": 80,                      
    "host": "ahost",                 
    "url": "GET /index",            
    "post_data": "mybodystring",     
    "username": "username",       
    "password": "/+mboU9rpJM8EIy41dsA5zwQjLjV2wDnPBCMuNXbAOc8EIy41dsA5zwQjLjV2wDn",          
    "code": "202",             
    "pattern": "rvstring"         
  },
  {
    "name": "common/arp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "arp"
  },
  {
    "name": "common/database",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "database",
    "database_name": "db",      
    "username": "aaa",
    "password": "/+mboU9rpJM8EIy41dsA5zwQjLjV2wDnPBCMuNXbAOc8EIy41dsA5zwQjLjV2wDn",
    "query": "",                
    "response_str": "",          
    "row": 1,                      
    "column": 1,                
    "database_type": 4       
  },
  {
    "name": "common/dns",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "dns",
    "port": 53,
    "domain": "www.baidu.com",  
    "record_type": "A",       
    "wantreturn": "1,2,3",         
    "want_ipv4": "4.3.2.1"      
  },
  {
    "name": "common/ftp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "ftp",
    "port": 21,
    "username": "",           
    "password": ""             
  },
  {
    "name": "common/https",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "https",
    "port": 443,                  
    "host": "ahost",             
    "url": "GET /index",              
    "post_data": "mybodystring",    
    "username": "username",        
    "password": "/+mboU9rpJM8EIy41dsA5zwQjLjV2wDnPBCMuNXbAOc8EIy41dsA5zwQjLjV2wDn",          
"code": "202",
"sslver": "tlsv12",                 
    "pattern": "rvstring"       
  },
  {
    "name": "imap",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "imap",
"port": 143,
"plain_text": 0,   
"login": 0,      
"cram_md5": 0, 
    "username": "",  
    "password": ""   
  },
  {
    "name": "common/ldap",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "ldap",
    "port": 389,
    "ssl": 0,                
    "distinguished_name": "",  
    "password": ""           
  },
  {
    "name": "common/ntp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "ntp",
    "port": 123
  },
  {
    "name": "pop3",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "pop3",
    "port": 110,
    "username": "aas",       
    "password": "/+mboU9rpJM8EIy41dsA5zwQjLjV2wDnPBCMuNXbAOc8EIy41dsA5zwQjLjV2wDn"       
  },
  {
    "name": "common/radius",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "radius",
    "port": 1812,
    "username": "",     
    "password": "",        
    "secret": "secret"       
  },
  {
    "name": "rtsp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "rtsp",
    "port": 554,
    "url": "/music.mp3"     
  },
  {
    "name": "common/sip",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "sip",
    "port": 5060,
    "register": 0    
  },
  {
    "name": "common/smtp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "smtp",
    "port": 25,
    "domain": "mail"           
  },
  {
    "name": "common/snmp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "snmp",
    "port": 161,
    "operation": "get",      
    "oid": "2.1.1.1.0",      
    "community": "public"   
  },
  {
    "name": "tcp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "tcp",
    "port": 80,
    "send_rst": 0,      
    "send_str": "aaaaa",        
    "response_str": "bbbbb"   
  },
  {
    "name": "common/udp",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "udp",
    "port": 8000
  },
  {
    "name": "common/script",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "script",
    "script": "checkbody.py",    
    "port": 80
  },
  {
    "name": "common/combo",
    "retry": 3,
    "interval": 5,
    "timeout": 5,
    "type": "combo",
    "combo": "hck ping not "       
  }



健康检查编辑
Action:  slb.healthcheck.edit
请求参数:
请求参数请参考 健康检查添加 中各种类型健康检查的响应参数
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.edit
请求body
{
    "name": "1",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 0,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "type": "https",
    "port": 443,
    "host": "",
    "url": "POST /*",
    "post_file": "aa.html",
    "username": "",
    "password": "",
    "code": "",
    "sslver": "TLS v1.2"
}
健康检查获取
Action:  slb.healthcheck.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	健康检查名称	是	必须存在

请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.get
请求body
{
    "name": "https_test"             
}
响应参数:
响应参数参考健康检查添加中各种类型健康检查的相应参数
响应举例：
{
    "name": "https_test",
    "retry": 3,
    "up_check_cnt": 1,
    "wait_all_retry": 0,
    "interval": 5,
    "timeout": 5,
    "auto_disable": 0,
    "type": "https",
    "port": 443,
    "host": "",
    "url": "POST /*",
    "post_file": "aa.html",
    "username": "",
    "password": "aAOc8EIy41dsA5zwQjLjV2wDn",
    "code": "",
    "sslver": "TLS v1.2"
}
健康检查删除
Action:  slb.healthcheck.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	健康检查名称	是	必须存在

请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.del
请求body
{
    "name": "ping"             
}

健康检查脚本列表
Action:  slb.healthcheck.script.list
请求参数:
无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.script.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-50	脚本名称
响应举例：
[
  {
    "name": "checkbody.py"    
  },
  {
    "name": "checkbody1.py"
  }
]

健康检查脚本上传
Action:  slb.healthcheck.script.upload
请求参数:
无
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.script.upload
	此API需要使用form-data的方式上传健康检查脚本文件

健康检查脚本删除
Action:  slb.healthcheck.script.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-50	脚本名称	是	唯一

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.script.del
请求body
{
    "name": "health_check_script1.py"   
}
健康检查POST文件列表
Action:  slb.healthcheck.postfile.list
请求参数:
无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.postfile.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-50	post文件名称
响应举例：
[
  {
    "name": "checkbody.html"    
  },
  {
    "name": "checkbody1.html"
  }
]
健康检查POST文件上传
Action:  slb.healthcheck.postfile.upload
请求参数:
无
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.postfile.upload
	此API需要使用form-data的方式上传健康检查POST文件

健康检查POST文件删除
Action:  slb.healthcheck.postfile.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-50	脚本名称	是	唯一

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthcheck.postfile.del
请求body
{
    "name": "health_check_post.html"   
}

健康检查检测
健康检查测试列表
Action:  slb.healthtest.list
请求参数:无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthtest.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	引用健康检查模块设定的名字
ip	ipv4/ipv6	不涉及	需要测试的目的ip地址
count	整数	1-10	测试的次数；默认为1
port	整数	0-65535	Ip地址的测试端口；0表示未设置端口
响应举例：
    [
    {
        
        "ip": "120.21.1.111",
        "name": "ping",
        "count": "2",
        "port": "53",
        "result": "1:  DOWN. (ICMP timeout) 2:  DOWN. (ICMP timeout) "
    }
]

添加健康检查测试
Action:  slb.healthtest.add
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	引用健康检查模块设定的名字	是	
ip	ipv4/ipv6	不涉及	需要测试的目的ip地址	是	
count	整数	1-10	测试的次数	否	缺省值：1
port	整数	0-65535	Ip地址的测试端口；0表示未设置端口	否	缺省值：0
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthtest.add
请求body
{
    "name": "ping",
    "count": "2", 
    "port":"53",
    "ip": "120.21.1.111"
}
获取健康检查测试
Action:  slb.healthtest.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	引用健康检查模块设定的名字	是	                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
ip	ipv4/ipv6	不涉及	需要测试的目的ip地址	是	
count	整数	1-10	测试的次数	是	缺省值：1
port	整数	0-65535	Ip地址的测试端口；0表示未设置端口	是	缺省值：0
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthtest.get
请求body
{
        "name": "ping",
        "ip": "120.21.1.111",
        "count": "2",
        "port": "53"
    }
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	引用健康检查模块设定的名字
ip	ipv4/ipv6	不涉及	需要测试的目的ip地址
count	整数	1-10	测试的次数，缺省为1
port	整数	0-65535	Ip地址的测试端口；0表示未设置端口
响应举例：
{
             
              "result": "1:  DOWN. (ICMP timeout) "
       }

删除健康检查测试
Action:  slb.healthtest.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	引用健康检查模块设定的名字	是	
ip	ipv4/ipv6	不涉及	需要测试的目的ip地址	是	
count	整数	1-10	测试的次数	否	缺省值：1
port	整数	0-65535	Ip地址的测试端口；0表示未设置端口	否	缺省值：0
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.healthtest.del
请求body
{
        "name": "ping",
        "ip": "120.21.1.111",
        "count": "2",
        "port": "53"
}
被动健康检查
添加被动健康检查配置
Action:  slb.passive-health-check.add

请求参数:
名称	类型	范围	含义
name	字符串	长度1-191	被动健康检查名称
description	字符串	长度1-191	描述信息
inband_check	整数	0,1	带内检查, 1：开启，0：关闭
inband_retry	整数	1-3	新建重试次数
inband_reassign	整数	1-127	新建失败次数
rst_check	整数	0,1	rst检查, 1：开启，0：关闭
rst_num	整数	1-127	rst统计数量
rst_interval	整数	1-3600	rst统计间隔
rst_log	整数	0,1	rst日志, 1：开启，0：关闭
zerowin_check	整数	0,1	零窗口检查, 1：开启，0：关闭
zerowin_num	整数	1-65535	零窗口统计
rsptime_check	整数	0,1	rsp检查, 1：开启，0：关闭
rsptime_delconn	整数	0,1	rsp删除连接, 1：开启，0：关闭
rsptime_log	整数	0,1	rsp日志, 1：开启，0：关闭
rsptime_interval	整数	1-3600	rsp统计间隔
rsptime_maxdelay	整数	1-3600	rsp最大延时
rsptime_maxcnt	整数	1-65535	rsp统计数量
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.passive-health-check.add
请求body：
{
    "name": "HC-passive1",
    "description": "",
    "inband_check": 1,
    "inband_retry": 1,
    "inband_reassign": 1,
    "rst_check": 1,
    "rst_num": 1,
    "rst_interval": 1,
    "rst_log": 1,
    "zerowin_check": 1,
    "zerowin_num": 1,
    "rsptime_check": 1,
    "rsptime_delconn": 1,
    "rsptime_log": 1,
    "rsptime_interval": 32,
    "rsptime_maxdelay": 5,
    "rsptime_maxcnt": 64
}
获取被动健康检查配置列表
Action:  slb.passive-health-check.list
请求参数:无
请求举例:
GET http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.passive-health-check.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	被动健康检查名称
description	字符串	长度1-191	描述信息
inband_check	整数	0,1	带内检查, 1：开启，0：关闭
inband_retry	整数	1-3	新建重试次数
inband_reassign	整数	1-127	新建失败次数
rst_check	整数	0,1	rst检查, 1：开启，0：关闭
rst_num	整数	1-127	rst统计数量
rst_interval	整数	1-3600	rst统计间隔
rst_log	整数	0,1	rst日志, 1：开启，0：关闭
zerowin_check	整数	0,1	零窗口检查, 1：开启，0：关闭
zerowin_num	整数	1-65535	零窗口统计
rsptime_check	整数	0,1	rsp检查, 1：开启，0：关闭
rsptime_delconn	整数	0,1	rsp删除连接, 1：开启，0：关闭
rsptime_log	整数	0,1	rsp日志, 1：开启，0：关闭
rsptime_interval	整数	1-3600	rsp统计间隔
rsptime_maxdelay	整数	1-3600	rsp最大延时
rsptime_maxcnt	整数	1-65535	rsp统计数量

响应举例： 
{
"name": "test",
"description": "",
"inband_check": 1,
"inband_retry": 1,
"inband_reassign": 2,
"rst_check": 1,
"rst_num": 8,
"rst_interval": 30,
"rst_log": 1,
"zerowin_check": 1,
"zerowin_num": 23,
"rsptime_check": 1,
"rsptime_delconn": 1,
"rsptime_log": 1,
"rsptime_interval": 10,
"rsptime_maxdelay": 2,
"rsptime_maxcnt": 5
}

获取指定被动健康检查配置
Action:  slb.passive-health-check.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	被动健康检查名称	是	

请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.passive-health-check.get
请求body：
{"name":"pcheck1"}
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	被动健康检查名称
description	字符串	长度1-191	描述信息
inband_check	整数	0,1	带内检查, 1：开启，0：关闭
inband_retry	整数	1-3	新建重试次数
inband_reassign	整数	1-127	新建失败次数
rst_check	整数	0,1	rst检查, 1：开启，0：关闭
rst_num	整数	1-127	rst统计数量
rst_interval	整数	1-3600	rst统计间隔
rst_log	整数	0,1	rst日志, 1：开启，0：关闭
zerowin_check	整数	0,1	零窗口检查, 1：开启，0：关闭
zerowin_num	整数	1-65535	零窗口统计
rsptime_check	整数	0,1	rsp检查, 1：开启，0：关闭
rsptime_delconn	整数	0,1	rsp删除连接, 1：开启，0：关闭
rsptime_log	整数	0,1	rsp日志, 1：开启，0：关闭
rsptime_interval	整数	1-3600	rsp统计间隔
rsptime_maxdelay	整数	1-3600	rsp最大延时
rsptime_maxcnt	整数	1-65535	rsp统计数量

响应举例：
{
"name": "test",
"description": "",
"inband_check": 1,
"inband_retry": 1,
"inband_reassign": 2,
"rst_check": 1,
"rst_num": 8,
"rst_interval": 30,
"rst_log": 1,
"zerowin_check": 1,
"zerowin_num": 23,
"rsptime_check": 1,
"rsptime_delconn": 1,
"rsptime_log": 1,
"rsptime_interval": 10,
"rsptime_maxdelay": 2,
"rsptime_maxcnt": 5
}
编辑指定被动健康检查配置
Action:  slb.passive-health-check.edit
请求参数:
名称	类型	范围	含义
name	字符串	长度1-191	被动健康检查名称
description	字符串	长度1-191	描述信息
inband_check	整数	0,1	带内检查, 1：开启，0：关闭
inband_retry	整数	1-3	新建重试次数
inband_reassign	整数	1-127	新建失败次数
rst_check	整数	0,1	rst检查, 1：开启，0：关闭
rst_num	整数	1-127	rst统计数量
rst_interval	整数	1-3600	rst统计间隔
rst_log	整数	0,1	rst日志, 1：开启，0：关闭
zerowin_check	整数	0,1	零窗口检查, 1：开启，0：关闭
zerowin_num	整数	1-65535	零窗口统计
rsptime_check	整数	0,1	rsp检查, 1：开启，0：关闭
rsptime_delconn	整数	0,1	rsp删除连接, 1：开启，0：关闭
rsptime_log	整数	0,1	rsp日志, 1：开启，0：关闭
rsptime_interval	整数	1-3600	rsp统计间隔
rsptime_maxdelay	整数	1-3600	rsp最大延时
rsptime_maxcnt	整数	1-65535	rsp统计数量

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.passive-health-check.edit
请求body：
{
    "name": "HC-passive1",
    "description": "",
    "inband_check": 1,
    "inband_retry": 1,
    "inband_reassign": 1,
    "rst_check": 1,
    "rst_num": 1,
    "rst_interval": 1,
    "rst_log": 1,
    "zerowin_check": 1,
    "zerowin_num": 1,
    "rsptime_check": 1,
    "rsptime_delconn": 1,
    "rsptime_log": 1,
    "rsptime_interval": 32,
    "rsptime_maxdelay": 5,
    "rsptime_maxcnt": 64
}

删除指定被动健康检查配置
Action:  slb.passive-health-check.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	被动健康检查名称	是	
请求举例:
POST http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.passive-health-check.del
请求body：
{"name":"pcheck1"}
eRule
eRule上传
Action:  slb.erule.upload
请求参数:无
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.erule.upload
	此API使用form-data方式上传一个erule 脚本文件

eRule在线编辑
Action:  slb.erule.content.add
请求参数:无
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.erule.content.add
	此API使用form-data在线编辑erule 脚本文件并创建


eRule删除
Action:  slb.erule.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	erule文件名称	是	

请求举例：
POST 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.erule.del
{
    "name": "erule-empty.txt"
}



eRule列表
Action:  slb.erule.list
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.erule.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	erule文件名称
syntax_ok	整数	0-1	erule文件语法检查结果:1:通过;0:失败
响应举例：
[
  {
"name": "erule-empty.txt",           
        "syntax_ok": 1           
  }
]


eRule服务器文件上传
Action:  slb.erulefiles.upload
请求参数:无
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.erulefiles.upload
	此API使用form-data方式上传一个erule 服务器文件


eRule服务器文件删除
Action:  slb.erulefiles.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	erule服务器文件名称	是	

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.erulefiles.del
请求body
{
    "name": "erulefiletest.txt"                  
}

eRule服务器文件列表
Action:  slb.erulefiles.list
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.erulefiles.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	erule服务器文件名称
time	字符串	长度1-63	erule服务器文件上传时间
响应举例：
[
    {
        "name": "erule_server_file.txt",
        "time": "2024-06-11 15:38:59"
    }
]
连接保持
Cookie连接保持
Cookie保持列表
Action：slb.persist.cookie.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.cookie.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	cookie连接保持名称
expire_enable	整数	0,1	expire是否使能;1：是；0：否
expire	整数	0-30000000	超时时间，仅当expire_enable为1时生效
method	整数	0,1，2	cookie保持方式,0插入,1重写，2被动；缺省值：0
encrypt	整数	0,1,2	cookie加密,0不加密,1加密服务池名称,2全加密
encrypt_password	字符串	长度1-63	加密的密码
http_only	整数	0,1	使用http_only字段, 1:是,0:否
secure	整数	0,1	使用secure字段, 1:是,0:否
cookie_name	字符串	长度1-63	cookie名称
domain	字符串	长度1-31	域名
path	字符串	长度1-31	路径
type	整数	0,1,2	匹配方法：0端口，1节点，2服务池节点，3服务池，缺省值0
insert	整数	0,1	cookie插入；1：是；0：否
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
description	字符串
	长度1-191	描述
响应举例：
[{
  "name": "profile_persist_cookie_1",
  "expire_enable": 1, 
  "expire": 123,
  "description": "23", 
  "method": 1, 
  "encrypt": 1, 
  "http_only": 1, 
  "secure": 1, 
  "cookie_name": "name",
  "domain": "domain",
  "path": "path",
  "type": 2,
  "insert": 1,
  "ignore_connlimit": 1
}]
Cookie保持获取
Action：slb.persist.cookie.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	cookie连接保持名称	是	
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.cookie.get
请求body：
{
    "name": "profile_persist_cookie_1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	cookie连接保持名称
expire_enable	整数	0,1	expire是否使能；1：是；0：否
method	整数	0,1,2	cookie保持方式，0插入，1重写，2被动；缺省值：0
encrypt	整数	0,1,2	cookie加密,0不加密,1加密服务池名称,2全加密
encrypt_password	字符串	长度1-63	加密的密码
http_only	整数	0,1	使用http_only字段, 1:是,0:否
secure	整数	0,1	使用secure字段, 1:是,0:否
expire	整数	0-30000000	cookie超时时间
cookie_name	字符串	长度1-63	cookie名称
domain	字符串	长度1-31	域名
path	字符串	长度1-31	路径
type	整数	0,1,2	匹配方法：0端口，1节点，2服务池节点，3服务池，缺省值0
insert	整数	0,1	cookie插入；1：是；0：否
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
description	字符串
	长度1-191	描述
响应举例：
{
  "name": "profile_persist_cookie_1",
  "expire_enable": 1,
  "expire": 123,
"method": 1, 
"description": "23", 
"encrypt": 1, 
"http_only": 1, 
"secure": 1,
  "cookie_name": "name",
  "domain": "domain",
  "path": "path",
  "type": 2,
  "insert": 1,
  "ignore_connlimit": 1
}
Cookie保持增加
Action：slb.persist.cookie.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	cookie连接保持名称	是	唯一
expire_enable	整数	0,1	expire是否使能;	否	1：是；0：否;缺省值0
expire	整数	0-30000000	超时时间	否	expire_enable为1时有效,缺省值0
method	整数	0,1,2	cookie保持方式	否	cookie保持方式，0插入，1重写，2被动；缺省值：0
encrypt	整数	0,1,2	cookie加密	否	,0不加密,1加密服务池名称,2全加密,缺省值0
encrypt_password	字符串	长度1-63	加密的密码	否	缺省的话为空，不显示
http_only	整数	0,1	使用http_only字段,	否	1:是,0:否,缺省值0
secure	整数	0,1	使用secure字段	否	1:是,0:否,缺省值0
cookie_name	字符串	长度1-63	cookie名称	否	缺省值:空字符串
domain	字符串	长度1-31	域名	否	缺省值:空字符串
path	字符串	长度1-31	路径	否	缺省值:空字符串
type	整数	0,1,2	匹配方法	否	0端口，1节点，2服务池节点，3服务池，缺省值0
insert	整数	0,1	开启cookie插入	否	1使能，0禁用，缺省值0
ignore_connlimit	整数	0,1	覆盖连接限制	否	1使能，0禁用，缺省值0
description	字符串
	长度1-191	描述	否	缺省值:空字符串
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.cookie.add
请求body：
{
  "name": "profile_persist_cookie_1",
  "expire_enable": 1,
  "description": "23", 
  "expire": 123,
  "method": 1, 
  "encrypt": 1, 
  "http_only": 1, 
  "secure": 1,
  "cookie_name": "name",
  "domain": "domain",
  "path": "path",
  "type": 2,
  "insert": 1,
  "ignore_connlimit": 1
}
Cookie保持编辑
Action：slb.persist.cookie.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	cookie连接保持名称	是	必须存在
expire_enable	整数	0,1	expire是否使能;	否	1：是；0：否;缺省值:不修改
expire	整数	0-30000000	超时时间	否	expire_enable为1时有效, 缺省值:不修改
method	整数	0,1,2	cookie保持方式	否	cookie保持方式，0插入，1重写，2被动
encrypt	整数	0,1,2	cookie加密	否	0不加密,1加密服务池名称,2全加密, 缺省值:不修改
encrypt_password	字符串	长度1-63	加密的密码	否	缺省的话为空，不显示
http_only	整数	0,1	使用http_only字段,	否	1:是,0:否, 缺省值:不修改
secure	整数	0,1	使用secure字段	否	1:是,0:否, 缺省值:不修改
cookie_name	字符串	长度1-63	cookie名称	否	缺省值:不修改
domain	字符串	长度1-31	域名	否	缺省值:不修改
path	字符串	长度1-31	路径	否	缺省值:不修改
type	整数	0,1,2	匹配方法	否	0端口，1节点，2服务池节点，3服务池，缺省值0
insert	整数	0,1	开启cookie插入	否	1使能，0禁用，缺省值:不修改
ignore_connlimit	整数	0,1	覆盖连接限制	否	1使能，0禁用，缺省值:不修改
description	字符串
	长度1-191	描述	否	缺省值:空字符串

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.cookie.edit
请求body：
{
  "name": "profile_persist_cookie_1",
  "expire_enable": 1,
  "expire": 123,
  "description": "34", 
  "method": 1, 
  "encrypt": 1, 
  "http_only": 1, 
  "secure": 1,
  "cookie_name": "name",
  "domain": "domain",
  "path": "path",
  "type": 2,
  "insert": 1,
  "ignore_connlimit": 1
}
Cookie保持删除
Action：slb.persist.cookie.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	cookie连接保持名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.cookie.del
请求body：
{
    "name": "profile_persist_cookie_1"
}

源地址连接保持
获取源IP地址保持模板列表
Action：slb.persist.srcip.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.srcip.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	源ip地址保持模版名称
type	整数	0,1,2	匹配方法，0端口，1节点，2服务池
timeout	整数	1-1800	超时,
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
with_port	整数	0,1	包含端口；1：是；0：否
netmask	掩码	不涉及	子网掩码
ipv6masklen	整数	0-128	ipv6前缀长度
conn_mirror	整数	0,1	连接镜像 1：是；0：否
description	字符串
	长度1-191	描述
响应举例：
[{
  "name": "p1",
  "type": 1,
  "timeout": 1012,                
  "ignore_connlimit": 1,
"description": "23", 
  "with_port": 0,
  "netmask": "255.255.255.0",
  "ipv6masklen": 23
}]


分区中获取common分区和自己分区的源地址列表
GET
http://{192.168.70.73/adcapi/v2.0/?authkey={{authkey}}&action=slb.persist.srcip.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	源ip地址保持模版名称
type	整数	0,1,2	匹配方法，0端口，1节点，2服务池
timeout	整数	1-1800	超时,
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
with_port	整数	0,1	包含端口；1：是；0：否
netmask	掩码	不涉及	子网掩码
ipv6masklen	整数	0-128	ipv6前缀长度
common_name	字符串	长度1-63	通用名称
conn_mirror	整数	0,1	连接镜像 1：是；0：否
description	字符串
	长度1-191	描述


[
    {
        "name": "12",
        "type": 0,
        "timeout": 10,
        "ignore_connlimit": 0,
        "with_port": 0,
"description": "23", 
        "netmask": "255.255.255.255",
        "ipv6masklen": 128,
        "conn_mirror": 0
    },
    {
        "name": "common/source-ip_1",
        "type": 0,
        "timeout": 20,
        "ignore_connlimit": 0,
        "with_port": 0,
"description": "23", 
        "netmask": "255.255.255.255",
        "ipv6masklen": 128,
        "conn_mirror": 0
    }
]


获取指定源IP地址保持模板
Action：slb.persist.srcip.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	源ip地址保持模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.srcip.get
请求body:
{
    "name": "p1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	源ip地址保持模版名称
type	整数	0,1,2	匹配方法，0端口，1节点，2服务池
timeout	整数	1-1800	超时,
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
with_port	整数	0,1	包含端口；1：是；0：否
netmask	掩码	不涉及	子网掩码
ipv6masklen	整数	0-128	ipv6前缀长度
conn_mirror	整数	0,1	连接镜像 1：是；0：否
description	字符串
	长度1-191	描述
响应举例：
{
  "name": "p1",
  "type": 1,
  "timeout": 1012,                
  "ignore_connlimit": 1,
"description": "23", 
  "with_port": 0,
  "netmask": "255.255.255.0",
  "ipv6masklen": 23
}
增加源IP地址保持模板
Action：slb.persist.srcip.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	源ip地址保持模版名称	是	唯一
type	整数	0,1,2	匹配方法	否	0端口，1节点，2服务池；缺省值0
timeout	整数	1-1800	超时时间,单位分钟	否	缺省值10
ignore_connlimit	整数	0,1	覆盖连接限制；	否	1：是；0：否；缺省值0
with_port	整数	0,1	包含端口；	否	1：是；0：否；缺省值0
netmask	掩码	不涉及	子网掩码	否	缺省值255.255.255.255
ipv6masklen	整数	0-128	ipv6前缀长度	否	缺省值128
conn_mirror	整数	0,1	连接镜像	否	1：是；0：否
description	字符串
	长度1-191	描述	否	缺省值:空字符串

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.srcip.add
请求body:
 {
        "name": "111",
        "type": 2,
        "timeout": 10,
        "ignore_connlimit": 1,
        "description":"23", 
        "with_port": 1,
        "netmask": "255.255.255.255",
        "ipv6masklen": 64,
        "conn_mirror": 1
} 


编辑源IP地址保持模板
Action：slb.persist.srcip.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	源IP地址保持模版名称	是	必须存在
type	整数	0,1,2	匹配方法	否	0端口，1节点，2服务池；缺省值0
timeout	整数	1-1800	超时时间,单位分钟	否	缺省值10
ignore_connlimit	整数	0,1	覆盖连接限制；	否	1：是；0：否；缺省值0
with_port	整数	0,1	包含端口；	否	1：是；0：否；缺省值0
netmask	掩码	不涉及	子网掩码	否	缺省值255.255.255.255
ipv6masklen	整数	0-128	ipv6前缀长度	否	缺省值128
conn_mirror	整数	0,1	连接镜像	否	 1：是；0：否
description	字符串
	长度1-191	描述	否	缺省值:空字符串

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.srcip.edit
请求body:
 {
        "name": "111",
        "type": 2,
        "timeout": 10,
        "ignore_connlimit": 1,
 "description": "23", 
        "with_port": 1,
        "netmask": "255.0.0.0",
        "ipv6masklen": 128,
        "conn_mirror": 1
}
删除源IP地址保持模板
Action：slb.persist.srcip.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	源IP地址保持模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.srcip.del
请求body:
{
    "name": "p1"
}

目的地址连接保持
获取目的IP地址保持模板列表
Action：slb.persist.dstip.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.dstip.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	目的ip地址保持模版名称
type	整数	0,1,2	匹配方法，0端口，1节点，2服务池
timeout	整数	1-1800	超时,
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
netmask	掩码	不涉及	子网掩码
ipv6masklen	整数	0-128	ipv6前缀长度
conn_mirror	整数	0,1	连接镜像
description	字符串
	长度1-191	描述

响应举例：
[{
  "name": "p1",
  "type": 2,
  "timeout": 34,
  "ignore_connlimit": 1,
"description": "23", 
  "netmask": "255.255.255.0",
  "ipv6masklen": 12，
  "conn_mirror": 1

}]
分区中获取common分区和自己分区的目的地址连接保持列表
GET
http://{192.168.70.73/adcapi/v2.0/?authkey={{authkey}}&action=slb.persist.dstip.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	源ip地址保持模版名称
type	整数	0,1,2	匹配方法，0端口，1节点，2服务池
timeout	整数	1-1800	超时,
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
with_port	整数	0,1	包含端口；1：是；0：否
netmask	掩码	不涉及	子网掩码
ipv6masklen	整数	0-128	ipv6前缀长度
common_name	字符串	长度1-63	通用名称
conn_mirror	整数	0,1	连接镜像
description	字符串
	长度1-191	描述

[
    {
        "name": "12",
        "type": 0,
        "timeout": 10,
        "ignore_connlimit": 0,
"description": "23", 
        "netmask": "255.255.255.255",
        "ipv6masklen": 0,
        "conn_mirror": 0
    },
    {
        "name": "common/source-ip_1",
        "type": 0,
        "timeout": 20,
        "ignore_connlimit": 0,
        "netmask": "255.255.255.255",
        "ipv6masklen": 0,
        "conn_mirror": 0
    }
]



获取指定目的IP地址保持模板
Action：slb.persist.dstip.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	目的ip地址保持模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.dstip.get
请求body：
{
    "name": "p1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	目的ip地址保持模版名称
type	整数	0,1,2	匹配方法，0端口，1节点，2服务池
timeout	整数	1-1800	超时,
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
netmask	掩码	不涉及	子网掩码
ipv6masklen	整数	0-128	ipv6前缀长度
conn_mirror	整数	0,1	连接镜像
description	字符串
	长度1-191	描述

响应举例：
{
  "name": "p1",
  "type": 2,
  "timeout": 34,
"description": "23", 

  "ignore_connlimit": 1,
  "netmask": "255.255.255.0",
  "ipv6masklen": 12，
  "conn_mirror": 1

}
增加目的IP地址保持模板
Action：slb.persist.dstip.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	目的ip地址保持模版名称	是	唯一
type	整数	0,1,2	匹配方法	否	0端口，1节点，2服务池；缺省值0
timeout	整数	1-1800	超时时间,单位分钟	否	缺省值10
ignore_connlimit	整数	0,1	覆盖连接限制；	否	1：是；0：否；缺省值0
netmask	掩码	不涉及	子网掩码	否	缺省值255.255.255.255
ipv6masklen	整数	0-128	ipv6前缀长度	否	缺省值128
conn_mirror	整数	0,1	连接镜像	否	 1：是；0：否
description	字符串
	长度1-191	描述	否	缺省值:空字符串

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.dstip.add
请求body：
{
  "name": "p1",
  "type": 2,
  "timeout": 34,
  "description":"23", 
  "ignore_connlimit": 1,
  "netmask": "255.255.255.0",
  "ipv6masklen": 12,
  "conn_mirror": 1

}
编辑目的IP地址保持模板
Action：slb.persist.dstip.edit
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	目的ip地址保持模版名称	是	必须存在
type	整数	0,1,2	匹配方法	否	0端口，1节点，2服务池；缺省值0
timeout	整数	1-1800	超时时间,单位分钟	否	缺省值10
ignore_connlimit	整数	0,1	覆盖连接限制；	否	1：是；0：否；缺省值0
netmask	掩码	不涉及	子网掩码	否	缺省值255.255.255.255
ipv6masklen	整数	0-128	ipv6前缀长度	否	缺省值128
conn_mirror	整数	0,1	连接镜像	否	 1：是；0：否
description	字符串
	长度1-191	描述	否	缺省值:空字符串
请求参数：

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.dstip.edit
请求body：
{
  "name":"p1",
  "type":2,
  "timeout":34,
  "ignore_connlimit":1,
  "description":"23", 
  "netmask":"255.255.255.0",
  "ipv6masklen":12,
  "conn_mirror":1

}
删除目的IP地址保持模板
Action：slb.persist.dstip.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	目的ip地址保持模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.dstip.del
请求body：
{
    "name": "p1"
}

SSL连接保持
获取SSL连接保持模板列表
Action：slb.persist.sslid.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.sslid.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	ssl连接保持模版名称
timeout	整数	1-1800	超时,
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
conn_mirror	整数	0,1	连接镜像
description	字符串
	长度1-191	描述

响应举例：
[{
  "name": "p1",
  "timeout": 1001,
"description": "23",
  "ignore_connlimit": 0，
  "conn_mirror": 1

}]
分区中获取common分区和自己分区的SSL连接保持列表
GET
http://{192.168.70.73/adcapi/v2.0/?authkey={{authkey}}&action=slb.persist.sslid.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	ssl连接保持模版名称
timeout	整数	1-1800	超时,
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
common_name	字符串	长度1-63	通用名称
conn_mirror	整数	0,1	连接镜像
description	字符串
	长度1-191	描述

    {
        "name": "common/ssl_persist_1",
        "timeout": 10,
"description": "23",
        "ignore_connlimit": 0,
        "conn_mirror": 0
    },
    {
        "name": "common/ssl_persist_10",
        "timeout": 10,
        "ignore_connlimit": 0,
        "conn_mirror": 0
    }
]

获取指定SSL连接保持模板
Action：slb.persist.sslid.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	ssl连接保持模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.sslid.get
请求body:
{
    "name": "p1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	ssl连接保持模版名称
timeout	整数	1-1800	超时,
ignore_connlimit	整数	0,1	覆盖连接限制；1：是；0：否
description	字符串
	长度1-191	描述

响应举例：
{
  "name": "p1",
  "timeout": 1001,
"description": "23",
  "ignore_connlimit": 0
}
增加SSL连接保持模板
Action：slb.persist.sslid.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	目的ip地址保持模版名称	是	唯一
timeout	整数	1-1800	超时时间,单位分钟	否	缺省值10
ignore_connlimit	整数	0,1	覆盖连接限制；	否	1：是；0：否；缺省值0
conn_mirror
	整数	0,1	连接镜像	否	1：是；0：否；缺省值0
description	字符串
	长度1-191	描述	否	缺省值:空字符串

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.sslid.add
请求body:
{
  "name":"p1",
  "timeout":1001,
  "ignore_connlimit":0,
  "conn_mirror":1,
  "description":"23"

}
编辑SSL连接保持模板
Action：slb.persist.sslid.edit
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	ssl连接保持模版名称	是	必须存在
timeout	整数	1-1800	超时时间,单位分钟	否	缺省值10
ignore_connlimit	整数	0,1	覆盖连接限制；	否	1：是；0：否；缺省值0
conn_mirror	整数	0,1	连接镜像	否	 1：是；0：否
description	字符串
	长度1-191	描述	否	缺省值:空字符串

POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.sslid.edit
请求body:
{
  "name":"p1",
  "timeout":1001,
  "ignore_connlimit":0,
  "conn_mirror":1,
  "description":"232222"

}
删除SSL连接保持模板
Action：slb.persist.sslid.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	ssl连接保持模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.persist.sslid.del
请求body:
{
    "name": "p1"
}

加速
缓存
获取当前分区缓存模板列表
Action：slb.cache.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.cache.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	缓存模版名称
age	整数	1-999999	最长保存时间
size_max	整数	1-16384	最大缓存数量
object_min	整数	1-268435455	最小对象大小,单位字节
object_max	整数	1-268435455	最大对象大小,单位字节
handle_reload_req	整数	0，1	缓存控制头；0禁用1使能
cache_host	整数	0，1	缓存主机名
no_cache	整数	0，1	默认不缓存
no_age_header	整数	0，1	不插入age头
no_via_header	整数	0，1	不插入via头
cache_policy	数组	最多支持16个策略	缓存策略对象组成的数组,根据URL设定缓存
cache_policy > url: 
类型：字符串，
范围：1-63，
含义：缓存策略-URL，匹配URL后使用本策略
cache_policy > match:
类型：字符串，
范围：1-63，
含义：缓存策略-匹配字符串,匹配字符串刷新存活时间
cache_policy > age: 
类型：整数,
范围：1-900000，
含义：缓存策略-缓存保存时间
cache_policy > action: 
类型：整数，
含义：缓存策略-算法：0缓存；1禁用缓存；2刷新
       范围：0-2

description	字符串
	长度1-191	描述
响应举例：
[{
  "name": "p1",
  "age": 3001,
"description": "23",
  "size_max": 101,
  "object_min": 501,
  "object_max": 50001,
  "handle_reload_req": 1,
  "cache_host": 1,
  "no_cache": 1,
  "no_age_header": 1,
  "no_via_header": 1,
  "cache_policy": [
    {
      "url": "/url",
      "match": "",
      "age": 0,
      "action": 1
    },
    {
      "url": "/url2",
      "match": "asdsa",
      "age": 0,
      "action": 2
    }
  ]
}]
获取common及本分区缓存模板列表
Action：slb.cache.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.cache.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	缓存模版名称
age	整数	1-999999	最长保存时间
size_max	整数	1-16384	最大缓存数量
object_min	整数	1-268435455	最小对象大小,单位字节
object_max	整数	1-268435455	最大对象大小,单位字节
handle_reload_req	整数	0，1	缓存控制头；0禁用1使能
cache_host	整数	0，1	缓存主机名
no_cache	整数	0，1	默认不缓存
no_age_header	整数	0，1	不插入age头
no_via_header	整数	0，1	不插入via头
cache_policy	数组	最多支持16个策略	缓存策略对象组成的数组,根据URL设定缓存
cache_policy > url: 
类型：字符串，
范围：1-63，
含义：缓存策略-URL，匹配URL后使用本策略
cache_policy > match:
类型：字符串，
范围：1-63，
含义：缓存策略-匹配字符串,匹配字符串刷新存活时间
cache_policy > age: 
类型：整数,
范围：1-900000，
含义：缓存策略-缓存保存时间
cache_policy > action: 
类型：整数，
含义：缓存策略-算法：0缓存；1禁用缓存；2刷新
       范围：0-2

description	字符串
	长度1-191	描述
响应举例：
[{
  "name": "common/p1",
  "age": 3001,
  "size_max": 101,
"description": "23",
  "object_min": 501,
  "object_max": 50001,
  "handle_reload_req": 1,
  "cache_host": 1,
  "no_cache": 1,
  "no_age_header": 1,
  "no_via_header": 1,
  "cache_policy": [
    {
      "url": "/url",
      "match": "",
      "age": 0,
      "action": 1
    },
    {
      "url": "/url2",
      "match": "asdsa",
      "age": 0,
      "action": 2
    }
  ]
}]

获取指定缓存模板
Action：slb.cache.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	缓存模版名称	是	必须存在
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.cache.get
请求body：
{
    "name": "p0"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	缓存模版名称
age	整数	1-999999	最长保存时间
size_max	整数	1-16384	最大缓存数量
object_min	整数	1-268435455	最小对象大小,单位字节
object_max	整数	1-268435455	最大对象大小,单位字节
handle_reload_req	整数	0，1	缓存控制头；0禁用1使能
cache_host	整数	0，1	缓存主机名
no_cache	整数	0，1	默认不缓存
no_age_header	整数	0，1	不插入age头
no_via_header	整数	0，1	不插入via头
cache_policy	数组	最多支持16个策略	缓存策略对象组成的数组,根据URL设定缓存
cache_policy > url: 
类型：字符串，
范围：1-63，
含义：缓存策略-URL，匹配URL后使用本策略
cache_policy > match:
类型：字符串，
范围：1-63，
含义：缓存策略-匹配字符串,匹配字符串刷新存活时间
cache_policy > age: 
类型：整数,
范围：1-900000，
含义：缓存策略-缓存保存时间
cache_policy > action: 
类型：整数，
含义：缓存策略-算法：0缓存；1禁用缓存；2刷新
       范围：0-2

description	字符串
	长度1-191	描述

响应举例：
{
  "name": "p1",
  "age": 3001,
  "size_max": 101,
"description": "23",
  "object_min": 501,
  "object_max": 50001,
  "handle_reload_req": 1,
  "cache_host": 1,
  "no_cache": 1,
  "no_age_header": 1,
  "no_via_header": 1,
  "cache_policy": [
    {
      "url": "/url",
      "match": "",
      "age": 0,
      "action": 1
    },
    {
      "url": "/url2",
      "match": "asdsa",
      "age": 0,
      "action": 2
    }
  ]
}
增加缓存模板
Action：slb.cache.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	缓存模版名称	是	唯一
age	整数	1-999999	最长保存时间	否	缺省值:3600
size_max	整数	1-16384	最大缓存数量	否	缺省值:80
object_min	整数	1-268435455	最小对象大小,单位字节	否	缺省值:512
object_max	整数	1-268435455	最大对象大小,单位字节	否	缺省值:81920
handle_reload_req	整数	0，1	缓存控制头	否	0禁用1使能，缺省值:0
cache_host	整数	0，1	缓存主机名	否	0禁用1使能，缺省值:0
no_cache	整数	0，1	默认不缓存	否	0禁用1使能，缺省值:0
no_age_header	整数	0，1	不插入age头	否	0禁用1使能，缺省值:0
no_via_header	整数	0，1	不插入via头	否	0禁用1使能，缺省值:0
cache_policy	数组	最多支持16个策略	缓存策略对象组成的数组,根据url设定缓存
cache_policy > url: 
类型：字符串，
范围：1-63，
含义：缓存策略-URL，匹配URL后使用本策略
cache_policy > match:
类型：字符串，
范围：1-63，
含义：缓存策略-匹配字符串,匹配字符串刷新存活时间
cache_policy > age: 
类型：整数,
范围：1-900000，
含义：缓存策略-缓存保存时间
cache_policy > action: 
类型：整数，
含义：缓存策略-算法：0缓存；1禁用缓存；2刷新
       范围：0-2
	否	缺省值:[]无缓存策略
url: 字符串，长度1-63，缓存策略-url，匹配url后使用本策略
match:字符串，长度1-63，缓存策略-匹配字符串,匹配字符串刷新存活时间
age: 整数,1-900000，缓存策略-缓存保存时间
action: 整数，缓存策略-算法：0缓存；1禁用缓存；2刷新

description	字符串
	长度1-191	描述	否	缺省值:空字符串
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.cache.add
请求body：
{
  "name": "p1",
  "age": 3001,
  "size_max": 101,
  "description":"23",
  "object_min": 501,
  "object_max": 50001,
  "handle_reload_req": 1,
  "cache_host": 1,
  "no_cache": 1,
  "no_age_header": 1,
  "no_via_header": 1,
  "cache_policy": [
    {
      "url": "/url",
      "match": "",
      "age": 0,
      "action": 1
    },
    {
      "url": "/url2",
      "match": "asdsa",
      "age": 0,
      "action": 2
    }
  ]
}
编辑缓存模板
Action：slb.cache.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	缓存模版名称	是	必须存在
age	整数	1-999999	最长保存时间	否	缺省值:3600
size_max	整数	1-16384	最大缓存数量	否	缺省值:80
object_min	整数	1-268435455	最小对象大小,单位字节	否	缺省值:512
object_max	整数	1-268435455	最大对象大小,单位字节	否	缺省值:81920
handle_reload_req	整数	0，1	缓存控制头	否	0禁用1使能，缺省值:0
cache_host	整数	0，1	缓存主机名	否	0禁用1使能，缺省值:0
no_cache	整数	0，1	默认不缓存	否	0禁用1使能，缺省值:0
no_age_header	整数	0，1	不插入age头	否	0禁用1使能，缺省值:0
no_via_header	整数	0，1	不插入via头	否	0禁用1使能，缺省值:0
cache_policy	数组	最多支持16个策略	缓存策略对象组成的数组,根据url设定缓存
cache_policy > url: 
类型：字符串，
范围：1-63，
含义：缓存策略-URL，匹配URL后使用本策略
cache_policy > match:
类型：字符串，
范围：1-63，
含义：缓存策略-匹配字符串,匹配字符串刷新存活时间
cache_policy > age: 
类型：整数,
范围：1-900000，
含义：缓存策略-缓存保存时间
cache_policy > action: 
类型：整数，
含义：缓存策略-算法：0缓存；1禁用缓存；2刷新
       范围：0-2
	否	缺省值:[]无缓存策略
url: 字符串，长度1-63，缓存策略-url，匹配url后使用本策略
match:字符串，长度1-63，缓存策略-匹配字符串,匹配字符串刷新存活时间
age: 整数,1-900000，缓存策略-缓存保存时间
action: 整数，缓存策略-算法：0缓存；1禁用缓存；2刷新

description	字符串
	长度1-191	描述	否	缺省值:空字符串

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.cache.edit
请求body：
{
  "name": "p1",
  "age": 30001,
  "size_max": 1001,
  "description":"203",
  "object_min": 501,
  "object_max": 50001,
  "handle_reload_req": 1,
  "cache_host": 1,
  "no_cache": 1,
  "no_age_header": 1,
  "no_via_header": 1,
  "cache_policy": [
    {
      "url": "/url",
      "match": "",
      "age": 0,
      "action": 1
    },
    {
      "url": "/url2",
      "match": "asdsa",
      "age": 0,
      "action": 2
    }
  ]
}
删除缓存模板
Action：slb.cache.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	缓存模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.cache.del
请求body：
{
    "name": "p1"
}
连接复用
获取当前分区连接复用模板列表
Action：slb.connmulti.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.connmulti.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	连接复用模版名称
limit	整数	0-65535	最大重用数量
timeout	整数	1-3600	最大重用数量
description	字符串
	长度1-191	描述
响应举例：
[{
  "name": "p1",
  "limit": 1025,
"description": "23",
  "timeout": 1801
}]
获取common及本分区连接复用模板列表
Action：slb.connmulti.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.connmulti.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	连接复用模版名称
limit	整数	0-65535	最大重用数量
timeout	整数	1-3600	最大重用数量
description	字符串
	长度1-191	描述
响应举例：
[{
  "name": "common/p1",
  "limit": 1025,
"description": "23",
  "timeout": 1801
}]

获取指定连接复用模板
Action：slb.connmulti.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	连接复用模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.connmulti.get
请求body：
{
    "name": "p0"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-63	连接复用模版名称
limit	整数	0-65535	最大重用数量
timeout	整数	1-3600	最大重用数量
description	字符串
	长度1-191	描述
响应举例：
{
  "name": "p1",
  "limit": 1025,
  "timeout": 1801
}
增加连接复用模板
Action：slb.connmulti.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	连接复用模版名称	是	唯一
limit	整数	0-65535	最大重用数量	否	缺省值:1024
timeout	整数	1-3600	最大重用数量	否	缺省值:1800
description	字符串
	长度1-191	描述	否	缺省值:空字符串

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.connmulti.add
请求body：
{
  "name":"p1",
  "description":"23",
  "limit":1025,
  "timeout": 1801
}
编辑连接复用模板
Action：slb.connmulti.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	连接复用模版名称	是	必须存在
limit	整数	0-65535	最大重用数量	否	缺省值:1024
timeout	整数	1-3600	最大重用数量	否	缺省值:1800
description	字符串
	长度1-191	描述	否	缺省值:空字符串


请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.connmulti.edit
请求body：
{
  "name":"p1",
  "description":"23000",
  "limit":1025,
  "timeout": 1801
}
删除连接复用模板
Action：slb.connmulti.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	连接复用模版名称	是	必须存在
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.connmulti.del
请求body：
{
    "name": "p1"
}
SSL卸载
证书管理
证书上传
Action:  slb.ssl.certificate.upload
请求参数:无
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.ssl.certificate.upload

	此API需要使用form-data的方式上传证书文件



私钥上传
Action:  slb.ssl.key.upload
请求参数:无
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.ssl.key.upload&password=root

	此API需要使用form-data的方式上传私钥文件
如果私钥没有密码，请将password之后的值置为空



证书吊销列表上传
Action:  slb.ssl.crl.upload
请求参数:无
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.ssl.crl.upload

	此API需要使用form-data的方式上传证书吊销列表文件

PFX证书上传
Action:  slb.ssl.pfx.upload
请求参数:
名称	类型	范围	含义	必选	备注
password	字符串		证书密码	否	

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.ssl.pfx.upload&password=admin

	1.此API需要使用form-data的方式上传pfx证书文件
2.此API参数在URL中指定而不是在BODY中
3.上传pfx证书会产生一个证书和一个私钥，如要删除需分别删除。
4.如果私pfx不携带密码，请将password之后的值置为空



证书删除
Action:  slb.ssl.certificate.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-255	证书名称	是	

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.ssl.certificate.del
请求body
{
    "name": "csr2"          
}




私钥删除
Action:  slb.ssl.key.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-63	私钥名称	是	

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.ssl.key.del
请求body
{
    "name": "csr2"          
}



获取SSL证书列表
Action:  slb.ssl.certificate.list
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.ssl.certificate.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	名称
type	字符串	证书类型
	类型字段说明：
certificate  证书
key       私钥
certificate-key  证书和私钥
crl           吊销列表
common_name	字符串	长度1-64	通用名称
organization	字符串	长度1-64	组织
key_size	整数	256/512/1024/2048/4096	密钥长度
expiration_time	字符串		证书过期时间显示
响应举例：
[
    {
        "name": "cert.name",
        "type": "certificate",
        "common_name": "common_name",
        "organization": "test",
        "key_size": 2048,
        "expiration_time": "Feb 27 05:21:11 2034 GMT"
}
]
获取common和自己分区的SSL证书列表
Action:  slb.ssl.certificate.list.withcommon
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.ssl.certificate.list.withcommon
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	名称
type	字符串	证书类型
	类型字段说明：
certificate  证书
key       私钥
certificate-key  证书和私钥
crl           吊销列表
common_name	字符串	长度1-64	通用名称
organization	字符串	长度1-64	组织
key_size	整数	256/512/1024/2048/4096	密钥长度
expiration_time	字符串		证书过期时间显示
响应举例：
[
    {
        "name": "common/cert.crt",
        "type": "certificate",
        "common_name": "123.com",
        "organization": "horizon",
        "key_size": 2048,
        "expiration_time": "Oct 16 05:35:55 2032 GMT"
}
]

获取SSL证书
Action:  system.sys.cert.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	证书名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=system.sys.cert.get
请求body:
{
    "name": "cert_name"
}

响应参数：

名称	类型	范围	含义
name	字符串	长度1-191	证书名称
type	字符串	证书类型
	类型字段说明：
certificate  证书
key       私钥
certificate-key  证书和私钥
crl           吊销列表
issuer	字符串	CA/Self	显示发行者
common_name	字符串	长度1-64	通用名称
organization	字符串	长度1-64	组织
division	字符串	长度1-64	部门
locality	字符串	长度1-128	位置（城市）
state_province	字符串	长度1-128	州/省
country	整数	长度2	国家
email	字符串	长度1-64	email
start_time	字符串		证书有效期起始时间
expiration	字符串		证书有效期过期时间
key_type	字符串	几种公钥类型	公钥类型说明：
id-ecPublicKey
rsa
sm2
version	字符串	版本	版本说明：
V1 V2 V3
serial_number	字符串		显示证书的序列号
fingerprint	字符串	摘要/指纹	显示根据摘要生成的指纹
subjectaltname	字符串	标准ipv4地址或者ipv6地址或者域名	使用者别名扩展项（subject altnative name）的具体内容
key_size	整数	公钥长度	公钥长度说明：
256/512/1024/2048/4096


响应举例：

{
    "name": "cert_name",
    "type": "certificate",
    "issuer": "Self",
    "common_name": "beijing",
    "organization": "",
    "division": "",
    "locality": "",
    "state_province": "",
    "country": "CN",
    "email": "",
    "start_time": "Mar 11 08:55:05 2024 GMT",
    "expiration": "Mar 11 08:55:05 2025 GMT",
    "key_type": "rsa",
    "version": "V1",
    "serial_number": "06f528a94da8ffed4fe8eff019d0c1536818d755",
    "fingerprint": "SHA1/2E:4F:3A:2B:CD:98:E4:87:24:27:B5:B9:14:AD:36:BE:BF:0C:BD:BA ",
    "subjectaltname": "",
    "key_size": 1024
}
生成ssl自签名证书
Action:  slb.ssl.certificate.add
请求参数:
名称	类型	范围	含义	必选	备注
issuer	字符串	ca	固定写ca表示是自签名	是	
name	字符串	长度1-191	证书名称	是	唯一
common_name	字符串	长度1-64	通用名称	是	
type	整数	1/2/3	证书类型	是	1.RSA 2. SM2 3.ecdsa
division	字符串	长度1-64	部门	否	缺省值:"" 空字符串
organization	字符串	长度1-64	组织	否	缺省值:"" 空字符串
locality	字符串	长度1-128	位置（城市）	否	缺省值:"" 空字符串
state	字符串	长度1-128	州/省	否	缺省值:"" 空字符串
country	整数	长度2	国家	否	缺省值:CN
email	字符串	长度1-64	email	否	缺省值:"" 空字符串
key_size	整数	512/1024/2048/4096	密钥长度	否	缺省值:1024
days	整数	1-3650	证书有效天数	否	缺省值:365
md_type	整数	64/672/673/674/675	摘要算法	否	64：SHA1  672：SHA256  673：SHA384 674：SHA512 675: SHA224 
subjectaltname_type	整数	0/1/2/3/4	使用者别名扩展项（subject altnative name）的类型		0代表不携带SAN字段；
1代表DNS字段，此时需要输入subjectaltname字段为域名;长度为1-255
2代表ipv4字段，此时需要输入subjectaltname字段为ipv4地址;
3代表ipv6字段，此时需要输入subjectaltname字段为ipv6地址;

subjectaltname	字符串	标准ipv4地址或者ipv6地址或者域名	使用者别名扩展项（subject altnative name）的具体内容		

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.ssl.certificate.add
请求body
1.RSA类型自签名证书生成：
{
 "issuer":"ca",                
"name":"mysert1",       
"type"  :  "1",
"common_name":"adc.com", 
"division":"division",
"organization":"organization",
"locality":"locality",
"state":"Beijing",
"country":"CN",              
"email":"a@b.c",
"key_size":2048,     
"md_type" : "674"   ,         
"days":345  ,
"subjectaltname_type":3 ,
"subjectaltname":"2001::1000"              
}

2.ECC类型自签名证书生成：
{
    "issuer":"ca",                
"name":"mysert1",       
 "type"  :  "3",
    "common_name":"adc.com", 
    "division":"division",
    "organization":"organization",
    "locality":"locality",
"state":"Beijing",
"country":"CN",              
"email":"a@b.c",        
"md_type" : "674"   ,
    "days":345                    
}
3.国密类型自签名证书生成：
{
    "issuer":"ca",                
"name":"mysert1",       
 "type"  :  "2",
    "common_name":"adc.com", 
    "division":"division",
    "organization":"organization",
    "locality":"locality",
    "state":"Beijing",
"country":"CN",              
"email":"a@b.c",        
    "days":345                    
}


获取CSR证书
Action:  system.sys.csr.get
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	证书名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=system.sys.csr.get
请求body:
{
    "name": "csr_name"
}

响应参数：

名称	类型	范围	含义
name	字符串	长度1-191	证书名称
common_name	字符串	长度1-64	通用名称
division	字符串	长度1-64	部门
organization	字符串	长度1-64	组织
locality	字符串	长度1-128	位置（城市）
state_province	字符串	长度1-128	州/省
country	整数	长度2	国家
email	字符串	长度1-64	email
key_type	字符串	几种公钥类型	公钥类型说明：
rsassaPss
id-ecPublicKey
rsa
subjectaltname	字符串	标准ipv4地址或者ipv6地址或者域名	使用者别名扩展项（subject altnative name）的具体内容
key_size	整数	256/512/1024/2048/4096	密钥长度
md_type	字符串	摘要类型	摘要类型说明：
SHA1  SHA256  SHA384 SHA512  SHA224   SM3  


响应举例：

{
    "name": "csr_name",
    "common_name": "adc.com",
    "organization": "",
    "division": "division",
    "locality": "locality",
    "state_province": "Beijing",
    "country": "CN",
    "email": "",
    "key_type": "rsassaPss",
    "subjectaltname": "IP Address:1.1.1.1",
    "key_size": 2048,
    "md_type": "SHA256"
}
生成CSR
Action:  slb.ssl.certificate.add
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	CSR名称	是	唯一
common_name	字符串	长度1-64	通用名称	是	
type	整数	1/2/3	CSR类型	是	1：RSA 2： SM2 3：ecdsa
division	字符串	长度1-64	部门	否	缺省值:"" 空字符串
organization	字符串	长度1-64	组织	否	缺省值:"" 空字符串
locality	字符串	长度1-128	位置（城市）	否	缺省值:"" 空字符串
state	字符串	长度1-128	州/省	否	缺省值:"" 空字符串
country	字符串	长度 2	国家	否	缺省值:CN
email	字符串	长度1-64	email	否	缺省值:"" 空字符串
password	字符串	长度4-64	密码	否	缺省值:"" 空字符串
confirm_password	字符串	长度4-64	确认密码	否	需要和密码字段一起配置，缺省值:"" 空字符串
key_size	整数	512/1024/2048/4096	密钥长度	否	缺省值:1024
md_type	整数	64/672/673/674/675	摘要算法	否	64：SHA1  672：SHA256  673：SHA384 674：SHA512 675: SHA224 
padding_type	字符串	PKCSv1.5/RSASSA-PSS	RSA证书的填充类型	否	当填充类型配置PKCSv1.5时，摘要类型SHA1 SHA256 SHA384 SHA512 SHA224 ；当填充类型配置RSASSA-PSS时，摘要类型 SHA256 SHA384  SHA512

ecc_group	字符串	Prime256v1/secp384r1/secp521r1	ECC曲线	否	
subjectaltname_type	整数	0/1/2/3/4	使用者别名扩展项（subject altnative name）的类型		0代表不携带SAN字段；
1代表DNS字段，此时需要输入subjectaltname字段为域名;长度为1-255
2代表ipv4字段，此时需要输入subjectaltname字段为ipv4地址;
3代表ipv6字段，此时需要输入subjectaltname字段为ipv6地址;

subjectaltname	字符串	标准ipv4地址或者ipv6地址或者域名	使用者别名扩展项（subject altnative name）的具体内容		

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=system.sys.csr.add
请求body
1.国密CSR生成body:
{                  
"name":"csr",      
"type":"2",            
"common_name":"adc.com",
"division":"division",
"organization":"",
"locality":"locality",
"state":"Beijing",
"country":"CN",
"email":"@",
"password":"123456",
"confirm_password":"123456",
"subjectaltname_type": 2,
"subjectaltname": "1.1.1.1"
}
2.RSA类型CSR生成body:
{                  
"name":"csr",                  
"type":"1",
"common_name":"adc.com",
"division":"division",
"organization":"",
"locality":"locality",
"state":"Beijing",
"country":"CN",
"email":"@",
"key_size":"2048",
"padding_type":"RSASSA-PSS",
"md_type" : "672",
"password":"123456",
"confirm_password":"123456",
"subjectaltname_type": 2,
"subjectaltname": "1.1.1.1"
}
3.ECC 类型的CSR生成body:
{                  
"name":"csr",  
"type":"3",                
"common_name":"adc.com",
 "division":"division",
 "organization":"",
 "locality":"locality",
 "state":"Beijing",
 "country":"CN",
"email":"@",
"ecc_group" : "secp521r1",
"md_type" : "672",
"password":"123456",
"confirm_password":"123456",
"subjectaltname_type": 2,
"subjectaltname": "1.1.1.1"
}
SSL过滤证书列表
Action:  slb.ssl.fitercert.list

请求参数:
名称	类型	范围	含义	必选	备注
type	字符串	all
cert
key
crl	搜索全部
搜索证书
搜索私钥
搜索crl	是	只允许输入范围中的几种类型
name	字符串	长度1-191	过滤名称	可选	适用于all/cert/key/crl
current	字符串	只允许设置数字，0或者不填为不过滤，非0为过滤出当前已过期证书	当前时间	可选	只适用于cert
并且curernt/custom/months/weeks/days只支持配置一个
custom	字符串	“YYYY-MM-DD HH:MM:SS”	自定义搜索时间	可选	只适用于cert
并且curernt/custom/months/weeks/days只支持配置一个
months	字符串	1-600	最近月数	可选	只适用于cert
并且curernt/custom/months/weeks/days只支持配置一个
weeks	字符串	1-2400	最近周数	可选	只适用于cert
并且curernt/custom/months/weeks/days只支持配置一个
days	字符串	1-18250	最近天数	可选	只适用于cert
并且curernt/custom/months/weeks/days只支持配置一个

请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.ssl.filtercert.list
过滤名字中有new字符串，600个月内有效期的证书。
请求body
{
"type":"cert",
"name":"new",
"months":"600"               
}
响应参数：

名称	类型	范围	含义
total	字符串		显示过滤的信息条数
name	字符串	长度1-191	名称
type	字符串	证书类型
	类型字段说明：
certificate  证书
key       私钥
certificate-key  证书和私钥
crl           吊销列表
common_name	字符串	长度1-64	通用名称
organization	字符串	长度1-64	组织
key_size	整数	256/512/1024/2048/4096	密钥长度
expiration_time	字符串		证书过期时间显示

响应举例：

{
    "total": 3,
    "Cert": [
        {
            "name": "newcert1.pem",
            "type": "certificate",
            "common_name": "123.com",
            "organization": "horizon",
            "key_size": 2048,
            "expiration_time": "May 26 08:35:02 2034 GMT"
        },
        {
            "name": "newcert2.pem",
            "type": "certificate-key",
            "common_name": "123.com",
            "organization": "horizon",
            "key_size": 256,
            "expiration_time": "May 26 08:34:38 2034 GMT"
        },
        {
            "name": "newcert3.pem",
            "type": "certificate",
            "common_name": "123.com",
            "organization": "horizon",
            "key_size": 256,
            "expiration_time": "May 26 08:34:15 2034 GMT"
        }
    ]
}

证书地图
Action:  action=system.sys.cert.relevance
请求参数：

名称	范围	含义	必选	备注
name	长度1-255	证书名称	是	必须存在

请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=system.sys.cert.relevance
请求body
{
    "name": "client.crt"
}
响应参数：

名称	类型	范围	含义
total	字符串	不涉及	显示证书被引用的数量
VSS	字符串	不涉及	显示证书地图
virtual server	字符串	长度1-191	显示VS 的名称
virtual address	字符串	不涉及	显示VS 的ip地址
port	整数	范围 0-65534	显示VS的端口
ssl_client_name	字符串	长度1-191	显示SSL客户端模版
ssl_server_name	字符串	长度1-191	显示SSL服务端模版

响应举例：
{
    "total": 1,
    "vss": [
        {
            "virtual server": "85.1.3.99",
            "virtual address": "85.1.3.99",
            "port": 5443,
            "ssl_client_name": "client",
            "ssl_server_name": "server"
        }
    ]
}

服务器SSL卸载
服务端SSL卸载模板列表
Action：slb.sslserver.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.sslserver.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	服务端SSL卸载模版名称
cert	字符串	长度1-255	证书名称
key	字符串	长度1-255	私钥名称
password	字符串	长度1-46	密码
ecert	字符串	长度1-255	国密加密证书名称
ekey	字符串	长度1-255	国密加密私钥名称
epassword	字符串	长度1-46	国密加密证书密码
ca_cert	字符串	长度1-255	CA证书名称
ssl_version	整数	0,1,2,3，5，6	版本；0：SSL v3.0 ；1：TLS v1.0 ；2：TLS v1.1，3：TLS v1.2， 5：TLS v1.3 ，6: GMTLSv1.1
sni_switch	整数	0，1	0：关闭SNI   ； 1：开启SNI
sni_name	字符串	长度1-191	SNI名称
cipher_suite	数组	不涉及	加密算法列表，支持以下算法：
             "GM1_ECDHE_SM4_GCM_SM3",
            "GM1_ECDHE_SM4_SM3",
            "GM1_ECC_SM4_GCM_SM3",
            "GM1_ECC_SM4_SM3",
            "TLS1_RSA_EXPORT1024_RC4_56_MD5",
            "TLS1_RSA_EXPORT1024_RC4_56_SHA",
            "SSL3_RSA_RC4_40_MD5",
            "SSL3_RSA_RC4_128_MD5",
            "SSL3_RSA_RC4_128_SHA",
            "SSL3_RSA_DES_40_CBC_SHA",
            "SSL3_RSA_DES_64_CBC_SHA",
            "SSL3_RSA_DES_192_CBC3_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
            "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS1_RSA_AES_256_SHA",
            "TLS1_RSA_AES_128_SHA",
            "TLS1_RSA_AES_256_SHA256",
            "TLS1_RSA_AES_128_SHA256",
            "TLS1_RSA_WITH_AES_256_GCM_SHA384",
            "TLS1_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_SM4_CCM_SM3",
            "TLS_SM4_GCM_SM3",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "TLS_AES_128_GCM_SHA256"
sign_cipher
	数组	不涉及	签名算法列表，支持以下签名算法：           
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
响应举例：
[
    {
        "name": "api-ssl_server",
        "description": "",
        "cert": "client.crt",
        "key": "client.key",
        "ca_cert": "",
        "password": "******",
        "ecert": "",
        "ekey": "",
        "epassword": "******",
        "ssl_version": 3,
        "sni_switch": 1,
        "sni_name": "www.123.com",
        "sign_cipher": [
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
        ],
        "cipher_suite": [
            "TLS1_RSA_AES_128_SHA",
            "TLS1_RSA_AES_256_SHA",
            "TLS1_RSA_EXPORT1024_RC4_56_MD5",
            "TLS1_RSA_EXPORT1024_RC4_56_SHA",
            "TLS1_RSA_AES_128_SHA256",
            "TLS1_RSA_AES_256_SHA256",
            "SSL3_RSA_DES_40_CBC_SHA",
            "SSL3_RSA_DES_64_CBC_SHA",
            "SSL3_RSA_DES_192_CBC3_SHA",
            "SSL3_RSA_RC4_40_MD5",
            "SSL3_RSA_RC4_128_MD5",
            "SSL3_RSA_RC4_128_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
            "TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
            "TLS1_RSA_WITH_AES_128_GCM_SHA256",
            "TLS1_RSA_WITH_AES_256_GCM_SHA384",
            "GM1_ECC_SM4_SM3",
            "GM1_ECDHE_SM4_SM3",
            "GM1_ECDHE_SM4_GCM_SM3",
            "GM1_ECC_SM4_GCM_SM3",
            "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_AES_128_GCM_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_SM4_GCM_SM3",
            "TLS_SM4_CCM_SM3"
        ]
    }
]
获取common以及自己分区下的服务端SSL卸载模板列表
Action：slb.sslserver.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.sslserver.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	服务端SSL卸载模版名称
cert	字符串	长度1-255	证书名称
key	字符串	长度1-255	私钥名称
password	字符串	长度1-46	密码
ecert	字符串	长度1-255	国密加密证书名称
ekey	字符串	长度1-255	国密加密私钥名称
epassword	字符串	长度1-46	国密加密证书密码
ca_cert	字符串	长度1-255	CA证书名称
ssl_version	整数	0,1,2,3，5，6	版本；0：SSL v3.0 ；1：TLS v1.0 ；2：TLS v1.1，3：TLS v1.2，5：TLS v1.3 ，6: GMTLSv1.1
sni_switch	整数	0，1	0：关闭SNI功能；1：开启SNI功能
sni_name	字符串	长度1-191	SNI名称
cipher_suite	数组	不涉及	加密算法列表，支持以下算法：
            "GM1_ECDHE_SM4_GCM_SM3",
            "GM1_ECDHE_SM4_SM3",
            "GM1_ECC_SM4_GCM_SM3",
            "GM1_ECC_SM4_SM3",
            "TLS1_RSA_EXPORT1024_RC4_56_MD5",
            "TLS1_RSA_EXPORT1024_RC4_56_SHA",
            "SSL3_RSA_RC4_40_MD5",
            "SSL3_RSA_RC4_128_MD5",
            "SSL3_RSA_RC4_128_SHA",
            "SSL3_RSA_DES_40_CBC_SHA",
            "SSL3_RSA_DES_64_CBC_SHA",
            "SSL3_RSA_DES_192_CBC3_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
            "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS1_RSA_AES_256_SHA",
            "TLS1_RSA_AES_128_SHA",
            "TLS1_RSA_AES_256_SHA256",
            "TLS1_RSA_AES_128_SHA256",
            "TLS1_RSA_WITH_AES_256_GCM_SHA384",
            "TLS1_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_SM4_CCM_SM3",
            "TLS_SM4_GCM_SM3",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "TLS_AES_128_GCM_SHA256"
sign_cipher
	数组	不涉及	签名算法列表，支持以下签名算法：           
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
响应举例：
[
    {
        "name": "api-ssl_server",
        "description": "",
        "cert": "client.crt",
        "key": "client.key",
        "ca_cert": "",
        "password": "******",
        "ecert": "",
        "ekey": "",
        "epassword": "******",
        "ssl_version": 3,
        "sni_switch": 1,
        "sni_name": "www.123.com",
        "sign_cipher": [
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
        ],
        "cipher_suite": [
            "TLS1_RSA_AES_128_SHA",
            "TLS1_RSA_AES_256_SHA",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
            "GM1_ECDHE_SM4_SM3",
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"
        ]
    },
    {
        "name": "common/asd",
        "description": "",
        "cert": "",
        "key": "",
        "ca_cert": "",
        "password": "******",
        "ecert": "",
        "ekey": "",
        "epassword": "******",
        "ssl_version": 3,
        "sni_switch": 0,
        "sign_cipher": [
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
        ],
        "cipher_suite": [
            "TLS1_RSA_AES_128_SHA",
            "TLS1_RSA_AES_256_SHA",
            "TLS1_RSA_EXPORT1024_RC4_56_MD5",
            "TLS1_RSA_EXPORT1024_RC4_56_SHA",
            "TLS1_RSA_AES_128_SHA256",
            "TLS1_RSA_AES_256_SHA256",
            "SSL3_RSA_DES_40_CBC_SHA",
            "SSL3_RSA_DES_64_CBC_SHA",
            "SSL3_RSA_DES_192_CBC3_SHA",
            "SSL3_RSA_RC4_40_MD5",
            "SSL3_RSA_RC4_128_MD5",
            "SSL3_RSA_RC4_128_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
            "TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
            "TLS1_RSA_WITH_AES_128_GCM_SHA256",
            "TLS1_RSA_WITH_AES_256_GCM_SHA384",
            "GM1_ECC_SM4_SM3",
            "GM1_ECDHE_SM4_SM3",
            "GM1_ECDHE_SM4_GCM_SM3",
            "GM1_ECC_SM4_GCM_SM3",
            "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_AES_128_GCM_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_SM4_GCM_SM3",
            "TLS_SM4_CCM_SM3"
        ]
    }
]
服务端SSL卸载模板获取
Action：slb.sslserver.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	服务端SSL卸载模版名称	是	必须存在
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.sslserver.get
请求body:
{
    "name": "api-ssl_server"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	服务端SSL卸载模版名称
cert	字符串	长度1-255	证书名称
key	字符串	长度1-255	私钥名称
password	字符串	长度1-46	密码
ecert	字符串	长度1-255	国密加密证书名称
ekey	字符串	长度1-255	国密加密私钥名称
epassword	字符串	长度1-46	国密加密证书密码
ca_cert	字符串	长度1-255	CA证书名称
ssl_version	整数	0,1,2,3，5，6	版本；0：SSL v3.0 ；1：TLS v1.0 ；2：TLS v1.1，3：TLS v1.2，5：TLS v1.3 ，6: GMTLSv1.1
sni_switch	整数	0，1	0：关闭SNI功能；1：开启SNI功能
sni_name	字符串	长度1-191	SNI名称
cipher_suite	数组	不涉及	加密算法列表，支持以下算法：
            "GM1_ECDHE_SM4_GCM_SM3",
            "GM1_ECDHE_SM4_SM3",
            "GM1_ECC_SM4_GCM_SM3",
            "GM1_ECC_SM4_SM3",
            "TLS1_RSA_EXPORT1024_RC4_56_MD5",
            "TLS1_RSA_EXPORT1024_RC4_56_SHA",
            "SSL3_RSA_RC4_40_MD5",
            "SSL3_RSA_RC4_128_MD5",
            "SSL3_RSA_RC4_128_SHA",
            "SSL3_RSA_DES_40_CBC_SHA",
            "SSL3_RSA_DES_64_CBC_SHA",
            "SSL3_RSA_DES_192_CBC3_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",             "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",           "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",          "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",          "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",        
  "TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS1_RSA_AES_256_SHA",
            "TLS1_RSA_AES_128_SHA",
            "TLS1_RSA_AES_256_SHA256",
            "TLS1_RSA_AES_128_SHA256",
            "TLS1_RSA_WITH_AES_256_GCM_SHA384",
            "TLS1_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_SM4_CCM_SM3",
            "TLS_SM4_GCM_SM3",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "TLS_AES_128_GCM_SHA256"
sign_cipher
	数组	不涉及	签名算法列表，支持以下签名算法：           
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"



响应举例：

{
    "name": "api-ssl_server",
    "description": "",
    "cert": "client.crt",
    "key": "client.key",
    "ca_cert": "",
    "password": "******",
    "ecert": "",
    "ekey": "",
    "epassword": "******",
    "ssl_version": 3,
    "sni_switch": 1,
    "sni_name": "www.123.com",
    "sign_cipher": [
        "sha512RSA",
        "sha384RSA",
        "sha256RSA",
        "sha224RSA",
        "sha1RSA",
        "sha512RSAE",
        "sm2sig_sm3",
        "ed25519",
        "ed448"
    ],
    "cipher_suite": [
        "TLS1_RSA_AES_128_SHA",
        "TLS1_RSA_AES_256_SHA",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
        "GM1_ECDHE_SM4_SM3",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
        "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"
    ]
}

服务端SSL卸载模板增加
Action：slb.sslserver.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	唯一
cert	字符串	长度1-255	证书名称	否	必须存在
key	字符串	长度1-255	私钥名称	否	必须存在
password	字符串	长度1-46	密码	否	缺省值:"" 空字符串
ecert	字符串	长度1-255	国密加密证书	否	必须存在，"" 空字符串
ekey	字符串	长度1-255	国密加密私钥	否	必须存在，"" 空字符串
epassword	字符串	长度1-46	国密加密证书密码	否	缺省值:"" 空字符串
ca_cert	字符串	长度1-255	CA证书名称	否	必须存在；缺省值:"" 空字符串
sni_switch	整数	0，1	SNI功能开关	否	0：关闭SNI功能；1：开启SNI功能，缺省为0
sni_name	字符串	长度1-191	SNI名称	否	缺省值:"" 空字符串
ssl_version	整数	0,1,2,3，5，6	SSL协议版本	否	版本；0：SSL v3.0 ；1：TLS v1.0 ；2：TLS v1.1，3：TLS v1.2 ，5：TLS v1.3 ，6: GMTLSv1.1
cipher_suite	数组	不涉及	加密算法列表	否	支持以下算法：
            "GM1_ECDHE_SM4_GCM_SM3",
            "GM1_ECDHE_SM4_SM3",
            "GM1_ECC_SM4_GCM_SM3",
            "GM1_ECC_SM4_SM3",
            "TLS1_RSA_EXPORT1024_RC4_56_MD5",
            "TLS1_RSA_EXPORT1024_RC4_56_SHA",
            "SSL3_RSA_RC4_40_MD5",
            "SSL3_RSA_RC4_128_MD5",
            "SSL3_RSA_RC4_128_SHA",
            "SSL3_RSA_DES_40_CBC_SHA",
            "SSL3_RSA_DES_64_CBC_SHA",
            "SSL3_RSA_DES_192_CBC3_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",            "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",            "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS1_RSA_AES_256_SHA",
            "TLS1_RSA_AES_128_SHA",
            "TLS1_RSA_AES_256_SHA256",
            "TLS1_RSA_AES_128_SHA256",
            "TLS1_RSA_WITH_AES_256_GCM_SHA384",
            "TLS1_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_SM4_CCM_SM3",
            "TLS_SM4_GCM_SM3",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "TLS_AES_128_GCM_SHA256"
缺省值:支持的全部算法
sign_cipher
	数组	不涉及	签名算法列表	否	签名算法列表，支持以下签名算法：           
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=3dc96e30a551175be4f021fb6325d7&action=slb.sslserver.add
请求body:
{
    "name": "api-ssl_server",
    "description": "",
    "cert": "client.crt",
    "key": "client.key",
    "ca_cert": "",
    "password": "******",
    "ecert": "",
    "ekey": "",
    "epassword": "******",
    "ssl_version": 3,
    "sni_switch": 1,
    "sni_name": "www.123.com",
    "sign_cipher": [
        "sha512RSA",
        "sha384RSA",
        "sha256RSA",
        "sha224RSA",
        "sha1RSA",
        "sha512RSAE",
        "sm2sig_sm3",
        "ed25519",
        "ed448"
    ],
    "cipher_suite": [
        "TLS1_RSA_AES_128_SHA",
        "TLS1_RSA_AES_256_SHA",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
        "GM1_ECDHE_SM4_SM3",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
        "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"
    ]
}

服务端SSL卸载模板编辑
Action：slb.sslserver.edit
请求参数：


名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	模版名称	是	唯一
cert	字符串	长度1-255	证书名称	否	必须存在
key	字符串	长度1-255	私钥名称	否	必须存在
password	字符串	长度1-46	密码	否	缺省值:"" 空字符串
ca_cert	字符串	长度1-255	CA证书名称	否	必须存在；缺省值:"" 空字符串
ecert	字符串	长度1-255	国密加密证书	否	必须存在，"" 空字符串
ekey	字符串	长度1-255	国密加密私钥	否	必须存在，"" 空字符串
epassword	字符串	长度1-46	国密加密证书密码	否	缺省值:"" 空字符串
sni_switch	整数	0，1	SNI功能开关	否	0：关闭SNI功能；1：开启SNI功能，缺省为0
sni_name	字符串	长度1-191	SNI名称	否	缺省值:"" 空字符串
ssl_version	整数	0,1,2,3，5，6	SSL协议版本	否	版本；0：SSL v3.0 ；1：TLS v1.0 ；2：TLS v1.1，3：TLS v1.2，5：TLS v1.3 ，6: GMTLSv1.1
cipher_suite	数组	不涉及	加密算法列表	否	支持以下算法：
            "GM1_ECDHE_SM4_GCM_SM3",
            "GM1_ECDHE_SM4_SM3",
            "GM1_ECC_SM4_GCM_SM3",
            "GM1_ECC_SM4_SM3",
            "TLS1_RSA_EXPORT1024_RC4_56_MD5",
            "TLS1_RSA_EXPORT1024_RC4_56_SHA",
            "SSL3_RSA_RC4_40_MD5",
            "SSL3_RSA_RC4_128_MD5",
            "SSL3_RSA_RC4_128_SHA",
            "SSL3_RSA_DES_40_CBC_SHA",
            "SSL3_RSA_DES_64_CBC_SHA",
            "SSL3_RSA_DES_192_CBC3_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
            "TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",            "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",            "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS1_RSA_AES_256_SHA",
            "TLS1_RSA_AES_128_SHA",
            "TLS1_RSA_AES_256_SHA256",
            "TLS1_RSA_AES_128_SHA256",
            "TLS1_RSA_WITH_AES_256_GCM_SHA384",
            "TLS1_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_SM4_CCM_SM3",
            "TLS_SM4_GCM_SM3",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "TLS_AES_128_GCM_SHA256"
缺省值:支持的全部算法
sign_cipher
	数组	不涉及	签名算法列表	否	签名算法列表，支持以下签名算法：           
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"


请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=3dc96e30a551175be4f021fb6325d7&action=slb.sslserver.edit
请求body:
{
    "name": "api-ssl_server",
    "description": "",
    "cert": "client.crt",
    "key": "client.key",
    "ca_cert": "",
    "password": "******",
    "ecert": "",
    "ekey": "",
    "epassword": "******",
    "ssl_version": 3,
    "sni_switch": 1,
    "sni_name": "www.123.com",
    "sign_cipher": [
        "sha512RSA",
        "sha384RSA",
        "sha256RSA",
        "sha224RSA",
        "sha1RSA",
        "sha512RSAE",
        "sm2sig_sm3",
        "ed25519",
        "ed448"
    ],
    "cipher_suite": [
        "TLS1_RSA_AES_128_SHA",
        "TLS1_RSA_AES_256_SHA",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
        "GM1_ECDHE_SM4_SM3",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
        "TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"
    ]
}
服务端SSL卸载模板删除
Action：slb.sslserver.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	服务端SSL卸载模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=3dc96e30a551175be4f021fb6325d7&action=slb.sslserver.del
请求body:
{
    "name": "sever"
}
客户端SSL卸载
客户端SSL卸载模板列表
Action：slb.sslclient.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.sslclient.list
响应参数：


名称	类型	范围	含义
name	字符串	长度1-191	客户端SSL卸载模版名称
cert	字符串	长度1-255	第一证书名称（可选RSA,ECC,国密签名证书）
chain_cert	字符串	长度1-255	第一证书链名称（可选RSA,ECC,国密签名证书）
key	字符串	长度1-255	第一证书私钥名称
password	字符串	长度1-46	第一证书密码
dcert	字符	长度1-255	第二证书名称
dchain_cert	字符串	长度1-255	第二证书链名称
dkey	字符串	长度1-255	第二证书私钥名称
dpassword	字符串	长度1-46	第二证书密码
ecert	字符串	长度1-255	国密加密证书名称
ekey	字符串	长度1-255	国密加密证书私钥
epassword	字符串	长度1-46	国密加密证书密码
resume_mode	整数	0/1	会话缓存模式，0代表session ticket ，1代表session id
cache_num	整数	0-131072	会话缓存大小
cache_timeout	整数	0-10000000	会话缓存超时，单位秒
disable_renegotiate	整数	0/1	禁用重协商，0代表关闭禁止重协商功能，1代表开启禁止重协商功能
disable_ssl30	整数	0/1/	SSL3.0协议版本开关：0开启，1关闭
disable_tls10	整数	0/1/	TLS1.0协议版本开关：0开启，1关闭
disable_tls11	整数	0/1/	TLS1.1协议版本开关：0开启，1关闭
disable_tls12	整数	0/1/	TLS1.2协议版本开关：0开启，1关闭
disable_tls13	整数	0/1/	TLS1.3协议版本开关：0开启，1关闭
disable_gm11	整数	0/1/	GMTLSv1.1协议版本开关：0开启，1关闭
client_cert_req	整数	0/1/2	检查客户端证书：0 必需；1可选；2忽略
revoke	字符串	长度1-255	吊销证书列表名称
ca_cert	字符串	长度1-255	客户端CA证书名称
cipher_suite	数组	不涉及	加密算法列表，支持以下算法：
"TLS_CHACHA20_POLY1305_SHA256",
"TLS1_RSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
"GM1_ECDHE_SM4_GCM_SM3",
"GM1_ECDHE_SM4_SM3",
"GM1_ECC_SM4_GCM_SM3",
"GM1_ECC_SM4_SM3",
"TLS1_RSA_EXPORT1024_RC4_56_MD5",
"TLS1_RSA_EXPORT1024_RC4_56_SHA",
"SSL3_RSA_RC4_40_MD5",
"SSL3_RSA_RC4_128_MD5",
"SSL3_RSA_RC4_128_SHA",
"SSL3_RSA_DES_40_CBC_SHA",
"SSL3_RSA_DES_64_CBC_SHA",
"SSL3_RSA_DES_192_CBC3_SHA",
"TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
"TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
"TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
"TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
"TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
"TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
"TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
"TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
"TLS1_RSA_AES_256_SHA",
"TLS1_RSA_AES_128_SHA",
"TLS1_RSA_AES_256_SHA256",
"TLS1_RSA_AES_128_SHA256",
"TLS1_RSA_WITH_AES_128_GCM_SHA256",
"TLS_SM4_CCM_SM3",
"TLS_SM4_GCM_SM3",
"TLS_AES_256_GCM_SHA384",
"TLS_AES_128_GCM_SHA256"
缺省为全部发送
sign_cipher	数组	不涉及	签名算法列表，支持以下签名算法：           
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
elliptic_curve	数组	不涉及	曲线列表，支持以下曲线：   
            "secp256r1",
            "secp384r1",
            "secp521r1",
            "X25519",
            "X448",
            "cureveSM2"
crs_cipher	数组	不涉及	签名请求算法列表，支持以下签名请求算法：  
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
sni_list
     
	数组	不涉及	SNI组成的数组，详细参数如下：
domain：SNI主机名，字符串，长度1-191
cert：SNI证书名称，字符串，长度1-255
cert_chain：SNi证书证书链，字符串，长度1-255
key：SNI私钥名称，字符串，长度1-255
password：SNI私钥密码，字符串，长度1-46
secondcert：SNI第二证书（国密签名证书）名称，字符串，长度1-255
secondcert_chain：SNI第二证书证书链，字符串，长度1-255
Secondkey：SNI第二证书（国密签名证书）私钥名称，字符串，长度1-255
Secondpassword：SNI第二证书（国密签名证书）私钥密码，字符串，长度1-46
gmenccert：SNI国密加密模式证书名称，字符串，长度1-255
gmenckey：SNI国密加密模式私钥名称，字符串，长度1-255
gmencpassword：SNI国密加密模式私钥密码，字符串，长度1-46

响应举例：
[
    {
    "name": "ADC-ssl-client",
    "description": "",
    "cert": "client.crt",
    "chain_cert": "",
    "key": "client.key",
    "password": "******",
    "dcert": "",
    "dchain_cert": "",
    "dkey": "",
    "dpassword": "******",
    "ecert": "",
    "ekey": "",
    "epassword": "******",
    "resume_mode": 1,
    "cache_num": 0,
    "close_notify": 0,
    "cache_timeout": 3600,
    "disable_renegotiate": 1,
    "disable_ssl30": 0,
    "disable_tls10": 0,
    "disable_tls11": 0,
    "disable_tls12": 0,
    "disable_tls13": 1,
    "disable_gm11": 1,
    "client_cert_req": 2,
    "revoke": "",
    "ca_cert": [],
    "sign_cipher": [
        "sm2sig_sm3",
        "sha256RSA",
        "sha256RSAE",
        "secp256r1_sha256ECDSA"
    ],
    "elliptic_curve": [
        "secp256r1"
    ],
    "crs_cipher": [
        "sm2sig_sm3",
        "sha256RSA",
        "sha256RSAE",
        "secp256r1_sha256ECDSA"
    ],
    "cipher_suite": [
        "GM1_ECC_SM4_SM3",
        "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
        "TLS1_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_CHACHA20_POLY1305_SHA256"
    ],
    "sni_list": [
        {
            "domain": "www.adc.com",
            "cert": "client.crt",
            "cert_chain": "",
            "key": "client.key",
            "password": "",
            "secondcert": "",
            "secondcert_chain": "",
            "secondkey": "",
            "secondpassword": "",
            "gmenccert": "",
            "gmenckey": "",
            "gmencpassword": ""
        }
    ]
}

]

获取common以及分区自己的客户端SSL卸载模板列表
Action：slb.sslclient.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.sslclient.list.withcommon
响应参数：

名称	类型	范围	含义
name	字符串	长度1-191	客户端SSL卸载模版名称
cert	字符串	长度1-255	第一证书名称（可选RSA,ECC,国密签名证书）
chain_cert	字符串	长度1-255	第一证书链名称（可选RSA,ECC,国密签名证书）
key	字符串	长度1-255	第一证书私钥名称
password	字符串	长度1-46	第一证书密码
dcert	字符	长度1-255	第二证书名称
dchain_cert	字符串	长度1-255	第二证书链名称
dkey	字符串	长度1-255	第二证书私钥名称
dpassword	字符串	长度1-46	第二证书密码
ecert	字符串	长度1-255	国密加密证书名称
ekey	字符串	长度1-255	国密加密证书私钥
epassword	字符串	长度1-46	国密加密证书密码
resume_mode	整数	0/1	会话缓存模式，0代表session ticket ，1代表session id
cache_num	整数	0-131072	会话缓存大小
cache_timeout	整数	0-10000000	会话缓存超时，单位秒
disable_renegotiate	整数	0/1	禁用重协商，0代表关闭禁止重协商功能，1代表开启禁止重协商功能
disable_ssl30	整数	0/1/	SSL3.0协议版本开关：0开启，1关闭
disable_tls10	整数	0/1/	TLS1.0协议版本开关：0开启，1关闭
disable_tls11	整数	0/1/	TLS1.1协议版本开关：0开启，1关闭
disable_tls12	整数	0/1/	TLS1.2协议版本开关：0开启，1关闭
disable_tls13	整数	0/1/	TLS1.3协议版本开关：0开启，1关闭
disable_gm11	整数	0/1/	GMTLSv1.1协议版本开关：0开启，1关闭
client_cert_req	整数	0/1/2	检查客户端证书：0 必需；1可选；2忽略
revoke	字符串	长度1-255	吊销证书列表名称
ca_cert	字符串	长度1-255	客户端CA证书名称
cipher_suite	数组	不涉及	加密算法列表，支持以下算法：
"TLS_CHACHA20_POLY1305_SHA256",
"TLS1_RSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
"GM1_ECDHE_SM4_GCM_SM3",
"GM1_ECDHE_SM4_SM3",
"GM1_ECC_SM4_GCM_SM3",
"GM1_ECC_SM4_SM3",
"TLS1_RSA_EXPORT1024_RC4_56_MD5",
"TLS1_RSA_EXPORT1024_RC4_56_SHA",
"SSL3_RSA_RC4_40_MD5",
"SSL3_RSA_RC4_128_MD5",
"SSL3_RSA_RC4_128_SHA",
"SSL3_RSA_DES_40_CBC_SHA",
"SSL3_RSA_DES_64_CBC_SHA",
"SSL3_RSA_DES_192_CBC3_SHA",
"TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
"TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
"TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
"TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
"TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
"TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
"TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
"TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
"TLS1_RSA_AES_256_SHA",
"TLS1_RSA_AES_128_SHA",
"TLS1_RSA_AES_256_SHA256",
"TLS1_RSA_AES_128_SHA256",
"TLS1_RSA_WITH_AES_128_GCM_SHA256",
"TLS_SM4_CCM_SM3",
"TLS_SM4_GCM_SM3",
"TLS_AES_256_GCM_SHA384",
"TLS_AES_128_GCM_SHA256"
缺省为全部发送
sign_cipher	数组	不涉及	签名算法列表，支持以下签名算法：           
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
elliptic_curve	数组	不涉及	曲线列表，支持以下曲线：   
            "secp256r1",
            "secp384r1",
            "secp521r1",
            "X25519",
            "X448",
            "cureveSM2"
crs_cipher	数组	不涉及	签名请求算法列表，支持以下签名请求算法：  
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
sni_list
     
	数组	不涉及	SNI组成的数组，详细参数如下：
domain：SNI主机名，字符串，长度1-191
cert：SNI证书名称，字符串，长度1-255
cert_chain：SNi证书证书链，字符串，长度1-255
key：SNI私钥名称，字符串，长度1-255
password：SNI私钥密码，字符串，长度1-46
secondcert：SNI第二证书（国密签名证书）名称，字符串，长度1-255
secondcert_chain：SNI第二证书证书链，字符串，长度1-255
Secondkey：SNI第二证书（国密签名证书）私钥名称，字符串，长度1-255
Secondpassword：SNI第二证书（国密签名证书）私钥密码，字符串，长度1-46
gmenccert：SNI国密加密模式证书名称，字符串，长度1-255
gmenckey：SNI国密加密模式私钥名称，字符串，长度1-255
gmencpassword：SNI国密加密模式私钥密码，字符串，长度1-46

响应举例：
[
        {
        "name": "common/ADC-ssl-client",
        "description": "",
        "cert": "common/client.crt",
        "chain_cert": "",
        "key": "common/client.key",
        "password": "******",
        "dcert": "",
        "dchain_cert": "",
        "dkey": "",
        "dpassword": "******",
        "ecert": "",
        "ekey": "",
        "epassword": "******",
        "resume_mode": 1,
        "cache_num": 0,
        "close_notify": 0,
        "cache_timeout": 3600,
        "disable_renegotiate": 1,
        "disable_ssl30": 0,
        "disable_tls10": 0,
        "disable_tls11": 0,
        "disable_tls12": 0,
        "disable_tls13": 1,
        "disable_gm11": 1,
        "client_cert_req": 2,
        "revoke": "",
        "ca_cert": [],
        "sign_cipher": [
            "sm2sig_sm3",
            "sha256RSA",
            "sha256RSAE",
            "secp256r1_sha256ECDSA"
        ],
        "elliptic_curve": [
            "secp256r1"
        ],
        "crs_cipher": [
            "sm2sig_sm3",
            "sha256RSA",
            "sha256RSAE",
            "secp256r1_sha256ECDSA"
        ],
        "cipher_suite": [
            "GM1_ECC_SM4_SM3",
            "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS1_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_CHACHA20_POLY1305_SHA256"
        ],
        "sni_list": [
            {
                "domain": "www.adc.com",
                "cert": "common/client.crt",
                "cert_chain": "",
                "key": "common/client.key",
                "password": "",
                "secondcert": "",
                "secondcert_chain": "",
                "secondkey": "",
                "secondpassword": "",
                "gmenccert": "",
                "gmenckey": "",
                "gmencpassword": ""
            }
        ]
    }

]
客户端SSL卸载模板获取
Action：slb.sslclient.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	客户端SSL卸载模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=4f1fdc5dca55b80fd8fbd743add066&action=slb.sslclient.get
请求body：
{
    "name": "1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	客户端SSL卸载模版名称
cert	字符串	长度1-255	第一证书名称（可选RSA,ECC,国密签名证书）
chain_cert	字符串	长度1-255	第一证书链名称（可选RSA,ECC,国密签名证书）
key	字符串	长度1-255	第一证书私钥名称
password	字符串	长度1-46	第一证书密码
dcert	字符	长度1-255	第二证书名称
dchain_cert	字符串	长度1-255	第二证书链名称
dkey	字符串	长度1-255	第二证书私钥名称
dpassword	字符串	长度1-46	第二证书密码
ecert	字符串	长度1-255	国密加密证书名称
ekey	字符串	长度1-255	国密加密证书私钥
epassword	字符串	长度1-46	国密加密证书密码
resume_mode	整数	0/1	会话缓存模式，0代表session ticket ，1代表session id
cache_num	整数	0-131072	会话缓存大小
cache_timeout	整数	0-10000000	会话缓存超时，单位秒
disable_renegotiate	整数	0/1	禁用重协商，0代表关闭禁止重协商功能，1代表开启禁止重协商功能
disable_ssl30	整数	0/1/	SSL3.0协议版本开关：0开启，1关闭
disable_tls10	整数	0/1/	TLS1.0协议版本开关：0开启，1关闭
disable_tls11	整数	0/1/	TLS1.1协议版本开关：0开启，1关闭
disable_tls12	整数	0/1/	TLS1.2协议版本开关：0开启，1关闭
disable_tls13	整数	0/1/	TLS1.3协议版本开关：0开启，1关闭
disable_gm11	整数	0/1/	GMTLSv1.1协议版本开关：0开启，1关闭
client_cert_req	整数	0/1/2	检查客户端证书：0 必需；1可选；2忽略
revoke	字符串	长度1-255	吊销证书列表名称
ca_cert	字符串	长度1-255	客户端CA证书名称
cipher_suite	数组		加密算法列表，支持以下算法：
     "TLS_CHACHA20_POLY1305_SHA256",
"TLS1_RSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
"GM1_ECDHE_SM4_GCM_SM3",
"GM1_ECDHE_SM4_SM3",
"GM1_ECC_SM4_GCM_SM3",
"GM1_ECC_SM4_SM3",
"TLS1_RSA_EXPORT1024_RC4_56_MD5",
"TLS1_RSA_EXPORT1024_RC4_56_SHA",
"SSL3_RSA_RC4_40_MD5",
"SSL3_RSA_RC4_128_MD5",
"SSL3_RSA_RC4_128_SHA",
"SSL3_RSA_DES_40_CBC_SHA",
"SSL3_RSA_DES_64_CBC_SHA",
"SSL3_RSA_DES_192_CBC3_SHA",
"TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
"TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
"TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
"TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
"TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
"TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
"TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
"TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
"TLS1_RSA_AES_256_SHA",
"TLS1_RSA_AES_128_SHA",
"TLS1_RSA_AES_256_SHA256",
"TLS1_RSA_AES_128_SHA256",
"TLS1_RSA_WITH_AES_128_GCM_SHA256",
"TLS_SM4_CCM_SM3",
"TLS_SM4_GCM_SM3",
"TLS_AES_256_GCM_SHA384",
"TLS_AES_128_GCM_SHA256"
缺省为全部发送     
sign_cipher	数组		签名算法列表，支持以下签名算法：           
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
elliptic_curve	数组		曲线列表，支持以下曲线：   
            "secp256r1",
            "secp384r1",
            "secp521r1",
            "X25519",
            "X448",
            "cureveSM2"
crs_cipher	数组		签名请求算法列表，支持以下签名请求算法：  
            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
sni_list
     
	数组	不涉及	SNI组成的数组，详细参数如下：
domain：SNI主机名，字符串，长度1-191
cert：SNI证书名称，字符串，长度1-255
cert_chain：SNi证书证书链，字符串，长度1-255
key：SNI私钥名称，字符串，长度1-255
password：SNI私钥密码，字符串，长度1-46
secondcert：SNI第二证书（国密签名证书）名称，字符串，长度1-255
secondcert_chain：SNI第二证书证书链，字符串，长度1-255
Secondkey：SNI第二证书（国密签名证书）私钥名称，字符串，长度1-255
Secondpassword：SNI第二证书（国密签名证书）私钥密码，字符串，长度1-46
gmenccert：SNI国密加密模式证书名称，字符串，长度1-255
gmenckey：SNI国密加密模式私钥名称，字符串，长度1-255
gmencpassword：SNI国密加密模式私钥密码，字符串，长度1-46

响应举例：

{
    "name": "ADC-ssl-client",
    "description": "",
    "cert": "client.crt",
    "chain_cert": "",
    "key": "client.key",
    "password": "******",
    "dcert": "",
    "dchain_cert": "",
    "dkey": "",
    "dpassword": "******",
    "ecert": "",
    "ekey": "",
    "epassword": "******",
    "resume_mode": 1,
    "cache_num": 0,
    "close_notify": 0,
    "cache_timeout": 3600,
    "disable_renegotiate": 1,
    "disable_ssl30": 0,
    "disable_tls10": 0,
    "disable_tls11": 0,
    "disable_tls12": 0,
    "disable_tls13": 1,
    "disable_gm11": 1,
    "client_cert_req": 2,
    "revoke": "",
    "ca_cert": [],
    "sign_cipher": [
        "sm2sig_sm3",
        "sha256RSA",
        "sha256RSAE",
        "secp256r1_sha256ECDSA"
    ],
    "elliptic_curve": [
        "secp256r1"
    ],
    "crs_cipher": [
        "sm2sig_sm3",
        "sha256RSA",
        "sha256RSAE",
        "secp256r1_sha256ECDSA"
    ],
    "cipher_suite": [
        "GM1_ECC_SM4_SM3",
        "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
        "TLS1_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_CHACHA20_POLY1305_SHA256"
    ],
    "sni_list": [
        {
            "domain": "www.adc.com",
            "cert": "client.crt",
            "cert_chain": "",
            "key": "client.key",
            "password": "",
            "secondcert": "",
            "secondcert_chain": "",
            "secondkey": "",
            "secondpassword": "",
            "gmenccert": "",
            "gmenckey": "",
            "gmencpassword": ""
        }
    ]
}
客户端SSL卸载模板增加
Action：slb.sslclient.add
请求参数：

名称	类型	范围	含义
name	字符串	长度1-191	客户端SSL卸载模版名称
cert	字符串	长度1-255	第一证书名称（可选RSA,ECC,国密签名证书）
chain_cert	字符串	长度1-255	第一证书链名称（可选RSA,ECC,国密签名证书）
key	字符串	长度1-255	第一证书私钥名称
password	字符串	长度1-46	第一证书密码
dcert	字符	长度1-255	第二证书名称
dchain_cert	字符串	长度1-255	第二证书链名称
dkey	字符串	长度1-255	第二证书私钥名称
dpassword	字符串	长度1-46	第二证书密码
ecert	字符串	长度1-255	国密加密证书名称
ekey	字符串	长度1-255	国密加密证书私钥
epassword	字符串	长度1-46	国密加密证书密码
resume_mode	整数	0/1	会话缓存模式，0代表session ticket ，1代表session id
cache_num	整数	0-131072	会话缓存大小
cache_timeout	整数	0-10000000	会话缓存超时，单位秒
disable_renegotiate	整数	0/1	禁用重协商，0代表关闭禁止重协商功能，1代表开启禁止重协商功能
disable_ssl30	整数	0/1/	SSL3.0协议版本开关：0开启，1关闭
disable_tls10	整数	0/1/	TLS1.0协议版本开关：0开启，1关闭
disable_tls11	整数	0/1/	TLS1.1协议版本开关：0开启，1关闭
disable_tls12	整数	0/1/	TLS1.2协议版本开关：0开启，1关闭
disable_tls13	整数	0/1/	TLS1.3协议版本开关：0开启，1关闭
disable_gm11	整数	0/1/	GMTLSv1.1协议版本开关：0开启，1关闭
client_cert_req	整数	0/1/2	检查客户端证书：0 必需；1可选；2忽略
revoke	字符串	长度1-255	吊销证书列表名称
ca_cert	字符串	长度1-255	客户端CA证书名称
cipher_suite	数组	不涉及	加密算法列表，支持以下算法：
"TLS_CHACHA20_POLY1305_SHA256",
"TLS1_RSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
"GM1_ECDHE_SM4_GCM_SM3",
"GM1_ECDHE_SM4_SM3",
"GM1_ECC_SM4_GCM_SM3",
"GM1_ECC_SM4_SM3",
"TLS1_RSA_EXPORT1024_RC4_56_MD5",
"TLS1_RSA_EXPORT1024_RC4_56_SHA",
"SSL3_RSA_RC4_40_MD5",
"SSL3_RSA_RC4_128_MD5",
"SSL3_RSA_RC4_128_SHA",
"SSL3_RSA_DES_40_CBC_SHA",
"SSL3_RSA_DES_64_CBC_SHA",
"SSL3_RSA_DES_192_CBC3_SHA",
"TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
"TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
"TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
"TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
"TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
"TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
"TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
"TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
"TLS1_RSA_AES_256_SHA",
"TLS1_RSA_AES_128_SHA",
"TLS1_RSA_AES_256_SHA256",
"TLS1_RSA_AES_128_SHA256",
"TLS1_RSA_WITH_AES_128_GCM_SHA256",
"TLS_SM4_CCM_SM3",
"TLS_SM4_GCM_SM3",
"TLS_AES_256_GCM_SHA384",
"TLS_AES_128_GCM_SHA256"
缺省为全部发送     
sign_cipher	数组	不涉及	            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
elliptic_curve	数组	不涉及	            "secp256r1",
            "secp384r1",
            "secp521r1",
            "X25519",
            "X448",
            "cureveSM2"
crs_cipher	数组	不涉及	            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
sni_list
     
	数组	不涉及	SNI组成的数组，详细参数如下：
domain：SNI主机名，字符串，长度1-191
cert：SNI证书名称，字符串，长度1-255
cert_chain：SNi证书证书链，字符串，长度1-255
key：SNI私钥名称，字符串，长度1-255
password：SNI私钥密码，字符串，长度1-46
secondcert：SNI第二证书（国密签名证书）名称，字符串，长度1-255
secondcert_chain：SNI第二证书证书链，字符串，长度1-255
Secondkey：SNI第二证书（国密签名证书）私钥名称，字符串，长度1-255
Secondpassword：SNI第二证书（国密签名证书）私钥密码，字符串，长度1-46
gmenccert：SNI国密加密模式证书名称，字符串，长度1-255
gmenckey：SNI国密加密模式私钥名称，字符串，长度1-255
gmencpassword：SNI国密加密模式私钥密码，字符串，长度1-46

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.sslclient.add
请求body:
       {
    "name": "ADC-ssl-client",
    "description": "",
    "cert": "client.crt",
    "chain_cert": "",
    "key": "client.key",
    "password": "******",
    "dcert": "",
    "dchain_cert": "",
    "dkey": "",
    "dpassword": "******",
    "ecert": "",
    "ekey": "",
    "epassword": "******",
    "resume_mode": 1,
    "cache_num": 0,
    "close_notify": 0,
    "cache_timeout": 3600,
    "disable_renegotiate": 1,
    "disable_ssl30": 0,
    "disable_tls10": 0,
    "disable_tls11": 0,
    "disable_tls12": 0,
    "disable_tls13": 1,
    "disable_gm11": 1,
    "client_cert_req": 2,
    "revoke": "",
    "ca_cert": [],
    "sign_cipher": [
        "sm2sig_sm3",
        "sha256RSA",
        "sha256RSAE",
        "secp256r1_sha256ECDSA"
    ],
    "elliptic_curve": [
        "secp256r1"
    ],
    "crs_cipher": [
        "sm2sig_sm3",
        "sha256RSA",
        "sha256RSAE",
        "secp256r1_sha256ECDSA"
    ],
    "cipher_suite": [
        "GM1_ECC_SM4_SM3",
        "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
        "TLS1_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_CHACHA20_POLY1305_SHA256"
    ],
    "sni_list": [
        {
            "domain": "www.adc.com",
            "cert": "client.crt",
            "cert_chain": "",
            "key": "client.key",
            "password": "",
            "secondcert": "",
            "secondcert_chain": "",
            "secondkey": "",
            "secondpassword": "",
            "gmenccert": "",
            "gmenckey": "",
            "gmencpassword": ""
        }
    ]
}

客户端SSL卸载模板编辑
Action：slb.sslclient.edit
请求参数：
名称	类型	范围	含义
name	字符串	长度1-191	客户端SSL卸载模版名称
cert	字符串	长度1-255	第一证书名称（可选RSA,ECC,国密签名证书）
chain_cert	字符串	长度1-255	第一证书链名称（可选RSA,ECC,国密签名证书）
key	字符串	长度1-255	第一证书私钥名称
password	字符串	长度1-46	第一证书密码
dcert	字符	长度1-255	第二证书名称
dchain_cert	字符串	长度1-255	第二证书链名称
dkey	字符串	长度1-255	第二证书私钥名称
dpassword	字符串	长度1-46	第二证书密码
ecert	字符串	长度1-255	国密加密证书名称
ekey	字符串	长度1-255	国密加密证书私钥
epassword	字符串	长度1-46	国密加密证书密码
resume_mode	整数	0/1	会话缓存模式，0代表session ticket ，1代表session id
cache_num	整数	0-131072	会话缓存大小
cache_timeout	整数	0-10000000	会话缓存超时，单位秒
disable_renegotiate	整数	0/1	禁用重协商，0代表关闭禁止重协商功能，1代表开启禁止重协商功能
disable_ssl30	整数	0/1/	SSL3.0协议版本开关：0开启，1关闭
disable_tls10	整数	0/1/	TLS1.0协议版本开关：0开启，1关闭
disable_tls11	整数	0/1/	TLS1.1协议版本开关：0开启，1关闭
disable_tls12	整数	0/1/	TLS1.2协议版本开关：0开启，1关闭
disable_tls13	整数	0/1/	TLS1.3协议版本开关：0开启，1关闭
disable_gm11	整数	0/1/	GMTLSv1.1协议版本开关：0开启，1关闭
client_cert_req	整数	0/1/2	检查客户端证书：0 必需；1可选；2忽略
revoke	字符串	长度1-255	吊销证书列表名称
ca_cert	字符串	长度1-255	客户端CA证书名称
cipher_suite	数组	不涉及	加密算法列表，支持以下算法：
  "TLS_CHACHA20_POLY1305_SHA256",
"TLS1_RSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_RSA_WITH_AES_256_CBC_SHA",
"GM1_ECDHE_SM4_GCM_SM3",
"GM1_ECDHE_SM4_SM3",
"GM1_ECC_SM4_GCM_SM3",
"GM1_ECC_SM4_SM3",
"TLS1_RSA_EXPORT1024_RC4_56_MD5",
"TLS1_RSA_EXPORT1024_RC4_56_SHA",
"SSL3_RSA_RC4_40_MD5",
"SSL3_RSA_RC4_128_MD5",
"SSL3_RSA_RC4_128_SHA",
"SSL3_RSA_DES_40_CBC_SHA",
"SSL3_RSA_DES_64_CBC_SHA",
"SSL3_RSA_DES_192_CBC3_SHA",
"TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
"TLS1_ECDHE_RSA_WITH_AES_128_CBC_SHA",
"TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
"TLS1_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
"TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
"TLS1_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
"TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS1_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
"TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
"TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
"TLS1_RSA_AES_256_SHA",
"TLS1_RSA_AES_128_SHA",
"TLS1_RSA_AES_256_SHA256",
"TLS1_RSA_AES_128_SHA256",
"TLS1_RSA_WITH_AES_128_GCM_SHA256",
"TLS_SM4_CCM_SM3",
"TLS_SM4_GCM_SM3",
"TLS_AES_256_GCM_SHA384",
"TLS_AES_128_GCM_SHA256"
缺省为全部发送     
sign_cipher	数组	不涉及	            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
elliptic_curve	数组	不涉及	            "secp256r1",
            "secp384r1",
            "secp521r1",
            "X25519",
            "X448",
            "cureveSM2"
crs_cipher	数组	不涉及	            "sha512RSA",
            "sha384RSA",
            "sha256RSA",
            "sha224RSA",
            "sha1RSA",
            "secp521r1_sha512ECDSA",
            "secp384r1_sha384ECDSA",
            "secp256r1_sha256ECDSA",
            "sha224ECDSA",
            "sha1ECDSA",
            "sha256RSAPSS",
            "sha384RSAPSS",
            "sha512RSAPSS",
            "sha256RSAE",
            "sha384RSAE",
            "sha512RSAE",
            "sm2sig_sm3",
            "ed25519",
            "ed448"
sni_list
     
	数组	不涉及	SNI组成的数组，详细参数如下：
domain：SNI主机名，字符串，长度1-191
cert：SNI证书名称，字符串，长度1-255
cert_chain：SNi证书证书链，字符串，长度1-255
key：SNI私钥名称，字符串，长度1-255
password：SNI私钥密码，字符串，长度1-46
secondcert：SNI第二证书（国密签名证书）名称，字符串，长度1-255
secondcert_chain：SNI第二证书证书链，字符串，长度1-255
Secondkey：SNI第二证书（国密签名证书）私钥名称，字符串，长度1-255
Secondpassword：SNI第二证书（国密签名证书）私钥密码，字符串，长度1-46
gmenccert：SNI国密加密模式证书名称，字符串，长度1-255
gmenckey：SNI国密加密模式私钥名称，字符串，长度1-255
gmencpassword：SNI国密加密模式私钥密码，字符串，长度1-46

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.sslclient.edit
请求body:
{
    "name": "ADC-ssl-client",
    "description": "",
    "cert": "client.crt",
    "chain_cert": "",
    "key": "client.key",
    "password": "******",
    "dcert": "",
    "dchain_cert": "",
    "dkey": "",
    "dpassword": "******",
    "ecert": "",
    "ekey": "",
    "epassword": "******",
    "resume_mode": 1,
    "cache_num": 0,
    "close_notify": 0,
    "cache_timeout": 3600,
    "disable_renegotiate": 1,
    "disable_ssl30": 0,
    "disable_tls10": 0,
    "disable_tls11": 0,
    "disable_tls12": 0,
    "disable_tls13": 1,
    "disable_gm11": 1,
    "client_cert_req": 2,
    "revoke": "",
    "ca_cert": [],
    "sign_cipher": [
        "sm2sig_sm3",
        "sha256RSA",
        "sha256RSAE",
        "secp256r1_sha256ECDSA"
    ],
    "elliptic_curve": [
        "secp256r1"
    ],
    "crs_cipher": [
        "sm2sig_sm3",
        "sha256RSA",
        "sha256RSAE",
        "secp256r1_sha256ECDSA"
    ],
    "cipher_suite": [
        "GM1_ECC_SM4_SM3",
        "TLS1_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "TLS1_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
        "TLS1_RSA_WITH_AES_128_GCM_SHA256",
        "TLS_CHACHA20_POLY1305_SHA256"
    ],
    "sni_list": [
        {
            "domain": "www.adc.com",
            "cert": "client.crt",
            "cert_chain": "",
            "key": "client.key",
            "password": "",
            "secondcert": "",
            "secondcert_chain": "",
            "secondkey": "",
            "secondpassword": "",
            "gmenccert": "",
            "gmenckey": "",
            "gmencpassword": ""
        }
    ]
}

客务端SSL卸载模板删除
Action：slb.sslserver.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	服务端SSL卸载模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=3dc96e30a551175be4f021fb6325d7&action=slb.sslserver.del
请求body:
{
    "name": "server"
}

策略
黑白名单
黑白名单上传
Action:  slb.bwlist.upload
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	黑白名单名称	是	唯一

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.bwlist.upload&name=bw1

	此API需要使用form-data的方式上传黑白名单文件
参数name在URL中不在Body中



黑白名单删除
Action:  slb.bwlist.del
请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	黑白名单名称	是	必须存在

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.bwlist.del
{"name": "myname"}


黑白名单列表
Action:  slb.bwlist.list
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.bwlist.list
响应参数:
名称	类型	范围	含义
name	字符串	长度1-191	黑白名单名称
响应举例：
[
  {
    "name": "bw_list"
  }
]
	黑白名单用于策略模板中调用使用

规则表
获取规则表列表
Action：slb.ruletable.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	规则表名称
entrys	数组	不涉及	规则条目组成的数组:
entrys > ip：
含义：ip地址，
类型：字符串，
范围：不涉及
entrys > id：
含义：id号
类型：整数，
范围：1-30
entrys > age：
含义：生存时间，
类型：整数，
范围：0-1800
strings	数组	不涉及	规则条目组成的数组
strings > key: 
含义：搜索关键字，
类型：字符串，
范围：1-255
strings > value: 
含义：返回值，
类型：字符串，
范围：0-639
dnss	数组	不涉及	规则条目组成的数组
dnss > domain: 
含义：所需要匹配的域名,
类型：字符串，
范围：1-64
dnss > lid:
含义：规则ID，
类型：整数，
范围：1-30
dnss > match_type:
含义：匹配类型，
类型：整数，
范围：0-2
响应举例：
[
    {
        "name": "rt-1",
        "location": 1,
        "type": 7,
        "entrys": [
            {
                "ip": "1.2.3.4/32",
                "id": 1,
                "age": 0,
                "value": ""
            }
        ],
        "strings": [],
        "dnss": []
    },
    {
        "name": "rt-2",
        "location": 1,
        "type": 9,
        "entrys": [],
        "strings": [
            {
                "key": "key1",
                "value": "value1"
            }
        ],
        "dnss": []
    },
    {
        "name": "rt-3",
        "location": 1,
        "type": 6,
        "entrys": [],
        "strings": [],
        "dnss": [
            {
                "domain": "www.baidu.com",
                "lid": 1,
                "match_type": 0
            }
        ]
    }
]


分区获取common和自己分区的规则表列表
Action：slb.ruletable.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	规则表名称
entrys	数组	不涉及	规则条目组成的数组:
entrys > ip：
含义：ip地址，
类型：字符串，
范围：不涉及
entrys > id：
含义：id号
类型：整数，
范围：1-30
entrys > age：
含义：生存时间，
类型：整数，
范围：0-1800
strings	数组	不涉及	规则条目组成的数组
strings > key: 
含义：搜索关键字，
类型：字符串，
范围：1-255
strings > value: 
含义：返回值，
类型：字符串，
范围：0-639
dnss	数组	不涉及	规则条目组成的数组
dnss > domain: 
含义：所需要匹配的域名,
类型：字符串，
范围：1-64
dnss > lid:
含义：规则ID，
类型：整数，
范围：1-30
dnss > match_type:
含义：匹配类型，
类型：整数，
范围：0-2
响应举例：
[
    {
        "name": "rt-1",
        "location": 1,
        "type": 7,
        "entrys": [
            {
                "ip": "1.2.3.4/32",
                "id": 1,
                "age": 0,
                "value": ""
            }
        ],
        "strings": [],
        "dnss": []
    },
    {
        "name": "rt-2",
        "location": 1,
        "type": 9,
        "entrys": [],
        "strings": [
            {
                "key": "key1",
                "value": "value1"
            }
        ],
        "dnss": []
    },
    {
        "name": "rt-3",
        "location": 1,
        "type": 6,
        "entrys": [],
        "strings": [],
        "dnss": [
            {
                "domain": "www.baidu.com",
                "lid": 1,
                "match_type": 0
            }
        ]
    }
]
获取指定规则表
Action：slb.ruletable.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	规则表名称	是	必须存在
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.get
请求body：
{
    "name": "rt1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	规则表名称
entrys	数组	不涉及	规则条目组成的数组:
entrys > ip：
含义：ip地址，
类型：字符串，
范围：不涉及
entrys > id：
含义：id号
类型：整数，
范围：1-30
entrys > age：
含义：生存时间，
类型：整数，
范围：0-1800
strings	数组	不涉及	规则条目组成的数组
strings > key: 
含义：搜索关键字，
类型：字符串，
范围：1-255
strings > value: 
含义：返回值，
类型：字符串，
范围：0-639
dnss	数组	不涉及	规则条目组成的数组
dnss > domain: 
含义：所需要匹配的域名,
类型：字符串，
范围：1-64
dnss > lid:
含义：规则ID，
类型：整数，
范围：1-30
dnss > match_type:
含义：匹配类型，
类型：整数，
范围：0-2

响应举例：
{
    "name": "rt1",
    "entrys": [
      {
        "ip": "1.2.3.4/32",
        "id": 1,
        "age": 0
      },
      {
        "ip": "1.2.3.5/32",
        "id": 2,
        "age": 123
      }
    ]
}
增加规则表
Action：slb.ruletable.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	规则表名称	是	唯一
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.add
请求body：
{
    "ruletable":
        {
          "name": "rt1"  
        }
}
删除规则表
Action：slb.ruletable.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	规则表名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.del
请求body：
{
    "name": "rt1"
}
增加规则表条目
Action：slb.ruletable.entry.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	规则表名称	是	必须存在
entrys	数组	不涉及	规则条目组成的数组	是	规则条目组成的数组:
entrys > ip：
含义：ip地址，
类型：字符串，
范围：不涉及
entrys > id：
含义：id号
类型：整数，
范围：1-30
entrys > age：
含义：生存时间，
类型：整数，
范围：0-1800

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.entry.add
请求body：
{
    "name": "rt1",
    "entrys": [
      {
        "ip": "1.2.3.4/32",
        "id": 1,
        "age": 0
      },
      {
        "ip": "1.2.3.5/32",
        "id": 2,
        "age": 123
      }
    ]
}
删除规则表条目
Action：slb.ruletable.entry.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	规则表名称	是	必须存在
entrys	数组	不涉及	规则条目组成的数组	是	规则条目组成的数组:
entrys > ip：
含义：ip地址，
类型：字符串，
范围：不涉及

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.entry.del
请求body：
{
    "name": "rt1",
    "entrys": [
      {
        "ip": "1.2.3.4/32"
      }
    ]
}


上传规则表文件
Action：slb.ruletable.file.upload&name=policy_name
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	规则表名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.file.upload&name=policy_name

	此API需要使用form-data的方式上传规则表文件
参数name在URL中不在Body中
增加规则表字符串条目
Action：slb.ruletable.string.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	规则表名称	是	必须存在
strings	数组	不涉及	规则条目组成的数组	是	规则条目组成的数组
strings > key: 
含义：搜索关键字，
类型：字符串，
范围：1-255
strings > value: 
含义：返回值，
类型：字符串，
范围：0-639

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.string.add
请求body：
{
    "name": "rt1",
    "strings": [
        {
            "key": "test1",
            "value": "na"
        }
    ]
 }

删除规则表字符条目
Action：slb.ruletable.string.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	规则表名称	是	必须存在
strings	数组	不涉及	规则条目组成的数组	是	规则条目组成的数组
strings > key: 
含义：搜索关键字，
类型：字符串，
范围：1-255
strings > value: 
含义：返回值，
类型：字符串，
范围：0-639

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.string.del
请求body：
{
    "name": "rt1",
    "strings": [
        {
            "key": "test1",
            "value": "na"
        }
    ]
 }
增加规则表DNS条目
Action：slb.ruletable.dns.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	规则表名称	是	必须存在
dnss	数组	不涉及	规则条目组成的数组	是	规则条目组成的数组
dnss > domain: 
含义：所需要匹配的域名,
类型：字符串，
范围：1-64
dnss > lid:
含义：规则ID，
类型：整数，
范围：1-30
dnss > match_type:
含义：匹配类型，
类型：整数，
范围：0-2

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.dns.add
请求body：
{
    "name": "rt1",
    "dnss": [
        {
                "domain": "www.ddd.com",
                "lid": 3,
                "match_type": 0       
 }
    ]
 }

删除规则表DNS条目
Action：slb.ruletable.dns.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	规则表名称	是	必须存在
dnss	数组	不涉及	规则条目组成的数组	是	规则条目组成的数组
dnss > domain: 
含义：所需要匹配的域名,
类型：字符串，
范围：1-64
dnss > lid:
含义：规则ID，
类型：整数，
范围：1-30
dnss > match_type:
含义：匹配类型，
类型：整数，
范围：0-2

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.ruletable.dns.del
请求body：
{
    "name": "rt1",
    "dnss": [
        {
            "domain": "www.baidu.com",
 	    "lid": 3,
            "match_type": 0
        }
    ]
 }

策略
策略模板列表
Action：slb.policy.list
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.policy.list
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	策略模版名称
match_dst_ip	整数	0-1	匹配目的ip地址;1:是；0:否
match_overlap	整数	0-1	覆盖匹配;1:是；0:否
bwlist_name	字符串	长度1-191	黑白名单名称
ruletable_name	字符串	长度1-191	规则表名称
match_client	整数	0-2	客户端匹配方式;
0:源ip匹配；
1:目的ip匹配；
2:头名称匹配
header_name	字符串	长度1-191	头名称
bwlists	数组	不涉及	基于黑白名单的策略规则列表
bwlists > type: 
含义：算法，
类型：字符串，
范围：范围1-63
bwlists > id: 
含义：黑白名单条目id，
类型：整数，
范围：范围1-31
ruletables	数组	不涉及	基于规则表的策略规则列表
策略规则列表组成的数组如下：
ruletables > id: 
含义：规则表条目id，
类型：整数，
范围：范围1-30
ruletables > conn_limit: 
含义：并发连接限制，
类型：整数，
范围：0-1048575
ruletables > conn_rate_limit: 
含义：连接速率限制，
类型：整数，
范围：0-2147483647
ruletables > req_limit: 
含义：并发请求限制，
类型：整数，
范围：0-1048575
ruletables > req_rate_limit: 
含义：请求速率限制，
类型：整数，
范围：0-4294967295
ruletables > type: 
含义：算法，
类型：整数，
范围：0-31
ruletables > lock_time: 
含义：锁定时间，
类型：整数，
范围：0-1023
pool_policys	数组	不涉及	基于acl的策略规则列表
pool_policys > acl_id: 
含义：acl id，
类型：整数，
范围：2-198
pool_policys > pool: 
含义：服务池名称，
类型：字符串，
范围：1-191
响应举例：
[{
  "name": "p1",
  "match_dst_ip": 1,
  "match_overlap": 1,
  "bwlist_name": "bwl",
  "ruletable_name": "rt0",
  "match_client": 2,
  "header_name": "head",
  "bwlists": [
    {
      "type": "pool",
      "id": 1
    },
    {
      "type": "RESET",
      "id": 2
    },
    {
      "type": "DROP",
      "id": 3
    }
  ],
  "ruletables": [
    {
      "id": 1,
      "conn_limit": 123,
      "conn_rate_limit": 456,
      "req_limit": 789,
      "req_rate_limit": 555,
      "type": 1,
      "lock_time": 666
    }
  ],
  "pool_policys": [
    {
      "acl_id": 101,
      "pool": "pool"
    }
  ]
}]

分区获取common和自己分区的策略列表
Action：slb.policy.list.withcommon
请求参数：无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.policy.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	策略模版名称
match_dst_ip	整数	0-1	匹配目的ip地址;1:是；0:否
match_overlap	整数	0-1	覆盖匹配;1:是；0:否
bwlist_name	字符串	长度1-191	黑白名单名称
ruletable_name	字符串	长度1-191	规则表名称
match_client	整数	0-2	客户端匹配方式;
0:源ip匹配；
1:目的ip匹配；
2:头名称匹配
header_name	字符串	长度1-191	头名称
bwlists	数组	不涉及	基于黑白名单的策略规则列表
bwlists > type: 
含义：算法，
类型：字符串，
范围：范围1-63
bwlists > id: 
含义：黑白名单条目id，
类型：整数，
范围：范围1-31
ruletables	数组	不涉及	基于规则表的策略规则列表
策略规则列表组成的数组如下：
ruletables > id: 
含义：规则表条目id，
类型：整数，
范围：范围1-30
ruletables > conn_limit: 
含义：并发连接限制，
类型：整数，
范围：0-1048575
ruletables > conn_rate_limit: 
含义：连接速率限制，
类型：整数，
范围：0-2147483647
ruletables > req_limit: 
含义：并发请求限制，
类型：整数，
范围：0-1048575
ruletables > req_rate_limit: 
含义：请求速率限制，
类型：整数，
范围：0-4294967295
ruletables > type: 
含义：算法，
类型：整数，
范围：0-31
ruletables > lock_time: 
含义：锁定时间，
类型：整数，
范围：0-1023
pool_policys	数组	不涉及	基于acl的策略规则列表
pool_policys > acl_id: 
含义：acl id，
类型：整数，
范围：2-198
pool_policys > pool: 
含义：服务池名称，
类型：字符串，
范围：1-191
响应举例：
[
    {
        "name": "partition_policy1",
        "match_dst_ip": 0,
        "match_overlap": 0,
        "bwlist_name": "",
        "ruletable_name": "",
        "match_client": 0,
        "header_name": "",
        "bwlists": [],
        "ruletables": [],
        "pool_policys": []
    },
    {
        "name": "common/policy2",
        "match_dst_ip": 0,
        "match_overlap": 0,
        "bwlist_name": "",
        "ruletable_name": "co_rule_test_for_va",
        "match_client": 0,
        "header_name": "",
        "bwlists": [
            {
                "type": "DROP",
                "id": 1
            }
        ],
        "ruletables": [],
        "pool_policys": []
    }
]

策略模板获取
Action：slb.policy.get
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	策略模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.policy.get
请求body：
{
    "name": "p1"
}
响应参数：
名称	类型	范围	含义
name	字符串	长度1-191	策略模版名称
match_dst_ip	整数	0-1	匹配目的ip地址;1:是；0:否
match_overlap	整数	0-1	覆盖匹配;1:是；0:否
bwlist_name	字符串	长度1-191	黑白名单名称
ruletable_name	字符串	长度1-191	规则表名称
match_client	整数	0-2	客户端匹配方式;
0:源ip匹配；
1:目的ip匹配；
2:头名称匹配
header_name	字符串	长度1-63	头名称
bwlists	数组	不涉及	基于黑白名单的策略规则列表
bwlists > type: 
含义：算法，
类型：字符串，
范围：范围1-63
bwlists > id: 
含义：黑白名单条目id，
类型：整数，
范围：范围1-31
ruletables	数组	不涉及	基于规则表的策略规则列表
策略规则列表组成的数组如下：
ruletables > id: 
含义：规则表条目id，
类型：整数，
范围：范围1-30
ruletables > conn_limit: 
含义：并发连接限制，
类型：整数，
范围：0-1048575
ruletables > conn_rate_limit: 
含义：连接速率限制，
类型：整数，
范围：0-2147483647
ruletables > req_limit: 
含义：并发请求限制，
类型：整数，
范围：0-1048575
ruletables > req_rate_limit: 
含义：请求速率限制，
类型：整数，
范围：0-4294967295
ruletables > type: 
含义：算法，
类型：整数，
范围：0-31
ruletables > lock_time: 
含义：锁定时间，
类型：整数，
范围：0-1023
pool_policys	数组	不涉及	基于acl的策略规则列表
pool_policys > acl_id: 
含义：acl id，
类型：整数，
范围：2-198
pool_policys > pool: 
含义：服务池名称，
类型：字符串，
范围：1-191

响应举例：
{
  "name": "p1",
  "match_dst_ip": 1,
  "match_overlap": 1,
  "bwlist_name": "bwl",
  "ruletable_name": "rt0",
  "match_client": 2,
  "header_name": "head",
  "bwlists": [
    {
      "type": "pool",
      "id": 1
    },
    {
      "type": "RESET",
      "id": 2
    },
    {
      "type": "DROP",
      "id": 3
    }
  ],
  "ruletables": [
    {
      "id": 1,
      "conn_limit": 123,
      "conn_rate_limit": 456,
      "req_limit": 789,
      "req_rate_limit": 555,
      "type": 1,
      "lock_time": 666
    }
  ],
  "pool_policys": [
    {
      "acl_id": 101,
      "pool": "pool"
    }
  ]
}
策略模板增加
Action：slb.policy.add
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	策略模版名称	是	唯一
match_dst_ip	整数	0-1	匹配目的ip地址;	否	1:是；0:否；缺省值:0
match_overlap	整数	0-1	覆盖匹配;1:是；0:否	否	1:是；0:否；缺省值:0
bwlist_name	字符串	长度1-191	黑白名单名称	否	缺省值:"" 空字符
ruletable_name	字符串	长度1-191	规则表名称	否	缺省值:"" 空字符
match_client	整数	0-2	客户端匹配方式;
	否	0:源IP匹配；
1:目的IP匹配；
2:头名称匹配；缺省值:0
header_name	字符串	长度1-63	头名称	否	缺省值:"" 空字符
bwlists	数组	不涉及	基于黑白名单的策略规则列表	否	基于黑白名单的策略规则列表
bwlists > type: 
含义：算法，
类型：字符串，
范围：范围1-63
bwlists > id: 
含义：黑白名单条目id，
类型：整数，
范围：范围1-31
ruletables	数组	不涉及	基于规则表的策略规则列表	否	基于规则表的策略规则列表
策略规则列表组成的数组如下：
ruletables > id: 
含义：规则表条目id，
类型：整数，
范围：范围1-30
ruletables > conn_limit: 
含义：并发连接限制，
类型：整数，
范围：0-1048575
ruletables > conn_rate_limit: 
含义：连接速率限制，
类型：整数，
范围：0-2147483647
ruletables > req_limit: 
含义：并发请求限制，
类型：整数，
范围：0-1048575
ruletables > req_rate_limit: 
含义：请求速率限制，
类型：整数，
范围：0-4294967295
ruletables > type: 
含义：算法，
类型：整数，
范围：0-31
ruletables > lock_time: 
含义：锁定时间，
类型：整数，
范围：0-1023
pool_policys	数组	不涉及	基于acl的策略规则列表	否	基于acl的策略规则列表
pool_policys > acl_id: 
含义：acl id，
类型：整数，
范围：2-198
pool_policys > pool: 
含义：服务池名称，
类型：字符串，
范围：1-191
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.policy.add
请求body：
{
  "name": "p1",
  "match_dst_ip": 1,
  "match_overlap": 1,
  "bwlist_name": "bwl",
  "ruletable_name": "rt0",
  "match_client": 2,
  "header_name": "head",
  "bwlists": [
    {
      "type": "pool",
      "id": 1
    },
    {
      "type": "RESET",
      "id": 2
    },
    {
      "type": "DROP",
      "id": 3
    }
  ],
  "ruletables": [
    {
      "id": 1,
      "conn_limit": 123,
      "conn_rate_limit": 456,
      "req_limit": 789,
      "req_rate_limit": 555,
      "type": 1,
      "lock_time": 666
    }
  ],
  "pool_policys": [
    {
      "acl_id": 101,
      "pool": "pool"
    }
  ]
}

策略模板编辑
Action：slb.policy.edit
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	策略模版名称	是	必须存在
match_dst_ip	整数	0-1	匹配目的ip地址;	否	1:是；0:否；缺省值:0
match_overlap	整数	0-1	覆盖匹配;1:是；0:否	否	1:是；0:否；缺省值:0
bwlist_name	字符串	长度1-191	黑白名单名称	否	缺省值:"" 空字符
ruletable_name	字符串	长度1-191	规则表名称	否	缺省值:"" 空字符
match_client	整数	0-2	客户端匹配方式;
	否	0:源ip匹配；
1:目的ip匹配；
2:头名称匹配；缺省值:0
header_name	字符串	长度1-63	头名称	否	缺省值:"" 空字符
bwlists	数组	不涉及	基于黑白名单的策略规则列表	否	基于黑白名单的策略规则列表
bwlists > type: 
含义：算法，
类型：字符串，
范围：范围1-63
bwlists > id: 
含义：黑白名单条目id，
类型：整数，
范围：范围1-31
ruletables	数组	不涉及	基于规则表的策略规则列表	否	基于规则表的策略规则列表
策略规则列表组成的数组如下：
ruletables > id: 
含义：规则表条目id，
类型：整数，
范围：范围1-30
ruletables > conn_limit: 
含义：并发连接限制，
类型：整数，
范围：0-1048575
ruletables > conn_rate_limit: 
含义：连接速率限制，
类型：整数，
范围：0-2147483647
ruletables > req_limit: 
含义：并发请求限制，
类型：整数，
范围：0-1048575
ruletables > req_rate_limit: 
含义：请求速率限制，
类型：整数，
范围：0-4294967295
ruletables > type: 
含义：算法，
类型：整数，
范围：0-31
ruletables > lock_time: 
含义：锁定时间，
类型：整数，
范围：0-1023
pool_policys	数组	不涉及	基于acl的策略规则列表	否	基于acl的策略规则列表
pool_policys > acl_id: 
含义：acl id，
类型：整数，
范围：2-198
pool_policys > pool: 
含义：服务池名称，
类型：字符串，
范围：1-191

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.policy.edit
请求body：
{
  "name": "p1",
  "match_dst_ip": 1,
  "match_overlap": 1,
  "bwlist_name": "bwl",
  "ruletable_name": "rt0",
  "match_client": 2,
  "header_name": "head",
  "bwlists": [
    {
      "type": "pool",
      "id": 1
    },
    {
      "type": "RESET",
      "id": 2
    },
    {
      "type": "DROP",
      "id": 3
    }
  ],
  "ruletables": [
    {
      "id": 1,
      "conn_limit": 123,
      "conn_rate_limit": 456,
      "req_limit": 789,
      "req_rate_limit": 555,
      "type": 1,
      "lock_time": 666
    }
  ],
  "pool_policys": [
    {
      "acl_id": 101,
      "pool": "pool"
    }
  ]
}

策略模板删除
Action：slb.policy.del
请求参数：
名称	类型	范围	含义	必选	备注
name	字符串	长度1-191	策略模版名称	是	必须存在

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dbc121e55cc33c67911a99ce4829db&action=slb.policy.del
请求body：
{
    "name": "p1"
}
Web安全
WAF模板
获取WAF模板列表
Action:  waf.profile.list

请求参数:无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.profile.list
响应参数：
名称	类型	范围	含义
name	字符串	1-191	WAF模板名称
rule_name	字符串	0-63	WAF规则表名称，默认空串
white_url_list	字符串列表	最多32个，每个长度1-127	url白名单列表：最多32个正则表达式，每个表达式长度1-127	正则表达式后台检查合法性，不对会返回
black_url_list	字符串列表	最多8个，每个长度1-127	url白名单列表：最多32个正则表达式，每个表达式长度1-127	正则表达式后台检查合法性，不对会返回
uri_stick_check	布尔	0-1	url严格检查开关：0关闭1开启
mode	整数	0-2	WAF模式： 0： normal  流量识别后进行流量阻断
1： forward  只进行流量识别操作，不阻断
2： learning  学习模式，自动学习流量规则
behavior	整数	0-1	阻断行为：0：block数据流
1：drop数据报
enable	布尔	0-1	使能：表示模版是否工作，0关闭，1开启动
logging	布尔	0-1	表示是否开启log日志：0关闭，1开启
injection_sql	布尔	0-1	表示是否开始sql注入：0关闭，1开启
injection_xss	布尔	0-1	表示是否开始xss注入：0关闭，1开启
disable_len_check	布尔	0-1	http字段长度检查：表示是否关闭http字段长度检查
headers_mlen	整数	1-65535	头部允许最大长度
url_mlen	整数	1-65535	URL允许最大长度
cookie_mlen	整数	1-65535	cookie允许最大长度
description	字符串
	长度1-191	描述

响应举例：
[{
	"name":	"wafprofile2",
	"rule_name":	"",
"description":	"test",
	"white_url_list":	["^/abcb", "^/aa"],
		"black_url_list":	["^/123"],
	"uri_stick_check":	0,
		"mode":	0,
		"behavior":	1,
		"enable":	1,
		"logging":	1,
		"injection_sql":	1,
		"injection_xss":	1,
		"disable_len_check":	0,
		"headers_mlen":	8192,
		"url_mlen":	2803,
		"cookie_mlen":	4079
	}, {
		"name":	"wafprofile1",
		"rule_name":	"",
		"white_url_list":	["^/abc", "^/aaa"],
		"black_url_list":	["^/123"],
		"uri_stick_check":	0,
		"mode":	1,
		"behavior":	1,
		"enable":	1,
		"logging":	1,
		"injection_sql":	1,
		"injection_xss":	1,
		"disable_len_check":	1,
		"headers_mlen":	8192,
		"url_mlen":	2803,
		"cookie_mlen":	4079
	}]

partition分区获取common分区WAF模板列表
Action:  waf.profile.list.withcommon

请求参数:无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.profile.list.withcommon
响应参数：
名称	类型	范围	含义
name	字符串	1-191	WAF模板名称
rule_name	字符串	0-63	WAF规则表名称，默认空串
white_url_list	字符串列表	最多32个，每个长度1-127	url白名单列表：最多32个正则表达式，每个表达式长度1-127	正则表达式后台检查合法性，不对会返回
black_url_list	字符串列表	最多8个，每个长度1-127	url白名单列表：最多32个正则表达式，每个表达式长度1-127	正则表达式后台检查合法性，不对会返回
uri_stick_check	布尔	0-1	url严格检查开关：0关闭1开启
mode	整数	0-2	WAF模式： 0： normal  流量识别后进行流量阻断
1： forward  只进行流量识别操作，不阻断
2： learning  学习模式，自动学习流量规则
behavior	整数	0-1	阻断行为：0：block数据流
1：drop数据报
enable	布尔	0-1	使能：表示模版是否工作，0关闭，1开启动
logging	布尔	0-1	表示是否开启log日志：0关闭，1开启
injection_sql	布尔	0-1	表示是否开始sql注入：0关闭，1开启
injection_xss	布尔	0-1	表示是否开始xss注入：0关闭，1开启
disable_len_check	布尔	0-1	http字段长度检查：表示是否关闭http字段长度检查
headers_mlen	整数	1-65535	头部允许最大长度
url_mlen"	整数	1-65535	url允许最大长度
cookie_mlen	整数	1-65535	cookie允许最大长度
description	字符串
	长度1-191	描述


响应举例：
[{
		"name":	"wafprofile2",
		"rule_name":	"",
"description":	"test",
		"white_url_list":	["^/abcb", "^/aa"],
		"black_url_list":	["^/123"],
		"uri_stick_check":	0,
		"mode":	0,
		"behavior":	1,
		"enable":	1,
		"logging":	1,
		"injection_sql":	1,
		"injection_xss":	1,
		"disable_len_check":	0,
		"headers_mlen":	8192,
		"url_mlen":	2803,
		"cookie_mlen":	4079
	},{
        "name": "common/waf_194",
        "rule_name": "waf_rules.txt",
        "white_url_list": [
            "987654321"
        ],
        "black_url_list": [
            "1234567e"
        ],
        "uri_stick_check": 1,
        "mode": 1,
        "behavior": 0,
        "enable": 1,
        "logging": 1,
        "injection_sql": 1,
        "injection_xss": 1,
        "disable_len_check": 0,
        "headers_mlen": 100,
        "url_mlen": 1234,
        "cookie_mlen": 1234
    	}]
获取指定WAF模板
Action:  waf.profile.get

请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	1-191	waf模板名称	是	必须存在
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.profile.get
请求body：
{
   	"name":	"wafprofile1"
}
响应参数：
名称	类型	范围	含义
name	字符串	1-63	waf模板名称
rule_name	字符串	0-63	waf规则表名称，默认空串
white_url_list	字符串列表	最多32个，每个长度1-127	url白名单列表：最多32个正则表达式，每个表达式长度1-127	正则表达式后台检查合法性，不对会返回
black_url_list	字符串列表	最多8个，每个长度1-127	url白名单列表：最多32个正则表达式，每个表达式长度1-127	正则表达式后台检查合法性，不对会返回
uri_stick_check	布尔	0-1	url严格检查开关：0关闭1开启
mode	整数	0-2	waf模式： 0： normal  流量识别后进行流量阻断
1： forward  只进行流量识别操作，不阻断
2： learning  学习模式，自动学习流量规则
behavior	整数	0-1	阻断行为：0：block数据流
1：drop数据报
enable	布尔	0-1	使能：表示模版是否工作，0关闭，1开启动
logging	布尔	0-1	表示是否开启log日志：0关闭，1开启
injection_sql	布尔	0-1	表示是否开始sql注入：0关闭，1开启
injection_xss	布尔	0-1	表示是否开始xss注入：0关闭，1开启
disable_len_check	布尔	0-1	http字段长度检查：表示是否关闭http字段长度检查
headers_mlen	整数	1-65535	头部允许最大长度
url_mlen	整数	1-65535	url允许最大长度
cookie_mlen	整数	1-65535	cookie允许最大长度
description	字符串
	长度1-191	描述
响应举例：
{
   	"name":	"wafprofile1",
   	"rule_name":	"naxsi_core.rules",
   	"white_url_list":	["^/abcb", "^/aa"],
   	"black_url_list":	["^/123"],
   	"uri_stick_check":	0,
"description":	"test",
   	"mode":	0,
   	"behavior":	1,
   	"enable":	1,
   	"logging":	1,
   	"injection_sql":	1,
   	"injection_xss":	1,
   	"disable_len_check":	0,
   	"headers_mlen":	8192,
   	"url_mlen":	2803,
   	"cookie_mlen":	4079
   }
WAF模板增加
Action:  waf.profile.add

请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	1-191	waf模板名称	是	唯一
rule_name	字符串	0-63	waf规则表名称	否	默认空串
white_url_list	字符串列表	最多32个，每个长度1-127	url白名单列表(默认[])：最多32个正则表达式，每个表达式长度1-127	正则表达式后台检查合法性，不对会返回	否	
black_url_list	字符串列表	最多8个，每个长度1-127	url白名单列表(默认[])：最多32个正则表达式，每个表达式长度1-127	正则表达式后台检查合法性，不对会返回	否	
uri_stick_check	布尔	0-1	url严格检查开关：0关闭1开启,默认0	否	
mode	整数	0-2	waf模式(默认0)： 0： normal  流量识别后进行流量阻断
1： forward  只进行流量识别操作，不阻断
2： learning  学习模式，自动学习流量规则	否	
behavior	整数	0-1	阻断行为(默认0)：0：block数据流
1：drop数据报	否	
enable	整数	0-1	使能：表示模版是否工作，0关闭，1开启动, 默认0	否	
logging	整数	0-1	表示是否开启log日志：0关闭，1开启, 默认0	否	
injection_sql	整数	0-1	表示是否开始sql注入：0关闭，1开启, 默认0	否	
injection_xss	整数	0-1	表示是否开始xss注入：0关闭，1开启, 默认0	否	
disable_len_check	整数	0-1	http字段长度检查：表示是否关闭http字段长度检查,默认0	否	0时表示不关闭检查，1表示关闭检查
headers_mlen	整数	1-65535	头部允许最大长度,默认8192	否	
url_mlen	整数	1-65535	url允许最大长度,默认2803	否	
cookie_mlen	整数	1-65535	cookie允许最大长度,默认4079	否	
description	字符串
	长度1-191	描述	否	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.profile.add 
请求body：
{
        "name": "p1",
        "description": "",
        "rule_name": "wrule_123.txt",
        "white_url_list": [
            "^/"
        ],
        "black_url_list": [
            "^/"
        ],
        "uri_stick_check": 1,
        "mode": 2,
        "behavior": 1,
        "enable": 1,
        "logging": 1,
        "injection_sql": 1,
        "injection_xss": 1,
        "disable_len_check": 0,
        "headers_mlen": 8192,
        "url_mlen": 2803,
        "cookie_mlen": 4079
    }

	rule_name是上传的WAF规则的名称

WAF模板编辑
Action:  waf.profile.edit

请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	1-191	waf模板名称	是	必须存在
rule_name	字符串	0-63	waf规则表名称	否	默认空串
white_url_list	字符串列表	最多32个，每个长度1-127	url白名单列表(默认[])：最多32个正则表达式，每个表达式长度1-127	正则表达式后台检查合法性，不对会返回	否	
black_url_list	字符串列表	最多8个，每个长度1-127	url白名单列表(默认[])：最多32个正则表达式，每个表达式长度1-127	正则表达式后台检查合法性，不对会返回	否	
uri_stick_check	整数	0-1	url严格检查开关：0关闭1开启,默认0	否	
mode	整数	0-2	waf模式(默认0)： 0： normal  流量识别后进行流量阻断
1： forward  只进行流量识别操作，不阻断
2： learning  学习模式，自动学习流量规则	否	
behavior	整数	0-1	阻断行为(默认0)：0：block数据流
1：drop数据报	否	
enable	整数	0-1	使能：表示模版是否工作，0关闭，1开启动, 默认0	否	
logging	整数	0-1	表示是否开启log日志：0关闭，1开启, 默认0	否	
injection_sql	整数	0-1	表示是否开始sql注入：0关闭，1开启, 默认0	否	
injection_xss	整数	0-1	表示是否开始xss注入：0关闭，1开启, 默认0	否	
disable_len_check	整数	0-1	http字段长度检查：表示是否关闭http字段长度检查,默认0	否	0时表示不关闭检查，1表示关闭检查
headers_mlen	整数	1-65535	头部允许最大长度,默认8192	否	
url_mlen	整数	1-65535	url允许最大长度,默认2803	否	
cookie_mlen	整数	1-65535	cookie允许最大长度,默认4079	否	

请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.profile.edit 
请求body：
{
        "name": "p1",
        "description": "",
        "rule_name": "wrule_123.txt",
        "white_url_list": [
            "^/"
        ],
        "black_url_list": [
            "^/"
        ],
        "uri_stick_check": 1,
        "mode": 2,
        "behavior": 1,
        "enable": 1,
        "logging": 1,
        "injection_sql": 1,
        "injection_xss": 1,
        "disable_len_check": 0,
        "headers_mlen": 8192,
        "url_mlen": 28030,
        "cookie_mlen": 65535
    }

WAF模板删除
Action:  waf.profile.del

请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	1-191	waf模板名称	是	必须存在
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.profile.del 
请求body：
{
"name":	"p1"
}
WAF规则
获取WAF规则脚本列表
Action:  waf.rule.list

请求参数:无
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.rule.list 
响应参数:
名称	类型	范围	含义
name	字符串	1-63	waf规则文件名
check	布尔	0-1	语法是否检查
1表示语法合法， 0表示语法不合法或没有检查语法
ref_count	整数	0-65535	当前使用数量
响应举例：
[{
		"name":	"naxsi_core.rules",
		"check":	1,
		"ref_count":	2
	}, {
		"name":	"main_core.rules",
		"check":	1,
		"ref_count":	0
	}]
获取指定WAF规则脚本
Action:  waf.rule.get

请求参数:
名称	类型	范围	含义
name	字符串	1-63	waf规则文件名
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.rule.get
请求body：
{
	"name":	"naxsi_core.rules"
}
响应参数:
名称	类型	范围	含义
name	字符串	1-63	waf规则文件名
check	布尔	0-1	语法是否检查
1表示语法合法， 0表示语法不合法或没有检查语法
ref_count	整数	0-65535	当前使用数量
响应举例：
{
   	"name":	"naxsi_core.rules",
   	"check":	1,
   	"ref_count":	2
}
WAF规则脚本删除
Action:  waf.rule.del

请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	1-63	waf规则文件名	是	必须存在
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.rule.del
请求body：
{
	"name":	"naxsi_core.rules"
}
WAF规则脚本下载
Action:  waf.rule.download

请求参数:
名称	类型	范围	含义	必选	备注
name	字符串	1-63	waf规则文件名	是	必须存在
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.rule.download
请求body：
{
	"name":	"naxsi_core.rules"
}
	此API会下载一个naxsi_core.rules的文件
WAF规则脚本上传
Action:  waf.rule.upload

请求参数:无
请求举例：
POST
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.rule.upload
	此API使用form-data的方式上传一个WAF规则脚本文件
WAF统计获取
Action:  waf.vserver.statis
请求参数:无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.vserver.statis
响应参数:
名称	类型	范围	含义
name	字符串	1-63	waf模板名称
req_check_total	整数	>=0	请求报文总数
req_check_matched	整数	>=0	请求报文匹配数量
req_check_block	整数	>=0	请求报文阻挡数量
uri_buf_check_total	整数	>=0	uri超长报文总数
uri_buf_check_matched	整数	>=0	uri超长报文匹配数量
uri_buf_check_block	整数	>=0	uri超长报阻挡数量
hdr_buf_check_total	整数	>=0	headers超长检查报文总数
hdr_buf_check_matched	整数	>=0	headers超长检查匹配数量
hdr_buf_check_block	整数	>=0	headers超常检查阻挡数量
cookie_buf_check_total	整数	>=0	cookie超长检查报文总数
cookie_buf_check_matched	整数	>=0	cookie超长报文检查匹配数量
cookie_buf_check_block	整数	>=0	cookie超长报文检查阻挡数量
uri_wlist_check_total	整数	>=0	uri白名单检查报文总数
uri_wlist_check_matched	整数	>=0	uri白名单检查报文匹配数量
uri_wlist_check_block	整数	>=0	uri白名单检查报文阻挡数量
uri_blist_check_total	整数	>=0	uri黑名单检查报文总数
uri_blist_check_matched	整数	>=0	uri黑名单检查报文匹配数量
uri_blist_check_block	整数	>=0	uri黑名单检查报文阻挡数量
sql_injection_check_total	整数	>=0	sql注入检查总数
sql_injection_check_matched	整数	>=0	sql注入检查匹配数量
sql_injection_check_block	整数	>=0	sql注入检查阻挡数量
xss_injection_check_total	整数	>=0	xss注入检查总数
xss_injection_check_matched	整数	>=0	xss注入检查匹配数量
xss_injection_check_block	整数	>=0	xss注入检查阻挡数量
rule_check_total	整数	>=0	waf规则检查总数
rule_check_matched	整数	>=0	waf规则匹配数
rule_check_block	整数	>=0	wad规则阻挡数量
响应举例：
[{
		"name":	"wafhttp",          
		"req_check_total":	0,
		"req_check_matched":	0,
		"req_check_block":	0,
		"uri_buf_check_total":	0,
		"uri_buf_check_matched":	0,
		"uri_buf_check_block":	0,
		"hdr_buf_check_total":	0,
		"hdr_buf_check_matched":	0,
		"hdr_buf_check_block":	0,
		"cookie_buf_check_total":	0,
		"cookie_buf_check_matched":	0,
		"cookie_buf_check_block":	0,
		"uri_wlist_check_total":	0,
		"uri_wlist_check_matched":	0,
		"uri_wlist_check_block":	0,
		"uri_blist_check_total":	0,
		"uri_blist_check_matched":	0,
		"uri_blist_check_block":	0,
		"sql_injection_check_total":	0,
		"sql_injection_check_matched":	0,
		"sql_injection_check_block":	0,
		"xss_injection_check_total":	0,
		"xss_injection_check_matched":	0,
		"xss_injection_check_block":	0,
		"rule_check_total":	0,
		"rule_check_matched":	0,
		"rule_check_block":	0
}]
WAF统计清除
Action:  waf.vserver.clear
请求参数:无
请求举例：
GET
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=waf.vserver.clear




全局选项
SLB全局混杂设置
获取SLB全局混杂配置
Action:  slb.global.allow_promis_intf_vip.get
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.global.allow_promis_intf_vip.get
名称	类型	范围	含义
status	整数	0,1	slb全局混杂设置，0：关闭，1：开启
响应参数：
响应举例：
{"status ": 0}

设置SLB全局混杂配置
Action:  slb.global.allow_promis_intf_vip.set
请求参数:
名称	类型	范围	含义	必选	备注
status	整数	0,1	slb全局混杂设置	是	0：关闭，1：开启

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.global.allow_promis_intf_vip.set
Body:
{"status": 1}
	当需要使用接口IP地址作为VIP地址时需要开启这个功能,具体步骤如下：
1.配置一个ACL，目的IP地址为接口IP地址，目的端口为准备作为虚拟服务的端口
2.使用该ACL创建一个虚拟地址,
3.使用该虚拟地址创建虚拟服务
4.开启SLB全局混杂功能


SLB全局软关机设置
获取SLB全局软关机配置
Action:  slb.graceful-shutdown.get
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.graceful-shutdown.get
响应参数：
名称	类型	范围	含义
time	整数	0,65535	软关机超时时间，0：表示软关机状态不会超时强制结束
delete	整数	0,1	删除node触发软关机，0：关闭，1：开启
disable	整数	0,1	禁用node触发软关机，0：关闭，1：开启
persist	整数	0,1	禁用node触发软关机后，会话保持表继续有效，0：关闭，1：开启
响应举例：
{
  "graceful_shutdown_node" : {
    "time" : 10000,
    "delete" : 1,
    "disable" : 1,
    "persist" : 1
  }
}
设置SLB全局软关机配置
Action:  slb.graceful-shutdown.set
请求参数: 
名称	类型	范围	含义	必选	备注
time	整数	0,65535	软关机超时时间	是	0：表示软关机状态不会超时强制结束
delete	整数	0,1	删除node触发软关机 	是	0：关闭，1：开启
disable	整数	0,1	禁用node触发软关机 	是	0：关闭，1：开启
persist	整数	0,1	禁用node触发软关机后，会话保持表继续有效	是	0：关闭，1：开启

请求举例：
POST 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.graceful-shutdown.set
Body:
{
  "graceful_shutdown_node" : {
    "time" : 10000,
    "delete" : 1,
    "disable" : 1,
    "persist" : 1
  }
}


SLB全局ICMP速率限制
获取ICMP速率限制配置
Action:  system.rate_limit_icmp.get
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=system.rate_limit_icmp.get
响应参数：
名称	类型	范围	含义
normal_rate_limit	整数	0,65535	速率限制值，0：关闭icmp速率限制，1-65535：开启icmp速率限制并配置速率限制值，单位为packets/second
max_rate_limit	整数	0,65535	锁定门限值，0：关闭锁定，1-65535：使能锁定并配置锁定门限值，单位为packets/second
lockup_period	整数	0,16383	锁定周期，0：关闭锁定周期，1-16383：使能锁定并配置锁定周期时间，单位为秒
响应举例：
{
"rate_limit_icmp":{
"normal_rate_limit":1000,
"max_rate_limit":2000,
"lockup_period":100
}
}

设置ICMP速率限制配置
Action:  system.rate_limit_icmp.set
请求参数:
名称	类型	范围	含义
normal_rate_limit	整数	0,65535	速率限制值，0：关闭icmp速率限制，1-65535：开启icmp速率限制并配置速率限制值，单位为packets/second
max_rate_limit	整数	0,65535	锁定门限值，0：关闭锁定，1-65535：使能锁定并配置锁定门限值，单位为packets/second
lockup_period	整数	0,16383	锁定周期，0：关闭锁定周期，1-16383：使能锁定并配置锁定周期时间，单位为秒

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=system.rate_limit_icmp.set
Body:
{
"rate_limit_icmp":{
"normal_rate_limit":1000,
"max_rate_limit":2000,
"lockup_period":100
}
}
SLB全局TCP新建保护
获取TCP新建保护配置
Action:  system.tcp_syn_protect.get
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=system.tcp_syn_protect.get

响应参数：
名称	类型	范围	含义
reset	整数	0,1	tcp新建保护重置开关，0：关闭，1：开启
rate_limit	整数	0,65535	tcp新建保护速率限制值，0，未开启，1：配置具体速率限制值
响应举例：
{
    "tcp_syn_protect": {
        "reset": 1,
        "rate_limit": 10
    }
}
设置TCP新建保护配置
Action:  system.tcp_syn_protect.set
请求参数:
名称	类型	范围	含义
reset	整数	0,1	tcp新建保护重置开关，0：关闭，1：开启
rate_limit	整数	0,65535	tcp新建保护速率限制值，0，未开启，1：配置具体速率限制值

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=system.tcp_syn_protect.set

Body:
{
    "tcp_syn_protect": {
        "reset": 1,
        "rate_limit": 10
    }
}


SLB全局VLAN一致性检查
获取SLB全局VLAN一致性检查
Action:  system.vlan_keyed_connection.get
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=system.vlan_keyed_connection.get
响应参数：
名称	类型	范围	含义
enable	整数	0,1	vlan一致性检查的开启状态；0：关闭，1：开启
响应举例：
{
    "vlan_keyed_connection": {
        "enable": 0
    }
}
设置SLB全局VLAN一致性检查
Action:  system.vlan_keyed_connection.set
请求参数: 
名称	类型	范围	含义
enable	整数	0,1	vlan一致性检查的开启状态；0：关闭，1：开启
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=system.vlan_keyed_connection.set
{
    "vlan_keyed_connection": {
        "enable": 1
    }
}


SLB全局连接镜像
获取SLB全局连接镜像
Action: global.connection_mirror.get
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=global.connection_mirror.get
响应参数：
名称	类型	范围	含义
global_connection_mirror	整数	0,1	全局连接镜像；0：关闭，1：开启
响应举例：
{
       "global_connection_mirror": 1
}
设置SLB全局连接镜像
Action:  global.connection_mirror.set

请求参数: 
名称	类型	范围	含义
global_connection_mirror	整数	0,1	全局连接镜像；0：关闭，1：开启
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=global.connection_mirror.set
{
    "global_connection_mirror": 1
}

SLB全局路径保持
获取SLB全局路径保持
Action:  global.path_persist.get
请求参数:无
请求举例：
GET http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=global.path_persist.get
名称	类型	范围	含义
global_path_persist	整数	0,1	slb全局路径保持，0：关闭，1：开启
响应参数：
响应举例：
{"global_path_persist":1}
设置SLB全局路径保持
Action:  global.path_persist.set
请求参数:
名称	类型	范围	含义	必选	备注
global_path_persist	整数	0,1	slb全局路径保持	是	0：关闭，1：开启

请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=global.path_persist.set
Body:
{"global_path_persist":1}

SLB全局地址转换
获取SLB全局策略地址转换配置
Action:  global.slb_snat_on_vip.get
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=global.slb_snat_on_vip.get
响应参数：
名称	类型	范围	含义
global_policy_snat
	整数	0,1	0：关闭，1：开启
响应举例：
{
    "global_policy_snat": 0
}
设置SLB全局策略地址转换配置
Action:  global.slb_snat_on_vip.set
请求参数: 
名称	类型	范围	含义
global_policy_snat
	整数	0,1	0：关闭，1：开启

请求举例：
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=global.slb_snat_on_vip.set
POST 
{
    "global_policy_snat": 1
}


获取SLB全局源nat接口地址轮询
Action:  global.slb_snat_interface_iprr.get
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=global.slb_snat_interface_iprr.get
响应参数：
名称	类型	范围	含义
global.slb_snat_interface_iprr
	整数	0,1	0：关闭，1：开启
响应举例：
{
    "global_snat_interface_iprr": 0
}
设置SLB全局源nat接口地址轮询
Action:  global.slb_snat_interface_iprr.set
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=global.slb_snat_interface_iprr.set
响应参数：
名称	类型	范围	含义
global.slb_snat_interface_iprr
	整数	0,1	0：关闭，1：开启
响应举例：
{
    "global_snat_interface_iprr": 1
}





SLB全局虚拟MAC
获取SLB虚拟MAC状态
Action:  slb.global.virtual_mac.get
请求参数:无
请求举例：
GET 
http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.global.virtual_mac.get
响应参数：
名称	类型	范围	含义
gvm	整数	0,1	全局mac状态；0：关闭，1：开启
响应举例：
{
    "gvm": 1
}
设置SLB虚拟MAC状态
Action:  slb.global.virtual_mac.set

请求参数: 
名称	类型	范围	含义
gvm	整数	0,1	全局mac状态；0：关闭，1：开启
请求举例：
POST http://192.168.70.73/adcapi/v2.0/?authkey=dfa0ebc0b62922154bee2943520b24&action=slb.global.virtual_mac.set
{
    "gvm": 1
}



