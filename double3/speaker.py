from typing import Callable, List


from state import Face, State
from thread import StoppableThread
from winter2021_recognition.amazon_rekognition import MaskStatus
from winter2021_recognition.amazon_polly import TTS


class Target:
    __index = 0

    def __init__(self,
                 face: Face,
                 message: str,
                 check: Callable[[], bool]) -> None:
        self.index = Target.__index
        Target.__index += 1
        self.face = face
        self.message = message
        self.check = check


class Speaker:
    def __init__(self, state: State) -> None:
        self.state = state
        self.targets: List[Target] = []

        try:
            from double3sdk import Double3SDK
            self.sdk = Double3SDK()
        except:
            self.sdk = None

    def __set(self) -> None:
        self.enable_speaker()
        self.target_pool_manager = DetectTargetThread(
            self.state, self.get_targets, self.update_targets)
        self.worker = SpeakThread(
            self.get_targets, self.remove_target, self.check_target_exist)

    def start(self) -> None:
        self.__set()
        self.target_pool_manager.start()
        self.worker.start()

    def close(self) -> None:
        self.target_pool_manager.terminate()
        self.target_pool_manager.join()

        self.worker.terminate()
        self.worker.join()

        self.targets.clear()

        self.disable_speaker()

    def enable_speaker(self) -> None:
        if not self.sdk:
            return

        self.sdk.speaker.enable()

    def disable_speaker(self) -> None:
        if not self.sdk:
            return

        self.sdk.speaker.disable()

    def update_targets(self, targets: List[Target]) -> None:
        self.targets = targets

    def get_targets(self) -> List[Target]:
        return self.targets

    def check_target_exist(self, target: Target) -> bool:
        return target in self.targets

    def remove_target(self, target: Target) -> None:
        self.targets.remove(target)


class DetectTargetThread(StoppableThread):
    def __init__(self,
                 state: State,
                 get_targets: Callable[[], List[Target]],
                 update_targets: Callable[[List[Target]], None]):
        super().__init__()
        self.state = state
        self.get_targets = get_targets
        self.update_targets = update_targets

    def run(self):
        while not self.stopped():
            if not self.state.is_core_running:
                self._stop_event.wait(0.1)
                continue

            targets = [
                Target(
                    face,
                    f'{face.name or "손"}님, 마스크를 착용해 주시기 바랍니다. ',
                    lambda: face.mask_status == MaskStatus.NOT_WEARED
                )
                for face in self.state.faces if face.mask_status == MaskStatus.NOT_WEARED
            ]
            self.update_targets(targets)

            self._stop_event.wait(0.1)


class SpeakThread(StoppableThread):
    def __init__(self,
                 get_targets: Callable[[], List[Target]],
                 remove_target: Callable[[Target], None],
                 check_target_exist: Callable[[Target], bool]):
        super().__init__()
        self.get_targets = get_targets
        self.remove_target = remove_target
        self.check_target_exist = check_target_exist
        self.tts = TTS()

    def run(self):
        while not self.stopped():
            targets = self.get_targets()
            for target in targets:
                if self.check_target_exist(target):
                    self.remove_target(target)
                    if target.check():
                        self.tts.read(target.message)
                    self._stop_event.wait(2)
