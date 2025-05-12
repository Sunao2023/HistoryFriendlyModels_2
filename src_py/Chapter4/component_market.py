#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ComponentMarket模块 - ComponentMarket类的Python实现
转换自Java版本的ComponentMarket.java
"""

import math
from src_py.Chapter3.java_compatible_random import JavaCompatibleRandom

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含涉及组件市场的所有参数和变量，以及操作这些变量或调用公司级方法的方法
"""
class ComponentMarket:
    
    def __init__(self, num_of_firms, delta_mod, delta_share, nu, rd_on_prof, 
                 markup, internal_cum, sd_cmp, draw_cost_cmp, start_mod_cmp, 
                 l0, l1, l2, external_mkts, buyers, exit_threshold, 
                 entry_time_cmp_tech, entry_delay_cmp, rng):
        """
        构造函数
        
        Args:
            num_of_firms: 可能在市场上的最大公司数量
            delta_mod: 方程2中的Mod指数，适用于组件 (delta-M_h)
            delta_share: 方程2中的市场份额指数，适用于组件 (delta-s_k)
            nu: 计算从Mod生产成本的比例因子 (nu_k)
            rd_on_prof: 投资于研发的利润比例 (phi-RD)
            markup: 加成 (m)
            internal_cum: 方程14中内部mod的权重 (w-K)
            sd_cmp: 组件技术知识分布的标准差 (sigma-RD_k)
            draw_cost_cmp: 方程13.b中组件技术的绘制成本 (C-RD_k)
            start_mod_cmp: 组件技术mod的初始值 (M-CO_k)
            l0: 方程15.b中组件技术公共知识的基线轨迹 (l-0_k)
            l1: 方程15.b中组件技术公共知识的渐近增长率 (l-1_k)
            l2: 方程15.b中组件技术公共知识的渐近增长率趋近速度 (l-2_k)
            external_mkts: 按组件技术划分的外部市场数量 (G-CO_k)
            buyers: 作为组件产品潜在买家的计算机公司数量
            exit_threshold: 组件公司可以在不向计算机公司销售的最大周期数 (T-E)
            entry_time_cmp_tech: 按组件技术划分的组件公司进入时间 (T_k)
            entry_delay_cmp: 组件技术出现与组件公司进入时间之间的延迟 (T-CO)
            rng: 随机数生成器
        """
        # 参数
        self.delta_mod = delta_mod            # 方程2中的Mod指数，适用于组件 (delta-M_h)
        self.delta_share = delta_share        # 方程2中的市场份额指数，适用于组件 (delta-s_k)
        self.draw_cost = draw_cost_cmp        # 方程13.b中组件技术的绘制成本 (C-RD_k)
        self.entry_delay_cmp = entry_delay_cmp  # 组件技术出现与组件公司进入时间之间的延迟 (T-CO)
        self.entry_time_cmp_tec = entry_time_cmp_tech  # 按组件技术划分的组件公司进入时间 (T_k)
        self.exit_threshold = exit_threshold  # 组件公司可以在不向计算机公司销售的最大周期数 (T-E)
        self.external_mkts = external_mkts    # 按组件技术划分的外部市场数量 (G-CO_k)
        self.internal_cum = internal_cum      # 方程14中内部mod的权重 (w-K)
        self.l0 = l0                          # 方程15.b中组件技术公共知识的基线轨迹 (l-0_k)
        self.l1 = l1                          # 方程15.b中组件技术公共知识的渐近增长率 (l-1_k)
        self.l2 = l2                          # 方程15.b中组件技术公共知识的渐近增长率趋近速度 (l-2_k)
        self.markup = markup                  # 加成 (m)
        self.nu = nu                          # 计算从Mod生产成本的比例因子 (nu_k)
        self.rd_on_prof = rd_on_prof          # 投资于研发的利润比例 (phi-RD)
        self.start_mod_cmp = start_mod_cmp    # 组件技术mod的初始值 (M-CO_k)
        self.sd_cmp = sd_cmp                  # 组件技术知识分布的标准差 (sigma-RD_k)
        
        # 变量
        self.pk = [0.0] * 3                   # 组件技术公共知识 (K-CO_k)
        
        # 技术变量和对象
        self.buyers = buyers                  # 作为组件产品潜在买家的计算机公司数量
        self.num_of_firms = num_of_firms      # 可能在市场上的最大公司数量
        self.rng = rng                        # 随机数生成器
        
        # 统计变量
        self.alive_firms = 0.0                # 市场上活跃的公司数量
        self.herfindahl_index = 0.0           # 赫芬达尔指数
        
        # 创建公司数组 - 增加大小以支持多次模拟
        # 计算每次模拟中可能的最大公司数量：初始公司数 + 2个新技术 * 每次新技术的公司数
        max_firms_per_sim = num_of_firms * 3  # 假设最多是初始公司数的3倍
        # 使用一个更合理的大小，足够支持单次模拟中所有公司
        # Java版本使用了1000，我们也用相似的大小
        from .component_firm import ComponentFirm
        self.firm = [None] * 1000
        
        for i in range(1, num_of_firms + 1):
            self.firm[i] = ComponentFirm(i, 0, start_mod_cmp[0], buyers, self)
    
    def new_entry(self, nf, t_id):
        """
        当新的组件技术出现时生成新的公司群体
        
        Args:
            nf: 新进入的公司数量
            t_id: 组件技术ID
        """
        from .component_firm import ComponentFirm
        
        # 确保有足够的空间容纳新公司
        next_index = self.num_of_firms + 1
        last_index = next_index + nf - 1
        if last_index >= len(self.firm):
            # 如果数组容量不足，则扩容
            new_size = max(len(self.firm) * 2, last_index + 100)
            new_firm = [None] * new_size
            for i in range(len(self.firm)):
                new_firm[i] = self.firm[i]
            self.firm = new_firm
            print(f"警告：组件公司数组已扩容至 {new_size}。这可能意味着模拟中公司数量超出预期。")
        
        for i in range(next_index, last_index + 1):
            self.firm[i] = ComponentFirm(i, t_id, self.start_mod_cmp[t_id], self.buyers, self)
        
        self.num_of_firms += nf
    
    def rating(self):
        """
        通过调用相应的公司级方法计算向计算机公司销售的倾向和概率（在进行当期的研发活动之前）
        """
        sum_rating = 0.0
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].component.calc_prop_to_sell()
                sum_rating += self.firm[f].component.u
        
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].component.calc_prob_to_sell(sum_rating)
    
    def rd_expenditure(self):
        """
        调用控制研发支出的公司级方法
        """
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].rd_expenditure()
    
    def mod_progress(self, time):
        """
        更新所有现有组件技术的公共知识水平，然后调用控制技术进步的公司级方法
        
        Args:
            time: 当前时间
        """
        # 防止时间差值为负或零
        time_diff_0 = time - (self.entry_time_cmp_tec[0] - self.entry_delay_cmp)
        if time_diff_0 <= 0:
            time_diff_0 = 0.1
            
        # 方程15.b - 晶体管技术
        self.pk[0] = self.l0[0] * math.exp(self.l1[0] * time) * (1 - 1 / (self.l2[0] * time_diff_0))
        
        if time > self.entry_time_cmp_tec[1] - self.entry_delay_cmp:
            # 防止时间差值为负或零
            time_diff_1 = time - (self.entry_time_cmp_tec[1] - self.entry_delay_cmp)
            if time_diff_1 <= 0:
                time_diff_1 = 0.1
                
            # 方程15.b - 集成电路技术
            self.pk[1] = self.l0[1] * math.exp(self.l1[1] * time) * (1 - 1 / (self.l2[1] * time_diff_1))
        
        if time > self.entry_time_cmp_tec[2] - self.entry_delay_cmp:
            # 防止时间差值为负或零
            time_diff_2 = time - (self.entry_time_cmp_tec[2] - self.entry_delay_cmp)
            if time_diff_2 <= 0:
                time_diff_2 = 0.1
                
            # 方程15.b - 微处理器技术
            self.pk[2] = self.l0[2] * math.exp(self.l1[2] * time) * (1 - 1 / (self.l2[2] * time_diff_2))
            
        # 确保pk值都不为负或零
        for i in range(3):
            if self.pk[i] <= 0:
                self.pk[i] = 0.0001
        
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].progress()
    
    def external_mkt(self):
        """
        通过调用相应的公司级方法计算向外部市场销售的倾向和概率（在进行当期的研发活动之后），然后计算向这些市场销售的数量
        """
        for k in range(3):
            sum_pts = 0.0
            for f in range(1, self.num_of_firms + 1):
                if self.firm[f].alive and self.firm[f].t_id == k:
                    self.firm[f].component.calc_prop_to_sell_ext()
                    sum_pts += self.firm[f].component.u_ext
            
            for f in range(1, self.num_of_firms + 1):
                if self.firm[f].alive and self.firm[f].t_id == k:
                    self.firm[f].component.calc_prob_to_sell_ext(sum_pts)
            
            external_market = [0] * self.external_mkts[k]
            for g in range(self.external_mkts[k]):
                external_market[g] = 0
                cumulated = 0.0
                random_number = self.rng.random()
                assigned = False
                f = 1
                
                while not assigned and f <= self.num_of_firms:
                    if self.firm[f].alive and self.firm[f].t_id == k:
                        cumulated += self.firm[f].component.U_ext
                        if random_number < cumulated:
                            external_market[g] = self.firm[f].id
                            assigned = True
                    f += 1
            
            for f in range(1, self.num_of_firms + 1):
                if self.firm[f].alive and self.firm[f].t_id == k:
                    count = 0
                    for g in range(self.external_mkts[k]):
                        if external_market[g] == self.firm[f].id:
                            count += 1
                    
                    self.firm[f].calc_external_sold(count)
    
    def accounting(self, mf, pc, pc_entry):
        """
        调用计算数量、利润和市场份额的公司级方法
        
        Args:
            mf: 主机市场对象
            pc: PC市场对象
            pc_entry: PC市场进入控制器
        """
        tot_sold = 0.0
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].accounting(mf, pc, pc_entry)
                tot_sold += self.firm[f].total_sold
        
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].calc_share(tot_sold)
    
    def check_exit(self):
        """
        调用控制退出条件的公司级方法
        """
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].check_exit()
    
    def statistics(self):
        """
        计算有关组件市场的相关统计数据
        """
        self.alive_firms = 0.0
        self.herfindahl_index = 0.0
        
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.alive_firms += 1
        
        if self.alive_firms == 0:
            self.herfindahl_index = 1.0
        else:
            for f in range(1, self.num_of_firms + 1):
                if self.firm[f].alive:
                    self.herfindahl_index += self.firm[f].share ** 2
    
    def choose_firm(self):
        """
        计算机市场用来根据评分选择要用作供应商的组件公司的辅助方法
        
        Returns:
            选定的公司ID
        """
        id_rating = 0
        cumulated = 0.0
        random_number = self.rng.random()
        chosen = False
        f = 1
        
        while not chosen and f <= self.num_of_firms:
            if self.firm[f].alive:
                cumulated += self.firm[f].component.U
                if random_number < cumulated:
                    id_rating = f
                    chosen = True
            f += 1
        
        return id_rating
    
    def size_of_biggest_producer(self):
        """
        计算最大独立组件生产商的规模的辅助方法
        
        Returns:
            最大生产商的销售量
        """
        max_sold = 0.0
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive and self.firm[f].total_sold >= max_sold:
                max_sold = self.firm[f].total_sold
        
        return max_sold
    
    def mod_of_best_producer(self):
        """
        计算最佳独立组件生产商的mod的辅助方法
        
        Returns:
            最佳生产商的mod
        """
        max_mod = 0.0
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive and self.firm[f].component.mod >= max_mod:
                max_mod = self.firm[f].component.mod
        
        return max_mod 