from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import time
import tkinter as tk
import datetime as dt

class JugglingWebsiteTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, fn):
        start_time = time.time()
        refresh_available = True
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                elif time.time() - start_time > 0.5 * self.MAX_WAIT and refresh_available:
                    self.browser.refresh()
                    refresh_available = False
                time.sleep(0.5)


class AdminAndSiteVisitorTest(JugglingWebsiteTest):

    def setUp(self):
        ## self.browser is the main browser (i.e. the site visitor), self.jj_browser is the admin browser
        self.browser = webdriver.Firefox()
        self.jj_browser = webdriver.Firefox()

        root = tk.Tk()
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        ## it seems that mint's menu bar is 64 pixels high
        gap = 0
        browser_height = int(screenheight - 64)
        browser_width = int((screenwidth / 2) - gap)
        root.destroy()

        User.objects.create_superuser(username='admin_user', email='admin@jjs_juggling_site.com', password='secret_password')

        self.browser.set_window_size(browser_width, browser_height)
        self.jj_browser.set_window_size(browser_width, browser_height)
        self.browser.set_window_position(0, 0)
        self.jj_browser.set_window_position(browser_width + (gap * 2), 0)
        ## If there's going to be an admin browswer, we might as well log in during the set up
        self.jj_browser.get(f'{self.live_server_url}/admin/')
        username_field = self.jj_browser.find_element_by_id('id_username')
        username_field.send_keys('admin_user')
        password_field = self.jj_browser.find_element_by_id('id_password')
        password_field.send_keys('secret_password')
        password_field.send_keys(Keys.ENTER)

    def tearDown(self):
        self.jj_browser.quit()
        self.browser.quit()


