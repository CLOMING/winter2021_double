from .base_robot import BaseRobot, MovingStrategyDrive, MovingStrategyStop, MovingStrategyTarget


class MockRobot(BaseRobot):
    def enable_camara(self):
        print('MockRobot camaera enabled.')

    def enable_navigate(self):
        print('MockRobot navigate enabled.')

    def disable_camera(self):
        print('MockRobot camaera disabled.')

    def disable_navigate(self):
        print('MockRobot navigate disabled.')

    def navigate_drive(self, strategy: MovingStrategyDrive):
        print(f'MockRobot will drive: {strategy}')

    def navigate_target(self, strategy: MovingStrategyTarget):
        print(f'MockRobot will navigate to target: {strategy}')

    def stop_move(self, strategy: MovingStrategyStop):
        print(f'MockRobot stopped.')
