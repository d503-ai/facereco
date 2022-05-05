from django.shortcuts import render
from .forms import ImageForm


def index(request):
    context = {'title': 'Facereco - Home'}
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            context.update({'form': form, 'img_obj': img_obj})
            return render(request, 'main/index.html', context)
    else:
        form = ImageForm()

    context.update({'form': form, 'img_obj': None})
    return render(request, 'main/index.html', context)


def result(request):
    context = {'title': 'Facereco - Result'}
    return render(request, 'main/result.html', context)