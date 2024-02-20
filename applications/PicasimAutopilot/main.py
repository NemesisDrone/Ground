from picasim import Plane
from model1 import AutopilotModel1


autopilot = AutopilotModel1(Plane())
autopilot.start()

# if __name__ == "__main__":
#     viewer = PlaneRenderer()
#     plane = Plane()
#     plane.take_control()
#     plane.control(3, 1)
#     plane.control(1, -1)
#
#     while True:
#         data = plane.get_telemetry()
#         if not data:
#             continue
#         viewer.set_orientation(data.roll, 0, 0)
#         time.sleep(0.01)

    # while True:
    #     data_input = input("Enter data to send: ")
    #
    #     if data_input == "exit":
    #         break
    #     pica_sim.send_data(data_input)

