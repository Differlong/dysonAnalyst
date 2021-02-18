from material import Material


# 继承是对的。但是设备是固定的，需要的就是那个东西。
# 需要一个工厂函数来生产。
# 那就还是配置式的，代码里面没有参数。
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
