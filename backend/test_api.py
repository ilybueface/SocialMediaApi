import pytest
from .models import CustomUser, Post
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_backend_post():
    client = APIClient()
    response = client.get('/backend/post/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_post_request():
    user = CustomUser.objects.create_user(username='test', password='test1234')
    refresh = RefreshToken.for_user(user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

    response = client.post('/backend/post/', {'text': 'Темник'}, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_double_like():
    user = CustomUser.objects.create_user(username='test', password='test1234')
    refresh = RefreshToken.for_user(user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

    first_post = Post.objects.create(author=user)

    response = client.post(f'/backend/post/{first_post.pk}/like/', format='json')
    assert response.status_code == 201

    response_too = client.post(f'/backend/post/{first_post.pk}/like/', format='json')
    assert response_too.status_code == 400

