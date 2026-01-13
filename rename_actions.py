#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量重命名 ADC Ansible 模块中的 action 和函数名
按照问题2规则：完整 URL 格式，所有 . 替换为 _
"""

import os
import re

# 定义需要修改的文件和对应的映射关系
MODULE_MAPPINGS = {
    'adc_slb_pool.py': {
        'adc_get_pools': 'adc_slb_pool_list',
        'get_pools': 'slb_pool_list',
        'get_pools_withcommon': 'slb_pool_list_withcommon',
        'get_pool': 'slb_pool_get',
        'add_pool': 'slb_pool_add',
        'edit_pool': 'slb_pool_edit',
        'delete_pool': 'slb_pool_del',
        'add_pool_node': 'slb_pool_member_add',
        'delete_pool_node': 'slb_pool_member_del',
        'edit_pool_member': 'slb_pool_member_edit',
        'onoff_pool_member': 'slb_pool_member_onoff',
    },
    'adc_slb_node.py': {
        'list_nodes': 'slb_node_list',
        'get_node': 'slb_node_get',
        'add_node': 'slb_node_add',
        'edit_node': 'slb_node_edit',
        'delete_node': 'slb_node_del',
        'add_node_port': 'slb_node_port_add',
        'edit_node_port': 'slb_node_port_edit',
        'delete_node_port': 'slb_node_port_del',
        'node_onoff': 'slb_node_onoff',
        'node_port_onoff': 'slb_node_port_onoff',
    },
    'adc_slb_va.py': {
        'list_vas': 'slb_va_list',
        'get_va': 'slb_va_get',
        'add_va': 'slb_va_add',
        'edit_va': 'slb_va_edit',
        'delete_va': 'slb_va_del',
    },
    'adc_slb_stat.py': {
        'node_stat_list': 'slb_node_stat_list',
        'node_stat_get': 'slb_node_stat_get',
        'node_stat_clear': 'slb_node_stat_clear',
        'pool_stat_list': 'slb_pool_stat_list',
        'pool_stat_get': 'slb_pool_stat_get',
        'pool_stat_clear': 'slb_pool_stat_clear',
        'session_clear': 'slb_session_clear',
    },
    'adc_slb_va_vs.py': {
        'add_vs': 'slb_va_vs_add',
        'edit_vs': 'slb_va_vs_edit',
        'delete_vs': 'slb_va_vs_del',
        'get_vs': 'slb_va_vs_get',
    },
    'adc_slb_va_vs_stat.py': {
        'get_vs_stat': 'slb_va_vs_stat_get',
        'list_vs_stat_count': 'slb_va_vs_stat_count_list',
    },
    'adc_slb_ssl_certificate.py': {
        'upload': 'slb_ssl_certificate_upload',
        'add': 'slb_ssl_certificate_add',
        'list': 'slb_ssl_certificate_list',
        'list_withcommon': 'slb_ssl_certificate_list_withcommon',
        'del': 'slb_ssl_certificate_del',
        'key_upload': 'slb_ssl_key_upload',
        'crl_upload': 'slb_ssl_crl_upload',
        'pfx_upload': 'slb_ssl_pfx_upload',
    },
    'adc_slb_sslclient.py': {
        'list_profiles': 'slb_sslclient_list',
        'list_profiles_withcommon': 'slb_sslclient_list_withcommon',
        'get_profile': 'slb_sslclient_get',
        'add_profile': 'slb_sslclient_add',
        'edit_profile': 'slb_sslclient_edit',
        'delete_profile': 'slb_sslclient_del',
    },
    'adc_slb_sslserver.py': {
        'list_profiles': 'slb_sslserver_list',
        'list_profiles_withcommon': 'slb_sslserver_list_withcommon',
        'get_profile': 'slb_sslserver_get',
        'add_profile': 'slb_sslserver_add',
        'edit_profile': 'slb_sslserver_edit',
        'delete_profile': 'slb_sslserver_del',
    },
    'adc_slb_profile_dns.py': {
        'list_profiles': 'slb_profile_dns_list',
        'list_profiles_withcommon': 'slb_profile_dns_list_withcommon',
        'get_profile': 'slb_profile_dns_get',
        'add_profile': 'slb_profile_dns_add',
        'edit_profile': 'slb_profile_dns_edit',
        'delete_profile': 'slb_profile_dns_del',
    },
    'adc_slb_ruletable_string.py': {
        'add_string': 'slb_ruletable_string_add',
        'delete_string': 'slb_ruletable_string_del',
    },
    'adc_slb_policy.py': {
        'list_policies': 'slb_policy_list',
        'list_policies_withcommon': 'slb_policy_list_withcommon',
        'get_policy': 'slb_policy_get',
        'add_policy': 'slb_policy_add',
        'edit_policy': 'slb_policy_edit',
        'delete_policy': 'slb_policy_del',
    },
    'adc_slb_healthcheck.py': {
        'list_healthchecks': 'slb_healthcheck_list',
        'get_healthcheck': 'slb_healthcheck_get',
        'add_healthcheck': 'slb_healthcheck_add',
        'edit_healthcheck': 'slb_healthcheck_edit',
        'delete_healthcheck': 'slb_healthcheck_del',
    },
}

# 函数名前缀映射（用于函数重命名）
FUNCTION_PREFIX_MAPPINGS = {
    'adc_slb_pool.py': {
        'adc_get_pools': 'adc_slb_pool_list',
        'adc_get_pool': 'adc_slb_pool_get',
        'adc_add_pool': 'adc_slb_pool_add',
        'adc_edit_pool': 'adc_slb_pool_edit',
        'adc_delete_pool': 'adc_slb_pool_del',
        'adc_add_pool_node': 'adc_slb_pool_member_add',
        'adc_delete_pool_node': 'adc_slb_pool_member_del',
        'edit_pool_member': 'adc_slb_pool_member_edit',
        'onoff_pool_member': 'adc_slb_pool_member_onoff',
        'get_pools_withcommon': 'adc_slb_pool_list_withcommon',
    },
    'adc_slb_node.py': {
        'adc_list_nodes': 'adc_slb_node_list',
        'adc_get_node': 'adc_slb_node_get',
        'adc_add_node': 'adc_slb_node_add',
        'adc_edit_node': 'adc_slb_node_edit',
        'adc_delete_node': 'adc_slb_node_del',
        'adc_add_node_port': 'adc_slb_node_port_add',
        'adc_edit_node_port': 'adc_slb_node_port_edit',
        'adc_delete_node_port': 'adc_slb_node_port_del',
        'adc_node_onoff': 'adc_slb_node_onoff',
        'adc_node_port_onoff': 'adc_slb_node_port_onoff',
    },
    'adc_slb_va.py': {
        'adc_list_vas': 'adc_slb_va_list',
        'adc_get_va': 'adc_slb_va_get',
        'adc_add_va': 'adc_slb_va_add',
        'adc_edit_va': 'adc_slb_va_edit',
        'adc_delete_va': 'adc_slb_va_del',
        'adc_va_stat_list': 'adc_slb_va_stat_list',
        'adc_va_stat_get': 'adc_slb_va_stat_get',
    },
    'adc_slb_stat.py': {
        'adc_node_stat_list': 'adc_slb_node_stat_list',
        'adc_node_stat_get': 'adc_slb_node_stat_get',
        'adc_node_stat_clear': 'adc_slb_node_stat_clear',
        'adc_pool_stat_list': 'adc_slb_pool_stat_list',
        'adc_pool_stat_get': 'adc_slb_pool_stat_get',
        'adc_pool_stat_clear': 'adc_slb_pool_stat_clear',
        'adc_session_clear': 'adc_slb_session_clear',
    },
    'adc_slb_va_vs.py': {
        'adc_add_vs': 'adc_slb_va_vs_add',
        'adc_edit_vs': 'adc_slb_va_vs_edit',
        'adc_delete_vs': 'adc_slb_va_vs_del',
        'adc_get_vs': 'adc_slb_va_vs_get',
    },
    'adc_slb_va_vs_stat.py': {
        'adc_get_vs_stat': 'adc_slb_va_vs_stat_get',
        'adc_list_vs_stat_count': 'adc_slb_va_vs_stat_count_list',
    },
    'adc_slb_ssl_certificate.py': {
        'adc_slb_ssl_certificate_upload': 'adc_slb_ssl_certificate_upload',
        'adc_slb_ssl_certificate_add': 'adc_slb_ssl_certificate_add',
        'adc_slb_ssl_certificate_list': 'adc_slb_ssl_certificate_list',
        'adc_slb_ssl_certificate_list_withcommon': 'adc_slb_ssl_certificate_list_withcommon',
        'adc_slb_ssl_certificate_del': 'adc_slb_ssl_certificate_del',
        'adc_slb_ssl_key_upload': 'adc_slb_ssl_key_upload',
        'adc_slb_ssl_crl_upload': 'adc_slb_ssl_crl_upload',
        'adc_slb_ssl_pfx_upload': 'adc_slb_ssl_pfx_upload',
    },
    'adc_slb_sslclient.py': {
        'adc_list_sslclient_profiles': 'adc_slb_sslclient_list',
        'adc_list_sslclient_profiles_withcommon': 'adc_slb_sslclient_list_withcommon',
        'adc_get_sslclient_profile': 'adc_slb_sslclient_get',
        'adc_add_sslclient_profile': 'adc_slb_sslclient_add',
        'adc_edit_sslclient_profile': 'adc_slb_sslclient_edit',
        'adc_delete_sslclient_profile': 'adc_slb_sslclient_del',
    },
    'adc_slb_sslserver.py': {
        'adc_list_sslserver_profiles': 'adc_slb_sslserver_list',
        'adc_list_sslserver_profiles_withcommon': 'adc_slb_sslserver_list_withcommon',
        'adc_get_sslserver_profile': 'adc_slb_sslserver_get',
        'adc_add_sslserver_profile': 'adc_slb_sslserver_add',
        'adc_edit_sslserver_profile': 'adc_slb_sslserver_edit',
        'adc_delete_sslserver_profile': 'adc_slb_sslserver_del',
    },
    'adc_slb_profile_dns.py': {
        'adc_list_dns_profiles': 'adc_slb_profile_dns_list',
        'adc_list_dns_profiles_withcommon': 'adc_slb_profile_dns_list_withcommon',
        'adc_get_dns_profile': 'adc_slb_profile_dns_get',
        'adc_add_dns_profile': 'adc_slb_profile_dns_add',
        'adc_edit_dns_profile': 'adc_slb_profile_dns_edit',
        'adc_delete_dns_profile': 'adc_slb_profile_dns_del',
    },
    'adc_slb_ruletable_string.py': {
        'adc_add_string_entries': 'adc_slb_ruletable_string_add',
        'adc_delete_string_entries': 'adc_slb_ruletable_string_del',
    },
    'adc_slb_policy.py': {
        'adc_list_policies': 'adc_slb_policy_list',
        'adc_list_policies_withcommon': 'adc_slb_policy_list_withcommon',
        'adc_get_policy': 'adc_slb_policy_get',
        'adc_add_policy': 'adc_slb_policy_add',
        'adc_edit_policy': 'adc_slb_policy_edit',
        'adc_delete_policy': 'adc_slb_policy_del',
    },
    'adc_slb_healthcheck.py': {
        'adc_list_healthchecks': 'adc_slb_healthcheck_list',
        'adc_get_healthcheck': 'adc_slb_healthcheck_get',
        'adc_add_healthcheck': 'adc_slb_healthcheck_add',
        'adc_edit_healthcheck': 'adc_slb_healthcheck_edit',
        'adc_delete_healthcheck': 'adc_slb_healthcheck_del',
    },
}


def process_file(filepath, action_mappings, function_mappings):
    """处理单个文件，替换 action 和函数名"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 替换函数定义
    for old_func, new_func in function_mappings.items():
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
    for old_action, new_action in action_mappings.items():
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
    for old_action, new_action in action_mappings.items():
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
    for filename, action_mappings in MODULE_MAPPINGS.items():
        filepath = os.path.join(library_dir, filename)
        function_mappings = FUNCTION_PREFIX_MAPPINGS.get(filename, {})

        if os.path.exists(filepath):
            if process_file(filepath, action_mappings, function_mappings):
                print(f"✓ 修改文件: {filename}")
                modified_count += 1
            else:
                print(f"○ 无需修改: {filename}")
        else:
            print(f"✗ 文件不存在: {filename}")

    print(f"\n修改完成！共修改 {modified_count} 个文件。")


if __name__ == '__main__':
    main()
