#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics模块 - Statistics类的Python实现
转换自Java版本的Statistics.java
"""

import os

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含存储和计算相关统计数据的所有变量和方法
"""
class Statistics:
    
    def __init__(self, model, is_single):
        """
        构造函数
        
        Args:
            model: 模型对象引用
            is_single: 是否为单次模拟
        """
        # 模型引用
        self.model = model
        
        # 技术变量和对象
        self.file_output = None  # 单次或多次模拟的输出文件对象
        
        # 统计变量
        # 这些元素在单次和多次模拟中都使用。它们可以用来精确地复现图4.1，
        # 并通过适当地修改参数值来复现图4.2-4.5
        self.alive_firms_mf = []   # 主机市场中活跃公司数量的存储
        self.alive_firms_pc = []   # PC市场中活跃公司数量的存储
        self.alive_firms_cmp = []  # 组件市场中活跃公司数量的存储
        self.herf_mf = []          # 主机市场中赫芬达尔指数的存储
        self.herf_pc = []          # PC市场中赫芬达尔指数的存储
        self.herf_cmp = []         # 组件市场中赫芬达尔指数的存储
        self.int_firms_mf = []     # 主机市场中集成公司数量的存储
        self.int_firms_pc = []     # PC市场中集成公司数量的存储
        self.int_ratio_mf = []     # 主机市场中集成比例的存储
        self.int_ratio_pc = []     # PC市场中集成比例的存储
        
        # 这些元素仅在单次模拟中使用。它们可以用来更近距离地观察单次模拟运行的动态。
        if is_single:
            self.single_share_mf = [[] for _ in range(model.end_time)]        # 主机市场中个体公司市场份额的存储
            self.single_share_pc = [[] for _ in range(model.end_time)]        # PC市场中个体公司市场份额的存储
            self.single_share_cmp = [[] for _ in range(model.end_time)]       # 组件市场中个体公司市场份额的存储
            self.single_mod_mf = [[] for _ in range(model.end_time)]          # 主机市场中个体公司mod的存储
            self.single_mod_pc = [[] for _ in range(model.end_time)]          # PC市场中个体公司mod的存储
            self.single_mod_cmp = [[] for _ in range(model.end_time)]         # 组件市场中个体公司mod的存储
            self.single_supplier_mf = [[] for _ in range(model.end_time)]     # 主机市场中供应商标识符的存储
            self.single_supplier_pc = [[] for _ in range(model.end_time)]     # PC市场中供应商标识符的存储
            self.single_num_of_buyers_cmp = [[] for _ in range(model.end_time)]  # 组件市场中购买计算机公司数量的存储
        else:
            # 多次模拟需要的初始化
            for t in range(model.end_time + 1):
                self.alive_firms_mf.append(0.0)
                self.alive_firms_pc.append(0.0)
                self.alive_firms_cmp.append(0.0)
                self.herf_mf.append(0.0)
                self.herf_pc.append(0.0)
                self.herf_cmp.append(0.0)
                self.int_firms_mf.append(0.0)
                self.int_firms_pc.append(0.0)
                self.int_ratio_mf.append(0.0)
                self.int_ratio_pc.append(0.0)
        
        # 控制器
        self.is_single = is_single

    def close_file(self):
        """
        关闭输出文件对象的方法
        """
        try:
            if self.file_output:
                self.file_output.flush()
                self.file_output.close()
        except Exception as e:
            print(f"关闭文件时出错: {e}")

    def open_file(self, name_output):
        """
        初始化输出文件对象的方法
        
        Args:
            name_output: 输出文件名
        """
        try:
            self.file_output = open(self.model.path_results + name_output, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")

    def print(self, text):
        """
        在输出文件对象中写入数据的辅助方法
        
        Args:
            text: 要写入的文本
        """
        try:
            if self.file_output:
                self.file_output.write(text)
        except Exception as e:
            print(f"写入文件时出错: {e}")

    def make_single_statistics(self):
        """
        从当前模拟运行中获取数据并在单次模拟的情况下将其存储到存储对象中
        """
        for f in range(1, self.model.mf_market.num_of_firms + 1):
            self.single_mod_mf[self.model.timer - 1].append(self.model.mf_market.firm[f].computer.mod)
            self.single_share_mf[self.model.timer - 1].append(self.model.mf_market.firm[f].share)

            if not self.model.mf_market.firm[f].integrated:
                self.single_supplier_mf[self.model.timer - 1].append(self.model.mf_market.firm[f].supplier_id)
            else:
                self.single_supplier_mf[self.model.timer - 1].append(-1)

        for f in range(1, self.model.pc_market.num_of_firms + 1):
            self.single_mod_pc[self.model.timer - 1].append(self.model.pc_market.firm[f].computer.mod)
            self.single_share_pc[self.model.timer - 1].append(self.model.pc_market.firm[f].share)

            if not self.model.pc_market.firm[f].integrated:
                self.single_supplier_pc[self.model.timer - 1].append(self.model.pc_market.firm[f].supplier_id)
            else:
                self.single_supplier_pc[self.model.timer - 1].append(-1)

        for f in range(1, self.model.cmp_market.num_of_firms + 1):
            self.single_mod_cmp[self.model.timer - 1].append(self.model.cmp_market.firm[f].component.mod)
            self.single_num_of_buyers_cmp[self.model.timer - 1].append(self.model.cmp_market.firm[f].how_many_buyers_mf + 
                                                                        self.model.cmp_market.firm[f].how_many_buyers_pc)
            self.single_share_cmp[self.model.timer - 1].append(self.model.cmp_market.firm[f].share)

        self.alive_firms_mf.append(self.model.mf_market.alive_firms)
        self.alive_firms_pc.append(self.model.pc_market.alive_firms)
        self.alive_firms_cmp.append(self.model.cmp_market.alive_firms)
        self.herf_mf.append(self.model.mf_market.herfindahl_index)
        self.herf_pc.append(self.model.pc_market.herfindahl_index)
        self.herf_cmp.append(self.model.cmp_market.herfindahl_index)
        self.int_firms_mf.append(self.model.mf_market.int_firms)
        self.int_firms_pc.append(self.model.pc_market.int_firms)
        self.int_ratio_mf.append(self.model.mf_market.int_ratio)
        self.int_ratio_pc.append(self.model.pc_market.int_ratio)

    def make_statistics(self):
        """
        从当前模拟运行中获取数据并在多次模拟的情况下将其存储到存储对象中
        """
        self.herf_mf[self.model.timer] = self.herf_mf[self.model.timer] + (self.model.mf_market.herfindahl_index / self.model.multi_time)
        self.herf_pc[self.model.timer] = self.herf_pc[self.model.timer] + (self.model.pc_market.herfindahl_index / self.model.multi_time)
        self.herf_cmp[self.model.timer] = self.herf_cmp[self.model.timer] + (self.model.cmp_market.herfindahl_index / self.model.multi_time)
        self.alive_firms_mf[self.model.timer] = self.alive_firms_mf[self.model.timer] + (self.model.mf_market.alive_firms / self.model.multi_time)
        self.alive_firms_pc[self.model.timer] = self.alive_firms_pc[self.model.timer] + (self.model.pc_market.alive_firms / self.model.multi_time)
        self.alive_firms_cmp[self.model.timer] = self.alive_firms_cmp[self.model.timer] + (self.model.cmp_market.alive_firms / self.model.multi_time)
        self.int_firms_mf[self.model.timer] = self.int_firms_mf[self.model.timer] + (self.model.mf_market.int_firms / self.model.multi_time)
        self.int_firms_pc[self.model.timer] = self.int_firms_pc[self.model.timer] + (self.model.pc_market.int_firms / self.model.multi_time)
        self.int_ratio_mf[self.model.timer] = self.int_ratio_mf[self.model.timer] + (self.model.mf_market.int_ratio / self.model.multi_time)
        self.int_ratio_pc[self.model.timer] = self.int_ratio_pc[self.model.timer] + (self.model.pc_market.int_ratio / self.model.multi_time)

    def print_multi_statistics(self):
        """
        在多次模拟的情况下将数据写入输出文件
        """
        # 写入Herfindahl指数部分
        self.print("Herfindahl index \n")
        self.print("MF;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.herf_mf[t]};")
        self.print("\n")
        self.print("PC;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.herf_pc[t]};")
        self.print("\n")
        self.print("CMP;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.herf_cmp[t]};")
        self.print("\n")
        
        self.print("\nNumber of Firms \n")
        self.print("MF;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.alive_firms_mf[t]};")
        self.print("\n")
        self.print("PC;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.alive_firms_pc[t]};")
        self.print("\n")
        self.print("CMP;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.alive_firms_cmp[t]};")
        self.print("\n")
        
        self.print("\nNumber of Integrated Firms\n")
        self.print("MF;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.int_firms_mf[t]};")
        self.print("\n")
        self.print("PC;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.int_firms_pc[t]};")
        self.print("\n")

        self.print("\n Integration Ratio (number of integrated F/total number of firms)\n")
        self.print("MF;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.int_ratio_mf[t]};")
        self.print("\n")
        self.print("PC;")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{self.int_ratio_pc[t]};")
        self.print("\n")

    def print_single_statistics(self):
        """
        在单次模拟的情况下将数据写入输出文件
        """
        self.print("Main Statistics\n")
        self.print("\n")
        self.print("T;HMF;NMF;INMF;IRMF;HPC;NPC;INPC;IRPC;HCMP;NCMP\n")
        for t in range(1, self.model.end_time):
            self.print(f"{t};")
            self.print(f"{self.herf_mf[t-1]};")
            self.print(f"{self.alive_firms_mf[t-1]};")
            self.print(f"{self.int_firms_mf[t-1]};")
            self.print(f"{self.int_ratio_mf[t-1]};")
            self.print(f"{self.herf_pc[t-1]};")
            self.print(f"{self.alive_firms_pc[t-1]};")
            self.print(f"{self.int_firms_pc[t-1]};")
            self.print(f"{self.int_ratio_pc[t-1]};")
            self.print(f"{self.herf_cmp[t-1]};")
            self.print(f"{self.alive_firms_cmp[t-1]}\n")
        
        self.print("\nComputerFirm MOD\n")
        self.print("T;")
        for f in range(1, len(self.single_mod_mf[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_mod_mf[t-1]) + 1):
                self.print(f"{self.single_mod_mf[t-1][f-1]};")
            self.print("\n")

        self.print("\nMFComputerFirm SHARE \n")
        self.print("T;")
        for f in range(1, len(self.single_share_mf[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_share_mf[t-1]) + 1):
                self.print(f"{self.single_share_mf[t-1][f-1]};")
            self.print("\n")
        
        self.print("\nMFComputerFirms Component supplier \n")
        self.print("T;")
        for f in range(1, len(self.single_supplier_mf[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_supplier_mf[t-1]) + 1):
                self.print(f"{self.single_supplier_mf[t-1][f-1]};")
            self.print("\n")
        
        self.print("\nPC Computer mod\n")
        self.print("T;")
        for f in range(1, len(self.single_mod_pc[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_mod_pc[t-1]) + 1):
                self.print(f"{self.single_mod_pc[t-1][f-1]};")
            self.print("\n")
        
        self.print("\nPCComputerFirm SHARE \n")
        self.print("T;")
        for f in range(1, len(self.single_share_pc[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_share_pc[t-1]) + 1):
                self.print(f"{self.single_share_pc[t-1][f-1]};")
            self.print("\n")
                
        self.print("\nPC ComputerFirms Component supplier \n")
        self.print("T;")
        for f in range(1, len(self.single_supplier_pc[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_supplier_pc[t-1]) + 1):
                self.print(f"{self.single_supplier_pc[t-1][f-1]};")
            self.print("\n")
        
        self.print("\nComponentFirm MOD\n")
        self.print("T;")
        for f in range(1, len(self.single_mod_cmp[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_mod_cmp[t-1]) + 1):
                self.print(f"{self.single_mod_cmp[t-1][f-1]};")
            self.print("\n")
        
        self.print("\nComponentFirms SHARE\n")
        self.print("T;")
        for f in range(1, len(self.single_share_cmp[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_share_cmp[t-1]) + 1):
                self.print(f"{self.single_share_cmp[t-1][f-1]};")
            self.print("\n")
        
        self.print("\nCMP num of buyers\n")
        self.print("T;")
        for f in range(1, len(self.single_num_of_buyers_cmp[self.model.end_time-1]) + 1):
            self.print(f"{f};")
        self.print("\n")
        for t in range(1, self.model.end_time + 1):
            self.print(f"{t};")
            for f in range(1, len(self.single_num_of_buyers_cmp[t-1]) + 1):
                self.print(f"{self.single_num_of_buyers_cmp[t-1][f-1]};")
            self.print("\n") 