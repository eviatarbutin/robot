import magicbot
import wpilib
from components.shooter import Shooter
from components.push_ball import Pusher
from ctre import WPI_TalonSRX
from wpilib import Joystick


class MyRobot(magicbot):
    shooter: Shooter
    pusher: Pusher

    def createObjects(self):
        self.shooter.master_shooter_motor = WPI_TalonSRX(7)
        self.shooter.slave_shooter_motor = WPI_TalonSRX(8)
        self.joystick = Joystick(0)

    def teleopPeriodic(self):
        if self.Joystick.getTriggerReleased():
            self.shooter.shoot()
        else:
            self.shooter.stop_shooting()











