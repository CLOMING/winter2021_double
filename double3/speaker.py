from multiprocessing import Process
from pip import List
from time import sleep


from state import Face, State
from winter2021_recognition.amazon_polly import TTS


class Speaker:
    def __init__(self, state: State) -> None:
        self.tts = TTS()
        self.state = state
        self.targets: List[Target] = []

        try:
            from double3sdk import Double3SDK
            self.sdk = Double3SDK()
        except:
            self.sdk = None

        self.detect_process = Process(target=self.__check)
        self.read_process = Process(target=self.__run)

    def set(self) -> None:
        self.enable_speaker()

    def start(self) -> None:
        self.detect_process.start()
        self.read_process.start()

    def close(self) -> None:
        self.detect_process.terminate()
        self.read_process.terminate()
        self.disable_speaker()

    def enable_speaker(self) -> None:
        if not self.sdk:
            return

        #TODO: double3sdk

    def disable_speaker(self) -> None:
        if not self.sdk:
            return

        #TODO: double3sdk

    def __check(self) -> None:
        while True:
            # TODO: 어떤 사람에게 마스크를 쓰라고 경고할지 결정
            pass

    def __run(self) -> None:
        while True:
            targets = [face for face in self.targets]
            for target in targets:
                if target in self.targets:
                    self.targets.remove(target)
                    self.tts.read(
                        f'{target.face.name or "손"}님, 마스크를 착용해주시기 바랍니다.')
                sleep(2)

            sleep(10)


class Target:
    __index = 0

    def __init__(self, face: Face) -> None:
        self.face = face
        self.index = Target.__index
        Target.__index += 1
