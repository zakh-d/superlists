from cgitb import text
from django.test import TestCase
from django.urls import reverse
from lists.models import Item, List


class ItemAndListModelsTests(TestCase):

    def test_saving_and_retrieving_items(self):
        
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'First item'
        first_item.list = list_
        first_item.save()

        second_item = Item(text='Second item')
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.last()
        self.assertEqual(saved_list, list_)

        items = Item.objects.all()

        self.assertEqual(items[0].text, 'First item')
        self.assertEqual(items[0].list, saved_list)
        self.assertEqual(items[1].text, 'Second item')
        self.assertEqual(items[1].list, saved_list)


class HomePageTests(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_save_item_when_it_is_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_items(self):
        
        list_ = List.objects.create()
        Item.objects.create(text='item1', list=list_)
        Item.objects.create(text='item2', list=list_)

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

