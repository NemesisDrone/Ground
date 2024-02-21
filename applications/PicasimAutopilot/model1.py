# Autopilot model
from datetime import datetime, timedelta
import time

from pid import PID
from picasim import Plane, Channels


class AutopilotModel1:
    """
    A simple autopilot model
    """
    def __init__(self, plane: Plane):
        self.plane = plane

        self.altitude_objective = 20
        self.roll_objective = 0.1

        self.is_climbing = False
        self.is_turning = False

    def test_pid_controller(self):
        last_update = datetime.now()
        update_interval = 0.1 # seconds

        p = 0.02
        i = p / 10
        d = 0

        roll_pid = PID(p, i, d)
        pitch_pid = PID(p, i, d)
        altitude_pid = PID(p, i, d)

        desired_roll = 0
        desired_pitch = 10

        roll_pid.SetPoint = desired_roll
        pitch_pid.SetPoint = desired_pitch
        altitude_pid.SetPoint = self.altitude_objective

        while True:
            if datetime.now() > (last_update + timedelta(milliseconds=update_interval*1000)):
                last_update = datetime.now()
                data = self.plane.get_telemetry()
                if not data:
                    continue

                roll_pid.update(data.roll)
                pitch_pid.update(data.pitch)

                self.plane.control(Channels.ELEVATOR, -pitch_pid.output)
                self.plane.control(Channels.AILERON, roll_pid.output)

                print(f"Roll: {data.roll}, Pitch: {data.pitch}, Roll PID: {roll_pid.output}, Pitch PID: {pitch_pid.output}")

                time.sleep(0.05)

    def run(self):
        print("Take control")
        self.plane.take_control()
        print("Start autopilot")

        # Set speed to maximum
        self.plane.control(Channels.THROTTLE, 1)
        self.test_pid_controller()

        # while True:
        #     data = self.plane.get_telemetry()
        #     if not data:
        #         continue
        #
        #     if data.altitude < self.altitude_objective-1:
        #         if data.pitch < 20:
        #             self.plane.control(Channels.ELEVATOR, -0.2)
        #         else:
        #             self.plane.control(Channels.ELEVATOR, 0)
        #     elif data.altitude > self.altitude_objective+1:
        #         self.plane.control(Channels.ELEVATOR, 0.2)
        #     else:
        #         self.plane.control(Channels.ELEVATOR, 0)
        #
        #     if data.roll < self.roll_objective-1:
        #         self.plane.control(Channels.AILERON, 0.2)
        #     elif data.roll > self.roll_objective+5:
        #         self.plane.control(Channels.AILERON, -0.2)
        #     else:
        #         self.plane.control(Channels.AILERON, 0)
        #
        #     time.sleep(0.01)

