#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ComputerMarket模块 - ComputerMarket类的Python实现
转换自Java版本的ComputerMarket.java
"""

import math
from .java_compatible_random import JavaCompatibleRandom

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含涉及计算机市场（主机和PC）的所有参数和变量，以及操作这些变量或调用公司级方法的方法
"""
class ComputerMarket:
    
    def __init__(self, id, num_of_firm, buyers, delta_mod, delta_share,
                 nu_computer, nu_cmp, pc, rd_on_prof, markup, start_share,
                 spillover, num_of_comp, rho, tau, phi, mod_sys, internal_cum,
                 min_length_contr, range_length_contr, xi_int, chi1, chi2,
                 chi0, xi_spec, min_int_time, inheritance, entry_time_cmp,
                 limit_sys_mod, entry_delay_sys, entry_delay_cmp, theta,
                 gamma, sd_sys, sd_cmp, l0_cmp, l1_cmp, l2_cmp, l0_sys,
                 l1_sys, l2_sys, draw_cost_sys, draw_cost_cmp, entry_time_sys_tec,
                 weight_exit, exit_threshold, rng, model=None):
        """
        构造函数
        
        Args:
            id: 计算机市场标识符："MAINFRAMES"或"PC"
            num_of_firm: 可能在市场上的最大公司数量
            buyers: 潜在买家组数 (G_h)
            delta_mod: 方程2中的Mod指数 (delta-M_h)
            delta_share: 方程2中的市场份额指数 (delta-s_kappa)
            nu_computer: 计算从便宜性计算计算机生产成本的比例因子 (nu_kappa)
            nu_cmp: 计算从Mod计算组件生产成本的比例因子 (nu_k)
            pc: 是否为PC市场
            rd_on_prof: 投资于研发的利润比例 (phi-RD)
            markup: 加成 (m)
            start_share: 初始市场份额
            spillover: 集成公司中系统研发向组件研发的溢出 (PSI-CO)
            num_of_comp: 每台计算机所需的组件数量
            rho: 方程1中与弹性相关的参数 (rho_kappa)
            tau: 方程1中组件的权重 (tau_kapp)
            phi: 方程1中的比例参数 (PHI_kappa)
            mod_sys: 系统元素的初始设计优点值
            internal_cum: 方程14中内部mod的权重 (w-K)
            min_length_contr: 与组件供应商签订合同的最短持续时间 (T-CO_f,t)
            range_length_contr: 与组件供应商签订合同的持续时间范围 (T-CO_f,t)
            xi_int: 方程17中的整合参数 (xi-I)
            chi1: （整合）方程16中技术年龄的指数 (chi-1)
            chi2: （整合）方程16中规模的指数 (chi-2)
            chi0: （整合）方程16中技术年龄的乘数 (chi-0)
            xi_spec: 方程17中的专业化参数 (xi-S)
            min_int_time: 整合的最短持续时间 (T-I)
            inheritance: 向垂直整合转移的公司继承的最后一个供应商mod的比例 (phi-I)
            entry_time_cmp: 按组件技术划分的组件公司进入时间 (T_k)
            limit_sys_mod: 系统mod技术限制 (LAMBDA-SY_k)
            entry_delay_sys: 组件技术出现与组件公司进入时间之间的延迟 (T-CO)
            entry_delay_cmp: 系统技术出现与计算机公司进入时间之间的延迟 (T-SY)
            theta: 定义技术轨迹的角度 (theta_kappa)
            gamma: 确定感知mod的便宜性指数 (gamma_h)
            sd_sys: 系统技术知识分布的标准差 (sigma-RD_kappa)
            sd_cmp: 组件技术知识分布的标准差 (sigma-RD_k)
            l0_cmp: 方程15.b中组件技术公共知识的基线轨迹 (l-0_k)
            l1_cmp: 方程15.b中组件技术公共知识的渐近增长率 (l-1_k)
            l2_cmp: 方程15.b中组件技术公共知识的渐近增长率趋近速度 (l-2_k)
            l0_sys: 方程15.a中系统技术公共知识的基线轨迹 (l-0_kappa)
            l1_sys: 方程15.a中系统技术公共知识的渐近增长率 (l-1_kappa)
            l2_sys: 方程15.a中系统技术公共知识的渐近增长率趋近速度 (l-2_kappa)
            draw_cost_sys: 方程13.a中系统技术的绘制成本 (C-RD_kappa)
            draw_cost_cmp: 方程13.b中组件技术的绘制成本 (C-RD_k)
            entry_time_sys_tec: 按系统技术划分的计算机公司进入时间 (T_kappa)
            weight_exit: 退出决策中当前市场份额的权重 (w-E)
            exit_threshold: 计算机公司的退出阈值 (lambda-E)
            rng: 随机数生成器
            model: 整体模型对象引用，用于访问组件市场
        """
        # 参数
        self.buyers = buyers                  # 潜在买家组数 (G_h)
        self.chi0 = chi0                      # （整合）方程16中技术年龄的乘数 (chi-0)
        self.chi1 = chi1                      # （整合）方程16中技术年龄的指数 (chi-1)
        self.chi2 = chi2                      # （整合）方程16中规模的指数 (chi-2)
        self.gamma = gamma                    # 确定感知mod的便宜性指数 (gamma_h)
        self.delta_mod = delta_mod            # 方程2中的Mod指数 (delta-M_h)
        self.delta_share = delta_share        # 方程2中的市场份额指数 (delta-s_kappa)
        self.draw_cost_cmp = draw_cost_cmp    # 方程13.b中组件技术的绘制成本 (C-RD_k)
        self.draw_cost_sys = draw_cost_sys    # 方程13.a中系统技术的绘制成本 (C-RD_kappa)
        self.entry_delay_sys = entry_delay_sys  # 组件技术出现与组件公司进入时间之间的延迟 (T-CO)
        self.entry_delay_cmp = entry_delay_cmp  # 系统技术出现与计算机公司进入时间之间的延迟 (T-SY)
        self.entry_time_cmp_tec = entry_time_cmp  # 按组件技术划分的组件公司进入时间 (T_k)
        self.entry_time_sys_tec = entry_time_sys_tec  # 按系统技术划分的计算机公司进入时间 (T_kappa)
        self.exit_threshold = exit_threshold  # 计算机公司的退出阈值 (lambda-E)
        self.inheritance = inheritance        # 向垂直整合转移的公司继承的最后一个供应商mod的比例 (phi-I)
        self.internal_cum = internal_cum      # 方程14中内部mod的权重 (w-K)
        self.l0_cmp = l0_cmp                  # 方程15.b中组件技术公共知识的基线轨迹 (l-0_k)
        self.l1_cmp = l1_cmp                  # 方程15.b中组件技术公共知识的渐近增长率 (l-1_k)
        self.l2_cmp = l2_cmp                  # 方程15.b中组件技术公共知识的渐近增长率趋近速度 (l-2_k)
        self.l0_sys = l0_sys                  # 方程15.a中系统技术公共知识的基线轨迹 (l-0_kappa)
        self.l1_sys = l1_sys                  # 方程15.a中系统技术公共知识的渐近增长率 (l-1_kappa)
        self.l2_sys = l2_sys                  # 方程15.a中系统技术公共知识的渐近增长率趋近速度 (l-2_kappa)
        self.limit_sys_mod = limit_sys_mod    # 系统mod技术限制 (LAMBDA-SY_k)
        self.markup = markup                  # 加成 (m)
        self.min_int_time = min_int_time      # 整合的最短持续时间 (T-I)
        self.min_length_contr = min_length_contr  # 与组件供应商签订合同的最短持续时间 (T-CO_f,t)
        self.nu_cmp = nu_cmp                  # 计算从Mod计算组件生产成本的比例因子 (nu_k)
        self.nu_computer = nu_computer        # 计算从便宜性计算计算机生产成本的比例因子 (nu_kappa)
        self.num_of_comp = num_of_comp        # 每台计算机所需的组件数量
        self.phi = phi                        # 方程1中的比例参数 (PHI_kappa)
        self.range_length_contr = range_length_contr  # 与组件供应商签订合同的持续时间范围 (T-CO_f,t)
        self.rd_on_prof = rd_on_prof          # 投资于研发的利润比例 (phi-RD)
        self.rho = rho                        # 方程1中与弹性相关的参数 (rho_kappa)
        self.tau = tau                        # 方程1中组件的权重 (tau_kapp)
        self.theta = theta                    # 定义技术轨迹的角度 (theta_kappa)
        self.sd_cmp = sd_cmp                  # 组件技术知识分布的标准差 (sigma-RD_k)
        self.sd_sys = sd_sys                  # 系统技术知识分布的标准差 (sigma-RD_kappa)
        self.weight_exit = weight_exit        # 退出决策中当前市场份额的权重 (w-E)
        self.xi_int = xi_int                  # 方程17中的整合参数 (xi-I)
        self.xi_spec = xi_spec                # 方程17中的专业化参数 (xi-S)
        
        # 变量
        self.pk_sys = 0.0                     # 系统技术公共知识 (K-SY_kappa)
        self.pk_cmp = [0.0] * 3               # 组件技术公共知识 (K-CO_k)
        
        # 技术变量和对象
        self.id = id                          # 计算机市场标识符："MAINFRAMES"或"PC"
        self.num_of_firms = num_of_firm       # 可能在市场上的最大公司数量
        self.t_id_cmp = 0                     # 当前主流组件技术的标识符
        self.rng = rng                        # 随机数生成器
        self.model = model                    # 整体模型对象引用
        
        # 统计变量
        self.alive_firms = 0.0                # 市场上活跃的公司数量
        self.herfindahl_index = 0.0           # 赫芬达尔指数
        self.int_firms = 0.0                  # 市场上活跃的集成公司数量
        self.int_ratio = 0.0                  # 集成比例
        
        # 创建公司数组
        from .computer_firm import ComputerFirm
        # 使用一个更合理的大小，足够支持单次模拟中所有公司
        # Java版本使用了1000，我们也用相似的大小
        self.firm = [None] * 1000
        
        for i in range(1, num_of_firm + 1):
            self.firm[i] = ComputerFirm(i, pc, start_share, spillover, mod_sys, self)
            
    def set_model(self, model):
        """
        设置模型引用，在初始化后调用
        
        Args:
            model: 整体模型对象引用
        """
        self.model = model
    
    def ensure_capacity(self, required_size):
        """
        确保firm数组有足够的容量
        
        Args:
            required_size: 需要的最小容量
        """
        if required_size >= len(self.firm):
            # 如果数组容量不足，则扩容
            new_size = max(len(self.firm) * 2, required_size + 100)
            new_firm = [None] * new_size
            for i in range(len(self.firm)):
                new_firm[i] = self.firm[i]
            self.firm = new_firm
            print(f"警告：计算机公司数组已扩容至 {new_size}。这可能意味着模拟中公司数量超出预期。")
    
    def rd_expenditure(self):
        """
        调用控制研发支出的公司级方法
        """
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].rd_expenditure()
    
    def mod_progress(self, time):
        """
        更新系统和组件技术的公共知识水平，然后调用控制技术进步的公司级方法
        
        Args:
            time: 当前时间
        """
        # 系统技术的公共知识（方程15.a）
        self.pk_sys = self.l0_sys * math.exp(self.l1_sys * time) * (1 - 1 / (self.l2_sys * time))
        
        # 如果系统技术公共知识超过技术限制，则限制其值
        if self.pk_sys > self.limit_sys_mod[self.t_id_cmp]:
            self.pk_sys = self.limit_sys_mod[self.t_id_cmp]
        
        # 晶体管技术的公共知识（方程15.b）
        self.pk_cmp[0] = self.l0_cmp[0] * math.exp(self.l1_cmp[0] * time) * \
                        (1 - 1 / (self.l2_cmp[0] * (time - (self.entry_time_cmp_tec[0] - self.entry_delay_cmp))))
        
        # 如果集成电路技术已经出现
        if time > self.entry_time_cmp_tec[1] - self.entry_delay_cmp:
            # 集成电路技术的公共知识（方程15.b）
            self.pk_cmp[1] = self.l0_cmp[1] * math.exp(self.l1_cmp[1] * time) * \
                            (1 - 1 / (self.l2_cmp[1] * (time - (self.entry_time_cmp_tec[1] - self.entry_delay_cmp))))
        
        # 如果微处理器技术已经出现
        if time > self.entry_time_cmp_tec[2] - self.entry_delay_cmp:
            # 微处理器技术的公共知识（方程15.b）
            self.pk_cmp[2] = self.l0_cmp[2] * math.exp(self.l1_cmp[2] * time) * \
                            (1 - 1 / (self.l2_cmp[2] * (time - (self.entry_time_cmp_tec[2] - self.entry_delay_cmp))))
        
        # 对所有活跃的公司执行技术进步
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].progress()
                
        # 检查整合和专业化的转型
        self.check_int()
        self.check_spec()
    
    def rating(self):
        """
        对所有计算机产品计算用户类h的倾向和概率
        """
        # 为每组买家计算权重
        for h in range(1, self.buyers + 1):
            sum_rating = 0.0
            for f in range(1, self.num_of_firms + 1):
                if self.firm[f].alive:
                    # 方程1（与性能和成本相关的mod）
                    self.firm[f].computer.mod_for_cust = (self.firm[f].computer.perf ** (1 - self.gamma)) * \
                                                      (self.firm[f].computer.cheap ** self.gamma)
                    
                    # 方程2（对客户的销售倾向）
                    self.firm[f].computer.u = (self.firm[f].computer.mod_for_cust ** self.delta_mod) * \
                                           ((1 + self.firm[f].share) ** self.delta_share)
                    
                    sum_rating += self.firm[f].computer.u
            
            # 对每个公司计算销售给该买家组的概率（方程3）
            for f in range(1, self.num_of_firms + 1):
                if self.firm[f].alive:
                    if sum_rating > 0:
                        self.firm[f].computer.U = self.firm[f].computer.u / sum_rating
                    else:
                        self.firm[f].computer.U = 0.0
    
    def demand(self):
        """
        为市场上的计算机公司分配买家
        """
        # 重置销售数量
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].q_sold = 0.0
        
        # 为每组买家分配供应商
        for h in range(1, self.buyers + 1):
            cumulated = 0.0
            random_number = self.rng.random()
            assigned = False
            f = 1
            
            # 寻找供应商（方程4）
            while not assigned and f <= self.num_of_firms:
                if self.firm[f].alive:
                    cumulated += self.firm[f].computer.U
                    if random_number < cumulated:
                        self.firm[f].q_sold += 1.0
                        assigned = True
                f += 1
    
    def accounting(self):
        """
        调用计算利润的公司级方法并更新市场份额
        """
        # 计算市场总销售量
        q_tot = 0.0
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                q_tot += self.firm[f].q_sold
        
        # 为每个公司计算利润和市场份额
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].accounting()
                self.firm[f].calc_share(q_tot)
    
    def check_exit(self, component_market, firm_offset):
        """
        调用控制退出条件的公司级方法
        
        Args:
            component_market: 组件市场对象
            firm_offset: 公司ID偏移量
        """
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                # 方程20（退出倾向的更新）
                self.firm[f].exit_share = (self.weight_exit * self.firm[f].share + 
                                          (1 - self.weight_exit) * self.firm[f].exit_share)
                
                # 检查退出条件
                random_number = self.rng.random()
                if self.firm[f].exit_share < self.exit_threshold and random_number < 0.5:
                    # 如果公司是专业化的且有供应商，通知供应商取消合同
                    if not self.firm[f].integrated and self.firm[f].supplier_id != -1:
                        component_market.firm[self.firm[f].supplier_id].cancel_contract(f + firm_offset)
                    
                    # 重置公司和产品层面变量
                    self.firm[f].alive = False
                    self.firm[f].born = False
                    self.firm[f].component_rd = 0.0
                    self.firm[f].exit_share = 0.0
                    self.firm[f].num_of_draws_cmp = 0
                    self.firm[f].num_of_draws_sys = 0
                    self.firm[f].price = 0.0
                    self.firm[f].profit = 0.0
                    self.firm[f].prop_to_int = 0.0
                    self.firm[f].prop_to_spec = 0.0
                    self.firm[f].q_sold = 0.0
                    self.firm[f].share = 0.0
                    self.firm[f].system_rd = 0.0
                    self.firm[f].supplier_id = -1
                    
                    # 重置产品层面变量
                    self.firm[f].computer.cheap = 0.0
                    self.firm[f].computer.mod = 0.0
                    self.firm[f].computer.perf = 0.0
                    self.firm[f].computer.production_cost = 0.0
                    self.firm[f].computer.u = 0.0
                    self.firm[f].computer.U = 0.0
                    
                    self.firm[f].system.mod = 0.0
                    self.firm[f].system.mu_prog = 0.0
                    
                    if self.firm[f].integrated:
                        self.firm[f].component.mod = 0.0
                        self.firm[f].component.production_cost = 0.0
                        self.firm[f].component.mu_prog = 0.0
    
    def check_int(self):
        """
        检查非整合公司是否决定整合
        """
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive and not self.firm[f].integrated:
                random_number = self.rng.random()
                
                # 如果随机数小于整合概率（方程17.a），则公司整合
                if random_number < self.firm[f].prob_to_int:
                    # 执行整合转型
                    self.firm[f].integrated = True
                    self.firm[f].int_time = 0
                    
                    # 继承供应商的组件mod（如果有供应商）
                    if self.firm[f].supplier_id != -1 and self.model:
                        # 通知供应商取消合同
                        component_firm = self.model.component.firm[self.firm[f].supplier_id]
                        component_firm.cancel_contract(self.firm[f].id)
                        
                        # 继承部分供应商mod
                        self.firm[f].component.mod = self.inheritance * component_firm.component.mod
                        
                        # 更新组件生产成本（方程11）
                        if self.firm[f].component.mod > 0:
                            self.firm[f].component.production_cost = self.nu_cmp / self.firm[f].component.mod
                        
                        self.firm[f].supplier_id = -1
    
    def check_spec(self):
        """
        检查整合公司是否决定专业化
        """
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive and self.firm[f].integrated:
                # 检查公司已经整合的时间是否超过最短整合时间
                if self.firm[f].int_time > self.min_int_time:
                    random_number = self.rng.random()
                    
                    # 如果随机数小于专业化概率（方程17.b），则公司专业化
                    if random_number < self.firm[f].prob_to_spec:
                        self.firm[f].integrated = False
                        self.firm[f].int_time = 0
                else:
                    # 增加整合时间计数器
                    self.firm[f].int_time += 1
    
    def statistics(self, end_time):
        """
        计算有关计算机市场的相关统计数据
        
        Args:
            end_time: 模拟的结束时间
        """
        self.alive_firms = 0.0
        self.int_firms = 0.0
        self.herfindahl_index = 0.0
        
        # 计数市场上的活跃公司和集成公司
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.alive_firms += 1
                if self.firm[f].integrated:
                    self.int_firms += 1
        
        # 计算集成率
        if self.alive_firms > 0:
            self.int_ratio = self.int_firms / self.alive_firms
        else:
            self.int_ratio = 0.0
        
        # 计算赫芬达尔指数
        if self.alive_firms == 0:
            self.herfindahl_index = 1.0
        else:
            for f in range(1, self.num_of_firms + 1):
                if self.firm[f].alive:
                    self.herfindahl_index += self.firm[f].share ** 2
    
    def check_supplier(self, time):
        """
        检查是否需要为计算机公司选择新供应商
        
        Args:
            time: 当前时间
        """
        # 确保模型已设置
        if not self.model:
            return
            
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive and not self.firm[f].integrated:
                # 如果尚未选择供应商或者当前合同已经到期
                if self.firm[f].supplier_id == -1 or time >= self.firm[f].contract_time + self.firm[f].contract_d:
                    # 选择新供应商
                    new_supplier = self.model.component.choose_firm()
                    
                    if new_supplier > 0:
                        # 如果有之前的供应商，通知取消合同
                        if self.firm[f].supplier_id != -1:
                            component_firm = self.model.component.firm[self.firm[f].supplier_id]
                            component_firm.cancel_contract(self.firm[f].id)
                        
                        # 更新供应商和合同信息
                        self.firm[f].supplier_id = new_supplier
                        self.firm[f].t_id = self.model.component.firm[new_supplier].t_id
                        self.firm[f].contract_time = time
                        
                        # 随机确定合同持续时间
                        self.firm[f].contract_d = self.min_length_contr + \
                                                int(self.rng.random() * self.range_length_contr)
                        
                        # 通知新供应商
                        self.model.component.firm[new_supplier].sign_contract(self.firm[f].id)
                        
                        # 如果是首次选择供应商，标记为非新生公司
                        if self.firm[f].born:
                            self.firm[f].born = False
    
    def contract_engine(self, component_market, time, firm_offset):
        """
        检查计算机公司与组件供应商之间的合同
        
        Args:
            component_market: 组件市场对象
            time: 当前时间
            firm_offset: 公司ID偏移量
        """
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive and not self.firm[f].integrated:
                # 如果尚未选择供应商或者当前合同已经到期
                if self.firm[f].supplier_id == -1 or time >= self.firm[f].contract_time + self.firm[f].contract_d:
                    # 选择新供应商
                    new_supplier = component_market.choose_firm()
                    
                    if new_supplier > 0:
                        # 如果有之前的供应商，通知取消合同
                        if self.firm[f].supplier_id != -1:
                            component_market.firm[self.firm[f].supplier_id].cancel_contract(f + firm_offset)
                        
                        # 更新供应商和合同信息
                        self.firm[f].supplier_id = new_supplier
                        self.firm[f].t_id = component_market.firm[new_supplier].t_id
                        self.firm[f].contract_time = time
                        
                        # 随机确定合同持续时间
                        self.firm[f].contract_d = self.min_length_contr + \
                                                int(self.rng.random() * self.range_length_contr)
                        
                        # 通知新供应商
                        component_market.firm[new_supplier].sign_contract(f + firm_offset)
                        
                        # 如果是首次选择供应商，标记为非新生公司
                        if self.firm[f].born:
                            self.firm[f].born = False
                            
    def change_cmp_technology(self, t_id):
        """
        更新当前主流组件技术
        
        Args:
            t_id: 新的组件技术ID
        """
        self.t_id_cmp = t_id
        
    def mod_component_progress(self, time, component_market):
        """
        处理垂直整合公司中组件的技术进步
        
        Args:
            time: 当前时间
            component_market: 组件市场对象
        """
        # 更新组件技术的公共知识
        # 晶体管技术的公共知识（方程15.b）
        self.pk_cmp[0] = self.l0_cmp[0] * math.exp(self.l1_cmp[0] * time) * \
                       (1 - 1 / (self.l2_cmp[0] * (time - (self.entry_time_cmp_tec[0] - self.entry_delay_cmp))))
        
        # 如果集成电路技术已经出现
        if time > self.entry_time_cmp_tec[1] - self.entry_delay_cmp:
            # 集成电路技术的公共知识（方程15.b）
            self.pk_cmp[1] = self.l0_cmp[1] * math.exp(self.l1_cmp[1] * time) * \
                           (1 - 1 / (self.l2_cmp[1] * (time - (self.entry_time_cmp_tec[1] - self.entry_delay_cmp))))
        
        # 如果微处理器技术已经出现
        if time > self.entry_time_cmp_tec[2] - self.entry_delay_cmp:
            # 微处理器技术的公共知识（方程15.b）
            self.pk_cmp[2] = self.l0_cmp[2] * math.exp(self.l1_cmp[2] * time) * \
                           (1 - 1 / (self.l2_cmp[2] * (time - (self.entry_time_cmp_tec[2] - self.entry_delay_cmp))))
        
        # 对所有垂直整合的公司执行组件技术进步
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive and self.firm[f].integrated:
                # 计算可能的创新次数（方程13.b）
                temp_num_of_draws = self.firm[f].component_rd / self.draw_cost_cmp[self.firm[f].t_id]
                self.firm[f].num_of_draws_cmp = int(temp_num_of_draws)
                remain = temp_num_of_draws - self.firm[f].num_of_draws_cmp
                
                # 处理剩余部分
                random_number = self.rng.random()
                if random_number <= remain:
                    self.firm[f].num_of_draws_cmp += 1
                
                # 计算当前的组件mu_prog（方程14.b）
                self.firm[f].component.mu_prog = ((1 - self.internal_cum) * 
                                                component_market.pk[self.firm[f].t_id] + 
                                                self.internal_cum * self.firm[f].component.mod)
                
                # 从正态分布中抽取可能的创新
                z_max = 0.0
                for i in range(1, self.firm[f].num_of_draws_cmp + 1):
                    z = self.firm[f].component.mu_prog + self.sd_cmp[self.firm[f].t_id] * self.rng.gauss(0, 1)
                    if z > z_max:
                        z_max = z
                
                # 如果新的mod值更大，则更新
                if z_max > self.firm[f].component.mod:
                    self.firm[f].component.mod = z_max
                
                # 更新组件生产成本（方程11）
                if self.firm[f].component.mod > 0:
                    self.firm[f].component.production_cost = self.nu_cmp / self.firm[f].component.mod
                    
                # 计算整合和专业化的概率
                # 计算技术年龄
                tech_age = self.t_id_cmp - self.firm[f].t_id
                
                if tech_age > 0:
                    # 计算专业化倾向（方程16）
                    self.firm[f].prop_to_spec = (self.chi0 * 
                                                (tech_age ** self.chi1) * 
                                                (self.firm[f].share ** self.chi2))
                    
                    # 计算专业化概率（方程17.b）
                    self.firm[f].prob_to_spec = 1 - math.exp(-self.xi_spec * self.firm[f].prop_to_spec)
                else:
                    self.firm[f].prop_to_spec = 0.0
                    self.firm[f].prob_to_spec = 0.0
    
    def mod_system_progress(self, time):
        """
        处理系统元素的技术进步
        
        Args:
            time: 当前时间
        """
        # 更新系统技术的公共知识（方程15.a）
        self.pk_sys = self.l0_sys * math.exp(self.l1_sys * time) * (1 - 1 / (self.l2_sys * time))
        
        # 如果系统技术公共知识超过技术限制，则限制其值
        if self.pk_sys > self.limit_sys_mod[self.t_id_cmp]:
            self.pk_sys = self.limit_sys_mod[self.t_id_cmp]
        
        # 确保公共知识不为零或负值
        if self.pk_sys <= 0:
            self.pk_sys = 0.0001
            
        # 对所有活跃的公司执行系统技术进步
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                # 计算可能的创新次数（方程13.a）
                temp_num_of_draws = self.firm[f].system_rd / self.draw_cost_sys
                self.firm[f].num_of_draws_sys = int(temp_num_of_draws)
                remain = temp_num_of_draws - self.firm[f].num_of_draws_sys
                
                # 处理剩余部分
                random_number = self.rng.random()
                if random_number <= remain:
                    self.firm[f].num_of_draws_sys += 1
                
                # 计算当前的系统mu_prog（方程14.a）
                # 确保内部mod值不为零
                internal_mod = self.firm[f].system.mod
                if internal_mod <= 0:
                    internal_mod = 0.0001
                    
                self.firm[f].system.mu_prog = ((1 - self.internal_cum) * self.pk_sys + 
                                            self.internal_cum * internal_mod)
                
                # 从正态分布中抽取可能的创新
                z_max = 0.0
                for i in range(1, self.firm[f].num_of_draws_sys + 1):
                    z = self.firm[f].system.mu_prog + self.sd_sys * self.rng.gauss(0, 1)
                    if z > z_max:
                        z_max = z
                
                # 如果新的mod值更大，则更新
                if z_max > self.firm[f].system.mod:
                    self.firm[f].system.mod = z_max
                    
                # 确保system.mod不为零
                if self.firm[f].system.mod <= 0:
                    self.firm[f].system.mod = 0.0001
                    
                # 如果公司不是垂直整合的，计算整合倾向和概率
                if not self.firm[f].integrated:
                    # 计算整合倾向（方程16）
                    self.firm[f].prop_to_int = self.firm[f].share ** self.chi2
                    
                    # 计算整合概率（方程17.a）
                    self.firm[f].prob_to_int = 1 - math.exp(-self.xi_int * self.firm[f].prop_to_int)
    
    def computer_mod_cost_price(self):
        """
        更新计算机的mod、成本和价格
        """
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                if self.firm[f].integrated:
                    # 计算性能和低成本性（方程8，9）
                    # 确保system.mod和component.mod不为零，防止负幂运算出错
                    if self.firm[f].system.mod <= 0:
                        self.firm[f].system.mod = 0.0001
                    if self.firm[f].component.mod <= 0:
                        self.firm[f].component.mod = 0.0001
                    
                    self.firm[f].computer.perf = (self.firm[f].system.mod ** (1 - self.tau)) * \
                                               (self.firm[f].component.mod ** self.tau)
                    
                    # 确保component.production_cost不为零，防止除零错误
                    if self.firm[f].component.production_cost <= 0:
                        self.firm[f].component.production_cost = 0.0001
                        
                    self.firm[f].computer.cheap = 1 / (self.firm[f].component.production_cost ** self.tau)
                else:
                    if self.firm[f].supplier_id != -1 and self.model:
                        try:
                            # 获取供应商组件的mod和生产成本
                            component_firm = self.model.component.firm[self.firm[f].supplier_id]
                            supplier_mod = component_firm.component.mod
                            supplier_cost = component_firm.component.production_cost
                            
                            # 确保system.mod和supplier_mod不为零，防止负幂运算出错
                            if self.firm[f].system.mod <= 0:
                                self.firm[f].system.mod = 0.0001
                            if supplier_mod <= 0:
                                supplier_mod = 0.0001
                            
                            # 计算性能和低成本性（方程8，9）
                            self.firm[f].computer.perf = (self.firm[f].system.mod ** (1 - self.tau)) * \
                                                      (supplier_mod ** self.tau)
                            
                            # 确保supplier_cost不为零，防止除零错误
                            if supplier_cost <= 0:
                                supplier_cost = 0.0001
                                
                            self.firm[f].computer.cheap = 1 / (supplier_cost ** self.tau)
                        except (AttributeError, IndexError):
                            # 如果模型或组件市场未正确设置，使用默认值
                            if self.firm[f].system.mod <= 0:
                                self.firm[f].system.mod = 0.0001
                            self.firm[f].computer.perf = self.firm[f].system.mod ** (1 - self.tau)
                            self.firm[f].computer.cheap = 1.0
                
                # 确保perf和cheap不为零
                if self.firm[f].computer.perf <= 0:
                    self.firm[f].computer.perf = 0.0001
                if self.firm[f].computer.cheap <= 0:
                    self.firm[f].computer.cheap = 0.0001
                    
                # 计算计算机mod（方程10）
                theta_radians = self.theta * math.pi / 180.0
                self.firm[f].computer.mod = self.phi * ((self.firm[f].computer.perf * math.cos(theta_radians)) + 
                                                     (self.firm[f].computer.cheap * math.sin(theta_radians))) ** self.rho
                
                # 计算计算机生产成本（方程11）
                if self.firm[f].computer.cheap <= 0:
                    # 防止除零错误，设置一个安全的小值
                    self.firm[f].computer.cheap = 0.0001
                self.firm[f].computer.production_cost = self.nu_computer / self.firm[f].computer.cheap
                
                # 计算价格（方程7）
                self.firm[f].price = self.firm[f].computer.production_cost * (1 + self.markup)
                
    def prob_of_selling(self):
        """
        计算所有计算机产品销售给用户类h的倾向和概率
        """
        # 为每组买家计算
        for h in range(1, self.buyers + 1):
            sum_rating = 0.0
            
            # 计算每个公司的销售倾向
            for f in range(1, self.num_of_firms + 1):
                if self.firm[f].alive:
                    # 确保perf和cheap不为零，防止负幂运算出错
                    if self.firm[f].computer.perf <= 0:
                        self.firm[f].computer.perf = 0.0001
                    if self.firm[f].computer.cheap <= 0:
                        self.firm[f].computer.cheap = 0.0001
                    
                    # 方程1（与性能和成本相关的mod）
                    self.firm[f].computer.mod_for_cust = ((self.firm[f].computer.perf ** (1 - self.gamma)) * 
                                                        (self.firm[f].computer.cheap ** self.gamma))
                    
                    # 确保mod_for_cust和share不导致负幂问题
                    if self.firm[f].computer.mod_for_cust <= 0:
                        self.firm[f].computer.mod_for_cust = 0.0001
                    
                    # 方程2（对客户的销售倾向）
                    self.firm[f].computer.u = ((self.firm[f].computer.mod_for_cust ** self.delta_mod) * 
                                             ((1 + self.firm[f].share) ** self.delta_share))
                    
                    sum_rating += self.firm[f].computer.u
            
            # 计算每个公司的销售概率
            for f in range(1, self.num_of_firms + 1):
                if self.firm[f].alive:
                    if sum_rating > 0:
                        # 方程4（销售概率）
                        self.firm[f].computer.U = self.firm[f].computer.u / sum_rating
                    else:
                        self.firm[f].computer.U = 0.0
                        
    def accounting(self, time):
        """
        调用计算利润的公司级方法并更新市场份额
        
        Args:
            time: 当前时间
        """
        # 重置销售数量
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                self.firm[f].q_sold = 0.0
        
        # 为每组买家分配供应商
        for h in range(1, self.buyers + 1):
            cumulated = 0.0
            random_number = self.rng.random()
            assigned = False
            f = 1
            
            # 寻找供应商（方程4）
            while not assigned and f <= self.num_of_firms:
                if self.firm[f].alive:
                    cumulated += self.firm[f].computer.U
                    if random_number < cumulated:
                        self.firm[f].q_sold += 1.0
                        assigned = True
                f += 1
                
        # 计算市场总销售量
        q_tot = 0.0
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                q_tot += self.firm[f].q_sold
        
        # 为每个公司计算利润和市场份额
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                # 方程6（计算利润）
                self.firm[f].profit = self.firm[f].q_sold * self.firm[f].computer.production_cost * self.markup
                
                if q_tot > 0:
                    self.firm[f].share = self.firm[f].q_sold / q_tot
                else:
                    self.firm[f].share = 0.0
                    
        # 检查整合和专业化的转型
        self.check_int()
        self.check_spec()
        
        # 为垂直整合的公司更新整合时间
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive and self.firm[f].integrated:
                self.firm[f].int_time += 1
                
    def check_exit(self, component_market, firm_offset):
        """
        调用控制退出条件的公司级方法
        
        Args:
            component_market: 组件市场对象
            firm_offset: 公司ID偏移量
        """
        for f in range(1, self.num_of_firms + 1):
            if self.firm[f].alive:
                # 方程20（退出倾向的更新）
                self.firm[f].exit_share = (self.weight_exit * self.firm[f].share + 
                                          (1 - self.weight_exit) * self.firm[f].exit_share)
                
                # 检查退出条件
                random_number = self.rng.random()
                if self.firm[f].exit_share < self.exit_threshold and random_number < 0.5:
                    # 如果公司是专业化的且有供应商，通知供应商取消合同
                    if not self.firm[f].integrated and self.firm[f].supplier_id != -1:
                        component_market.firm[self.firm[f].supplier_id].cancel_contract(f + firm_offset)
                    
                    # 重置公司和产品层面变量
                    self.firm[f].alive = False
                    self.firm[f].born = False
                    self.firm[f].component_rd = 0.0
                    self.firm[f].exit_share = 0.0
                    self.firm[f].num_of_draws_cmp = 0
                    self.firm[f].num_of_draws_sys = 0
                    self.firm[f].price = 0.0
                    self.firm[f].profit = 0.0
                    self.firm[f].prop_to_int = 0.0
                    self.firm[f].prop_to_spec = 0.0
                    self.firm[f].q_sold = 0.0
                    self.firm[f].share = 0.0
                    self.firm[f].system_rd = 0.0
                    self.firm[f].supplier_id = -1
                    
                    # 重置产品层面变量
                    self.firm[f].computer.cheap = 0.0
                    self.firm[f].computer.mod = 0.0
                    self.firm[f].computer.perf = 0.0
                    self.firm[f].computer.production_cost = 0.0
                    self.firm[f].computer.u = 0.0
                    self.firm[f].computer.U = 0.0
                    
                    self.firm[f].system.mod = 0.0
                    self.firm[f].system.mu_prog = 0.0 