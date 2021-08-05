import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catalog.models import (
    BookInstance,
    Genre,
    Book,
)
from v1.serializers import (
    GenreSerializer,
    BookSerializer,
)
from v1.factories import (
    AuthorFactory,
    BookFactory,
    GenreFactory,
    LanguageFactory,
)
import ipdb
class GenreListTest(APITestCase):
    def setUp(self):
        self.genre = GenreFactory()
        self.valid_payload = {
            "name": "Classic"
        }
        self.invalid_payload = {
            "name": ""
        }
        self.genre = Genre.objects.create(name="Adventures")

    def test_specific_genre(self):

        expected_result = [{'id': 2, 'name': 'Adventures'}]
        res = self.client.get('/api/genres/', {'q': 'Adventures'})

        self.assertEqual(res.json(), expected_result)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_get_genre_list(self):
        response = self.client.get(reverse('genres'))
        queryset = Genre.objects.all()
        count_genres = queryset.count()
        serializer = GenreSerializer(queryset, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(count_genres,2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_genre(self):
        response = self.client.post(
            reverse('genres'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.json(), {'id': 3, 'name': 'Classic'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_genre(self):
        response = self.client.post(
            reverse('genres'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.json(), {'name': ['This field may not be blank.']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BookListTest(APITestCase):
    def setUp(self):
        #self.book = BookFactory()
        self.genre = GenreFactory()
        self.language = LanguageFactory()
        self.author = AuthorFactory()
        self.book = Book.objects.create(
            title = 'The lost boy',
            summary = 'A story about a powerful martial artist',
            isbm = '1234567890981',
            author=self.author,
            language=self.language,
        )
        self.book.genre.add(self.genre)

        self.junglebook = Book.objects.create(
            title = 'The jungle book',
            summary = 'A story about a boy in the jungle',
            isbm = '1234588888811',
            author=self.author,
            language=self.language,
        )
        self.junglebook.genre.add(self.genre)
        
        self.valid_payload = {
            'title': 'Murim book',
            'summary': 'Legend of the Northern Blade',
            'isbm': '1234567890123',
            'author': '1',
            'language': '1',
            'genre': [1]
        }
        self.invalid_payload = {
            'title': 'Murim book',
            'summary': 'Legend of the Northern Blade',
            'isbm': '',
            'author': '2',
            'language': '1',
            'genre': [1]
        }
        
    def test_get_all_books(self):
        response = self.client.get(reverse('books'))
        qs = Book.objects.all()
        books = qs.count()
        serializer = BookSerializer(qs, many=True)
        self.assertEqual(books, 2)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_create_valid_book(self):
        response = self.client.post(
            reverse('books'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.json(), {'id': 3, 'title': 'Murim book', 'summary': 'Legend of the Northern Blade', 'isbm': '1234567890123', 'author': 1, 'language': 1, 'genre': [1]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_book(self):
        response = self.client.post(
            reverse('books'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.json(), {'isbm': ['This field may not be blank.'], 'author': ['Invalid pk "2" - object does not exist.']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_book(self):
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book.pk}))
        book = Book.objects.get(pk=self.book.pk)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_update_book(self):
        response = self.client.put(
            reverse('book-detail', kwargs={'pk': self.book.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.json(), {'id': 1, 'title': 'Murim book', 'summary': 'Legend of the Northern Blade', 'isbm': '1234567890123', 'author': 1, 'language': 1, 'genre': [1]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_book(self):
        response = self.client.put(
            reverse('book-detail', kwargs={'pk': self.book.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.json(), {'isbm': ['This field may not be blank.'], 'author': ['Invalid pk "2" - object does not exist.']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_book(self):
        response = self.client.delete(
            reverse('book-detail', kwargs={'pk': self.junglebook.pk})
        )
        books = Book.objects.count()
        self.assertEqual(books, 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)