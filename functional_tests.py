from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jane heart about a cool new website to-do app.
        # So she goes to homepage to check it
        self.browser.get('http://localhost:8000')

        # She notices that title says to-do
        self.assertIn('To-Do', self.browser.title)
        self.fail()

        # She is invited to enter a to-do item 

        # She types '1: do ironing'

        # Then after she pressed enter the page refreshes and new item appears at it

        # There is still textbox inviting her to type

        # She types '2: do homework'

        # After she press enter page reloads and both items are shown

        # Jane wonders wheather site will remember her list. 
        # She sees that site has generated a unique URL for her

        # She visites that URL and sees her to-do list

        # Satisfied she goes sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')

