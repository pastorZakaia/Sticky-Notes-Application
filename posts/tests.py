from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth import get_user_model
from .forms import PostForm

class PostListViewTest(TestCase):
    """
    Tests for the PostListView.
    """
    def setUp(self):
        """
        Set up test data for the PostListView.
        """
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        Post.objects.create(title='Test Post 1', content='Test Content 1', author=self.user)
        Post.objects.create(title='Test Post 2', content='Test Content 2', author=self.user)

    def test_post_list_view(self):
        """
        Test that the post list view returns a 200 status code, uses the correct template,
        and contains the correct posts.
        """
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_list.html')
        self.assertContains(response, 'Test Post 1')
        self.assertContains(response, 'Test Post 2')

class PostDetailViewTest(TestCase):
    """
    Tests for the PostDetailView.
    """
    def setUp(self):
        """
        Set up test data for the PostDetailView.
        """
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_post_detail_view(self):
        """
        Test that the post detail view returns a 200 status code, uses the correct template,
        and contains the correct post content.
        """
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test Content')

class PostCreateViewTest(TestCase):
    """
    Tests for the PostCreateView.
    """
    def setUp(self):
        """
        Set up test data and log in the test user for the PostCreateView.
        """
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_post_create_view_get(self):
        """
        Test that the post create view returns a 200 status code, uses the correct template,
        and contains a valid PostForm instance.
        """
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_create_view_post(self):
        """
        Test that the post create view successfully creates a new post and redirects correctly.
        """
        response = self.client.post(reverse('post_create'), {'title': 'New Post', 'content': 'New Content'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post').exists())

class PostDeleteViewTest(TestCase):
    """
    Tests for the PostDeleteView.
    """
    def setUp(self):
        """
        Set up test data and log in the test user for the PostDeleteView.
        """
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_post_delete_view_get(self):
        """
        Test that the post delete view returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_confirm_delete.html')
