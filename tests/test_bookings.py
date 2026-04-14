import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from hotels.models import Hotel
from bookings.models import Booking

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='booker', email='booker@test.com', password='pass123')

@pytest.fixture
def owner(db):
    return User.objects.create_user(username='owner2', email='owner2@test.com', password='pass123', role='business_owner')

@pytest.fixture
def hotel(db, owner):
    return Hotel.objects.create(
        name='Book Hotel', city='Bishkek',
        address='Book St', price_per_night=80,
        rating=4.0, available_rooms=20,
        description='Bookable hotel', owner=owner
    )

@pytest.fixture
def booking(db, user, hotel):
    return Booking.objects.create(
        user=user, booking_type='hotel', hotel=hotel,
        check_in='2026-05-01', check_out='2026-05-05',
        guests=2, total_price=320, status='pending'
    )

@pytest.mark.django_db
def test_create_booking(client, user, hotel):
    client.force_authenticate(user=user)
    res = client.post('/api/bookings/', {
        'booking_type': 'hotel',
        'hotel': hotel.id,
        'check_in': '2026-06-01',
        'check_out': '2026-06-05',
        'guests': 2,
        'total_price': 320
    })
    assert res.status_code == 201

@pytest.mark.django_db
def test_booking_requires_auth(client, hotel):
    res = client.post('/api/bookings/', {'hotel': hotel.id})
    assert res.status_code == 401

@pytest.mark.django_db
def test_get_my_bookings(client, user, booking):
    client.force_authenticate(user=user)
    res = client.get('/api/bookings/')
    assert res.status_code == 200

@pytest.mark.django_db
def test_cancel_booking(client, user, booking):
    client.force_authenticate(user=user)
    res = client.post(f'/api/bookings/{booking.id}/cancel/')
    assert res.status_code == 200

@pytest.mark.django_db
def test_availability_check(client, hotel):
    res = client.get(f'/api/bookings/availability/?type=hotel&id={hotel.id}&check_in=2026-07-01&check_out=2026-07-05')
    assert res.status_code == 200
    assert 'available' in res.data