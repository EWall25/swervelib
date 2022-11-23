import math

import astropy.units as u
import ctre
import wpilib
from astropy.units import Quantity
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics

from swervelib import Swerve, SwerveParameters, SwerveModuleParameters
from swervelib.configs import CANDeviceID, RelativeModulePosition


class RobotContainer:
    def __init__(self):
        field_relative = True
        open_loop = True

        track_width: Quantity = 21.73 * u.imperial.inch
        wheel_base: Quantity = 21.73 * u.imperial.inch
        # fmt: off
        swerve_params = SwerveParameters(
            wheel_circumference=4 * math.pi * u.imperial.inch,  # SDS Wheel Circumference

            open_loop_ramp=0,
            closed_loop_ramp=0,

            # Mk4i L3 Gear Ratios
            drive_gear_ratio=6.12 / 1,
            angle_gear_ratio=(150 / 7) / 1,

            max_speed=4.5 * (u.m / u.s),
            max_angular_velocity=11.5 * (u.rad / u.s),

            kinematics=SwerveDrive4Kinematics(
                Translation2d(wheel_base.to_value(u.m) / 2, -track_width.to_value(u.m) / 2),
                Translation2d(wheel_base.to_value(u.m) / 2, track_width.to_value(u.m) / 2),
                Translation2d(-wheel_base.to_value(u.m) / 2, -track_width.to_value(u.m) / 2),
                Translation2d(-wheel_base.to_value(u.m) / 2, track_width.to_value(u.m) / 2),
            ),

            angle_continuous_current_limit=40,
            angle_peak_current_limit=60,
            angle_peak_current_duration=0.01,
            angle_enable_current_limit=True,

            drive_continuous_current_limit=40,
            drive_peak_current_limit=60,
            drive_peak_current_duration=0.01,
            drive_enable_current_limit=True,

            angle_kP=1,
            angle_kI=0,
            angle_kD=0,
            angle_kF=0,

            drive_kP=1,
            drive_kI=0,
            drive_kD=0,
            drive_kF=0,

            drive_kS=1 / 12,
            drive_kV=0 / 12,
            drive_kA=0 / 12,

            angle_neutral_mode=ctre.NeutralMode.Brake,
            drive_neutral_mode=ctre.NeutralMode.Coast,

            invert_angle_motor=False,
            invert_drive_motor=False,
            invert_angle_encoder=False,

            invert_gyro=True,
            gyro_id=CANDeviceID(0),
        )
        module_params = (
            SwerveModuleParameters(
                position=RelativeModulePosition.FRONT_LEFT,
                angle_offset=0,
                drive_motor_id=CANDeviceID(0),
                angle_motor_id=CANDeviceID(4),
                angle_encoder_id=CANDeviceID(0),
            ),
            SwerveModuleParameters(
                position=RelativeModulePosition.FRONT_RIGHT,
                angle_offset=0,
                drive_motor_id=CANDeviceID(1),
                angle_motor_id=CANDeviceID(5),
                angle_encoder_id=CANDeviceID(1),
            ),
            SwerveModuleParameters(
                position=RelativeModulePosition.BACK_LEFT,
                angle_offset=0,
                drive_motor_id=CANDeviceID(2),
                angle_motor_id=CANDeviceID(6),
                angle_encoder_id=CANDeviceID(2),
            ),
            SwerveModuleParameters(
                position=RelativeModulePosition.BACK_RIGHT,
                angle_offset=0,
                drive_motor_id=CANDeviceID(3),
                angle_motor_id=CANDeviceID(7),
                angle_encoder_id=CANDeviceID(3),
            ),
        )
        # fmt: on

        self.stick = wpilib.Joystick(0)

        self.swerve = Swerve(module_params, swerve_params)
        self.swerve.setDefaultCommand(
            self.swerve.teleop_command(
                lambda: -self.stick.getRawAxis(1),
                lambda: self.stick.getRawAxis(0),
                lambda: -self.stick.getRawAxis(2),  # Invert for CCW+
                field_relative,
                open_loop,
            )
        )