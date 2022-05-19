from pathlib import Path
import time
from .siamese.face_detection_dlib import FaceDetectorDlib
from .siamese.media_utils import load_image_path
from .siamese.face_recognition import FaceRecognition

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def siameseFace(img, path):
    start_time = time.time()
    face_detector = FaceDetectorDlib(model_type="hog")
    face_recognizer = FaceRecognition(
        model_loc="models",
        persistent_data_loc="data/facial_data.json",
        face_detector="dlib",
    )
    image = load_image_path(img)


def registerFace(img, fr, fd):
    
    # Matches is a list containing information about the matches
    # for each of the faces in the image
    matches = face_recognizer.register_face(image=img, name=name)
    result = face_recognizer.recognize_faces(image=img, threshold=0.6)
    bboxes = face_detector.detect_faces(image)


# adds a new user face to the database using his/her image stored on disk using the image path
def add_user_img_path(user_db, FRmodel, name, img_path):
    if name not in user_db:
        user_db[name] = img_to_encoding(img_path, FRmodel)
        print("Encodings:",user_db[name])
        # save the database
        with open('database/user_dict.pickle', 'wb') as handle:
                pickle.dump(user_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('User ' + name + ' added successfully')
    else:
        print('The name is already registered! Try a different name.........')