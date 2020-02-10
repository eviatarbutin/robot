from wpilib import Talon


class Tower_conveyor:
    motor: Talon
    speed = 0.7
    is_enable = False
    min_speed = 0

    def enable(self):
        self.is_enable = True

    def disable(self):
        self.is_enable = False

    def execute(self):
        if self.is_enable:
            self.motor.set(self.speed)
        else:
            self.motor.set(self.min_speed)
