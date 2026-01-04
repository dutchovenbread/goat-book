from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):

  def test_cannot_add_empty_list_items(self):
    # Edith goes to the home page and tries to submit
    # an empty list item. She hits Enter on the empty input box
    self.browser.get(self.live_server_url)
    inputbox = self.get_item_input_box()
    inputbox.send_keys(Keys.ENTER)

    # The browser intercepts the request, and does not load the list page
    self.wait_for(
      lambda: 
        self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
    )

    # She tries again with some text for the item, which now works
    inputbox = self.get_item_input_box()
    inputbox.send_keys('Purchase milk')
    self.wait_for(
      lambda:
        self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')
    )
    
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: Purchase milk')

    # Perversely, she now decides to submit a second blank list item
    inputbox = self.get_item_input_box()
    inputbox.send_keys(Keys.ENTER)

    # She receives a similar warning on the list page
    self.wait_for(
      lambda: 
        self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
    )

    # And she can correct it by filling some text in
    self.get_item_input_box().send_keys('Make tea')
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('2: Make tea')