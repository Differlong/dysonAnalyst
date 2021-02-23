class Material(object):

    def __init__(self, name: str = "material"):
        self.name = name

    def init(self, config):
        pass

    def __hash__(self):
        return hash("_|_" + self.name + "_|_")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
