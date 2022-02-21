class MovingStrategy:
    # TODO: double3sdk
    pass


class BaseRobot:
    def set(self):
        self.enable_speaker()
        self.enable_camara()

    def close(self):
        self.disable_camera()
        self.disable_speaker()

    def enable_speaker(self):
        pass

    def enable_camara(self):
        pass

    def disable_speaker(self):
        pass

    def disable_camera(self):
        pass

    def move(self, moving_strategy: MovingStrategy):
        pass


try:
    from robot.robot import Robot as _Robot
    _Robot()
except:
    from robot.mock_robot import MockRobot as _Robot


Robot: BaseRobot = _Robot
