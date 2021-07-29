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
    GenreFactory
)

class ModelsTestCases(TestCase):
    def setUp(self):
        self.genre = GenreFactory()
        self.author = Author.objects.create(
            first_name="Tasha",
            last_name="testDaije"
        )
        self.language = Language.objects.create(name="Arabic")

    def test_can_create_genre_model(self):
        self.assertEqual(self.genre.__str__(), self.genre.name)

    
    def test_can_create_book(self):
        book = Book.objects.create(
            title="testBook",
            author=self.author,
            summary="This is a testcase book for testing Book model",
            isbm="1234567890987",
            Language=self.language,
        )
        book.genre.add(self.genre)
        number_of_books = Book.objects.all().count()

        x = book.display_genre()
        #ipdb.set_trace()
        self.assertEqual(book.__str__(), book.title)
        self.assertEqual(number_of_books,1)
        self.assertEqual(book.get_absolute_url(), f'/api/books/{book.id}')
        self.assertEqual(book.display_genre(), ', '.join(genre.name for genre in book.genre.all()))
        


    
