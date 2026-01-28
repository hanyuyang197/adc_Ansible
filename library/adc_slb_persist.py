#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.horizon.modules.plugins.module_utils.adc_common import (
    make_adc_request,
    format_adc_response,
    check_adc_auth,
    handle_adc_error,
    build_adc_params,
    validate_adc_params,
    adc_result_check,
    adc_format_output,
    build_params_with_optional,
    make_http_request,
    get_param_if_exists,
    create_adc_module_args,
    adc_response_to_ansible_result,
    format_adc_response_for_ansible,
    send_request
)
import json
import sys


def slb_persist_cookie_list(module):
    """cookie连接保持列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.cookie.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取cookie连接保持列表", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取cookie连接保持列表失败: %s" % str(e))


def slb_persist_cookie_get(module):
    """cookie连接保持获取"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="cookie连接保持获取需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.cookie.get" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取cookie连接保持详情", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取cookie连接保持详情失败: %s" % str(e))


def slb_persist_cookie_add(module):
    """cookie连接保持增加"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="cookie连接保持增加需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.cookie.add" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    # 添加可选参数
    if module.params.get('expire_enable') is not None:
        persist_data['expire_enable'] = module.params['expire_enable']
    if module.params.get('expire') is not None:
        persist_data['expire'] = module.params['expire']
    if module.params.get('method') is not None:
        persist_data['method'] = module.params['method']
    if module.params.get('encrypt') is not None:
        persist_data['encrypt'] = module.params['encrypt']
    if module.params.get('encrypt_password') is not None:
        persist_data['encrypt_password'] = module.params['encrypt_password']
    if module.params.get('http_only') is not None:
        persist_data['http_only'] = module.params['http_only']
    if module.params.get('secure') is not None:
        persist_data['secure'] = module.params['secure']
    if module.params.get('cookie_name') is not None:
        persist_data['cookie_name'] = module.params['cookie_name']
    if module.params.get('domain') is not None:
        persist_data['domain'] = module.params['domain']
    if module.params.get('path') is not None:
        persist_data['path'] = module.params['path']
    if module.params.get('type') is not None:
        persist_data['type'] = module.params['type']
    if module.params.get('insert') is not None:
        persist_data['insert'] = module.params['insert']
    if module.params.get('ignore_connlimit') is not None:
        persist_data['ignore_connlimit'] = module.params['ignore_connlimit']
    if module.params.get('description') is not None:
        persist_data['description'] = module.params['description']

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "cookie连接保持增加", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="cookie连接保持增加失败: %s" % str(e))


def slb_persist_cookie_edit(module):
    """cookie连接保持编辑"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="cookie连接保持编辑需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.cookie.edit" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    # 添加可选参数
    if module.params.get('expire_enable') is not None:
        persist_data['expire_enable'] = module.params['expire_enable']
    if module.params.get('expire') is not None:
        persist_data['expire'] = module.params['expire']
    if module.params.get('method') is not None:
        persist_data['method'] = module.params['method']
    if module.params.get('encrypt') is not None:
        persist_data['encrypt'] = module.params['encrypt']
    if module.params.get('encrypt_password') is not None:
        persist_data['encrypt_password'] = module.params['encrypt_password']
    if module.params.get('http_only') is not None:
        persist_data['http_only'] = module.params['http_only']
    if module.params.get('secure') is not None:
        persist_data['secure'] = module.params['secure']
    if module.params.get('cookie_name') is not None:
        persist_data['cookie_name'] = module.params['cookie_name']
    if module.params.get('domain') is not None:
        persist_data['domain'] = module.params['domain']
    if module.params.get('path') is not None:
        persist_data['path'] = module.params['path']
    if module.params.get('type') is not None:
        persist_data['type'] = module.params['type']
    if module.params.get('insert') is not None:
        persist_data['insert'] = module.params['insert']
    if module.params.get('ignore_connlimit') is not None:
        persist_data['ignore_connlimit'] = module.params['ignore_connlimit']
    if module.params.get('description') is not None:
        persist_data['description'] = module.params['description']

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "cookie连接保持编辑", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="cookie连接保持编辑失败: %s" % str(e))


def slb_persist_cookie_del(module):
    """cookie连接保持删除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="cookie连接保持删除需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.cookie.del" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "cookie连接保持删除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="cookie连接保持删除失败: %s" % str(e))


def slb_persist_cookie_list_withcommon(module):
    """获取 common 和本分区 cookie 连接保持列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.cookie.list.withcommon" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取common和本分区cookie连接保持列表", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取common和本分区cookie连接保持列表失败: %s" % str(e))


