import json
from icecream import ic


# ic.disable()
def to_string(data, sep=", "):
    return sep.join(("{}*{}".format(data[key], key) for key in data))


def prescription_writer(func):
    def __wrapper__(*k):
        return "1{}: {}".format(k[1], to_string(func(*k)))

    return __wrapper__


class DysonAnalyst(object):
    def __init__(self):
        pass

    def read_material_list(self, config_file="./files/resources/materialList.json"):
        pass

    def read_reaction_list(self, config_file="./files/resources/reactionList.json"):
        pass

    def start(self):
        self.read_material_list()
        self.read_reaction_list()


    def manage(self):
        self.start()

if __name__ == "__main__":
    analyst = DysonAnalyst()
    analyst.manage()
