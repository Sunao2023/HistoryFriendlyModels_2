#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C3Model模块 - C3Model类的Python实现
转换自Java版本的C3Model.java
"""

import os
import random
import sys
import numpy as np

from .parameter import Parameter
from .technology import Technology
from .industry import Industry
from .user_class import UserClass
from .statistics import Statistics
from .sa_statistics import SA_Statistics
from .java_compatible_random import JavaCompatibleRandom

"""
@author Gianluca Capone & Davide Sgobba
Python转换

美国计算机行业与集中度动态:
模拟代码

这是第三章描述的模型的主类。在这里，参数通过import_parameters方法上传，
模型的时间线在make_single_simulation方法中表示
"""
class C3Model:
    
    def __init__(self):
        """
        构造函数
        """
        # 技术变量和对象
        # 获取项目根目录，这个方法更可靠
        # 从当前文件路径向上回溯找到项目根目录
        current_file_path = os.path.abspath(__file__)  # 当前文件的绝对路径
        src_py_dir = os.path.dirname(os.path.dirname(current_file_path))  # src_py目录
        root_dir = os.path.dirname(src_py_dir)  # 项目根目录
        
        # 设置正确的参数文件路径和结果目录
        self.path_parameters = os.path.join(root_dir, "parameters", "Chapter3", "parameters.txt")
        self.path_results = os.path.join(root_dir, "results_py", "Chapter3")
        
        # 确保结果目录存在
        os.makedirs(self.path_results, exist_ok=True)
        
        # 打印路径信息用于调试
        print(f"参数文件路径: {self.path_parameters}")
        print(f"结果目录: {self.path_results}")
        
        # 使用与Java相同的种子
        # 创建一个Java风格的随机数生成器
        self.rng = JavaCompatibleRandom(13)
        
        self.parameters = [None] * 200
        
        # 声明类的其他属性
        self.param_in = None       # 包含行业供给侧参数的NumPy数组
        self.param_tr = None       # 包含晶体管技术参数的NumPy数组
        self.param_mp = None       # 包含微处理器技术参数的NumPy数组
        self.param_cd = None       # 包含需求侧共同参数的NumPy数组
        self.param_lo = None       # 包含大型组织用户类共同参数的NumPy数组
        self.param_sui = None      # 包含小型用户和个人用户类共同参数的NumPy数组
        self.stat = None           # 用于存储和打印相关统计数据的对象
        self.sens = None           # 用于存储和打印敏感性分析相关统计数据的对象
        self.tr_tec = None         # 晶体管(TR)技术
        self.mp_tec = None         # 微处理器(MP)技术
        self.computer_industry = None   # 计算机行业的供给侧
        self.large_orgs = None      # 大型组织(LO)用户类
        self.small_users = None     # 小型用户和个人(SUI)用户类
        
        # 参数
        self.end_time = 0          # 模拟周期数(T)
        self.multi_time = 0        # 每个参数组合下的运行次数
        self.multi_sens = 0        # 敏感性分析随机提取的参数组合数量
        self.entry_time_mp = 0     # 基于微处理器的企业的进入周期(T-AD)
        self.intro_time_mp = 0     # 计算机企业可以采用微处理器的周期(T_MP)
        self.aware_div = 0.0       # PC市场多元化的最小阈值(lambda-DV)
        
        # 变量
        self.timer = 0             # 时间指示器(t)
    
    def import_parameters(self, is_sens, reload_param):
        """
        此方法用于从txt文件导入参数，将其存储在合适的对象中，并初始化模型的主要对象。
        每当需要使用新的参数集时，reload_param控制取值为True。
        当需要随机提取受敏感性分析的参数时，is_sens控制取值为True。
        
        Args:
            is_sens: 是否进行敏感性分析
            reload_param: 是否重新加载参数
        """
        if reload_param:
            for i in range(200):
                self.parameters[i] = Parameter()
            
            nn = 1
            start_in, end_in = 0, 0
            start_tr, end_tr = 0, 0
            start_mp, end_mp = 0, 0
            start_cd, end_cd = 0, 0
            start_lo, end_lo = 0, 0
            start_sui, end_sui = 0, 0
            
            try:
                with open(self.path_parameters, 'r', encoding='utf-8') as input_file:
                    for line in input_file:
                        line = line.strip()
                        if line:
                            is_under_sa = line.find('@')
                            if is_under_sa > 0:
                                self.parameters[nn].set_value(line[line.find('=') + 2:is_under_sa])
                                
                                # 尝试找到Java标准的分隔符§
                                c_type = line.find('§', is_under_sa)
                                
                                # 如果找不到标准分隔符，尝试寻找任何非数字非小数点字符作为分隔符
                                if c_type <= 0:
                                    for i, char in enumerate(line[is_under_sa + 1:]):
                                        if not (char.isdigit() or char == '.'):
                                            c_type = is_under_sa + 1 + i
                                            break
                                
                                if c_type > 0:
                                    # 变异部分是数字
                                    variation = line[is_under_sa + 1:c_type]
                                    
                                    # 转换类型是最后一个字符
                                    conv_type = line[c_type + 1:].strip()
                                    # 确保类型是有效的 (i 或 d)
                                    if conv_type and conv_type[0] in ['i', 'd']:
                                        conv_type = conv_type[0]
                                    else:
                                        conv_type = 'd'  # 默认为double类型
                                        
                                    self.parameters[nn].set_variation(variation)
                                    self.parameters[nn].set_is_under_sa(True)
                                    self.parameters[nn].set_conversion_type(conv_type)
                                else:
                                    # 无法识别分隔符，使用默认处理
                                    # 假设@后全部是变异值，类型是double
                                    variation = line[is_under_sa + 1:].strip()
                                    self.parameters[nn].set_variation(variation)
                                    self.parameters[nn].set_is_under_sa(True)
                                    self.parameters[nn].set_conversion_type("d")
                            else:
                                self.parameters[nn].set_value(line[line.find('=') + 2:])
                            
                            self.parameters[nn].set_name(line[:line.find('=') - 1])
                            
                            if "--IN-S-" in self.parameters[nn].get_name():
                                start_in = nn + 1
                            if "--IN-E-" in self.parameters[nn].get_name():
                                end_in = nn - 1
                            if "--TR-S-" in self.parameters[nn].get_name():
                                start_tr = nn + 1
                            if "--TR-E-" in self.parameters[nn].get_name():
                                end_tr = nn - 1
                            if "--MP-S-" in self.parameters[nn].get_name():
                                start_mp = nn + 1
                            if "--MP-E-" in self.parameters[nn].get_name():
                                end_mp = nn - 1
                            if "--CD-S-" in self.parameters[nn].get_name():
                                start_cd = nn + 1
                            if "--CD-E-" in self.parameters[nn].get_name():
                                end_cd = nn - 1
                            if "--LO-S-" in self.parameters[nn].get_name():
                                start_lo = nn + 1
                            if "--LO-E-" in self.parameters[nn].get_name():
                                end_lo = nn - 1
                            if "--SUI-S-" in self.parameters[nn].get_name():
                                start_sui = nn + 1
                            if "--SUI-E-" in self.parameters[nn].get_name():
                                end_sui = nn - 1
                            
                            nn += 1
            except IOError as e:
                print(f"读取参数文件错误: {e}")
            
            self.parameters[0].set_value(str(nn - 1))
            
            if is_sens:
                self.check_param_value_for_sa()
            
            # 针对技术参数使用普通列表，不转换为NumPy数组，保留字符串标签
            self.param_in = np.zeros(end_in - start_in + 2, dtype=np.float64)
            # 使用普通列表存储TR技术参数
            self.param_tr = [None] * (end_tr - start_tr + 2)
            # 使用普通列表存储MP技术参数
            self.param_mp = [None] * (end_mp - start_mp + 2)
            self.param_cd = np.zeros(end_cd - start_cd + 2, dtype=np.float64)
            self.param_lo = np.zeros(end_lo - start_lo + 2, dtype=np.float64)
            self.param_sui = np.zeros(end_sui - start_sui + 2, dtype=np.float64)

            for i in range(start_in, end_in + 1):
                idx = i - start_in + 1
                try:
                    self.param_in[idx] = float(self.parameters[i].get_value())
                except ValueError:
                    print(f"警告: 无法转换参数值 '{self.parameters[i].get_value()}' 为浮点数，使用0.0代替")
                    self.param_in[idx] = 0.0

            # 处理TR技术参数，保留标签为字符串
            for i in range(start_tr, end_tr + 1):
                idx = i - start_tr + 1
                if i == start_tr:  # 这是标签参数
                    self.param_tr[idx] = self.parameters[i].get_value()  # 直接保存字符串
                else:
                    try:
                        self.param_tr[idx] = float(self.parameters[i].get_value())
                    except ValueError:
                        print(f"警告: 无法转换参数值 '{self.parameters[i].get_value()}' 为浮点数，使用0.0代替")
                        self.param_tr[idx] = 0.0

            # 处理MP技术参数，保留标签为字符串
            for i in range(start_mp, end_mp + 1):
                idx = i - start_mp + 1
                if i == start_mp:  # 这是标签参数
                    self.param_mp[idx] = self.parameters[i].get_value()  # 直接保存字符串
                else:
                    try:
                        self.param_mp[idx] = float(self.parameters[i].get_value())
                    except ValueError:
                        print(f"警告: 无法转换参数值 '{self.parameters[i].get_value()}' 为浮点数，使用0.0代替")
                        self.param_mp[idx] = 0.0

            for i in range(start_cd, end_cd + 1):
                idx = i - start_cd + 1
                try:
                    self.param_cd[idx] = float(self.parameters[i].get_value())
                except ValueError:
                    print(f"警告: 无法转换参数值 '{self.parameters[i].get_value()}' 为浮点数，使用0.0代替")
                    self.param_cd[idx] = 0.0

            for i in range(start_lo, end_lo + 1):
                idx = i - start_lo + 1
                try:
                    self.param_lo[idx] = float(self.parameters[i].get_value())
                except ValueError:
                    print(f"警告: 无法转换参数值 '{self.parameters[i].get_value()}' 为浮点数，使用0.0代替")
                    self.param_lo[idx] = 0.0

            for i in range(start_sui, end_sui + 1):
                idx = i - start_sui + 1
                try:
                    self.param_sui[idx] = float(self.parameters[i].get_value())
                except ValueError:
                    print(f"警告: 无法转换参数值 '{self.parameters[i].get_value()}' 为浮点数，使用0.0代替")
                    self.param_sui[idx] = 0.0
        
        self.end_time = int(self.parameters[1].get_value())
        self.multi_time = int(self.parameters[2].get_value())
        self.multi_sens = int(self.parameters[3].get_value())
        self.entry_time_mp = int(self.parameters[4].get_value())
        self.intro_time_mp = int(self.parameters[5].get_value())
        self.aware_div = float(self.parameters[6].get_value())

        self.large_orgs = UserClass(self.param_cd, self.param_lo, self.rng)
        self.small_users = UserClass(self.param_cd, self.param_sui, self.rng)
        
        self.tr_tec = Technology(self.param_tr)
        self.mp_tec = Technology(self.param_mp)

        self.computer_industry = Industry(self.param_in, self.tr_tec, self.rng)
    
    def check_param_value_for_sa(self):
        """
        这是一个辅助方法，用于在敏感性分析时从随机分布中提取参数值
        """
        for i in range(1, int(self.parameters[0].get_value()) + 1):
            if self.parameters[i].get_is_under_sa():
                try:
                    value = float(self.parameters[i].get_value())
                    variation = float(self.parameters[i].get_variation())
                    min_val = value - (value * variation)
                    max_val = value + (value * variation)
                    
                    if self.parameters[i].get_conversion_type() == "i":
                        i_min = int(np.round(min_val))
                        i_max = int(np.round(max_val) + 1)
                        i_value = i_min + self.rng.randint(0, i_max - i_min - 1)
                        self.parameters[i].set_value(str(int(i_value)))
                    else:
                        # 使用NumPy生成随机数，提高精度
                        value = min_val + (self.rng.random() * (max_val - min_val))
                        self.parameters[i].set_value(str(value))
                except Exception as e:
                    print(f"Error processing parameter {i}: {e}")
    
    def make_single_simulation(self, is_single):
        """
        此方法控制模型的时间线。如果is_single控制为"True"，
        使用特定方法上传参数并创建输出
        
        Args:
            is_single: 是否为单次模拟
        """
        if is_single:
            self.import_parameters(False, True)
            self.stat = Statistics(self, True)
            self.stat.open_file("/singleSimulation.csv")
        else:
            self.import_parameters(False, False)
        
        # 当前模拟标识 - 首先检查_current_sim_info变量，为多重调用场景提供支持
        sim_info = getattr(self, '_current_sim_info', None) if not is_single else "单次模拟"
        
        # 使用NumPy数组存储比率计算，提高性能
        for self.timer in range(1, self.end_time + 1):
            if self.timer == self.entry_time_mp:
                self.computer_industry.second_generation_creation(self.timer, self.mp_tec, sim_info)
            
            # 使用NumPy的矢量化操作优化比率计算
            if self.small_users.size > 0 and self.large_orgs.size > 0:
                ratio = self.small_users.size / self.large_orgs.size
                if ratio > self.aware_div:
                    self.computer_industry.diversification(self.timer, self.mp_tec, self.small_users, self.large_orgs, sim_info)
            
            self.computer_industry.rd_invest(self.timer)
            self.computer_industry.mkting_invest(self.timer)
            
            if self.timer > self.intro_time_mp:
                self.computer_industry.adoption(self.mp_tec)
            
            self.computer_industry.innovation()
            
            self.small_users.market(self.computer_industry, self.timer)
            self.large_orgs.market(self.computer_industry, self.timer)
            
            self.computer_industry.accounting(self.timer)
            
            if is_single:
                self.stat.make_single_statistics()
            else:
                self.stat.make_statistics()
        
        if is_single:
            self.stat.print_single_statistics()
            self.stat.close_file()
    
    def make_multiple_simulation(self, is_multi):
        """
        此方法自动化多次模拟运行。如果is_multi控制为"True"，
        使用特定方法上传参数并创建输出，并显示运行次数
        
        Args:
            is_multi: 是否为多次模拟
        """
        if is_multi:
            # 仅在直接多次模拟时导入参数
            self.import_parameters(False, True)
        
        # 创建统计对象
        self.stat = Statistics(self, False)
        
        if is_multi:
            # 仅在直接多次模拟时打开文件
            self.stat.open_file("/multiSimulation.csv")
        
        # 运行多次模拟
        for multi_counter in range(1, self.multi_time + 1):
            # 生成当前模拟的标识
            current_sim_info = None
            if is_multi:
                current_sim_info = f"多次模拟 {multi_counter}/{self.multi_time}"
            elif hasattr(self, 'sens') and multi_counter == 1:
                # 在敏感性分析的第一次模拟中传递信息
                current_sim_info = "SA模拟示例"
            print(f"{multi_counter}")
            # 运行单次模拟 - 但不重新导入参数
            # 修改make_single_simulation方法，使其使用当前模拟标识
            self._current_sim_info = current_sim_info
            self.make_single_simulation(False)
        
        # 在敏感性分析模式下，保存统计数据
        if not is_multi:
            self.sens.make_statistics()
        
        # 仅在直接多次模拟时打印结果并关闭文件
        if is_multi:
            self.stat.print_multi_statistics()
            self.stat.close_file()
    
    def make_sensitivity_simulation(self, print_sens_counter):
        """
        此方法自动化敏感性分析模拟运行。如果print_sens_counter控制为"True"，
        则应显示敏感性运行的次数
        
        Args:
            print_sens_counter: 是否打印敏感性计数器
        """
        # 完全按照Java版本实现
        # 导入参数但不恢复自定义设置，使用文件中的值
        self.import_parameters(True, True)
        
        # 创建敏感性统计对象
        self.sens = SA_Statistics(self)
        self.sens.open_file()
        
        if print_sens_counter:
            print(f"开始敏感性分析, 参数组合数: {self.multi_sens}, 每组运行次数: {self.multi_time}, 每次周期数: {self.end_time}")
            print(f"总模拟次数: {self.multi_sens * self.multi_time}，与Java版本行为一致")
        
        # 运行多次敏感性模拟
        for sens_counter in range(1, self.multi_sens + 1):
            # 每次敏感性分析循环重新导入参数并随机化
            self.import_parameters(True, True)
            
            # 改进敏感性分析的进度输出
            if print_sens_counter:
                print(f"敏感性分析进度: {sens_counter}/{self.multi_sens} [{sens_counter/self.multi_sens*100:.1f}%]")
                print(f"  运行参数组合 {sens_counter}, 执行 {self.multi_time} 次模拟...")
            
            # 调用多次模拟方法，与Java版本保持一致
            self.make_multiple_simulation(False)
        
        # 打印结果并关闭文件
        if print_sens_counter:
            print(f"敏感性分析完成")
        self.sens.print_statistics()
        self.sens.close_file() 