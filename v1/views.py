from django.http.request import QueryDict
from django.shortcuts import render
from catalog.models import (
    Genre,
    Book,
)

from rest_framework import generics
from .serializers import (
    GenreSerializer,
    BookSerializer,
)

# Create your views here.


class GenreListAPIView(generics.ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

class BookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

