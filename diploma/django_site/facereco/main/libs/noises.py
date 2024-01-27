import io
import cv2
import numpy as np
from PIL import Image as PILImage
from wand.image import Image as WandImage


def apply_noises(img_path, noise_type, attenuate=0.5):
    with WandImage(filename=img_path) as image:
        # Накласти обранний шум noise_type на зображення image
        # Noise_type може бути 'gaussian', 'laplacian', 'poisson', 'impulse'
        image.noise(noise_type, attenuate=attenuate)

        # Convert Wand Image to PIL Image
        pil_image = PILImage.open(io.BytesIO(image.make_blob()))

        # Convert PIL Image to bytes
        with io.BytesIO() as output:
            pil_image.save(output, format='JPEG')  # Adjust the format as needed
            image_bytes = output.getvalue()

        # Convert PIL Image to NumPy array
        numpy_array = np.array(pil_image)

        cv2.imwrite(img_path, cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR))

        # Return the PIL Image
        return image_bytes
