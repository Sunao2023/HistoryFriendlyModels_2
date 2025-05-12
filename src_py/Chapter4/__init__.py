#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chapter4包 - 转换自Java版本的Chapter4包
这个包包含了第4章模型的Python实现
"""

# 导入主要类，使它们可以从包中直接导入
from .parameter import Parameter
from .system_element import SystemElement
from .component_firm import ComponentFirm
from .component_market import ComponentMarket
from .computer_firm import ComputerFirm
from .computer_market import ComputerMarket
from .end_product import EndProduct
from .not_sold_component import NotSoldComponent
from .sold_component import SoldComponent
from .statistics import Statistics
from .sa_statistics import SA_Statistics
from .c4_model import C4Model 