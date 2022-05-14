import django

django.setup()

from django.test import TestCase
from .models import Record
from .libs.libdlib import dlibFace


class ImageTestCase(TestCase):
    def recognizeFaces(self):
        """
        Check if result is correct (0 faces of >1 faces)
        :return:
        """
        image1 = Record.object.create(first_image='/test/plane.jpg')
        image2 = Record.object.create(first_image='/test/faces.jpg')

        result = dlibFace(image1)
        self.assertEqual(result, {})
