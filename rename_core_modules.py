#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量重命名核心模块的 action 和函数名
"""

import os
import re

# 定义核心模块的映射关系
CORE_MODULES = {
    'adc_slb_va.py': {
        'functions': {
            'adc_list_vas': 'adc_slb_va_list',
            'adc_get_va': 'adc_slb_va_get',
            'adc_add_va': 'adc_slb_va_add',
            'adc_edit_va': 'adc_slb_va_edit',
            'adc_delete_va': 'adc_slb_va_del',
            'adc_va_stat_list': 'adc_slb_va_stat_list',
            'adc_va_stat_get': 'adc_slb_va_stat_get',
        },
        'actions': {
            'list_vas': 'slb_va_list',
            'get_va': 'slb_va_get',
            'add_va': 'slb_va_add',
            'edit_va': 'slb_va_edit',
            'delete_va': 'slb_va_del',
            'va_stat_list': 'slb_va_stat_list',
            'va_stat_get': 'slb_va_stat_get',
        }
    },
    'adc_slb_va_vs.py': {
        'functions': {
            'adc_add_vs': 'adc_slb_va_vs_add',
            'adc_edit_vs': 'adc_slb_va_vs_edit',
            'adc_delete_vs': 'adc_slb_va_vs_del',
            'adc_get_vs': 'adc_slb_va_vs_get',
        },
        'actions': {
            'add_vs': 'slb_va_vs_add',
            'edit_vs': 'slb_va_vs_edit',
            'delete_vs': 'slb_va_vs_del',
            'get_vs': 'slb_va_vs_get',
        }
    },
    'adc_slb_va_vs_stat.py': {
        'functions': {
            'adc_get_vs_stat': 'adc_slb_va_vs_stat_get',
            'adc_list_vs_stat_count': 'adc_slb_va_vs_stat_count_list',
        },
        'actions': {
            'get_vs_stat': 'slb_va_vs_stat_get',
            'list_vs_stat_count': 'slb_va_vs_stat_count_list',
        }
    },
    'adc_slb_stat.py': {
        'functions': {
            'adc_node_stat_list': 'adc_slb_node_stat_list',
            'adc_node_stat_get': 'adc_slb_node_stat_get',
            'adc_node_stat_clear': 'adc_slb_node_stat_clear',
            'adc_pool_stat_list': 'adc_slb_pool_stat_list',
            'adc_pool_stat_get': 'adc_slb_pool_stat_get',
            'adc_pool_stat_clear': 'adc_slb_pool_stat_clear',
            'adc_session_clear': 'adc_slb_session_clear',
        },
        'actions': {
            'node_stat_list': 'slb_node_stat_list',
            'node_stat_get': 'slb_node_stat_get',
            'node_stat_clear': 'slb_node_stat_clear',
            'pool_stat_list': 'slb_pool_stat_list',
            'pool_stat_get': 'slb_pool_stat_get',
            'pool_stat_clear': 'slb_pool_stat_clear',
            'session_clear': 'slb_session_clear',
        }
    },
    'adc_slb_healthcheck.py': {
        'functions': {
            'adc_list_healthchecks': 'adc_slb_healthcheck_list',
            'adc_get_healthcheck': 'adc_slb_healthcheck_get',
            'adc_add_healthcheck': 'adc_slb_healthcheck_add',
            'adc_edit_healthcheck': 'adc_slb_healthcheck_edit',
            'adc_delete_healthcheck': 'adc_slb_healthcheck_del',
        },
        'actions': {
            'list_healthchecks': 'slb_healthcheck_list',
            'get_healthcheck': 'slb_healthcheck_get',
            'add_healthcheck': 'slb_healthcheck_add',
            'edit_healthcheck': 'slb_healthcheck_edit',
            'delete_healthcheck': 'slb_healthcheck_del',
        }
    },
    'adc_slb_sslclient.py': {
        'functions': {
            'adc_list_sslclient_profiles': 'adc_slb_sslclient_list',
            'adc_list_sslclient_profiles_withcommon': 'adc_slb_sslclient_list_withcommon',
            'adc_get_sslclient_profile': 'adc_slb_sslclient_get',
            'adc_add_sslclient_profile': 'adc_slb_sslclient_add',
            'adc_edit_sslclient_profile': 'adc_slb_sslclient_edit',
            'adc_delete_sslclient_profile': 'adc_slb_sslclient_del',
        },
        'actions': {
            'list_profiles': 'slb_sslclient_list',
            'list_profiles_withcommon': 'slb_sslclient_list_withcommon',
            'get_profile': 'slb_sslclient_get',
            'add_profile': 'slb_sslclient_add',
            'edit_profile': 'slb_sslclient_edit',
            'delete_profile': 'slb_sslclient_del',
        }
    },
    'adc_slb_sslserver.py': {
        'functions': {
            'adc_list_sslserver_profiles': 'adc_slb_sslserver_list',
            'adc_list_sslserver_profiles_withcommon': 'adc_slb_sslserver_list_withcommon',
            'adc_get_sslserver_profile': 'adc_slb_sslserver_get',
            'adc_add_sslserver_profile': 'adc_slb_sslserver_add',
            'adc_edit_sslserver_profile': 'adc_slb_sslserver_edit',
            'adc_delete_sslserver_profile': 'adc_slb_sslserver_del',
        },
        'actions': {
            'list_profiles': 'slb_sslserver_list',
            'list_profiles_withcommon': 'slb_sslserver_list_withcommon',
            'get_profile': 'slb_sslserver_get',
            'add_profile': 'slb_sslserver_add',
            'edit_profile': 'slb_sslserver_edit',
            'delete_profile': 'slb_sslserver_del',
        }
    },
    'adc_slb_profile_dns.py': {
        'functions': {
            'adc_list_dns_profiles': 'adc_slb_profile_dns_list',
            'adc_list_dns_profiles_withcommon': 'adc_slb_profile_dns_list_withcommon',
            'adc_get_dns_profile': 'adc_slb_profile_dns_get',
            'adc_add_dns_profile': 'adc_slb_profile_dns_add',
            'adc_edit_dns_profile': 'adc_slb_profile_dns_edit',
            'adc_delete_dns_profile': 'adc_slb_profile_dns_del',
        },
        'actions': {
            'list_profiles': 'slb_profile_dns_list',
            'list_profiles_withcommon': 'slb_profile_dns_list_withcommon',
            'get_profile': 'slb_profile_dns_get',
            'add_profile': 'slb_profile_dns_add',
            'edit_profile': 'slb_profile_dns_edit',
            'delete_profile': 'slb_profile_dns_del',
        }
    },
    'adc_slb_policy.py': {
        'functions': {
            'adc_list_policies': 'adc_slb_policy_list',
            'adc_list_policies_withcommon': 'adc_slb_policy_list_withcommon',
            'adc_get_policy': 'adc_slb_policy_get',
            'adc_add_policy': 'adc_slb_policy_add',
            'adc_edit_policy': 'adc_slb_policy_edit',
            'adc_delete_policy': 'adc_slb_policy_del',
        },
        'actions': {
            'list_policies': 'slb_policy_list',
            'list_policies_withcommon': 'slb_policy_list_withcommon',
            'get_policy': 'slb_policy_get',
            'add_policy': 'slb_policy_add',
            'edit_policy': 'slb_policy_edit',
            'delete_policy': 'slb_policy_del',
        }
    },
}


def process_file(filepath, mappings):
    """处理单个文件，替换 action 和函数名"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 替换函数定义
    for old_func, new_func in mappings.get('functions', {}).items():
        # 替换函数定义行
        content = re.sub(
            r'\bdef\s+' + re.escape(old_func) + r'\s*\(',
            'def ' + new_func + '(',
            content
        )
        # 替换函数调用
        content = re.sub(
            r'\b' + re.escape(old_func) + r'\s*\(',
            new_func + '(',
            content
        )

    # 替换 choices 中的 action 字符串
    for old_action, new_action in mappings.get('actions', {}).items():
        # 在 choices 列表中替换
        content = re.sub(
            r"'{}'".format(re.escape(old_action)),
            "'{}'".format(new_action),
            content
        )
        content = re.sub(
            r'"{}"'.format(re.escape(old_action)),
            '"{}"'.format(new_action),
            content
        )

    # 替换 if-elif 中的 action 比较
    for old_action, new_action in mappings.get('actions', {}).items():
        # 替换 action == 'xxx'
        content = re.sub(
            r"action\s*==\s*'{}'".format(re.escape(old_action)),
            "action == '{}'".format(new_action),
            content
        )
        content = re.sub(
            r'action\s*==\s*"{}"'.format(re.escape(old_action)),
            'action == "{}"'.format(new_action),
            content
        )

    # 只在内容有变化时写入文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    """主函数"""
    library_dir = r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library'

    modified_count = 0
    for filename, mappings in CORE_MODULES.items():
        filepath = os.path.join(library_dir, filename)

        if os.path.exists(filepath):
            if process_file(filepath, mappings):
                print(f"✓ 修改文件: {filename}")
                modified_count += 1
            else:
                print(f"○ 无需修改: {filename}")
        else:
            print(f"✗ 文件不存在: {filename}")

    print(f"\n修改完成！共修改 {modified_count} 个文件。")


if __name__ == '__main__':
    main()
