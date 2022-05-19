from django.shortcuts import render


def page_not_found_view(request, exception):
    """
    Error handler for 404
    """
    return render(request, '404.html', status=404)
