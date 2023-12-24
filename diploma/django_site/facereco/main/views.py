import os
import time
from pathlib import Path
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import RecordForm
from .models import Record, Neural
from scipy.spatial import distance
from .libs.libdlib import dlibFace
from .libs.libopencv import openCVFace, detectFaces, cropFaces
from .libs.libsiamese import siameseFaceRecog, siameseFaceDetect

# Адреса каталогу
BASE_DIR = Path(__file__).resolve().parent.parent


# New views for registration, login, logout, and profile
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'registration/logout.html')


@login_required
def profile(request):
    user_recognitions = Record.objects.filter(user=request.user)
    return render(request, 'main/profile.html', {'user': request.user, 'recognitions': user_recognitions})


def login_view(request):
    if request.method == 'POST':
        # Use Django's built-in authentication to log in the user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('profile'))
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# Allow upload only
# Allowed extensions are: png, apng, bmp, tif, tiff, jfif, jpe, jpg, jpeg
def index(request):
    """
    Home page
    """
    # Видатили усі записи на початку роботи додатку
    # Record.objects.all().delete()
    # if os.path.exists(str(BASE_DIR) + "/main/libs/data/facial_data.json"):
    #    os.remove(str(BASE_DIR) + "/main/libs/data/facial_data.json")

    context = {'title': 'Facereco'}
    return render(request, 'main/index.html', context)


@user_passes_test(lambda u: u.is_authenticated, login_url='/login/')
def record_details(request, record_id):
    record = get_object_or_404(Record, id=record_id)

    # Ensure that the user can only view their own records
    if request.user != record.user:
        return HttpResponseForbidden("You don't have permission to view this record.")

    neurals = Neural.objects.filter(record=record)

    context = {'record': record, 'neurals': neurals}
    return render(request, 'main/record_details.html', context)


@login_required
def recognize(request):
    """
    Recognition page
    """
    context = {'title': 'Recognition'}

    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES)

        if form.is_valid():
            # Save the form, but set the user before saving
            record = form.save(commit=False)
            record.user = request.user  # Set the user to the currently logged-in user
            record.save()

            # Redirect to the result page
            return redirect('test', record_id=record.id)
    else:
        form = RecordForm()

    context.update({'form': form})
    return render(request, 'main/recognition.html', context)


@login_required
def resultRecon(request, record_id):
    """
    Result page - Виконання розпізнання обличчя та відображення результату
    :param request: request data
    :return:        Сторінка рузультат
    """
    context = {'title': 'Result'}
    # Отримання останнього запису у БД
    rec = get_object_or_404(Record, id=record_id)

    # Set the user to the currently logged-in user
    rec.user = request.user

    # Виконання розпізнання обличчя
    dlib = reconExec(rec, "Dlib")
    opencv = reconExec(rec, "OpenCV")
    snn = reconExec(rec, "SNN")
    vggimp = reconExec(rec, "VGGImp")
    # Якщо обличчя були знайдені та розпізнанні
    if dlib and opencv and snn and vggimp:
        # Set the user for the Neural objects
        user = request.user

        dlib_mod = Neural(
            title="Dlib",
            record=rec,
            recognition_image_1=dlib[0]['path'],
            recognition_image_2=dlib[1]['path'],
            euclidian_distance=dlib[2] + 0.15,
            time=dlib[3],
            faces=dlib[0]['faces'],
            user=user  # Set the user to the currently logged-in user
        )
        dlib_mod.save()

        opencv_mod = Neural(
            title="OpenCV",
            record=rec,
            recognition_image_1=opencv[0]['path'],
            recognition_image_2=opencv[1]['path'],
            euclidian_distance=opencv[2],
            time=opencv[3],
            faces=opencv[0]['faces'],
            user=user  # Set the user to the currently logged-in user
        )
        opencv_mod.save()

        snn_mod = Neural(
            title="SNN",
            record=rec,
            recognition_image_1=snn[0]['path'],
            recognition_image_2=snn[1]['path'],
            euclidian_distance=snn[2],
            time=snn[3],
            faces=snn[0]['faces'],
            user=user  # Set the user to the currently logged-in user
        )
        snn_mod.save()

        vggimp_mod = Neural(
            title="VGGImp",
            record=rec,
            recognition_image_1=vggimp[0]['path'],
            recognition_image_2=vggimp[1]['path'],
            euclidian_distance=vggimp[2] + 0.15,
            time=vggimp[3],
            faces=vggimp[0]['faces'],
            user=user  # Set the user to the currently logged-in user
        )
        vggimp_mod.save()

        context.update({'data': {dlib_mod, opencv_mod, snn_mod, vggimp_mod}, 'obj': rec})

    return render(request, 'main/result_recon.html', context)


@login_required
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
    elif mode == "VGGImp":
        data1 = vggImpFaceRecog(str(BASE_DIR) + "/static/" + str(rec.first_image.url),
                           "vggimp_recon_1.jpg")
        data2 = vggImpFaceRecog(str(BASE_DIR) + "/static/" + str(rec.second_image.url),
                           "vggimp_recon_2.jpg")
    else:
        data1 = siameseFaceRecog(str(BASE_DIR) + "/static/" + str(rec.first_image.url), "snn_01",
                                 "snn_recon_1.jpg")
        data2 = siameseFaceRecog(str(BASE_DIR) + "/static/" + str(rec.second_image.url), "snn_02",
                                 "snn_recon_2.jpg")
    if data1 and data2:
        # Розрахунок евклидової відстані
        try:
            if mode == "OpenCV":
                a = distance.euclidean(data1['facedesc'][0].flatten(), data2['facedesc'][0].flatten())
            else:
                a = distance.euclidean(data1['facedesc'], data2['facedesc'])
        except:
            return data1, data2, 0.0, float("{:.4f}".format(time.time() - start_time))

    return data1, data2, a, float("{:.4f}".format(time.time() - start_time))


def test(request, record_id):
    # Get the Record object based on the record_id
    record = get_object_or_404(Record, id=record_id)

    if request.method == 'POST':
        selected_first_image = request.POST.get('selected_first_image')
        selected_second_image = request.POST.get('selected_second_image')

        # Update the Record object with selected images
        record.first_image = selected_first_image
        record.second_image = selected_second_image
        record.save()

        # Redirect to the result_recon page with the updated Record ID
        return redirect('result-recon', record_id=record.id)

    # Assuming your images are in the static/images/ folder
    first_image_path = str(BASE_DIR) + "/static/" + str(record.first_image.url)
    second_image_path = str(BASE_DIR) + "/static/" + str(record.second_image.url)

    # Detect faces on the first image
    faces_first_image = detectFaces(first_image_path)

    # Crop faces from the first image
    cropped_faces_first_image = cropFaces(first_image_path, faces_first_image, record.first_image)

    # Detect faces on the second image
    faces_second_image = detectFaces(second_image_path)

    # Crop faces from the second image
    cropped_faces_second_image = cropFaces(second_image_path, faces_second_image, record.second_image)

    # Pass relevant information to the template context
    context = {
        'title': 'Test',
        'cropped_faces_first_image': cropped_faces_first_image,
        'cropped_faces_second_image': cropped_faces_second_image,
    }

    return render(request, 'main/test.html', context)
