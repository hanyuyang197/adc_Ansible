#!/usr/bin/env python
# -*- coding: utf-8 -*-

def verify_syntax_fix():
    """验证语法错误修复"""
    print("验证adc_slb_profile_vs.py语法修复...")
    
    try:
        # 测试编译
        import py_compile
        py_compile.compile(r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library\adc_slb_profile_vs.py', doraise=True)
        print("✅ 语法检查通过")
        return True
    except Exception as e:
        print(f"❌ 语法检查失败: {e}")
        return False

def check_common_issues():
    """检查常见问题"""
    print("\n检查常见问题...")
    
    try:
        with open(r'c:\任务列表\8、巡检脚本集合\港交所\adc_Ansible\library\adc_slb_profile_vs.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查不完整的赋值语句
        if "action = \n" in content or "action =\n" in content:
            print("❌ 发现不完整的赋值语句")
            return False
        else:
            print("✅ 未发现不完整的赋值语句")
        
        # 检查语法错误
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip().endswith('=') and not line.strip().startswith('#'):
                print(f"❌ 第{i}行发现可能的语法错误: {line.strip()}")
                return False
        
        print("✅ 未发现明显的语法错误")
        return True
        
    except Exception as e:
        print(f"❌ 检查过程中出现错误: {e}")
        return False

def main():
    """主函数"""
    print("adc_slb_profile_vs.py 修复验证")
    print("=" * 40)
    
    syntax_ok = verify_syntax_fix()
    issues_ok = check_common_issues()
    
    if syntax_ok and issues_ok:
        print("\n🎉 所有检查通过！模块应该可以正常使用了。")
    else:
        print("\n⚠️  仍有一些问题需要解决。")

if __name__ == '__main__':
    main()