import dlib
from skimage import io
from pathlib import Path
import time
import cv2
from imutils import face_utils
from facereco.main.libs.siamese.face_recognition import FaceRecognition

BASE_DIR = Path(__file__).resolve().parent
predictor = dlib.shape_predictor(str(BASE_DIR) + '\models\shape_predictor_5_face_landmarks.dat')


def siameseFace(img, name, path):
    start_time = time.time()
    face_recognizer = FaceRecognition(
        model_loc="models",
        persistent_data_loc="data/facial_data.json",
        face_detector="dlib",
    )
    image = io.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_recognizer.register_face(image=image, name=name)
    result = face_recognizer.recognize_faces(image)
    dets = result[0][0]
    face_desc = result[0][1]['encoding']
    if dets:
        for i, det in enumerate(dets):
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, det)
            shape2 = face_utils.shape_to_np(shape)
            # convert dlib's rectangle to a OpenCV-style bounding box
            # [i.e., (x, y, w, h)], then draw the face bounding box
            (x, y, w, h) = face_utils.rect_to_bb(det)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # show the face number
            cv2.putText(img, "Face #{}".format(i + 1), (x + 30, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # loop over the (x, y)-coordinates for the facial landmarks
            # and draw them on the image
            for (x, y) in shape2:
                cv2.circle(img, (x, y), 1, (0, 0, 255), 2)
    else:
        return {'path': path, 'facedesc': None, 'faces': len(dets),
                'time': float("{:.4f}".format(time.time() - start_time))}
    # show the output image with the face detections + facial landmarks
    cv2.imwrite(img, str(BASE_DIR).parent.parent + "/static/images/" + path)
    return {'path': path, 'facedesc': face_desc, 'faces': len(dets),
            'time': float("{:.4f}".format(time.time() - start_time))}
