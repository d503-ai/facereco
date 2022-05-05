# Библиотека OpenCV
import cv2
# pyplot используется для вывода изображения (фото)
import matplotlib.pyplot as plt
# Используется для обнаружения лица человека
import face_recognition as fr



# Загрузка фото
image1 = fr.load_image_file("photo_1.jpg")

# Перевод изображения в серое цветовое пространство
gray_img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

# Метод отображения
plt.imshow(gray_img, cmap='gray')

# Выбор шаблона примитивов Хаара для обнаружения лиц на фото
haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces = haar_face_cascade.detectMultiScale(gray_img)
print('Faces found: ', len(faces))

# Вывод изображения с выделенными лицами
plt.imshow(image1)
input()