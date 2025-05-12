#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manager for running History-Friendly Models in Python.

This is the main entry point for running simulations of the different models
from the "Innovation and the Evolution of Industries: History-Friendly Models" book.
Python conversion of the Manager.java file.
"""

import os
import sys
import time

# 确保src_py目录和项目根目录在Python路径中
current_file_path = os.path.abspath(__file__)
src_py_dir = os.path.dirname(current_file_path)
root_dir = os.path.dirname(src_py_dir)

# 将项目根目录添加到Python路径
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 将src_py目录添加到Python路径
if src_py_dir not in sys.path:
    sys.path.insert(0, src_py_dir)

# ================== 模拟参数设置 ==================


# 是否显示详细信息
VERBOSE = True
# ==================================================

# 检查模型可用性
c3_available = False
c4_available = False
c5_available = True  # We'll focus only on Chapter 5 for now

try:
    from Chapter3.c3_model import C3Model
    c3_available = True
except ImportError:
    c3_available = False

try:
    from Chapter4.c4_model import C4Model
    c4_available = True
except ImportError:
    c4_available = False

try:
    from Chapter6.c5_model import C5Model
    c5_available = True
except ImportError:
    c5_available = False

def run_chapter3_single(verbose=True):
    """运行Chapter 3的计算机产业模型单次模拟"""
    if not c3_available:
        print("Chapter 3模型未实现或不可用")
        return False
        
    if verbose:
        print("运行Chapter 3 - 计算机产业模型 - 单次模拟")
        print("结果将保存在results_py/Chapter3/目录下")
    
    model = C3Model()
    model.make_single_simulation(True)
    
    if verbose:
        print("模拟完成！")
    return True

def run_chapter3_multiple(verbose=True):
    """运行Chapter 3的计算机产业模型多次模拟"""
    if not c3_available:
        print("Chapter 3模型未实现或不可用")
        return False
        
    if verbose:
        print(f"运行Chapter 3 - 计算机产业模型 - 多次模拟")
        print("结果将保存在results_py/Chapter3/目录下")
    
    model = C3Model()
    model.make_multiple_simulation(True)
    
    if verbose:
        print("模拟完成！")
    return True

def run_chapter3_sensitivity(verbose=True):
    """运行Chapter 3的计算机产业模型敏感性分析"""
    if not c3_available:
        print("Chapter 3模型未实现或不可用")
        return False
        
    if verbose:
        print("运行Chapter 3 - 计算机产业模型 - 敏感性分析")
        print("结果将保存在results_py/Chapter3/目录下")
    
    model = C3Model()
    model.make_sensitivity_simulation(True)
    
    if verbose:
        print("敏感性分析完成！")
    return True

def run_chapter4_single(verbose=True):
    """运行Chapter 4的半导体产业模型单次模拟"""
    if not c4_available:
        print("Chapter 4模型未实现或不可用")
        return False
        
    if verbose:
        print("运行Chapter 4 - 半导体产业模型 - 单次模拟")
        print("结果将保存在results_py/Chapter4/目录下")
    
    model = C4Model()
    model.make_single_simulation(True)
    
    if verbose:
        print("模拟完成！")
    return True

def run_chapter4_multiple( verbose=True):
    """运行Chapter 4的半导体产业模型多次模拟"""
    if not c4_available:
        print("Chapter 4模型未实现或不可用")
        return False
        
    if verbose:
        print(f"运行Chapter 4 - 半导体产业模型 - 多次模拟")
        print("结果将保存在results_py/Chapter4/目录下")
    
    model = C4Model()
    model.make_multiple_simulation(True)
    
    if verbose:
        print("模拟完成！")
    return True

def run_chapter4_sensitivity(verbose=True):
    """运行Chapter 4的半导体产业模型敏感性分析"""
    if not c4_available:
        print("Chapter 4模型未实现或不可用")
        return False
        
    if verbose:
        print("运行Chapter 4 - 半导体产业模型 - 敏感性分析")
        print("结果将保存在results_py/Chapter4/目录下")
    
    try:
        model = C4Model()
        # 设置更小的iterations值用于敏感性分析
        model.multi_time = 5  # 每次敏感性分析运行5次迭代
        model.multi_sens = 2  # 只运行2次敏感性分析
        model.make_sensitivity_simulation(True)
        
        if verbose:
            print("敏感性分析完成！")
        return True
    except Exception as e:
        print(f"运行敏感性分析时出错: {e}")
        if verbose:
            print("敏感性分析未能成功完成")
        return False

def run_chapter5_single(verbose=True):
    """运行Chapter 5的药物产业模型单次模拟"""
    if not c5_available:
        print("Chapter 5模型未实现或不可用")
        return False
        
    if verbose:
        print("运行Chapter 5 - 药物产业模型 - 单次模拟")
        print("结果将保存在results_py/Chapter5/目录下")
    
    try:
        model = C5Model()
        # 设置较小的参数进行测试
        model.end_time = 100  # 100个时期
        model.num_of_tc = 200  # 200个治疗类别
        model.num_of_firm = 50  # 50个潜在公司
        model.num_of_mol = 400  # 每个治疗类别400个分子
        model.make_single_simulation()
        
        if verbose:
            print("模拟完成！")
            print(f"结果已保存在results_py/Chapter5/目录下的singleSimulation.txt文件中")
        return True
    except Exception as e:
        print(f"运行模拟时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_chapter5_multiple( verbose=True):
    """运行Chapter 5的药物产业模型多次模拟"""
    if not c5_available:
        print("Chapter 5模型未实现或不可用")
        return False
        
    if verbose:
        print(f"运行Chapter 5 - 药物产业模型 - 多次模拟")
        print("结果将保存在results_py/Chapter5/目录下")
    
    try:
        model = C5Model()
        # 设置较小的参数进行测试
        model.end_time = 100  # 100个时期
        model.num_of_tc = 200  # 200个治疗类别
        model.num_of_firm = 50  # 50个潜在公司
        model.num_of_mol = 400  # 每个治疗类别400个分子
        model.make_multiple_simulation()
        
        if verbose:
            print("多次模拟完成！")
            print(f"结果已保存在results_py/Chapter5/目录下的multiout.txt和param.txt文件中")
        return True
    except Exception as e:
        print(f"运行多次模拟时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_and_create_dirs():
    """检查并创建必要的目录结构"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for chapter in ["Chapter3", "Chapter4", "Chapter5"]:
        results_dir = os.path.join(base_dir, "results_py", chapter)
        os.makedirs(results_dir, exist_ok=True)

def main():
    """主函数，根据注释/解注释的配置运行选定的模型"""
    # 确保结果目录存在
    check_and_create_dirs()
    
    # 根据注释/解注释的设置运行相应的模型
    
    # Chapter 3 模型
    # run_chapter3_single(VERBOSE)
    #
    # run_chapter3_multiple(VERBOSE)
    #
    # run_chapter3_sensitivity(VERBOSE)

    # Chapter 4 模型
    run_chapter4_single(VERBOSE)

    run_chapter4_multiple(VERBOSE)

    run_chapter4_sensitivity(VERBOSE)


    # Chapter 5 模型
    # run_chapter5_single(VERBOSE)
    #
    # run_chapter5_multiple(VERBOSE)
    
    return True

if __name__ == "__main__":
    main() 