import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as error:
                if time.time() - start_time > MAX_WAIT:
                    raise error
                time.sleep(.5)

    def test_can_start_a_list_for_one_user(self):
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
        self.wait_for_row_in_list_table('1: Do ironing')

        # There is still textbox inviting her to type
        # She types 'Do homework'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do homework')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # After she press enter page reloads and both items are shown
        self.wait_for_row_in_list_table('1: Do ironing')
        self.wait_for_row_in_list_table('2: Do homework')

    def test_can_start_list_for_multiple_users(self):
        # Jane starts new todo list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers!')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers!')
        # She sees that site has generated a unique URL for her
        jane_list_url = self.browser.current_url
        self.assertRegex(jane_list_url, r'/lists/.+')

        # Now a new user, Francis, comes along to the site
        
        ## We use a new browser session to make sure no info
        ## about Jane come from cookies

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits homepage and there is no sign of Jane's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers!', page_text)
        self.assertNotIn('Do homework', page_text)
        # Francis start a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('Buy milk')

        # Francis gets his own url
        francis_list_url = self.browser.current_url
        self.assertNotEqual(francis_list_url, jane_list_url)
        self.assertRegex(francis_list_url, '/lists/.+')

        # Again there is no trace of Jane's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers!', page_text)
        self.assertIn('Buy milk', page_text)
