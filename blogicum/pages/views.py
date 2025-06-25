from django.shortcuts import render


def about(request):
    view_name = request.resolver_match.view_name
    context = {'current_view': view_name}
    return render(request, 'pages/about.html', context)


def rules(request):
    view_name = request.resolver_match.view_name
    context = {'current_view': view_name}
    return render(request, 'pages/rules.html', context)
