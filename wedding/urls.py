from django.contrib import admin
from django.urls import path
from rsvp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('stats/', views.stats, name='stats'),  # ← Добавляем статистику
]