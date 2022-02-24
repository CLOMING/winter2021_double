from typing import Any, Callable, Final, Optional, Tuple

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

from state import Face, State
from winter2021_recognition.amazon_rekognition import MaskStatus


class Window:
    def __init__(
        self,
        state: State,
        window_name: str,
        width: int,
        height: int,
        capture: Callable[[], Tuple[bool, np.ndarray]],
        on_lbutton_down: Optional[Callable[[
            int, int, Any, Any, ], None]] = None,
    ) -> None:
        self.state: Final = state
        self.window_name: Final = window_name
        self.width: Final = width
        self.height: Final = height
        self.capture: Final = capture
        self.on_lbutton_down: Final = on_lbutton_down
        self.stop_flag = False

    def set(self) -> None:
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.width, self.height)
        cv2.moveWindow(self.window_name, 0, 0)
        cv2.setWindowTitle(self.window_name, self.window_name)
        cv2.setMouseCallback(
            self.window_name, lambda *args: self.on_mouse_click(*args))

    def start(self) -> None:
        self.__draw()

    def close(self) -> None:
        self.stop_flage = True
        cv2.destroyWindow(self.window_name)

    def on_mouse_click(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN and self.on_lbutton_down:
            self.on_lbutton_down(x, y, flags, params)

    def is_opened(self) -> bool:
        return cv2.getWindowProperty(self.window_name, 0) >= 0

    def __draw(self) -> None:
        while True:
            if self.stop_flag:
                raise Exception('stop flag set.')

            if not self.is_opened():
                raise Exception('window is not opened')

            _, img = self.capture()

            if not self.state.is_core_running:
                img = self.__show_help_text(img)
            else:
                img = self.__draw_faces(img)

            cv2.imshow(self.window_name, img)
            key = cv2.waitKey(10)

            if key == 27:  # Press ESC
                raise Exception('Press esc')

    def __show_help_text(self, img: np.ndarray) -> np.ndarray:
        text = 'Tap screen to start rekognition'
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, 1, 6)[0]
        org = (int((img.shape[1] - text_size[0]) / 2),
               int((img.shape[0] + text_size[1]) / 2))
        cv2.putText(img, text, org, font, 1, (255, 255, 255), 6,)

        return img

    def __draw_faces(self, img: np.ndarray) -> np.ndarray:
        for face in self.state.faces:
            img = self.__draw_face(face, img)

        return img

    def __draw_face(self, face: Face, img: np.ndarray) -> np.ndarray:
        mask_color_dict = {
            MaskStatus.NOT_WEARED: (0, 0, 255),
            MaskStatus.UNKNOWN: (0, 0, 0),
            MaskStatus.WEARED: (0, 255, 0),
        }

        color = mask_color_dict[face.mask_status]
        cv2.rectangle(
            img,
            (face.box.left, face.box.top),
            (face.box.right, face.box.bottom),
            color,
            thickness=4,
        )

        mask_text_dict = {
            MaskStatus.NOT_WEARED: '마스크 미착용',
            MaskStatus.UNKNOWN: '',
            MaskStatus.WEARED: '마스크 착용'
        }

        mask_text = mask_text_dict[face.mask_status]

        text = ''

        if face.name:
            text += face.name

        if mask_text:
            text += f': {mask_text}'

        org = (face.box.left, face.box.bottom)

        pil_image = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype("fonts/gulim.ttc", 22)
        draw.text(org, text, font=font, fill=color)

        return np.array(pil_image)
