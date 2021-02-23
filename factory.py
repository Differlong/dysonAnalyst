from material import Material
from reaction import Reaction
from device import Furnace, ManufactureStation, get_device_type
from globalWatcher import GW


class FactoryError(Exception):
    pass


class MaterialFactory(object):
    def __init__(self):
        self._material_dict = GW.material_dict
        self._device_set = GW.device_set

    def get_material(self, info):
        name = info["name"]
        if name in self._material_dict:
            print("factory get from gw: ", name)
            return self._material_dict[name]

        if "material" in info["type"]:
            m = Material(name)
            m.init(info)
            self._material_dict[name] = m
            return m
        elif "device" in info["type"]:
            if "furnace" in info["type"]:
                m = Furnace(name)
                m.init(info)
                self._material_dict[name] = m
                self._device_set.add(m)
                return m
            elif "manufactureStation" in info["type"]:
                m = ManufactureStation(name)
                m.init(info)
                self._material_dict[name] = m
                self._device_set.add(m)
                return m
            else:
                raise FactoryError("error device: " + name)
        else:
            raise FactoryError("Error Material: " + name)


class ReactionFactory(object):
    def __init__(self):
        self._reaction_dict = GW.reaction_dict

    def get_reaction(self, info):
        id_ = info["id"]
        if id_ in self._reaction_dict:
            return self._reaction_dict[id_]
        from_material = {GW.get_material(name): info["rawMaterial"][name] for name in info["rawMaterial"]}
        to_material = {GW.get_material(name): info["product"][name] for name in info["product"]}
        duration = info["time"]
        device = get_device_type(info["device"])
        reaction = Reaction(id_, from_material, to_material, device=device, duration=duration)
        self._reaction_dict[id_] = reaction
        return reaction


if __name__ == '__main__':
    import json

    with open("./files/resources/materialList.json", encoding="utf8") as f:
        material_list = json.load(f)

    mf = MaterialFactory()
    for i in material_list:
        m = mf.get_material(i)
        print(m)

    for i in material_list:
        m = mf.get_material(i)
        print(m)

    with open("./files/resources/reactionList.json", encoding="utf8") as f:
        reaction_list = json.load(f)

    rf = ReactionFactory()
    for i in reaction_list:
        r = rf.get_reaction(i)
        print(r)
