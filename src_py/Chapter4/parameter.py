#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter模块 - Parameter类的Python实现
转换自Java版本的Parameter.java
"""

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含存储和检索参数值的所有元素
"""
class Parameter:
    
    def __init__(self):
        """
        构造函数
        """
        # 参数属性
        self.name = ""               # 参数名称
        self.value = ""              # 参数值
        self.variation = ""          # 敏感性分析的变异范围
        self.conversion_type = ""    # 参数类型：整数或浮点数
        self.is_under_sa = False     # 敏感性分析控制器
    
    # 以下是设置参数属性值的辅助方法
    def set_name(self, name):
        self.name = name
        
    def set_value(self, value):
        self.value = value
        
    def set_variation(self, variation):
        self.variation = variation
        
    def set_conversion_type(self, conversion_type):
        self.conversion_type = conversion_type
        
    def set_is_under_sa(self, is_under_sa):
        self.is_under_sa = is_under_sa
    
    # 以下是检索参数属性值的辅助方法
    def get_name(self):
        return self.name
        
    def get_value(self):
        return self.value
        
    def get_variation(self):
        return self.variation
        
    def get_is_under_sa(self):
        return self.is_under_sa
        
    def get_conversion_type(self):
        return self.conversion_type 