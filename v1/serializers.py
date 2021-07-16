from rest_framework import serializers
from catalog.models import (
    Genre,
    Book,
    Author,
    BookInstance,
)


class GenreSerializer(serializers.ModelSerializer):
    """Check difference between serializers.ModelSerializers & serializers.Serializers 
    """
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ( 'id','title')

class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author
        fields = '__all__'

class BookInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookInstance
        fields = '__all__'