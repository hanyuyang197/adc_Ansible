#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import pandas as pd

print("=== 开始创建缺失的模块和YAML文件 ===")

# 读取Excel文件
df = pd.read_excel('ansible_yml_path.xlsx')

# 构建模块模板
def create_module_template(module_name, functions):
    """创建模块模板"""
    template = '''#!/usr/bin/python
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
    format_adc_response_for_ansible
)
import json
import sys

# ADC API响应解析函数
'''
    
    # 添加函数定义
    for func in functions:
        api_name = func.replace('adc_', '').replace('_', '.')
        template += f'''

def {func}(module):
    """{api_name}操作"""
    ip = module.params['ip']
    authkey = module.params['authkey']

    # 构造请求URL
    url = "http://%s/adcapi/v2.0/?authkey=%s&action={api_name}" % (ip, authkey)

    # 初始化响应数据
    response_data = ""

    try:
        # 根据Python版本处理请求
        if sys.version_info[0] >= 3:
            # Python 3
            import urllib.request as urllib_request
            req = urllib_request.Request(url, method='GET')
            response = urllib_request.urlopen(req)
            response_data = response.read().decode('utf-8')
        else:
            # Python 2
            import urllib2 as urllib_request
            req = urllib_request.Request(url)
            req.get_method = lambda: 'GET'
            response = urllib_request.urlopen(req)
            response_data = response.read()

        # 对于获取列表操作，直接返回响应数据，不判断success
        if response_data:
            try:
                parsed_data = json.loads(response_data)
                # 检查是否有错误信息
                if 'errmsg' in parsed_data and parsed_data['errmsg']:
                    module.fail_json(msg="操作失败", response=parsed_data)
                else:
                    module.exit_json(changed=False, result=parsed_data)
            except Exception as e:
                module.fail_json(msg="解析响应失败: %s" % str(e))
        else:
            module.fail_json(msg="未收到有效响应")

    except Exception as e:
        module.fail_json(msg="请求失败: %s" % str(e))
'''

    # 添加主函数
    template += '''

def main():
    """主函数"""
    # 定义模块参数
    module_args = dict(
        ip=dict(type='str', required=True),
        authkey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=True)
    )

    # 创建模块
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # 根据action参数调用相应的函数
    action = module.params.get('action')
    '''
    
    # 添加action映射
    for func in functions:
        action_name = func.replace('adc_', '')
        template += f'''
    if action == '{action_name}':
        {func}(module)'''
    
    template += '''
    else:
        module.fail_json(msg="不支持的action: " + str(action))


if __name__ == '__main__':
    main()'''
    
    return template

# 构建YAML模板
def create_yaml_template(api_name, module_name, function_name):
    """创建YAML模板"""
    # 从API名称生成YAML文件名
    yaml_name = f"adc_{api_name.replace('.', '_')}.yml"
    
    template = f'''---
- name: {api_name}操作
  hosts: localhost
  gather_facts: false
  
  tasks:
    - name: 调用{api_name}API
      {module_name}:
        ip: "{{{{ ip }}}}"
        authkey: "{{{{ authkey }}}}"
        action: {function_name.replace('adc_', '')}
      register: result
      
    - name: 显示结果
      debug:
        msg: "{api_name}操作成功"
      when: result.changed == false'''
    
    return yaml_name, template

# API到模块函数的映射规则
def api_to_module_function(api):
    """将API转换为模块函数名"""
    parts = api.split('.')
    if len(parts) < 3:
        return None, None, None
    
    category = parts[0]  # slb
    
    if len(parts) == 3:
        # slb.node.add
        resource = parts[1]  # node
        action = parts[2]   # add
        
        module_name = f'adc_{category}_{resource}.py'
        function_name = f'adc_{action}_{resource}'
        
    elif len(parts) >= 4:
        # slb.healthcheck.script.list
        subcategory = parts[1]  # healthcheck
        resource = parts[2]     # script
        action = parts[3]       # list
        
        # 尝试两种模块命名方式
        module_name1 = f'adc_{category}_{subcategory}.py'
        module_name2 = f'adc_{category}_{subcategory}_{resource}.py'
        
        # 优先使用第二种方式
        module_name = module_name2
        function_name = f'adc_{resource}_{action}'
    else:
        return None, None, None
    
    return module_name, function_name, api

# 分析缺失的API并创建对应的文件
missing_apis = []
for idx, row in df.iterrows():
    api = str(row.iloc[1]).strip()
    h_col = str(row.iloc[7]).strip() if len(row) > 7 else ''
    
    if not api or api == 'nan' or h_col:
        continue
    
    missing_apis.append(api)

print(f"需要创建的API数量: {len(missing_apis)}")

# 按模块分组
modules_to_create = {}
for api in missing_apis:
    module_name, function_name, _ = api_to_module_function(api)
    if module_name and function_name:
        if module_name not in modules_to_create:
            modules_to_create[module_name] = []
        modules_to_create[module_name].append((api, function_name))

print(f"需要创建的模块数量: {len(modules_to_create)}")

# 创建模块文件
created_modules = []
for module_name, apis in modules_to_create.items():
    module_path = os.path.join('library', module_name)
    
    # 如果模块文件已存在，跳过
    if os.path.exists(module_path):
        print(f"模块文件已存在: {module_name}")
        continue
    
    # 提取函数名
    functions = [func for _, func in apis]
    
    # 创建模块内容
    module_content = create_module_template(module_name, functions)
    
    # 写入文件
    with open(module_path, 'w', encoding='utf-8') as f:
        f.write(module_content)
    
    print(f"已创建模块文件: {module_name}")
    created_modules.append(module_name)

# 创建YAML文件
created_yamls = []
for module_name, apis in modules_to_create.items():
    for api, function_name in apis:
        yaml_name, yaml_content = create_yaml_template(api, module_name[:-3], function_name)
        yaml_path = os.path.join('playbooksNew', yaml_name)
        
        # 如果YAML文件已存在，跳过
        if os.path.exists(yaml_path):
            print(f"YAML文件已存在: {yaml_name}")
            continue
        
        # 写入文件
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        print(f"已创建YAML文件: {yaml_name}")
        created_yamls.append(yaml_name)

print(f"\n=== 创建完成 ===")
print(f"创建的模块文件: {len(created_modules)}")
print(f"创建的YAML文件: {len(created_yamls)}")

# 更新Excel文件
print("\n=== 更新Excel文件 ===")

for idx, row in df.iterrows():
    api = str(row.iloc[1]).strip()
    if not api or api == 'nan':
        continue
    
    module_name, function_name, _ = api_to_module_function(api)
    
    if module_name and function_name:
        module_path = os.path.join('library', module_name)
        
        # 检查模块文件是否存在
        if os.path.exists(module_path):
            # 检查函数是否存在于模块中
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if f'def {function_name}(module):' in content:
                    # 填充H、I、J列
                    df.iloc[idx, 7] = f'library/{module_name[:-3]}'  # H列
                    df.iloc[idx, 8] = module_name[:-3]              # I列
                    df.iloc[idx, 9] = function_name                 # J列

# 保存Excel文件
df.to_excel('ansible_yml_path.xlsx', index=False)
print("已保存更新后的Excel文件")

# 统计更新后的结果
missing_count = sum(1 for idx, row in df.iterrows() if str(row.iloc[7]).strip() == '')
print(f"\n更新后缺失模块函数的API数量: {missing_count}")

print("\n创建完成！")