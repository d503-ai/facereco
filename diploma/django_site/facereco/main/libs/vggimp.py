from keras.models import load_model
from keras.preprocessing import image
from pathlib import Path
import numpy as np
import time

BASE_DIR = Path(__file__).resolve().parent

# Завантаження навченої моделі VGGImp
vggimp_model = load_model(str(BASE_DIR) + '/models/vggimp_model.keras')


def vggimp_face(image_path, output_path):
    """
    Recognition and face detection using the VGGImp model
    :param image_path: relative path to the image
    :param output_path: path to save the resulting image
    :return: dictionary containing path, facedesc, faces, and time
    """
    start_time = time.time()

    # Завантаження та попередня обробка зображення
    img = image.load_img(image_path, target_size=(50, 37), grayscale=True)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Нормалізація значень пікселів до діапазону [0, 1]

    # Розпізнавання обличчя за допомогою навченої моделі VGGImp
    predictions = vggimp_model.predict(img_array)

    # Збереження результатів та додаткової обробки

    elapsed_time = float("{:.4f}".format(time.time() - start_time))

    # Формування результуючого словника
    result_dict = {'path': output_path,
                   'facedesc': predictions.tolist(),
                   'faces': len(predictions),
                   'time': elapsed_time}

    return result_dict