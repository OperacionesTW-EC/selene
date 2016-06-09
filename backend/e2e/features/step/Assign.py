import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lettuce import step
from lettuce import world
from datetime import datetime
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
from page_objects import PageObject, PageElement
from page_objects import PageObject, MultiPageElement

class AssignPageLocators(object):
    assigned = (By.CSS_SELECTOR, 'input[name="assignee_name"]')
    project = (By.CSS_SELECTOR, 'select[name="project"]')
    return_date = (By.CSS_SELECTOR, 'input[name="expected_return_date"]')
    btn_save = (By.CSS_SELECTOR, 'a[id="save"] i')
    devices_list = (By.CSS_SELECTOR, '#device-list tbody tr')
    title = (By.CSS_SELECTOR, 'a[id="save"] i')

class AssignPage(Page):


class LoginPage(PageObject):
    username = PageElement(css='input[name="login"]')
    password = PageElement(css='input[name="password"]')
    login = PageElement(css='a[type="submit"]')
    title = PageElement(css='a[type="submit"]')
    form = PageElement(css='form.login-form')


class AssignPage(PageObject):
    assigned = PageElement(css='input[name="assignee_name"]')
    project = PageElement(css='select[name="project"]')
    return_date = PageElement(css='input[name="expected_return_date"]')
    btn_save = PageElement(css='a[id="save"] i')
    devices_list = MultiPageElement(css='#device-list tbody tr')
    title = PageElement(css='a[id="save"] i')

class RegisterDevicePage(PageObject):
    btn_save = PageElement(css='a[id="save"] i')
    type = PageElement(css='select[name="device_type"]')
    brand = PageElement(css='select[name="device_brand"]')
    assets =