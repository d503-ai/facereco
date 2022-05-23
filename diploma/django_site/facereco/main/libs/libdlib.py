from pathlib import Path
import dlib
import time
import cv2
from skimage import io
from imutils import face_utils

BASE_DIR = Path(__file__).resolve().parent

# Навченна модель провіснику ознак обличчя
predictor = dlib.shape_predictor(str(BASE_DIR) + '\models\shape_predictor_68_face_landmarks.dat')
# Навченна модель для розпізнання обличчя
facerec = dlib.face_recognition_model_v1(str(BASE_DIR) + '\models\dlib_face_recognition_resnet_model_v1.dat')
# Модель для знаходження обличь на зображені
detector = dlib.get_frontal_face_detector()


def dlibFace(image, path):
    """
    Recognition and face detection Dlib's func
    :param image:   relative path to image
    :param path:    ex. "../../static/images/dlib_detect.jpg"
    :return:        path to new image & facedescr
    """
    start_time = time.time()
    # Читання зображення
    img = io.imread(image)
    # Перетворення його до сірих відтінків
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Знаходження усіх обличь на зображені
    dets = detector(gray, 1)
    # Якщо обличчя існують, то виконати обробку
    if dets:
        # Обробка кожного обличчя
        for i, det in enumerate(dets):
            # Знайти ознаки обличчя та перетворити їх вектор
            # координат до масиву типу NumPy
            shape = predictor(gray, det)
            shape2 = face_utils.shape_to_np(shape)
            # Привести об'єкт Dlib до вигляду OpenCV-style bounding box
            # [(x, y, w, h)] та створити рамку щодо обличчя
            (x, y, w, h) = face_utils.rect_to_bb(det)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Додання напису номера обличчя
            cv2.putText(img, "Face #{}".format(i + 1), (x + 30, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # Цикл для проходження по координатам ознак для того,
            # щоб намалювати їх
            for (x, y) in shape2:
                cv2.circle(img, (x, y), 1, (0, 0, 255), 2)
    else:
        return {'path': path, 'facedesc': None, 'faces': len(dets),
                'time': float("{:.4f}".format(time.time() - start_time))}
    # Визначення дескриптору обличчя за ознаками
    face_descriptor = facerec.compute_face_descriptor(img, shape)
    # Збереження зображення із намальованними ознаками та дескриптором
    dlib.save_image(img, str(BASE_DIR.parent.parent) + "/static/images/" + path)
    return {'path': path, 'facedesc': face_descriptor, 'faces': len(dets),
            'time': float("{:.4f}".format(time.time() - start_time))}
