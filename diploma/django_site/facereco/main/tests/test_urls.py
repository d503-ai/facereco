import django
from django.shortcuts import redirect

django.setup()

from django.test import TestCase
from django.urls import resolve, NoReverseMatch
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


    def test_none_existing_url_is_resolved(self):
        """
        Перевірка на неіснуючий URL
        """
        reverse('non-existing-page')

        self.assertRaises(NoReverseMatch)

    def test_redirect_to_non_existing_page(self):
        """
        Перехід з існуючої сторінки до неіснуючої
        """
        reverse('home')

        redirect('non-existing-page')

        self.assertRaises(NoReverseMatch)