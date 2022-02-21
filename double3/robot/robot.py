from .base_robot import BaseRobot, MovingStrategy
from double3sdk import Double3SDK


class Robot(BaseRobot):
    def __init__(self) -> None:
        self.sdk = Double3SDK()

    def enable_camara(self):
        # TODO: double3sdk
        pass

    def enable_speaker(self):
        # TODO: double3sdk
        pass

    def disable_camera(self):
        # TODO: double3sdk
        pass

    def disable_speaker(self):
        # TODO: double3sdk
        pass

    def move(self, moving_strategy: MovingStrategy):
        # TODO: double3sdk
        pass
