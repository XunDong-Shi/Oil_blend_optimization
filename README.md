# Oil_blend_optimization
## 1.项目内容
炼油厂具有催化裂化、重整、加氢精制等多套生产装置，不同装置产生的组分油的性质、成本各不相同，选择优化成品油调和方案进行调和是提高炼油厂经济效益的重要途径。本项目结合炼油厂实例，分析成品油调和过程建模所需的元素和方法，求解给定成品油产量下的经济指标最优时各调和组分质量提出解决方案，并输出可视化图表。

## 2.成品油调和优化模型
### 2.1 目标函数
成产成本最小
### 2.2 约束
#### 2.2.1 成品油产品总量要求
#### 2.2.2 成品油物性要求（辛烷值/凝点）
#### 2.2.3 成品油物性要求（MTBE含量）
#### 2.2.4 成品油集合储罐库存要求
#### 2.2.5 成品油各组分生产能力要求
#### 2.2.6 成品油各组分储罐库存要求

## 3.实例数据简介
该炼油厂出售G89、G92、G95三种汽油产品，D0、D-10两种柴油产品，上述成品油的物性要求详见sheet_oil，初始库存及要求详见sheet_capacity； 
  
汽油调和组分包括MTBE、催化裂化装置汽油产品、重整装置产品等9种，各汽油调和组分的生产单元、物性、成本、产量、库存要求详见sheet_Gasoline;  
  
柴油调和组分包括常减压装置产品呢、催化裂化装置产品、焦化装置产品等6种，各柴油调和组分的生产单元、物性、成本、产量、库存要求详见sheet_Diesel。  

## 4.环境依赖
Pulp,Pandas,Seaborn,Matplotlib
