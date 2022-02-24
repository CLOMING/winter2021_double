from abc import ABCMeta, abstractmethod
import time
from typing import Callable, List, Optional

from thread import StoppableThread
from state import State
from winter2021_recognition.amazon_rekognition.detect_protective_equipment import MaskStatus


class MovingStrategy:
    pass


class MovingStrategyStop(MovingStrategy):
    def __init__(self) -> None:
        super().__init__()


class MovingStrategyTarget(MovingStrategy):
    def __init__(self,
                 x: int,
                 y: int) -> None:
        self.x = x
        self.y = y


class MovingStrategyDrive(MovingStrategy):
    # forward, clockwise = double3 sdk navigate.py drive (throttle, turn)
    def __init__(self,
                 forward: float,
                 clockwise: float) -> None:
        self.forward = float(forward)
        self.clockwise = float(clockwise)


class MovingStrategyBackward(MovingStrategyDrive):
    def __init__(self,
                 clockwise: Optional[float] = None) -> None:
        super().__init__(forward=-1.0, clockwise=clockwise or 0.0)


class BaseRobot(metaclass=ABCMeta):
    def __init__(self, state: State) -> None:
        self.state = state
        self.moving_strategies: List[MovingStrategy] = []

    def __set(self):
        self.enable_camara()
        self.enable_navigate()
        self.check_thread = CheckRobotThread(self.get_state,
                                             self.get_moving_strategies,
                                             self.update_moving_strategies)
        self.move_thread = RunRobotThread(self.get_moving_strategies,
                                          self.remove_strategy,
                                          self.check_exist,
                                          self.move)
        time.sleep(2)

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
        for strategy in moving_strategies:
            self.moving_strategies.append(strategy)

    def get_moving_strategies(self) -> List[MovingStrategy]:
        return self.moving_strategies

    def remove_strategy(self, strategy: MovingStrategy) -> None:
        self.moving_strategies.remove(strategy)

    def check_exist(self, strategy: MovingStrategy) -> bool:
        return strategy in self.moving_strategies

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

    @abstractmethod
    def navigate_drive(self, strategy: MovingStrategyDrive):
        pass

    @abstractmethod
    def navigate_target(self, strategy: MovingStrategyTarget):
        pass

    @abstractmethod
    def stop_move(self, strategy: MovingStrategyStop):
        pass

    def move(self, strategy: MovingStrategy):
        if isinstance(strategy, MovingStrategyDrive):
            self.navigate_drive(strategy)
        elif isinstance(strategy, MovingStrategyTarget):
            self.navigate_target(strategy)
        elif isinstance(strategy, MovingStrategyStop):
            self.stop_move(strategy)


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
            faces = [face for face in self.get_state(
            ).faces if face.mask_status == MaskStatus.WEARED]
            people = [person for person in self.get_state().people]

            if not faces and people:
                closest_person = people[0]
                if not (len(people) == 1):
                    for person in people:
                        if person.bounding_box.bottom > closest_person.bounding_box.bottom:
                            closest_person = person

                closest_bounding_box = closest_person.bounding_box
                if closest_bounding_box.width > 0.9 or closest_bounding_box.height > 0.9:
                    self.update_moving_strategies([MovingStrategyBackward()])
                else:
                    clockwise = closest_bounding_box.left+closest_bounding_box.width/2-0.5
                    self.update_moving_strategies(
                        [MovingStrategyDrive(0.5, clockwise)])
            else:
                self.update_moving_strategies([MovingStrategyStop()])

            self._stop_event.wait(0.1)


class RunRobotThread(StoppableThread):
    def __init__(self,
                 get_moving_strategies: Callable[[], List[MovingStrategy]],
                 remove_strategy: Callable[[MovingStrategy], None],
                 check_exist: Callable[[MovingStrategy], bool],
                 move: Callable[[MovingStrategy], None]):
        super().__init__()
        self.get_moving_strategies = get_moving_strategies
        self.remove_strategy = remove_strategy
        self.check_exist = check_exist
        self.move = move

    def run(self):
        while not self.stopped():
            strategies = [
                strategy for strategy in self.get_moving_strategies()]

            if not strategies:
                self._stop_event.wait(0.1)
                continue

            for strategy in strategies:
                if self.check_exist(strategy):
                    self.remove_strategy(strategy)
                    self.move(strategy)

            self._stop_event.wait(0.1)


try:
    from robot.robot import Robot as __Robot
    __Robot(State())
except:
    from robot.mock_robot import MockRobot as __Robot


Robot: BaseRobot = __Robot
