from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ImageForm
from .models import Record, Neural
from scipy.spatial import distance
from .libs.libdlib import *
from .libs.libopencv import *

BASE_DIR = Path(__file__).resolve().parent.parent


# Allow upload only
# Allowed extensions are: png, apng, bmp, tif, tiff, jfif, jpe, jpg, jpeg

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
    context = {'title': 'Result'}

    rec = Record.objects.last()
    dlib = dlibFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                    "dlib_detector.jpg")
    opencv = openCVFace(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                        "opencv_detector.jpg")
    if dlib and opencv:
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

        context.update({'data': {dlib_mod, opencv_mod}, 'obj': rec})

    rec.save()
    return render(request, 'main/result_detect.html', context)


def resultRecon(request):
    """
    Result page - Executing Neural Network for recognition of faces
    :param request: request data
    :param data:    transferred data
    :return:        the view of page
    """
    context = {'title': 'Result'}
    rec = Record.objects.last()
    dlib = reconExec(rec, "Dlib")
    opencv = reconExec(rec, "OpenCV")

    if dlib and opencv:
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

        context.update({'data': {dlib_mod, opencv_mod}, 'obj': rec})

    return render(request, 'main/result_recon.html', context)


def reconExec(rec, mode):
    """
    Method for recognition of faces
    :param rec:
    :param mode:
    :return:
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
        return {}
    if data1 and data2:
        try:
            a = distance.euclidean(data1['facedesc'], data2['facedesc'])
        except:
            return data1, data2, 0.0, float("{:.4f}".format(time.time() - start_time))

    return data1, data2, a, float("{:.4f}".format(time.time() - start_time))
