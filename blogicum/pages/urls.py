from django.views.generic import TemplateView
from django.urls import path


app_name = 'pages'

urlpatterns = [
    path(
        'about/',
        TemplateView.as_view(template_name='pages/about.html'),
        name='about'
    ),
    path(
        'rules/',
        TemplateView.as_view(template_name='pages/rules.html'),
        name='rules'
    ),
    path(
        'csrf_failure/',
        TemplateView.as_view(template_name='pages/csrf_failure.html'),
        name='csrf_failure',
    ),
]
