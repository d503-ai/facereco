from imutils import face_utils
import dlib
import cv2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

predictor = dlib.shape_predictor(str(BASE_DIR) + '\static\data\shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1(str(BASE_DIR) + '\static\data\dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()


def test():
    img = cv2.imread('test.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dets = detector(gray, 1)
    path = "../../static/images/dlib_detect.jpg"
    for (i, det) in enumerate(dets):
        shape = predictor(gray, det)
        shape = face_utils.shape_to_np(shape)
        (x, y, w, h) = face_utils.rect_to_bb(det)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, "Face #{}".format(i + 1), (x + 30, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        for (x, y) in shape:
            cv2.circle(img, (x, y), 1, (0, 0, 255), 1)
    cv2.imwrite(path, img)

result = {'path': "path"}

print(result.path)