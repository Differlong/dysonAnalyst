from reaction import Reaction
from device import Device
from material import Material


class Workshop(object):
    def __init__(self, reaction: Reaction, device: Device):
        self.reaction = reaction
        self.device = device

    @property
    def speed(self):
        return self.device.speed(self.reaction.base_speed)

    @property
    def duration(self):
        return 60 / self.speed

    def get_material_speed(self, material: Material) -> float:
        speed = 0
        if material in self.reaction.from_materials:
            speed -= self.speed * self.reaction.from_materials[material]
        if material in self.reaction.to_materials:
            speed += self.speed * self.reaction.to_materials[material]
        return speed
