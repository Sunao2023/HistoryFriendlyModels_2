#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NotSoldComponent模块 - NotSoldComponent类的Python实现
转换自Java版本的NotSoldComponent.java
"""

import math

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含定义集成计算机公司生产的组件产品的所有变量以及操作这些变量的方法
"""
class NotSoldComponent:
    
    def __init__(self, firm):
        """
        构造函数
        
        Args:
            firm: 公司对象引用
        """
        # 变量
        self.mod = 0.0               # 组件产品的设计优点 (M-CO_f,t)
        self.mu_prog = 0.0           # 组件技术进步分布的均值 (mu-CO_f,t)
        self.production_cost = 0.0    # 组件生产成本 (C-CO_f,t)
        
        # 技术变量和对象
        self.firm = firm             # 访问公司对象
        
    def calc_mod(self):
        """
        根据过去的mod水平和公共知识水平计算组件的mod
        """
        z_max = 0.0
        # 方程14.b
        self.mu_prog = (math.log(self.firm.computer_market.pk_cmp[self.firm.t_id]) * 
                      (1 - self.firm.computer_market.internal_cum) + 
                      math.log(self.mod) * self.firm.computer_market.internal_cum)
        
        for i in range(1, self.firm.num_of_draws_cmp + 1):
            z = math.exp(self.mu_prog + math.sqrt(self.firm.computer_market.sd_cmp[self.firm.t_id]) * 
                       self.firm.computer_market.rng.gauss(0, 1))
            if z > z_max:
                z_max = z
                
        if z_max > self.mod:
            self.mod = z_max
            
        if self.mod > 0:
            # 方程11
            self.production_cost = self.firm.computer_market.nu_cmp / self.mod
            
    def exit_component(self):
        """
        退出时激活的方法：重置产品层面的最相关变量
        """
        self.mu_prog = 0.0
        self.mod = 0.0
        self.production_cost = 0.0 