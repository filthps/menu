from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name="main.html")),
    path('test-path', TemplateView.as_view(template_name="main.html")),
    path('test-path2', TemplateView.as_view(template_name="main.html")),
]
