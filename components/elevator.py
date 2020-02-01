from ctre import WPI_TalonSRX, FeedbackDevice
from wpilib.drive import DifferentialDrive
from wpilib import DigitalInput


class Elevator:
    micro_switch: DigitalInput
    master_raiser: WPI_TalonSRX
    slave_raiser: WPI_TalonSRX
    min_speed = 0
    max_speed = 0.7
    up = False

    def setup(self):
        self.slave_raiser.follow(self.master_raiser)

    def execute(self):
        if self.up:
            self.master_raiser.set(self.max_speed)
        elif not self.micro_switch.get():
            self.master_raiser.set(-self.max_speed)
        else:
            self.master_raiser.set(self.min_speed)

    def lift(self):
        self.up = True

    def go_down(self):
        self.up = False
