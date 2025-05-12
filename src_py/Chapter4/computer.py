#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Computer模块 - Computer类的Python实现
转换自Java版本的EndProduct.java
"""

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含定义计算机产品的所有变量以及操作这些变量的方法
"""
class Computer:
    
    def __init__(self, firm=None):
        """
        构造函数
        
        Args:
            firm: 计算机公司对象引用
        """
        # 变量
        self.cheap = 0.0          # 计算机产品的便宜性 (Z-CH_f,t)
        self.mod = 0.0            # 计算机产品的设计优点 (M_f,t)
        self.mod_for_cust = 0.0   # 用户类h感知的设计优点 (M_f,h,t)
        self.perf = 0.0           # 计算机产品的性能 (Z-PE_f,t)
        self.production_cost = 0.0  # 计算机生产成本 (C-CO_f,t)
        self.u = 0.0              # 计算机销售给客户的倾向 (u_f,h,t)
        self.U = 0.0              # 计算机销售给客户的概率 (U_f,h,t)
        
        # 技术变量和对象
        self.firm = firm          # 访问公司对象
        
    def exit_computer(self):
        """
        退出时激活的方法：重置产品层面的最相关变量
        """
        self.cheap = 0.0
        self.mod = 0.0
        self.mod_for_cust = 0.0
        self.perf = 0.0
        self.production_cost = 0.0
        self.u = 0.0
        self.U = 0.0 