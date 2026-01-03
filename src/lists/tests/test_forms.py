from django.test import TestCase
from lists.forms import ItemForm

class ItemFormTest(TestCase):

  def test_form_renders_item_text_input(self):
    form = ItemForm()

    rendered = form.as_p()

    self.assertIn('placeholder="Enter a to-do item"', rendered)
    self.assertIn('class="form-control input-lg"', rendered)
