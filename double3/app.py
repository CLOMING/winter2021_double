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
from window import Window


class App:
    def __init__(self) -> None:
        width: int = 1920
        height: int = 1080

        self.core = Core()
        self.camera = Camera(width=width,
                             height=height)
        self.robot: BaseRobot = Robot()
        self.window = Window(window_name='DEMO',
                             width=width,
                             height=height,
                             on_lbutton_down=lambda *_: self.core.switch())

    def main(self):
        self.window.set()
        self.camera.set()
        self.robot.set()
        while True:
            if not self.window.is_opened():
                break

            _, img = self.camera.capture()

            self.core.detect_person(img)
            img = self.core.detect_face_and_mask(img)

            key = self.window.show(img)
            if key == 27:  # ESC
                if self.core.rekognition_setting.is_enabled:
                    self.core.switch()
                break

            moving_strategy = self.core.decide_move()
            self.robot.move(moving_strategy)
            self.core.speak()

        self.camera.close()
        self.window.close()
        self.robot.close()


if __name__ == "__main__":
    App().main()
