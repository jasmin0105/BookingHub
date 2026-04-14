import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from hotels.models import Hotel

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def owner(db):
    return User.objects.create_user(username='owner1', email='o1@test.com', password='pass123', role='business_owner')

@pytest.fixture
def hotel(db, owner):
    return Hotel.objects.create(
        name='Test Hotel', city='Bishkek',
        address='Test St 1', price_per_night=100,
        rating=4.5, available_rooms=10,
        description='Test hotel', owner=owner
    )

@pytest.mark.django_db
def test_get_hotels(client):
    res = client.get('/api/hotels/')
    assert res.status_code == 200

@pytest.mark.django_db
def test_get_hotel_detail(client, hotel):
    res = client.get(f'/api/hotels/{hotel.id}/')
    assert res.status_code == 200
    assert res.data['name'] == 'Test Hotel'

@pytest.mark.django_db
def test_similar_hotels(client, hotel):
    res = client.get(f'/api/hotels/{hotel.id}/similar/')
    assert res.status_code == 200

@pytest.mark.django_db
def test_create_hotel_requires_auth(client):
    res = client.post('/api/hotels/', {'name': 'New', 'city': 'Osh'})
    assert res.status_code == 401