#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaCompatibleRandom模块 - 精确模拟Java Random类行为的随机数生成器
"""

import math

class JavaCompatibleRandom:
    """
    这个类精确模拟Java的Random类行为，确保Python和Java版本结果一致
    
    Java Random类实现是一个标准的线性同余生成器，使用以下参数：
    multiplier (a): 0x5DEECE66D (25214903917)
    addend (c): 0xB (11)
    mask: 0xFFFFFFFFFFFF (2^48 - 1)
    """
    
    def __init__(self, seed):
        """
        初始化随机数生成器，使用与Java完全相同的种子算法
        
        Args:
            seed: 随机种子，与Java的setSeed方法使用相同的种子
        """
        # Java Random类的常量
        self.multiplier = 0x5DEECE66D
        self.addend = 0xB
        self.mask = (1 << 48) - 1
        
        # 初始化种子，与Java相同的处理
        self.seed = (seed ^ self.multiplier) & self.mask
        
        # 高斯分布变量，与Java的nextGaussian()相同
        self.haveNextNextGaussian = False
        self.nextNextGaussian = 0.0
    
    def setSeed(self, seed):
        """
        重置随机数生成器的种子，与Java的setSeed方法完全一致
        
        Args:
            seed: 新的随机种子
        """
        self.seed = (seed ^ self.multiplier) & self.mask
        self.haveNextNextGaussian = False
    
    def next(self, bits):
        """
        生成指定位数的随机数，这是Java Random类的核心方法
        
        Args:
            bits: 返回的随机位数
            
        Returns:
            int: 随机整数
        """
        self.seed = (self.seed * self.multiplier + self.addend) & self.mask
        return self.seed >> (48 - bits)
    
    def nextBytes(self, bytes_array):
        """
        填充字节数组，与Java的nextBytes方法相同
        
        Args:
            bytes_array: 要填充的字节数组
            
        Returns:
            list: 填充后的字节数组
        """
        for i in range(len(bytes_array)):
            if i % 4 == 0:
                rnd = self.next(32)
            bytes_array[i] = rnd & 0xFF
            rnd >>= 8
        return bytes_array
    
    def nextInt(self, n=None):
        """
        生成随机整数，与Java的nextInt方法完全一致
        
        Args:
            n: 上限(不包含)，如果为None，返回完整的int范围
            
        Returns:
            int: 随机整数
        """
        if n is None:
            return self.next(32)
        
        if n <= 0:
            raise ValueError("n must be positive")
        
        if (n & -n) == n:  # n是2的幂
            return (n * self.next(31)) >> 31
        
        bits = self.next(31)
        val = bits % n
        while bits - val + (n - 1) < 0:
            bits = self.next(31)
            val = bits % n
        return val
    
    def nextLong(self):
        """
        生成64位随机整数，与Java的nextLong方法相同
        
        Returns:
            int: 随机长整数
        """
        return ((self.next(32) << 32) + self.next(32))
    
    def nextBoolean(self):
        """
        生成随机布尔值，与Java的nextBoolean方法相同
        
        Returns:
            bool: 随机布尔值
        """
        return self.next(1) != 0
    
    def nextFloat(self):
        """
        生成0.0到1.0之间的随机浮点数，与Java的nextFloat方法相同
        
        Returns:
            float: 0.0到1.0之间的随机数
        """
        return self.next(24) / float(1 << 24)
    
    def nextDouble(self):
        """
        生成0.0到1.0之间的随机双精度数，与Java的nextDouble方法相同
        
        Returns:
            float: 0.0到1.0之间的随机数
        """
        return ((self.next(26) << 27) + self.next(27)) / float(1 << 53)
    
    def nextGaussian(self):
        """
        生成标准正态分布的随机数，与Java的nextGaussian方法相同
        
        Returns:
            float: 均值为0、标准差为1的随机数
        """
        if self.haveNextNextGaussian:
            self.haveNextNextGaussian = False
            return self.nextNextGaussian
        
        v1 = 0
        v2 = 0
        s = 0
        
        while s >= 1 or s == 0:
            v1 = 2 * self.nextDouble() - 1
            v2 = 2 * self.nextDouble() - 1
            s = v1 * v1 + v2 * v2
        
        multiplier = math.sqrt(-2 * math.log(s) / s)
        self.nextNextGaussian = v2 * multiplier
        self.haveNextNextGaussian = True
        return v1 * multiplier
    
    # 为了方便使用，提供一些Python风格的别名
    def random(self):
        """
        生成0.0到1.0之间的随机浮点数，Python风格的别名
        
        Returns:
            float: 0.0到1.0之间的随机数
        """
        return self.nextDouble()
    
    def randint(self, a, b):
        """
        生成[a, b]范围内的随机整数，Python风格的别名
        
        Args:
            a: 下限(包含)
            b: 上限(包含)
            
        Returns:
            int: a到b之间的随机整数
        """
        return a + self.nextInt(b - a + 1)
    
    def gauss(self, mu, sigma):
        """
        生成指定均值和标准差的高斯分布随机数
        
        Args:
            mu: 均值
            sigma: 标准差
            
        Returns:
            float: 服从高斯分布的随机数
        """
        return mu + sigma * self.nextGaussian() 