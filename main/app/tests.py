import requests
from django.test import TestCase

class IndexViewTest(TestCase):

    # Verifica que se pueda consumir la api, y recuperar los datos necesarios para el correcto funcionamiento de la app
    def integracion_api(self):
        url = 'https://dn8mlk7hdujby.cloudfront.net/interview/insurance/58'
        response = requests.get(url)
        api_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('insurance', api_data)
        self.assertIn('name', api_data['insurance'])
        self.assertIn('description', api_data['insurance'])
        self.assertIn('price', api_data['insurance'])
        self.assertIn('image', api_data['insurance'])