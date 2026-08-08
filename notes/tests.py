from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class SearchViewAuthTests(TestCase):
    def test_anonymous_user_is_redirected_not_crashed(self):
        """
        Regression test: search() used to call
        notes.objects.filter(user_1=request.user) without checking
        is_authenticated first, which raised a ValueError for
        AnonymousUser instead of redirecting to login.
        """
        response = self.client.get(reverse('search'), {'q': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
