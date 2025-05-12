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
        self.__name = ""                # 参数名称
        self.__value = ""               # 参数值
        self.__variation = ""           # 敏感性分析的变化范围
        self.__conversion_type = ""     # 参数类型：Integer或Double
        self.__is_under_sa = False      # 敏感性分析控制器
    
    # 以下是设置参数属性值的辅助方法
    def set_name(self, name):
        """
        设置参数名称
        
        Args:
            name: 参数名称
        """
        self.__name = name
    
    def set_value(self, value):
        """
        设置参数值
        
        Args:
            value: 参数值
        """
        self.__value = value
    
    def set_variation(self, variation):
        """
        设置变化范围
        
        Args:
            variation: 变化范围
        """
        self.__variation = variation
    
    def set_conversion_type(self, conversion_type):
        """
        设置转换类型
        
        Args:
            conversion_type: 转换类型
        """
        self.__conversion_type = conversion_type
    
    def set_is_under_sa(self, is_under_sa):
        """
        设置是否进行敏感性分析
        
        Args:
            is_under_sa: 是否进行敏感性分析
        """
        self.__is_under_sa = is_under_sa
    
    # 以下是检索参数属性值的辅助方法
    def get_name(self):
        """
        获取参数名称
        
        Returns:
            str: 参数名称
        """
        return self.__name
    
    def get_value(self):
        """
        获取参数值
        
        Returns:
            str: 参数值
        """
        return self.__value
    
    def get_variation(self):
        """
        获取变化范围
        
        Returns:
            str: 变化范围
        """
        return self.__variation
    
    def get_conversion_type(self):
        """
        获取转换类型
        
        Returns:
            str: 转换类型
        """
        return self.__conversion_type
    
    def get_is_under_sa(self):
        """
        获取是否进行敏感性分析
        
        Returns:
            bool: 是否进行敏感性分析
        """
        return self.__is_under_sa 