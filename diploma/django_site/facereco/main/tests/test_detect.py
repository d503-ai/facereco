import django
django.setup()
from django.test import TestCase
from ..libs.libdlib import dlibFace
from ..libs.libopencv import openCVFace
from ..libs.libsiamese import siameseFaceDetect


class TestDetection(TestCase):
    """
    Тестування щодо знаходження обличчя.
    - присутні декілька обличь
    - присутнє одне обличчя
    - відстуні обличчя
    """
    def test_multiple_faces(self):
        """
        Тестування на знаходження декількох обличь на зображені
        """
        img = './static/images/test_images/many_faces.jpg'

        dlib = dlibFace(img, 'dlib_output.jpg')
        opencv = openCVFace(img, 'opencv_output.jpg')
        snn = siameseFaceDetect(img, 'snn_output.jpg')

        self.assertTrue(dlib['faces'] > 1 and opencv['faces'] > 1 and snn['faces'] > 1)

    def test_one_face(self):
        """
        Тестування на знаходження одного зображення
        """
        img = './static/images/test_images/photo_1.jpg'

        dlib = dlibFace(img, 'dlib_output.jpg')
        opencv = openCVFace(img, 'opencv_output.jpg')
        snn = siameseFaceDetect(img, 'snn_output.jpg')

        self.assertTrue(dlib['faces'] > 0 and opencv['faces'] > 0 and snn['faces'] > 0)

    def test_no_faces(self):
        """
        Тестування на не знаходження обличь на зображені
        """
        img = './static/images/test_images/no_faces.jpg'

        dlib = dlibFace(img, 'dlib_output.jpg')
        opencv = openCVFace(img, 'opencv_output.jpg')
        snn = siameseFaceDetect(img, 'snn_output.jpg')

        self.assertEquals(dlib['faces'], 0)
        self.assertEquals(opencv['faces'], 0)
        self.assertEquals(snn['faces'], 0)
