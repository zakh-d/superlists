from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import homepage


class HomePageTests(TestCase):

    def test_root_url_resolves_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = homepage(request)
        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do list</title>', html)
        self.assertTrue(html.endswith('</html>'))
