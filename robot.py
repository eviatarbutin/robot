import wpilib
from navx import AHRS
from ctre import WPI_TalonSRX
from magicbot import MagicRobot
from components.chassis import Chassis
from networktables.networktables import NetworkTables
from wpilib import Joystick, DoubleSolenoid, DigitalInput
from wpilib import Compressor
from components.intake import Intake
from components.elevator import Elevator


class MyRobot(MagicRobot):
    chassis: Chassis
    intake: Intake
    elevator: Elevator

    def createObjects(self):
        self.chassis_left_master = WPI_TalonSRX(2)
        self.chassis_left_slave = WPI_TalonSRX(1)
        self.chassis_right_master = WPI_TalonSRX(4)
        self.chassis_right_slave = WPI_TalonSRX(3)

        self.intake_maaster_raiser = WPI_TalonSRX()  # some port
        self.intake_slave_raiser = WPI_TalonSRX()  # some port
        self.intake_micro_switch = DigitalInput()  # some port

        self.intake_master_roller = WPI_TalonSRX()  # some port
        self.intake_slave_roller = WPI_TalonSRX()  # some port

        self.intake_master_saving_roller = WPI_TalonSRX()  # some port
        self.intake_slave_saving_roller = WPI_TalonSRX()  # some port

        self.elevator_micro_switch = DigitalInput()  # some port
        self.elevator_master_raiser = WPI_TalonSRX()  # some port
        self.elevator_slave_raiser = WPI_TalonSRX()  # some port

        self.pusher_disk_pusher = DoubleSolenoid(0, 1)

        self.rocket_launch_left_switch = DigitalInput(0)
        self.rocket_launch_right_switch = DigitalInput(1)

        self.joystick = Joystick(0)
        # self.chassis_navx = AHRS.create_spi()
        Compressor().setClosedLoopControl(False)

    def robotPeriodic(self):
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

        if self.sd.getBoolean("intake save roll", False):
            self.intake.save_roll()
        else:
            self.intake.stop_save_rolling()

        if self.sd.getBoolean("elevator up", False):
            self.elevator.lift()
        else:
            self.elevator.go_down()

        self.chassis.set_speed(self.joystick.getY(), self.joystick.getZ())
        # self.elevator.set_button(self.joystick.getTopPressed())
        # self.rocket_launch.launch()
        # self.state.engage()


if __name__ == "__main__":
    wpilib.run(MyRobot)