def slb_persist_srcip_list(module):
    """源地址连接保持列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.srcip.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取源地址连接保持列表", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取源地址连接保持列表失败: %s" % str(e))


def slb_persist_srcip_get(module):
    """源地址连接保持获取"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="源地址连接保持获取需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.srcip.get" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取源地址连接保持详情", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取源地址连接保持详情失败: %s" % str(e))


def slb_persist_srcip_add(module):
    """源地址连接保持增加"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="源地址连接保持增加需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.srcip.add" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    # 添加可选参数
    if module.params.get('type') is not None:
        persist_data['type'] = module.params['type']
    if module.params.get('timeout') is not None:
        persist_data['timeout'] = module.params['timeout']
    if module.params.get('ignore_connlimit') is not None:
        persist_data['ignore_connlimit'] = module.params['ignore_connlimit']
    if module.params.get('with_port') is not None:
        persist_data['with_port'] = module.params['with_port']
    if module.params.get('netmask') is not None:
        persist_data['netmask'] = module.params['netmask']
    if module.params.get('ipv6masklen') is not None:
        persist_data['ipv6masklen'] = module.params['ipv6masklen']
    if module.params.get('conn_mirror') is not None:
        persist_data['conn_mirror'] = module.params['conn_mirror']
    if module.params.get('description') is not None:
        persist_data['description'] = module.params['description']

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "源地址连接保持增加", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="源地址连接保持增加失败: %s" % str(e))


def slb_persist_srcip_edit(module):
    """源地址连接保持编辑"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="源地址连接保持编辑需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.srcip.edit" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    # 添加可选参数
    if module.params.get('type') is not None:
        persist_data['type'] = module.params['type']
    if module.params.get('timeout') is not None:
        persist_data['timeout'] = module.params['timeout']
    if module.params.get('ignore_connlimit') is not None:
        persist_data['ignore_connlimit'] = module.params['ignore_connlimit']
    if module.params.get('with_port') is not None:
        persist_data['with_port'] = module.params['with_port']
    if module.params.get('netmask') is not None:
        persist_data['netmask'] = module.params['netmask']
    if module.params.get('ipv6masklen') is not None:
        persist_data['ipv6masklen'] = module.params['ipv6masklen']
    if module.params.get('conn_mirror') is not None:
        persist_data['conn_mirror'] = module.params['conn_mirror']
    if module.params.get('description') is not None:
        persist_data['description'] = module.params['description']

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "源地址连接保持编辑", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="源地址连接保持编辑失败: %s" % str(e))


def slb_persist_srcip_del(module):
    """源地址连接保持删除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="源地址连接保持删除需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.srcip.del" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "源地址连接保持删除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="源地址连接保持删除失败: %s" % str(e))


def slb_persist_srcip_list_withcommon(module):
    """获取 common 和本分区源地址连接保持列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.srcip.list.withcommon" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取common和本分区源地址连接保持列表", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取common和本分区源地址连接保持列表失败: %s" % str(e))


def slb_persist_dstip_list(module):
    """目的地址连接保持列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.dstip.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取目的地址连接保持列表", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取目的地址连接保持列表失败: %s" % str(e))


def slb_persist_dstip_get(module):
    """目的地址连接保持获取"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="目的地址连接保持获取需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.dstip.get" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取目的地址连接保持详情", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取目的地址连接保持详情失败: %s" % str(e))


def slb_persist_dstip_add(module):
    """目的地址连接保持增加"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="目的地址连接保持增加需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.dstip.add" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    # 添加可选参数
    if module.params.get('type') is not None:
        persist_data['type'] = module.params['type']
    if module.params.get('timeout') is not None:
        persist_data['timeout'] = module.params['timeout']
    if module.params.get('ignore_connlimit') is not None:
        persist_data['ignore_connlimit'] = module.params['ignore_connlimit']
    if module.params.get('netmask') is not None:
        persist_data['netmask'] = module.params['netmask']
    if module.params.get('ipv6masklen') is not None:
        persist_data['ipv6masklen'] = module.params['ipv6masklen']
    if module.params.get('conn_mirror') is not None:
        persist_data['conn_mirror'] = module.params['conn_mirror']
    if module.params.get('description') is not None:
        persist_data['description'] = module.params['description']

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "目的地址连接保持增加", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="目的地址连接保持增加失败: %s" % str(e))


def slb_persist_dstip_edit(module):
    """目的地址连接保持编辑"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="目的地址连接保持编辑需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.dstip.edit" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    # 添加可选参数
    if module.params.get('type') is not None:
        persist_data['type'] = module.params['type']
    if module.params.get('timeout') is not None:
        persist_data['timeout'] = module.params['timeout']
    if module.params.get('ignore_connlimit') is not None:
        persist_data['ignore_connlimit'] = module.params['ignore_connlimit']
    if module.params.get('netmask') is not None:
        persist_data['netmask'] = module.params['netmask']
    if module.params.get('ipv6masklen') is not None:
        persist_data['ipv6masklen'] = module.params['ipv6masklen']
    if module.params.get('conn_mirror') is not None:
        persist_data['conn_mirror'] = module.params['conn_mirror']
    if module.params.get('description') is not None:
        persist_data['description'] = module.params['description']

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "目的地址连接保持编辑", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="目的地址连接保持编辑失败: %s" % str(e))


