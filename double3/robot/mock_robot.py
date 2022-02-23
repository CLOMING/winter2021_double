from .base_robot import BaseRobot, MovingStrategy


class MockRobot(BaseRobot):
    def enable_camara(self):
        print('MockRobot camaera enabled.')

    def enable_navigate(self):
        print('MockRobot navigate enabled.')

    def disable_camera(self):
        print('MockRobot camaera disabled.')

    def disable_navigate(self):
        print('MockRobot navigate disabled.')
