from threading import Lock
from typing import List, Optional, Tuple
import numpy as np

from winter2021_recognition.amazon_rekognition import MaskStatus
from winter2021_recognition.amazon_rekognition.detect_labels import Person
from winter2021_recognition.amazon_rekognition.utils import calculate_IoU


class State:
    def __init__(self) -> None:
        self.faces: List[Face] = []
        self.people: List[Person] = []
        self.is_core_running: bool = False
        self.lock = Lock()

    def clear(self) -> None:
        try:
            self.lock.release()
            try:
                self.lock.acquire()
                self.faces.clear()
                self.people.clear()
            finally:
                self.lock.release()
        except:
            pass

    def set_face_info(self, id: int, external_id: Optional[str], name: Optional[str]) -> None:
        self.lock.acquire()
        try:
            face = [face for face in self.faces if face.id == id]
            index = self.faces.index(face[0])
            self.faces[index].set_external_id(external_id)
            self.faces[index].set_name(name)
        except:
            pass
        finally:
            self.lock.release()

    def set_mask_status(self, id: int, mask_status: MaskStatus) -> None:
        self.lock.acquire()
        try:
            face = [face for face in self.faces if face.id == id]
            index = self.faces.index(face[0])
            self.faces[index].set_mask_status(mask_status)
        except:
            pass
        finally:
            self.lock.release()


class Box:
    def __init__(
        self,
        left: int,
        right: int,
        top: int,
        bottom: int,
        frame: int,
    ) -> None:
        self.left = int(left)
        self.right = int(right)
        self.top = int(top)
        self.bottom = int(bottom)
        self.frame = int(frame)

    def to_tuple(self) -> Tuple[int, int, int, int]:
        return self.left, self.right, self.top, self.bottom


class Face:
    __id = 0

    def __init__(
        self,
        box: Box,
        img: np.ndarray,
    ) -> None:
        self.id = Face.__id
        Face.__id += 1

        self.external_id: Optional[str] = None
        self.box = box
        self.img = img
        self.mask_status: MaskStatus = MaskStatus.UNKNOWN
        self.name: Optional[str] = None

    @property
    def frame(self) -> int:
        return self.box.frame

    def set_external_id(self, external_id: Optional[str]) -> None:
        if external_id:
            self.external_id = external_id

    def set_name(self, name: Optional[str]) -> None:
        if name:
            self.name = name

    def set_mask_status(self, mask_status: MaskStatus) -> None:
        if not (mask_status == MaskStatus.UNKNOWN):
            self.mask_status = mask_status

    def compare(self, box: Box) -> bool:
        return calculate_IoU(box.to_tuple(), self.box.to_tuple()) >= 0.5

    def update(self, box: Box, img: np.ndarray) -> None:
        self.box = box
        self.img = img
