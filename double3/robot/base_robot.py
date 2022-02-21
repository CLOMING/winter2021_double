from abc import ABCMeta, abstractmethod
from multiprocessing import Process
from pip import List
from state import State


class BaseRobot(metaclass=ABCMeta):
    def __init__(self, state: State) -> None:
        self.state = state
        self.moving_strategies: List[MovingStrategy] = []

        self.check_thread = Process(target=self.__check)
        self.move_thread = Process(target=self.__run)

    def set(self):
        self.enable_camara()
        self.enable_navigate()

    def start(self):
        self.check_thread.start()
        self.move_thread.start()

    def close(self):
        self.check_thread.stop()
        self.move_thread.stop()
        self.disable_camera()
        self.disable_navigate()

    @abstractmethod
    def enable_navigate(self):
        pass

    @abstractmethod
    def enable_camara(self):
        pass

    @abstractmethod
    def disable_navigate(self):
        pass

    @abstractmethod
    def disable_camera(self):
        pass

    def __check(self) -> None:
        while True:
            # TODO: 로봇을 움직여야 하는지 여부 판단
            pass

    def __run(self) -> None:
        while True:
            # TODO: 로봇 움직이기
            pass


class MovingStrategy:
    # TODO: double3sdk
    pass


try:
    from robot.robot import Robot as __Robot
    __Robot()
except:
    from robot.mock_robot import MockRobot as __Robot


Robot: BaseRobot = __Robot
