import dlib
from skimage import io
from pathlib import Path
import time
import cv2
from imutils import face_utils
from .siamese.face_recognition import FaceRecognition
from .siamese.face_detection_dlib import FaceDetectorDlib

BASE_DIR = Path(__file__).resolve().parent
predictor = dlib.shape_predictor(str(BASE_DIR) + '\models\shape_predictor_5_face_landmarks.dat')


def siameseFaceRecog(img, name, path):
    start_time = time.time()
    # Клас для розпізнання обличчя
    face_recognizer = FaceRecognition(
        model_loc=str(BASE_DIR) + "/models",
        persistent_data_loc=str(BASE_DIR) + "/data/facial_data.json",
        face_detector="dlib",
    )
    # Зчитання зображення
    image = io.imread(img)
    # Створення об'єкту для знаходження обличь
    face_detector = FaceDetectorDlib(model_type="hog")
    # Знаходження обличь
    bboxes = face_detector.detect_faces(image)
    # Перевірка, чи були знайдені обличчя
    if bboxes:
        # Зареєструвати обличчя у локальній БД
        face_recognizer.register_face(image=image, name=name)
        # Розпізнати обличчя за зареєстрованний шаблоном
        result = face_recognizer.recognize_faces(image)
        dets = [result[0][0]]
        face_desc = result[0][1]['encoding']
        for i, det in enumerate(dets):
            # Перетворення координат знайденного обличчя до
            # об'єкту Rectangle для подальшої обробки
            rectangle = dlib.rectangle(det[0], det[1], det[2], det[3])
            # Знайти ознаки обличчя
            shape = predictor(image, rectangle)
            shape2 = face_utils.shape_to_np(shape)
            # Привести об'єкт Dlib до вигляду OpenCV-style bounding box
            (x, y, w, h) = face_utils.rect_to_bb(rectangle)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Додання напису номера обличчя
            cv2.putText(image, "Face #{}".format(i + 1), (x + 30, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # Цикл для проходження по координатам ознак для того,
            # щоб намалювати їх
            for (x, y) in shape2:
                cv2.circle(image, (x, y), 1, (0, 0, 255), 2)
    else:
        return {'path': path, 'facedesc': None, 'faces': len(bboxes),
                'time': float("{:.4f}".format(time.time() - start_time))}
    # Збереження зображення із намальованними ознаками та дескриптором
    dlib.save_image(image, str(BASE_DIR.parent.parent) + "/static/images/" + path)
    return {'path': path, 'facedesc': face_desc, 'faces': len(bboxes),
            'time': float("{:.4f}".format(time.time() - start_time))}
