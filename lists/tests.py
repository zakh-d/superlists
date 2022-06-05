from cgitb import text
from django.test import TestCase
from django.urls import reverse
from lists.models import Item


class HomePageTests(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_save_item_when_it_is_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTests(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'First item'
        first_item.save()

        second_item = Item(text='Second item')
        second_item.save()

        items = Item.objects.all()

        self.assertEqual(items[0].text, 'First item')
        self.assertEqual(items[1].text, 'Second item')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_items(self):
        item1 = Item.objects.create(text='item1')
        item2 = Item.objects.create(text='item2')

        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')


class NewListTests(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

