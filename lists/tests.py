from django.test import TestCase
from lists.models import Item


class HomePageTests(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertContains(response, 'A new list item')
        self.assertTemplateUsed(response, 'home.html')

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
