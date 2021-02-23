from material import Material


# 继承是对的。但是设备是固定的，需要的就是那个东西。
# 需要一个工厂函数来生产。
# 那就还是配置式的，代码里面没有参数。

class Device(Material):
    name = "设备"
    speed_para = 1

    def init(self, config):
        pass

    def speed(self, speed: float):
        return speed * self.speed_para


class Furnace(Device):
    name = "熔炉类"
    pass


class ManufactureStation(Device):
    name = "制造类"

    def init(self, config):
        self.speed_para = config["speed"]


def get_device_type(name):
    if name == "furnace":
        return Furnace
    if name == "manufactureStation":
        return ManufactureStation


if __name__ == "__main__":
    device = ManufactureStation("ms3")
    print(device.speed(10))
