#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C4Model模块 - C4Model类的Python实现
转换自Java版本的C4Model.java
"""

import os
import random
import numpy as np

from .parameter import Parameter
from .component_market import ComponentMarket
from .computer_market import ComputerMarket
from .statistics import Statistics
from .sa_statistics import SA_Statistics
from .java_compatible_random import JavaCompatibleRandom

"""
@author Gianluca Capone & Davide Sgobba
Python转换

计算机行业中的垂直整合和分解:
模拟代码

这是第四章描述的模型的主类。在这里，参数通过import_parameters方法上传，
模型的时间线在make_single_simulation方法中表示
"""
class C4Model:
    
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
        self.path_parameters = os.path.join(root_dir, "parameters", "Chapter4", "parameters.txt")
        self.path_results = os.path.join(root_dir, "results_py", "Chapter4")
        
        # 确保结果目录存在
        os.makedirs(self.path_results, exist_ok=True)
        
        # 使用与Java完全相同的种子值，确保结果一致性
        self.rng_seed = 1000
        self.rng = JavaCompatibleRandom(self.rng_seed)
        
        # 重置随机种子，确保与Java实现完全一致
        random.seed(self.rng_seed)
        np.random.seed(self.rng_seed)
        
        self.parameters = [None] * 200
        
        # 声明类的其他属性
        self.statistics = None         # 用于存储和打印相关统计数据的对象
        self.sens = None               # 用于存储和打印敏感性分析相关统计数据的对象
        self.cmp_market = None         # 组件市场
        self.mf_market = None          # 主机市场
        self.pc_market = None          # 个人电脑(PC)市场
        
        # 参数
        self.end_time = 0              # 模拟周期数 (T)
        self.multi_time = 0            # 每个参数组合下的运行次数
        self.multi_sens = 0            # 敏感性分析随机提取的参数组合数量
        self.entry_time_cmp = [0, 0, 0]  # 专业化组件公司的进入周期 (T_k)
        self.entry_time_pc = 0         # PC公司的进入周期 (T_PC)
        self.num_of_firm_mf = 0        # 进入主机市场的公司数量 (F_MF)
        self.num_of_firm_pc = 0        # 进入PC市场的公司数量 (F_PC)
        self.num_of_firm_cmp = 0       # 当新技术出现时进入组件市场的公司数量 (F_k)
        
        # 变量
        self.pc_entry = False          # PC市场出现的控制器
        self.timer = 0                 # 时间指示器 (t)

    def import_parameters(self, is_sens, reload_param):
        """
        从参数文件上传参数值的方法
        
        Args:
            is_sens: 是否为敏感性分析
            reload_param: 是否重新加载参数
        """
        # 如果不是重新加载，则直接返回
        if not reload_param:
            return
            
        try:
            # 使用utf-8编码打开文件，确保正确解析特殊字符
            with open(self.path_parameters, 'r', encoding='utf-8') as input_file:
                nn = 1
                for line in input_file:
                    if line.strip():  # 确保行不为空
                        is_under_sa = line.find('@')
                        if is_under_sa > 0:
                            value_str = line[line.find("=") + 2:is_under_sa]
                            self.parameters[nn] = Parameter()
                            self.parameters[nn].set_value(value_str)
                            
                            # 确保正确识别分隔符§，如果找不到则尝试使用其他可能的编码
                            c_type = line.find('§')
                            if c_type < 0:
                                c_type = line.find('\u00a7')  # 尝试Unicode编码
                            if c_type < 0:
                                # 如果仍然找不到，使用第二个@后的位置作为备选策略
                                parts = line[is_under_sa+1:].split('@')
                                if len(parts) > 1:
                                    variation = parts[0]
                                    conversion_type = parts[1]
                                else:
                                    # 如果找不到第二个@，尝试最后一个字符作为类型
                                    variation = line[is_under_sa+1:-1]
                                    conversion_type = line[-1]
                            else:
                                variation = line[is_under_sa + 1:c_type]
                                conversion_type = line[c_type + 1:]
                                
                            self.parameters[nn].set_variation(variation)
                            self.parameters[nn].set_is_under_sa(True)
                            self.parameters[nn].set_conversion_type(conversion_type)
                        else:
                            value_str = line[line.find("=") + 2:]
                            self.parameters[nn] = Parameter()
                            self.parameters[nn].set_value(value_str)
                            
                        name = line[:line.find("=") - 1]
                        self.parameters[nn].set_name(name)
                        nn += 1
                    
        except Exception as e:
            print(f"读取参数文件时出错: {e}")
            
        self.parameters[0] = Parameter()
        self.parameters[0].set_value(str(nn - 1))
        
        if is_sens:
            self.check_param_value_for_sa()
            
        # 迭代/敏感性
        self.multi_time = int(self.parameters[1].value)
        self.multi_sens = int(self.parameters[3].value)
        
        # 所有行业：时间和进入
        self.end_time = int(self.parameters[2].value)
        self.num_of_firm_cmp = int(self.parameters[4].value)
        self.num_of_firm_mf = int(self.parameters[5].value)
        self.num_of_firm_pc = int(self.parameters[6].value)
        self.entry_time_cmp[0] = int(self.parameters[7].value)
        self.entry_time_cmp[1] = int(self.parameters[8].value)
        self.entry_time_cmp[2] = int(self.parameters[9].value)
        entry_time_mf = int(self.parameters[62].value)
        self.entry_time_pc = int(self.parameters[10].value)
        
        # 修正PC进入逻辑
        # 确保正确处理布尔值，与Java逻辑保持一致
        pc_entered_str = self.parameters[86].value.strip().lower()
        if pc_entered_str == "true":
            # 即使参数值是true，也初始化为false，只有当达到entry_time_pc时才会设为true
            self.pc_entry = False
        else:
            self.pc_entry = False
        
        # 所有行业：通用元素
        internal_cum = float(self.parameters[61].value)
        markup = float(self.parameters[32].value)
        rd_on_prof = float(self.parameters[31].value)
        
        # 组件：需求/市场
        delta_mod_cmp = float(self.parameters[43].value)
        delta_share_cmp = [0.0] * 3
        delta_share_cmp[0] = float(self.parameters[46].value)
        delta_share_cmp[1] = float(self.parameters[47].value)
        delta_share_cmp[2] = float(self.parameters[48].value)
        external_mkts_cmp = [0] * 3
        external_mkts_cmp[0] = int(self.parameters[13].value)
        external_mkts_cmp[1] = int(self.parameters[14].value)
        external_mkts_cmp[2] = int(self.parameters[15].value)
        buyers_cmp = self.num_of_firm_mf + self.num_of_firm_pc
        exit_threshold_cmp = int(self.parameters[87].value)
        
        # 组件：技术
        draw_cost_cmp = [0.0] * 3
        draw_cost_cmp[0] = float(self.parameters[51].value)
        draw_cost_cmp[1] = float(self.parameters[52].value)
        draw_cost_cmp[2] = float(self.parameters[53].value)
        ent_del_cmp = int(self.parameters[89].value)
        l1_cmp = [0.0] * 3
        l1_cmp[0] = float(self.parameters[66].value)
        l1_cmp[1] = float(self.parameters[67].value)
        l1_cmp[2] = float(self.parameters[68].value)
        l2_cmp = [0.0] * 3
        l2_cmp[0] = float(self.parameters[71].value)
        l2_cmp[1] = float(self.parameters[72].value)
        l2_cmp[2] = float(self.parameters[73].value)
        l0_cmp = [0.0] * 3
        l0_cmp[0] = float(self.parameters[63].value)
        l0_cmp[1] = (l0_cmp[0] * np.exp(l1_cmp[0] * self.entry_time_cmp[1]) 
                     * (1 - 1 / (l2_cmp[0] * (self.entry_time_cmp[1] 
                                              - (self.entry_time_cmp[0] - ent_del_cmp))))) \
                   / (np.exp(l1_cmp[1] * self.entry_time_cmp[1]) 
                     * (1 - 1 / (l2_cmp[1] * ent_del_cmp)))
        l0_cmp[2] = (l0_cmp[1] * np.exp(l1_cmp[1] * self.entry_time_cmp[2]) 
                     * (1 - 1 / (l2_cmp[1] * (self.entry_time_cmp[2] 
                                              - (self.entry_time_cmp[1] - ent_del_cmp))))) \
                   / (np.exp(l1_cmp[2] * self.entry_time_cmp[2]) 
                     * (1 - 1 / (l2_cmp[2] * ent_del_cmp)))
        nu_cmp = float(self.parameters[28].value)
        start_mod_cmp = [0.0] * 3
        start_mod_cmp[0] = float(self.parameters[20].value)
        start_mod_cmp[1] = float(self.parameters[21].value)
        start_mod_cmp[2] = float(self.parameters[22].value)
        st_dev_cmp = [0.0] * 3
        st_dev_cmp[0] = float(self.parameters[56].value)
        st_dev_cmp[1] = float(self.parameters[57].value)
        st_dev_cmp[2] = float(self.parameters[58].value)
        
        self.cmp_market = ComponentMarket(self.num_of_firm_cmp, delta_mod_cmp, delta_share_cmp,
                             nu_cmp, rd_on_prof, markup, internal_cum, st_dev_cmp,
                             draw_cost_cmp, start_mod_cmp, l0_cmp, l1_cmp, l2_cmp,
                             external_mkts_cmp, buyers_cmp, exit_threshold_cmp,
                             self.entry_time_cmp, ent_del_cmp, self.rng)
        
        # 计算机：通用元素
        chi0 = float(self.parameters[80].value)
        chi1 = float(self.parameters[78].value)
        chi2 = float(self.parameters[79].value)
        ent_del_sys = int(self.parameters[88].value)
        exit_share_par = float(self.parameters[84].value)
        inher_mod = float(self.parameters[82].value)
        leng_cont_min = int(self.parameters[11].value)
        leng_cont_bias = int(self.parameters[12].value)
        max_mod_sys = [0.0] * 3
        max_mod_sys[0] = float(self.parameters[25].value)
        max_mod_sys[1] = float(self.parameters[26].value)
        max_mod_sys[2] = float(self.parameters[27].value)
        min_int_time = int(self.parameters[76].value)
        spillover = float(self.parameters[81].value)
        weight_exit = float(self.parameters[85].value)
        xi_int = float(self.parameters[77].value)
        xi_spec = float(self.parameters[83].value)
                
        # 主机：需求/市场
        buyers_mf = int(self.parameters[16].value)
        delta_mod_mf = float(self.parameters[44].value)
        delta_share_mf = float(self.parameters[49].value)
        gamma_mf = float(self.parameters[41].value)
        start_share_mf = 1.0 / self.num_of_firm_mf
        exit_threshold_mf = exit_share_par * start_share_mf
        
        # 主机：技术
        draw_cost_mf = float(self.parameters[54].value)
        l0_mf = float(self.parameters[64].value)
        l1_mf = float(self.parameters[69].value)
        l2_mf = float(self.parameters[74].value)
        nu_mf = float(self.parameters[29].value)
        num_of_cmp_mf = float(self.parameters[18].value)
        phi_mf = float(self.parameters[33].value)
        ro_mf = float(self.parameters[37].value)
        start_mod_sys_mf = float(self.parameters[23].value)
        tau_mf = float(self.parameters[35].value)
        temp_angle_mf = float(self.parameters[39].value)
        # 防止除零错误，确保角度不为零
        if temp_angle_mf <= 0:
            temp_angle_mf = 0.1
        theta_mf = np.pi / temp_angle_mf
        st_dev_mf = float(self.parameters[59].value)
        
        self.mf_market = ComputerMarket("MF", self.num_of_firm_mf, buyers_mf, delta_mod_mf,
                        delta_share_mf, nu_mf, nu_cmp, False, rd_on_prof, markup,
                        start_share_mf, spillover, num_of_cmp_mf, ro_mf, tau_mf,
                        phi_mf, start_mod_sys_mf, internal_cum, leng_cont_min,
                        leng_cont_bias, xi_int, chi1, chi2, chi0, xi_spec, min_int_time,
                        inher_mod, self.entry_time_cmp, max_mod_sys, ent_del_sys, ent_del_cmp,
                        theta_mf, gamma_mf, st_dev_mf, st_dev_cmp, l0_cmp, l1_cmp,
                        l2_cmp, l0_mf, l1_mf, l2_mf, draw_cost_mf, draw_cost_cmp,
                        entry_time_mf, weight_exit, exit_threshold_mf, self.rng)
        
        # PC：需求/市场
        buyers_pc = int(self.parameters[17].value)
        delta_mod_pc = float(self.parameters[45].value)
        delta_share_pc = float(self.parameters[50].value)
        gamma_pc = float(self.parameters[42].value)
        start_share_pc = 1.0 / self.num_of_firm_pc
        exit_threshold_pc = exit_share_par * start_share_pc
        
        # PC：技术
        draw_cost_pc = float(self.parameters[55].value)
        l0_pc = float(self.parameters[65].value)
        l1_pc = float(self.parameters[70].value)
        l2_pc = float(self.parameters[75].value)
        nu_pc = float(self.parameters[30].value)
        num_of_cmp_pc = float(self.parameters[19].value)
        phi_pc = float(self.parameters[34].value)
        ro_pc = float(self.parameters[38].value)
        start_mod_sys_pc = float(self.parameters[24].value)
        tau_pc = float(self.parameters[36].value)
        temp_angle_pc = float(self.parameters[40].value)
        # 防止除零错误，确保角度不为零
        if temp_angle_pc <= 0:
            temp_angle_pc = 0.1
        theta_pc = np.pi / temp_angle_pc
        st_dev_pc = float(self.parameters[60].value)
        
        self.pc_market = ComputerMarket("PC", self.num_of_firm_pc, buyers_pc, delta_mod_pc,
                        delta_share_pc, nu_pc, nu_cmp, True, rd_on_prof, markup,
                        start_share_pc, spillover, num_of_cmp_pc, ro_pc, tau_pc,
                        phi_pc, start_mod_sys_pc, internal_cum, leng_cont_min,
                        leng_cont_bias, xi_int, chi1, chi2, chi0, xi_spec, min_int_time,
                        inher_mod, self.entry_time_cmp, max_mod_sys, ent_del_sys, ent_del_cmp,
                        theta_pc, gamma_pc, st_dev_pc, st_dev_cmp, l0_cmp, l1_cmp,
                        l2_cmp, l0_pc, l1_pc, l2_pc, draw_cost_pc, draw_cost_cmp,
                        self.entry_time_pc, weight_exit, exit_threshold_pc, self.rng)

    def check_param_value_for_sa(self):
        """
        在敏感性分析的情况下设置参数值的辅助方法，从随机分布中提取参数值
        """
        for i in range(1, int(self.parameters[0].value) + 1):
            if self.parameters[i].is_under_sa:
                try:
                    value = float(self.parameters[i].value)
                    variation = float(self.parameters[i].variation)
                    
                    # 确保variation是有效值
                    if variation <= 0:
                        print(f"警告: 参数 {self.parameters[i].name} 的变异值 {variation} 无效，使用默认值0.1")
                        variation = 0.1
                    
                    min_val = value - (value * variation)
                    max_val = value + (value * variation)
                    
                    conversion_type = self.parameters[i].conversion_type.strip()
                    # 移除可能的非打印字符
                    conversion_type = ''.join(c for c in conversion_type if c.isprintable())
                    
                    if conversion_type == "i":
                        i_min = round(min_val)
                        i_max = round(max_val) + 1
                        i_value = i_min + self.rng.randint(0, i_max - i_min)
                        self.parameters[i].set_value(str(i_value))
                    else:
                        value = min_val + (self.rng.random() * (max_val - min_val))
                        self.parameters[i].set_value(str(value))
                except ValueError as e:
                    print(f"处理参数 {self.parameters[i].name} 时出错: {e}")
                    print(f"  - 值: '{self.parameters[i].value}'")
                    print(f"  - 变异: '{self.parameters[i].variation}'")
                    print(f"  - 类型: '{self.parameters[i].conversion_type}'")
                    # 使用默认值继续
                    self.parameters[i].set_value(self.parameters[i].value)

    def make_single_simulation(self, is_single):
        """
        控制模型时间线的方法
        如果控制is_single为"True"，则使用特定方法上传参数并创建输出
        
        Args:
            is_single: 是否为单次模拟
        """
        if is_single:
            self.import_parameters(False, True)
            self.statistics = Statistics(self, True)
            self.statistics.open_file("/singleSimulation.csv")
        else:
            self.import_parameters(False, False)

        # 重置随机数生成器，确保每次运行的随机性与Java版本完全一致
        self.rng = JavaCompatibleRandom(self.rng_seed)
        random.seed(self.rng_seed)
        np.random.seed(self.rng_seed)
        
        # 确保PC市场最初是关闭的，只有在到达入口时间时才开启
        self.pc_entry = False
        
        # 重新初始化市场，确保每次运行的初始状态一致
        from .component_market import ComponentMarket
        from .computer_market import ComputerMarket
        
        # 重新计算市场初始化参数
        # 所有行业：通用元素
        internal_cum = float(self.parameters[61].value)
        markup = float(self.parameters[32].value)
        rd_on_prof = float(self.parameters[31].value)
        
        # 组件：需求/市场
        delta_mod_cmp = float(self.parameters[43].value)
        delta_share_cmp = [0.0] * 3
        delta_share_cmp[0] = float(self.parameters[46].value)
        delta_share_cmp[1] = float(self.parameters[47].value)
        delta_share_cmp[2] = float(self.parameters[48].value)
        external_mkts_cmp = [0] * 3
        external_mkts_cmp[0] = int(self.parameters[13].value)
        external_mkts_cmp[1] = int(self.parameters[14].value)
        external_mkts_cmp[2] = int(self.parameters[15].value)
        buyers_cmp = self.num_of_firm_mf + self.num_of_firm_pc
        exit_threshold_cmp = int(self.parameters[87].value)
        
        # 组件：技术
        draw_cost_cmp = [0.0] * 3
        draw_cost_cmp[0] = float(self.parameters[51].value)
        draw_cost_cmp[1] = float(self.parameters[52].value)
        draw_cost_cmp[2] = float(self.parameters[53].value)
        ent_del_cmp = int(self.parameters[89].value)
        l1_cmp = [0.0] * 3
        l1_cmp[0] = float(self.parameters[66].value)
        l1_cmp[1] = float(self.parameters[67].value)
        l1_cmp[2] = float(self.parameters[68].value)
        l2_cmp = [0.0] * 3
        l2_cmp[0] = float(self.parameters[71].value)
        l2_cmp[1] = float(self.parameters[72].value)
        l2_cmp[2] = float(self.parameters[73].value)
        l0_cmp = [0.0] * 3
        l0_cmp[0] = float(self.parameters[63].value)
        l0_cmp[1] = (l0_cmp[0] * np.exp(l1_cmp[0] * self.entry_time_cmp[1]) 
                     * (1 - 1 / (l2_cmp[0] * (self.entry_time_cmp[1] 
                                              - (self.entry_time_cmp[0] - ent_del_cmp))))) \
                   / (np.exp(l1_cmp[1] * self.entry_time_cmp[1]) 
                     * (1 - 1 / (l2_cmp[1] * ent_del_cmp)))
        l0_cmp[2] = (l0_cmp[1] * np.exp(l1_cmp[1] * self.entry_time_cmp[2]) 
                     * (1 - 1 / (l2_cmp[1] * (self.entry_time_cmp[2] 
                                              - (self.entry_time_cmp[1] - ent_del_cmp))))) \
                   / (np.exp(l1_cmp[2] * self.entry_time_cmp[2]) 
                     * (1 - 1 / (l2_cmp[2] * ent_del_cmp)))
        nu_cmp = float(self.parameters[28].value)
        start_mod_cmp = [0.0] * 3
        start_mod_cmp[0] = float(self.parameters[20].value)
        start_mod_cmp[1] = float(self.parameters[21].value)
        start_mod_cmp[2] = float(self.parameters[22].value)
        st_dev_cmp = [0.0] * 3
        st_dev_cmp[0] = float(self.parameters[56].value)
        st_dev_cmp[1] = float(self.parameters[57].value)
        st_dev_cmp[2] = float(self.parameters[58].value)
        
        self.cmp_market = ComponentMarket(self.num_of_firm_cmp, delta_mod_cmp, delta_share_cmp,
                             nu_cmp, rd_on_prof, markup, internal_cum, st_dev_cmp,
                             draw_cost_cmp, start_mod_cmp, l0_cmp, l1_cmp, l2_cmp,
                             external_mkts_cmp, buyers_cmp, exit_threshold_cmp,
                             self.entry_time_cmp, ent_del_cmp, self.rng)
        
        # 计算机：通用元素
        chi0 = float(self.parameters[80].value)
        chi1 = float(self.parameters[78].value)
        chi2 = float(self.parameters[79].value)
        ent_del_sys = int(self.parameters[88].value)
        exit_share_par = float(self.parameters[84].value)
        inher_mod = float(self.parameters[82].value)
        leng_cont_min = int(self.parameters[11].value)
        leng_cont_bias = int(self.parameters[12].value)
        max_mod_sys = [0.0] * 3
        max_mod_sys[0] = float(self.parameters[25].value)
        max_mod_sys[1] = float(self.parameters[26].value)
        max_mod_sys[2] = float(self.parameters[27].value)
        min_int_time = int(self.parameters[76].value)
        spillover = float(self.parameters[81].value)
        weight_exit = float(self.parameters[85].value)
        xi_int = float(self.parameters[77].value)
        xi_spec = float(self.parameters[83].value)
                
        # 主机：需求/市场
        buyers_mf = int(self.parameters[16].value)
        delta_mod_mf = float(self.parameters[44].value)
        delta_share_mf = float(self.parameters[49].value)
        gamma_mf = float(self.parameters[41].value)
        start_share_mf = 1.0 / self.num_of_firm_mf
        exit_threshold_mf = exit_share_par * start_share_mf
        
        # 主机：技术
        draw_cost_mf = float(self.parameters[54].value)
        l0_mf = float(self.parameters[64].value)
        l1_mf = float(self.parameters[69].value)
        l2_mf = float(self.parameters[74].value)
        nu_mf = float(self.parameters[29].value)
        num_of_cmp_mf = float(self.parameters[18].value)
        phi_mf = float(self.parameters[33].value)
        ro_mf = float(self.parameters[37].value)
        start_mod_sys_mf = float(self.parameters[23].value)
        tau_mf = float(self.parameters[35].value)
        temp_angle_mf = float(self.parameters[39].value)
        # 防止除零错误，确保角度不为零
        if temp_angle_mf <= 0:
            temp_angle_mf = 0.1
        theta_mf = np.pi / temp_angle_mf
        st_dev_mf = float(self.parameters[59].value)
        entry_time_mf = int(self.parameters[62].value)
        
        self.mf_market = ComputerMarket("MF", self.num_of_firm_mf, buyers_mf, delta_mod_mf,
                         delta_share_mf, nu_mf, nu_cmp, False, rd_on_prof, markup,
                         start_share_mf, spillover, num_of_cmp_mf, ro_mf, tau_mf,
                         phi_mf, start_mod_sys_mf, internal_cum, leng_cont_min,
                         leng_cont_bias, xi_int, chi1, chi2, chi0, xi_spec, min_int_time,
                         inher_mod, self.entry_time_cmp, max_mod_sys, ent_del_sys, ent_del_cmp,
                         theta_mf, gamma_mf, st_dev_mf, st_dev_cmp, l0_cmp, l1_cmp,
                         l2_cmp, l0_mf, l1_mf, l2_mf, draw_cost_mf, draw_cost_cmp,
                         entry_time_mf, weight_exit, exit_threshold_mf, self.rng)
        
        # PC：需求/市场
        buyers_pc = int(self.parameters[17].value)
        delta_mod_pc = float(self.parameters[45].value)
        delta_share_pc = float(self.parameters[50].value)
        gamma_pc = float(self.parameters[42].value)
        start_share_pc = 1.0 / self.num_of_firm_pc
        exit_threshold_pc = exit_share_par * start_share_pc
        
        # PC：技术
        draw_cost_pc = float(self.parameters[55].value)
        l0_pc = float(self.parameters[65].value)
        l1_pc = float(self.parameters[70].value)
        l2_pc = float(self.parameters[75].value)
        nu_pc = float(self.parameters[30].value)
        num_of_cmp_pc = float(self.parameters[19].value)
        phi_pc = float(self.parameters[34].value)
        ro_pc = float(self.parameters[38].value)
        start_mod_sys_pc = float(self.parameters[24].value)
        tau_pc = float(self.parameters[36].value)
        temp_angle_pc = float(self.parameters[40].value)
        # 防止除零错误，确保角度不为零
        if temp_angle_pc <= 0:
            temp_angle_pc = 0.1
        theta_pc = np.pi / temp_angle_pc
        st_dev_pc = float(self.parameters[60].value)
        
        self.pc_market = ComputerMarket("PC", self.num_of_firm_pc, buyers_pc, delta_mod_pc,
                        delta_share_pc, nu_pc, nu_cmp, True, rd_on_prof, markup,
                        start_share_pc, spillover, num_of_cmp_pc, ro_pc, tau_pc,
                        phi_pc, start_mod_sys_pc, internal_cum, leng_cont_min,
                        leng_cont_bias, xi_int, chi1, chi2, chi0, xi_spec, min_int_time,
                        inher_mod, self.entry_time_cmp, max_mod_sys, ent_del_sys, ent_del_cmp,
                        theta_pc, gamma_pc, st_dev_pc, st_dev_cmp, l0_cmp, l1_cmp,
                        l2_cmp, l0_pc, l1_pc, l2_pc, draw_cost_pc, draw_cost_cmp,
                        self.entry_time_pc, weight_exit, exit_threshold_pc, self.rng)
            
        for self.timer in range(1, self.end_time + 1):
            if self.timer == self.entry_time_cmp[1]:
                self.cmp_market.new_entry(self.num_of_firm_cmp, 1)
                self.mf_market.change_cmp_technology(1)

            if self.timer == self.entry_time_cmp[2]:
                self.cmp_market.new_entry(self.num_of_firm_cmp, 2)
                self.mf_market.change_cmp_technology(2)

            if self.timer == self.entry_time_pc:
                # 检查参数是否允许PC市场进入
                pc_entered_str = self.parameters[86].value.strip().lower()
                if pc_entered_str == "true":
                    self.pc_entry = True
                    
            self.cmp_market.rating()
            self.mf_market.contract_engine(self.cmp_market, self.timer, 0)
            if self.pc_entry:
                self.pc_market.contract_engine(self.cmp_market, self.timer, self.num_of_firm_mf)

            self.mf_market.rd_expenditure()
            if self.pc_entry:
                self.pc_market.rd_expenditure()
            self.cmp_market.rd_expenditure()
            
            self.cmp_market.mod_progress(self.timer)
            self.mf_market.mod_component_progress(self.timer, self.cmp_market)
            self.mf_market.mod_system_progress(self.timer)
            if self.pc_entry:
                self.pc_market.mod_component_progress(self.timer, self.cmp_market)
                self.pc_market.mod_system_progress(self.timer)
            
            self.mf_market.computer_mod_cost_price()
            if self.pc_entry:
                self.pc_market.computer_mod_cost_price()
            
            self.mf_market.prob_of_selling()
            if self.pc_entry:
                self.pc_market.prob_of_selling()
            self.cmp_market.external_mkt()
            
            self.mf_market.accounting(self.timer)
            if self.pc_entry:
                self.pc_market.accounting(self.timer)
            self.cmp_market.accounting(self.mf_market, self.pc_market, self.pc_entry)
            
            self.mf_market.check_exit(self.cmp_market, 0)
            if self.pc_entry:
                self.pc_market.check_exit(self.cmp_market, self.num_of_firm_mf)
            self.cmp_market.check_exit()
            
            self.mf_market.statistics(self.end_time)
            if self.pc_entry:
                self.pc_market.statistics(self.end_time)
            self.cmp_market.statistics()
            
            if is_single:
                self.statistics.make_single_statistics()
            else:
                self.statistics.make_statistics()

        if is_single:
            self.statistics.print_single_statistics()
            self.statistics.close_file()

    def make_multiple_simulation(self, is_multi):
        """
        自动化多次模拟运行的方法
        如果控制is_multi为"True"，则使用特定方法上传参数并创建输出，并显示运行次数
        
        Args:
            is_multi: 是否为多次模拟
        """
        if is_multi:
            self.import_parameters(False, True)
        
        self.statistics = Statistics(self, False)
        if is_multi:
            self.statistics.open_file("/multiSimulation.csv")
        
        # 使用基础种子，但为每次循环设置不同的随机种子
        base_seed = self.rng_seed
        
        for multi_counter in range(1, self.multi_time + 1):
            # 为每次模拟设置不同但确定的随机种子 - 与Java版本一致的方式
            self.rng_seed = base_seed + multi_counter
            
            if is_multi:
                print(f"{multi_counter}")
            self.make_single_simulation(False)
        
        # 恢复基础种子
        self.rng_seed = base_seed
        
        if not is_multi:
            # 确保self.sens已初始化
            if hasattr(self, 'sens') and self.sens is not None:
                try:
                    self.sens.make_statistics()
                except Exception as e:
                    print(f"敏感性分析统计处理时出错: {e}")
        
        if is_multi:
            self.statistics.print_multi_statistics()
            self.statistics.close_file()
    
    def make_sensitivity_simulation(self, print_sens_counter):
        """
        自动化敏感性分析模拟运行的方法
        如果控制print_sens_counter为"True"，则应显示敏感性运行次数
        
        Args:
            print_sens_counter: 是否打印敏感性计数器
        """
        try:
            # 保存基础随机种子
            base_seed = self.rng_seed
            
            # 确保参数初始化
            self.import_parameters(True, True)
            
            # 初始化敏感性分析统计对象
            from .sa_statistics import SA_Statistics
            self.sens = SA_Statistics(self)
            self.sens.open_file()
            
            # 运行多次敏感性分析
            for sens_counter in range(1, self.multi_sens + 1):
                try:
                    # 设置不同但确定的随机种子 - 确保与Java版本一致
                    # 敏感性分析种子从基础种子+1000开始，确保与多次模拟不重叠
                    self.rng_seed = base_seed + 1000 + sens_counter
                    self.rng = JavaCompatibleRandom(self.rng_seed)
                    random.seed(self.rng_seed)
                    np.random.seed(self.rng_seed)
                    
                    self.import_parameters(True, True)
                    self.make_multiple_simulation(False)
                    
                    if print_sens_counter:
                        print(f"敏感性分析运行 {sens_counter}/{self.multi_sens}")
                except Exception as e:
                    print(f"敏感性分析第{sens_counter}次运行时出错: {e}")
            
            # 恢复基础种子
            self.rng_seed = base_seed
            self.rng = JavaCompatibleRandom(self.rng_seed)
            random.seed(self.rng_seed)
            np.random.seed(self.rng_seed)
            
            # 打印结果并关闭文件
            self.sens.print_statistics()
            self.sens.close_file()
        except Exception as e:
            print(f"敏感性分析整体运行时出错: {e}")
            # 确保文件被关闭
            if hasattr(self, 'sens') and self.sens is not None:
                try:
                    self.sens.close_file()
                except:
                    pass 