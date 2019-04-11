from rest_framework.test import APISimpleTestCase, APITestCase, APIClient, force_authenticate,APIRequestFactory
from django.urls import reverse
from rest_framework.views import status
from .models import Bonds
from .serializers import BondSerializer
import datetime
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BondListCreateAPIViewTestCase(APITestCase):
    client = APIClient()
    url = reverse("bonds")

    def setUp(self):
        self.username = "ipsum"
        self.email = "lorem@ipsum.com"
        self.password = "ipsumlorem"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

    def test_create_bond(self):
        self.client.force_login(user=self.user)
        self.bond_data = {"isin": "QWERTYU123", "currency":"GBP", "lei": "R0MUWSFPU8MPRO8K5P83", "size":100000, "maturity":datetime.datetime.now()}
        response = self.client.post(self.url, data=self.bond_data)
        self.assertEqual(response.status_code, 201)
        # test legal_name assigned from api
        # TODO: remove hardcoded data "R0MUWSFPU8MPRO8K5P83" > "BNP PARIBAS"
        response_get = self.client.get(self.url)
        response_data = json.loads(response_get.content)[0]
        self.assertEqual(response_data["legal_name"], "BNP PARIBAS")

    def test_user_bonds(self):
        self.bond = Bonds.objects.create(user=self.user, isin="QWERTYU123", lei="R0MUWSFPU8MPRO8K5P83",  legal_name="TESTBOND1", currency = "GBP", size = 100000, maturity=datetime.datetime.now())
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)) == Bonds.objects.count())

    def test_bond_object_bundle(self):
        self.bond = Bonds.objects.create(user=self.user, isin="QWERTYU123",lei="R0MUWSFPU8MPRO8K5P83", legal_name="TESTBOND1", currency = "GBP", size = 100000, maturity=datetime.datetime.now())
        response = self.client.get(self.url)
        bond_serializer_data = BondSerializer(instance=self.bond).data
        response_data = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bond_serializer_data, response_data)

    def test_bond_object_update(self):
        # HTTP PUT (NOT ALLOWED)
        response = self.client.put(self.url, {"size": "99999999"})
        self.assertEqual(response.status_code, 405)

    def test_bond_object_partial_patch(self):
        # HTTP PATCH (NOT ALLOWED)
        response = self.client.patch(self.url, {"legal_name": "new name"})
        self.assertEqual(response.status_code, 405)

    def test_bond_object_delete(self):
        # HTTP DELETE (NOT ALLOWED)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 405)

    def test_bond_object_update_authorization(self):
        """
            Penetration tests
        """
        new_user = User.objects.create_user("username", "username@user.com", "username123")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

        # HTTP PUT (NOT ALLOWED)
        response = self.client.put(self.url, {"size": "99999999"})
        self.assertEqual(response.status_code, 405)

    def test_bond_object_update_authorization(self):
        new_user = User.objects.create_user("username", "username@user.com", "username123")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

        # HTTP PATCH (NOT ALLOWED)
        response = self.client.patch(self.url, {"legal_name": "Haker"})
        self.assertEqual(response.status_code, 405)

    def test_bond_object_delete_authorization(self):
        new_user = User.objects.create_user("hacker", "haker@lulzsec.com", "digitalfortress")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        # HTTP DELETE (NOT ALLOWED
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 405)
