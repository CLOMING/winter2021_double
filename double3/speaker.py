from typing import Callable, List


from state import Face, State
from thread import StoppableThread
from winter2021_recognition.amazon_polly import TTS


class Target:
    __index = 0

    def __init__(self, face: Face) -> None:
        self.face = face
        self.index = Target.__index
        Target.__index += 1


class Speaker:
    def __init__(self, state: State) -> None:
        self.state = state
        self.targets: List[Target] = []

        try:
            from double3sdk import Double3SDK
            self.sdk = Double3SDK()
        except:
            self.sdk = None

        self.detect_thread = DetectTargetThread(
            self.get_targets, self.update_targets)
        self.read_thread = SpeakThread(
            self.get_targets, self.remove_target, self.check_target_exist)

    def set(self) -> None:
        self.enable_speaker()

    def start(self) -> None:
        self.detect_thread.start()
        self.read_thread.start()

    def close(self) -> None:
        self.detect_thread.terminate()
        self.detect_thread.join()

        self.read_thread.terminate()
        self.read_thread.join()

        self.disable_speaker()

    def enable_speaker(self) -> None:
        if not self.sdk:
            return

        #TODO: double3sdk

    def disable_speaker(self) -> None:
        if not self.sdk:
            return

        #TODO: double3sdk

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
                 get_targets: Callable[[], List[Target]],
                 update_targets: Callable[[List[Target]], None]):
        super().__init__()
        self.get_targets = get_targets
        self.update_targets = update_targets

    def run(self):
        while not self.stopped():
            # TODO: TTS: 어떤 사람에게 마스크를 쓰라고 경고할지 target 결정
            # targets = []
            # self.update_targets(targets)

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
                    self.tts.read(
                        f'{target.face.name or "손"}님, 마스크를 착용해주시기 바랍니다.')
                    self._stop_event.wait(2)
            self._stop_event.wait(10)
