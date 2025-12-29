from unittest import skip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):
  @skip
  def test_cannot_add_empty_list_items(self):
    # Edith goes to the home page and tries to submit
    # an empty list item. She hits Enter on the empty input box
    # self.browser.get(self.live_server_url)
    # inputbox = self.browser.find_element(By.ID, 'id_new_item')
    # inputbox.send_keys(Keys.ENTER)

    # The home page refreshes, and there is an error message
    # saying that list items cannot be blank
    # self.wait_for_row_in_list_table("You can't have an empty list item")

    # She tries again with some text for the item, which now works
    # inputbox = self.browser.find_element(By.ID, 'id_new_item')
    # inputbox.send_keys('Buy milk')
    # inputbox.send_keys(Keys.ENTER)
    # self.wait_for_row_in_list_table('1: Buy milk')

    # Perversely, she now decides to submit a second blank list item

    # And she can correct it by filling some text in
    self.fail('Write me!')