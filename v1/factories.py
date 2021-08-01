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