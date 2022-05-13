from django.test import TestCase
from django.urls import reverse
from lists.models import Item


class HomePageTests(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertRedirects(response, reverse('homepage'))

    def test_only_save_item_when_it_is_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='first item')
        Item.objects.create(text='second item')

        response = self.client.get('/')
        self.assertContains(response, 'first item')
        self.assertContains(response, 'second item')


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
