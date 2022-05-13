from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jane heart about a cool new website to-do app.
        # So she goes to homepage to check it
        self.browser.get(self.live_server_url)

        # She notices that title and headline says to-do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types 'Do ironing'
        inputbox.send_keys('Do ironing')
        inputbox.send_keys(Keys.ENTER)
        
        time.sleep(1)

        # Then after she pressed enter the page refreshes and new item appears at it
        self.check_for_row_in_list_table('1: Do ironing')

        # There is still textbox inviting her to type
        # She types 'Do homework'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do homework')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # After she press enter page reloads and both items are shown
        
        self.check_for_row_in_list_table('2: Do homework')

        # Jane wonders wheather site will remember her list.
        # She sees that site has generated a unique URL for her
        self.fail('Finish tests')

        # She visites that URL and sees her to-do list
        # Satisfied she goes sleep
