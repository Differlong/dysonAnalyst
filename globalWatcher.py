class MaterialError(Exception):
    pass


class GlobalWatcher(object):
    def __init__(self):
        self.material_dict = dict()
        self.device_set = set()
        self.reaction_dict = dict()

    def get_material(self, name):
        if name in self.material_dict:
            return self.material_dict[name]
        else:
            raise MaterialError("can't find material: " + name)


GW = GlobalWatcher()
