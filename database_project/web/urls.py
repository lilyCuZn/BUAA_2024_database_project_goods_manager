from django.urls import path

from . import admin, views

urlpatterns = [
    #path('admin', admin.site.urls),
    path('process_frontend/', views.process_frontend),

]