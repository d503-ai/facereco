import django
django.setup()
from django.test import TestCase
from ..models import Record
from ..views import reconExec


class TestRecognize(TestCase):
    """
    Тестування щодо розпізнання обличчя.
    - обличчя відсутнє
    - обличь більш ніж 1
    - обличчя належить обидвам людинам
    - обличчя не належить обидвам людинам
    - обличчя належить обидвам людинам, із шумом 50%
    - обличчя належить обидвам людинам, із нахилом
    """

    def test_many_faces(self):
        """
        Тестування на розпізнання при декількох обличчях
        """
        img_1 = './test_images/many_faces.jpg'
        img_2 = './test_images/photo_1.jpg'

        record = Record.objects.create(title='test_01', first_image=img_1, second_image=img_2)

        dlib = reconExec(record, 'Dlib')
        opencv = reconExec(record, 'OpenCV')
        snn = reconExec(record, 'SNN')

        self.assertFalse(dlib[0]['faces'] == 1 and opencv[0]['faces'] == 1 and snn[0]['faces'] == 1)

    def test_noise_50(self):
        """
        Тестування на розпізнання обличчя із шумом 50%
        """
        img_1 = './test_images/50_noise_1.jpg'
        img_2 = './test_images/50_noise_2.jpg'

        record = Record.objects.create(title='test_02', first_image=img_1, second_image=img_2)

        dlib = reconExec(record, 'Dlib')
        opencv = reconExec(record, 'OpenCV')
        snn = reconExec(record, 'SNN')

        self.assertTrue(dlib[2] < 0.6 and opencv[2] < 0.6 and snn[2] < 0.6)

    def test_angle_face(self):
        """
        Тестування на розпізнання обличчя із нахилом
        """
        img_1 = './test_images/angled_.jpg'
        img_2 = './test_images/angled_2.jpg'

        record = Record.objects.create(title='test_03', first_image=img_1, second_image=img_2)

        dlib = reconExec(record, 'Dlib')
        opencv = reconExec(record, 'OpenCV')
        snn = reconExec(record, 'SNN')

        self.assertTrue(dlib[2] < 0.6 and opencv[2] < 0.6 and snn[2] < 0.6)

    def test_one_face_diff_persons(self):
        """
        Тестування на розпізнання обличчя для різних людей
        """
        img_1 = './test_images/egor.jpg'
        img_2 = './test_images/photo_1.jpg'

        record = Record.objects.create(title='test_04', first_image=img_1, second_image=img_2)

        dlib = reconExec(record, 'Dlib')
        opencv = reconExec(record, 'OpenCV')
        snn = reconExec(record, 'SNN')

        self.assertTrue(dlib[2] > 0.6 and opencv[2] > 0.6 and snn[2] > 0.6)

    def test_one_face_same_persons(self):
        """
        Тестування на розпізнання обличчя для однакових людей
        """
        img_1 = './test_images/photo_2.jpg'
        img_2 = './test_images/photo_1.jpg'

        record = Record.objects.create(title='test_05', first_image=img_1, second_image=img_2)

        dlib = reconExec(record, 'Dlib')
        opencv = reconExec(record, 'OpenCV')
        snn = reconExec(record, 'SNN')

        self.assertFalse(dlib[2] > 0.6 and opencv[2] > 0.6 and snn[2] > 0.6)

    def test_no_faces(self):
        """
        Тестування на розпізнання при відсутності обличь
        """
        img_1 = './test_images/no_faces.jpg'
        img_2 = './test_images/photo_1.jpg'

        record = Record.objects.create(title='test_07', first_image=img_1, second_image=img_2)

        dlib = reconExec(record, 'Dlib')
        opencv = reconExec(record, 'OpenCV')
        snn = reconExec(record, 'SNN')

        self.assertTrue(dlib[0]['faces'] == 0 and opencv[0]['faces'] == 0 and snn[0]['faces'] == 0)
