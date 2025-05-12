#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np

"""
@author Gianluca Capone & Davide Sgobba
Converted to Python by AI

This class contains all elements to store and produce the relevant
statistics from the simulation model in the case of sensitivity analysis
"""
class SA_Statistics:
    
    def __init__(self, model):
        """
        Initialize SA_Statistics class
        
        Args:
            model: C3Model object
        """
        # TECHNICAL VARIABLES AND OBJECTS
        self.model = model
        # Access to simulation data
        
        # Names of output files - 确保文件扩展名正确
        self.name_sens_herf_LO = "sa_herfLO.csv"
        self.name_sens_herf_SUI = "sa_herfSUI.csv"
        self.name_sens_enter_firms_1st_LO = "sa_firm1stLO.csv"
        self.name_sens_enter_firms_2nd_LO = "sa_firm2ndLO.csv"
        self.name_sens_enter_firms_3rd_SUI = "sa_firm3rdSUI.csv"
        self.name_sens_enter_firms_2nd_SUI = "sa_firm2ndSUI.csv"
        self.name_sens_share_2nd_SUI = "sa_share2ndSUI.csv"
        self.name_sens_share_3rd_SUI = "sa_share3rdSUI.csv"
        self.name_sens_share_best2nd_SUI = "sa_shareb2ndSUI.csv"
        self.name_sens_share_1st_LO = "sa_share1stLO.csv"
        self.name_sens_share_2nd_LO = "sa_share2ndLO.csv"
        self.name_sens_parameters = "sa_parameters.csv"
        
        # Output file objects
        self.file_sens_herf_LO = None
        self.file_sens_herf_SUI = None
        self.file_sens_enter_firms_1st_LO = None
        self.file_sens_enter_firms_2nd_LO = None
        self.file_sens_enter_firms_3rd_SUI = None
        self.file_sens_enter_firms_2nd_SUI = None
        self.file_sens_share_2nd_SUI = None
        self.file_sens_share_3rd_SUI = None
        self.file_sens_share_best2nd_SUI = None
        self.file_sens_share_1st_LO = None
        self.file_sens_share_2nd_LO = None
        self.file_sens_parameters = None
        
        # STATS VARIABLES - 使用列表存储NumPy数组
        # 为敏感性分析存储的统计量使用NumPy数组提高计算效率
        self.sens_herf_LO = []
        self.sens_herf_SUI = []
        self.sens_enter_firms_1st_LO = []
        self.sens_enter_firms_2nd_LO = []
        self.sens_enter_firms_3rd_SUI = []
        self.sens_enter_firms_2nd_SUI = []
        self.sens_share_2nd_SUI = []
        self.sens_share_3rd_SUI = []
        self.sens_share_best2nd_SUI = []
        self.sens_share_1st_LO = []
        self.sens_share_2nd_LO = []
        self.sens_parameters = []
    
    def close_file(self):
        """This is a method to close the output file objects"""
        file_list = [
            self.file_sens_herf_LO,
            self.file_sens_herf_SUI,
            self.file_sens_enter_firms_1st_LO,
            self.file_sens_enter_firms_2nd_LO,
            self.file_sens_enter_firms_3rd_SUI,
            self.file_sens_enter_firms_2nd_SUI,
            self.file_sens_share_2nd_SUI,
            self.file_sens_share_3rd_SUI,
            self.file_sens_share_best2nd_SUI,
            self.file_sens_share_1st_LO,
            self.file_sens_share_2nd_LO,
            self.file_sens_parameters
        ]
        
        for file in file_list:
            try:
                if file:
                    file.flush()
                    file.close()
            except Exception as e:
                print(e)
    
    def open_file(self):
        """This is a method to initialize the output file objects"""
        # 不再需要移除文件名开头的斜杠
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_herf_LO)
            print(f"Creating output file: {output_path}")
            self.file_sens_herf_LO = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_herf_LO}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_herf_SUI)
            print(f"Creating output file: {output_path}")
            self.file_sens_herf_SUI = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_herf_SUI}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_enter_firms_1st_LO)
            print(f"Creating output file: {output_path}")
            self.file_sens_enter_firms_1st_LO = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_enter_firms_1st_LO}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_enter_firms_2nd_LO)
            print(f"Creating output file: {output_path}")
            self.file_sens_enter_firms_2nd_LO = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_enter_firms_2nd_LO}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_enter_firms_3rd_SUI)
            print(f"Creating output file: {output_path}")
            self.file_sens_enter_firms_3rd_SUI = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_enter_firms_3rd_SUI}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_enter_firms_2nd_SUI)
            print(f"Creating output file: {output_path}")
            self.file_sens_enter_firms_2nd_SUI = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_enter_firms_2nd_SUI}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_share_2nd_SUI)
            print(f"Creating output file: {output_path}")
            self.file_sens_share_2nd_SUI = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_share_2nd_SUI}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_share_3rd_SUI)
            print(f"Creating output file: {output_path}")
            self.file_sens_share_3rd_SUI = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_share_3rd_SUI}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_share_best2nd_SUI)
            print(f"Creating output file: {output_path}")
            self.file_sens_share_best2nd_SUI = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_share_best2nd_SUI}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_share_1st_LO)
            print(f"Creating output file: {output_path}")
            self.file_sens_share_1st_LO = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_share_1st_LO}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_share_2nd_LO)
            print(f"Creating output file: {output_path}")
            self.file_sens_share_2nd_LO = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_share_2nd_LO}: {e}")
            
        try:
            output_path = os.path.join(self.model.path_results, self.name_sens_parameters)
            print(f"Creating output file: {output_path}")
            self.file_sens_parameters = open(output_path, 'w')
        except Exception as e:
            print(f"Error opening {self.name_sens_parameters}: {e}")
    
    # The following are ancillary methods to write data in the output file objects
    def print_sens_herf_LO(self, string):
        try:
            self.file_sens_herf_LO.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_herf_SUI(self, string):
        try:
            self.file_sens_herf_SUI.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_enter_firms_1st_LO(self, string):
        try:
            self.file_sens_enter_firms_1st_LO.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_enter_firms_2nd_LO(self, string):
        try:
            self.file_sens_enter_firms_2nd_LO.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_enter_firms_3rd_SUI(self, string):
        try:
            self.file_sens_enter_firms_3rd_SUI.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_enter_firms_2nd_SUI(self, string):
        try:
            self.file_sens_enter_firms_2nd_SUI.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_share_2nd_SUI(self, string):
        try:
            self.file_sens_share_2nd_SUI.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_share_3rd_SUI(self, string):
        try:
            self.file_sens_share_3rd_SUI.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_share_best2nd_SUI(self, string):
        try:
            self.file_sens_share_best2nd_SUI.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_share_1st_LO(self, string):
        try:
            self.file_sens_share_1st_LO.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_share_2nd_LO(self, string):
        try:
            self.file_sens_share_2nd_LO.write(string)
        except Exception as e:
            print(e)
    
    def print_sens_parameters(self, string):
        try:
            self.file_sens_parameters.write(string)
        except Exception as e:
            print(e)
    
    # The following are ancillary methods to transfer data from the regular
    # statistics object to the sensitivity analysis storage objects
    def copy_values(self, input_list, output_list):
        """
        Copy values from one list to another
        
        Args:
            input_list: source list
            output_list: destination list
        """
        # 优化策略：如果是NumPy数组，使用array.copy()或np.copy()
        if isinstance(input_list, np.ndarray):
            # 创建NumPy数组的副本
            return input_list.copy().astype(str)
        else:
            # 原有逻辑：不是NumPy数组时执行复制
            for i in range(len(input_list)):
                output_list[i] = str(input_list[i])
            return output_list
    
    def copy_values_param(self, input_param, output_list):
        """
        Copy values from parameters to a list
        
        Args:
            input_param: source parameter array
            output_list: destination list
        """
        # 将参数复制为NumPy数组
        for i in range(len(input_param)):
            output_list[i] = input_param[i].get_value()
        return output_list
    
    def make_statistics(self):
        """
        This method gets data from the current simulation run and stores them
        into the storage objects
        """
        end_time = self.model.end_time
        
        # 使用NumPy创建数据数组，提高效率
        # 创建和初始化存储数组
        herf_lo_array = np.zeros(end_time + 1, dtype=np.str_)
        herf_sui_array = np.zeros(end_time + 1, dtype=np.str_)
        enter_firms_1st_lo_array = np.zeros(end_time + 1, dtype=np.str_)
        enter_firms_2nd_lo_array = np.zeros(end_time + 1, dtype=np.str_)
        enter_firms_3rd_sui_array = np.zeros(end_time + 1, dtype=np.str_)
        enter_firms_2nd_sui_array = np.zeros(end_time + 1, dtype=np.str_)
        share_2nd_sui_array = np.zeros(end_time + 1, dtype=np.str_)
        share_3rd_sui_array = np.zeros(end_time + 1, dtype=np.str_)
        share_best2nd_sui_array = np.zeros(end_time + 1, dtype=np.str_)
        share_1st_lo_array = np.zeros(end_time + 1, dtype=np.str_)
        share_2nd_lo_array = np.zeros(end_time + 1, dtype=np.str_)
        
        # 复制数据，统一处理
        if isinstance(self.model.stat.herf_LO, np.ndarray):
            herf_lo_array = self.model.stat.herf_LO.copy().astype(str)
            herf_sui_array = self.model.stat.herf_SUI.copy().astype(str)
            enter_firms_1st_lo_array = self.model.stat.enter_firms_1st_LO.copy().astype(str)
            enter_firms_2nd_lo_array = self.model.stat.enter_firms_2nd_LO.copy().astype(str)
            enter_firms_3rd_sui_array = self.model.stat.enter_firms_3rd_SUI.copy().astype(str)
            enter_firms_2nd_sui_array = self.model.stat.enter_firms_2nd_SUI.copy().astype(str)
            share_2nd_sui_array = self.model.stat.share_2nd_SUI.copy().astype(str)
            share_3rd_sui_array = self.model.stat.share_3rd_SUI.copy().astype(str)
            share_best2nd_sui_array = self.model.stat.share_best2nd_SUI.copy().astype(str)
            share_1st_lo_array = self.model.stat.share_1st_LO.copy().astype(str)
            share_2nd_lo_array = self.model.stat.share_2nd_LO.copy().astype(str)
        else:
            # 处理非NumPy数组的情况
            herf_lo_array = np.array([str(v) for v in self.model.stat.herf_LO])
            herf_sui_array = np.array([str(v) for v in self.model.stat.herf_SUI])
            enter_firms_1st_lo_array = np.array([str(v) for v in self.model.stat.enter_firms_1st_LO])
            enter_firms_2nd_lo_array = np.array([str(v) for v in self.model.stat.enter_firms_2nd_LO])
            enter_firms_3rd_sui_array = np.array([str(v) for v in self.model.stat.enter_firms_3rd_SUI])
            enter_firms_2nd_sui_array = np.array([str(v) for v in self.model.stat.enter_firms_2nd_SUI])
            share_2nd_sui_array = np.array([str(v) for v in self.model.stat.share_2nd_SUI])
            share_3rd_sui_array = np.array([str(v) for v in self.model.stat.share_3rd_SUI])
            share_best2nd_sui_array = np.array([str(v) for v in self.model.stat.share_best2nd_SUI])
            share_1st_lo_array = np.array([str(v) for v in self.model.stat.share_1st_LO])
            share_2nd_lo_array = np.array([str(v) for v in self.model.stat.share_2nd_LO])
        
        # 参数数组处理
        param_array = np.empty(200, dtype=object)
        for i in range(200):
            if self.model.parameters[i] is not None:
                param_array[i] = self.model.parameters[i].get_value()
            else:
                param_array[i] = "0.0"
        
        # 将数组添加到存储中
        self.sens_herf_LO.append(herf_lo_array)
        self.sens_herf_SUI.append(herf_sui_array)
        self.sens_enter_firms_1st_LO.append(enter_firms_1st_lo_array)
        self.sens_enter_firms_2nd_LO.append(enter_firms_2nd_lo_array)
        self.sens_enter_firms_3rd_SUI.append(enter_firms_3rd_sui_array)
        self.sens_enter_firms_2nd_SUI.append(enter_firms_2nd_sui_array)
        self.sens_share_2nd_SUI.append(share_2nd_sui_array)
        self.sens_share_3rd_SUI.append(share_3rd_sui_array)
        self.sens_share_best2nd_SUI.append(share_best2nd_sui_array)
        self.sens_share_1st_LO.append(share_1st_lo_array)
        self.sens_share_2nd_LO.append(share_2nd_lo_array)
        self.sens_parameters.append(param_array)
    
    def print_statistics(self):
        """
        This method writes data in the output file in case of sensitivity
        analysis
        """
        # 使用矢量化批处理打印大量数据
        # 为提高IO效率，采用批量写入策略
        
        # 函数帮助批量打印数据
        def print_array_data(print_func, data_list):
            """批量处理和打印数组数据"""
            for i, array in enumerate(data_list):
                line = f"{i};"
                # 连接所有数据项，只在处理较大范围时才使用NumPy操作
                if len(array) > 100 and hasattr(array, 'size') and array.size > 100:
                    # 大型NumPy数组使用向量化处理
                    items = [f"{x};" for x in array[1:self.model.end_time+1]]
                    line += "".join(items)
                else:
                    # 小型数组或非NumPy对象用循环处理
                    for t in range(1, self.model.end_time + 1):
                        if t < len(array):
                            line += f"{array[t]};"
                        else:
                            line += "0.0;"
                
                line += "\n"
                print_func(line)
        
        # 使用批量打印函数打印所有统计数据
        print_array_data(self.print_sens_herf_LO, self.sens_herf_LO)
        print_array_data(self.print_sens_herf_SUI, self.sens_herf_SUI)
        print_array_data(self.print_sens_enter_firms_1st_LO, self.sens_enter_firms_1st_LO)
        print_array_data(self.print_sens_enter_firms_2nd_LO, self.sens_enter_firms_2nd_LO)
        print_array_data(self.print_sens_enter_firms_3rd_SUI, self.sens_enter_firms_3rd_SUI)
        print_array_data(self.print_sens_enter_firms_2nd_SUI, self.sens_enter_firms_2nd_SUI)
        print_array_data(self.print_sens_share_2nd_SUI, self.sens_share_2nd_SUI)
        print_array_data(self.print_sens_share_3rd_SUI, self.sens_share_3rd_SUI)
        print_array_data(self.print_sens_share_best2nd_SUI, self.sens_share_best2nd_SUI)
        print_array_data(self.print_sens_share_1st_LO, self.sens_share_1st_LO)
        print_array_data(self.print_sens_share_2nd_LO, self.sens_share_2nd_LO)
        
        # 参数数据的处理方式略有不同
        for i, params in enumerate(self.sens_parameters):
            line = f"{i};"
            # 参数通常较少，使用简单循环即可
            for t in range(1, len(params)):
                if params[t] is not None:
                    line += f"{params[t]};"
                else:
                    line += "0.0;"
            line += "\n"
            self.print_sens_parameters(line) 