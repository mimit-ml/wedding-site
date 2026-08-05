from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from rsvp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('stats/', views.stats, name='stats'),  # ← Добавляем статистику
    path('stats/delete/<int:pk>/', views.delete_response, name='delete_response'),
]

if settings.DEBUG:
    # runserver wires this up automatically; gunicorn doesn't, so /static/ 404s under it without this.
    urlpatterns += staticfiles_urlpatterns()