#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import pandas as pd

# 读取Excel
df = pd.read_excel('ansible_yml_path.xlsx')

print('当前Excel文件结构:')
print(df.columns.tolist())
print('总列数:', len(df.columns))

# 检查是否需要添加新列
if len(df.columns) < 10:
    # 添加H、I、J三列，并命名为对应中文名
    # H列: 模块文件相对路径
    # I列: 模块名
    # J列: Action名
    
    # 如果已经有7列，添加3列
    if len(df.columns) == 7:
        df['模块文件相对路径'] = ''  # H列
        df['模块名'] = ''           # I列
        df['Action名'] = ''         # J列
    else:
        # 如果列数不对，重新创建正确的列结构
        while len(df.columns) < 7:
            df[f'列{len(df.columns)+1}'] = ''
        
        # 确保有7列后，添加H、I、J列
        df['模块文件相对路径'] = ''
        df['模块名'] = ''
        df['Action名'] = ''

library_dir = 'library'

# 模块函数查找函数
def find_module_function(api):
    parts = api.split('.')
    if len(parts) < 3:
        return None, None, None

    category = parts[0]  # slb
    subcategory = parts[1]  # healthcheck

    if len(parts) == 3:
        # slb.node.add -> resource=node, action=add
        resource = parts[1]
        action = parts[2]
    elif len(parts) >= 4:
        # slb.healthcheck.script.list -> resource=script, action=list
        resource = parts[2]
        action = parts[3]
    else:
        return None, None, None

    # 确定可能的模块名
    module_name1 = f'adc_{category}_{subcategory}.py'  # adc_slb_healthcheck.py
    module_name2 = f'adc_{category}_{subcategory}_{resource}.py'  # adc_slb_healthcheck_script.py

    # 确定可能的函数名 - 添加更多可能的模式
    possible_functions = [
        f'adc_{resource}_{action}',  # adc_script_list (最常见)
        f'adc_{action}_{resource}',  # adc_add_node
        f'adc_list_{resource}s' if action == 'list' and len(parts) == 3 else None,  # adc_list_nodes (特殊处理)
        f'{resource}_{action}',  # script_list
        f'{action}_{resource}',  # add_node
        f'get_{resource}' if action == 'get' else None,  # get_pool
        f'get_{resource}s' if action == 'list' else None,  # get_pools
        f'list_{resource}' if action == 'list' else None,  # list_pools
        f'list_{resource}s' if action == 'list' else None,  # list_pools (复数)
        f'add_{resource}' if action == 'add' else None,  # add_node_port
        f'adc_add_{resource}' if action == 'add' else None,  # adc_add_node_port
        f'{action}_{subcategory}_{resource}' if len(parts) == 4 else None,  # add_node_port (特殊: action + subcategory + resource)
        f'adc_{action}_{subcategory}_{resource}' if len(parts) == 4 else None,  # adc_add_node_port
        f'edit_{resource}' if action == 'edit' else None,  # edit_node_port
        f'adc_edit_{resource}' if action == 'edit' else None,  # adc_edit_node_port
        f'{action}_{subcategory}_{resource}' if len(parts) == 4 and action == 'edit' else None,  # edit_node_port
        f'delete_{resource}' if action == 'del' else None,  # delete_node_port
        f'adc_delete_{resource}' if action == 'del' else None,  # adc_delete_node_port
        f'{action}_{subcategory}_{resource}' if len(parts) == 4 and action == 'del' else None,  # delete_node_port
        f'node_{action}' if resource == 'node' else None,  # node_onoff
        f'adc_node_{action}' if resource == 'node' else None,  # adc_node_onoff
        f'port_{action}' if resource == 'port' else None,  # port_onoff
        f'{action}_{subcategory}_{resource}' if len(parts) == 4 and resource == 'port' and action == 'onoff' else None,  # node_port_onoff
        f'member_{action}' if resource == 'member' else None,  # member_add
        f'adc_member_{action}' if resource == 'member' else None,  # adc_member_add
        f'{action}_{subcategory}_{resource}' if len(parts) == 4 and resource == 'member' else None,  # onoff_pool_member
        f'stat_{action}' if resource == 'stat' else None,  # stat_list
        f'adc_stat_{action}' if resource == 'stat' else None,  # adc_stat_list
        f'{resource}_{action}' if resource == 'stat' and len(parts) == 4 else None,  # node_stat_list
        f'{subcategory}_{resource}_{action}' if len(parts) == 4 and resource == 'stat' else None,  # node_stat_list
        f'vs_{action}' if resource == 'vs' else None,  # vs_add
        f'pool_{action}' if resource == 'pool' else None,  # pool_list
        f'adc_pool_{action}' if resource == 'pool' else None,  # adc_pool_list
    ]
    possible_functions = [f for f in possible_functions if f]

    # 检查哪个模块和函数存在
    for module_name, module_path in [(module_name1, os.path.join(library_dir, module_name1)),
                                      (module_name2, os.path.join(library_dir, module_name2))]:
        if not os.path.exists(module_path):
            continue

        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()

            for func_name in possible_functions:
                if f'def {func_name}(module):' in content:
                    # 找到了!
                    module_name_without_py = module_name[:-3]  # 去掉.py
                    return f'library/{module_name_without_py}', module_name_without_py, func_name

    return None, None, None

print('\\n开始填充H、I、J列...')

# 填充新列
found_count = 0
missing_count = 0

for idx, row in df.iterrows():
    api = str(row.iloc[1]).strip()

    if not api or api == 'nan':
        continue

    module_file, module_name, action_name = find_module_function(api)

    # 填充到H、I、J列（第7、8、9列，索引6、7、8）
    if module_file:
        df.iloc[idx, 7] = module_file  # H列: 模块文件相对路径
        df.iloc[idx, 8] = module_name  # I列: 模块名
        df.iloc[idx, 9] = action_name  # J列: Action名
        found_count += 1
    else:
        # 留空
        missing_count += 1

print(f'=== 填充结果 ===')
print(f'找到模块函数: {found_count}')
print(f'未找到: {missing_count}')

# 保存更新后的Excel
df.to_excel('ansible_yml_path.xlsx', index=False)
print(f'\\n已保存到 ansible_yml_path.xlsx')

# 检查新列是否正确添加
print('\\n=== 检查新列结构 ===')
print('列名:', df.columns.tolist())
print('总列数:', len(df.columns))

# 显示前5行的H、I、J列数据
print('\\n前5行的H、I、J列数据:')
for i in range(min(5, len(df))):
    api = df.iloc[i, 1]
    h_col = df.iloc[i, 7] if len(df.columns) > 7 else 'N/A'
    i_col = df.iloc[i, 8] if len(df.columns) > 8 else 'N/A'
    j_col = df.iloc[i, 9] if len(df.columns) > 9 else 'N/A'
    print(f'{api}: H={h_col}, I={i_col}, J={j_col}')