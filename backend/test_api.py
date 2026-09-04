import pytest

from .conftest import second_auth_client
from .models import CustomUser, Post, Follow, Story
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
def test_backend_post():
    client = APIClient()
    response = client.get('/backend/post/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_request(user, auth_client):
    client = auth_client

    response = client.post('/backend/post/', {'text': 'Темник', 'author_id': user.id}, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_double_like(auth_client, user):
    client = auth_client


    first_post = Post.objects.create(author=user)

    response = client.post(f'/backend/post/{first_post.pk}/like/', format='json')
    assert response.status_code == 201

    response_too = client.post(f'/backend/post/{first_post.pk}/like/', format='json')
    assert response_too.status_code == 400


@pytest.mark.django_db
def test_feed_check(auth_client, user):
    user_a = user
    user_b = CustomUser.objects.create_user(username='test12', password='test12234')
    user_c = CustomUser.objects.create_user(username='test1', password='test1234')

    client = auth_client

    follow = Follow.objects.create(follower=user_a, following=user_b)
    post_a = Post.objects.create(author=user_b)
    post_b = Post.objects.create(author=user_c)

    response = client.get('/backend/post/', format='json')

    post_ids = []
    for post in response.data['results']:
        post_ids.append(post['id'])

    assert post_a.id in post_ids
    assert post_b.id not in post_ids


@pytest.mark.django_db
def test_count_follow(user, auth_client):
    user_a = user
    user_b = CustomUser.objects.create_user(username='test123', password='tester1234')

    client = auth_client

    follow = Follow.objects.create(follower=user_a, following=user_b)

    response = client.get(f'/backend/user/{user_b.id}/', format='json')

    assert response.data['followers_count'] == 1


@pytest.mark.django_db
def test_pagination_list(user, auth_client):
    user_a = user
    user_b = CustomUser.objects.create_user(username='test344', password='tester1234')

    client = auth_client

    follow = Follow.objects.create(follower=user_a, following=user_b)
    post_a = Post.objects.create(author=user_b, text='test')
    post_b = Post.objects.create(author=user_b, text='test')
    post_c = Post.objects.create(author=user_b, text='test')

    response = client.get('/backend/post/?page_size=2')

    assert len(response.data['results']) == 2


@pytest.mark.django_db
def test_delta_story(user, auth_client):
    client = auth_client

    story = Story.objects.create(author=user, text='test')
    old_story = Story.objects.create(author=user, text='tester')
    old_story.created_at = timezone.now() - timedelta(hours=25)
    old_story.save()

    response = client.get('/backend/story/')
    story_ids = [s['id'] for s in response.data]

    assert story.id in story_ids
    assert old_story.id not in story_ids


@pytest.mark.django_db
def test_permission_list(user, second_user, second_auth_client):
    user_a = user
    user_b = second_user

    client = second_auth_client

    post = Post.objects.create(author=user_a, text='test1')
    follow = Follow.objects.create(follower=user_b, following=user_a)

    response = client.delete(f'/backend/post/{post.id}/')

    assert response.status_code == 403
