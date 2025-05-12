#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C5Model模块 - C5Model类的Python实现
模拟制药产业的历史友好模型
"""

import os
import random
import math
import numpy as np
from datetime import datetime
from .molecule import Molecule
from .therapeutic_category import TherapeuticCategory
from .product import Product
from .firm import Firm
from .files import Files
from .statistic import Statistic

# Use absolute import for JavaCompatibleRandom
try:
    from src_py.Chapter3.java_compatible_random import JavaCompatibleRandom
except ImportError:
    import sys
    import os
    # Add fallback path if needed
    src_py_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chapter3_dir = os.path.join(src_py_dir, 'Chapter3')
    if chapter3_dir not in sys.path:
        sys.path.append(chapter3_dir)
    from java_compatible_random import JavaCompatibleRandom

import time

class C5Model:
    """
    药物产业模型的主类。
    这个类实现了第5章的药物产业模型。
    """
    
    def __init__(self):
        """
        构造函数，初始化模型参数和目录
        """
        # 获取项目根目录
        current_file_path = os.path.abspath(__file__)  # 当前文件的绝对路径
        src_py_dir = os.path.dirname(os.path.dirname(current_file_path))  # src_py目录
        self.root_dir = os.path.dirname(src_py_dir)  # 项目根目录
        
        # 设置正确的参数文件路径和结果目录
        self.path_parameters = os.path.join(self.root_dir, "parameters", "Chapter5")
        self.path_results = os.path.join(self.root_dir, "results_py", "Chapter5")
        
        # 确保结果目录存在
        os.makedirs(self.path_results, exist_ok=True)
        
        # 初始化模型参数
        self.seed = 1000
        self.end_time = 50  # 默认值，会被参数文件覆盖
        self.num_of_tc = 200  # 治疗类别数量
        self.num_of_firm = 50  # 公司数量
        self.num_of_mol = 400  # 每个治疗类别的分子数量
        self.mt = 10  # 多次模拟的迭代次数
        
        # 初始化随机数生成器
        random.seed(self.seed)
        np.random.seed(self.seed)
        
        # Initialize static variables and parameters
        self.get_params()
        
        # Initialize helper classes
        self.file = Files()
        self.st = Statistic()
        # Initialize statistics arrays
        self.st.create_array(self.end_time, self.num_of_tc, self.num_of_firm)
        
        # Initialize model components
        self.tc = None  # Therapeutic Categories array
        self.f = None   # Firms array
        
        # 使用与Java相同的种子值初始化随机数生成器
        seed = 13  # 默认种子值
        self.rng_seed = seed
        self.r = JavaCompatibleRandom(seed)
        self.rand = JavaCompatibleRandom(seed)
        # 同步Python内置随机数生成器
        random.seed(seed)
        np.random.seed(seed)
        
    def get_params(self):
        """Set default parameters for the model"""
        # Multiple simulations
        self.mt = 2
        # Periods of simulation
        self.end_time = 100
        # Number of potential firms
        self.num_of_firm = 50
        # Probability of drawing a zero-quality molecule
        self.q_mol_null = 0.97
        # Unit cost of search
        self.draw_cost = 20
        # Unit cost of production
        self.cost_prod = 1
        # Unit cost of development of innovative drugs
        self.cost_of_research_inn = 60
        # Unit cost of development of imitative drugs
        self.cost_of_research_imi = 20
        # Periods to develop a drug
        self.time_develop = 24
        # Speed of development of an innovative drug
        self.speed_development_inno = 3
        # Speed of development of an imitative drug
        self.speed_development_imi = 6
        # Patent duration
        self.patent_duration = 20
        # Patent width
        self.patent_width = 5
        # Minimum quality threshold of the drugs to be sold on the market
        self.quality_check = 30
        # Interest rate
        self.interest_rate = 0.08
        # Indicator of market leaders power
        self.omega = 0.5
        # Perceived price elasticity of demand
        self.elasticity = 1.5
        # Erosion rate of product image
        self.erosion = 0.01
        # Minimum market share threshold for survival of a firm in the market
        self.e_failure = 0.004
        # Minimum market share threshold for survival of a product in the market
        self.out_pro_limit = 0.05
        # Periods without drawing a promising molecule after which an innovative firm exits
        self.search_failure = 7

        # Therapeutic Classes, Molecules and Drugs Characteristics
        # Number of TCs
        self.num_of_tc = 200
        # Number of molecules in TC
        self.num_of_mol = 400
        # Mean of normal distribution of the number of patients per TC
        self.tc_patients_cost = 600
        # Standard deviation of normal distribution of the number of patients per TC
        self.tc_patients_rand = 200
        # Number of groups of patients in TC that might buy drug
        self.num_of_sub_mkt = 4

        # Economic value of a TC
        # Weight of product quality for TC in Equation 9
        self.a_value_cost = 0.5
        self.a_value_rand = 0.1
        # Weight of inverse of price for TC in Equation 9
        self.b_value_cost = 0.15
        self.b_value_rand = 0.05
        # Weight of product image for TC in Equation 9
        self.c_value_cost = 0.35
        self.c_value_rand = 0.05
        # Mean of normal distribution of positive quality molecules
        self.q_mol_cost = 30
        # Standard deviation of normal distribution of positive quality molecules
        self.q_mol_var = 20

        # Firm characteristics
        # Fraction of budget invested in R&D activities by firm
        self.min_rd = 0.25
        self.add_rd = 0.5
        # Fraction of budget invested in search activities by firm
        self.min_s = 0.1
        self.add_s = 0.05
        # Initial budget of a potential firm
        self.b = 4500
        
        # OTHER PARAMETERS
        self.cost_of_search = 0
        self.acc_mkting = 30
        self.quality_max = 90
        self.quota_invested_in_search = 0.1
        self.alfa_cumulativeness = 1
        self.alfa_cumulativeness_exp = 0  # Not used in original Java code
             
        # SWITCHES
        # Probability of finding new promising molecules is positively 
        # affected by previous (successful) research efforts when dwaw1=true                                          
        self.draw1 = False

        # Initial allocation for products per firm
        self.num_of_products_init = 10

    def make_single_simulation(self):
        """
        执行单次模拟
        """
        print(f"Starting single simulation with {self.end_time} periods...")
        
        # 记录开始时间
        start_time = time.time()
        
        # 创建统计数组
        self.st.create_array(self.end_time, self.num_of_tc, self.num_of_firm)
        
        # 初始化治疗类别
        print("Initializing therapeutic categories...")
        self.init_tc()
        
        # 初始化企业
        print("Initializing firms...")
        self.init_firm()
        
        # 执行主模拟循环
        print("Running simulation...")
        for t in range(1, self.end_time + 1):
            # 每10个周期显示一次进度
            if t % 10 == 0:
                print(f"Period {t}/{self.end_time}")
                
            # 企业进入市场
            self.entry(self.num_of_firm, t)
            
            # 分子价值更新
            self.mol_value(t)
            
            # 搜索方法选择
            self.method_of_search(t)
            
            # 研究活动
            self.research_activity(t)
            
            # 检查分子是否达到质量标准
            self.check_mol(t)
            
            # 计算市场份额
            self.calc_share(t)
            
            # 计算利润
            self.calc_profit(t)
            
            # 市场营销活动
            self.mkting(t)
            
            # 退出规则检查
            self.exit_rule(t)
            
            # 收集统计数据
            self.collect_statistics(t)
        
        # 记录结束时间并计算运行时间
        end_time = time.time()
        run_time = end_time - start_time
        print(f"Simulation completed in {run_time:.2f} seconds")
        
        # 生成单次模拟报告（使用ASCII编码，与Java版本一致）
        result_file = os.path.join(self.path_results, "singleSimulation.txt")
        with open(result_file, 'w', encoding='ascii') as f:
            f.write("Pharmaceutical Industry Model - Single Simulation\n")
            f.write("Runtime: {}\n".format(time.strftime('%Y-%m-%d %H:%M:%S')))
            f.write("Parameters:\n")
            f.write("- Simulation periods: {}\n".format(self.end_time))
            f.write("- Number of therapeutic categories: {}\n".format(self.num_of_tc))
            f.write("- Number of firms: {}\n".format(self.num_of_firm))
            f.write("- Molecules per therapeutic category: {}\n\n".format(self.num_of_mol))
            
            # 记录基本结果统计（使用Java格式）
            f.write("Simulation Results:\n")
            f.write("- Final active firms: {:.2f}\n".format(self.st.alive_f_with_prod[self.end_time]))
            f.write("- Innovative products: {:.2f}\n".format(self.st.inno_prod[self.end_time]))
            f.write("- Imitative products: {:.2f}\n".format(self.st.imi_prod[self.end_time]))
            f.write("- Total Herfindahl index: {:.6f}\n".format(self.st.tot_h[self.end_time]))
            f.write("- Average Herfindahl index: {:.6f}\n".format(self.st.mean_h[self.end_time]))
            f.write("- Average price of innovative products: {:.6f}\n".format(self.st.price_mean_inno[self.end_time]))
            f.write("- Average price of imitative products: {:.6f}\n".format(self.st.price_mean_imi[self.end_time]))
            f.write("- Total profit: {:.2f}\n".format(self.st.profit_tot[self.end_time]))
        
        # 生成param.txt文件（与Java版本格式一致）
        self.generate_param_file()
        
        print(f"Single simulation report saved to {result_file}")
        return True
        
    def collect_statistics(self, t):
        """收集当前时期的统计数据"""
        # 统计活跃企业数量
        alive_firms = 0
        for f_id in range(1, self.num_of_firm + 1):
            if f_id < len(self.f) and self.f[f_id] is not None and self.f[f_id].alive:
                if self.f[f_id].tot_share[t] > 0:  # 只计算有市场份额的企业
                    alive_firms += 1
        
        # 统计创新产品和仿制产品数量
        inno_products = 0
        imi_products = 0
        inno_price_sum = 0.0
        imi_price_sum = 0.0
        inno_price_count = 0
        imi_price_count = 0
        
        for f_id in range(1, self.num_of_firm + 1):
            if f_id < len(self.f) and self.f[f_id] is not None and self.f[f_id].alive:
                for p_id in range(1, self.f[f_id].num_of_products + 1):
                    if p_id < len(self.f[f_id].prod) and self.f[f_id].prod[p_id] is not None and not self.f[f_id].prod[p_id].out:
                        if self.f[f_id].prod[p_id].imitative:
                            imi_products += 1
                            if self.f[f_id].prod[p_id].price > 0:
                                imi_price_sum += self.f[f_id].prod[p_id].price
                                imi_price_count += 1
                        else:
                            inno_products += 1
                            if self.f[f_id].prod[p_id].price > 0:
                                inno_price_sum += self.f[f_id].prod[p_id].price
                                inno_price_count += 1
        
        # 计算平均价格
        inno_price_avg = inno_price_sum / inno_price_count if inno_price_count > 0 else 0
        imi_price_avg = imi_price_sum / imi_price_count if imi_price_count > 0 else 0
        
        # 计算总赫芬达尔指数和平均赫芬达尔指数
        tot_h = 0.0
        tc_count = 0
        h_sum = 0.0
        
        for tc_id in range(1, self.num_of_tc + 1):
            if tc_id < len(self.tc) and self.tc[tc_id] is not None and hasattr(self.tc[tc_id], 'herfindahl'):
                if self.tc[tc_id].in_product[t] > 0:  # 只计算有产品的治疗类别
                    h_sum += self.tc[tc_id].herfindahl[t]
                    tc_count += 1
        
        mean_h = h_sum / tc_count if tc_count > 0 else 0
        
        # 计算总市场集中度（总赫芬达尔指数）
        firm_shares = {}
        total_market = 0.0
        
        for f_id in range(1, self.num_of_firm + 1):
            if f_id < len(self.f) and self.f[f_id] is not None and self.f[f_id].alive:
                firm_shares[f_id] = self.f[f_id].tot_share[t]
                total_market += self.f[f_id].tot_share[t]
        
        if total_market > 0:
            for f_id in firm_shares:
                market_share = firm_shares[f_id] / total_market
                tot_h += market_share * market_share
        
        # 更新统计对象
        self.st.alive_f_with_prod[t] = alive_firms
        self.st.inno_prod[t] = inno_products
        self.st.imi_prod[t] = imi_products
        self.st.tot_h[t] = tot_h
        self.st.mean_h[t] = mean_h
        self.st.price_mean_inno[t] = inno_price_avg
        self.st.price_mean_imi[t] = imi_price_avg
        # profit_tot已经在calc_profit方法中更新
        
    def generate_param_file(self):
        """生成与Java版本格式一致的param.txt文件"""
        param_file = os.path.join(self.path_results, "param.txt")
        with open(param_file, 'w', encoding='ascii') as f:
            f.write("Multi Time: {}\n".format(self.mt))
            f.write("drawCost: {}\n".format(self.draw_cost))
            f.write("numOfFirm: {}\n".format(self.num_of_firm))
            f.write("numOfTC: {}\n".format(self.num_of_tc))
            f.write("TCValueCost: {}\n".format(self.tc_patients_cost))
            f.write("numOfMol: {}\n".format(self.num_of_mol))
            f.write("qMolNull: {}\n".format(self.q_mol_null))
            f.write("patentDuration: {}\n".format(self.patent_duration))
            f.write("CostOfSearch: {}\n".format(self.cost_of_search))
            f.write("costOfResearchInn: {}\n".format(self.cost_of_research_inn))
            f.write("costOfResearchImi: {}\n".format(self.cost_of_research_imi))
            f.write("Initial Budget: {}\n".format(self.b))
            f.write("qualityCheck: {}\n".format(self.quality_check))
            f.write("AvgWeightInno: {}\n".format(self.speed_development_inno))
            f.write("AvgWeightImi: {}\n".format(self.speed_development_imi))
            f.write("Product exits below this threshold: {}\n".format(self.out_pro_limit))
            f.write("Firm exits market after n unsuccesful searches: {}\n".format(self.search_failure))
            f.write("interestRate: {}\n".format(self.interest_rate))
            f.write("timeDevelop: {}\n".format(self.time_develop))
            f.write("erosion marketing: {}\n".format(self.erosion))
            f.write("Firm exits below this threshold: {}\n".format(self.e_failure))
            f.write("costProd: {}\n".format(self.cost_prod))
            f.write("eta: {}\n".format(self.omega))
            f.write("elasticity in the markup formula: {}\n".format(self.elasticity))
            f.write("endTime: {}\n".format(self.end_time))
            f.write("patentOriz: {}\n".format(self.patent_width))
            f.write("TCValueRand: {}\n".format(self.tc_patients_rand))
            f.write("a avg: {}\n".format(self.a_value_cost))
            f.write("a range: {}\n".format(self.a_value_rand))
            f.write("b avg: {}\n".format(self.b_value_cost))
            f.write("b range: {}\n".format(self.b_value_rand))
            f.write("c avg: {}\n".format(self.c_value_cost))
            f.write("c range: {}\n".format(self.c_value_rand))
            f.write("qMolCost: {}\n".format(self.q_mol_cost))
            f.write("qMolVar: {}\n".format(self.q_mol_var))
            f.write("numOfSubMKT: {}\n".format(self.num_of_sub_mkt))
            f.write("% of R&D budget invested in search: {}\n".format(self.quota_invested_in_search))

    def make_multiple_simulation(self):
        """
        执行多次模拟并生成统计报告
        """
        print(f"Starting multiple simulations ({self.mt} iterations)...")
        
        # 记录开始时间
        total_start_time = time.time()
        
        # 执行多次模拟
        for i in range(1, self.mt + 1):
            print(f"Running simulation {i}/{self.mt}")
            
            # 重置随机数生成器，使用不同的种子
            seed = self.rng_seed + i
            self.r = JavaCompatibleRandom(seed)
            self.rand = JavaCompatibleRandom(seed)
            random.seed(seed)
            np.random.seed(seed)
            
            # 初始化统计对象
            self.st.create_array(self.end_time, self.num_of_tc, self.num_of_firm)
            
            # 初始化治疗类别
            self.init_tc()
            
            # 初始化企业
            self.init_firm()
            
            # 执行主模拟循环
            for t in range(1, self.end_time + 1):
                # 企业进入市场
                self.entry(self.num_of_firm, t)
                
                # 分子价值更新
                self.mol_value(t)
                
                # 搜索方法选择
                self.method_of_search(t)
                
                # 研究活动
                self.research_activity(t)
                
                # 检查分子是否达到质量标准
                self.check_mol(t)
                
                # 计算市场份额
                self.calc_share(t)
                
                # 计算利润
                self.calc_profit(t)
                
                # 市场营销活动
                self.mkting(t)
                
                # 退出规则检查
                self.exit_rule(t)
                
                # 收集统计数据
                self.collect_statistics(t)
            
            # 累积统计结果
            self.st.generate_multi_report(self.end_time, self.num_of_firm, self.num_of_tc)
            
            # 显示进度
            if i % 10 == 0 or i == self.mt:
                print(f"Completed {i}/{self.mt} simulations")
        
        # 生成多次模拟报告（生成与Java版本相同格式的multiout.txt）
        self.generate_multiout_file()
        
        # 生成param.txt文件
        self.generate_param_file()
        
        print(f"Multiple simulation reports generated in {self.path_results}")
        return True
        
    def generate_multiout_file(self):
        """生成与Java版本格式一致的multiout.txt文件"""
        output_file = os.path.join(self.path_results, "multiout.txt")
        with open(output_file, 'w', encoding='ascii') as f:
            # 严格按照Java版本的格式编写标题行（没有空格）
            f.write("H,H_avg_TC,prod_inno,prod_imi,alive_firms_with_prod,TC_viewed,price_inno,price_imi\n")
            
            # 写入每个时间周期的数据
            for t in range(self.end_time + 1):
                # 计算观察到的治疗类别数量
                tc_viewed = 0
                for tc_id in range(1, self.num_of_tc + 1):
                    if tc_id < len(self.tc) and self.tc[tc_id] is not None and hasattr(self.tc[tc_id], 'in_product'):
                        if self.tc[tc_id].in_product[t] > 0:
                            tc_viewed += 1
                
                # 确保获取到的值不为None
                h_value = self.st.multi_tot_h[t] if hasattr(self.st, 'multi_tot_h') and t < len(self.st.multi_tot_h) else 0.0
                h_avg = self.st.multi_mean_h[t] if hasattr(self.st, 'multi_mean_h') and t < len(self.st.multi_mean_h) else 0.0
                inno_prod = self.st.multi_inno_prod[t] if hasattr(self.st, 'multi_inno_prod') and t < len(self.st.multi_inno_prod) else 0
                imi_prod = self.st.multi_imi_prod[t] if hasattr(self.st, 'multi_imi_prod') and t < len(self.st.multi_imi_prod) else 0
                alive_f = self.st.multi_alive_f_with_prod[t] if hasattr(self.st, 'multi_alive_f_with_prod') and t < len(self.st.multi_alive_f_with_prod) else 0
                price_inno = self.st.multi_price_inno[t] if hasattr(self.st, 'multi_price_inno') and t < len(self.st.multi_price_inno) else 0.0
                price_imi = self.st.multi_price_imi[t] if hasattr(self.st, 'multi_price_imi') and t < len(self.st.multi_price_imi) else 0.0
                
                # 格式化为与Java版本完全一致的格式（注意precision和没有空格）
                f.write("{:.6f},{:.6f},{},{},{},{},{:.6f},{:.6f}\n".format(
                    h_value, h_avg, int(inno_prod), int(imi_prod), int(alive_f), tc_viewed, price_inno, price_imi))

    def init_tc(self):
        """Initialize therapeutic categories."""
        # Initialize array of therapeutic categories
        self.tc = [None] * (self.num_of_tc + 1)
        
        # For each therapeutic category
        for i in range(1, self.num_of_tc + 1):
            # Generate random parameters for this TC
            # Number of patients: normal distribution
            patients = int(max(0, self.tc_patients_cost + self.r.nextGaussian() * self.tc_patients_rand))
            
            # Quality importance: random variation around mean
            a_val = self.a_value_cost + (self.r.random() * 2 - 1) * self.a_value_rand
            
            # Price importance: random variation around mean
            b_val = self.b_value_cost + (self.r.random() * 2 - 1) * self.b_value_rand
            
            # Marketing importance: random variation around mean
            c_val = self.c_value_cost + (self.r.random() * 2 - 1) * self.c_value_rand
            
            # Create the therapeutic category with these parameters
            self.tc[i] = TherapeuticCategory(i, patients, a_val, b_val, c_val, self.end_time, self)
            
            # Set submarket values
            self.tc[i].set_sub_mkt_value(self)
            
            # Calculate minimum quality requirements for each submarket
            self.tc[i].calc_q_min_in_smkt(self)
            
            # For each molecule in the TC
            for j in range(self.num_of_mol + 1):
                # Determine molecule quality
                if self.r.random() < self.q_mol_null:
                    # Zero quality (not promising molecule)
                    self.tc[i].mol[j].q = 0
                else:
                    # Positive quality (promising molecule)
                    # Generate random quality from normal distribution
                    qual = int(max(self.quality_check, 
                                  min(self.quality_max,
                                      self.q_mol_cost + self.r.nextGaussian() * self.q_mol_var)))
                    self.tc[i].mol[j].q = qual

    def init_firm(self):
        """Initialize firms."""
        # Create array of firms
        self.f = [None] * (self.num_of_firm + 1)
        
        # For each potential firm
        for i in range(1, self.num_of_firm + 1):
            # 60% chance of being an innovator, 40% chance of being an imitator
            is_innovator = self.r.random() < 0.6
            
            # Random propensity to be innovator/imitator between 0.4 and 0.6
            imin = 0.4 + self.r.random() * 0.2
            
            # Random allocation of budget between R&D and marketing
            search_research = self.min_rd + self.r.random() * self.add_rd
            
            # Random allocation within R&D budget for search vs. development
            alfa = self.min_s + self.r.random() * self.add_s
            
            # Create the firm
            self.f[i] = Firm(self.b, 1.0 - search_research, search_research,
                            alfa, self.num_of_tc, is_innovator, imin, self)
            
            # Mark the firm as active
            self.f[i].alive = True

    def entry(self, nfirm, t):
        """
        Method for firm entry into the industry.
        
        Args:
            nfirm (int): Number of firms to potentially enter
            t (int): Current time period
        """
        # Loop through potential firms
        for i in range(1, nfirm + 1):
            # Find the first inactive firm
            for firm_id in range(1, self.num_of_firm + 1):
                if not self.f[firm_id].alive:
                    # Activate the firm with probability 0.5
                    if self.r.random() < 0.5:
                        # Generate random values for firm characteristics
                        imin = self.r.random()  # Propensity to be innovator/imitator
                        innovator = self.r.random() < 0.5  # 50% chance to be innovator
                        
                        # Set economic variables
                        self.f[firm_id].alive = True
                        self.f[firm_id].budget = self.b
                        self.f[firm_id].innovator = innovator
                        self.f[firm_id].imin = imin
                        self.f[firm_id].cost_of_inno = self.cost_of_research_inn
                        self.f[firm_id].cost_of_imi = self.cost_of_research_imi
                        
                        # Log entry
                        if t > 1:
                            if innovator:
                                firm_type = "Innovative"
                            else:
                                firm_type = "Imitative"
                            self.file.print(f"Time {t}: {firm_type} firm {firm_id} enters the market")
                    break
        
    def mol_value(self, t):
        """
        Determine the value of molecules in each TC.
        
        Args:
            t (int): Current time period
        """
        # For each therapeutic category
        for tc_id in range(1, self.num_of_tc + 1):
            # Calculate the value of the TC (number of potential patients)
            self.tc[tc_id].dim[t] = self.tc[tc_id].value
            
            # Use set_sub_mkt_value to update submarket values
            self.tc[tc_id].set_sub_mkt_value(self)
            
            # Calculate minimum quality requirements for each submarket
            self.tc[tc_id].calc_q_min_in_smkt(self)
            
            # For each molecule in the TC
            for j in range(self.num_of_mol + 1):
                mol = self.tc[tc_id].mol[j]
                
                # Skip already valued molecules
                if mol.q != 0:
                    continue
                
                # Random draw to determine molecule quality
                if self.r.random() < self.q_mol_null:
                    # Zero-quality molecule (97% chance by default)
                    mol.q = 0
                else:
                    # Non-zero quality molecule (3% chance)
                    # Generate quality from normal distribution
                    q = int(max(0, min(self.quality_max, 
                                      self.q_mol_cost + self.q_mol_var * self.r.nextGaussian())))
                    mol.q = q
                    
                    # Record statistics for therapeutic category
                    self.tc[tc_id].dim[t] += 1

    def method_of_search(self, t):
        """
        Research method selection.
        
        Determines whether firms will pursue innovative or imitative research.
        
        Args:
            t (int): Current time period
        """
        # Randomly initialize the order of firms to avoid bias
        init_firm = min(self.r.nextInt(self.num_of_firm), self.num_of_firm - 1)
        
        # First half of firms (from init_firm to end)
        for i in range(init_firm, self.num_of_firm):
            if i < len(self.f) and self.f[i] is not None and self.f[i].alive:
                # Determine if firm is innovator or imitator based on propensity
                self.f[i].innovatort = self.f[i].choose_im_in(self)
                
                # Calculate number of innovative and imitative products
                self.f[i].calc_imi_inno(t)
                
                # Select behavior based on innovator status or availability of products to imitate
                if self.f[i].innovatort or (not self.f[i].innovatort and self.selection_imit_tc_best_earnings(i, t) == -1):
                    # Set budget for search/development (Equation 2 in chapter)
                    self.f[i].search(t, "inno", self.draw_cost, self)
                    # Perform search and record drawn molecules
                    self.f[i].search_action.do_search(t, self.f[i].tot_prod, self)
                else:
                    self.f[i].search(t, "imi", 0, self)
                
                # Update search activity
                self.search_activity(t, i)
        
        # Second half of firms (from 0 to init_firm)
        for i in range(init_firm):
            if i < len(self.f) and self.f[i] is not None and self.f[i].alive:
                self.f[i].innovatort = self.f[i].choose_im_in(self)
                self.f[i].calc_imi_inno(t)
                
                if self.f[i].innovatort or (not self.f[i].innovatort and self.selection_imit_tc_best_earnings(i, t) == -1):
                    self.f[i].search(t, "inno", self.draw_cost, self)
                    self.f[i].search_action.do_search(t, self.f[i].tot_prod, self)
                else:
                    self.f[i].search(t, "imi", 0, self)
                
                # Update search activity
                self.search_activity(t, i)
    
    def search_activity(self, time, firm_id):
        """
        Search activity implementation.
        
        Args:
            time (int): Current time period
            firm_id (int): Firm ID
        """
        # Check if firm is innovative
        if self.f[firm_id].innovatort:
            # Innovative search - check portfolio for molecules to patent
            for n in range(len(self.f[firm_id].search_action.portfolio_tc)):
                if n < len(self.f[firm_id].search_action.portfolio_mol):
                    tc_id = self.f[firm_id].search_action.portfolio_tc[n]
                    mol_id = self.f[firm_id].search_action.portfolio_mol[n]
                    
                    # Check if molecule has quality and is not patented
                    if (self.tc[tc_id].mol[mol_id].q > 0 and 
                        not self.tc[tc_id].mol[mol_id].patent):
                        # Patent the molecule
                        self.tc[tc_id].patent(mol_id, time, firm_id, self)
            
            # Record found molecules in memory for innovation
            self.f[firm_id].on_pro_inno.record_memory(
                self.f[firm_id].search_action.portfolio_mol,
                self.f[firm_id].search_action.portfolio_tc,
                self.f[firm_id].search_action.number_draw,
                self
            )
            
            # Check if firm has failed to find molecules for too long
            if self.f[firm_id].search_action.bad_perf > self.search_failure:
                # Firm fails if it cannot find new molecules
                self.f[firm_id].failure(self)
        else:
            # Imitative search
            # Identify TC with highest potential earnings
            tc_to_imit = self.selection_imit_tc_best_earnings(firm_id, time)
            
            # If a TC is identified
            if tc_to_imit != -1:
                # Record molecules for imitation
                self.f[firm_id].on_pro_imi.record_memory_imi(self)

    def selection_imit_tc_best_earnings(self, firm, t):
        """
        Select therapeutic category to imitate based on earnings potential.
        
        Args:
            firm (int): Firm ID
            t (int): Current time period
            
        Returns:
            int: Selected TC ID or -1 if none found
        """
        best_ta = -1
        best_amount = 0
        
        # For each TC, evaluate potential earnings
        for ta in range(1, self.num_of_tc + 1):
            if hasattr(self.tc[ta], 'herfindahl') and self.tc[ta].herfindahl is not None and len(self.tc[ta].herfindahl) > 0:
                # Skip TCs where the firm already operates
                has_products = False
                for j in range(self.f[firm].num_of_products):
                    if self.f[firm].prod[j] is not None and self.f[firm].prod[j].tc == ta:
                        has_products = True
                        break
                
                if not has_products:
                    # Find best product in the TC
                    best_prod = 0
                    best_earn = 0
                    
                    # Check all products in the TC
                    for j in range(1, self.num_of_firm + 1):
                        if self.f[j].alive:
                            for k in range(self.f[j].num_of_products):
                                if (self.f[j].prod[k] is not None and 
                                    self.f[j].prod[k].tc == ta and
                                    not self.f[j].prod[k].out and
                                    self.f[j].prod[k].b_prod <= t - self.patent_duration):
                                    
                                    # Calculate average earnings
                                    avg_earn = sum(self.f[j].prod[k].history_earnings) / t
                                    
                                    if avg_earn > best_earn:
                                        best_earn = avg_earn
                                        best_prod = k
                                        best_amount = avg_earn
                                        best_ta = ta
        
        return best_ta

    def research_activity(self, t):
        """
        Conduct research activities for all active firms.
        
        Args:
            t (int): Current time period
        """
        # For each firm, evaluate research projects and allocate budget
        for f in range(1, self.num_of_firm + 1):
            if self.f[f].alive:
                # Calculate capacity for innovative and imitative projects
                capacity_inno = self.f[f].num_projects(True, self.time_develop / self.speed_development_inno)
                capacity_imi = self.f[f].num_projects(False, self.time_develop / self.speed_development_imi)
                
                # Allocate projects based on capacity
                if capacity_inno > 0:
                    # If firm has innovative capacity, select projects
                    from .multiprojectselection import MultiProjectSelection
                    MultiProjectSelection.in_projects(
                        [], [], capacity_inno, f, t, self
                    )
                
                if capacity_imi > 0:
                    # If firm has imitative capacity, select projects
                    from .multiprojectselection import MultiProjectSelection
                    MultiProjectSelection.in_projects(
                        [], [], capacity_imi, f, t, self
                    )
                
                # Progress existing research projects
                self.f[f].research(t, self)
        
    def check_mol(self, t):
        """
        Check molecules for patent expiration.
        
        Args:
            t (int): Current time period
        """
        # For each therapeutic category
        for tc_id in range(1, self.num_of_tc + 1):
            # Check patents and update statistics
            self.tc[tc_id].patent_time_control(t, self.patent_duration, self)
            
            # Count patented molecules
            num_patents = 0
            for i in range(self.num_of_mol + 1):
                if self.tc[tc_id].mol[i].patent:
                    num_patents += 1
            
            # Update statistics
            self.tc[tc_id].pat[t] = num_patents
        
    def calc_share(self, time):
        """
        Calculate market shares for products and firms.
        
        Args:
            time (int): Current time period
        """
        # Reset counters and statistics
        for i in range(1, self.num_of_firm + 1):
            self.f[i].tot_share[time] = 0
            self.f[i].tot_share_quantity[time] = 0
            self.f[i].total_reached_patients = 0
            
            # Reset shares for each therapeutic category
            for j in range(1, self.num_of_tc + 1):
                self.f[i].sh_tc[j] = 0
                self.f[i].sh_ta1[j] = 0
        
        # Process each therapeutic category
        for tc_id in range(1, self.num_of_tc + 1):
            tc = self.tc[tc_id]
            tc.store_pos = 0
            
            # For each submarket in this therapeutic category
            for smt_id in range(self.num_of_sub_mkt):
                submarket = tc.s_mkt[smt_id]
                submarket.store_pos = 0
                
                # Count active products in this therapeutic category
                in_product_tc = 0
                in_product_only_inno_tc = 0
                
                # Calculate probabilities of sell for all products
                for f_id in range(1, self.num_of_firm + 1):
                    firm = self.f[f_id]
                    
                    # Skip if firm is not active
                    if not firm.alive:
                        continue
                    
                    # Process each product
                    for prod_id in range(1, firm.num_of_products + 1):
                        if prod_id >= len(firm.prod) or firm.prod[prod_id] is None:
                            continue  # Skip if product doesn't exist
                            
                        product = firm.prod[prod_id]
                        
                        # Skip products that are out of market or in different TC
                        if product.out or product.tc != tc_id:
                            continue
                        
                        # Calculate product utility
                        product.prob_of_sell(time, f_id, self)
                        
                        # If product quality meets submarket requirements
                        if product.qp >= submarket.q_min_req:
                            # Add product utility to submarket
                            submarket.store_pos += product.pos
                            
                            # Count product
                            in_product_tc += 1
                            if not product.imitative:
                                in_product_only_inno_tc += 1
                
                # Save statistics
                tc.in_product[time] = in_product_tc
                tc.in_product_only_inno[time] = in_product_only_inno_tc
            
            # Calculate share for each product in the therapeutic category
            inno_sh = 0
            imi_sh = 0
            inno_sh_q = 0
            imi_sh_q = 0
            inno_count = 0
            imi_count = 0
            
            # Calculate market shares for each product
            for f_id in range(1, self.num_of_firm + 1):
                firm = self.f[f_id]
                
                # Skip if firm is not active
                if not firm.alive:
                    continue
                
                # Process each product
                for prod_id in range(1, firm.num_of_products + 1):
                    if prod_id >= len(firm.prod) or firm.prod[prod_id] is None:
                        continue  # Skip if product doesn't exist
                        
                    product = firm.prod[prod_id]
                    
                    # Skip products that are out of market or in different TC
                    if product.out or product.tc != tc_id:
                        continue
                    
                    # For each submarket
                    for smt_id in range(self.num_of_sub_mkt):
                        submarket = tc.s_mkt[smt_id]
                        
                        # If product quality meets submarket requirements
                        if product.qp >= submarket.q_min_req:
                            # If there's at least one product in the submarket
                            if submarket.store_pos > 0:
                                # Calculate market share (equation 10 in chapter 5)
                                share = product.pos / submarket.store_pos
                                
                                # Calculate patients reached
                                patients = share * submarket.value_mkt
                                product.num_patients += patients
                                firm.total_reached_patients += patients
                                
                                # Update statistics based on product type
                                if product.imitative:
                                    imi_sh += share
                                    imi_sh_q += patients
                                    imi_count += 1
                                else:
                                    inno_sh += share
                                    inno_sh_q += patients
                                    inno_count += 1
                                
                                # Store patients in product history
                                product.history_patients[time] = product.num_patients
                                
                                # Update firm's share in this TC
                                firm.sh_tc[tc_id] += product.num_patients
                
                # Store firm's overall share for this TC
                firm.sh_ta1[tc_id] = firm.sh_tc[tc_id]
                
                # Add to firm's total share across all TCs
                firm.tot_share[time] += firm.sh_tc[tc_id]
                firm.tot_share_quantity[time] += firm.sh_tc[tc_id]
            
            # Update statistics for shares by innovation type
            if in_product_tc > 0:
                tc.inno_sh = inno_sh / in_product_tc
                tc.imi_sh = imi_sh / in_product_tc
            
            # Calculate Herfindahl index (market concentration)
            h_index = 0
            h_index_quantity = 0
            
            for f_id in range(1, self.num_of_firm + 1):
                if tc.value > 0 and self.f[f_id].alive:
                    # Calculate market share as percentage
                    share_perc = self.f[f_id].sh_tc[tc_id] / tc.value
                    
                    # Add squared market share to Herfindahl index
                    h_index += share_perc * share_perc
                    h_index_quantity += share_perc * share_perc
            
            # Store Herfindahl index
            tc.herfindahl[time] = h_index
            tc.herfindahl1[time] = h_index_quantity
            
            # Count firms active in this TC
            in_firm_count = 0
            for f_id in range(1, self.num_of_firm + 1):
                if self.f[f_id].alive and self.f[f_id].sh_tc[tc_id] > 0:
                    in_firm_count += 1
            
            # Store count of firms
            tc.in_firm[time] = in_firm_count
        
    def calc_profit(self, time):
        """
        Calculate profits for all firms and products.
        
        Args:
            time (int): Current time period
        """
        # Process each firm
        total_profit = 0
        
        for firm_id in range(1, self.num_of_firm + 1):
            firm = self.f[firm_id]
            
            # Skip if firm is not active
            if not firm.alive:
                continue
            
            # Reset firm profit
            firm.tot_profit = 0
            
            # Process each product
            for prod_id in range(1, firm.num_of_products + 1):
                if prod_id >= len(firm.prod) or firm.prod[prod_id] is None:
                    continue  # Skip if product doesn't exist
                    
                product = firm.prod[prod_id]
                
                # Skip products that are out of market
                if product.out:
                    continue
                
                # Calculate markup for this product if it hasn't been calculated yet
                if product.mup <= 0:
                    product.mup = self.mean_mup(product.tc, time, self.elasticity, "inno")
                
                # Calculate product earnings (equation 11 in chapter 5)
                # Revenue = price * quantity
                # Price = unit cost * (1 + markup)
                # Profit = (price - unit cost) * quantity = unit cost * markup * quantity
                earnings = self.cost_prod * product.mup * product.num_patients
                
                # Store earnings in product history
                product.history_earnings[time] = earnings
                
                # Add to firm's total profit
                firm.tot_profit += earnings
            
            # Add to total industry profit
            total_profit += firm.tot_profit
        
        # Store total profit for this time period
        self.st.profit_tot[time] = total_profit
    
    def calc_mup(self, num_of_firm, num_of_ta, firm, file, ta, time, eta, elasticity):
        """
        Calculate markup for products.
        
        Args:
            num_of_firm (int): Number of firms
            num_of_ta (int): Number of therapeutic categories
            firm (list): List of firms
            file (Files): File handler
            ta (list): List of therapeutic categories
            time (int): Current time period
            eta (float): Market power parameter (omega)
            elasticity (float): Price elasticity
            
        Returns:
            float: Calculated markup
        """
        # Calculate markup based on equation 6 in chapter 5
        # Markup = η / (ε * (1 - η * s))
        # Where η is market power, ε is elasticity, and s is market share
        
        return self.mean_mup(0, time, elasticity, "general")
    
    def mean_mup(self, area, t, elasticity, st):
        """
        Calculate mean markup for products based on their market position.
        
        Args:
            area (int): Therapeutic category area (0 for all areas)
            t (int): Current time period
            elasticity (float): Price elasticity
            st (str): Product type ("inno", "imi", or "general")
            
        Returns:
            float: Calculated mean markup
        """
        # Set default markup
        if elasticity <= 0:
            return 1.0
        
        # Base markup for all products (equation 6 in chapter 5)
        markup = self.omega / elasticity
        
        # Adjust markup based on market concentration (Herfindahl index)
        if t > 1:
            h_index_tot = 0
            h_count = 0
            
            # Calculate average Herfindahl index across all TCs
            for i in range(1, self.num_of_tc + 1):
                if self.tc[i].in_product[t-1] > 0:
                    h_index_tot += self.tc[i].herfindahl[t-1]
                    h_count += 1
            
            # If there are active TCs, adjust markup based on concentration
            if h_count > 0:
                avg_h_index = h_index_tot / h_count
                
                # Higher concentration allows for higher markups
                if st == "inno":
                    # Innovative products can charge higher markups
                    markup = (self.omega / elasticity) * (1 + avg_h_index)
                elif st == "imi":
                    # Imitative products charge lower markups
                    markup = (self.omega / elasticity) * (1 - avg_h_index)
                else:
                    # General case
                    markup = self.omega / elasticity
        
        # Ensure markup is reasonable
        return max(0.05, min(2.0, markup))
        
    def mkting(self, time):
        """
        Manage marketing activities for all firms.
        
        Args:
            time (int): Current time period
        """
        # Process each firm
        for firm_id in range(1, self.num_of_firm + 1):
            firm = self.f[firm_id]
            
            # Skip if firm is not active
            if not firm.alive:
                continue
            
            # Plan marketing investments
            firm.proj_mkting()
            
            # Execute marketing strategy
            firm.mkting()
    
    def exit_rule(self, time):
        """
        Apply exit rules to determine which firms and products leave the market.
        
        Args:
            time (int): Current time period
        """
        # Calculate the total market value (total number of patients)
        tot_market_value = 0
        for i in range(1, self.num_of_tc + 1):
            if i < len(self.tc) and self.tc[i] is not None:
                tot_market_value += self.tc[i].value
        
        # Skip exit checks in first period
        if time <= 1 or tot_market_value <= 0:
            return
        
        # Process each firm
        for firm_id in range(1, self.num_of_firm + 1):
            if firm_id >= len(self.f) or self.f[firm_id] is None:
                continue
                
            firm = self.f[firm_id]
            
            # Skip if firm is not active
            if not firm.alive:
                continue
            
            # Calculate firm's overall market share
            firm_share = firm.tot_share[time] / tot_market_value
            
            # Check if firm has sufficient market share to stay in business
            if firm_share < self.e_failure:
                # If market share is too small, the firm exits
                firm.alive = False
                firm.on_mkt = False
                
                # Log exit event if file is open
                if hasattr(self.file, 'fp') and self.file.fp is not None and not self.file.fp.closed:
                    self.file.print(f"Time {time}: Firm {firm_id} exits due to insufficient market share ({firm_share:.4f})")
                
                # Mark all firm's products as out of market
                for prod_id in range(1, firm.num_of_products + 1):
                    if prod_id < len(firm.prod) and firm.prod[prod_id] is not None and not firm.prod[prod_id].out:
                        firm.prod[prod_id].out = True
            else:
                # Firm stays in business, but check if any products should exit
                firm.products_out(self.out_pro_limit, self)

# Helper classes will be defined in separate files

class Files:
    """File operations class"""
    def __init__(self):
        self.fp = None
        self.fparam = None
    
    def create_dir(self, dir_name):
        """Create directory if it doesn't exist"""
        os.makedirs(dir_name, exist_ok=True)
        
    def print(self, text):
        """Print to output file"""
        if self.fp:
            self.fp.write(f"{text}\n")
            
    def print_param(self, text):
        """Print parameters to parameters file"""
        if self.fparam:
            self.fparam.write(f"{text}\n")
            
    def init_files(self, name):
        """Initialize output files"""
        try:
            self.fp = open(f"{name}.csv", "w")
            self.fparam = open(f"{name}_params.txt", "w")
        except Exception as e:
            print(f"Error opening files: {e}")
            
    def close_files(self):
        """Close output files"""
        if self.fp:
            self.fp.close()
        if self.fparam:
            self.fparam.close()

