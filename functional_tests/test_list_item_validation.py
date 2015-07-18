from .base import FunctionalTest
from unittest import skip


class ItemValidationTest(FunctionalTest):

    def test_cant_add_empty_list_items(self):

        # edith goes to the home page and accidentally tries to add an empty
        # item.  She hits enter with an empty input box
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # The home page refreshes and there is an error message saying that the
        # input box cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item.")

        # She tries again with some text for the item, which now succeeds
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        # She tries to enter another empty line
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item.")

        # She corrects it by entering new text
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
