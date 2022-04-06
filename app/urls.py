# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path
from app import views

urlpatterns = [
         path('<str:group_name>/', views.index, name='index'),
]