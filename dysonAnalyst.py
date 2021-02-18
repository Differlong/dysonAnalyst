from icecream import ic
import utils
from material import Material


# ic.disable()
def to_string(data, sep=", "):
    return sep.join(("{}*{}".format(data[key], key) for key in data))


def prescription_writer(func):
    def __wrapper__(*k):
        return "1{}: {}".format(k[1], to_string(func(*k)))

    return __wrapper__


class DysonAnalyst(object):
    def __init__(self):
        self.material_list = []
        pass

    def read_material_list(self, config_file="./files/resources/materialList.json"):
        material_list = utils.read_from_json(config_file)
        for material in material_list:
            self.material_list.append(Material(material))

        ic(self.material_list)


def read_reaction_list(self, config_file="./files/resources/reactionList.json"):
    reaction_list = utils.read_from_json(config_file)

    ic(reaction_list)

    pass


def start(self):
    self.read_material_list()
    self.read_reaction_list()


def manage(self):
    self.start()


if __name__ == "__main__":
    analyst = DysonAnalyst()
    analyst.manage()
