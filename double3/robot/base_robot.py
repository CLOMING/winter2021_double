from abc import ABCMeta, abstractmethod
from typing import Callable, List

from thread import StoppableThread
from state import State


class MovingStrategy:
    # TODO: double3sdk
    pass


class BaseRobot(metaclass=ABCMeta):
    def __init__(self, state: State) -> None:
        self.state = state
        self.moving_strategies: List[MovingStrategy] = []

    def __set(self):
        self.enable_camara()
        self.enable_navigate()
        self.check_thread = CheckRobotThread(
            self.get_state, self.get_moving_strategies, self.update_moving_strategies)
        self.move_thread = RunRobotThread(self.get_moving_strategies)

    def start(self):
        self.__set()
        self.check_thread.start()
        self.move_thread.start()

    def close(self):
        self.check_thread.terminate()
        self.check_thread.join()

        self.move_thread.terminate()
        self.move_thread.join()

        self.moving_strategies.clear()

        self.disable_camera()
        self.disable_navigate()

    def get_state(self) -> State:
        return self.state

    def update_moving_strategies(self, moving_strategies: List[MovingStrategy]) -> None:
        self.moving_strategies = moving_strategies

    def get_moving_strategies(self) -> List[MovingStrategy]:
        return self.moving_strategies

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


class CheckRobotThread(StoppableThread):
    def __init__(self,
                 get_state: Callable[[], State],
                 get_moving_strategies: Callable[[], List[MovingStrategy]],
                 update_moving_strategies: Callable[[List[MovingStrategy]], None]):
        super().__init__()
        self.get_state = get_state
        self.get_moving_strategies = get_moving_strategies
        self.update_moving_strategies = update_moving_strategies

    def run(self):
        while not self.stopped():
            # TODO: 로봇을 어떻게 움직일지 여부 판단
            self._stop_event.wait(0.1)


class RunRobotThread(StoppableThread):
    def __init__(self,
                 get_moving_strategies: Callable[[], List[MovingStrategy]]):
        super().__init__()
        self.get_moving_strategies = get_moving_strategies

    def run(self):
        while not self.stopped():
            # TODO: 로봇 움직이기
            self._stop_event.wait(0.1)


try:
    from robot.robot import Robot as __Robot
    __Robot()
except:
    from robot.mock_robot import MockRobot as __Robot


Robot: BaseRobot = __Robot
