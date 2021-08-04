import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catalog.models import (
    BookInstance,
    Genre,
)
from v1.serializers import (
    GenreSerializer,
)
from v1.factories import (
    GenreFactory,
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





