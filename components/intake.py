from ctre import WPI_TalonSRX, FeedbackDevice
from wpilib.drive import DifferentialDrive
from wpilib import DigitalInput

class Intake:
    master_raiser : WPI_TalonSRX
    slave_raiser : WPI_TalonSRX #follows after the right one
    micro_switch: DigitalInput
    max_speed=0.6
    min_speed = 0
    up = True

    master_roller: WPI_TalonSRX
    slave_roller : WPI_TalonSRX
    rolling = False
    max_rolling_speed = 0.7
    min_rolling_speed = 0

    master_saving_roller: WPI_TalonSRX
    slave_saving_roller: WPI_TalonSRX
    save_rolling = False
    max_save_rolling_speed = 0.7
    min_save_rolling_speed = 0

    def setup(self):
        self.slave_raiser.follow(self.master_raiser)

        self.slave_roller.follow(self.master_roller)

        self.slave_saving_roller.follow(self.master_saving_roller)

    def execute(self):
        self.the_real_lifting()
        self.the_real__rolling()
        self.the_real_save_rolling()

    def the_real_lifting(self):
        if self.up:
            self.master_raiser.set(self.max_speed)
        elif not self.micro_switch.get():
            self.master_raiser.set(-self.max_speed)
        else:
            self.master_raiser.set(self.min_speed)

    def the_real__rolling(self):
        if self.rolling:
            self.master_roller.set(self.max_rolling_speed)
        else:
            self.master_roller.set(self.min_rolling_speed)

    def the_real_save_rolling(self):
        if self.save_rolling:
            self.master_saving_roller.set(self.max_save_rolling_speed)
        else:
            self.master_saving_roller.set(self.min_save_rolling_speed)

    def lift(self):
        self.up = True

    def unlift(self):
        self.up = False

    def roll(self):
        self.rolling = True

    def stop_rolling(self):
        self.rolling = False

    def save_roll(self):
        self.save_rolling = True

    def stop_save_rolling(self):
        self.save_rolling = False