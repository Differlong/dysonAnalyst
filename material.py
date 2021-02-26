class Material(object):

    def __init__(self, name: str = "material"):
        self.name = name
        self.reaction_list_as_raw = []
        self.reaction_list_as_product = []

    def init(self, config):
        pass

    def __hash__(self):
        return hash("_|_" + self.name + "_|_")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_reaction_as_raw(self):
        return self.reaction_list_as_raw[0]

    def get_reaction_as_product(self):
        return self.reaction_list_as_product[0]
