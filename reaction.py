class Reaction(object):
    def __init__(self, id_, from_materials, to_materials, device, duration):
        self.id = id_
        self.from_materials = from_materials
        for m in self.from_materials:
            m.reaction_list_as_raw.append(self)
        self.to_materials = to_materials
        for m in self.to_materials:
            m.reaction_list_as_product.append(self)
        self.device = device
        self.base_duration = duration
        self.base_speed = 60 / self.base_duration

    def __str__(self):
        string = self.device.name + ": "
        string += " + ".join(["{} * {}".format(self.from_materials[i], i.name) for i in self.from_materials])
        string += "\t==>\t"
        string += " + ".join(["{} * {}".format(self.to_materials[i], i.name) for i in self.to_materials])
        return string

    def __repr__(self):
        return self.__str__()
