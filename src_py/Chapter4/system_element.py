#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SystemElement模块 - SystemElement类的Python实现
转换自Java版本的SystemElement.java
"""

import math

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含定义计算机公司生产的系统元素的所有变量以及操作这些变量的方法
"""
class SystemElement:
    
    def __init__(self, mod, firm):
        """
        构造函数
        
        Args:
            mod: 系统元素的设计优点 (M-SY_f,t)
            firm: 公司对象引用
        """
        # 变量
        self.mod = mod          # 系统元素的设计优点 (M-SY_f,t)
        self.mu_prog = 0.0      # 系统技术进步分布的均值 (mu-SY_f,t)
        
        # 技术变量和对象
        self.firm = firm        # 访问公司对象
        
    def calc_mod(self):
        """
        根据过去的mod水平和公共知识水平计算系统的mod
        """
        z_max = 0.0
        # 方程14.a
        self.mu_prog = (math.log(self.firm.computer_market.pk_sys) * 
                      (1 - self.firm.computer_market.internal_cum) + 
                      math.log(self.mod) * self.firm.computer_market.internal_cum)
        
        for i in range(1, self.firm.num_of_draws_sys + 1):
            z = math.exp(self.mu_prog + 
                       math.sqrt(self.firm.computer_market.sd_sys) * 
                       self.firm.computer_market.rng.nextGaussian())
            if z > z_max:
                z_max = z
                
        if z_max > self.mod:
            self.mod = z_max
            
    def exit_system(self):
        """
        退出时激活的方法：重置产品层面的最相关变量
        """
        self.mu_prog = 0.0
        self.mod = 0.0 