from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item, List
from lists.views import home_page
import lxml.html

class HomePageTest(TestCase):

  def test_uses_home_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')

  def test_renders_input_form(self):
    response = self.client.get('/')
    parsed = lxml.html.fromstring(response.content)
    [form] = parsed.cssselect('form[method="POST"]')
    self.assertEqual(form.get("action"), "/lists/new")
    intputs = form.cssselect('input[name=item_text]')
    self.assertIn("item_text", [input.get("name") for input in intputs])

class ListAndItemModelTest(TestCase):
  def test_saving_and_retrieving_items(self):
    mylist = List()
    mylist.save()

    first_item = Item()
    first_item.text = 'The first (ever) list item'
    first_item.list = mylist
    first_item.save()

    second_item = Item()
    second_item.text = 'Item the second'
    second_item.list = mylist
    second_item.save()

    saved_list = List.objects.get()
    self.assertEqual(saved_list, mylist)

    saved_items = Item.objects.all()
    self.assertEqual(saved_items.count(), 2)

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    self.assertEqual(first_saved_item.text, 'The first (ever) list item')
    self.assertEqual(first_saved_item.list, mylist)
    self.assertEqual(second_saved_item.text, 'Item the second')
    self.assertEqual(second_saved_item.list, mylist)

class ListViewTest(TestCase):
  def test_uses_list_template(self):
    mylist = List.objects.create()
    response = self.client.get(f'/lists/{mylist.id}/')
    self.assertTemplateUsed(response, 'list.html')

  def test_renders_input_form(self):
    mylist = List.objects.create()
    response = self.client.get(f'/lists/{mylist.id}/')
    parsed = lxml.html.fromstring(response.content)
    [form] = parsed.cssselect('form[method="POST"]')
    self.assertEqual(form.get("action"), f"/lists/{mylist.id}/add_item")
    intputs = form.cssselect('input[name=item_text]')
    self.assertIn("item_text", [input.get("name") for input in intputs])


  def test_displays_all_list_items(self):
    correct_list = List.objects.create()
    Item.objects.create(text='itemey 1', list=correct_list)
    Item.objects.create(text='itemey 2', list=correct_list)

    other_list = List.objects.create()
    Item.objects.create(text='other list item', list=other_list)

    response = self.client.get(f'/lists/{correct_list.id}/')

    self.assertContains(response, 'itemey 1')
    self.assertContains(response, 'itemey 2')
    self.assertNotContains(response, 'other list item')

class NewListTest(TestCase):
  def test_can_savea_POST_request(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()
    self.client.post(
      f'/lists/{other_list.id}/add_item',
      data={'item_text': 'A new item for an existing list'}
    )

    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'A new item for an existing list')

  def test_redirects_after_POST(self):
    response = self.client.post(
      f'/lists/new',
      data={'item_text': 'A new list item'}
    )
    new_list = List.objects.get()
    self.assertRedirects(response, f'/lists/{new_list.id}/')