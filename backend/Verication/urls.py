from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('collecting/', views.CollectingData.as_view(), name='collecting'),
    path('check/', views.VerificationData.as_view(), name='check'),
]