from material import Material


class Device(Material):
    speed_para = 1

    def speed(self, speed: float):
        return speed * self.speed_para


class Furnace(Device):
    speed_para = 1


class ManufactureStation(Device):
    pass


class ManufactureStation1(ManufactureStation):
    speed_para = 0.8


class ManufactureStation2(ManufactureStation):
    speed_para = 2


class ManufactureStation3(ManufactureStation):
    speed_para = 3


if __name__ == "__main__":
    device = ManufactureStation3("ms3")
    print(device.speed(10))
