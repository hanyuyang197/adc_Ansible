#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import sys

# 定义模块参数 - 注意这里只定义了 name 参数
module_args = dict(
    name=dict(type='str', required=True)
)

# 创建 AnsibleModule 实例
module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=False
)

# 打印所有接收到的参数
module.exit_json(
    msg="测试未定义参数",
    all_params=module.params,
    keys_in_params=list(module.params.keys())
)
