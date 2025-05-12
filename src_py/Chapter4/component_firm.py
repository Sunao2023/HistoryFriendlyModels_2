#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ComponentFirm模块 - ComponentFirm类的Python实现
转换自Java版本的ComponentFirm.java
"""

import math

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含定义组件市场中公司异质性的所有变量以及操作这些变量的方法
"""
class ComponentFirm:
    
    def __init__(self, id, t_id, mod, num_of_potential_buyers, cmp_market):
        """
        构造函数
        
        Args:
            id: 公司标识符
            t_id: 组件技术标识符。0=晶体管技术；1=集成电路技术；2=微处理器技术
            mod: 组件初始设计优点值
            num_of_potential_buyers: 潜在购买者数量
            cmp_market: 组件市场对象引用
        """
        # 变量
        self.component_rd = 0.0     # 投资于研发的资源量 (B-CO_f,t)
        self.count_no_sales = 0.0   # 公司连续不向计算机生产商销售的周期数 (T-E_f,t)
        self.num_of_draws_cmp = 0   # 公司绘制的新潜在组件mod数量 (N-CO_f,t)
        self.price = 0.0            # 组件公司收取的单位价格 (P_f,t)
        self.profit = 0.0           # 公司赚取的利润量 (PI_f,t)
        self.share = 0.0            # 公司的市场份额 (s_f,t)
        self.total_sold = 0.0       # 销售的组件数量 (q_f,h,t; q_f,t)
        
        # 技术变量和对象
        self.id = id                # 公司标识符
        self.t_id = t_id            # 组件技术标识符
        self.alive = True           # 如果公司活跃于市场则为"True"，否则为"False"
        self.external_sold = 0.0    # 在外部市场上销售的组件数量
        self.how_many_buyers_mf = 0 # 从组件公司购买的主机公司数量
        self.how_many_buyers_pc = 0 # 从组件公司购买的PC公司数量
        self.q_sold = 0.0           # 销售给计算机公司的组件数量
        self.buyer_id = [0] * (num_of_potential_buyers + 1)  # 标识可能从组件公司购买的计算机公司
        
        # 关联对象
        from .sold_component import SoldComponent
        self.component = SoldComponent(mod, self)  # 公司生产的组件
        self.cmp_market = cmp_market               # 访问组件市场 
        
    def rd_expenditure(self):
        """
        计算研发支出的方法
        """
        self.component_rd = self.cmp_market.rd_on_prof * self.profit
    
    def progress(self):
        """
        控制创新过程的公司级方法
        首先，计算计算可能创新的次数
        然后，从知识分布中随机提取，并根据提取值可能更新mod
        最后，更新组件生产成本
        """
        # 临时变量是组件RD与绘制成本的比率
        # 计算可能的创新次数（方程13.b）
        # 确保draw_cost不为零
        draw_cost = self.cmp_market.draw_cost[self.t_id]
        if draw_cost <= 0:
            draw_cost = 0.0001
            
        temp_num_of_draws = self.component_rd / draw_cost
        self.num_of_draws_cmp = int(temp_num_of_draws)
        remain = temp_num_of_draws - self.num_of_draws_cmp
        
        # 对于剩余部分，使用概率来决定是否增加一次创新次数
        random_number = self.cmp_market.rng.random()
        if random_number <= remain:
            self.num_of_draws_cmp += 1
        
        # 计算当前的mu_prog（方程14.b）
        # 确保公共知识和内部知识不为零
        pk_val = self.cmp_market.pk[self.t_id]
        if pk_val <= 0:
            pk_val = 0.0001
        
        internal_mod = self.component.mod
        if internal_mod <= 0:
            internal_mod = 0.0001
            
        self.component.mu_prog = ((1 - self.cmp_market.internal_cum) * pk_val + 
                                self.cmp_market.internal_cum * internal_mod)
        
        # 从分布中提取并找到最大值（方程14.b）
        z_max = 0.0
        for i in range(self.num_of_draws_cmp):
            # 使用nextGaussian()方法确保与Java版本一致的随机数
            z = self.component.mu_prog + self.cmp_market.sd_cmp[self.t_id] * self.cmp_market.rng.nextGaussian()
            if z > z_max:
                z_max = z
        
        # 如果新的mod值更大，则更新
        if z_max > self.component.mod:
            self.component.mod = z_max
        
        # 确保mod值不为零，防止后续除零错误
        if self.component.mod <= 0:
            self.component.mod = 0.0001
            
        # 更新组件生产成本（方程11）
        self.component.production_cost = self.cmp_market.nu / self.component.mod
        
        # 更新价格（方程7）
        self.price = self.component.production_cost * (1 + self.cmp_market.markup)
    
    def calc_external_sold(self, num_of_ext_mkts):
        """
        计算外部市场销售量的方法
        
        Args:
            num_of_ext_mkts: 外部市场数量
        """
        # 方程5（适用于组件）
        self.external_sold = num_of_ext_mkts * self.component.mod
    
    def accounting(self, mf, pc, pc_entry):
        """
        更新公司的销售和利润账户
        
        Args:
            mf: 主机市场对象
            pc: PC市场对象
            pc_entry: PC市场进入控制器
        """
        self.q_sold = 0.0
        self.total_sold = 0.0
        self.how_many_buyers_mf = 0
        
        for f in range(1, mf.num_of_firms + 1):
            if self.buyer_id[f] == 1:
                self.q_sold += mf.firm[f].q_sold * mf.num_of_comp
                self.how_many_buyers_mf += 1
        
        if pc_entry:
            self.how_many_buyers_pc = 0
            for f in range(mf.num_of_firms + 1, mf.num_of_firms + pc.num_of_firms + 1):
                if self.buyer_id[f] == 1:
                    self.q_sold += pc.firm[f - mf.num_of_firms].q_sold * pc.num_of_comp
                    self.how_many_buyers_pc += 1
        
        self.total_sold = self.q_sold + self.external_sold
        # 方程6（适用于组件）
        self.profit = self.total_sold * self.component.production_cost * self.cmp_market.markup
    
    def calc_share(self, tot_sold):
        """
        计算公司的市场份额
        
        Args:
            tot_sold: 市场总销售量
        """
        if tot_sold != 0:
            self.share = self.total_sold / tot_sold
        else:
            self.share = 0
    
    def check_exit(self):
        """
        检查是否仍然满足留在行业的条件
        """
        random_number = self.cmp_market.rng.random()
        
        if self.q_sold == 0:
            self.count_no_sales += 1
        else:
            self.count_no_sales = 0
        
        # 方程21
        exit_prob = (self.count_no_sales / self.cmp_market.exit_threshold) ** 2
        if exit_prob > random_number:
            self.exit_firm()
    
    def exit_firm(self):
        """
        退出时激活的方法：将公司活动控制器切换为"False"并重置公司和产品层面的最相关变量
        """
        self.alive = False
        self.count_no_sales = 0
        self.component_rd = 0.0
        self.external_sold = 0.0
        self.profit = 0.0
        self.price = 0.0
        self.q_sold = 0.0
        self.share = 0.0
        self.total_sold = 0.0
        self.how_many_buyers_mf = 0
        self.how_many_buyers_pc = 0
        self.num_of_draws_cmp = 0
        
        for i in range(len(self.buyer_id)):
            self.buyer_id[i] = 0
        
        self.component.exit_component()
    
    def sign_contract(self, id):
        """
        签订新合同时更新买家列表
        
        Args:
            id: 买家公司ID
        """
        self.buyer_id[id] = 1
    
    def cancel_contract(self, id):
        """
        合同到期时更新买家列表
        
        Args:
            id: 买家公司ID
        """
        self.buyer_id[id] = 0 