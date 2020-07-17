from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


def read_data(path, kind):
    file = path + "data.xlsx"
    try:
        components = pd.read_excel(file, sheet_name=kind)
        oil = pd.read_excel(file, sheet_name="Oil", index_col=0)
        capacity = pd.read_excel(file, sheet_name="Capacity", index_col=0)
        return components, oil, capacity
    except Exception as e:
        print("请确认文件路径，并输入类型'Gasoline'或'Diesel'")
        raise e


def optimize_model(blend_oils, components, oil, capacity):
    prob = LpProblem("Oil_Blending", LpMinimize)

    # 声明变量
    oil_components = LpVariable.dicts("fraction", ((i, j) for i in components.index for j in blend_oils), lowBound=0,
                                      cat="Continuous")

    # 添加生产成本最小的目标函数
    prob += lpSum([oil_components[(i, j)] * components['cost'][i] for i in components.index for j in blend_oils])

    # 添加产品总量要求
    for blend_oil, production in blend_oils.items():
        prob += lpSum([oil_components[(i, blend_oil)] for i in components.index]) == production

    # 添加产品物性要求（辛烷值）
    for blend_oil in blend_oils.keys():
        prob += oil.loc[blend_oil, "LB"] * lpSum([oil_components[(i, blend_oil)] for i in components.index]) <= lpSum(
            [oil_components[(i, blend_oil)] * components["proper"][i] for i in components.index])
        prob += lpSum([oil_components[(i, blend_oil)] * components["proper"][i] for i in components.index]) <= oil.loc[
            blend_oil, "Up"] * lpSum([oil_components[(i, blend_oil)] for i in components.index])

    # 添加产品含量要求（MTBE含量要求）
    for blend_oil in blend_oils.keys():
        prob += oil_components[(0, blend_oil)] <= lpSum(oil_components[(i, blend_oil)] for i in components.index) * 0.02

    # 添加产品组分产量要求
    for i in components.index:
        prob += lpSum(oil_components[(i, blend_oil)] for blend_oil in blend_oils.keys()) <= components["production"][i]

    # 添加产品组分库存要求
    for i in components.index:
        prob += components["production"][i] - lpSum(oil_components[(i, blend_oil)] for blend_oil in blend_oils) + \
                components["INIVF"][i] <= components["UP"][i]
        prob += components["production"][i] - lpSum(oil_components[(i, blend_oil)] for blend_oil in blend_oils) + \
                components["INIVF"][i] >= components["LB"][i]

    # 添加集合罐库存要求
    for blend_oil, production in blend_oils.items():
        prob += capacity.loc[blend_oil, "INIVF"] + lpSum(
            oil_components[(i, blend_oil)] for i in components.index) - production <= capacity.loc[blend_oil, "UP"]
        prob += capacity.loc[blend_oil, "INIVF"] + lpSum(
            oil_components[(i, blend_oil)] for i in components.index) - production >= capacity.loc[blend_oil, "LB"]

    # 模型求解
    prob.solve()

    # 输出求解结果
    if LpStatus[prob.status] == "Optimal":
        print("Status:", LpStatus[prob.status])
        print("经过求解总成本为{}".format(value(prob.objective)))
        return oil_components, prob
    else:
        print("无法完成模型求解，请确认数据输入")


class Output:
    def __init__(self, oil_components, prob, blend_oils, path):
        self.oil_components = oil_components
        self.prob = prob
        self.blend_oils = blend_oils
        self.path = path

    def __data_format(self):
        output = []
        for i, j in self.oil_components.items():
            var_output = {"unit": i[0], "oil": i[1], "fraction": j.varValue}
            output.append(var_output)
        data_frame = pd.DataFrame.from_records(output).sort_values(["unit", "oil"]).reset_index()
        return data_frame

    def plot(self):
        data_frame = self.__data_format()
        sns.color_palette('hls', 10)
        sns.set(style="whitegrid")
        plt.figure(figsize=(16, 10), dpi=300)
        figs = sns.barplot(x="unit", y="fraction", hue="oil", data=data_frame, saturation=0.75)
        figs.set_title("The results of optimization model of the blending {}".format(self.blend_oils), fontsize=20)
        for i in range(0, data_frame.shape[0]):
            width = 0.8 / len(self.blend_oils)
            if len(self.blend_oils) % 2 == 1:
                x_location = int(i / len(self.blend_oils)) + (i % len(self.blend_oils) - 1) * width
            else:
                x_location = int(i / len(self.blend_oils)) + (i % len(self.blend_oils) - 0.5) * width
            figs.text(x_location, data_frame["fraction"][i] + 10, round(data_frame["fraction"][i], 1), fontsize=12,
                      ha="center", style="italic")
        plt.savefig(self.path + "result.jpg")
        plt.show()

    def csv_output(self):
        data_frame = self.__data_format()
        data_frame.set_index(["unit", "oil"], inplace=True)
        data_frame.to_csv(self.path + "output.csv", encoding='utf-8')


if __name__ == '__main__':
    file_path = " "
    oil_kind = "Gasoline"
    target = {"G89": 2500, "G92": 1500, "G95": 500}
    df_components, df_oil, df_capacity = read_data(file_path, oil_kind)
    components_fraction, problem = optimize_model(target, df_components, df_oil, df_capacity)
    result = Output(components_fraction, problem, target, file_path)
    result.plot()
    result.csv_output()
