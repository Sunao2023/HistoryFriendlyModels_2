#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
治疗类别模块 - 定义药物产业模型中的治疗类别
"""

import numpy as np
from .molecule import Molecule

class SubMarket:
    """子市场类，表示治疗类别中的一个细分市场"""
    
    def __init__(self, value=0):
        """
        初始化子市场
        
        Args:
            value: 子市场的大小（患者数量）
        """
        self.value_mkt = value    # 子市场大小（患者数量）
        self.q_min_req = 0        # 进入该子市场所需的最低质量
        self.store_pos = 0        # 所有产品效用的总和
        
    def __str__(self):
        return f"SubMarket(value_mkt={self.value_mkt}, q_min_req={self.q_min_req}, store_pos={self.store_pos})"

class TherapeuticCategory:
    """治疗类别，表示药物针对的疾病种类"""
    
    def __init__(self, tc_id, patients, a_val, b_val, c_val, end_time, model):
        """
        初始化治疗类别
        
        Args:
            tc_id: 治疗类别ID
            patients: 患者数量
            a_val: 质量权重
            b_val: 价格权重
            c_val: 市场营销权重
            end_time: 模拟结束时间
            model: 模型实例
        """
        self.id = tc_id                  # 治疗类别ID
        self.value = patients            # 患者数量（市场规模）
        self.a = a_val                   # 质量权重
        self.b = b_val                   # 价格权重
        self.c = c_val                   # 市场营销权重
        
        # 初始化分子数组
        self.mol = [Molecule(i) for i in range(model.num_of_mol + 1)]
        
        # 初始化统计数组
        self.dim = [0] * (end_time + 1)  # 维度数组
        self.in_product = [0] * (end_time + 1)  # 产品数量
        self.in_product_only_inno = [0] * (end_time + 1)  # 创新产品数量
        self.in_firm = [0] * (end_time + 1)  # 公司数量
        self.herfindahl = [0.0] * (end_time + 1)  # 赫芬达尔指数
        self.herfindahl1 = [0.0] * (end_time + 1)  # 另一个赫芬达尔指数
        self.pat = [0] * (end_time + 1)  # 专利数量
        
        # 治疗类别的子市场
        self.s_mkt = [SubMarket() for _ in range(model.num_of_sub_mkt)]
        
        # 其他统计量
        self.inno_sh = 0.0  # 创新份额
        self.imi_sh = 0.0   # 仿制份额
        
        # 研发活动跟踪
        self.on_ta_res = 0  # 正在研发的分子数量
        self.store_pos = 0  # 产品效用总和
        
    def set_sub_mkt_value(self, model):
        """
        设置子市场的价值
        
        Args:
            model: 模型实例
        """
        # 分配总患者到不同子市场
        # 假设子市场大小遵循指数分布
        total_patients = self.value
        remaining_patients = total_patients
        
        # 计算最后一个子市场之前的所有子市场大小
        for i in range(model.num_of_sub_mkt - 1):
            if i == 0:
                # 第一个子市场最大
                market_size = int(remaining_patients * 0.4)
            elif i == 1:
                # 第二个子市场较小
                market_size = int(remaining_patients * 0.3)
            else:
                # 剩余子市场平均分配
                market_size = int(remaining_patients / (model.num_of_sub_mkt - i))
                
            self.s_mkt[i].value_mkt = market_size
            remaining_patients -= market_size
        
        # 最后一个子市场获得剩余患者
        self.s_mkt[model.num_of_sub_mkt - 1].value_mkt = remaining_patients
    
    def calc_q_min_in_smkt(self, model):
        """
        计算每个子市场的最低质量要求
        
        Args:
            model: 模型实例
        """
        # 计算每个子市场的最低质量要求
        # 子市场越大，质量要求越低
        for i in range(model.num_of_sub_mkt):
            # 第一个子市场没有最低质量要求
            if i == 0:
                self.s_mkt[i].q_min_req = 0
            else:
                # 其他子市场的质量要求
                # 更高的索引表示更小的子市场，需要更高的质量
                q_min = int(model.quality_check * (1 + i * 0.2))
                self.s_mkt[i].q_min_req = min(q_min, model.quality_max)
    
    def patent(self, mol_id, time, firm_id, model):
        """
        为分子申请专利
        
        Args:
            mol_id: 分子ID
            time: 当前时间
            firm_id: 公司ID
            model: 模型实例
        """
        # 如果分子质量过低或已被专利，则返回
        if self.mol[mol_id].q <= 0 or self.mol[mol_id].patent:
            return
        
        # 标记分子为已被专利
        self.mol[mol_id].patent = True
        self.mol[mol_id].patent_firm = firm_id
        self.mol[mol_id].patent_time = time
        self.mol[mol_id].patent_by = firm_id
        self.mol[mol_id].focal = mol_id
        
        # 专利保护范围 - 也保护类似分子
        # 专利宽度确定保护的类似分子数量
        patent_width = model.patent_width
        
        # 向前查找类似分子
        for i in range(1, patent_width + 1):
            target_mol = mol_id - i
            # 确保不越界
            if target_mol >= 0 and target_mol < len(self.mol):
                # 如果该分子有价值且未被专利
                if self.mol[target_mol].q > 0 and not self.mol[target_mol].patent:
                    # 标记为被专利保护
                    self.mol[target_mol].patent = True
                    self.mol[target_mol].patent_firm = firm_id
                    self.mol[target_mol].patent_time = time
                    self.mol[target_mol].patent_by = firm_id
                    self.mol[target_mol].focal = mol_id
        
        # 向后查找类似分子
        for i in range(1, patent_width + 1):
            target_mol = mol_id + i
            # 确保不越界
            if target_mol >= 0 and target_mol < len(self.mol):
                # 如果该分子有价值且未被专利
                if self.mol[target_mol].q > 0 and not self.mol[target_mol].patent:
                    # 标记为被专利保护
                    self.mol[target_mol].patent = True
                    self.mol[target_mol].patent_firm = firm_id
                    self.mol[target_mol].patent_time = time
                    self.mol[target_mol].patent_by = firm_id
                    self.mol[target_mol].focal = mol_id
    
    def patent_time_control(self, time, patent_duration, model):
        """
        检查专利是否过期
        
        Args:
            time: 当前时间
            patent_duration: 专利有效期
            model: 模型实例
        """
        # 检查所有分子的专利状态
        for i in range(len(self.mol)):
            mol = self.mol[i]
            # 如果分子有专利
            if mol.patent:
                # 如果专利已过期
                if time - mol.patent_time >= patent_duration:
                    # 标记专利为已过期
                    mol.patent = False
                    mol.now_free = True 