class Statistic:
    """Statistics collection and reporting"""
    def __init__(self):
        """Initialize statistic arrays"""
        self.tot_h = None                 # 总赫芬达尔指数
        self.mean_h = None                # 平均赫芬达尔指数
        self.inno_prod = None             # 创新产品数量
        self.imi_prod = None              # 仿制产品数量
        self.alive_f_with_prod = None     # 有产品的存活公司数量
        self.price_mean_inno = None       # 创新产品平均价格
        self.price_mean_imi = None        # 仿制产品平均价格
        self.profit_tot = None            # 总利润
        self.concentration = None         # 市场集中度
        
        # 多次运行的统计
        self.multi_tot_h = None           # 多次运行的总赫芬达尔指数
        self.multi_mean_h = None          # 多次运行的平均赫芬达尔指数
        self.multi_inno_prod = None       # 多次运行的创新产品数量
        self.multi_imi_prod = None        # 多次运行的仿制产品数量
        self.multi_alive_f_with_prod = None  # 多次运行的有产品的存活公司数量
        self.multi_price_inno = None      # 多次运行的创新产品平均价格
        self.multi_price_imi = None       # 多次运行的仿制产品平均价格
        
    def create_array(self, end_time, num_of_ta, num_of_firm):
        """Create arrays for statistics"""
        # Initialize arrays
        self.tot_h = [0.0] * (end_time + 1)                 # 总赫芬达尔指数
        self.mean_h = [0.0] * (end_time + 1)                # 平均赫芬达尔指数
        self.inno_prod = [0.0] * (end_time + 1)             # 创新产品数量
        self.imi_prod = [0.0] * (end_time + 1)              # 仿制产品数量
        self.alive_f_with_prod = [0.0] * (end_time + 1)     # 有产品的存活公司数量
        self.price_mean_inno = [0.0] * (end_time + 1)       # 创新产品平均价格
        self.price_mean_imi = [0.0] * (end_time + 1)        # 仿制产品平均价格
        self.profit_tot = [0.0] * (end_time + 1)            # 总利润
        self.concentration = [0.0] * (end_time + 1)         # 市场集中度
        
    def generate_multi_report(self, end_time, num_of_firm, num_of_tc):
        """Initialize multi-run statistics"""
        # 初始化多次运行的统计数组
        self.multi_tot_h = [0.0] * (end_time + 1)           # 多次运行的总赫芬达尔指数
        self.multi_mean_h = [0.0] * (end_time + 1)          # 多次运行的平均赫芬达尔指数
        self.multi_inno_prod = [0.0] * (end_time + 1)       # 多次运行的创新产品数量
        self.multi_imi_prod = [0.0] * (end_time + 1)        # 多次运行的仿制产品数量
        self.multi_alive_f_with_prod = [0.0] * (end_time + 1)  # 多次运行的有产品的存活公司数量
        self.multi_price_inno = [0.0] * (end_time + 1)      # 多次运行的创新产品平均价格
        self.multi_price_imi = [0.0] * (end_time + 1)       # 多次运行的仿制产品平均价格
        
    def statistics(self, t, multi_time, num_of_ta, num_of_mol, num_of_firm):
        """Collect statistics for current time period"""
        # 在实际实现中，这里会收集各种统计数据
        pass
        
    def report_xls(self, end_time, num_of_firm, num_of_ta):
        """Generate report files"""
        # 这里可以实现生成报告的逻辑
        pass 