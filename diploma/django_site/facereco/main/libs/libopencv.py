from pathlib import Path
import cv2
import time
import face_recognition

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def openCVFace(img, path):
    start_time = time.time()
    image = face_recognition.load_image_file(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Знаходження обличь на зображені
    faces = face_recognition.face_locations(image)
    # Визначення дескриптору обличчя
    encodings = face_recognition.face_encodings(image)

    if faces:
        for i, face in enumerate(faces):
            cv2.rectangle(image, (face[3], face[0]), (face[1], face[2]), (255, 0, 0), 2)
            cv2.putText(image, "Face #{}".format(i + 1), (face[3] + 30, face[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imwrite(str(BASE_DIR) + "/static/images/" + path, image)
        return {'path': path, 'facedesc': encodings, 'faces': len(faces),
                'time': float("{:.4f}".format(time.time() - start_time))}
    else:
        return {'path': path, 'facedesc': None, 'faces': len(faces),
                'time': float("{:.4f}".format(time.time() - start_time))}


# New function to detect faces without drawing rectangles and labels
def detectFaces(img):
    image = face_recognition.load_image_file(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Знаходження обличь на зображені
    faces = face_recognition.face_locations(image)

    return faces


def cropFaces(record_id, img, faces, path, expansion_factor=1.5):
    image = face_recognition.load_image_file(img)
    cropped_faces = []

    fixed_size = (200, 200)  # Set the desired fixed size for the cropped faces

    for i, (top, right, bottom, left) in enumerate(faces):
        # Calculate the expanded bounding box
        expanded_top = max(0, int(top - (bottom - top) * (expansion_factor - 1) / 2))
        expanded_bottom = min(image.shape[0], int(bottom + (bottom - top) * (expansion_factor - 1) / 2))
        expanded_left = max(0, int(left - (right - left) * (expansion_factor - 1) / 2))
        expanded_right = min(image.shape[1], int(right + (right - left) * (expansion_factor - 1) / 2))

        # Crop the face region with expanded bounding box
        face_image = image[expanded_top:expanded_bottom, expanded_left:expanded_right]

        if not face_image.size == 0:  # Check if the face is not empty
            # Resize the face image to the fixed size
            resized_face = cv2.resize(face_image, fixed_size)

            # Save the resized face image
            cv2.imwrite(
                str(BASE_DIR) + f"/static/images/cropped_face_{record_id}_{i}_{path}",
                cv2.cvtColor(resized_face, cv2.COLOR_RGB2BGR),
            )
            cropped_faces.append(f"cropped_face_{record_id}_{i}_{path}")

    return cropped_faces
