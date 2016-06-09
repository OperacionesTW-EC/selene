from lettuce_webdriver.util import assert_true
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.ui import Select
from lettuce_webdriver.util import assert_false
from lettuce_webdriver.util import AssertContextManager
from lettuce_webdriver.util import find_button
from lettuce_webdriver.util import find_field
from lettuce_webdriver.util import find_option
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver


class LoginPage(object):

    url = "http://10.71.23.101/selene/#/?_k=pr900o"
    driver = None
    username = None
    password = None
    submit_button = None

def __init__(self, driver):
    self.driver = driver

def open(self):
    self.driver.get(self.url)
    self.setLocators()

def setLocators(self)
    self.submit_button=self.find_element_by_css_selector(".btn.btn-secondary.btn-block")

def login(self)
    self.submit_button.click()