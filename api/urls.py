from django.urls import path 
from . import views

urlpatterns = [
    path('mp/', views.enviarRequestAMP),
    path('render/', views.frontEndIntegration)
]