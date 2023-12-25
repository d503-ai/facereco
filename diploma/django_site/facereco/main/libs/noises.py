import cv2
import numpy as np


def noise(img, noise_type, strength=0.5):
    if noise_type == 'gaussian':
        return apply_gaussian_noise(img, strength)
    elif noise_type == 'laplacian':
        return apply_laplacian_noise(img, strength)
    elif noise_type == 'poisson':
        return apply_poisson_noise(img, strength)
    elif noise_type == 'impulse':
        return apply_impulse_noise(img, strength)
    else:
        return img  # No noise applied for unknown/noise_type


def apply_gaussian_noise(img, strength):
    row, col, ch = img.shape
    mean = 0
    var = 0.1
    sigma = var ** 0.5
    gauss = strength * np.random.normal(mean, sigma, (row, col, ch))
    noisy = np.clip(img + gauss, 0, 255).astype(np.uint8)
    return noisy


def apply_laplacian_noise(img, strength):
    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    noisy = strength * np.clip(img + laplacian.astype(np.uint8), 0, 255)
    return noisy


def apply_poisson_noise(img, strength):
    vals = len(np.unique(img))
    vals = 2 ** np.ceil(np.log2(vals))
    noisy = strength * np.random.poisson(img * vals) / float(vals)
    return np.clip(noisy, 0, 255).astype(np.uint8)


def apply_impulse_noise(img, strength):
    noisy = img.copy()
    num_pixels = int(strength * img.size)
    coordinates = [np.random.randint(0, i - 1, num_pixels) for i in img.shape]
    noisy[coordinates] = 255
    return noisy
