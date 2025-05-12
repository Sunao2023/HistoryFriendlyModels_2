#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SA_Statistics模块 - SA_Statistics类的Python实现
转换自Java版本的SA_Statistics.java
"""

"""
@author Gianluca Capone & Davide Sgobba
Python转换

此类包含存储和计算敏感性分析相关统计数据的所有变量和方法
"""
class SA_Statistics:
    
    def __init__(self, model):
        """
        构造函数
        
        Args:
            model: 模型对象引用
        """
        # 模型引用
        self.model = model
        
        # 技术变量和对象
        # 输出文件名称
        self.name_sens_herf_mf = "/sa_herf_MF.csv"
        self.name_sens_herf_pc = "/sa_herf_PC.csv"
        self.name_sens_herf_cmp = "/sa_herf_CMP.csv"
        self.name_sens_alive_firms_mf = "/sa_firms_MF.csv"
        self.name_sens_alive_firms_pc = "/sa_firms_PC.csv"
        self.name_sens_alive_firms_cmp = "/sa_firms_CMP.csv"
        self.name_sens_int_ratio_mf = "/sa_intRat_MF.csv"
        self.name_sens_int_ratio_pc = "/sa_intRat_PC.csv"
        self.name_sens_parameters = "/sa_parameters.csv"
        
        # 输出文件对象
        self.file_sens_herf_mf = None
        self.file_sens_herf_pc = None
        self.file_sens_herf_cmp = None
        self.file_sens_alive_firms_mf = None
        self.file_sens_alive_firms_pc = None
        self.file_sens_alive_firms_cmp = None
        self.file_sens_int_ratio_mf = None
        self.file_sens_int_ratio_pc = None
        self.file_sens_parameters = None
        
        # 统计变量
        self.sens_herf_mf = []         # 主机市场赫芬达尔指数存储
        self.sens_herf_pc = []         # PC市场赫芬达尔指数存储
        self.sens_herf_cmp = []        # 组件市场赫芬达尔指数存储
        self.sens_alive_firms_mf = []  # 主机市场活跃公司数量存储
        self.sens_alive_firms_pc = []  # PC市场活跃公司数量存储
        self.sens_alive_firms_cmp = [] # 组件市场活跃公司数量存储
        self.sens_int_ratio_mf = []    # 主机市场集成比例存储
        self.sens_int_ratio_pc = []    # PC市场集成比例存储
        self.sens_parameters = []      # 模拟运行中使用的参数存储

    def close_file(self):
        """
        关闭输出文件对象的方法
        """
        file_list = [
            self.file_sens_herf_mf, self.file_sens_herf_pc, self.file_sens_herf_cmp,
            self.file_sens_alive_firms_mf, self.file_sens_alive_firms_pc, self.file_sens_alive_firms_cmp,
            self.file_sens_int_ratio_mf, self.file_sens_int_ratio_pc, self.file_sens_parameters
        ]
        
        for file in file_list:
            try:
                if file:
                    file.flush()
                    file.close()
            except Exception as e:
                print(f"关闭文件时出错: {e}")

    def open_file(self):
        """
        初始化输出文件对象的方法
        """
        try:
            self.file_sens_herf_mf = open(self.model.path_results + self.name_sens_herf_mf, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")
        
        try:
            self.file_sens_herf_pc = open(self.model.path_results + self.name_sens_herf_pc, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")
        
        try:
            self.file_sens_herf_cmp = open(self.model.path_results + self.name_sens_herf_cmp, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")
        
        try:
            self.file_sens_alive_firms_mf = open(self.model.path_results + self.name_sens_alive_firms_mf, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")
        
        try:
            self.file_sens_alive_firms_pc = open(self.model.path_results + self.name_sens_alive_firms_pc, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")
        
        try:
            self.file_sens_alive_firms_cmp = open(self.model.path_results + self.name_sens_alive_firms_cmp, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")
        
        try:
            self.file_sens_int_ratio_mf = open(self.model.path_results + self.name_sens_int_ratio_mf, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")
        
        try:
            self.file_sens_int_ratio_pc = open(self.model.path_results + self.name_sens_int_ratio_pc, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")
        
        try:
            self.file_sens_parameters = open(self.model.path_results + self.name_sens_parameters, 'w', encoding='utf-8')
        except Exception as e:
            print(f"打开文件时出错: {e}")

    # 以下是在输出文件对象中写入数据的辅助方法
    def print_sens_herf_mf(self, text):
        """在主机市场赫芬达尔指数输出文件中写入数据"""
        try:
            if self.file_sens_herf_mf:
                self.file_sens_herf_mf.write(text)
        except Exception as e:
            print(f"写入文件时出错: {e}")
    
    def print_sens_herf_pc(self, text):
        """在PC市场赫芬达尔指数输出文件中写入数据"""
        try:
            if self.file_sens_herf_pc:
                self.file_sens_herf_pc.write(text)
        except Exception as e:
            print(f"写入文件时出错: {e}")
    
    def print_sens_herf_cmp(self, text):
        """在组件市场赫芬达尔指数输出文件中写入数据"""
        try:
            if self.file_sens_herf_cmp:
                self.file_sens_herf_cmp.write(text)
        except Exception as e:
            print(f"写入文件时出错: {e}")
    
    def print_sens_alive_firms_mf(self, text):
        """在主机市场活跃公司数量输出文件中写入数据"""
        try:
            if self.file_sens_alive_firms_mf:
                self.file_sens_alive_firms_mf.write(text)
        except Exception as e:
            print(f"写入文件时出错: {e}")
    
    def print_sens_alive_firms_pc(self, text):
        """在PC市场活跃公司数量输出文件中写入数据"""
        try:
            if self.file_sens_alive_firms_pc:
                self.file_sens_alive_firms_pc.write(text)
        except Exception as e:
            print(f"写入文件时出错: {e}")
    
    def print_sens_alive_firms_cmp(self, text):
        """在组件市场活跃公司数量输出文件中写入数据"""
        try:
            if self.file_sens_alive_firms_cmp:
                self.file_sens_alive_firms_cmp.write(text)
        except Exception as e:
            print(f"写入文件时出错: {e}")
    
    def print_sens_int_ratio_mf(self, text):
        """在主机市场集成比例输出文件中写入数据"""
        try:
            if self.file_sens_int_ratio_mf:
                self.file_sens_int_ratio_mf.write(text)
        except Exception as e:
            print(f"写入文件时出错: {e}")
    
    def print_sens_int_ratio_pc(self, text):
        """在PC市场集成比例输出文件中写入数据"""
        try:
            if self.file_sens_int_ratio_pc:
                self.file_sens_int_ratio_pc.write(text)
        except Exception as e:
            print(f"写入文件时出错: {e}")
    
    def print_sens_parameters(self, text):
        """在参数输出文件中写入数据"""
        try:
            if self.file_sens_parameters:
                self.file_sens_parameters.write(text)
        except Exception as e:
            print(f"写入文件时出错: {e}")
    
    def copy_values(self, input_list, output_list):
        """
        从输入ArrayList复制值到输出数组
        
        Args:
            input_list: 输入列表
            output_list: 输出列表
        """
        for i in range(len(input_list)):
            output_list[i] = input_list[i]
    
    def copy_values_param(self, input_params, output_list):
        """
        从输入参数数组复制值到输出数组
        
        Args:
            input_params: 输入参数数组
            output_list: 输出列表
        """
        try:
            # 确保输入参数不为空
            if input_params is None:
                print("错误: 输入参数数组为空")
                return
            
            # 安全地访问参数值
            max_len = min(len(input_params), len(output_list))
            for i in range(max_len):
                if input_params[i] is not None and hasattr(input_params[i], 'value'):
                    output_list[i] = str(input_params[i].value)
                else:
                    # 如果参数为空或没有value属性，设置为默认值
                    output_list[i] = "N/A"
                    
        except Exception as e:
            print(f"复制参数值时出错: {e}")
            # 确保输出列表中的所有元素都有值
            for i in range(len(output_list)):
                if output_list[i] is None or output_list[i] == "":
                    output_list[i] = "N/A"
    
    def make_statistics(self):
        """
        从当前模拟运行中获取数据并存储到存储对象中
        """
        try:
            # 确保model和model.end_time存在并有效
            if not hasattr(self.model, 'end_time') or self.model.end_time <= 0:
                print("错误: 模型参数未正确初始化")
                return
            
            # 确保model.parameters存在
            if not hasattr(self.model, 'parameters') or self.model.parameters is None:
                print("错误: 模型参数列表未初始化")
                return
                
            new_herf_mf = [""] * (self.model.end_time + 1)
            new_herf_pc = [""] * (self.model.end_time + 1)
            new_herf_cmp = [""] * (self.model.end_time + 1)
            new_alive_firms_mf = [""] * (self.model.end_time + 1)
            new_alive_firms_pc = [""] * (self.model.end_time + 1)
            new_alive_firms_cmp = [""] * (self.model.end_time + 1)
            new_int_ratio_mf = [""] * (self.model.end_time + 1)
            new_int_ratio_pc = [""] * (self.model.end_time + 1)
            new_parameters = [""] * (len(self.model.parameters) + 1)
            
            # 确保统计数据已初始化
            if not hasattr(self.model, 'statistics') or self.model.statistics is None:
                print("错误: 模型统计数据未初始化")
                return
                
            for t in range(1, self.model.end_time + 1):
                # 防止访问空对象
                if hasattr(self.model.statistics, 'herf_mf') and t < len(self.model.statistics.herf_mf):
                    new_herf_mf[t] = str(self.model.statistics.herf_mf[t])
                if hasattr(self.model.statistics, 'herf_pc') and t < len(self.model.statistics.herf_pc):
                    new_herf_pc[t] = str(self.model.statistics.herf_pc[t])
                if hasattr(self.model.statistics, 'herf_cmp') and t < len(self.model.statistics.herf_cmp):
                    new_herf_cmp[t] = str(self.model.statistics.herf_cmp[t])
                if hasattr(self.model.statistics, 'alive_firms_mf') and t < len(self.model.statistics.alive_firms_mf):
                    new_alive_firms_mf[t] = str(self.model.statistics.alive_firms_mf[t])
                if hasattr(self.model.statistics, 'alive_firms_pc') and t < len(self.model.statistics.alive_firms_pc):
                    new_alive_firms_pc[t] = str(self.model.statistics.alive_firms_pc[t])
                if hasattr(self.model.statistics, 'alive_firms_cmp') and t < len(self.model.statistics.alive_firms_cmp):
                    new_alive_firms_cmp[t] = str(self.model.statistics.alive_firms_cmp[t])
                if hasattr(self.model.statistics, 'int_ratio_mf') and t < len(self.model.statistics.int_ratio_mf):
                    new_int_ratio_mf[t] = str(self.model.statistics.int_ratio_mf[t])
                if hasattr(self.model.statistics, 'int_ratio_pc') and t < len(self.model.statistics.int_ratio_pc):
                    new_int_ratio_pc[t] = str(self.model.statistics.int_ratio_pc[t])
            
            # 设置随机种子参数
            if hasattr(self.model, 'rng_seed'):
                new_parameters[0] = str(self.model.rng_seed)
            else:
                new_parameters[0] = "unknown"
                
            # 安全地复制参数值
            try:
                self.copy_values_param(self.model.parameters, new_parameters[1:])
            except Exception as e:
                print(f"复制参数值时出错: {e}")
            
            # 将数据添加到结果列表
            self.sens_herf_mf.append(new_herf_mf)
            self.sens_herf_pc.append(new_herf_pc)
            self.sens_herf_cmp.append(new_herf_cmp)
            self.sens_alive_firms_mf.append(new_alive_firms_mf)
            self.sens_alive_firms_pc.append(new_alive_firms_pc)
            self.sens_alive_firms_cmp.append(new_alive_firms_cmp)
            self.sens_int_ratio_mf.append(new_int_ratio_mf)
            self.sens_int_ratio_pc.append(new_int_ratio_pc)
            self.sens_parameters.append(new_parameters)
        except Exception as e:
            print(f"生成敏感性分析统计数据时出错: {e}")
    
    def print_statistics(self):
        """
        将存储在相关对象中的数据打印到输出文件中
        """
        try:
            # 检查是否有数据可打印
            if not self.sens_parameters or len(self.sens_parameters) == 0:
                print("警告: 没有敏感性分析数据可打印")
                return
                
            # 打印参数值
            for sens_counter in range(len(self.sens_parameters)):
                try:
                    param_data = "Run" + str(sens_counter) + ","
                    for p in range(len(self.sens_parameters[sens_counter])):
                        if self.sens_parameters[sens_counter][p] is not None:
                            param_data += self.sens_parameters[sens_counter][p]
                        else:
                            param_data += "N/A"
                        param_data += ","
                    param_data += "\n"
                    self.print_sens_parameters(param_data)
                except Exception as e:
                    print(f"打印参数数据时出错 (运行 {sens_counter}): {e}")
            
            # 打印主机市场赫芬达尔指数
            self._print_data_series(self.sens_herf_mf, self.print_sens_herf_mf, "HMF")
            
            # 打印PC市场赫芬达尔指数
            self._print_data_series(self.sens_herf_pc, self.print_sens_herf_pc, "HPC")
            
            # 打印组件市场赫芬达尔指数
            self._print_data_series(self.sens_herf_cmp, self.print_sens_herf_cmp, "HCMP")
            
            # 打印主机市场活跃公司数量
            self._print_data_series(self.sens_alive_firms_mf, self.print_sens_alive_firms_mf, "MF")
            
            # 打印PC市场活跃公司数量
            self._print_data_series(self.sens_alive_firms_pc, self.print_sens_alive_firms_pc, "PC")
            
            # 打印组件市场活跃公司数量
            self._print_data_series(self.sens_alive_firms_cmp, self.print_sens_alive_firms_cmp, "CMP")
            
            # 打印主机市场集成比例
            self._print_data_series(self.sens_int_ratio_mf, self.print_sens_int_ratio_mf, "IMF")
            
            # 打印PC市场集成比例
            self._print_data_series(self.sens_int_ratio_pc, self.print_sens_int_ratio_pc, "IPC")
            
        except Exception as e:
            print(f"打印敏感性分析数据时出错: {e}")
    
    def _print_data_series(self, data_series, print_func, series_name):
        """
        打印特定数据系列到输出文件
        
        Args:
            data_series: 数据系列
            print_func: 用于打印的函数
            series_name: 数据系列名称
        """
        try:
            if not data_series or len(data_series) == 0:
                print(f"警告: 没有 {series_name} 数据可打印")
                return
            
            # 打印首行（运行标识）
            header = "Time,"
            for i in range(len(data_series)):
                header += "Run" + str(i) + ","
            header += "\n"
            print_func(header)
            
            # 如果没有时间点数据，直接返回
            if len(data_series[0]) == 0:
                return
                
            # 打印每个时间点的值
            for t in range(1, len(data_series[0])):
                line = str(t) + ","
                for run in range(len(data_series)):
                    if t < len(data_series[run]) and data_series[run][t] is not None:
                        line += data_series[run][t]
                    else:
                        line += "N/A"
                    line += ","
                line += "\n"
                print_func(line)
        except Exception as e:
            print(f"打印 {series_name} 数据时出错: {e}") 