def slb_persist_dstip_del(module):
    """目的地址连接保持删除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="目的地址连接保持删除需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.dstip.del" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "目的地址连接保持删除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="目的地址连接保持删除失败: %s" % str(e))


def slb_persist_dstip_list_withcommon(module):
    """获取 common 和本分区目的地址连接保持列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.dstip.list.withcommon" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取common和本分区目的地址连接保持列表", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取common和本分区目的地址连接保持列表失败: %s" % str(e))


def slb_persist_sslid_list(module):
    """ssl地址连接保持列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.sslid.list" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取ssl地址连接保持列表", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取ssl地址连接保持列表失败: %s" % str(e))


def slb_persist_sslid_get(module):
    """ssl地址连接保持获取"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="ssl地址连接保持获取需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.sslid.get" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取ssl地址连接保持详情", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取ssl地址连接保持详情失败: %s" % str(e))


def slb_persist_sslid_add(module):
    """ssl地址连接保持增加"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="ssl地址连接保持增加需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.sslid.add" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    # 添加可选参数
    if module.params.get('timeout') is not None:
        persist_data['timeout'] = module.params['timeout']
    if module.params.get('ignore_connlimit') is not None:
        persist_data['ignore_connlimit'] = module.params['ignore_connlimit']
    if module.params.get('conn_mirror') is not None:
        persist_data['conn_mirror'] = module.params['conn_mirror']
    if module.params.get('description') is not None:
        persist_data['description'] = module.params['description']

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "ssl地址连接保持增加", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="ssl地址连接保持增加失败: %s" % str(e))


def slb_persist_sslid_edit(module):
    """ssl地址连接保持编辑"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="ssl地址连接保持编辑需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.sslid.edit" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    # 添加可选参数
    if module.params.get('timeout') is not None:
        persist_data['timeout'] = module.params['timeout']
    if module.params.get('ignore_connlimit') is not None:
        persist_data['ignore_connlimit'] = module.params['ignore_connlimit']
    if module.params.get('conn_mirror') is not None:
        persist_data['conn_mirror'] = module.params['conn_mirror']
    if module.params.get('description') is not None:
        persist_data['description'] = module.params['description']

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "ssl地址连接保持编辑", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="ssl地址连接保持编辑失败: %s" % str(e))


def slb_persist_sslid_del(module):
    """ssl地址连接保持删除"""
    ip = module.params['ip']
    authkey = module.params['authkey']
    name = module.params['name']

    if not name:
        module.fail_json(msg="ssl地址连接保持删除需要提供name参数")

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.sslid.del" % (
        ip, authkey)

    persist_data = {
        "name": name
    }

    post_data = json.dumps(persist_data)

    try:
        response_data = send_request(url, post_data)
        success, result_dict = format_adc_response_for_ansible(
            response_data, "ssl地址连接保持删除", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="ssl地址连接保持删除失败: %s" % str(e))


