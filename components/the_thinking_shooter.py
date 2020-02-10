from components.shooter_pid import ShooterPID
from components.tower_conveyor import Tower_conveyor
from magicbot import StateMachine, state
from components.effective_shooter import Effective_Shooter
from components.shooter import Shooter
from wpilib.timer import Timer


class ShooterControl(StateMachine):
    shooter_pid: ShooterPID
    tower_conveyor: Tower_conveyor
    effective_shooter: Effective_Shooter
    timer: Timer

    def fire(self):
        self.engage()
        self.shooter_pid.engage()

    @state(first=True)
    def prepare_to_fire(self):
        self.shooter_pid.setup_values()

        if self.shooter_pid.is_ready():
            self.next_state_now('firing')

    @state
    def firing(self, initial_call):
        if self.effective_shooter.number_of_balls > 0:
            self.tower_conveyor.enable()
        elif self.timer.get() >= 0.5:
            self.tower_conveyor.disable()
            self.done()
        if initial_call and self.tower_conveyor.is_enable:
            self.timer.start()
