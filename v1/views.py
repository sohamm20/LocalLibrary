from django.http.request import QueryDict
from django.shortcuts import render
from catalog.models import (
    Genre,
    Book,
    Author,
)

from rest_framework import generics
from .serializers import (
    GenreSerializer,
    BookSerializer,
    AuthorSerializer,
)

# Create your views here.


class GenreListAPIView(generics.ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

class BookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class AuthorListAPIView(generics.ListAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
