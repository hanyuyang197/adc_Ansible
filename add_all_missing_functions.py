# -*- coding: utf-8 -*-
import os
import re
import pandas as pd
import json

# 读取缺失函数的列表
with open('missing_functions.json', 'r', encoding='utf-8') as f:
    missing_list = json.load(f)

# 读取API文档获取参数信息
api_docs = {}
for doc_file in ['adc_api_doc.md', 'adc_api_network_doc.md', 'adc_api_system_doc.md']:
    if os.path.exists(doc_file):
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 简单提取API信息
            matches = re.findall(r'###\s+([a-z]+\.[a-z._]+)(.*?)(?=###|$)', content, re.DOTALL)
            for api, desc in matches:
                api_docs[api] = desc

# 按模块分组
module_functions = {}
for item in missing_list:
    module = item['module']
    if module not in module_functions:
        module_functions[module] = []
    module_functions[module].append(item)

print(f"找到 {len(module_functions)} 个模块需要添加函数")

# 为每个模块添加缺失的函数
library_dir = 'library'

for module_name, functions in module_functions.items():
    # 检查模块是否存在
    if ' 或 ' in module_name:
        # 尝试找到存在的模块
        modules = module_name.split(' 或 ')
        actual_module = None
        for m in modules:
            if os.path.exists(os.path.join(library_dir, m)):
                actual_module = m
                break
        if not actual_module:
            print(f"警告: {module_name} 都不存在,跳过")
            continue
        module_name = actual_module
    
    module_path = os.path.join(library_dir, module_name)
    if not os.path.exists(module_path):
        print(f"警告: {module_name} 不存在,跳过")
        continue
    
    print(f"\n处理模块: {module_name}")
    
    # 读取模块文件
    with open(module_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到main函数中的action列表
    main_match = re.search(r'action=dict\(type=\'str\', required=True, choices=\[(.*?)\]\)', content, re.DOTALL)
    if not main_match:
        print(f"  无法找到action choices,跳过")
        continue
    
    current_choices_str = main_match.group(1)
    current_choices = [c.strip().strip("'\"") for c in current_choices_str.split(',') if c.strip()]
    
    # 找到if-elif action判断部分
    action_dispatch_match = re.search(r'action = module\.params\[\'action\'\].*?^(if __name__ == \'__main__\':)', content, re.DOTALL | re.MULTILINE)
    if not action_dispatch_match:
        print(f"  无法找到action dispatch部分,跳过")
        continue
    
    dispatch_section = action_dispatch_match.group(0)
    
    # 为每个缺失的函数添加实现
    new_functions_code = ""
    new_actions = []
    new_dispatch_code = ""
    
    for item in functions:
        api = item['api']
        action_name = item['missing_function']  # 如 port_add, script_list
        
        # 跳过已存在的action
        if action_name in current_choices:
            continue
        
        print(f"  添加函数: {action_name} (API: {api})")
        
        # 解析API: slb.node.port.add
        parts = api.split('.')
        api_action = parts[-1]  # add/edit/del/list/get
        
        # 生成函数代码
        new_functions_code += generate_function_code(action_name, api, api_action) + "\n\n"
        new_actions.append(f"'{action_name}'")
        new_dispatch_code += f"    elif action == '{action_name}':\n        {action_name}(module)\n"
    
    if not new_functions_code:
        print(f"  没有需要添加的新函数")
        continue
    
    # 在main函数之前插入新函数
    main_pos = content.find('def main():')
    if main_pos == -1:
        print(f"  找不到main函数")
        continue
    
    # 插入新函数
    new_content = content[:main_pos] + new_functions_code + "\n" + content[main_pos:]
    
    # 更新action choices
    updated_choices_str = current_choices_str + ",\n                    " + ",\n                    ".join(new_actions)
    new_content = new_content.replace(current_choices_str, updated_choices_str)
    
    # 更新dispatch部分
    dispatch_end_match = re.search(r'(\n    elif action == \'[^\']+\':\n        \w+\(module\)\s*)(\n\nif __name__ == )', new_content, re.DOTALL)
    if dispatch_end_match:
        insert_pos = dispatch_end_match.end(1)
        new_content = new_content[:insert_pos] + "\n" + new_dispatch_code + new_content[insert_pos:]
    
    # 写回文件
    with open(module_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  已添加 {len(new_actions)} 个新函数")


def generate_function_code(action_name, api, api_action):
    """生成函数代码模板"""
    parts = api.split('.')
    
    if api_action in ['list', 'get']:
        # GET请求 - 查询类
        return f'''def {action_name}(module):
    """{api}"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action={api}" % (ip, authkey)

    response_data = ""
    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="请求失败: %s" % str(e))

    if response_data:
        try:
            parsed_data = json.loads(response_data)
            if 'errmsg' in parsed_data and parsed_data['errmsg']:
                module.fail_json(msg="操作失败", response=parsed_data)
            else:
                module.exit_json(changed=False, data=parsed_data)
        except Exception as e:
            module.fail_json(msg="解析响应失败: %s" % str(e))
    else:
        module.fail_json(msg="未收到有效响应")'''
    
    elif api_action in ['add', 'edit', 'del']:
        # POST请求 - 操作类
        return f'''def {action_name}(module):
    """{api}"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action={api}" % (ip, authkey)

    # 构造请求参数 - 根据API类型调整
    params = {{}}
    # TODO: 添加必要的参数
    
    post_data = json.dumps(params)
    response_data = ""

    try:
        if sys.version_info[0] >= 3:
            import urllib.request as urllib_request
            post_data = post_data.encode('utf-8')
            req = urllib_request.Request(url, data=post_data, headers={{
                                         'Content-Type': 'application/json'}})
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            import urllib2 as urllib_request
            req = urllib_request.Request(url, data=post_data, headers={{
                                         'Content-Type': 'application/json'}})
            response = urllib_request.urlopen(req)
            response_data = response.read()
    except Exception as e:
        module.fail_json(msg="操作失败: %s" % str(e))

    if response_data:
        success, result_dict = format_adc_response_for_ansible(
            response_data, "操作", True)
        if success:
            module.exit_json(**result_dict)
        else:
            module.fail_json(**result_dict)
    else:
        module.fail_json(msg="未收到有效响应")'''
    
    else:
        # 默认模板
        return f'''def {action_name}(module):
    """{api}"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    url = "http://%s/adcapi/v2.0/?authkey=%s&action={api}" % (ip, authkey)

    # TODO: 实现具体的请求逻辑
    module.fail_json(msg="函数 {action_name} 尚未实现")'''


print("\n完成!")
