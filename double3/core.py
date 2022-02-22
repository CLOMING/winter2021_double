from collections import deque
from multiprocessing import Process
from time import sleep
from typing import Callable, Deque, Tuple
import numpy as np

from state import Box, Face, State
from winter2021_recognition.amazon_rekognition import AmazonImage, FaceManager, FaceManagerExceptionFaceNotExistException, FaceManagerExceptionFaceNotSearchedException, MaskDetector, MaskStatus, PeopleDetector, UserDatabase


class Core:
    def __init__(
        self,
        state: State,
        capture: Callable[[], Tuple[bool, np.ndarray]]
    ) -> None:
        self.state = state
        self.capture = capture
        self.face_manager = FaceManager()
        self.db = UserDatabase()

    def __set(self) -> None:
        self.detect_person_process = Process(target=self.__detect_person)

        self.crop_image_process = Process(target=self.__crop_image)
        self.__crop_image_count = 0

        self.mask_status_queue: Deque[Face] = deque()
        self.detect_mask_process = Process(target=self.__update_mask_status)
        self.manage_mask_status_queue_process = Process(
            target=self.__manage_mask_status_queue)

        self.name_queue: Deque[Face] = deque()
        self.search_face_process = Process(target=self.__update_name)
        self.manage_name_queue_process = Process(
            target=self.__manage_name_queue)

    def start(self) -> None:
        if self.state.is_core_running:
            return

        self.state.is_core_running = True
        self.__set()
        self.detect_person_process.start()
        self.crop_image_process.start()
        self.manage_mask_status_queue_process.start()
        self.detect_mask_process.start()
        self.manage_name_queue_process.start()
        self.search_face_process.start()

    def close(self) -> None:
        if not self.state.is_core_running:
            return

        self.state.is_core_running = False
        self.detect_person_process.terminate()
        self.crop_image_process.terminate()
        self.manage_mask_status_queue_process.terminate()
        self.detect_mask_process.terminate()
        self.manage_name_queue_process.terminate()
        self.search_face_process.terminate()
        self.state.clear()

    def __detect_person(self) -> None:
        while True:
            _, img = self.capture()
            people_detector = PeopleDetector(AmazonImage.from_ndarray(img))
            self.state.people = people_detector.run()

            sleep(0.1)

    def __crop_image(self) -> None:
        while True:
            _, img = self.capture()
            self.__crop_image_count += 1
            try:
                cropped_img_infos = self.face_manager.crop_image(
                    AmazonImage.from_ndarray(img))
            except FaceManagerExceptionFaceNotExistException:
                cropped_img_infos = None

            if not cropped_img_infos:
                # TODO: 사진에 얼굴 검출 결과가 없을 때
                sleep(0.1)
                continue

            for info in cropped_img_infos:
                img = info[0]
                width, height = img.shape[1], img.shape[0]
                left, top = info[1], info[2]
                right, bottom = left + width, top + height
                box = Box(left, right, top, bottom, self.__crop_image_count)

                is_exist = False
                for face in self.state.faces:
                    if face.frame == self.__crop_image_count:
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
                if face.frame == self.__crop_image_count:
                    continue

                del self.state.faces[i]

            sleep(0.1)

    def __manage_mask_status_queue(self) -> None:
        order_dict = {
            MaskStatus.UNKNOWN: 1,
            MaskStatus.NOT_WEARED: 2,
            MaskStatus.WEARED: 3,
        }

        while True:
            if self.mask_status_queue:
                continue

            if not self.state.faces:
                continue

            faces = [face for face in self.state.faces]
            faces.sort(key=lambda face: order_dict[face.mask_status])

            for face in faces:
                self.mask_status_queue.append(face)

    def __update_mask_status(self) -> None:
        while True:
            if not self.mask_status_queue:
                sleep(0.1)
                continue

            face = self.mask_status_queue.popleft()

            def runner(face: Face):
                mask_detector = MaskDetector(
                    AmazonImage.from_ndarray(face.img))
                people = mask_detector.run()

                if not people:
                    return

                person = people[0]
                self.state.set_mask_status(face.id, person.mask_status)

            process = Process(target=runner, args=(face,))
            process.start()

            sleep(0.1)

    def __manage_name_queue(self) -> None:
        while True:
            if self.name_queue:
                continue

            if not self.state.faces:
                continue

            faces = [face for face in self.state.faces]
            faces.sort(key=lambda face: 1 if not face.name else 2)

            for face in faces:
                self.name_queue.append(face)

    def __update_name(self) -> None:
        while True:
            if not self.name_queue:
                sleep(0.1)
                continue

            face = self.name_queue.popleft()

            def runner(face: Face):
                image = AmazonImage.from_ndarray(face.img)
                try:
                    face_match = self.face_manager.search_only_one_face(image)
                except FaceManagerExceptionFaceNotSearchedException:
                    face_match = None

                user_id: str
                if not face_match:
                    try:
                        user_id, _ = self.face_manager.add_face(
                            image=image, check_face_exist=False)
                    except:
                        return
                else:
                    user_id = face_match.face.external_image_id

                name = self.db.read(user_id).name

                self.state.set_face_info(face.id, user_id, name)

            process = Process(target=runner, args=(face,))
            process.start()

            sleep(0.1)
