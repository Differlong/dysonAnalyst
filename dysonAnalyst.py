from icecream import ic
import utils
from material import Material
from config import Config
from factory import MaterialFactory, ReactionFactory
from globalWatcher import GW
from reaction import Reaction
from scipy.optimize import linprog
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
        #
        # e = 1e-8
        #
        m_list = list(material_set)
        m_dict = {m_list[i]: i for i in range(len(m_list))}
        r_list = list(reaction_set)

        print(m_list, m_dict, r_list)

        c = np.array([0 if i >= len(m_list) else 1 for i in range(len(m_list) + len(r_list))])
        ic(c)
        bounds = [(0, None) for i in range(len(m_list) + len(r_list))]
        a = list()
        b = list()
        for i in range(len(m_list)):
            item = m_list[i]
            arg_list = [0 for i in range(len(m_list) + len(r_list))]
            arg_list[i] = -1
            for j in range(len(r_list)):
                arg = 0
                reaction = r_list[j]
                if item in reaction.from_materials:
                    arg -= reaction.from_materials[item]
                if item in reaction.to_materials:
                    arg += reaction.to_materials[item]
                arg_list[len(m_list) + j] = arg
            a.append(arg_list)
            if item == material:
                b.append(speed)
            else:
                b.append(0)
        print(c)
        print(a)
        print(b)
        print(bounds)
        res= linprog(c, A_eq=a, b_eq=b, bounds=bounds,options={"disp": True})
        print(res)
        print("最小值： ", res.fun)
        print("最优解： ", res.x)
        for i in range(len(m_list) + len(r_list)):
            if i < len(m_list):
                print(m_list[i], round(res.x[i]))
            else:
                print(r_list[i-len(m_list)], round(res.x[i]))
        print('迭代终止是否成功：', res.success)
        print('迭代终止原因：', res.message)


if __name__ == "__main__":
    analyst = DysonAnalyst()
    analyst.calculate("铁块", 60)
