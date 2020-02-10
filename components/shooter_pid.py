from components.shooter import Shooter
from magicbot import StateMachine, state
from wpilib import PIDController, Notifier
from shit.holder import IOSpeedHolder


class ShooterPID(StateMachine):
    shooter: Shooter
    finished = True
    enabled = False
    speed = 0
    p = 0
    i = 0
    d = 0
    f = 0
    setpoint = 0
    period = 0
    tolerance = 0
    input_range = 0
    output_range = 0

    def setup(self):
        self.motor_updater = Notifier(self.update_motors)

        self.shooter_holder = IOSpeedHolder(self.shooter.get_wheel_speed, self.output)
        self.shooter_controller = PIDController(self.p, self.i, self.d, self.f, source=self.shooter_holder,
                                                output=self.shooter_holder, period=self.period)
        self.shooter_controller.setInputRange(-self.input_range, self.input_range)
        self.shooter_controller.setOutputRange(-self.output_range, self.output_range)
        self.shooter_controller.setAbsoluteTolerance(self.tolerance)

    def setup_values(self, p=0, i=0, d=0, f=0, setpoint=0.7, period=0.02, tolerance=0, input_range=1.5, output_range=1):
        self.p = p
        self.i = i
        self.d = d
        self.f = f
        self.setpoint = setpoint
        self.period = period
        self.tolerance = tolerance
        self.input_range = input_range
        self.output_range = output_range

    def update_motors(self):
        self.shooter.set_motor_value(self.speed)

    def output(self, output):
        self.speed = output

    def is_finished(self):
        return self.shooter_controller.onTarget()

    def initialize(self):
        self.shooter.reset_encoder()

        self.shooter_controller.setSetpoint(self.setpoint)

        self.shooter_controller.enable()
        self.motor_updater.startPeriodic(self.period)

    def close_threads(self):
        self.shooter_controller.close()
        self.motor_updater.close()

    def is_ready(self):
        return self.shooter_controller.onTarget()

    @state(first=True)
    def shooting(self, initial_call):
        if initial_call:
            self.initialize()
        if self.enabled:
            self.close_threads()
            self.finished = True
            self.done()
