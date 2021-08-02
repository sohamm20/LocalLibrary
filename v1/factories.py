import factory
from faker import Factory
from catalog.models import (
    Book, 
    Genre,
    Author,
    Language,
    BookInstance,
)

faker=Factory.create()
class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre
    
    name = "Adventure"

class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Language

    name = faker.name()

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = faker.text(max_nb_chars=100, ext_word_list=['Best', 'book', 'Adventure'])
    summary = faker.paragraph(nb_sentences=4)
    isbm = faker.isbn13()
   

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = faker.first_name()
    last_name = faker.last_name()
    
class BookInstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookInstance

    id = faker.uuid4()
    imprint = faker.text(max_nb_chars=80)
    due_back = faker.date()
    status = faker.random_element(elements=('m', 'o', 'a', 'r'))

