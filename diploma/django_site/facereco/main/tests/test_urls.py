import django
from django.shortcuts import redirect

django.setup()

from django.test import TestCase
from django.urls import reverse, resolve, NoReverseMatch
from ..views import *


class TestUrls(TestCase):
    """
    Тестування щодо URL-конфігурації сторінок.
    - Перехід до сторінок
    - Перехід до неіснуючих сторінок
    """

    def test_home_ulr_is_resolved(self):
        """
        Перевірка на URL головної сторінки
        """
        self.assertEquals(resolve(reverse('home')).func, index)

    def test_detection_ulr_is_resolved(self):
        """
        Перевірка на URL результату створення запиту на знаходження обличь
        """
        self.assertEquals(resolve(reverse('detection')).func, detection)

    def test_recognize_ulr_is_resolved(self):
        """
        Перевірка на URL результату створення запиту на розпізнання обличчя
        """
        self.assertEquals(resolve(reverse('recognize')).func, recognize)

    def test_result_recon_ulr_is_resolved(self):
        """
        Перевірка на URL результату розпізнання обличчя
        """
        self.assertEquals(resolve(reverse('result-recon')).func, resultRecon)

    def test_result_detect_ulr_is_resolved(self):
        """
        Перевірка на URL результату знаходження обличь
        """
        self.assertEquals(resolve(reverse('result-detect')).func, resultDetect)

    def test_none_existing_url_is_resolved(self):
        """
        Перевірка на неіснуючий URL
        """
        try:
            reverse('non-existing-page')
        except NoReverseMatch:
            pass

    def test_redirect_to_non_existing_page(self):
        reverse('home')
        try:
            redirect('non-existing-page')
        except NoReverseMatch:
            pass
