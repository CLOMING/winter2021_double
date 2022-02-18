from dataclasses import dataclass
from threading import Thread
from typing import List, Optional, Tuple

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

from winter2021_recognition.amazon_rekognition import AmazonImage, FaceManager, FaceManagerExceptionFaceNotExistException, FaceManagerExceptionFaceNotSearchedException, FaceMatch, MaskDetector, MaskStatus, PeopleDetector, UserDatabase
from winter2021_recognition.amazon_rekognition.detect_labels import PeopleDetector, Person
from winter2021_recognition.amazon_rekognition.utils import calculate_IoU


@dataclass
class RekognitionSetting:
    period: int = 50
    face_detect_period: int = 5
    period_count: int = 0
    is_enabled: bool = False


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
    def __init__(
        self,
        box: Box,
        img: np.ndarray,
    ) -> None:
        self.external_id: Optional[str] = None
        self.box = box
        self.img = img
        self.mask_status: MaskStatus = MaskStatus.UNKNOWN
        self.name: Optional[str] = None
        self.__mask_thread: Optional[Thread] = None
        self.__face_thread: Optional[Thread] = None

    @property
    def frame(self) -> int:
        return self.box.frame

    def set_mask_thread(self) -> None:
        if self.__mask_thread and self.__mask_thread.is_alive():
            return

        self.__mask_thread = Thread(target=self.__detect_mask)

    def set_face_thread(self) -> None:
        if self.__face_thread and self.__face_thread.is_alive():
            return

        self.__face_thread = Thread(target=self.__detect_face)

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

    def run_rekognition(self) -> None:
        self.update_mask_status()
        self.update_name()

    def update_mask_status(self) -> None:
        self.set_mask_thread()

        if not self.__mask_thread.is_alive():
            self.__mask_thread.start()

    def update_name(self) -> None:
        self.set_face_thread()

        if not self.__face_thread.is_alive():
            self.__face_thread.start()

    def __detect_mask(self) -> None:
        mask_detector = MaskDetector(
            AmazonImage.from_ndarray(self.img), confidence=70)
        people = mask_detector.run()

        if not people:
            return

        person = people[0]

        self.set_mask_status(person.mask_status)

    def __detect_face(self) -> None:
        image = AmazonImage.from_ndarray(self.img)
        face_manager = FaceManager()

        face_match: FaceMatch
        try:
            face_match = face_manager.search_only_one_face(image)
        except FaceManagerExceptionFaceNotSearchedException:
            face_match = None

        user_id = str
        if not face_match:
            try:
                user_id, _ = face_manager.add_face(
                    image=image, check_face_exist=False)
            except:
                return
        else:
            user_id = face_match.face.external_image_id

        name = UserDatabase().read(user_id).name

        self.set_external_id(user_id)
        self.set_name(name)

    def draw(self, img: np.ndarray) -> np.ndarray:
        mask_color_dict = {
            MaskStatus.NOT_WEARED: (0, 0, 255),
            MaskStatus.UNKNOWN: (0, 0, 0),
            MaskStatus.WEARED: (0, 255, 0),
        }

        color = mask_color_dict[self.mask_status]
        cv2.rectangle(
            img,
            (self.box.left, self.box.top),
            (self.box.right, self.box.bottom),
            color,
            thickness=2,
        )

        mask_text_dict = {
            MaskStatus.NOT_WEARED: '마스크 미착용',
            MaskStatus.UNKNOWN: '',
            MaskStatus.WEARED: '마스크 착용'
        }

        mask_text = mask_text_dict[self.mask_status]

        text = ''

        if self.name:
            text += self.name

        if mask_text:
            text += f': {mask_text}'

        org = (self.box.left, self.box.bottom)

        pil_image = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype("fonts/gulim.ttc", 20)
        draw.text(org, text, font=font, fill=color)

        return np.array(pil_image)


class Core:
    def __init__(self) -> None:
        self.rekognition_setting = RekognitionSetting()
        self.faces: List[Face] = []
        self.people: List[Person] = []

    def switch(self):
        self.rekognition_setting.is_enabled = not self.rekognition_setting.is_enabled
        if self.rekognition_setting.is_enabled:
            self.faces.clear()

    def detect_face_and_mask(self, img: np.ndarray) -> np.ndarray:
        if not self.rekognition_setting.is_enabled:
            img = self.show_help_text(img)
            return img

        t = Thread(target=lambda: self.detect_face_and_mask_rekognition(img))
        t.start()

        img = self.draw(img)

        return img

    def detect_person(self, img: np.ndarray):
        if not self.rekognition_setting.is_enabled:
            return

        t = Thread(target=lambda: self.detect_person_rekognition(img))
        t.start()

    def draw(self, img: np.ndarray) -> np.ndarray:
        for face in self.faces:
            img = face.draw(img)

        return img

    def show_help_text(self, img: np.ndarray) -> np.ndarray:
        text = 'Tap screen to start rekognition'
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, 1, 2)[0]
        org = (int((img.shape[1] - text_size[0]) / 2),
               int((img.shape[0] + text_size[1]) / 2))
        cv2.putText(img, text, org, font, 1, (255, 255, 255), 2,)

        return img

    def detect_person_rekognition(self, img: np.ndarray):
        people_detector = PeopleDetector(AmazonImage.from_ndarray(img))
        self.people = people_detector.run()
        print(self.people)

    def detect_face_and_mask_rekognition(self, img: np.ndarray) -> None:
        self.rekognition_setting.period_count += 1

        current_period_count = self.rekognition_setting.period_count

        if current_period_count % self.rekognition_setting.face_detect_period:
            return

        face_manager = FaceManager()
        try:
            cropped_img_infos = face_manager.crop_image(
                AmazonImage.from_ndarray(img))
        except FaceManagerExceptionFaceNotExistException:
            return

        for infos in cropped_img_infos:
            is_exist = False
            width, height = infos[0].shape[1], infos[0].shape[0]
            left, top = infos[1], infos[2]
            right, bottom = left + width, top + height
            box = Box(left, right, top, bottom, current_period_count)
            for face in self.faces:
                if face.frame == current_period_count:
                    continue

                if not face.compare(box):
                    continue

                face.update(box, infos[0])
                is_exist = True
                break

            if not is_exist:
                self.faces.append(Face(box, infos[0]))

        for i, face in enumerate(self.faces):
            if face.frame == current_period_count:
                continue

            del self.faces[i]

        if current_period_count % self.rekognition_setting.period:
            return

        threads: List[Thread] = []
        for face in self.faces:
            thread = Thread(target=face.run_rekognition)
            thread.start()

        for thread in threads:
            thread.join()
