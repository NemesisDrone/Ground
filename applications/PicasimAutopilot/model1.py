# Autopilot model
from picasim import Plane


class AutopilotModel1:
    def __init__(self, plane: Plane):
        self.plane = plane

    def start(self):
        print("Take control")
        self.plane.take_control()
        print("Start autopilot")

        while True:
            pass

    def update(self, state, setpoint):
        pass
