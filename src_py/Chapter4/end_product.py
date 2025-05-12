#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EndProduct模块 - EndProduct类的Python实现
转换自Java版本的EndProduct.java
"""

import math

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含定义计算机产品的所有变量以及操作这些变量的方法
"""
class EndProduct:
    
    def __init__(self, firm):
        """
        构造函数
        
        Args:
            firm: 公司对象引用
        """
        # 变量
        self.cheap = 0.0           # 计算机产品的低成本性 (Z-CH_f,t)
        self.perf = 0.0            # 计算机产品的性能 (Z-PE_f,t)
        self.mod = 0.0             # 计算机产品的设计优点 (M_f,t)
        self.mod_for_cust = 0.0    # 用户类h的客户感知的设计优点 (M_f,h,t)
        self.production_cost = 0.0  # 计算机生产成本 (C-CO_f,t)
        self.u = 0.0               # 计算机销售给客户的倾向 (u_f,h,t)
        self.U = 0.0               # 计算机销售给客户的概率 (U_f,h,t)
        
        # 技术变量和对象
        self.firm = firm           # 访问公司对象
        
    def calc_mod(self):
        """
        根据组件和系统元素的mod水平计算计算机的mod
        """
        if self.firm.system.mod > self.firm.computer_market.limit_sys_mod[self.firm.t_id]:
            # 方程1，参见关于系统元素mod技术限制的脚注14
            self.mod = self.firm.computer_market.phi * math.pow(
                self.firm.computer_market.tau 
                * math.pow(self.firm.component.mod, -self.firm.computer_market.rho)
                + (1 - self.firm.computer_market.tau)
                * math.pow(self.firm.computer_market.limit_sys_mod[self.firm.t_id], -self.firm.computer_market.rho),
                -(1 / self.firm.computer_market.rho))
        else:
            # 方程1
            self.mod = self.firm.computer_market.phi * math.pow(
                self.firm.computer_market.tau
                * math.pow(self.firm.component.mod, -self.firm.computer_market.rho)
                + (1 - self.firm.computer_market.tau)
                * math.pow(self.firm.system.mod, -self.firm.computer_market.rho),
                -(1 / self.firm.computer_market.rho))
                
    def calc_cheap_perf(self):
        """
        根据计算机的mod计算其低成本性和性能
        """
        self.cheap = self.mod * math.cos(self.firm.computer_market.theta)
        self.perf = self.mod * math.sin(self.firm.computer_market.theta)
        
    def calc_cost(self):
        """
        计算计算机的生产成本
        """
        # 方程9
        self.production_cost = self.firm.price / (1 + self.firm.computer_market.markup)
        
    def calc_prop_to_sell(self):
        """
        计算特定用户类感知的mod和向这些客户销售的倾向
        """
        # 方程3
        self.mod_for_cust = (math.pow(self.cheap, self.firm.computer_market.gamma) 
                           * math.pow(self.perf, 1 - self.firm.computer_market.gamma))
        # 方程2
        self.u = (math.pow(self.mod_for_cust, self.firm.computer_market.delta_mod)
                * math.pow(1 + self.firm.share, self.firm.computer_market.delta_share))
                
    def calc_prob_to_sell(self, sum_pts):
        """
        计算销售概率
        
        Args:
            sum_pts: 所有倾向总和
        """
        # 方程4
        self.U = self.u / sum_pts
        
    def exit_computer(self):
        """
        退出时激活的方法：重置产品层面的最相关变量
        """
        self.cheap = 0.0
        self.perf = 0.0
        self.mod = 0.0
        self.mod_for_cust = 0.0
        self.production_cost = 0.0
        self.u = 0.0
        self.U = 0.0 