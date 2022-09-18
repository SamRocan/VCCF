from django.urls import path
from . import views
from .views import ChartData

urlpatterns = [
    path('', views.index, name="index"),
    path('product/', views.product, name="product"),
    path('product/<slug:productSlug>/', views.productHome, name="productHome"),
    path('graphs/', ChartData.as_view(), name="ChartDate")
]