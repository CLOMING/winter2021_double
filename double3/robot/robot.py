from .base_robot import BaseRobot, MovingStrategyDrive, MovingStrategyStop, MovingStrategyTarget
from double3sdk import Double3SDK
from state import State


class Robot(BaseRobot):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.sdk = Double3SDK()

    def enable_camara(self):
        self.sdk.camera.enable()

    def enable_navigate(self):
        self.sdk.navigate.enable()

    def disable_camera(self):
        self.sdk.camera.disable()

    def disable_navigate(self):
        self.sdk.navigate.disable()

    def navigate_drive(self, strategy: MovingStrategyDrive):
        print(f'strategy: {strategy.forward}, {strategy.clockwise}')
        self.sdk.navigate.drive(
            strategy.forward, strategy.clockwise, False, False)

    def navigate_target(self, strategy: MovingStrategyTarget):
        self.sdk.navigate.target(strategy.x, strategy.y, 0, True, False, 0, "")

    def stop_move(self, strategy: MovingStrategyStop):
        print(f'stopped')
        pass
        # self.sdk.navigate.cancel_target() # if navigate.target is called
