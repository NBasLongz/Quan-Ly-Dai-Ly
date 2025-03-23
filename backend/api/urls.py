from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'quan', views.QuanViewSet)
router.register(r'loaidaily', views.LoaiDaiLyViewSet)
router.register(r'daily', views.DaiLyViewSet)
router.register(r'quydinh', views.QuyDinhViewSet)

urlpatterns = router.urls