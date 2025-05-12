#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
产品模块 - 定义制药产业模型中的药物产品
"""

import numpy as np

class Product:
    """药物产品类，表示上市的药物"""
    
    def __init__(self, prod_id, tc, mol, f, is_imitative, quality, model):
        """
        初始化药物产品
        
        Args:
            prod_id: 产品ID
            tc: 治疗类别ID
            mol: 分子ID
            f: 公司ID
            is_imitative: 是否为仿制药
            quality: 产品质量
            model: 模型实例
        """
        self.id = prod_id                  # 产品ID
        self.tc = tc                       # 治疗类别ID
        self.mol_id = mol                  # 分子ID
        self.firm = f                      # 公司ID
        self.imitative = is_imitative      # 是否为仿制药
        
        # 产品特性
        self.qp = quality                  # 产品质量
        self.c = model.cost_prod           # 单位生产成本
        self.mup = 0.0                     # 加价率
        self.p = 0.0                       # 价格
        self.pos = 0.0                     # 产品效用
        self.mkting = 0.0                  # 营销投入
        self.num_patients = 0              # 使用该产品的患者数量
        self.b_prod = 0                    # 产品上市时间
        self.out = False                   # 产品是否退出市场
        
        # 历史数据
        self.history_patients = [0.0] * (model.end_time + 1)  # 每个时间步的患者数量
        self.history_earnings = [0.0] * (model.end_time + 1)  # 每个时间步的收益
        
    def prob_of_sell(self, time, firm_id, model):
        """
        计算产品销售概率（效用）
        
        Args:
            time: 当前时间
            firm_id: 公司ID
            model: 模型实例
        """
        # 重置效用
        self.pos = 0.0
        
        # 计算产品价格
        if self.p <= 0:
            # 如果价格未设置，使用成本加价格
            self.p = self.c * (1 + self.mup)
        
        # 获取治疗类别
        tc = model.tc[self.tc]
        
        # 创新药和仿制药的质量差异
        quality = self.qp
        
        # 计算产品在该治疗类别的效用
        # 效用 = a * 质量 + b * (1/价格) + c * 营销投入
        # 其中 a、b、c 是治疗类别的权重参数
        self.pos = (tc.a * quality + 
                   tc.b * (1.0 / self.p) + 
                   tc.c * self.mkting)
        
        # 确保效用为正数
        self.pos = max(0.0, self.pos)
        
        # 重置患者数量，将在market_share计算中累加
        self.num_patients = 0 