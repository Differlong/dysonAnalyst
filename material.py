class Material(object):
    def __init__(self, name: str = "material"):
        self.name = name

    def __hash__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
