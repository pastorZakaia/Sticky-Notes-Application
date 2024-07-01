from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth import get_user_model
from .forms import PostForm


class PostListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        Post.objects.create(title='Test Post 1', content='Test Content 1', author=self.user)
        Post.objects.create(title='Test Post 2', content='Test Content 2', author=self.user)

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_list.html')
        self.assertContains(response, 'Test Post 1')
        self.assertContains(response, 'Test Post 2')


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test Content')

class PostCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_post_create_view_get(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_create_view_post(self):
        response = self.client.post(reverse('post_create'), {'title': 'New Post', 'content': 'New Content'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post').exists())

class PostUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_post_update_view_get(self):
        response = self.client.get(reverse('post_update', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_update_view_post(self):
        response = self.client.post(reverse('post_update', args=[self.post.pk]), {'title': 'Updated Post', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')
        self.assertEqual(self.post.content, 'Updated Content')

class PostDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_post_delete_view_get(self):
        response = self.client.get(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_confirm_delete.html')

  