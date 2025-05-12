#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Firm模块 - Firm类的Python实现
转换自Java版本的Firm.java
"""

import random
import math
import numpy as np
from scipy import stats

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含定义企业异质性的所有变量和对这些变量进行操作的方法
"""
class Firm:
    
    def __init__(self, id_num, time_birth, generation, tec, computer_industry=None, 
                 rng=None, user_class=None, init_bud=None, ebw=None):
        """
        构造函数
        
        Args:
            id_num: 企业标识符
            time_birth: 企业创建的时间周期
            generation: 代标识符(1=第一代；2=第二代；3=多元化)
            tec: Technology对象
            computer_industry: Industry对象，对通用行业信息的访问
            rng: 随机数生成器
            user_class: 由企业服务的用户类(LO, SUI)
            init_bud: 初始预算(仅用于多元化企业)
            ebw: 营销能力(仅用于多元化企业)
        """
        # 技术变量和对象
        self.alive = True                 # 所有企业以"TRUE"开始，当企业失败时取值"FALSE"
        self.adopted = False              # 所有企业以"FALSE"开始，当TR企业采用新的MP技术时取值"TRUE"
        self.entered = False              # 所有企业以"FALSE"开始，当企业进入MF或PC市场时取值"TRUE"
        self.mother = False               # 所有企业以"FALSE"开始，当TR企业通过多元化进入PC市场时取值"TRUE"
        self.rng = rng                    # 随机数生成器
        self.id = id_num                  # 企业标识符
        self.time_birth = time_birth      # 企业创建的时间周期
        self.served_user_class = None     # 默认值，确保所有情况下都有定义
        
        self.computer = self.Product()
        
        # 是否为多元化企业的构造函数决定了初始化方式
        if user_class is not None:  # 多元化企业构造函数
            self.generation = 3
            self.tec = tec
            self.init_bud = init_bud
            self.bud = init_bud
            self.debt = 0
            self.mkting_capab = ebw
            self.computer_industry = computer_industry
            self.served_user_class = user_class
            
            self.traj = self.Trajectory(self)
            
            self.adv_expend = 0
            self.exit_var = 0
            self.experience = 0
            self.mod = 0
            self.norm_nw = 0
            self.share = 0
            self.number_of_bl_returns = 0
            self.number_of_breakdowns = 0
            self.number_of_new_buyers = 0
            self.number_of_served_buyers = 0
            
            self.computer.cheap = user_class.mean_cheap
            self.computer.perf = user_class.mean_perf
            
        else:  # 常规企业构造函数
            self.generation = generation
            self.tec = tec
            self.init_bud = tec.min_init_bud + rng.random() * tec.range_init_bud
            self.bud = self.init_bud
            self.debt = self.init_bud
            self.mkting_capab = 0
            self.computer_industry = computer_industry
            
            self.traj = self.Trajectory(self)
            
            self.adv_expend = 0
            self.exit_var = 0
            self.experience = 0
            self.mod = 0
            self.norm_nw = 0
            self.share = 0
            self.number_of_bl_returns = 0
            self.number_of_breakdowns = 0
            self.number_of_new_buyers = 0
            self.number_of_served_buyers = 0
        
        # 变量
        self.cheap_rd_input = 0          # 在成本方面的研发投资 (R-CH_f,t)
        self.perf_rd_input = 0           # 在性能方面的研发投资 (R-PE_f,t)
        self.price = 0                   # 计算机价格 (P_f,t)
        self.production_cost = 0         # 计算机生产成本 (C-PD_f,t)
        self.profit = 0                  # 利润 (PI_f,t)
        self.q_sold = 0                  # 企业销售的计算机数量 (q_f,h,t; q_f,t)
        self.u = 0                       # 计算机销售的倾向 (u_f,h,t)
    
    def rd_investment(self, time):
        """
        计算研发投资，区分四种情况
        
        Args:
            time: 当前时间
        """
        ante_rd = self.cheap_rd_input + self.perf_rd_input
        cur_rd_invest_prof = self.profit * (1 - self.computer_industry.phi_debt) * self.computer_industry.phi_rd
        
        # 情况1: 企业是第一代或第二代初创企业，仍有来自初始项目的资源
        if (self.generation < 3) and (time - self.time_birth < self.computer_industry.project_time):
            self.cheap_rd_input = int(math.floor(((self.init_bud / self.computer_industry.project_time + cur_rd_invest_prof)
                                               * self.traj.cheap_mix) / self.computer_industry.rd_cost))
            self.perf_rd_input = int(math.floor(((self.init_bud / self.computer_industry.project_time + cur_rd_invest_prof)
                                               * self.traj.perf_mix) / self.computer_industry.rd_cost))
        
        # 情况2: 企业已多元化，仍有来自初始项目的资源
        elif (self.generation == 3) and (time - self.time_birth < self.computer_industry.proj_time_div):
            self.cheap_rd_input = int(math.floor((((self.init_bud * self.computer_industry.phi_b_div / self.computer_industry.proj_time_div)
                                                + cur_rd_invest_prof) * self.traj.cheap_mix) / self.computer_industry.rd_cost))
            self.perf_rd_input = int(math.floor((((self.init_bud * self.computer_industry.phi_b_div / self.computer_industry.proj_time_div)
                                                + cur_rd_invest_prof) * self.traj.perf_mix) / self.computer_industry.rd_cost))
        
        # 情况3: 企业利润不允许保持当前研发支出水平
        elif cur_rd_invest_prof < ante_rd * self.computer_industry.rd_cost:
            decrease = self.computer_industry.phi_rd_tild_min + self.rng.random() * self.computer_industry.phi_rd_tild_bias
            self.cheap_rd_input = int(math.floor(self.cheap_rd_input * decrease))
            self.perf_rd_input = int(math.floor(self.perf_rd_input * decrease))
        
        # 情况4: 企业根据利润比例规则投资研发
        else:
            self.cheap_rd_input = int(math.floor((cur_rd_invest_prof * self.traj.cheap_mix)
                                               / self.computer_industry.rd_cost))
            self.perf_rd_input = int(math.floor((cur_rd_invest_prof * self.traj.perf_mix)
                                               / self.computer_industry.rd_cost))
        
        self.bud -= (self.cheap_rd_input + self.perf_rd_input) * self.computer_industry.rd_cost
        post_rd = self.cheap_rd_input + self.perf_rd_input
        
        if (self.bud <= 0) or (post_rd < 1):
            self.exit_firm()
    
    def adv_expenditure(self, time):
        """
        计算广告投资及其对营销能力的影响
        
        Args:
            time: 当前时间
        """
        # 方程6
        self.adv_expend = self.computer_industry.phi_adv * self.profit * (1 - self.computer_industry.phi_debt)
        # 方程7
        self.mkting_capab += self.computer_industry.adv0 * math.pow(self.adv_expend, self.computer_industry.adv1)
        self.bud -= self.adv_expend
        
        if self.bud <= 0:
            self.exit_firm()
    
    def calc_mod(self, perc_error):
        """
        计算所服务用户类感知的计算机mod，该用户类客户的购买倾向，
        以及由于产品故障而再次进入市场的当前客户数量
        
        Args:
            perc_error: 随机扰动因子
        """
        # 如果 served_user_class 为 None，直接返回而不执行后续操作
        if self.served_user_class is None:
            self.mod = 0
            self.u = 0
            self.number_of_new_buyers = 0
            return
            
        if ((self.computer.cheap <= self.served_user_class.lambda_cheap) or 
            (self.computer.perf <= self.served_user_class.lambda_perf)):
            self.mod = 0
        else:
            # 方程8
            self.mod = (self.served_user_class.gamma_mod *
                      math.pow((self.computer.cheap - self.served_user_class.lambda_cheap), 
                               (self.served_user_class.gamma_cheap)) *
                      math.pow((self.computer.perf - self.served_user_class.lambda_perf), 
                               (self.served_user_class.gamma_perf)))
        
        # 方程9
        self.u = (math.pow(self.mod, self.served_user_class.delta_mod) *
                math.pow(max(self.served_user_class.lambda_share, self.share), 
                         self.served_user_class.delta_share) *
                math.pow(max(self.served_user_class.lambda_a, self.mkting_capab), 
                         self.served_user_class.delta_a) *
                perc_error)
        
        self.number_of_new_buyers = 0
        
        if self.number_of_served_buyers > 0:
            # 使用scipy.stats替代Java的Binomial类
            n_b = stats.binom(int(self.number_of_served_buyers), self.served_user_class.theta)
            self.number_of_breakdowns = n_b.rvs(random_state=int(self.rng.random() * 1000000))
            self.number_of_bl_returns = int(self.number_of_breakdowns * self.served_user_class.brand_loyalty)
            self.number_of_served_buyers -= self.number_of_breakdowns
            self.number_of_new_buyers = self.number_of_bl_returns
    
    def calc_share_price_profit(self, sum_u, buying_cust):
        """
        计算市场份额、价格、生产成本、利润
        
        Args:
            sum_u: 所有企业u值的总和
            buying_cust: 购买客户数量
        """
        # 如果served_user_class为None，则不进行计算
        if self.served_user_class is None:
            return
            
        if sum_u != 0:
            # 方程10
            self.share = self.u / sum_u
        else:
            self.share = 0
        
        self.number_of_new_buyers += int(round(self.share * buying_cust))
        self.number_of_served_buyers += self.number_of_new_buyers
        
        # 方程11
        self.q_sold = self.mod * self.number_of_new_buyers
        
        if self.computer.cheap > 0:
            # 方程2
            self.price = (self.computer_industry.nu / (self.computer.cheap))
        else:
            self.price = 0
        
        # 方程3
        self.production_cost = self.price / (1 + self.computer_industry.mark_up)
        # 方程4
        self.profit = self.production_cost * self.computer_industry.mark_up * self.q_sold
        self.bud += self.profit
    
    def diversify(self):
        """
        更新多元化进入SUI市场的企业的预算和指标，设立新的独立部门
        """
        self.bud = self.bud * (1 - self.computer_industry.phi_div)
        self.mother = True
    
    def adoption(self, best_mp, new_tec):
        """
        检查是否满足企业层面采用新技术的条件，并在采用情况下对企业变量
        (预算、技术、采用控制器、经验)进行适当的更改
        
        Args:
            best_mp: 最佳微处理器企业的技术水平
            new_tec: 新Technology对象
        """
        # 方程12
        probability = math.pow(0.5 * math.pow(self.distance_from_corner(), self.computer_industry.alpha_tr) +
                             0.5 * math.pow(best_mp, self.computer_industry.alpha_mp), 
                             self.computer_industry.alpha_ado)
        
        if self.rng.random() < probability:
            # 方程13
            budget_after_adoption = self.bud * (1 - self.computer_industry.phi_ado) - self.computer_industry.fixed_ado
            
            if budget_after_adoption > 0:
                self.bud = budget_after_adoption
                self.tec = new_tec
                self.adopted = True
                
                e = (self.computer_industry.phi_exp_min + self.rng.random() * 
                     self.computer_industry.phi_exp_bias) * self.experience
                
                if e < self.experience:
                    self.experience = e
    
    def distance_from_corner(self):
        """
        这是一个辅助方法，由adoption方法调用。计算方程12中分子的第一个元素
        
        Returns:
            float: 与角落的距离
        """
        return 1 - math.sqrt((self.tec.cheap_lim - self.computer.cheap) ** 2 +
                            (self.tec.perf_lim - self.computer.perf) ** 2) / self.tec.diagonal
    
    def distance_covered(self):
        """
        这是一个辅助方法，由adoption方法调用。计算方程12中分子的第二个元素
        
        Returns:
            float: 已覆盖的距离
        """
        return math.sqrt(self.computer.cheap ** 2 + self.computer.perf ** 2) / self.tec.diagonal
    
    def innovation(self):
        """
        确定企业创新活动的结果，确定企业生产的计算机的性能和成本水平，并更新经验水平
        """
        # 在Java中，随机变量是按特定顺序生成的：先为cheap生成，再为perf生成
        # 生成随机变量，严格按照Java代码相同的顺序
        # 在Java中: double randomCheap = MU_INN + rng.nextGaussian() * SIGMA_INN;
        random_cheap = self.computer_industry.mu_inn + self.rng.nextGaussian() * self.computer_industry.sigma_inn
        # 在Java中: double randomPerf = MU_INN + rng.nextGaussian() * SIGMA_INN;
        random_perf = self.computer_industry.mu_inn + self.rng.nextGaussian() * self.computer_industry.sigma_inn
        
        # 方程1.a - 确保按照Java方式进行计算
        # 1) Java会全部转换为double进行计算
        # 2) Java的浮点运算是从左到右进行的
        # 3) Java使用IEEE 754标准
        
        # 在Java中使用的方程和执行顺序：
        # computer.perf += (BETA_PE *
        #               Math.pow((TEC.PERF_LIM - computer.perf), BETA_LAMBDA) *
        #               Math.pow(perfRDinput, BETA_R) *
        #               Math.pow(experience, BETA_EX) *
        #               randomPerf);
        
        # 先计算每一个操作数
        term1 = float(self.computer_industry.beta_perf)
        term2 = math.pow(float(self.tec.perf_lim - self.computer.perf), float(self.computer_industry.beta_lim))
        term3 = math.pow(float(self.perf_rd_input), float(self.computer_industry.beta_res)) 
        term4 = math.pow(float(self.experience), float(self.computer_industry.beta_exp))
        term5 = float(random_perf)
        
        # 从左到右乘法，确保与Java相同的计算顺序
        partial1 = term1 * term2
        partial2 = partial1 * term3
        partial3 = partial2 * term4
        perf_increment = partial3 * term5
        
        # 更新性能值
        old_perf = self.computer.perf
        self.computer.perf += perf_increment
        
        # 与阈值比较，Java会进行浮点比较
        if self.computer.perf > self.tec.perf_lim:
            self.computer.perf = self.tec.perf_lim
        
        # 方程1.b - 使用相同的精确方法控制浮点计算
        # 在Java中使用的方程和执行顺序：
        # computer.cheap += (BETA_CH *
        #                Math.pow((TEC.CHEAP_LIM - computer.cheap), BETA_LAMBDA) *
        #                Math.pow(cheapRDinput, BETA_R) *
        #                Math.pow(experience, BETA_EX) *
        #                randomCheap);
        
        # 先计算每一个操作数
        term1 = float(self.computer_industry.beta_cheap)
        term2 = math.pow(float(self.tec.cheap_lim - self.computer.cheap), float(self.computer_industry.beta_lim))
        term3 = math.pow(float(self.cheap_rd_input), float(self.computer_industry.beta_res))
        term4 = math.pow(float(self.experience), float(self.computer_industry.beta_exp))
        term5 = float(random_cheap)
        
        # 从左到右乘法，确保与Java相同的计算顺序
        partial1 = term1 * term2
        partial2 = partial1 * term3
        partial3 = partial2 * term4
        cheap_increment = partial3 * term5
        
        # 更新成本值
        old_cheap = self.computer.cheap
        self.computer.cheap += cheap_increment
        
        # 与阈值比较，Java会进行浮点比较
        if self.computer.cheap > self.tec.cheap_lim:
            self.computer.cheap = self.tec.cheap_lim
        
        # 增加经验值
        self.experience += 1
    
    def check_entry(self, time, user_class):
        """
        检查到目前为止尚未进入市场的企业生产的计算机是否满足任何用户类的最低性能和成本阈值。
        如果满足条件，企业将进入该特定用户类
        
        Args:
            time: 当前时间
            user_class: UserClass对象
        """
        # 确保user_class参数不为None
        if user_class is None:
            return
            
        if not self.entered:
            # 精确控制浮点比较，避免浮点误差导致判断不一致
            perf_condition = float(self.computer.perf) > float(user_class.lambda_perf)
            cheap_condition = float(self.computer.cheap) > float(user_class.lambda_cheap)
            
            if perf_condition and cheap_condition:
                self.entered = True
                self.served_user_class = user_class
    
    def accounting(self, time):
        """
        更新企业的债务和预算账户，并检查留在行业中是否仍然有利
        
        Args:
            time: 当前时间
        """
        if self.debt > 0:
            if (self.profit > 0) and ((time - self.time_birth > self.computer_industry.project_time)):
                self.debt -= self.profit * self.computer_industry.phi_debt
                self.bud -= self.profit * self.computer_industry.phi_debt
                
                if self.debt < 0:
                    self.bud -= self.debt
                    self.debt = 0
            
            self.debt *= (1 + self.computer_industry.r)
        
        self.bud *= (1 + self.computer_industry.r)
        past_norm_nw = self.norm_nw
        self.norm_nw = (self.bud - self.debt) / (self.init_bud * 
                                                math.pow(1 + self.computer_industry.r, time - self.time_birth))
        
        y = self.norm_nw - past_norm_nw
        # 方程5
        self.exit_var = (self.exit_var * (1 - self.computer_industry.weight_exit)) + (y * self.computer_industry.weight_exit)
        
        if self.entered and self.norm_nw < 0 and self.exit_var < self.computer_industry.exit_threshold:
            self.exit_firm()
    
    def exit_firm(self):
        """
        当退出发生时激活：将企业活动控制器切换为"FALSE"并重置最相关的变量
        """
        self.alive = False
        self.debt -= self.bud
        self.bud = 0
        self.share = 0
        self.mod = 0
        self.computer.cheap = 0
        self.computer.perf = 0
    
    class Trajectory:
        """
        此类包含有关企业技术轨迹的信息，确定研发投资资源如何分配给成本和性能
        """
        
        def __init__(self, firm):
            """
            构造函数
            
            Args:
                firm: 外部Firm类的实例
            """
            # 参数
            self.cheap_mix = firm.rng.random()          # 分配给成本研究的资源比例
            self.perf_mix = (1 - self.cheap_mix)         # 分配给性能研究的资源比例
    
    class Product:
        """
        此类包含有关企业生产的计算机在两个属性(成本和性能)中的技术水平的信息
        """
        
        def __init__(self):
            """
            构造函数
            """
            # 变量
            self.cheap = 0.0           # 成本水平 (Z-CH_f,t)
            self.perf = 0.0            # 性能水平 (Z-PE_f,t) 