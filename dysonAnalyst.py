from icecream import ic
import utils
from material import Material
from config import Config
from factory import MaterialFactory, ReactionFactory
from globalWatcher import GW
from reaction import Reaction
from scipy.optimize import minimize, OptimizeResult
import numpy as np


class DysonAnalyst(object):
    def __init__(self):
        self.material_list = []
        self.reaction_list = []
        self.start()

    def start(self):
        material_info_list = utils.read_from_json(Config.material_list_path)
        mf = MaterialFactory()
        for i in material_info_list:
            m = mf.get_material(i)
            print("create material: ", m)
            self.material_list.append(m)

        reaction_info_list = utils.read_from_json(Config.reaction_list_path)
        rf = ReactionFactory()
        for i in reaction_info_list:
            r = rf.get_reaction(i)
            print("create reaction: ", r)
            self.reaction_list.append(r)

    def calculate(self, material, speed, reaction_dict=None):
        # 需要考虑的因素有点多，涉及到多种来源的。选择来源之后，还有附属来源。乱七八糟的。看别人怎么写的吧。
        # 不考虑附属来源，单纯处理多产出的问题。
        # 自己用，不管了，算60次，然后求平均值。
        # 还是采用计算最优化的方式来做，这个靠谱一点。
        reaction_dict = dict() if not reaction_dict else reaction_dict
        material: Material = GW.get_material(material) if type(material) == str else material

        reaction_set = set()
        material_set = set()
        focus_material_set = set()

        item_list = [material]
        while len(item_list) != 0:
            item = item_list.pop()
            if item in focus_material_set:
                continue
            reaction: Reaction = item.get_reaction_as_product() if item not in reaction_dict else reaction_dict[item]
            from_items = reaction.from_materials
            item_list.extend(from_items)
            focus_material_set.add(item)
            material_set.update(reaction.to_materials)
            reaction_set.add(reaction)
        ic(reaction_set)
        ic(material_set)
        ic(focus_material_set)
        # 开始列方程计算。

        e = 1e-8

        m_list = list(material_set)
        m_dict = {m_list[i]: i for i in range(len(m_list))}
        r_list = list(reaction_set)

        print(m_list, m_dict, r_list)

        x_list = np.zeros(len(m_list) + len(r_list))

        purpose_function = lambda x: sum(x[:len(m_list)])
        cons = list()

        def gen_func(item):
            def __wrapper__(x: np.array):
                result = 0
                if item.name == material.name:
                    result += speed
                else:
                    result -= x[m_dict[item]]
                for j in range(len(r_list)):
                    r = r_list[j]
                    if item in r.from_materials:
                        result -= x[len(m_list) + j] * r.from_materials[item]
                    if item in r.to_materials:
                        result += x[len(m_list) + j] * r.to_materials[item]
                return result
            cons.append({"type": "eq", "fun": __wrapper__})

        # 约束条件
        for item in m_list:
            gen_func(item)

        for i in range(len(m_list) + len(r_list)):
            cons.append({"type": "ineq", "fun": lambda x: x[i]})
        # for _ in range(100):
        #     x_list += 1
        #     print(x_list)
        #     for c in cons:
        #         print(c["fun"](x_list))

        res: OptimizeResult = minimize(purpose_function, x_list, method="SLSQP", bounds=[(0, None)] * (len(m_list) + len(r_list)), constraints=cons)
        print("最小值： ", res.fun)
        print("最优解： ", res.x)
        for i in range(len(m_list) + len(r_list)):
            if i < len(m_list):
                print(m_list[i], int(res.x[i]))
            else:
                print(r_list[i-len(m_list)], int(res.x[i]))
        print('迭代终止是否成功：', res.success)
        print('迭代终止原因：', res.message)


if __name__ == "__main__":
    analyst = DysonAnalyst()
    analyst.calculate("铁块", 72)
