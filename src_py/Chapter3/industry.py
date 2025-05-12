#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Industry模块 - Industry类的Python实现
转换自Java版本的Industry.java
"""

import random
import numpy as np

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含所有引用供给侧的变量和参数，这些变量和参数对所有企业通用或在总体层面上定义，
以及对这些变量操作或调用企业层面方法的方法
"""
class Industry:
    
    def __init__(self, parameters, tec, rng):
        """
        构造函数
        参数在此被初始化为从类外部传递的值。变量被初始化为合适的值。
        
        Args:
            parameters: 参数数组
            tec: Technology对象
            rng: 随机数生成器
        """
        # 参数初始化 - 使用严格的double精度控制
        # 由于parameters现在是numpy数组，可以直接访问
        # 数值参数直接从数组获取，不再需要单独转换
        self.project_time = parameters[1]        # 开发计算机项目的周期数 (T-D)
        self.rd_cost = parameters[2]             # 研发单位成本 (C-RD)
        self.phi_adv = parameters[3]             # 还债后分配给广告支出的利润比例 (phi-A)
        self.adv0 = parameters[4]                # 营销能力的规模参数 (a-0)
        self.adv1 = parameters[5]                # 营销能力的指数 (a-1)
        self.alpha_tr = parameters[6]            # 晶体管技术前沿距离在决定采用概率中的权重 (alpha-TR)
        self.alpha_mp = parameters[7]            # 微处理器技术进步在决定采用概率中的权重 (alpha-MP)
        self.alpha_ado = parameters[8]           # 采用新技术时感知的难度 (alpha-AD)
        self.phi_ado = parameters[9]             # 分配给采用新技术的累积资源比例 (phi-AD)
        self.fixed_ado = parameters[10]          # 采用新技术的固定成本 (C-AD)
        self.phi_exp_min = parameters[11]        # 转移到采用技术的经验最小比例 (phi-EX)
        self.phi_exp_bias = parameters[12]       # 转移到采用技术的经验比例范围 (phi-EX)
        self.phi_div = parameters[13]            # 转移到多元化部门的累积资源比例 (phi-DV)
        self.proj_time_div = parameters[14]      # 开发计算机项目的周期数 - 多元化企业 (T-DV)
        self.phi_b_div = parameters[15]          # 多元化进入者每期花费的初始预算比例 (phi-B)
        self.mark_up = parameters[16]            # 加成 (m)
        self.phi_rd = parameters[17]             # 还债后分配给研发支出的利润比例 (phi-RD)
        self.psi_div = parameters[18]            # 营销能力向多元化部门的溢出 (psi-DV)
        self.beta_lim = parameters[19]           # 技术前沿距离对技术变革的权重 (beta-LAMBDA)
        self.beta_res = parameters[20]           # 研发投资对技术变革的权重 (beta-R)
        self.beta_exp = parameters[21]           # 技术经验对技术变革的权重 (beta-EX)
        self.beta_perf = parameters[22]          # 性能维度技术变革的规模参数 (beta-PE)
        self.beta_cheap = parameters[23]         # 成本降低维度技术变革的规模参数 (beta-CH)
        self.sigma_inn = parameters[24]          # 技术变革随机扰动的标准差 (sigma-e)
        self.mu_inn = parameters[25]             # 技术变革随机扰动的平均值 (mu-e)
        self.phi_debt = parameters[26]           # 分配给还债的利润比例 (phi-DB)
        self.r = parameters[27]                  # 利率 (r)
        self.phi_rd_tild_min = parameters[28]    # 当前期间必须花费的过去研发支出的最小比例 (phitilde-RD)
        self.phi_rd_tild_bias = parameters[29]   # 当前期间必须花费的过去研发支出的比例范围 (phitilde-RD)
        self.weight_exit = parameters[30]        # 退出决策中当前表现的权重 (w-E)
        self.exit_threshold = parameters[31]     # 退出的最小阈值 (lambda-E)
        self.nu = parameters[32]                 # 从成本计算价格的比例因子 (nu)
        
        # 随机扰动参数epsilon，与Java版本一致
        self.epsilon = self.sigma_inn
        
        # 变量初始化
        self.rng = rng  # 随机数生成器
        self.firms = [None] * 200  # 企业数组，索引0未使用，与Java保持一致
        self.number_of_firms = tec.num_of_firms  # 计算机行业中潜在活跃的企业数量
        
        # 导入Firm类
        from .firm import Firm  
        
        # 初始化第一代企业
        for f in range(1, self.number_of_firms + 1):
            # 计算企业的随机属性 - 使用NumPy的随机数生成器提高精度
            cheap_mix = self.rng.random()
            perf_mix = 1.0 - cheap_mix
            init_bud = tec.min_init_bud + self.rng.random() * tec.range_init_bud
            
            # 创建企业实例
            self.firms[f] = Firm(f, 1, 1, tec, self, rng)
            
            # 设置企业属性 - 确保浮点精度
            self.firms[f].traj.cheap_mix = float(cheap_mix)
            self.firms[f].traj.perf_mix = float(perf_mix)
            self.firms[f].init_bud = float(init_bud)
            self.firms[f].bud = float(self.firms[f].init_bud)
    
    def second_generation_creation(self, time, tec, sim_info=None):
        """
        创建使用新的微处理器技术(TEC = MP)的新一代企业
        
        Args:
            time: 当前时间
            tec: Technology对象
            sim_info: 模拟信息字符串，用于调试输出
        """
        from .firm import Firm  # 导入Firm类
        
        # 检查firms数组是否需要扩展，如果需要则扩展
        max_index_needed = tec.num_of_firms + self.number_of_firms
        if max_index_needed >= len(self.firms):
            # 创建一个更大的数组并复制现有元素
            old_size = len(self.firms)
            new_size = max(old_size * 2, max_index_needed + 1)  # 确保足够大
            
            # 创建新数组并复制现有元素
            new_firms = [None] * new_size
            for i in range(old_size):
                new_firms[i] = self.firms[i]
            self.firms = new_firms
        
        # 创建新一代企业
        for f in range(self.number_of_firms + 1, tec.num_of_firms + self.number_of_firms + 1):
            self.firms[f] = Firm(f, time, 2, tec, self, self.rng)
        
        self.number_of_firms += tec.num_of_firms
    
    def diversification(self, time, tec, small_users, large_orgs, sim_info=None):
        """
        检查企业层面的多元化条件是否满足，并通过调用特定的企业构造函数创建新的多元化企业，
        通过该构造函数可以转移母公司的资源和能力。调用企业层面的方法来更新母公司的预算和条件。
        
        Args:
            time: 当前时间
            tec: Technology对象
            small_users: 小型用户UserClass对象
            large_orgs: 大型组织UserClass对象
            sim_info: 模拟信息字符串，用于调试输出
        """
        from .firm import Firm  # 导入Firm类
        
        # 计算满足多元化条件的企业数量
        # 使用NumPy数组预先分配可能的候选企业
        potential_candidates = np.zeros(self.number_of_firms, dtype=np.bool_)
        potential_new_firms = 0
        
        # 使用向量化操作查找有资格的企业
        for f in range(1, self.number_of_firms + 1):
            if (self.firms[f].alive and 
                not self.firms[f].mother and 
                self.firms[f].served_user_class == large_orgs and
                self.firms[f].tec == tec and 
                self.firms[f].norm_nw > 0 and 
                self.firms[f].bud > 0):
                potential_candidates[f-1] = True
                potential_new_firms += 1
        
        if potential_new_firms > 0:
            # 如果有可能多元化的企业，检查并扩展firms数组
            max_index_needed = self.number_of_firms + potential_new_firms
            if max_index_needed >= len(self.firms):
                # 创建一个更大的数组并复制现有元素
                old_size = len(self.firms)
                new_size = max(old_size * 2, max_index_needed + 1)  # 确保足够大
                
                # 创建新数组并复制现有元素
                new_firms = [None] * new_size
                for i in range(old_size):
                    new_firms[i] = self.firms[i]
                self.firms = new_firms
            
            # 跟踪实际创建的多元化企业数量
            diversified_count = 0
            
            # 创建多元化企业 - 只处理符合条件的企业
            for f in range(1, self.number_of_firms + 1):
                if potential_candidates[f-1]:
                    self.number_of_firms += 1
                    diversified_count += 1
                    
                    # 预先计算预算和营销能力，避免多次计算
                    init_bud = self.firms[f].bud * self.phi_div
                    mkting_capab = self.firms[f].mkting_capab * self.psi_div
                    
                    # 创建多元化企业
                    self.firms[self.number_of_firms] = Firm(
                        self.number_of_firms,  # id_num
                        time,                  # time_birth
                        3,                     # generation - 使用3代表多元化企业
                        tec,                   # tec
                        self,                  # computer_industry
                        self.rng,              # rng
                        small_users,           # user_class
                        init_bud,              # init_bud
                        mkting_capab           # ebw
                    )
                    
                    self.firms[f].diversify()
    
    def rd_invest(self, time):
        """
        调用企业层面的方法来规范研发投资
        
        Args:
            time: 当前时间
        """
        for f in range(1, self.number_of_firms + 1):
            if self.firms[f].alive:
                self.firms[f].rd_investment(time)
    
    def mkting_invest(self, time):
        """
        调用企业层面的方法来规范营销投资
        
        Args:
            time: 当前时间
        """
        for f in range(1, self.number_of_firms + 1):
            if self.firms[f].alive:
                self.firms[f].adv_expenditure(time)
    
    def adoption(self, new_tec):
        """
        获取MP技术用户的信息，并调用企业层面的方法检查是否满足采用新技术(NEWTEC = MP)的条件
        
        Args:
            new_tec: 新Technology对象
        """
        best_mp = self.find_best_mp_distance(new_tec)
        
        for f in range(1, self.number_of_firms + 1):
            if self.firms[f].alive and self.firms[f].entered and self.firms[f].tec != new_tec:
                self.firms[f].adoption(best_mp, new_tec)
    
    def find_best_mp_distance(self, tec):
        """
        采用的辅助方法：计算最佳微处理器企业的技术水平
        
        Args:
            tec: Technology对象
        
        Returns:
            float: 最大距离
        """
        # 使用NumPy优化查找最大距离
        # 预分配距离数组
        firm_distances = np.zeros(self.number_of_firms, dtype=np.float64)
        valid_firms_count = 0
        
        # 收集所有有效企业的距离
        for f in range(1, self.number_of_firms + 1):
            if self.firms[f].alive and self.firms[f].tec == tec:
                firm_distances[valid_firms_count] = self.firms[f].distance_covered()
                valid_firms_count += 1
        
        # 如果有有效企业，返回最大距离
        if valid_firms_count > 0:
            return np.max(firm_distances[:valid_firms_count])
        else:
            return 0.0
    
    def innovation(self):
        """
        调用企业层面的方法来规范技术进步活动
        """
        # 使用并行或向量化操作可以进一步优化
        for f in range(1, self.number_of_firms + 1):
            if self.firms[f].alive:
                self.firms[f].innovation()
    
    def accounting(self, time):
        """
        调用企业层面的方法来规范会计活动
        
        Args:
            time: 当前时间
        """
        for f in range(1, self.number_of_firms + 1):
            if self.firms[f].alive:
                self.firms[f].accounting(time)

    def firm_creation(self, time, user_class=None):
        """
        在给定的时间点为计算机供应商创建企业
        
        Args:
            time: 当前时间
            user_class: UserClass对象
        """
        init_computer = None
        
        # 使用NumPy高精度计算，保证数值稳定性
        ebw = np.float64(self.alfa_ebw) * np.float64(self.tec.perf_lim)
        init_bud = np.float64(self.gamma) * np.float64(self.xi) * 2.0
        
        # 预分配企业取向数组，提高效率
        orient_array = np.empty(self.batch_firms, dtype=object)
        
        # 预先决定所有企业的取向
        for i in range(self.batch_firms):
            if i % 2 == 0:  # 偶数企业标识符 - 随机取向
                if self.rng.random() < self.perf_orient_ratio:
                    orient_array[i] = "PERF_ORIENT"
                else:
                    orient_array[i] = "CHEAP_ORIENT"
            else:  # 奇数企业标识符 - 确定性取向(与行业平均方向相反)
                if self.perf_orient_ratio < 0.5:
                    orient_array[i] = "PERF_ORIENT"
                else:
                    orient_array[i] = "CHEAP_ORIENT"
        
        for i in range(self.batch_firms):
            # 使用NumPy高精度随机数生成
            init_computer_cheap = np.float64(self.tec.cheap_lim) * np.float64(self.rng.random())
            init_computer_perf = np.float64(self.tec.perf_lim) * np.float64(self.rng.random())
            
            # 获取企业取向
            orient = orient_array[i]
            
            # 创建企业，确保参数传递与Java版本一致
            self.number_of_firms += 1
            
            # 根据企业的取向设置不同参数，使用NumPy高精度计算
            if orient == "PERF_ORIENT":
                perf_rd_fraction = np.float64(self.perf_rd_fraction_perf_oriented)
                min_rd_for_prod = np.float64(self.min_rd_for_prod_perf_oriented)
            else:  # "CHEAP_ORIENT"
                perf_rd_fraction = np.float64(self.perf_rd_fraction_cheap_oriented)
                min_rd_for_prod = np.float64(self.min_rd_for_prod_cheap_oriented)
            
            init_computer = Computer(init_computer_cheap, init_computer_perf)
            
            # 创建常规企业（非多元化企业）
            self.firms[self.number_of_firms] = Firm(
                self.number_of_firms, time, self.tec.generation, 
                self.tec, self, self.rng, user_class,
                perf_rd_fraction=perf_rd_fraction, 
                min_rd_for_prod=min_rd_for_prod,
                init_computer=init_computer
            ) 