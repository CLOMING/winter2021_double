import subprocess
import sys
from typing import Tuple
import cv2
import numpy as np


class Camera:
    def __init__(
        self,
        width: int,
        height: int,
    ) -> None:
        self.width = width
        self.height = height

    def use_usb_camera(self):
        self.cam = cv2.VideoCapture(6)
        self.cam.set(3, self.width)
        self.cam.set(4, self.height)

    def use_default(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, self.width)
        self.cam.set(4, self.height)

    def use_linux_usb(
        self,
        dev: int = 0,
    ):
        """
        Need compiling OpenCV with Gstreamer - See `install-opencv.md`
        """
        gst_str = ('v4l2src device=/dev/video{} ! '
                   'video/x-raw, width=(int){}, height=(int){} ! '
                   'videoconvert ! appsink').format(dev, self.width, self.height)
        self.cam = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

    def use_jetson(self):
        """
        Need compiling OpenCV with Gstreamer - See `install-opencv.md`
        """
        gst_elements = str(subprocess.check_output('gst-inspect-1.0'))
        if 'nvcamerasrc' in gst_elements:
            # On versions of L4T prior to 28.1, add 'flip-method=2' into gst_str
            gst_str = ('nvcamerasrc ! '
                       'video/x-raw(memory:NVMM), '
                       'width=(int)2592, height=(int)1458, '
                       'format=(string)I420, framerate=(fraction)30/1 ! '
                       'nvvidconv ! '
                       'video/x-raw, width=(int){}, height=(int){}, '
                       'format=(string)BGRx ! '
                       'videoconvert ! appsink').format(self.width, self.height)
        elif 'nvarguscamerasrc' in gst_elements:
            gst_str = ('nvarguscamerasrc ! '
                       'video/x-raw(memory:NVMM), '
                       'width=(int){}, height=(int){}, '
                       'format=(string)NV12, framerate=(fraction)30/1 ! '
                       'nvvidconv flip-method=2 ! '
                       'video/x-raw, width=(int){}, height=(int){}, '
                       'format=(string)BGRx ! '
                       'videoconvert ! appsink').format(self.width, self.height, self.width, self.height)
        else:
            raise RuntimeError('onboard camera source not found!')

        self.cam = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

    def set(self):
        """
        Due to onboard-camera error, we will use usb camera
        """
        # try:
        #     self.use_jetson()
        # except RuntimeError:
        #     self.use_linux_usb()
        # except:
        #     self.use_default()

        self.use_usb_camera()

        if not self.cam or not self.cam.isOpened():
            self.use_default()

        if not self.cam or not self.cam.isOpened():
            sys.exit('Fail to open camera')

    def close(self):
        self.cam.release()

    def capture(self) -> Tuple[bool, np.ndarray]:
        return self.cam.read()
