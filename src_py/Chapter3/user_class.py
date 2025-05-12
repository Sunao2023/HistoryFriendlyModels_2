#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UserClass模块 - UserClass类的Python实现
转换自Java版本的UserClass.java
"""

import random

"""
@author Gianluca Capone and Davide Sgobba
Python转换

此类包含引用需求侧的所有变量和参数，这些变量和参数对所有企业通用或在总体层面上定义，
以及对这些变量操作或调用企业层面方法的方法
"""
class UserClass:
    
    def __init__(self, common_par, specific_par, rng):
        """
        构造函数
        在此参数被初始化为从类外部传递的值。通用参数在两个用户类之间相等；
        特定参数值在不同类之间有所不同。
        变量被初始化为合适的值。
        
        Args:
            common_par: 通用参数数组
            specific_par: 特定参数数组
            rng: 随机数生成器
        """
        # 常量定义
        self.BUYERS_OUT = 0  # 表示买家不在市场中
        self.BUYERS_IN = 1   # 表示买家在市场中
        
        # 参数初始化 - 使用严格浮点精度
        self.gamma_mod = float(specific_par[1])         # 方程8中的规模参数 (gamma-M_h)
        self.gamma_cheap = float(specific_par[2])       # 方程8中成本的指数 (gamma-CH_h)
        self.lambda_cheap = float(specific_par[3])      # 方程8中的最小成本水平 (lambda-CH_h)
        self.gamma_perf = float(specific_par[4])        # 方程8中性能的指数 (gamma-PE_h)
        self.lambda_perf = float(specific_par[5])       # 方程8中的最小性能水平 (lambda-PE_h)
        self.delta_mod = float(specific_par[6])         # 方程9中mod的指数 (delta-M_h)
        self.delta_share = float(specific_par[7])       # 方程9中跟风效应(市场份额)的指数 (delta-s_h)
        self.delta_a = float(specific_par[8])           # 方程9中品牌形象(营销能力)的指数 (delta-A_h)
        self.lambda_f = float(specific_par[9])          # 全市场活动的最小阈值 (lambda-F_h)
        self.brand_loyalty = float(specific_par[10])    # 返回到同一台计算机的客户百分比（未激活）
        self.lambda_share = float(specific_par[11])     # 方程9中的最小市场份额水平 (lambda-s_h)
        self.theta = float(specific_par[12])            # 计算机故障的概率 (THETA_h)
        
        # 根据Java实现，计算替换频率：tr_frequency = 1 / theta
        # Java中通常使用类型转换为int进行截断，Python使用int强制截断以保持一致性
        self.tr_frequency = int(1.0 / self.theta)
        
        self.min_prop_error = float(common_par[1])           # 方程9中随机因子的最小值 (e-u_f,t)
        self.range_prop_error = float(common_par[2])         # 方程9中随机因子的范围 (e-u_f,t)
        self.lambda_a = float(common_par[3])                 # 方程9中营销能力的最小水平 (lambda-A)
        self.num_of_potential_buyers = int(common_par[4])    # 潜在客户组数 (G_h)
        
        # 技术变量和对象
        self.rng = rng                  # 随机数生成器
        self.full_market = False        # 此变量初始化为"FALSE"，一旦活跃企业数量等于全市场活动的阈值，它将取值为"TRUE"
        
        # 买家相关属性初始化 - 确保与Java版本一致的处理顺序
        self.num_of_buyers = self.num_of_potential_buyers  # 实际买家数量等于潜在买家数量
        
        # 初始化买家数组，注意Python索引从0开始，但我们用1开始以匹配Java版本
        self.buyers_time_to_replace = [0] * (self.num_of_buyers + 1)  # 索引0未使用
        self.buyers_time_to_entry = [0] * (self.num_of_buyers + 1)    # 索引0未使用
        self.buyers_status = [self.BUYERS_OUT] * (self.num_of_buyers + 1)  # 索引0未使用
        
        # 初始化买家行为，确保与Java版本完全一致
        # 在Java中，nextInt(n)生成0到n-1的随机数
        # 我们在这里预先生成所有随机数，确保顺序一致
        # 存储所有随机值，避免每次调用rng导致序列不同
        random_values = []
        for i in range(self.num_of_buyers):
            random_values.append(self.rng.nextDouble())
        
        # 使用预先生成的随机数值
        for i in range(1, self.num_of_buyers + 1):
            # Java中：int timeToEntry = (int) (rng.nextDouble() * FREQ_h * 2);
            self.buyers_time_to_entry[i] = int(random_values[i-1] * self.tr_frequency * 2)
        
        # 变量
        self.size = 0                   # 用户类的规模，即当前期间向用户类买家销售的计算机数量
        
        # 统计变量
        self.mean_cheap = 0             # 活跃企业的平均成本水平
        self.mean_perf = 0              # 活跃企业的平均性能水平
        self.share_1st_gen = 0          # 第一代企业的总市场份额
        self.share_2nd_gen = 0          # 第二代企业的总市场份额
        self.share_best_2nd = 0         # 最佳第二代企业的市场份额
        self.share_div = 0              # 多元化企业的总市场份额（仅在大型组织用户类中定义）
        self.herfindahl = 0             # 赫芬达尔指数
        self.num_of_first_gen_firms = 0       # 第一代活跃企业数量
        self.num_of_adopting_firms = 0        # 使用微处理器技术的第一代企业数量（仅在大型组织用户类中定义）
        self.num_of_second_gen_firms = 0      # 第二代活跃企业数量
        self.num_of_diversified_firms = 0     # 多元化企业数量（仅在小型用户和个人用户类中定义）
    
    def reset_stats(self):
        """
        这是一个辅助方法，用于在变量取新的当前值之前将其重置为零
        """
        self.mean_cheap = 0
        self.mean_perf = 0
        self.size = 0
        
        self.share_1st_gen = 0
        self.share_2nd_gen = 0
        self.share_best_2nd = 0
        self.share_div = 0
        self.herfindahl = 0
        
        self.num_of_first_gen_firms = 0
        self.num_of_adopting_firms = 0
        self.num_of_second_gen_firms = 0
        self.num_of_diversified_firms = 0
    
    def market(self, industry, t):
        """
        这是用户类的主要方法，在此计算市场操作和统计数据
        
        Args:
            industry: Industry对象
            t: 当前时间
        """
        self.reset_stats()
        
        # 仅在此方法中使用的技术变量在此定义，统一初始化为浮点数
        num_of_purchasing_buyers = 0
        cumulated_prob = 0.0  # 使用0.0确保是浮点数
        num_of_selling_firms = 0
        busy_buyers = 0
        
        # 此循环检查企业的进入
        for f in range(1, industry.number_of_firms + 1):
            if industry.firms[f].alive:
                industry.firms[f].check_entry(t, self)
        
        # 提前生成所有随机数，确保顺序一致性
        # 在Java中，随机数是按需生成的，但每个生成的顺序是固定的
        gaussian_values = []
        for f in range(1, industry.number_of_firms + 1):
            if (industry.firms[f].alive and 
                industry.firms[f].served_user_class is not None and 
                industry.firms[f].served_user_class == self):
                # 使用与原Java代码相同的方式生成高斯随机数
                gaussian_values.append(industry.rng.nextGaussian())
        
        # 统计需要计算的企业数量以确保随机数对应
        gaussian_index = 0
        
        # 此循环计算用户类中活跃的不同企业类别的数量，并调用计算买家感知到的mod的方法
        for f in range(1, industry.number_of_firms + 1):
            if (industry.firms[f].alive and 
                industry.firms[f].served_user_class is not None and 
                industry.firms[f].served_user_class == self):
                num_of_selling_firms += 1
                
                # 添加随机扰动以破坏对称性，与Java代码保持一致
                # 在Java中: double percError = 1 + rng.nextGaussian() * EPSILON;
                # 保持精确的15位浮点数精度
                perc_error = 1.0 + (gaussian_values[gaussian_index] * industry.epsilon)
                # 按Java的处理方式，直接传递浮点值，不进行四舍五入
                industry.firms[f].calc_mod(perc_error)
                gaussian_index += 1
        
        # 计算所有企业u值之和
        sum_u = 0.0  # 使用0.0确保是浮点数
        for f in range(1, industry.number_of_firms + 1):
            if (industry.firms[f].alive and 
                industry.firms[f].served_user_class is not None and 
                industry.firms[f].served_user_class == self):
                sum_u += industry.firms[f].u
        
        # 计算累积概率，以确定新进入市场的买家的数量
        for i in range(1, self.num_of_buyers + 1):
            if (self.buyers_time_to_entry[i] == t) and (self.buyers_status[i] == self.BUYERS_OUT):
                num_of_purchasing_buyers += 1
                self.buyers_status[i] = self.BUYERS_IN
        
        # 计算所有企业的价格、利润、生产量、生产成本、市场份额
        for f in range(1, industry.number_of_firms + 1):
            if (industry.firms[f].alive and 
                industry.firms[f].served_user_class is not None and 
                industry.firms[f].served_user_class == self):
                industry.firms[f].calc_share_price_profit(sum_u, num_of_purchasing_buyers)
        
        # 预先生成更新买家状态所需的所有随机数
        random_values = []
        num_required_random = 0
        for i in range(1, self.num_of_buyers + 1):
            if self.buyers_status[i] == self.BUYERS_IN and self.buyers_time_to_replace[i] <= 0:
                num_required_random += 1

        # 生成足够的随机数
        for i in range(num_required_random):
            random_values.append(industry.rng.nextDouble())

        # 更新购买者状态
        random_index = 0
        for i in range(1, self.num_of_buyers + 1):
            if self.buyers_status[i] == self.BUYERS_IN:
                self.buyers_time_to_replace[i] -= 1
                if self.buyers_time_to_replace[i] <= 0:
                    self.buyers_status[i] = self.BUYERS_OUT
                    # 确保有足够的随机数
                    if random_index < len(random_values):
                        # 在Java中: buyers_time_to_replace[i] = (int) (rng.nextDouble() * TR_FREQUENCY * 2);
                        self.buyers_time_to_replace[i] = int(random_values[random_index] * self.tr_frequency * 2)
                        random_index += 1
                    else:
                        # 如果随机数不够，就直接生成一个新的
                        self.buyers_time_to_replace[i] = int(industry.rng.nextDouble() * self.tr_frequency * 2)
                        
                    self.buyers_time_to_entry[i] = t + 1
                    busy_buyers += 1
        
        # 计算统计数据
        if num_of_selling_firms > 0:
            self.calc_stats(industry, t)

    def calc_stats(self, industry, t):
        """
        计算市场统计数据
        
        Args:
            industry: Industry对象
            t: 当前时间
        """
        num_of_selling_firms = 0
        
        # 重置所有统计变量
        self.herfindahl = 0.0
        self.size = 0.0
        self.mean_cheap = 0.0
        self.mean_perf = 0.0
        self.share_1st_gen = 0.0
        self.share_2nd_gen = 0.0
        self.share_div = 0.0
        self.share_best_2nd = 0.0
        self.num_of_first_gen_firms = 0
        self.num_of_second_gen_firms = 0
        self.num_of_diversified_firms = 0
        self.num_of_adopting_firms = 0
        
        # 计算市场统计数据
        for f in range(1, industry.number_of_firms + 1):
            if (industry.firms[f].alive and industry.firms[f].served_user_class is not None and industry.firms[f].served_user_class == self):
                num_of_selling_firms += 1
                
                self.herfindahl += industry.firms[f].share * industry.firms[f].share
                self.size += industry.firms[f].q_sold
                self.mean_cheap += industry.firms[f].computer.cheap
                self.mean_perf += industry.firms[f].computer.perf
                
                if industry.firms[f].generation == 1:
                    self.num_of_first_gen_firms += 1
                    self.share_1st_gen += industry.firms[f].share
                    
                    # 这仅在大型组织用户类中正确定义
                    if hasattr(industry.firms[f], 'adopted') and industry.firms[f].adopted:
                        self.num_of_adopting_firms += 1
                
                if industry.firms[f].generation == 2:
                    self.num_of_second_gen_firms += 1
                    self.share_2nd_gen += industry.firms[f].share
                    if industry.firms[f].share >= self.share_best_2nd:
                        self.share_best_2nd = industry.firms[f].share
                
                # 这仅在小型用户和个人用户类中正确定义
                if industry.firms[f].generation == 3:
                    self.num_of_diversified_firms += 1
                    self.share_div += industry.firms[f].share
        
        # 计算平均值
        if num_of_selling_firms > 0:
            self.mean_cheap /= num_of_selling_firms
            self.mean_perf /= num_of_selling_firms 