from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item
from lists.views import home_page

class HomePageTest(TestCase):

  def test_uses_home_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')

  def test_renders_input_form(self):
    response = self.client.get('/')
    self.assertContains(response, '<form method="POST">')
    self.assertContains(response, '<input name="item_text"')

  def test_cans_save_a_POST_request(self):
    response = self.client.post('/', data={'item_text': 'A new list item'})

    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'A new list item')

    self.assertContains(response, 'A new list item')
    self.assertTemplateUsed(response, 'home.html')
  def test_only_saves_items_when_necessary(self):
    self.client.get('/')
    self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):
  def test_saving_and_retrieving_items(self):
    from lists.models import Item

    item1 = Item()
    item1.text = 'The first (ever) list item'
    item1.save()

    item2 = Item()
    item2.text = 'Item the second'
    item2.save()

    saved_items = Item.objects.all()
    self.assertEqual(saved_items.count(), 2)

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    self.assertEqual(first_saved_item.text, 'The first (ever) list item')
    self.assertEqual(second_saved_item.text, 'Item the second')

