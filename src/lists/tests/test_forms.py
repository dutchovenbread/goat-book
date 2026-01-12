from django.test import TestCase
from lists.forms import (
  DUPLICATE_ITEM_ERROR,
  EMPTY_ITEM_ERROR,
  ExistingListItemForm,
  ItemForm, 
)
from lists.models import Item, List

class ExistingListItemFormTest(TestCase):
  def test_form_save(self):
    mylist = List.objects.create()
    form = ExistingListItemForm(for_list=mylist, data={'text': 'hi'})
    self.assertTrue(form.is_valid())
    new_item = form.save()
    self.assertEqual(new_item, Item.objects.all()[0])

  def test_form_renders_item_text_input(self):
    list_ = List.objects.create()
    form = ExistingListItemForm(for_list=list_)
    self.assertIn('placeholder="Enter a to-do item"', form.as_p())

  def test_form_validation_for_blank_items(self):
    list_ = List.objects.create()
    form = ExistingListItemForm(for_list=list_, data={'text': ''})
    self.assertFalse(form.is_valid())
    self.assertEqual(
      form.errors['text'],
      [EMPTY_ITEM_ERROR]
    )

  def test_form_save_handles_saving_to_a_list(self):
    list_ = List.objects.create()
    Item.objects.create(list=list_, text='no twins!')
    form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
    self.assertFalse(form.is_valid())
    self.assertEqual(
      form.errors['text'],
      [DUPLICATE_ITEM_ERROR]
    )

class ItemFormTest(TestCase):

  def test_form_renders_item_text_input(self):
    form = ItemForm()

    rendered = form.as_p()

    self.assertIn('placeholder="Enter a to-do item"', rendered)
    self.assertIn('class="form-control input-lg"', rendered)

  def test_form_validation_for_blank_items(self):
    form = ItemForm(data={'text': ''})
    self.assertFalse(form.is_valid())
    self.assertEqual(
      form.errors['text'],
      [EMPTY_ITEM_ERROR]
    )

  def test_form_save_handles_saving_to_a_list(self):
    mylist = List.objects.create()
    form = ItemForm(data={'text': 'do me'})
    new_item = form.save(for_list=mylist)
    self.assertEqual(new_item, Item.objects.get())
    self.assertEqual(new_item.text, 'do me')
    self.assertEqual(new_item.list, mylist)

  def test_invalid_form_has_bootstrap_is_invalid_css_class(self):
    form = ItemForm(data={'text': ''})
    self.assertFalse(form.is_valid())
    field = form.fields["text"]
    self.assertEqual(
      field.widget.attrs["class"],
      "form-control input-lg is-invalid"
    )