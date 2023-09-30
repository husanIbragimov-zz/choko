from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.product.models import Brand

client = APIClient()


class BrandAPITest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test', password='test', is_staff=True, is_active=True)
        self.url = 'http://127.0.0.1:8000/api/v1/brand/'
        self.data = {
            'title': 'hp'
        }

        client.login(username='test', password='test')

    def test_create_object(self):
        if client.force_login(user=self.user):
            response = self.client.post(self.url, self.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Brand.objects.count(), 1)
            self.assertEqual(Brand.objects.get().title, 'hp')

    def test_list_object(self):
        if client.force_login(user=self.user):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_object(self):
        if client.force_login(user=self.user):
            brand = Brand.objects.create(title='dell')
            edit_url = reverse(self.url, kwargs={'pk': brand.pk})
            updated_data = {
                'title': 'lenovo'
            }
            response = self.client.put(edit_url, updated_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            brand.refresh_from_db()
            self.assertEqual(brand.title, 'lenovo')

    def test_destroy_object(self):
        if client.force_login(user=self.user):
            brand = Brand.objects.create(title='acer')
            destroy_url = reverse(self.url, kwargs={'pk': brand.pk})
            response = self.client.delete(destroy_url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            print(self.user, response)
            self.assertEqual(Brand.objects.count(), 0)
