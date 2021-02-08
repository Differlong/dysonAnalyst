from typing import Dict

from material import Material
from device import Device


class Reaction(object):
    def __init__(self, from_materials: Dict[Material: int], to_materials: Dict[Material: int], device: Device,
                 duration: float):
        self.from_materials = from_materials
        self.to_materials = to_materials
        self.device = device
        self.base_duration = duration
        self.base_speed = 60 / self.base_duration
