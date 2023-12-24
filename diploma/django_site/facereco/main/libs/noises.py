import os


def noisy(img, path, mode):
    img.noise(mode, attenuate=0.5)
    img.save(filename=path)