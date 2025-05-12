#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
公司模块 - 定义制药产业模型中的公司
"""

import numpy as np
import random
import math
from .product import Product

class SearchAction:
    """搜索行为类，表示公司寻找新分子的活动"""
    
    def __init__(self):
        """初始化搜索行为"""
        self.budget = 0.0                   # 搜索预算
        self.num_draws = 0                  # 搜索次数
        self.number_draw = 0                # 实际找到的分子数量
        self.perf = 0                       # 表现
        self.count = 0                      # 计数器
        self.bad_perf = 0                   # 不良表现计数
        self.portfolio_tc = []              # 找到的治疗类别ID列表
        self.portfolio_mol = []             # 找到的分子ID列表
    
    def do_search(self, time, prod_count, model):
        """
        执行搜索活动
        
        Args:
            time: 当前时间
            prod_count: 产品数量
            model: 模型实例
        """
        # 清空之前的搜索结果
        self.portfolio_tc = []
        self.portfolio_mol = []
        self.number_draw = 0
        
        # 计算可以进行的搜索次数
        if model.draw_cost > 0:
            self.num_draws = int(self.budget / model.draw_cost)
        else:
            self.num_draws = 10  # 默认搜索次数
        
        # 如果可以搜索
        if self.num_draws > 0:
            # 搜索给定次数
            for i in range(self.num_draws):
                # 随机选择一个治疗类别
                tc_id = model.r.nextInt(model.num_of_tc) + 1
                
                # 在该治疗类别中随机选择一个分子
                mol_id = model.r.nextInt(model.num_of_mol) + 1
                
                # 检查该分子是否有价值且未被专利保护
                if (model.tc[tc_id].mol[mol_id].q > 0 and 
                    not model.tc[tc_id].mol[mol_id].patent):
                    # 记录找到的分子
                    self.portfolio_tc.append(tc_id)
                    self.portfolio_mol.append(mol_id)
                    self.number_draw += 1
                    self.bad_perf = 0  # 重置不良表现计数
                else:
                    # 增加不良表现计数
                    self.bad_perf += 1

class Memory:
    """记忆类，存储公司的研发记忆"""
    
    def __init__(self, end_time):
        """
        初始化记忆
        
        Args:
            end_time: 模拟结束时间
        """
        self.tc = []                        # 治疗类别ID列表
        self.mol = []                       # 分子ID列表
        self.molecules_found = 0            # 找到的分子数量
        self.mem_of_tc = []                 # 记忆中的治疗类别ID
        self.mem_of_mol = []                # 记忆中的分子ID
        self.on = []                        # 是否正在研发的标志
        self.value = []                     # 分子价值
        
    def record_memory(self, mol_list, tc_list, count, model):
        """
        记录找到的分子
        
        Args:
            mol_list: 分子ID列表
            tc_list: 治疗类别ID列表
            count: 分子数量
            model: 模型实例
        """
        # 记录找到的分子
        for i in range(count):
            self.tc.append(tc_list[i])
            self.mol.append(mol_list[i])
            self.mem_of_tc.append(tc_list[i])
            self.mem_of_mol.append(mol_list[i])
            self.molecules_found += 1
            
            # 记录分子的值和研发状态
            tc_id = tc_list[i]
            mol_id = mol_list[i]
            
            # 分子价值（治疗类别的市场价值乘以分子质量）
            mol_value = model.tc[tc_id].value * model.tc[tc_id].mol[mol_id].q / 100.0
            self.value.append(mol_value)
            
            # 初始未研发状态
            self.on.append(0)
    
    def record_memory_imi(self, model):
        """
        记录仿制药的分子
        
        Args:
            model: 模型实例
        """
        # 遍历所有治疗类别，寻找可仿制的分子
        for tc_id in range(1, model.num_of_tc + 1):
            # 遍历该治疗类别中的所有分子
            for mol_id in range(1, model.num_of_mol + 1):
                # 检查分子是否有价值
                if model.tc[tc_id].mol[mol_id].q > 0:
                    # 检查是否已经专利过期但仍有价值
                    if (model.tc[tc_id].mol[mol_id].patent and 
                        model.tc[tc_id].mol[mol_id].patent_expired):
                        
                        # 记录这个分子用于仿制
                        self.mem_of_tc.append(tc_id)
                        self.mem_of_mol.append(mol_id)
                        
                        # 分子价值（治疗类别的市场价值乘以分子质量，乘以0.8因为是仿制药）
                        mol_value = model.tc[tc_id].value * model.tc[tc_id].mol[mol_id].q * 0.8 / 100.0
                        self.value.append(mol_value)
                        
                        # 初始未研发状态
                        self.on.append(0)

class Firm:
    """公司类，表示制药产业中的公司"""
    
    def __init__(self, initial_budget, mkting_share, rd_share, search_share, 
                 num_tc, is_innovator, innovator_tendency, model):
        """
        初始化公司
        
        Args:
            initial_budget: 初始预算
            mkting_share: 营销预算比例
            rd_share: 研发预算比例
            search_share: 搜索预算比例
            num_tc: 治疗类别数量
            is_innovator: 是否为创新型公司
            innovator_tendency: 创新倾向
            model: 模型实例
        """
        # 公司基本特性
        self.budget = initial_budget        # 公司预算
        self.mkting_budget = 0.0            # 营销预算
        self.rd_budget = 0.0                # 研发预算
        self.mkting_share = mkting_share    # 营销预算比例
        self.rd_share = rd_share            # 研发预算比例
        self.search_share = search_share    # 搜索预算比例（研发预算中）
        self.innovator = is_innovator       # 是否为创新型公司
        self.innovatort = False             # 当前时期是否选择创新
        self.imin = innovator_tendency      # 创新倾向
        
        # 业绩统计
        self.sh_tc = [0.0] * (num_tc + 1)   # 各治疗类别市场份额
        self.sh_ta1 = [0.0] * (num_tc + 1)  # 各治疗类别市场份额（替代计算）
        self.tot_share = [0.0] * (model.end_time + 1)  # 总市场份额
        self.tot_share_quantity = [0.0] * (model.end_time + 1)  # 总市场份额（按数量）
        self.tot_profit = 0.0               # 总利润
        self.total_reached_patients = 0.0   # 总服务患者数
        
        # 产品和研发
        self.num_of_products = model.num_of_products_init  # 产品数量
        self.prod = [None] * (self.num_of_products + 1)    # 产品列表
        self.tot_prod = 0                   # 总产品数
        self.cost_of_inno = model.cost_of_research_inn  # 创新成本
        self.cost_of_imi = model.cost_of_research_imi   # 仿制成本
        
        # 研发管理
        self.on_pro_inno = Memory(model.end_time)  # 创新记忆
        self.on_pro_imi = Memory(model.end_time)   # 仿制记忆
        self.search_action = SearchAction()  # 搜索行为
        
        # 状态标志
        self.alive = True                   # 公司是否存活
        self.on_mkt = False                 # 是否已进入市场
        
        # 计数器
        self.num_inno = 0                   # 创新产品数量
        self.num_imi = 0                    # 仿制产品数量
        
        # 治疗类别跟踪
        self.ntc_f = num_tc                 # 公司可覆盖的治疗类别数量
        self.tc_f = [0] * (num_tc + 1)      # 每个治疗类别产品数量
        self.counter_ta = [0] * (num_tc + 1)  # 每个治疗类别的计数器
        self.tot_tc = 0                     # 公司涉及的治疗类别总数
    
    def choose_im_in(self, model):
        """
        选择是否进行创新
        
        Args:
            model: 模型实例
            
        Returns:
            bool: 是否选择创新
        """
        # 随机决定是否进行创新
        if model.r.random() < self.imin:
            return True
        else:
            return False
    
    def calc_imi_inno(self, time):
        """
        计算仿制和创新产品数量
        
        Args:
            time: 当前时间
        """
        self.num_inno = 0
        self.num_imi = 0
        
        # 遍历公司的所有产品
        for i in range(1, self.num_of_products + 1):
            if i < len(self.prod) and self.prod[i] is not None and not self.prod[i].out:
                if self.prod[i].imitative:
                    self.num_imi += 1
                else:
                    self.num_inno += 1
    
    def search(self, time, search_type, cost, model):
        """
        分配预算到搜索活动
        
        Args:
            time: 当前时间
            search_type: 搜索类型（"inno"或"imi"）
            cost: 搜索成本
            model: 模型实例
        """
        # 计算研发预算
        self.rd_budget = self.budget * self.rd_share
        
        # 计算搜索预算
        search_budget = self.rd_budget * self.search_share
        
        # 设置搜索预算
        self.search_action.budget = search_budget
    
    def research(self, time, model):
        """
        执行研发活动
        
        Args:
            time: 当前时间
            model: 模型实例
        """
        # 研发实现
        pass
    
    def proj_mkting(self):
        """
        规划营销投入
        """
        # 计算营销预算
        self.mkting_budget = self.budget * self.mkting_share
    
    def mkting(self):
        """
        执行营销活动
        """
        # 如果没有产品，则不进行营销
        if self.tot_prod <= 0:
            return
        
        # 计算每个产品的营销投入
        mkting_per_product = self.mkting_budget / self.tot_prod
        
        # 分配营销投入到各产品
        for i in range(1, self.num_of_products + 1):
            if i < len(self.prod) and self.prod[i] is not None and not self.prod[i].out:
                self.prod[i].mkting = mkting_per_product
    
    def failure(self, model):
        """
        公司失败/退出市场
        
        Args:
            model: 模型实例
        """
        # 标记公司为不存活
        self.alive = False
        
        # 标记所有产品为退出市场
        for i in range(1, self.num_of_products + 1):
            if i < len(self.prod) and self.prod[i] is not None:
                self.prod[i].out = True
    
    def products_out(self, out_pro_limit, model):
        """
        检查产品是否应退出市场
        
        Args:
            out_pro_limit: 退出市场的市场份额阈值
            model: 模型实例
        """
        # 遍历所有产品
        for i in range(1, self.num_of_products + 1):
            if i < len(self.prod) and self.prod[i] is not None and not self.prod[i].out:
                # 获取产品所在治疗类别
                tc_id = self.prod[i].tc
                if tc_id < len(model.tc) and model.tc[tc_id] is not None:
                    # 计算产品在治疗类别中的市场份额
                    share = self.prod[i].num_patients / model.tc[tc_id].value
                    
                    # 如果市场份额低于阈值，则退出市场
                    if share < out_pro_limit:
                        self.prod[i].out = True
    
    def num_projects(self, is_inno, speed):
        """
        计算可以同时进行的项目数量
        
        Args:
            is_inno: 是否为创新项目
            speed: 开发速度
            
        Returns:
            int: 可同时进行的项目数量
        """
        # 计算剩余可用于研发的预算（已扣除搜索预算）
        rd_budget_for_development = self.rd_budget * (1 - self.search_share)
        
        # 确定项目成本
        if is_inno:
            project_cost = self.cost_of_inno
        else:
            project_cost = self.cost_of_imi
        
        # 计算可同时进行的项目数量
        if project_cost > 0:
            # 每个开发周期的成本 = 项目成本 / 开发速度
            cost_per_cycle = project_cost / speed
            
            # 可同时进行的项目数量 = 研发预算 / 每个开发周期的成本
            num_projects = int(rd_budget_for_development / cost_per_cycle)
            return max(0, num_projects)
        else:
            return 0

    def num_of_ta(self):
        """计算公司涉及的治疗类别数量"""
        # 重置计数器
        self.tot_tc = 0
        for i in range(self.ntc_f + 1):
            self.counter_ta[i] = 0
            self.tc_f[i] = 0
        
        # 计算每个治疗类别的产品数量
        for i in range(1, self.num_of_products + 1):
            if i < len(self.prod) and self.prod[i] is not None and not self.prod[i].out:
                tc_id = self.prod[i].tc
                if tc_id < len(self.tc_f):
                    self.tc_f[tc_id] += 1
                    self.counter_ta[tc_id] += 1
        
        # 计算公司涉及的治疗类别总数
        for i in range(self.ntc_f + 1):
            if self.counter_ta[i] > 0:
                self.tot_tc += 1
    
    def accounting(self):
        """
        Allocate budget to different activities (marketing, research).
        """
        # Calculate budget for different activities
        if self.alive:
            # Allocate budget to marketing and research based on firm strategy
            self.budget_m = self.budget * self.mkting_budget
            self.budget_res = self.budget * self.search_research
            
            # Reset expenditure counters
            self.search_expenditure = 0
            self.research_expenditure = 0 
    
    def proj_mkting(self):
        """
        Plan marketing investments.
        Allocates marketing budget across therapeutic categories where the firm has products.
        """
        # Only active firms with budget can plan marketing
        if not self.alive or self.budget <= 0:
            return
        
        # Calculate marketing budget
        self.budget_m = self.budget * self.mkting_budget
        
        # Calculate the number of TCs where the firm is active
        self.num_of_ta()
        
        # Allocate marketing budget per TC
        if self.tot_tc > 0:
            self.v_tot_ta_mkting = self.budget_m / self.tot_tc
        else:
            self.v_tot_ta_mkting = 0.0
    
    def mkting(self):
        """
        Execute marketing strategies.
        Invests in marketing for products based on their therapeutic category.
        """
        # Only active firms can invest in marketing
        if not self.alive:
            return
        
        # For each product, apply marketing investment
        for i in range(1, self.num_of_products + 1):
            if i < len(self.prod) and self.prod[i] is not None and not self.prod[i].out:
                # Increase marketing investment by the TC allocation
                self.prod[i].m += self.v_tot_ta_mkting
                
                # Ensure non-zero marketing
                if self.prod[i].m <= 0:
                    self.prod[i].m = 1.0
        
        # Update firm status
        if self.num_of_products > 0:
            self.on_mkt = True 

    def select_mol(self, ta_counts, idx, memory):
        """
        从记忆中选择一个分子进行研发
        
        Args:
            ta_counts: 每个治疗类别已选择的分子数量
            idx: 当前考虑的分子索引
            memory: 记忆对象（创新或仿制）
            
        Returns:
            int: 选择的分子索引，如果没找到合适的分子则返回-1
        """
        # Check if index is valid
        if idx < 0 or idx >= len(memory.mem_of_tc):
            return -1
            
        # 获取要研究的治疗类别
        tc_id = memory.mem_of_tc[idx]
        
        # Check if TC index is valid
        if tc_id < 0 or tc_id >= len(ta_counts):
            return idx  # Return original index if TC is out of range
        
        # 如果该治疗类别已经有多个分子被研究，尝试选择其他类别
        if ta_counts[tc_id] > 2:
            # 寻找其他符合条件的分子
            best_idx = -1
            best_value = 0.0
            
            for i in range(len(memory.mem_of_tc)):
                # Skip invalid indices
                if i < 0 or i >= len(memory.on) or memory.on[i] != 0:
                    continue
                    
                # Get therapeutic category
                alt_tc = memory.mem_of_tc[i]
                
                # Skip invalid TC values
                if alt_tc < 0 or alt_tc >= len(ta_counts):
                    continue
                    
                if ta_counts[alt_tc] <= 2:  # 该类别研发数量少
                    # Skip invalid value indices
                    if i >= len(memory.value):
                        continue
                        
                    if memory.value[i] > best_value:
                        best_value = memory.value[i]
                        best_idx = i
            
            # 如果找到了更好的选择，返回它
            if best_idx != -1:
                return best_idx
        
        # 如果没有更好的选择或原选择已经符合条件，返回原索引
        return idx 