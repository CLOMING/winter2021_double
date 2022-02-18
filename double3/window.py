from typing import Any, Callable, Final, Optional

import cv2
import numpy as np


class Window:
    def __init__(
        self,
        window_name: str,
        width: int = 1920,
        height: int = 1080,
        on_lbutton_down: Optional[Callable[[
            int, int, Any, Any, ], None]] = None,
    ) -> None:
        self.window_name: Final[str] = window_name
        self.width = width
        self.height = height
        self.on_lbutton_down = on_lbutton_down

    def set(self) -> None:
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.width, self.height)
        cv2.moveWindow(self.window_name, 0, 0)
        cv2.setWindowTitle(self.window_name, self.window_name)
        cv2.setMouseCallback(
            self.window_name, lambda *args: self.on_mouse_click(*args))

    def on_mouse_click(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN and self.on_lbutton_down:
            self.on_lbutton_down(x, y, flags, params)

    def is_opened(self) -> bool:
        return cv2.getWindowProperty(self.window_name, 0) >= 0

    def show(self, img: np.ndarray) -> None:
        cv2.imshow(self.window_name, img)
        return cv2.waitKey(10)

    def close(self) -> None:
        cv2.destroyWindow(self.window_name)
