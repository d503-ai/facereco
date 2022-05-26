from http import HTTPStatus

import django

django.setup()

import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase


class TestUploads(TestCase):
    """
    Перевірка завантажень зображення
    """

    def generate_photo_file(self, mode='png'):
        """
        Створення зображення для завантаження
        """
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, mode)
        file.name = 'test.jpg'
        file.seek(0)
        return file

    def setUp(self):
        """
        Ініціалізація класу
        """
        super(TestUploads, self).setUp()

    def test_invalid_form(self):
        """
        Перевірка на недійсне завантаження зображення
        """
        url = reverse('recognize')
        avatar = self.generate_photo_file()
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {'image': avatar_file}
        response = self.client.post(url, data, follow=True)

        self.assertNotEquals(response.status_code, 200)
        self.assertTemplateUsed('main/recognize_result.html')

    def test_valid_form(self):
        """
        Перевірка на дійсне завантаження зображення
        """
        url = reverse('detection')
        avatar = self.generate_photo_file()
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {'image': avatar_file}
        response = self.client.post(url, data, follow=True)

        self.assertNotEquals(response.status_code, 200)
        self.assertTemplateUsed('main/detect_result.html')

    def test_incorrect_format_file(self):
        """
        Перевірка на завантаження файлу некоректного типу даних
        """
        response = self.client.post('detection/', {'first_image': 'test.gif'})
        self.assertNotEquals(response.status_code, HTTPStatus.FOUND)
