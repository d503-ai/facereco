from django.shortcuts import render, redirect
from .forms import ImageForm


'''
Home page - Uploading the images
'''
def index(request):
    context = {'title': 'Facereco - Home'}
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        # setattr(form, 'title', 'title ' + str(form.objects.get('id')))
        if form.is_valid():
            form.save()
            img_obj = form.instance
            context.update({'form': form, 'img_obj': img_obj})
            return redirect('result')
    else:
        form = ImageForm()

    context.update({'form': form, 'img_obj': None})
    return render(request, 'main/index.html', context)



'''
Result page - Executing Neural Network functions and showing the result
'''
def result(request):
    context = {'title': 'Facereco - Result'}
    return render(request, 'main/result.html', context)