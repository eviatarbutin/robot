from ctre import WPI_TalonSRX, FeedbackDevice
from wpilib.drive import DifferentialDrive

from navx import AHRS
#from physics import PhysicsEngine
"""
import wpilib.serialport as s
d=s.SerialPort(baudRate=5,port=s.SerialPort.Port.kUSB)
d.getBytesReceived()
"""

class Chassis:
    left_master: WPI_TalonSRX
    left_slave: WPI_TalonSRX
    right_master: WPI_TalonSRX
    right_slave: WPI_TalonSRX
    #navx: AHRS

    def __init__(self):
        self.teleop = False
        self.autonomous = False
        self.y_speed = 0
        self.z_speed = 0
        self.left_motor_speed = 0
        self.right_motor_speed = 0

    def setup(self):
        self.left_slave.follow(self.left_master)
        self.right_slave.follow(self.right_master)

        self.right_master.setSensorPhase(False)
        self.left_slave.setSensorPhase(False)

        self.right_master.setInverted(True)
        self.right_slave.setInverted(True)
        self.left_master.setInverted(True)
        self.left_slave.setInverted(True)

        self.left_master.configSelectedFeedbackSensor(FeedbackDevice.QuadEncoder)
        self.right_master.configSelectedFeedbackSensor(FeedbackDevice.QuadEncoder)

        self.left_master.configVoltageCompSaturation(11)
        self.right_master.configVoltageCompSaturation(11)

        self.left_master.enableVoltageCompensation(True)
        self.right_master.enableVoltageCompensation(True)

        self.diff_drive = DifferentialDrive(self.left_master, self.right_master)

    def set_teleop(self):
        self.teleop = True
        self.autonomous = False

    def set_autonomous(self):
        self.autonomous = True
        self.teleop = False

    def get_encoder_ticks(self):
        left_pos = self.left_master.getSelectedSensorPosition()
        right_pos = self.right_master.getSelectedSensorPosition()
        return left_pos, right_pos

    def set_motors_values(self, left: float, right: float):
        self.left_motor_speed = left
        self.right_motor_speed = right
        self.left_master.set(self.left_motor_speed)
        self.right_master.set(self.right_motor_speed)
        #self.diff_drive.leftMotor.set(left)
        #self.diff_drive.rightMotor.set(right)

    def set_speed(self, y_speed, z_speed):
        self.y_speed = y_speed
        self.z_speed = z_speed

    def reset_encoders(self):
        self.left_master.setSelectedSensorPosition(0)
        self.right_master.setSelectedSensorPosition(0)

    def execute(self):
        if self.teleop:
            self.diff_drive.arcadeDrive(self.y_speed, self.z_speed)
        elif self.autonomous:
            pass
            #print("chassis", self.left_motor_speed, self.right_motor_speed)
            #self.diff_drive.leftMotor.set(self.left_motor_speed)
            #self.diff_drive.rightMotor.set(self.right_motor_speed)
            #self.left_master.set(ControlMode.PercentOutput, self.left_motor_speed)
            #self.right_master.set(ControlMode.PercentOutput, self.right_motor_speed)
            #self.left_master.set(self.left_motor_speed)
            #self.right_master.set(self.right_motor_speed)

