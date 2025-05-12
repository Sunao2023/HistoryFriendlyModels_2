#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import io
import numpy as np

"""
@author Gianluca Capone & Davide Sgobba
Converted to Python by AI

This class contains all elements to store and produce the relevant
statistics from the simulation model in the case of a single run or of
multiple runs
"""
class Statistics:
    
    def __init__(self, model, is_single=False):
        """
        Initialize Statistics class
        
        Args:
            model: C3Model object
            is_single: boolean, True for single simulation, False for multiple simulation
        """
        # TECHNICAL VARIABLES AND OBJECTS
        self.model = model
        # Access to simulation data
        self.file_output = None
        # Output file object of a single or multiple simulation
        
        # STATS VARIABLES
        # These elements are used in both the single and the multiple runs
        # simulation. They can be used to reproduce exactly figures 3.6-3.9 and
        # with suitable changes in the values of parameters figures 3.10-3.13
        
        # 初始化统计数组 - 使用NumPy数组提高性能
        if is_single:
            # 单次模拟初始化为列表，用于动态添加
            self.herf_LO = []
            self.herf_SUI = []
            self.enter_firms_1st_LO = []
            self.enter_firms_2nd_LO = []
            self.enter_firms_2nd_SUI = []
            self.enter_firms_3rd_SUI = []
            self.share_1st_LO = []
            self.share_2nd_LO = []
            self.share_3rd_SUI = []
            self.share_2nd_SUI = []
            self.share_best2nd_SUI = []
            
            # These elements are used only in the single run simulation. They can be
            # used to have a closer look in the dynamics of single simulation run.
            # Performance and cheapness data can be used to reconstruct firm
            # trajectories in the technological space, as in figures 3.3-3.5
            
            # 使用更高效的数据结构存储单次模拟的结果
            # 预先分配列表，避免动态扩展
            self.single_share = [[] for _ in range(model.end_time)]
            self.single_mod = [[] for _ in range(model.end_time)]
            self.single_cheapness = [[] for _ in range(model.end_time)]
            self.single_performance = [[] for _ in range(model.end_time)]
            self.single_served_user_class = [[] for _ in range(model.end_time)]
        else:
            # 多次模拟使用NumPy数组提高计算效率
            self.herf_LO = np.zeros(model.end_time + 1, dtype=np.float64)
            self.herf_SUI = np.zeros(model.end_time + 1, dtype=np.float64)
            self.enter_firms_1st_LO = np.zeros(model.end_time + 1, dtype=np.float64)
            self.enter_firms_2nd_LO = np.zeros(model.end_time + 1, dtype=np.float64)
            self.enter_firms_2nd_SUI = np.zeros(model.end_time + 1, dtype=np.float64)
            self.enter_firms_3rd_SUI = np.zeros(model.end_time + 1, dtype=np.float64)
            self.share_1st_LO = np.zeros(model.end_time + 1, dtype=np.float64)
            self.share_2nd_LO = np.zeros(model.end_time + 1, dtype=np.float64)
            self.share_3rd_SUI = np.zeros(model.end_time + 1, dtype=np.float64)
            self.share_2nd_SUI = np.zeros(model.end_time + 1, dtype=np.float64)
            self.share_best2nd_SUI = np.zeros(model.end_time + 1, dtype=np.float64)
    
    def close_file(self):
        """This is a method to close the output file object"""
        try:
            self.file_output.flush()
            self.file_output.close()
        except Exception as e:
            print(e)
    
    def open_file(self, name_output):
        """This is a method to initialize the output file object"""
        try:
            # 移除name_output开头的斜杠，防止路径解析问题
            if name_output.startswith("/"):
                name_output = name_output[1:]
            
            output_path = os.path.join(self.model.path_results, name_output)
            print(f"Creating output file: {output_path}")
            self.file_output = open(output_path, 'w')
            print(f"Output file created successfully")
        except Exception as e:
            print(f"Error opening output file: {e}")
    
    def print(self, string):
        """This is an ancillary method to write data in the output file object"""
        try:
            self.file_output.write(string)
        except Exception as e:
            print(e)
    
    def make_single_statistics(self):
        """
        This method gets data from the current simulation run and stores them
        into the storage objects in case of a single simulation
        """
        # Store firm specific data - 预先估计最大企业数量，避免动态扩展
        timer_idx = self.model.timer - 1
        num_firms = self.model.computer_industry.number_of_firms
        
        # 预分配数组
        if timer_idx < len(self.single_share):
            self.single_share[timer_idx] = []
            self.single_mod[timer_idx] = []
            self.single_cheapness[timer_idx] = []
            self.single_performance[timer_idx] = []
            self.single_served_user_class[timer_idx] = []
        
        # 一次性收集所有企业数据，然后批量添加
        share_data = []
        mod_data = []
        cheap_data = []
        perf_data = []
        user_class_data = []
        
        for f in range(1, num_firms + 1):
            firm = self.model.computer_industry.firms[f]
            
            share_data.append(firm.share)
            mod_data.append(firm.mod)
            cheap_data.append(firm.computer.cheap)
            perf_data.append(firm.computer.perf)
            
            if not firm.entered:
                user_class_data.append("NONE")
            else:
                if firm.served_user_class == self.model.large_orgs:
                    user_class_data.append("LO")
                if firm.served_user_class == self.model.small_users:
                    user_class_data.append("SUI")
        
        # 批量添加数据
        self.single_share[timer_idx].extend(share_data)
        self.single_mod[timer_idx].extend(mod_data)
        self.single_cheapness[timer_idx].extend(cheap_data)
        self.single_performance[timer_idx].extend(perf_data)
        self.single_served_user_class[timer_idx].extend(user_class_data)
        
        # Store market statistics
        self.herf_LO.append(self.model.large_orgs.herfindahl)
        self.herf_SUI.append(self.model.small_users.herfindahl)
        self.enter_firms_1st_LO.append(self.model.large_orgs.num_of_first_gen_firms)
        self.enter_firms_2nd_LO.append(self.model.large_orgs.num_of_second_gen_firms)
        self.enter_firms_2nd_SUI.append(self.model.small_users.num_of_second_gen_firms)
        self.enter_firms_3rd_SUI.append(self.model.small_users.num_of_diversified_firms)
        self.share_1st_LO.append(self.model.large_orgs.share_1st_gen)
        self.share_2nd_LO.append(self.model.large_orgs.share_2nd_gen)
        self.share_2nd_SUI.append(self.model.small_users.share_2nd_gen)
        self.share_best2nd_SUI.append(self.model.small_users.share_best_2nd)
        self.share_3rd_SUI.append(self.model.small_users.share_div)
    
    def make_statistics(self):
        """
        This method gets data from the current simulation run and stores them
        into the storage objects in case of a multiple simulation
        """
        timer = self.model.timer
        multi_time = float(self.model.multi_time)  # 转换为浮点数避免整除
        
        # 使用NumPy数组的矢量化操作提高性能
        # 提前计算除数，减少重复计算
        div_factor = 1.0 / multi_time
        
        # 使用高效的NumPy数组原位操作
        self.herf_LO[timer] += self.model.large_orgs.herfindahl * div_factor
        self.herf_SUI[timer] += self.model.small_users.herfindahl * div_factor
        self.enter_firms_1st_LO[timer] += self.model.large_orgs.num_of_first_gen_firms * div_factor
        self.enter_firms_2nd_LO[timer] += self.model.large_orgs.num_of_second_gen_firms * div_factor
        self.enter_firms_2nd_SUI[timer] += self.model.small_users.num_of_second_gen_firms * div_factor
        self.enter_firms_3rd_SUI[timer] += self.model.small_users.num_of_diversified_firms * div_factor
        self.share_1st_LO[timer] += self.model.large_orgs.share_1st_gen * div_factor
        self.share_2nd_LO[timer] += self.model.large_orgs.share_2nd_gen * div_factor
        self.share_2nd_SUI[timer] += self.model.small_users.share_2nd_gen * div_factor
        self.share_best2nd_SUI[timer] += self.model.small_users.share_best_2nd * div_factor
        self.share_3rd_SUI[timer] += self.model.small_users.share_div * div_factor
    
    def print_multi_statistics(self):
        """
        This method writes data in the output file in case of multiple
        simulation
        """
        # Herfindahl indices
        self.print("Herfindahl in PC and mainframe markets\n")
        self.print("MF;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.herf_LO[t]};")
        self.print("\n")
        self.print("PC;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.herf_SUI[t]};")
        self.print("\n")
        
        # Mainframe market firms
        self.print("\nNumber of firms in mainframe market\n")
        self.print("1st gen firms;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.enter_firms_1st_LO[t]};")
        self.print("\n")
        self.print("2nd gen firms;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.enter_firms_2nd_LO[t]};")
        self.print("\n")
        self.print("Total number;")
        
        # 使用NumPy向量化操作加速计算
        if isinstance(self.enter_firms_1st_LO, np.ndarray) and isinstance(self.enter_firms_2nd_LO, np.ndarray):
            # 使用NumPy的矢量化操作一次计算所有总数
            total_mf = self.enter_firms_1st_LO[1:self.model.end_time+1] + self.enter_firms_2nd_LO[1:self.model.end_time+1]
            for t in range(self.model.end_time):
                self.print(f"{total_mf[t]};")
        else:
            # 如果不是NumPy数组，则使用循环计算
            for t in range(1, self.model.end_time + 1):
                total_mf = self.enter_firms_1st_LO[t] + self.enter_firms_2nd_LO[t]
                self.print(f"{total_mf};")
        
        self.print("\n")
        
        # PC market firms
        self.print("\nNumber of firms in PC market\n")
        self.print("MP start-ups;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.enter_firms_2nd_SUI[t]};")
        self.print("\n")
        self.print("Diversified firms;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.enter_firms_3rd_SUI[t]};")
        self.print("\n")
        self.print("Total number;")
        
        # 使用NumPy向量化操作加速计算
        if isinstance(self.enter_firms_2nd_SUI, np.ndarray) and isinstance(self.enter_firms_3rd_SUI, np.ndarray):
            # 使用NumPy的矢量化操作一次计算所有总数
            total_pc = self.enter_firms_2nd_SUI[1:self.model.end_time+1] + self.enter_firms_3rd_SUI[1:self.model.end_time+1]
            for t in range(self.model.end_time):
                self.print(f"{total_pc[t]};")
        else:
            # 如果不是NumPy数组，则使用循环计算
            for t in range(1, self.model.end_time + 1):
                total_pc = self.enter_firms_2nd_SUI[t] + self.enter_firms_3rd_SUI[t]
                self.print(f"{total_pc};")
                
        self.print("\n")
        
        # PC market share
        self.print("\nMarket share in PC market\n")
        self.print("Total MP start-ups;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.share_2nd_SUI[t]};")
        self.print("\n")
        self.print("Diversified firms;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.share_3rd_SUI[t]};")
        self.print("\n")
        self.print("Best MP start-up;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.share_best2nd_SUI[t]};")
        self.print("\n")
        
        # Mainframe market share
        self.print("\nMarket share in Mainframe market\n")
        self.print("1st gen firms;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.share_1st_LO[t]};")
        self.print("\n")
        self.print("2nd gen firms;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.share_2nd_LO[t]};")
        self.print("\n")
    
    def print_single_statistics(self):
        """
        This method writes data in the output file in case of single
        simulation
        """
        # Main statistics
        self.print("Main Statistics\n\n")
        self.print("T;HLO;F1stLO;F2ndLO;S1stLO;S2ndLO;HSUI;F2ndSUI;F3rdSUI;S2ndSUI;S3rdSUI;SB2ndSUI\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            self.print(f"{self.herf_LO[t-1]};")
            self.print(f"{self.enter_firms_1st_LO[t-1]};")
            self.print(f"{self.enter_firms_2nd_LO[t-1]};")
            self.print(f"{self.share_1st_LO[t-1]};")
            self.print(f"{self.share_2nd_LO[t-1]};")
            self.print(f"{self.herf_SUI[t-1]};")
            self.print(f"{self.enter_firms_2nd_SUI[t-1]};")
            self.print(f"{self.enter_firms_3rd_SUI[t-1]};")
            self.print(f"{self.share_2nd_SUI[t-1]};")
            self.print(f"{self.share_3rd_SUI[t-1]};")
            self.print(f"{self.share_best2nd_SUI[t-1]}\n")
        
        # Computer Firm MOD
        self.print("\nComputerFirm MOD\n")
        self.print("FIRM;")
        for f in range(1, len(self.single_mod[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        self.print("T;")
        for f in range(1, len(self.single_mod[self.model.end_time-1]) + 1):
            self.print(f"{self.single_served_user_class[self.model.end_time-1][f-1]};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_mod[t-1]) + 1):
                self.print(f"{self.single_mod[t-1][f-1]};")
            self.print("\n")
        
        # Computer Firm SHARE
        self.print("\nComputerFirm SHARE \n")
        self.print("FIRM;")
        for f in range(1, len(self.single_share[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        self.print("T;")
        for f in range(1, len(self.single_mod[self.model.end_time-1]) + 1):
            self.print(f"{self.single_served_user_class[self.model.end_time-1][f-1]};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_share[t-1]) + 1):
                self.print(f"{self.single_share[t-1][f-1]};")
            self.print("\n")
        
        # Computer Firms Cheapness
        self.print("\nComputerFirms Cheapness \n")
        self.print("FIRM;")
        for f in range(1, len(self.single_cheapness[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        self.print("T;")
        for f in range(1, len(self.single_mod[self.model.end_time-1]) + 1):
            self.print(f"{self.single_served_user_class[self.model.end_time-1][f-1]};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_cheapness[t-1]) + 1):
                self.print(f"{self.single_cheapness[t-1][f-1]};")
            self.print("\n")
        
        # Computer Firms Performance
        self.print("\nComputerFirms Performance \n")
        self.print("FIRM;")
        for f in range(1, len(self.single_performance[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        self.print("T;")
        for f in range(1, len(self.single_mod[self.model.end_time-1]) + 1):
            self.print(f"{self.single_served_user_class[self.model.end_time-1][f-1]};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_performance[t-1]) + 1):
                self.print(f"{self.single_performance[t-1][f-1]};")
            self.print("\n") 