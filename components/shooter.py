from magicbot import StateMachine
from ctre import WPI_TalonSRX, FeedbackDevice
from components.shooter_pid import ShooterPID


class Shooter:
    master_shooter_motor: WPI_TalonSRX
    slave_shooter_motor: WPI_TalonSRX
    shooter_pid: ShooterPID
    shooting_speed = 0.7
    shooting = False
    just_pressed = False

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

    def get_wheel_speed(self):
        return self.master_shooter_motor.getSelectedSensorVelocity() % 256

    def set_motor_value(self, speed):
        self.shooting_speed = speed

    def reset_encoder(self):
        self.master_shooter_motor.setSelectedSensorPosition(0)

    def has_just_been_pressed(self, x):
        self.just_pressed = x
