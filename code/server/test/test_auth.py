# tests/test_auth.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

@pytest.mark.django_db
def test_login_with_valid_credentials():
    # Create a test user
    user = CustomUser.objects.create_user(
        email="testuser@example.com",
        password="TestPassword123"
    )
    
    # Use APIClient to simulate a POST request to login
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {
        'email': 'testuser@example.com',
        'password': 'TestPassword123'
    })

    # Assert response status and check if token is issued
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data  # Check if the token is in the response

@pytest.mark.django_db
def test_login_with_invalid_credentials():
    # Use APIClient to simulate a POST request to login with invalid credentials
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {
        'email': 'wronguser@example.com',
        'password': 'WrongPassword123'
    })

    # Assert response status and check for unauthorized access
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
