#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ComputerFirm模块 - ComputerFirm类的Python实现
转换自Java版本的ComputerFirm.java
"""

import math

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含定义计算机市场中公司异质性的所有变量以及操作这些变量的方法。计算机公司可以是垂直整合的或专业化的。
"""
class ComputerFirm:
    
    def __init__(self, id, pc, start_share, spillover, mod_sys, computer_market):
        """
        构造函数
        
        Args:
            id: 公司标识符
            pc: 如果是PC公司则为True，否则为False
            start_share: 初始市场份额
            spillover: 垂直整合公司中系统研发向组件研发的溢出
            mod_sys: 系统元素的初始设计优点值
            computer_market: 计算机市场对象引用
        """
        # 变量
        self.born = True              # 公司第一次出现时置为"True"，当首次选择供应商后设为"False"
        self.component_rd = 0.0       # 投资于组件研发的资源量 (B-CO_f,t)
        self.contract_d = 0           # 合同持续时间 (T-CO_f,t)
        self.contract_time = 0        # 签订合同的时间 (t_f)
        self.exit_share = start_share # 移动平均市场份额 (SE_f,t)
        self.int_time = 0             # 公司处于整合状态的周期数 (t-I_f)
        self.integrated = False       # 如果公司是垂直整合的则为"True"，否则为"False"
        self.num_of_draws_cmp = 0     # 公司绘制的新潜在组件mod数量 (N-CO_f,t)
        self.num_of_draws_sys = 0     # 公司绘制的新潜在系统mod数量 (N-SY_f,t)
        self.price = 0.0              # 计算机公司收取的单位价格 (P_f,t)
        self.prob_to_int = 0.0        # 公司整合的概率 (Pr(I_f,t))
        self.prob_to_spec = 0.0       # 公司专业化的概率 (Pr(S_f,t))
        self.profit = 0.0             # 公司赚取的利润量 (PI_f,t)
        self.prop_to_int = 0.0        # 公司整合的倾向 (PI_f,t)
        self.prop_to_spec = 0.0       # 公司专业化的倾向 (PS_f,t)
        self.q_sold = 0.0             # 销售的计算机数量 (q_f,t)
        self.share = start_share      # 公司的市场份额 (s_f,t)
        self.supplier_id = -1         # 公司供应商的标识符 (f_f,t)
        self.system_rd = 0.0          # 投资于系统研发的资源量 (B-SY_f,t)
        
        # 技术变量和对象
        self.id = id                  # 公司标识符
        self.t_id = 0                 # 计算机公司使用的组件技术标识符
        self.alive = True             # 如果公司活跃于市场则为"True"，否则为"False"
        self.pc = pc                  # 如果是PC公司则为"True"，否则为"False"
        self.spillover = spillover    # 垂直整合公司中系统研发向组件研发的溢出
        
        # 关联对象
        from .computer import Computer
        from .component import Component
        from .system_element import SystemElement
        
        self.computer = Computer()    # 公司生产的计算机
        self.component = Component(0, self)  # 对于整合公司，公司生产的组件
        self.system = SystemElement(mod_sys, self)  # 公司生产的系统元素
        self.computer_market = computer_market       # 访问计算机市场
        
    def rd_expenditure(self):
        """
        计算研发支出的方法，包括用于系统和组件研发的资源分配
        """
        # 计算总研发支出
        rd = self.computer_market.rd_on_prof * self.profit
        
        if self.integrated:
            # 方程12，垂直整合公司在系统和组件研发之间分配资源
            self.system_rd = rd / (1 + self.spillover)
            self.component_rd = rd - self.system_rd
        else:
            # 非集成企业，所有研发资源分配给系统开发
            self.system_rd = rd
            self.component_rd = 0.0
    
    def progress(self):
        """
        确定公司创新活动的结果
        """
        # 计算可能的创新次数 (方程13)
        temp_num_of_draws = self.system_rd / self.computer_market.draw_cost_sys
        self.num_of_draws_sys = int(temp_num_of_draws)
        remain = temp_num_of_draws - self.num_of_draws_sys
        
        # 处理剩余部分
        random_number = self.computer_market.rng.random()
        if random_number <= remain:
            self.num_of_draws_sys += 1
            
        # 如果公司是垂直整合的，也要计算组件创新
        if self.integrated:
            temp_num_of_draws = self.component_rd / self.computer_market.draw_cost_cmp
            self.num_of_draws_cmp = int(temp_num_of_draws)
            remain = temp_num_of_draws - self.num_of_draws_cmp
            
            random_number = self.computer_market.rng.random()
            if random_number <= remain:
                self.num_of_draws_cmp += 1
        
        # 更新系统元素的mod
        # 计算当前的mu_prog (方程14.a)
        self.system.mu_prog = ((1 - self.computer_market.internal_cum) * 
                             self.computer_market.pk_sys + 
                             self.computer_market.internal_cum * self.system.mod)
        
        z_max = 0.0
        for i in range(1, self.num_of_draws_sys + 1):
            # 从正态分布中抽取
            z = self.system.mu_prog + self.computer_market.sd_sys * self.computer_market.rng.nextGaussian()
            if z > z_max:
                z_max = z
                
        if z_max > self.system.mod:
            self.system.mod = z_max
            
        # 如果公司是垂直整合的，还要更新组件mod
        if self.integrated:
            # 计算当前的组件mu_prog (方程14.b)
            self.component.mu_prog = ((1 - self.computer_market.internal_cum) * 
                                   self.computer_market.pk_cmp[self.t_id] + 
                                   self.computer_market.internal_cum * self.component.mod)
            
            z_max = 0.0
            for i in range(1, self.num_of_draws_cmp + 1):
                # 从正态分布中抽取
                z = self.component.mu_prog + self.computer_market.sd_cmp * self.computer_market.rng.nextGaussian()
                if z > z_max:
                    z_max = z
                    
            if z_max > self.component.mod:
                self.component.mod = z_max
                
            # 更新组件生产成本 (方程11)
            if self.component.mod > 0:
                self.component.production_cost = self.computer_market.nu_cmp / self.component.mod
                
        # 计算整合和专业化的概率
        if self.integrated:
            # 方程16
            tech_age = self.computer_market.t_id_cmp - self.t_id
            
            if tech_age > 0:
                # 计算专业化倾向 (方程16)
                self.prop_to_spec = (self.computer_market.chi0 * 
                                    (tech_age ** self.computer_market.chi1) * 
                                    (self.share ** self.computer_market.chi2))
                
                # 方程17.b
                self.prob_to_spec = 1 - math.exp(-self.computer_market.xi_spec * self.prop_to_spec)
            else:
                self.prop_to_spec = 0.0
                self.prob_to_spec = 0.0
        else:
            # 计算整合倾向 (方程16)
            self.prop_to_int = self.share ** self.computer_market.chi2
            
            # 方程17.a
            self.prob_to_int = 1 - math.exp(-self.computer_market.xi_int * self.prop_to_int)
            
        # 更新计算机产品特性和价格
        if self.integrated:
            # 方程8，9，10
            self.calculate_computer_features_integrated()
        else:
            # 供应商组件特性影响计算机特性
            self.calculate_computer_features_specialized()
            
        # 计算价格 (方程7)
        self.price = self.computer.production_cost * (1 + self.computer_market.markup)
        
    def calculate_computer_features_integrated(self):
        """
        为垂直整合的公司计算计算机特性
        """
        import math
        # 计算性能和低成本性 (方程8，9)
        self.computer.perf = self.system.mod ** (1 - self.computer_market.tau) * self.component.mod ** self.computer_market.tau
        self.computer.cheap = 1 / (self.component.production_cost ** self.computer_market.tau)
        
        # 计算计算机mod (方程10)
        theta_radians = self.computer_market.theta * math.pi / 180.0
        self.computer.mod = self.computer_market.phi * (self.computer.perf * math.cos(theta_radians) + 
                                                     self.computer.cheap * math.sin(theta_radians)) ** self.computer_market.rho
        
        # 计算计算机生产成本 (方程11)
        self.computer.production_cost = self.computer_market.nu_computer / self.computer.cheap
        
    def calculate_computer_features_specialized(self):
        """
        为专业化公司计算计算机特性
        """
        import math
        # 如果有供应商
        if self.supplier_id != -1:
            # 获取供应商组件的mod和生产成本
            component_firm = self.computer_market.model.component.firm[self.supplier_id]
            supplier_mod = component_firm.component.mod
            supplier_cost = component_firm.component.production_cost
            
            # 计算性能和低成本性 (方程8，9)
            self.computer.perf = self.system.mod ** (1 - self.computer_market.tau) * supplier_mod ** self.computer_market.tau
            self.computer.cheap = 1 / (supplier_cost ** self.computer_market.tau)
            
            # 计算计算机mod (方程10)
            theta_radians = self.computer_market.theta * math.pi / 180.0
            self.computer.mod = self.computer_market.phi * (self.computer.perf * math.cos(theta_radians) + 
                                                        self.computer.cheap * math.sin(theta_radians)) ** self.computer_market.rho
            
            # 计算计算机生产成本 (方程11)
            self.computer.production_cost = self.computer_market.nu_computer / self.computer.cheap
        
    def accounting(self):
        """
        更新公司的销售和利润账户
        """
        # 方程6
        self.profit = self.q_sold * self.computer.production_cost * self.computer_market.markup
        
    def calc_share(self, q_market):
        """
        计算公司的市场份额
        
        Args:
            q_market: 市场总销售量
        """
        if q_market > 0:
            self.share = self.q_sold / q_market
        else:
            self.share = 0.0
            
    def check_exit(self):
        """
        检查是否仍然满足留在行业的条件
        """
        # 方程20
        self.exit_share = self.computer_market.weight_exit * self.share + (1 - self.computer_market.weight_exit) * self.exit_share
        
        random_number = self.computer_market.rng.random()
        if self.exit_share < self.computer_market.exit_threshold and random_number < 0.5:
            self.exit_firm()
            
    def exit_firm(self):
        """
        退出时激活的方法：将公司活动控制器切换为"False"并重置公司和产品层面的最相关变量
        """
        self.alive = False
        self.born = False
        self.component_rd = 0.0
        self.exit_share = 0.0
        self.num_of_draws_cmp = 0
        self.num_of_draws_sys = 0
        self.price = 0.0
        self.profit = 0.0
        self.prop_to_int = 0.0
        self.prop_to_spec = 0.0
        self.q_sold = 0.0
        self.share = 0.0
        self.system_rd = 0.0
        
        # 如果是专业化公司，通知供应商取消合同
        if not self.integrated and self.supplier_id != -1 and self.computer_market.model:
            component_firm = self.computer_market.model.component.firm[self.supplier_id]
            component_firm.cancel_contract(self.id)
            self.supplier_id = -1
            
        # 重置产品层面变量
        self.computer.cheap = 0.0
        self.computer.mod = 0.0
        self.computer.perf = 0.0
        self.computer.production_cost = 0.0
        self.computer.u = 0.0
        self.computer.U = 0.0
        
        self.system.mod = 0.0
        self.system.mu_prog = 0.0
        
        if self.integrated:
            self.component.mod = 0.0
            self.component.production_cost = 0.0
            self.component.mu_prog = 0.0 