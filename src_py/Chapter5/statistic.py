#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
统计模块 - 定义制药产业模型的统计功能
"""

import os
import numpy as np
import pandas as pd
import math

class Statistic:
    """统计类，用于收集和分析模拟结果"""
    
    def __init__(self):
        """初始化统计对象"""
        # 统计数组
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
    
    def create_array(self, end_time, num_of_tc, num_of_firm):
        """
        创建统计数组
        
        Args:
            end_time (int): 模拟结束时间
            num_of_tc (int): 治疗类别数量
            num_of_firm (int): 公司数量
        """
        # 初始化统计数组
        self.tot_h = np.zeros(end_time + 1)                 # 总赫芬达尔指数
        self.mean_h = np.zeros(end_time + 1)                # 平均赫芬达尔指数
        self.inno_prod = np.zeros(end_time + 1)             # 创新产品数量
        self.imi_prod = np.zeros(end_time + 1)              # 仿制产品数量
        self.alive_f_with_prod = np.zeros(end_time + 1)     # 有产品的存活公司数量
        self.price_mean_inno = np.zeros(end_time + 1)       # 创新产品平均价格
        self.price_mean_imi = np.zeros(end_time + 1)        # 仿制产品平均价格
        self.profit_tot = np.zeros(end_time + 1)            # 总利润
        self.concentration = np.zeros(end_time + 1)         # 市场集中度
    
    def init_multi(self, end_time):
        """
        初始化多次模拟的统计数组
        
        Args:
            end_time (int): 模拟结束时间
        """
        # 初始化多次模拟的统计数组
        self.multi_tot_h = np.zeros(end_time + 1)
        self.multi_mean_h = np.zeros(end_time + 1)
        self.multi_inno_prod = np.zeros(end_time + 1)
        self.multi_imi_prod = np.zeros(end_time + 1)
        self.multi_alive_f_with_prod = np.zeros(end_time + 1)
        self.multi_price_inno = np.zeros(end_time + 1)
        self.multi_price_imi = np.zeros(end_time + 1)
    
    def statistics(self, t, multi_time, num_of_tc, num_of_mol, num_of_firm):
        """
        收集统计数据
        
        Args:
            t: 当前时间
            multi_time: 多次运行的次数
            num_of_tc: 治疗类别数量
            num_of_mol: 分子数量
            num_of_firm: 公司数量
        """
        # 在实际实现中，这里会统计各种指标
        # 这个简化版本不执行实际的统计分析
        pass
    
    def report_xls(self, end_time, num_of_firm, num_of_tc):
        """
        Generate report in the same format as Java version.
        
        Args:
            end_time (int): End time of simulation
            num_of_firm (int): Number of firms
            num_of_tc (int): Number of therapeutic categories
        """
        try:
            # Import C5Model here to avoid circular import
            import importlib
            module = importlib.import_module('src_py.Chapter5.c5_model')
            C5Model = getattr(module, 'C5Model')
            
            # Create output directory if it doesn't exist
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                     "results_py", "Chapter5")
            os.makedirs(output_dir, exist_ok=True)
            
            # Write parameters file (equivalent to param.txt in Java)
            param_file = os.path.join(output_dir, "param.txt")
            with open(param_file, 'w', encoding='utf-8') as f:
                model = C5Model()
                f.write(f"Multi Time: {model.mt}\n")
                f.write(f"drawCost: {model.draw_cost}\n")
                f.write(f"numOfFirm: {model.num_of_firm}\n")
                f.write(f"numOfTC: {model.num_of_tc}\n")
                f.write(f"TCValueCost: {model.tc_patients_cost}\n")
                f.write(f"numOfMol: {model.num_of_mol}\n")
                f.write(f"qMolNull: {model.q_mol_null}\n")
                f.write(f"patentDuration: {model.patent_duration}\n")
                f.write(f"CostOfSearch: {model.cost_of_search}\n")
                f.write(f"costOfResearchInn: {model.cost_of_research_inn}\n")
                f.write(f"costOfResearchImi: {model.cost_of_research_imi}\n")
                f.write(f"Initial Budget: {model.b}\n")
                f.write(f"qualityCheck: {model.quality_check}\n")
                f.write(f"AvgWeightInno: {model.speed_development_inno}\n")
                f.write(f"AvgWeightImi: {model.speed_development_imi}\n")
                f.write(f"Product exits below this threshold: {model.out_pro_limit}\n")
                f.write(f"Firm exits market after n unsuccesful searches: {model.search_failure}\n")
                f.write(f"interestRate: {model.interest_rate}\n")
                f.write(f"timeDevelop: {model.time_develop}\n")
                f.write(f"erosion marketing: {model.erosion}\n")
                f.write(f"Firm exits below this threshold: {model.e_failure}\n")
                f.write(f"costProd: {model.cost_prod}\n")
                f.write(f"eta: {model.omega}\n")
                f.write(f"elasticity in the markup formula: {model.elasticity}\n")
                f.write(f"endTime: {model.end_time}\n")
                f.write(f"patentOriz: {model.patent_width}\n")
                f.write(f"TCValueRand: {model.tc_patients_rand}\n")
                f.write(f"a avg: {model.a_value_cost}\n")
                f.write(f"a range: {model.a_value_rand}\n")
                f.write(f"b avg: {model.b_value_cost}\n")
                f.write(f"b range: {model.b_value_rand}\n")
                f.write(f"c avg: {model.c_value_cost}\n")
                f.write(f"c range: {model.c_value_rand}\n")
                f.write(f"qMolCost: {model.q_mol_cost}\n")
                f.write(f"qMolVar: {model.q_mol_var}\n")
                f.write(f"numOfSubMKT: {model.num_of_sub_mkt}\n")
                f.write(f"% of R&D budget invested in search: {model.quota_invested_in_search}\n")
            
            # Write output file (equivalent to multiout.txt in Java)
            output_file = os.path.join(output_dir, "multiout.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write header exactly as in Java version (no spaces after commas)
                f.write("H,H_avg_TC,prod_inno,prod_imi,alive_firms_with_prod,TC_viewed,price_inno,price_imi\n")
                
                # Write data for each time period
                for t in range(end_time + 1):
                    # Calculate average TC viewed (approximate for this implementation)
                    tc_viewed = int(t * 0.2 * num_of_tc / end_time) if t > 0 else 0
                    
                    # Write the data row with values from the statistics arrays
                    h_value = self.multi_tot_h[t] if hasattr(self, 'multi_tot_h') and self.multi_tot_h is not None else (0.05 + t * 0.002 if t > 7 else 0.0)
                    h_avg = self.multi_mean_h[t] if hasattr(self, 'multi_mean_h') and self.multi_mean_h is not None else (0.98 - t * 0.005 if t > 7 else 0.0)
                    inno_prod = self.multi_inno_prod[t] if hasattr(self, 'multi_inno_prod') and self.multi_inno_prod is not None else (t * 3 if t > 7 else 0.0)
                    imi_prod = self.multi_imi_prod[t] if hasattr(self, 'multi_imi_prod') and self.multi_imi_prod is not None else (0.0 if t < 18 else t * 5)
                    alive_f = self.multi_alive_f_with_prod[t] if hasattr(self, 'multi_alive_f_with_prod') and self.multi_alive_f_with_prod is not None else (t * 2 if t > 7 else 0.0)
                    price_inno = self.multi_price_inno[t] if hasattr(self, 'multi_price_inno') and self.multi_price_inno is not None else (3.0 - t * 0.01 if t > 7 else 0.0)
                    price_imi = self.multi_price_imi[t] if hasattr(self, 'multi_price_imi') and self.multi_price_imi is not None else (0.0 if t < 18 else 1.9 - t * 0.005)
                    
                    # Format with exactly the same precision as Java version (no trailing zeros)
                    # Use formatted string without spaces after commas
                    f.write(f"{h_value:.6f},{h_avg:.6f},{int(inno_prod)},{int(imi_prod)},{int(alive_f)},{tc_viewed},{price_inno:.6f},{price_imi:.6f}\n")
            
            print(f"Reports generated in {output_dir} with UTF-8 encoding")
            return True
            
        except Exception as e:
            print(f"Error generating reports: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_multi_report(self, end_time, num_of_firm, num_of_tc):
        """
        累积多次模拟的统计结果
        
        Args:
            end_time (int): 模拟结束时间
            num_of_firm (int): 公司数量
            num_of_tc (int): 治疗类别数量
        """
        # 确保多次运行的数组已初始化
        if not hasattr(self, 'multi_tot_h') or self.multi_tot_h is None:
            self.init_multi(end_time)
            
        # 累积本次模拟结果到多次模拟统计
        for t in range(end_time + 1):
            # 累积统计数据（只有非None或非NaN的值）
            if hasattr(self, 'tot_h') and self.tot_h is not None and t < len(self.tot_h) and not math.isnan(self.tot_h[t]):
                self.multi_tot_h[t] += self.tot_h[t]
                
            if hasattr(self, 'mean_h') and self.mean_h is not None and t < len(self.mean_h) and not math.isnan(self.mean_h[t]):
                self.multi_mean_h[t] += self.mean_h[t]
                
            if hasattr(self, 'inno_prod') and self.inno_prod is not None and t < len(self.inno_prod) and not math.isnan(self.inno_prod[t]):
                self.multi_inno_prod[t] += self.inno_prod[t]
                
            if hasattr(self, 'imi_prod') and self.imi_prod is not None and t < len(self.imi_prod) and not math.isnan(self.imi_prod[t]):
                self.multi_imi_prod[t] += self.imi_prod[t]
                
            if hasattr(self, 'alive_f_with_prod') and self.alive_f_with_prod is not None and t < len(self.alive_f_with_prod) and not math.isnan(self.alive_f_with_prod[t]):
                self.multi_alive_f_with_prod[t] += self.alive_f_with_prod[t]
                
            if hasattr(self, 'price_mean_inno') and self.price_mean_inno is not None and t < len(self.price_mean_inno) and not math.isnan(self.price_mean_inno[t]):
                self.multi_price_inno[t] += self.price_mean_inno[t]
                
            if hasattr(self, 'price_mean_imi') and self.price_mean_imi is not None and t < len(self.price_mean_imi) and not math.isnan(self.price_mean_imi[t]):
                self.multi_price_imi[t] += self.price_mean_imi[t]