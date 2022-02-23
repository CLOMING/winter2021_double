from collections import deque
from typing import Callable, Deque, List, Tuple
import numpy as np

from state import Box, Face, State
from thread import StoppableThread
from winter2021_recognition.amazon_rekognition import AmazonImage, FaceManager, MaskDetector, MaskStatus, PeopleDetector, UserDatabase


class Core:
    def __init__(
        self,
        state: State,
        capture: Callable[[], Tuple[bool, np.ndarray]]
    ) -> None:
        self.state = state
        self.capture = capture

    def __set(self) -> None:
        self.detect_person_thread = DetectPersonThread(
            self.state, self.capture)

        self.crop_image_thread = CropImageThread(self.state, self.capture)

        self.mask_status_pool: Deque[Face] = deque()
        self.mask_status_pool_manager = ManageMaskStatusQueueThread(
            self.state, self.mask_status_pool)
        self.detect_mask_worker: List[UpdateMaskStatusThread] = []
        for _ in range(5):
            self.detect_mask_worker.append(
                UpdateMaskStatusThread(self.state, self.mask_status_pool))

        self.face_recognition_pool: Deque[Face] = deque()
        self.face_recognition_pool_manager = ManageNameQueueThread(
            self.state, self.face_recognition_pool)
        self.face_recognition_worker: List[UpdateNameThread] = []
        for _ in range(5):
            self.face_recognition_worker.append(
                UpdateNameThread(self.state, self.face_recognition_pool))

    def start(self) -> None:
        if self.state.is_core_running:
            return

        self.state.clear()

        self.state.is_core_running = True
        self.__set()
        self.detect_person_thread.start()
        self.crop_image_thread.start()
        self.mask_status_pool_manager.start()
        for thread in self.detect_mask_worker:
            thread.start()
        self.face_recognition_pool_manager.start()
        for thread in self.face_recognition_worker:
            thread.start()

    def close(self) -> None:
        if not self.state.is_core_running:
            return

        self.state.is_core_running = False

        self.detect_person_thread.terminate()

        self.crop_image_thread.terminate()

        self.mask_status_pool_manager.terminate()

        for thread in self.detect_mask_worker:
            thread.terminate()
        self.detect_mask_worker.clear()

        self.face_recognition_pool_manager.terminate()

        for thread in self.face_recognition_worker:
            thread.terminate()
        self.face_recognition_worker.clear()

        self.state.clear()


class DetectPersonThread(StoppableThread):
    def __init__(self,
                 state: State,
                 capture: Callable[[], Tuple[bool, np.ndarray]]):
        super().__init__()
        self.state = state
        self.capture = capture

    def run(self):
        while not self.stopped():
            _, img = self.capture()
            if img is None or img.size == 0:
                self._stop_event.wait(0.1)
                continue
            try:
                people_detector = PeopleDetector(AmazonImage.from_ndarray(img))
                self.state.people = people_detector.run()
            except Exception as error:
                print(error)

            self._stop_event.wait(0.1)


class CropImageThread(StoppableThread):
    def __init__(self,
                 state: State,
                 capture: Callable[[], Tuple[bool, np.ndarray]]):
        super().__init__()
        self.state = state
        self.face_manager = FaceManager()
        self.capture = capture
        self.__count = 0

    def run(self):
        while not self.stopped():
            _, img = self.capture()
            if img is None or img.size == 0:
                self._stop_event.wait(0.1)
                continue
            self.__count += 1
            try:
                cropped_img_infos = self.face_manager.crop_image(
                    AmazonImage.from_ndarray(img))
            except:
                cropped_img_infos = None

            if not cropped_img_infos:
                # TODO: 사진에 얼굴 검출 결과가 없을 때
                self._stop_event.wait(0.1)
                continue

            for info in cropped_img_infos:
                img = info[0]
                width, height = img.shape[1], img.shape[0]
                left, top = info[1], info[2]
                right, bottom = left + width, top + height
                box = Box(left, right, top, bottom, self.__count)

                is_exist = False
                for face in self.state.faces:
                    if face.frame == self.__count:
                        continue

                    if not face.compare(box):
                        continue

                    face.update(box, img)
                    is_exist = True
                    break

                if not is_exist:
                    self.state.faces.append(Face(box, img))

            faces = [face for face in self.state.faces]
            for i, face in enumerate(faces):
                if face.frame == self.__count:
                    continue

                del self.state.faces[i]

            self._stop_event.wait(0.1)


class ManageMaskStatusQueueThread(StoppableThread):
    def __init__(self,
                 state: State,
                 mask_status_queue: Deque[Face]):
        super().__init__()
        self.order_dict = {
            MaskStatus.UNKNOWN: 1,
            MaskStatus.NOT_WEARED: 2,
            MaskStatus.WEARED: 3,
        }
        self.state = state
        self.mask_status_queue = mask_status_queue

    def run(self):
        while not self.stopped():
            if len(self.mask_status_queue) > 2:
                self._stop_event.wait(0.1)
                continue

            if not self.state.faces:
                self._stop_event.wait(0.1)
                continue

            faces = [face for face in self.state.faces]
            faces.sort(key=lambda face: self.order_dict[face.mask_status])

            for face in faces:
                self.mask_status_queue.append(face)


class UpdateMaskStatusThread(StoppableThread):
    def __init__(self,
                 state: State,
                 mask_status_queue: Deque[Face]):
        super().__init__()
        self.state = state
        self.mask_status_queue = mask_status_queue

    def run(self):
        while not self.stopped():
            if not self.mask_status_queue:
                self._stop_event.wait(0.1)
                continue

            face = self.mask_status_queue.popleft()

            mask_detector = MaskDetector(
                AmazonImage.from_ndarray(face.img))
            try:
                people = mask_detector.run()
            except:
                people = None

            if not people:
                self._stop_event.wait(0.1)
                continue

            person = people[0]
            self.state.set_mask_status(face.id, person.mask_status)


class ManageNameQueueThread(StoppableThread):
    def __init__(self,
                 state: State,
                 name_queue: Deque[Face]):
        super().__init__()
        self.state = state
        self.name_queue = name_queue

    def run(self):
        while not self.stopped():
            if len(self.name_queue) > 2:
                self._stop_event.wait(0.1)
                continue

            if not self.state.faces:
                self._stop_event.wait(0.1)
                continue

            faces = [face for face in self.state.faces]
            faces.sort(key=lambda face: 1 if not face.name else 2)

            for face in faces:
                self.name_queue.append(face)


class UpdateNameThread(StoppableThread):
    def __init__(self,
                 state: State,
                 name_queue: Deque[Face]):
        super().__init__()
        self.state = state
        self.name_queue = name_queue
        self.face_manager = FaceManager()
        self.db = UserDatabase()

    def run(self):
        while not self.stopped():
            if not self.name_queue:
                self._stop_event.wait(0.1)
                continue

            face = self.name_queue.popleft()

            image = AmazonImage.from_ndarray(face.img)
            try:
                face_match = self.face_manager.search_only_one_face(image)
            except:
                face_match = None

            user_id: str
            if not face_match:
                try:
                    user_id, _ = self.face_manager.add_face(
                        image=image, check_face_exist=False)
                except:
                    self._stop_event.wait(0.1)
                    continue
            else:
                user_id = face_match.face.external_image_id

            try:
                name = self.db.read(user_id).name
            except:
                name = None

            self.state.set_face_info(face.id, user_id, name)
