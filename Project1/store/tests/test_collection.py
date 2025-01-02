from rest_framework import status
from django.contrib.auth.models import User
from model_bakery import baker
from store.models import Collection, Product
import pytest

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.fixture
def authenticate_user(api_client):
    def force_authenticate_user(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return force_authenticate_user


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # @pytest.skip()
    # def test_if_user_is_not_admin_returns_403(self, authenticate_user ,create_collection):

    #     authenticate_user(is_staff=False)
    #     response = create_collection({'title': 'a'})
    #     assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate_user ,create_collection):

        authenticate_user(is_staff=True)
        response = create_collection({'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate_user ,create_collection):
        authenticate_user(is_staff=True)
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        # Collection.objects.create(title='a')
        collection = baker.make(Collection)
        response = api_client.get(f'/store/collections/{collection.id}/')
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id' : collection.id,
            'title' : collection.title,
            'products_count': 0
        }
        
