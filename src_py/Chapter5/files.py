#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件模块 - 定义制药产业模型的文件操作
"""

import os

class Files:
    """文件操作类，处理模型的输入输出文件"""
    
    def __init__(self):
        """初始化文件操作对象"""
        self.fp = None                # 输出文件
        self.fparam = None            # 参数文件
    
    def create_dir(self, dir_name):
        """
        创建目录
        
        Args:
            dir_name: 目录名称
        """
        os.makedirs(dir_name, exist_ok=True)
        
    def print(self, text):
        """
        输出文本到文件
        
        Args:
            text: 输出文本
        """
        if self.fp:
            self.fp.write(f"{text}\n")
            
    def print_param(self, text):
        """
        输出参数到参数文件
        
        Args:
            text: 参数文本
        """
        if self.fparam:
            self.fparam.write(f"{text}\n")
            
    def init_files(self, name):
        """
        初始化输出文件
        
        Args:
            name: 文件名前缀
        """
        try:
            self.fp = open(f"{name}.csv", "w")
            self.fparam = open(f"{name}_params.txt", "w")
        except Exception as e:
            print(f"Error opening files: {e}")
            
    def close_files(self):
        """关闭所有文件"""
        if self.fp:
            self.fp.close()
        if self.fparam:
            self.fparam.close() 