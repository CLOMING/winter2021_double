from .base_robot import BaseRobot
from double3sdk import Double3SDK
from state import State


class Robot(BaseRobot):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.sdk = Double3SDK()

    def enable_camara(self):
        # TODO: double3sdk
        pass

    def enable_navigate(self):
        # TODO: double3sdk
        pass

    def disable_camera(self):
        # TODO: double3sdk
        pass

    def disable_navigate(self):
        # TODO: double3sdk
        pass
