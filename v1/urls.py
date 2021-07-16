from django.urls import path
from . import views

urlpatterns = [
    path('genres/', views.GenreListAPIView.as_view(), name='genres'),
    path('books/', views.BookListAPIView.as_view(), name='books'),

]