def slb_persist_sslid_list_withcommon(module):
    """获取 common 和本分区 ssl 地址连接保持列表"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action=slb.persist.sslid.list.withcommon" % (
        ip, authkey)

    try:
        response_data = send_request(url)
        # 使用通用响应解析函数
        success, result_dict = format_adc_response_for_ansible(
            response_data, "获取common和本分区ssl地址连接保持列表", False, check_status=False)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    except Exception as e:
        module.fail_json(msg="获取common和本分区ssl地址连接保持列表失败: %s" % str(e))


def main():
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True, choices=[
            'slb_persist_cookie_list', 'slb_persist_cookie_get', 'slb_persist_cookie_add',
            'slb_persist_cookie_edit', 'slb_persist_cookie_del', 'slb_persist_cookie_list_withcommon',
            'slb_persist_srcip_list', 'slb_persist_srcip_get', 'slb_persist_srcip_add',
            'slb_persist_srcip_edit', 'slb_persist_srcip_del', 'slb_persist_srcip_list_withcommon',
            'slb_persist_dstip_list', 'slb_persist_dstip_get', 'slb_persist_dstip_add',
            'slb_persist_dstip_edit', 'slb_persist_dstip_del', 'slb_persist_dstip_list_withcommon',
            'slb_persist_sslid_list', 'slb_persist_sslid_get', 'slb_persist_sslid_add',
            'slb_persist_sslid_edit', 'slb_persist_sslid_del', 'slb_persist_sslid_list_withcommon'
        ]),
        # 连接保持通用参数
        name=dict(type='str', required=False),
        description=dict(type='str', required=False),
        timeout=dict(type='int', required=False),
        ignore_connlimit=dict(type='int', required=False, choices=[0, 1]),
        conn_mirror=dict(type='int', required=False, choices=[0, 1]),
        # Cookie 连接保持特有参数
        expire_enable=dict(type='int', required=False, choices=[0, 1]),
        expire=dict(type='int', required=False),
        method=dict(type='int', required=False, choices=[0, 1, 2]),
        encrypt=dict(type='int', required=False, choices=[0, 1, 2]),
        encrypt_password=dict(type='str', required=False),
        http_only=dict(type='int', required=False, choices=[0, 1]),
        secure=dict(type='int', required=False, choices=[0, 1]),
        cookie_name=dict(type='str', required=False),
        domain=dict(type='str', required=False),
        path=dict(type='str', required=False),
        insert=dict(type='int', required=False, choices=[0, 1]),
        type=dict(type='int', required=False, choices=[0, 1, 2, 3]),
        # 源/目的 IP 连接保持特有参数
        with_port=dict(type='int', required=False, choices=[0, 1]),
        netmask=dict(type='str', required=False),
        ipv6masklen=dict(type='int', required=False)
    )

    # 创建AnsibleModule实例
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 根据action执行相应操作
    action = module.params['action']

    if action == 'slb_persist_cookie_list':
        slb_persist_cookie_list(module)
    elif action == 'slb_persist_cookie_get':
        slb_persist_cookie_get(module)
    elif action == 'slb_persist_cookie_add':
        slb_persist_cookie_add(module)
    elif action == 'slb_persist_cookie_edit':
        slb_persist_cookie_edit(module)
    elif action == 'slb_persist_cookie_del':
        slb_persist_cookie_del(module)
    elif action == 'slb_persist_cookie_list_withcommon':
        slb_persist_cookie_list_withcommon(module)
    elif action == 'slb_persist_srcip_list':
        slb_persist_srcip_list(module)
    elif action == 'slb_persist_srcip_get':
        slb_persist_srcip_get(module)
    elif action == 'slb_persist_srcip_add':
        slb_persist_srcip_add(module)
    elif action == 'slb_persist_srcip_edit':
        slb_persist_srcip_edit(module)
    elif action == 'slb_persist_srcip_del':
        slb_persist_srcip_del(module)
    elif action == 'slb_persist_srcip_list_withcommon':
        slb_persist_srcip_list_withcommon(module)
    elif action == 'slb_persist_dstip_list':
        slb_persist_dstip_list(module)
    elif action == 'slb_persist_dstip_get':
        slb_persist_dstip_get(module)
    elif action == 'slb_persist_dstip_add':
        slb_persist_dstip_add(module)
    elif action == 'slb_persist_dstip_edit':
        slb_persist_dstip_edit(module)
    elif action == 'slb_persist_dstip_del':
        slb_persist_dstip_del(module)
    elif action == 'slb_persist_dstip_list_withcommon':
        slb_persist_dstip_list_withcommon(module)
    elif action == 'slb_persist_sslid_list':
        slb_persist_sslid_list(module)
    elif action == 'slb_persist_sslid_get':
        slb_persist_sslid_get(module)
    elif action == 'slb_persist_sslid_add':
        slb_persist_sslid_add(module)
    elif action == 'slb_persist_sslid_edit':
        slb_persist_sslid_edit(module)
    elif action == 'slb_persist_sslid_del':
        slb_persist_sslid_del(module)
    elif action == 'slb_persist_sslid_list_withcommon':
        slb_persist_sslid_list_withcommon(module)


if __name__ == '__main__':
    main()
