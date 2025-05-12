#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SoldComponent模块 - SoldComponent类的Python实现
转换自Java版本的SoldComponent.java
"""

import math

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含定义专业组件公司生产的组件产品的所有变量以及操作这些变量的方法
"""
class SoldComponent:
    
    def __init__(self, mod, firm):
        """
        构造函数
        
        Args:
            mod: 组件产品的设计优点 (M-CO_f,t)
            firm: 公司对象引用
        """
        # 变量
        self.mu_prog = 0.0         # 组件技术进步分布的均值 (mu-CO_f,t)
        self.production_cost = 0.0  # 组件生产成本 (C-CO_f,t)
        self.u = 0.0               # 组件销售给计算机公司的倾向 (u_f,h,t)
        self.U = 0.0               # 组件销售给计算机公司的概率 (U_f,h,t)
        self.u_ext = 0.0           # 组件销售给外部用户的倾向 (u_f,h,t)，见脚注11的u/U和uExt/UExt的区别
        self.U_ext = 0.0           # 组件销售给外部用户的概率 (U_f,h,t)
        self.mod = mod             # 组件的设计优点 (M-CO_f,t)
        
        # 技术变量和对象
        self.firm = firm           # 访问公司对象 
    
    def calc_prop_to_sell(self):
        """
        计算向计算机公司销售的倾向
        """
        # 方程2（适用于组件）
        self.u = (self.mod ** self.firm.cmp_market.delta_mod) * \
                ((1 + self.firm.share) ** self.firm.cmp_market.delta_share[self.firm.t_id])
    
    def calc_prob_to_sell(self, sum_rat):
        """
        计算向计算机公司销售的概率
        
        Args:
            sum_rat: 所有公司倾向的总和
        """
        # 方程4（适用于组件）
        self.U = self.u / sum_rat
    
    def calc_mod(self):
        """
        根据过去的mod水平和公共知识水平计算组件的mod
        """
        z_max = 0.0
        # 方程14.b
        self.mu_prog = ((1 - self.firm.cmp_market.internal_cum) * 
                         math.log(self.firm.cmp_market.pk[self.firm.t_id]) + 
                         self.firm.cmp_market.internal_cum * math.log(self.mod))
        
        for i in range(1, self.firm.num_of_draws_cmp + 1):
            z = math.exp(self.mu_prog + 
                       math.sqrt(self.firm.cmp_market.sd_cmp[self.firm.t_id]) * 
                       self.firm.cmp_market.rng.gauss(0, 1))
            if z > z_max:
                z_max = z
        
        if z_max > self.mod:
            self.mod = z_max
        
        if self.mod > 0:
            # 方程11
            self.production_cost = self.firm.cmp_market.nu / self.mod
    
    def calc_prop_to_sell_ext(self):
        """
        计算向外部市场销售的倾向
        """
        # 方程2（适用于组件）
        self.u_ext = (self.mod ** self.firm.cmp_market.delta_mod) * \
                    ((1 + self.firm.share) ** self.firm.cmp_market.delta_share[self.firm.t_id])
    
    def calc_prob_to_sell_ext(self, sum_pts):
        """
        计算向外部市场销售的概率
        
        Args:
            sum_pts: 所有公司倾向的总和
        """
        # 方程4（适用于组件）
        self.U_ext = self.u_ext / sum_pts
    
    def exit_component(self):
        """
        退出时激活的方法：重置产品层面的最相关变量
        """
        self.mu_prog = 0.0
        self.production_cost = 0.0
        self.u = 0.0
        self.U = 0.0
        self.u_ext = 0.0
        self.U_ext = 0.0
        self.mod = 0.0 