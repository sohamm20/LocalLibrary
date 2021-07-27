import factory
from faker import Factory
from catalog.models import *

faker=Factory.create()


class GenreFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Genre
    
    name = "Adventure"