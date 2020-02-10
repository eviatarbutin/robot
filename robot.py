from networktables.networktables import NetworkTables
from components.tower_conveyor import Tower_conveyor
from components.conveyor import Conveyor
from components.elevator import Elevator
from components.chassis import Chassis
from components.shooter import Shooter
from components.intake import Intake
from magicbot import MagicRobot
from shit.robot_map import Robot_Map
from wpilib import Joystick, DigitalInput, Compressor, Talon
from ctre import WPI_TalonSRX
from navx import AHRS
import wpilib


class MyRobot(MagicRobot):
    chassis: Chassis
    intake: Intake
    elevator: Elevator
    conveyor: Conveyor
    shooter: Shooter
    tower_conveyor: Tower_conveyor
    ports: Robot_Map
    def createObjects(self):
        self.chassis_left_master = WPI_TalonSRX(self.ports.chassis_left_master_port)
        self.chassis_left_slave = WPI_TalonSRX(self.ports.chassis_left_slave_port)
        self.chassis_right_master = WPI_TalonSRX(self.ports.chassis_right_master)
        self.chassis_right_slave = WPI_TalonSRX(self.ports.chassis_right_slave_port)

        self.intake_master_raiser = WPI_TalonSRX(self.ports.intake_master_raiser_port)  # some port
        self.intake_slave_raiser = WPI_TalonSRX(self.ports.intake_slave_raiser_port)  # some port
        self.intake_micro_switch = DigitalInput(self.ports.intake_micro_switch_port)  # some port

        self.intake_master_roller = WPI_TalonSRX(self.ports.intake_master_roller_port)  # some port
        self.intake_slave_roller = WPI_TalonSRX(self.ports.intake_slave_roller_port)  # some port

        self.intake_master_saving_roller = WPI_TalonSRX(self.ports.intake_master_saving_roller_port)  # some port
        self.intake_slave_saving_roller = WPI_TalonSRX(self.ports.intake_slave_saving_roller_port)  # some port

        self.elevator_micro_switch = DigitalInput(self.ports.elevator_micro_switch_port)  # some port
        self.elevator_master_raiser = WPI_TalonSRX(self.ports.elevator_master_raiser_port)  # some port
        self.elevator_slave_raiser = WPI_TalonSRX(self.ports.elevator_slave_raiser_port)  # some port

        self.conveyor_motor = Talon(self.ports.conveyor_motor_port)  # some port

        self.tower_conveyor_motor = Talon(self.ports.tower_conveyor_motor_port)  # some port

        self.joystick = Joystick(0)
        # self.chassis_navx = AHRS.create_spi()
        Compressor().setClosedLoopControl(False)

    def robotPeriodic(self):
        self.shooter.has_just_been_pressed(self.joystick.getRawButtonPressed(0))
        self.intake.has_just_been_pressed(self.joystick.getTopPressed())
        if self.isAutonomousEnabled():
            self.chassis.set_autonomous()
        elif self.isOperatorControlEnabled():
            self.chassis.set_teleop()

    def teleopInit(self):
        self.chassis.set_teleop()
        NetworkTables.initialize(server="10.43.20.149")
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.chassis.reset_encoders()

        self.sd.putBoolean("intake up", True)
        self.sd.putBoolean("intake roll", False)
        self.sd.putBoolean("intake save roll", False)

        self.sd.putBoolean("elevator up", False)
        # logging.basicConfig(level=logging.DEBUG)

    def teleopPeriodic(self):
        """
        r,l = self.chassis.get_encoder_ticks()
        self.sd.putNumber('right encoder',r)
        self.sd.putNumber("space")
        self.sd.putNumber('left encoder',l)
        self.sd.putNumber("space")
        self.sd.putNumber("angle")
        """
        if self.sd.getBoolean("intake up", True):
            self.intake.lift()
        else:
            self.intake.unlift()

        if self.sd.getBoolean("intake roll", False):
            self.intake.roll()
        else:
            self.intake.stop_rolling()

        # if self.joystick.getTopReleased():


        if self.sd.getBoolean("intake save roll", False):
            self.intake.save_roll()
        else:
            self.intake.stop_save_rolling()

        if self.sd.getBoolean("elevator up", False):
            self.elevator.lift()
        else:
            self.elevator.go_down()

        self.chassis.set_speed(self.joystick.getY(), self.joystick.getZ())


if __name__ == "__main__":
    wpilib.run(MyRobot)
