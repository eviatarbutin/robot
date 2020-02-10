from components.tower_conveyor import Tower_conveyor
from components.conveyor import Conveyor
from components.shooter import Shooter
from components.intake import Intake
from wpilib import Ultrasonic, Timer


class Effective_Shooter:
    first_sensor: Ultrasonic
    second_sensor: Ultrasonic
    conveyor: Conveyor
    tower_conveyor: Tower_conveyor
    intake: Intake
    shooter: Shooter
    timer: Timer

    tolerance = 50
    number_of_balls = 0
    time = 1

    first_previous_dist = 0
    first_current_dist = 0

    second_previous_dist = 0
    second_current_dist = 0

    def execute(self):
        self.first_current_dist = self.first_sensor.getRangeMM()
        self.second_current_dist = self.second_sensor.getRangeMM()
        if self.first_previous_dist - self.first_current_dist > self.tolerance:
            self.plus_ball()
        if self.second_previous_dist - self.second_current_dist > self.tolerance:
            self.minus_ball()
        self.first_previous_dist = self.first_current_dist
        self.second_previous_dist = self.second_current_dist
        if self.timer.get() > self.time:
            self.conveyor.disable()

    def plus_ball(self):
        self.number_of_balls += 1
        if self.number_of_balls < 4:
            self.timer.reset()
            self.timer.start()
            self.conveyor.enable()

    def minus_ball(self):
        self.number_of_balls -= 1
        if self.number_of_balls > 0:
            self.timer.reset()
            self.timer.start()
            self.tower_conveyor.enable()
