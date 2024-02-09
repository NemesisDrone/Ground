import json
import threading
import DjangoSetup
from CommunicationHandler import CommunicationLayer
from ReplaySession import ReplaySessionManager


class SensorsListener(CommunicationLayer):
    """
    This class is used to listen to sensors data and save it in a replay session when recording
    """

    def __init__(self):
        super().__init__()
        self.replay_session_manager = ReplaySessionManager()

        """
        We start the thread to listen to the actions from the frontend
        """
        self.action_thread = threading.Thread(
            target=self._listen_redis_actions,
            daemon=True,
        )
        self.action_thread.start()

        self.sensors_thread = threading.Thread(
            target=self._listen_sensors,
            daemon=True,
        )
        self.sensors_thread.start()

        self.send_to_frontend({"route": "recorder:ready"})
        self.action_thread.join()
        self.sensors_thread.join()

    def _listen_redis_actions(self):
        """
        This method is used to listen to redis actions from the frontend
        """
        print("Listening to actions")
        for message in self.ps_frontend.listen():
            data = json.loads(message["data"])

            match data["route"]:
                case "recorder:start":
                    self.replay_session_manager.start_recording()

                case "recorder:stop":
                    self.replay_session_manager.stop_recording()

                case "recorder:pause":
                    self.replay_session_manager.pause_recording()

    def _listen_sensors(self):
        """
        This method is used to listen to the sensors data
        """
        print("Listening to sensors")
        for message in self.ps_drone.listen():
            try:
                data = json.loads(message["data"])
                self.replay_session_manager.add_update_data(data)

            except json.decoder.JSONDecodeError:
                print("Decode error")
                pass
            # data = json.loads(message["data"])
            # print(data)


if __name__ == "__main__":
    sensors_listener = SensorsListener()
    # sensors_listener.start()
