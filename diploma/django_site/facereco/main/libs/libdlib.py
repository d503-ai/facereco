"""
a = distance.euclidean(face_descriptor1, face_descriptor2)

dets = detector(img, 1)
for k, d in enumerate(dets):
    print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        k, d.left(), d.top(), d.right(), d.bottom()))


res1 = dlib_reco("test1.jpg", "output.jpg")
res2 = dlib_reco("test1.jpg", "output2.jpg")

a = distance.euclidean(res1['facedesc'], res2['facedesc'])

if a > 0.6:
    print("Different persons")
else:
    print("The same persons")
"""


from pathlib import Path
import dlib
import cv2
from skimage import io
from imutils import face_utils

BASE_DIR = Path(__file__).resolve().parent.parent.parent

predictor = dlib.shape_predictor(str(BASE_DIR) + '\static\data\shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1(str(BASE_DIR) + '\static\data\dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()


def dlibFace(image, path):
    """
    Recognition and face detection Dlib's func
    :param image:   relative path to image
    :param path:    ex. "../../static/images/dlib_detect.jpg"
    :return:        path to new image & facedescr
    """
    img = io.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dets = detector(gray, 1)
    for (i, det) in enumerate(dets):
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, det)
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        shape = face_utils.shape_to_np(shape)
        # convert dlib's rectangle to a OpenCV-style bounding box
        # [i.e., (x, y, w, h)], then draw the face bounding box
        (x, y, w, h) = face_utils.rect_to_bb(det)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # show the face number
        cv2.putText(img, "Face #{}".format(i + 1), (x + 30, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        for (x, y) in shape:
            cv2.circle(img, (x, y), 1, (0, 0, 255), 2)
    # show the output image with the face detections + facial landmarks
    dlib.save_image(img, str(BASE_DIR) + "/static/images/" + path)
    return {'path': path, 'facedesc': face_descriptor, 'faces': len(dets)}
