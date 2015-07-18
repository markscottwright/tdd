from .base import FunctionalTest
from unittest import skip


class ItemValidationTest(FunctionalTest):

    @skip
    def test_cant_add_empty_list_items(self):

        # edith goes to the home page and accidentally tries to add an empty
        # item.  She hits enter with an empty input box

        # The home page refreshes and there is an error message saying that the
        # input box cannot be blank

        # [...]

        self.fail('finish me')
