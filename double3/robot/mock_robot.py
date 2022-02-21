from .base_robot import BaseRobot, MovingStrategy


class MockRobot(BaseRobot):
    def enable_camara(self):
        print('MockRobot camaera enabled.')

    def enable_speaker(self):
        print('MockRobot speaker enabled.')

    def disable_camera(self):
        print('MockRobot camaera disabled.')

    def disable_speaker(self):
        print('MockRobot speaker disabled.')

    def move(self, moving_strategy: MovingStrategy):
        print(f'MockRobot is moving along with {moving_strategy}')
