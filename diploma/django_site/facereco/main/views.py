from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ImageForm
from .models import Result
from scipy.spatial import distance
from .libs.libdlib import *
from .libs.libopencv import *


BASE_DIR = Path(__file__).resolve().parent.parent


def index(request):
    """
    Home page
    """
    # Delete all instances on start
    Result.objects.all().delete()
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
    rec = Result.objects.last()
    data = dlibFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                       "dlib_detector.jpg")
    setattr(rec, 'first_image', data['path'])
    rec.save()
    context = {'title': 'Result', 'data': data, 'obj': rec}
    return render(request, 'main/result_detect.html', context)


def resultRecon(request):
    """
    Result page - Executing Neural Network functions and showing the result
    """
    rec = Result.objects.last()
    data1 = dlibFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                       "dlib_detector.jpg")
    setattr(rec, 'dlib', data1['path'])
    rec.save()
    context = {'title': 'Result', 'data': result}
    return render(request, 'main/result_recon.html', context)


def pageNotFound(request, exception):
    """

    :param request:
    :param exception:
    :return:
    """
    return render(request, "404.html")
