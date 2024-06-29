from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post

class PostViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post1 = Post.objects.create(title='Test Post 1', content='Content for post 1', author=self.user)
        self.post2 = Post.objects.create(title='Test Post 2', content='Content for post 2', author=self.user)

    def test_post_list_view(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post 1')
        self.assertContains(response, 'Test Post 2')

    def test_post_detail_view(self):
        response = self.client.get(f'/posts/{self.post1.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post 1')

    def test_post_create_view_get(self):
        response = self.client.get('/posts/new/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_view_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/posts/new/', {
            'title': 'New Post',
            'content': 'New content',
            'author': self.user.pk
        })
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after creation
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_post_update_view_get(self):
        response = self.client.get(f'/posts/{self.post1.pk}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_post_update_view_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(f'/posts/{self.post1.pk}/edit/', {
            'title': 'Updated Post',
            'content': 'Updated content',
            'author': self.user.pk
        })
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after updating
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Post')

    def test_post_delete_view_get(self):
        response = self.client.get(f'/posts/{self.post1.pk}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_post_delete_view_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(f'/posts/{self.post1.pk}/delete/')
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after deleting
        self.assertFalse(Post.objects.filter(pk=self.post1.pk).exists())
