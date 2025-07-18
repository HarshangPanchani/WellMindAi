from django.urls import path
from . import views

urlpatterns = [
    path('', views.wellmind_home, name='wellmind_home'),
    path('analyze-mood/', views.analyze_mood, name='analyze_mood'),
] 