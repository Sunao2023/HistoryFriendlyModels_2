#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Component模块 - Component类的Python实现
转换自Java版本的NotSoldComponent.java
"""

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含定义计算机公司生产的组件的所有变量以及操作这些变量的方法
"""
class Component:
    
    def __init__(self, mod, firm):
        """
        构造函数
        
        Args:
            mod: 组件的设计优点 (M-CO_f,t)
            firm: 公司对象引用
        """
        # 变量
        self.mod = mod              # 组件的设计优点 (M-CO_f,t)
        self.mu_prog = 0.0          # 组件技术进步分布的均值 (mu-CO_f,t)
        self.production_cost = 0.0  # 组件生产成本 (C-CO_f,t)
        
        # 技术变量和对象
        self.firm = firm            # 访问公司对象
        
    def exit_component(self):
        """
        退出时激活的方法：重置产品层面的最相关变量
        """
        self.mod = 0.0
        self.mu_prog = 0.0
        self.production_cost = 0.0 