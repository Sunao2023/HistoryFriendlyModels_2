#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Technology模块 - Technology类的Python实现
转换自Java版本的Technology.java
"""

import math

"""
@author Gianluca Capone and Davide Sgobba
Python转换

此类包含所有标识两种半导体技术的变量和参数：晶体管和微处理器
"""
class Technology:
    
    def __init__(self, parameters):
        """
        构造函数
        
        Args:
            parameters: 参数数组
        """
        # 参数
        self.label = parameters[1]                    # 技术标签 - 直接使用字符串 'TR' 或 'MP'
        self.cheap_lim = float(parameters[2])         # 成本技术前沿 (LAMBDA-CH_k)
        self.perf_lim = float(parameters[3])          # 性能技术前沿 (LAMBDA-PE_k)
        self.diagonal = math.sqrt(                    # 对角线：从原点到前沿的距离 (d_k)
            self.cheap_lim**2 + self.perf_lim**2
        )
        self.min_init_bud = float(parameters[4])      # 企业初始预算的最小值 (B-0_f,k)
        self.range_init_bud = float(parameters[5])    # 企业初始预算的值范围 (B-0_f,k)
        self.num_of_firms = int(parameters[6])        # 潜在企业数量 (F_k) 