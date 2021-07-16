from django.http.request import QueryDict
from django.shortcuts import render
from catalog.models import (
    BookInstance,
    Genre,
    Book,
    Author,
)

from rest_framework import generics
from .serializers import (
    GenreSerializer,
    BookSerializer,
    AuthorSerializer,
    BookInstanceSerializer,
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

class LoanedBooksAllListAPIView(generics.ListAPIView):
    serializer_class = BookInstanceSerializer
    queryset = BookInstance.objects.filter(status__exact='o')
