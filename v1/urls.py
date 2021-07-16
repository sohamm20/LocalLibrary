from django.urls import path
from . import views

urlpatterns = [
    path('genres/', views.GenreListAPIView.as_view(), name='genres'),
    path('books/', views.BookListAPIView.as_view(), name='books'),
    path('authors/', views.AuthorListAPIView.as_view(), name='authors'),
    path('borrowed/', views.LoanedBooksAllListAPIView.as_view(), name='all-borrowed'),
    path('mybooks/', views.LoanedBooksByUserListAPIView.as_view(), name='my-borrowed'),
]
