from django.http.request import QueryDict
from django.shortcuts import render
from rest_framework.serializers import Serializer
from catalog.models import (
    BookInstance,
    Genre,
    Book,
    Author,
)
from catalog.forms import RenewBookForm
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    GenreSerializer,
    BookSerializer,
    AuthorSerializer,
    BookInstanceSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
class GenreListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = self.request.GET.get('q')
        
        if query is None:
            qs = Genre.objects.all()
        else:
            qs = Genre.objects.filter(name__iexact=query)

        serializer = GenreSerializer(qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class BookListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class BookDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(data=serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AuthorListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        queryset = Author.objects.all()
        serializer = AuthorSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class AuthorDetailView(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author)
        return Response(data=serializer.data)

    def put(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        author = self.get_object(pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoanedBooksAllListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = self.request.GET.get('q')
        queryset = BookInstance.objects.filter(status__iexact=query)
        serializer = BookInstanceSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        serializer = BookInstanceSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)




class LoanedBooksByUserListAPIView(generics.ListAPIView):
    serializer_class = BookInstanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return BookInstance.objects.filter(borrower=user, status__exact='o').order_by('due_back')
class BookInstanceView(APIView):
    serializer_class = BookInstanceSerializer

    def get_queryset(self):
        return BookInstance.objects.all()
