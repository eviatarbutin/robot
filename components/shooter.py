from magicbot import StateMachine
from ctre import WPI_TalonSRX, FeedbackDevice


class Shooter:
    master_shooter_motor: WPI_TalonSRX
    slave_shooter_motor: WPI_TalonSRX
    shooting_speed = 0.7
    shooting = False

    def setup(self):
        self.master_shooter_motor.configSelectedFeedbackSensor(FeedbackDevice.QuadEncoder)
        self.slave_shooter_motor.follow(self.master_shooter_motor)

    def execute(self):
        if self.shooting:
            self.master_shooter_motor.set(self.shooting_speed)
        else:
            self.master_shooter_motor.set(0)

    def get_shooter_ticks(self):
        return self.master_shooter_motor.getSelectedSensorPosition()

    def shoot(self):
        self.shooting = True

    def stop_shooting(self):
        self.shooting = False
