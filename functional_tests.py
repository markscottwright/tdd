"Functional test script"

from selenium import webdriver
import unittest


class TestNewVisitor(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # user opens our todo app
        self.browser.get("http://localhost:8000")

        # header says To-do
        self.assertIn("To-Do", self.browser.title)

        # she is invited to add a todo item right away

        # she types buy peacock feathers into a text box

        # When she hits enter, the page updates and now the page lsits
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text box inviting her to enter another item.  She
        # enters "Use peacock feathers to make a fly"

        # The page updates again and now shows both items on her list

        # the user notices that the site has generated a unique URL for her --
        # there is some explanatory text to that effect

        # She visits that URL - her todo list is still there

if __name__ == "__main__":
    unittest.main()
