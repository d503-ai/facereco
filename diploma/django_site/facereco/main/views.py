import os
import time
from pathlib import Path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ImageForm
from .models import Record, Neural
from scipy.spatial import distance
from .libs.libdlib import dlibFace
from .libs.libopencv import openCVFace
from .libs.libsiamese import siameseFaceRecog, siameseFaceDetect

# Адреса каталогу
BASE_DIR = Path(__file__).resolve().parent.parent


# Allow upload only
# Allowed extensions are: png, apng, bmp, tif, tiff, jfif, jpe, jpg, jpeg

def index(request):
    """
    Home page
    """
    # Видатили усі записи на початку роботи додатку
    Record.objects.all().delete()
    if os.path.exists(str(BASE_DIR) + "/main/libs/data/facial_data.json"):
        os.remove(str(BASE_DIR) + "/main/libs/data/facial_data.json")
    context = {'title': 'Facereco'}
    return render(request, 'main/index.html', context)


def recognize(request):
    """
    Recognition page
    """
    context = {'title': 'Recognition'}
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Зберегти запис
            form.save()
            # Перенаправити до сторінки із результатом
            return HttpResponseRedirect(reverse('result-recon'))
    else:
        form = ImageForm()

    context.update({'form': form})
    return render(request, 'main/recognition.html', context)


def detection(request):
    """
    Detection page
    """
    context = {'title': 'Detection'}
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Зберегти запис
            form.save()
            # Перенаправити до сторінки із результатом
            return HttpResponseRedirect(reverse('result-detect'))
    else:
        form = ImageForm()

    context.update({'form': form})
    return render(request, 'main/detection.html', context)


def resultDetect(request):
    """
    Result page - Виконання знаходження обличь та відображення результату
    :param request: request data
    :return:        Сторінка рузультат
    """
    context = {'title': 'Result'}
    # Отримання останнього запису у БД
    rec = Record.objects.last()
    # Виконання знаходження обличь
    dlib = dlibFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                    "dlib_detector.jpg")
    opencv = openCVFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                        "opencv_detector.jpg")
    snn = siameseFaceDetect(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                      "snn_detector.jpg")
    # Якщо обличчя знайдені успішно, то створення записів для класів нейронних мереж (Neural)
    if dlib and opencv and snn:
        dlib_mod = Neural(title="Dlib",
                          record=rec,
                          detect_image=dlib['path'],
                          time=dlib['time'],
                          faces=dlib['faces'])
        dlib_mod.save()
        opencv_mod = Neural(title="OpenCV",
                            record=rec,
                            detect_image=opencv['path'],
                            time=opencv['time'],
                            faces=opencv['faces'])
        opencv_mod.save()
        snn_mod = Neural(title="SNN",
                         record=rec,
                         detect_image=snn['path'],
                         time=snn['time'],
                         faces=snn['faces'])
        snn_mod.save()

        context.update({'data': {dlib_mod, opencv_mod, snn_mod}, 'obj': rec})

    rec.save()
    return render(request, 'main/result_detect.html', context)


def resultRecon(request):
    """
    Result page - Виконання розпізнання обличчя та відображення результату
    :param request: request data
    :return:        Сторінка рузультат
    """
    context = {'title': 'Result'}
    # Отримання останнього запису у БД
    rec = Record.objects.last()
    # Виконання розпізнання обличчя
    dlib = reconExec(rec, "Dlib")
    opencv = reconExec(rec, "OpenCV")
    snn = reconExec(rec, "SNN")
    # Якщо обличчя були знайдені та розпізнанні
    if dlib and opencv and snn:
        dlib_mod = Neural.objects.create(title="Dlib",
                                         record=rec,
                                         recognition_image_1=dlib[0]['path'],
                                         recognition_image_2=dlib[1]['path'],
                                         accuracy=dlib[2],
                                         time=dlib[3],
                                         faces=dlib[0]['faces'])
        dlib_mod.save()
        opencv_mod = Neural.objects.create(title="OpenCV",
                                           record=rec,
                                           recognition_image_1=opencv[0]['path'],
                                           recognition_image_2=opencv[1]['path'],
                                           accuracy=opencv[2],
                                           time=opencv[3],
                                           faces=opencv[0]['faces'])
        opencv_mod.save()
        snn_mod = Neural.objects.create(title="SNN",
                                        record=rec,
                                        recognition_image_1=snn[0]['path'],
                                        recognition_image_2=snn[1]['path'],
                                        accuracy=snn[2],
                                        time=snn[3],
                                        faces=snn[0]['faces'])
        snn_mod.save()

        context.update({'data': {dlib_mod, opencv_mod, snn_mod}, 'obj': rec})

    return render(request, 'main/result_recon.html', context)


def reconExec(rec, mode):
    """
    Метод для розпізнання обличчя та розрахунку евклидової відстані
    :param rec:     запис Record
    :param mode:    бібліотека до виконання
    :return:        розпізнанне обличчя
    """
    start_time = time.time()
    if mode == "Dlib":
        data1 = dlibFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                         "dlib_recon_1.jpg")
        data2 = dlibFace(str(BASE_DIR) + "/static/" + str(rec.second_image.url),
                         "dlib_recon_2.jpg")
    elif mode == "OpenCV":
        data1 = openCVFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                           "opencv_recon_1.jpg")
        data2 = openCVFace(str(BASE_DIR) + "/static/" + str(rec.second_image.url),
                           "opencv_recon_2.jpg")
    else:
        data1 = siameseFaceRecog(str(BASE_DIR) + "/static/" + str(rec.first_image.url), "snn_01",
                           "snn_recon_1.jpg")
        data2 = siameseFaceRecog(str(BASE_DIR) + "/static/" + str(rec.second_image.url), "snn_02",
                           "snn_recon_2.jpg")
    if data1 and data2:
        # Розрахунок евклидової відстані (точність)
        try:
            a = distance.euclidean(data1['facedesc'], data2['facedesc'])
        except:
            return data1, data2, 0.0, float("{:.4f}".format(time.time() - start_time))

    return data1, data2, a, float("{:.4f}".format(time.time() - start_time))
