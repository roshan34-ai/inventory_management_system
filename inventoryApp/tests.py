from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Item
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

class ItemTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = AccessToken.for_user(self.user)

    def test_create_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        data = {'name': 'Laptop', 'description': 'A laptop', 'quantity': 10, 'price': '999.99'}
        response = self.client.post(reverse('item-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_items(self):
        Item.objects.create(name='Laptop', description='A laptop', quantity=10, price='999.99')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.get(reverse('item-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        item = Item.objects.create(name='Laptop', description='A laptop', quantity=10, price='999.99')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        data = {'name': 'Updated Laptop', 'description': 'Updated description', 'quantity': 5, 'price': '599.99'}
        response = self.client.put(reverse('item-retrieve-update-destroy', args=[item.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        item = Item.objects.create(name='Laptop', description='A laptop', quantity=10, price='999.99')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.delete(reverse('item-retrieve-update-destroy', args=[item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
