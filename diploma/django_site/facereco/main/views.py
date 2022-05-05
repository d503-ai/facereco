from django.shortcuts import render, redirect


def index(request):
    context = {'title': 'Home'}
    return render(request, 'main/index.html', context)


def result(request):
    context = {'title': 'Result'}
    return render(request, 'main/result.html', context)