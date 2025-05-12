#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
模拟制药产业的分子类。
"""

class Molecule:
    """分子类，代表药物发现过程中的分子"""
    
    def __init__(self, mol_id=0, quality=0):
        """
        初始化分子对象
        
        Args:
            mol_id: 分子ID
            quality: 分子质量/有效性
        """
        self.id = mol_id        # 分子的唯一标识符
        self.q = quality        # 分子的质量
        self.patent = False     # 是否已被申请专利
        self.patent_firm = 0    # 持有专利的公司ID
        self.patent_time = 0    # 专利申请时间
        self.viewed = False     # 是否已被查看
        self.view_time = 0      # 查看时间
        self.view_firm = 0      # 查看公司
        self.patent_by = -1      # Firm that patented the molecule (-1 if not patented)
        self.focal = 0           # Identifies if it's a focal molecule (0 for variants)
        self.products_on = 0     # A product based on this molecule has been developed
        self.on_mol_res = 0      # Counts how many firms are doing research on the same molecule
        self.now_free = False    # If the patent expired

    def __str__(self):
        return f"Molecule(id={self.id}, q={self.q}, patent={self.patent}, patent_firm={self.patent_firm}, patent_time={self.patent_time}, viewed={self.viewed}, view_time={self.view_time}, view_firm={self.view_firm}, patent_by={self.patent_by}, focal={self.focal}, products_on={self.products_on}, on_mol_res={self.on_mol_res}, now_free={self.now_free})" 