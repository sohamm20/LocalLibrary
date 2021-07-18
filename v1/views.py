from django.http.request import QueryDict
from django.shortcuts import render
from catalog.models import (
    BookInstance,
    Genre,
    Book,
    Author,
)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
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

class LoanedBooksByUserListAPIView(generics.ListAPIView):
    serializer_class = BookInstanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return BookInstance.objects.filter(borrower=user, status__exact='o').order_by('due_back')
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer