"""
from pathlib import Path

from scipy.spatial import distance

from facereco.main.libs.libdlib import dlibFace
from facereco.main.libs.libopencv import openCVFace

BASE_DIR = Path(__file__).resolve().parent.parent.parent


data1 = dlibFace(str(BASE_DIR) + "/static/images/test.jpg",
                 "dlib_recon_1.jpg")

data2 = dlibFace(str(BASE_DIR) + "/static/images/test.jpg",
                 "dlib_recon_2.jpg")


print(data1)

a = distance.euclidean(data1['facedesc'], data2['facedesc'])

print(a)
"""


# Выбор готовых обученных сетей для использования
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()

# Загрузка первого фото
img = io.imread('test.jpg')

# Отображение фото
win1 = dlib.image_window()
win1.clear_overlay()
win1.set_image(img)

# Нахождение лица на фото
dets = detector(img, 1)
for k, d in enumerate(dets):
    print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        k, d.left(), d.top(), d.right(), d.bottom()))
    shape = sp(img, d)
    win1.clear_overlay()
    win1.add_overlay(d)
    win1.add_overlay(shape)

# Выбор дескриптора (векторы признаков) с лица на фото
face_descriptor1 = facerec.compute_face_descriptor(img, shape)

# Вывод дескриптора
print(face_descriptor1)

# Загрузка второго фото
img = io.imread('photo_2.jpg')
win2 = dlib.image_window()
win2.clear_overlay()
win2.set_image(img)
dets_webcam = detector(img, 1)
for k, d in enumerate(dets_webcam):
    print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        k, d.left(), d.top(), d.right(), d.bottom()))
    shape = sp(img, d)
    win2.clear_overlay()
    win2.add_overlay(d)
    win2.add_overlay(shape)

# Берём дескриптор
face_descriptor2 = facerec.compute_face_descriptor(img, shape)

# Вычисление евклидового расстояния
a = distance.euclidean(face_descriptor1, face_descriptor2)
print(a)

input()