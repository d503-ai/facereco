from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ImageForm
from .models import Record, Neural
from scipy.spatial import distance
from .libs.libdlib import *
from .libs.libopencv import *

BASE_DIR = Path(__file__).resolve().parent.parent


def index(request):
    """
    Home page
    """
    # Delete all instances on start
    Record.objects.all().delete()
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
            # Save new instance
            form.save()
            # Redirect to view by name
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
            # Save new instance
            form.save()
            # Redirect to view by name
            return HttpResponseRedirect(reverse('result-detect'))
    else:
        form = ImageForm()

    context.update({'form': form})
    return render(request, 'main/detection.html', context)


def resultDetect(request):
    """
    Result page - Executing Neural Network of detection and showing the result
    :param request: request data
    :param data:    transferred data
    :return:        the view of page
    """
    rec = Record.objects.last()
    dlib = dlibFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                    "dlib_detector.jpg")
    opencv = OpenCVFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                        "opencv_detector.jpg")
    if dlib:
        dlib_mod = Neural(title="Dlib", record=rec, detect_image=dlib['path'], time=dlib['time'])
        dlib_mod.save()

    if opencv:
        opencv_mod = Neural(title="OpenCV", record=rec, detect_image=opencv['path'], time=opencv['time'])
        opencv_mod.save()

    rec.save()
    context = {'title': 'Result', 'data': {dlib_mod, opencv_mod}, 'obj': rec, 'faces': dlib['faces']}
    return render(request, 'main/result_detect.html', context)


def resultRecon(request):
    """
    Result page - Executing Neural Network functions and showing the result
    """
    rec = Record.objects.last()
    data1 = dlibFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                     "dlib_recon_1.jpg")
    data2 = dlibFace(str(BASE_DIR) + "/static/" + str(rec.second_image.url),
                     "dlib_recon_2.jpg")
    setattr(rec, 'first_image', data1['path'])
    setattr(rec, 'second_image', data2['path'])
    rec.save()
    a = distance.euclidean(data1['facedesc'], data2['facedesc'])
    if a > 0.6:
        pers = "Different persons"
    else:
        pers = "The same persons"
    context = {'title': 'Result', 'pers': pers, 'data': rec, 'data1': data1, 'data2': data2}
    return render(request, 'main/result_recon.html', context)


def pageNotFound(request, exception):
    """

    :param request:
    :param exception:
    :return:
    """
    return render(request, "404.html")
