from pathlib import Path
import cv2
import time
import face_recognition

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def OpenCVFace(img, path):
    start_time = time.time()
    image = face_recognition.load_image_file(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image)

    if faces:
        for i, face in enumerate(faces):
            cv2.rectangle(image, (face[3], face[0]), (face[1], face[2]), (255, 0, 0), 2)
            cv2.putText(image, "Face #{}".format(i + 1), (face[3] + 30, face[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        return {}

    cv2.imwrite(str(BASE_DIR) + "/static/images/" + path, image)
    return {'path': path, 'facedesc': encodings, 'faces': len(faces), 'time': time.time() - start_time}
