# History-Friendly Models - Python 实现

本目录包含"Innovation and the Evolution of Industries: History-Friendly Models"书中模型的Python版本实现。

## 目录结构

```
HistoryFriendlyModels_1/
│
├── parameters/              # 模型参数文件目录
│   ├── Chapter3/            # 第3章模型参数
│   │   └── parameters.txt   # 参数配置文件
│   ├── Chapter4/            # 第4章模型参数
│       └── parameters.txt   # 参数配置文件
│
├── results_py/              # Python实现的模型运行结果
│   ├── Chapter3/            # 第3章模型结果
│   │   ├── multiSimulation.csv      # 多次模拟结果
│   │   └── singleSimulation.csv     # 单次模拟结果
│   ├── Chapter3_1/          # 第3章模型的1000次循环(每次10次模拟)结果
│   ├── Chapter4/            # 第4章模型结果
│   │   ├── multiSimulation.csv      # 多次模拟结果
│   │   └── singleSimulation.csv     # 单次模拟结果
│   ├── Chapter4_1/          # 第4章模型的1000次循环(每次10次模拟)结果
│   └── Chapter5/            # 第5章模型结果
│
├── src_py/                  # Python源代码目录
│   ├── Chapter3/            # 第3章模型Python实现
│   ├── Chapter4/            # 第4章模型Python实现
│   ├── Chapter5/            # 第5章模型Python实现
│   ├── manager.py           # 模型运行管理器
│   └── requirements.txt     # Python依赖包列表
```

## 参数文件

模型的参数文件位于项目根目录的`parameters`目录下，按章节分别存放。各章节模型运行时会自动读取对应章节的参数文件。
如果需要修改模拟次数以及循环次数，请直接在参数配置文件中进行修改

## 运行结果

模型运行的结果将保存在项目根目录的`results_py`目录下，按章节分别存放。

- `Chapter3_1`和`Chapter4_1`目录包含的是循环1000次、每次执行10次模拟后生成的汇总结果
- 其他`Chapter3`、`Chapter4`和`Chapter5`目录包含常规单次或多次模拟的结果

## 运行模型

`manager.py`是主要的程序入口，可以直接运行此文件来执行不同的模型：

```bash
python manager.py
```

在`manager.py`的`main`函数中，可以通过注释/取消注释不同的函数调用来选择要运行的模型和模拟类型：

```python
# Chapter 3 模型
# run_chapter3_single(VERBOSE)
# run_chapter3_multiple(VERBOSE)
# run_chapter3_sensitivity(VERBOSE)

# Chapter 4 模型
# run_chapter4_single(VERBOSE)
# run_chapter4_multiple(VERBOSE)
# run_chapter4_sensitivity(VERBOSE)

# Chapter 5 模型
# run_chapter5_single(VERBOSE)
# run_chapter5_multiple(VERBOSE)
```

## 依赖包

运行模型需要安装以下Python依赖包，可以通过以下命令安装：

```bash
pip install -r requirements.txt
```

依赖包包括：
- numpy
- pandas 
- matplotlib（用于可视化结果）
- 
