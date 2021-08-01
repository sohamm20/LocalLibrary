from django.test import TestCase
from catalog.models import (
    Genre,
    Book,
    Author,
    Language,
    BookInstance
)
from django.urls import reverse
from v1.factories import (
    BookFactory,
    GenreFactory,
    LanguageFactory,
)
import ipdb

class ModelsTestCases(TestCase):
    def setUp(self):
        self.genre = GenreFactory()
        self.author = Author.objects.create(
            first_name="Tasha",
            last_name="testDaije"
        )
        self.language = LanguageFactory()
        self.book = BookFactory()

    def test_can_create_genre_model(self):
        self.assertEqual(self.genre.__str__(), self.genre.name)

    def test_can_create_language(self):
        self.assertEqual(self.language.__str__(), self.language.name)
    
    def test_can_create_book(self):
        book = Book.objects.create(
            author=self.author,
            Language=self.language,
        )
        book.genre.add(self.genre)
        number_of_books = Book.objects.all().count()

        self.assertEqual(book.__str__(), book.title)
        #self.assertEqual(number_of_books,1)
        self.assertEqual(book.get_absolute_url(), f'/api/books/{book.id}')
        self.assertEqual(book.display_genre(), ', '.join(genre.name for genre in book.genre.all()))
        


    
