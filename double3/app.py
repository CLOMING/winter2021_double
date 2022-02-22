if __name__ == '__main__':
    import os.path
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__),
                    'winter2021_recognition/amazon_rekognition'))
    sys.path.append(os.path.join(os.path.dirname(__file__),
                    'winter2021_recognition/amazon_polly'))
    sys.path.append(os.path.join(os.path.dirname(__file__), 'double3sdk'))

from camera import Camera
from core import Core
from robot import BaseRobot, Robot
from speaker import Speaker
from state import State
from window import Window


class App:
    def __init__(self) -> None:
        width: int = 1920
        height: int = 1080

        self.state = State()

        self.camera = Camera(width=width,
                             height=height)
        self.core = Core(self.state,
                         capture=self.camera.capture)
        self.robot: BaseRobot = Robot(self.state)
        self.speaker = Speaker(self.state)
        self.window = Window(self.state,
                             window_name='DEMO',
                             width=width,
                             height=height,
                             capture=self.camera.capture,
                             on_lbutton_down=lambda *_: self.core.close() if self.state.is_core_running else self.core.start())

    def main(self):
        self.set()
        try:
            self.window.start()
            self.robot.start()
            self.speaker.start()
        except Exception as e:
            print(f'Exception Raised: {e}')
        finally:
            self.close()

    def set(self):
        self.window.set()
        self.camera.set()
        self.robot.set()
        self.speaker.set()

    def close(self):
        try:
            self.window.close()
            self.state.lock.release()
            self.camera.close()
            self.core.close()
            self.robot.close()
            self.speaker.close()
        except:
            pass
        finally:
            sys.exit(0)


if __name__ == "__main__":
    App().main()
