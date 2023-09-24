from django.urls import path, include
from .views import LessonListView, ProductLessonsView, ProductStatsView

urlpatterns = [
    path('api/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('api/products/<int:product_id>/lessons/',
         ProductLessonsView.as_view(), name='product-lessons'),
    path('api/products/stats/',
         ProductStatsView.as_view(), name='product-stats'),
]
