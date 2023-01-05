from django.urls import path
from . import views

urlpatterns = [
    path('s/<str:short_url_key>', views.ShortUrlRedirectView.as_view(), name='short_url_redirect'),
]
