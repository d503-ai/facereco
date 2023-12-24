from pathlib import Path
import time
import keras

BASE_DIR = Path(__file__).resolve().parent
# Завантаження моделі
loaded_model = keras.models.load_model('\models\vgg_improved.keras')

def vggImpFaceRecog(img, name, path):
    start_time = time.time()

    #return {'path': path, 'facedesc': face_desc, 'faces': len(bboxes),
    #        'time': float("{:.4f}".format(time.time() - start_time))}