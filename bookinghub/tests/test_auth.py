import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='testpass123'
    )

@pytest.mark.django_db
def test_register(client):
    res = client.post('/api/auth/register/', {
        'username': 'newuser',
        'email': 'new@test.com',
        'password': 'pass123456'
    })
    assert res.status_code == 201

@pytest.mark.django_db
def test_login(client, user):
    res = client.post('/api/auth/login/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert res.status_code == 200
    assert 'access' in res.data

@pytest.mark.django_db
def test_login_wrong_password(client, user):
    res = client.post('/api/auth/login/', {
        'username': 'testuser',
        'password': 'wrongpass'
    })
    assert res.status_code in [400, 401]

@pytest.mark.django_db
def test_profile_requires_auth(client):
    res = client.get('/api/auth/profile/')
    assert res.status_code == 401

@pytest.mark.django_db
def test_profile_with_auth(client, user):
    client.force_authenticate(user=user)
    res = client.get('/api/auth/profile/')
    assert res.status_code == 200
    assert res.data['email'] == 'test@test.com'