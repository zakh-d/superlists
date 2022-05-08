from django.urls import resolve
from django.test import TestCase

from lists.views import homepage


class HomePageTests(TestCase):

    def test_root_url_resolves_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

