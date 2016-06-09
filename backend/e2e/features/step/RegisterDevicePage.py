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



class MainPage(object):

    title = None
    type = None
    brand = None
    assets = None
    serial = None
    model = None
    purchase_date = None
    ownership = None
    btn_save = None

def __init__(self, driver):
    self.driver = webdriver.Chrome()
    self.implicitly_wait(1)

def open(self):
    self.driver.get(self.url)
    self.setLocators()

def setLocators(self):
    self.title = self.find_element_by_css_selector(".container-fluid>h1")
    self.type =  self.find_element_by_css_selector("select[name="device_type"]")
    self.brand = self.find_element_by_css_selector("select[name="device_brand"]")
    self.assets = self.find_element_by_css_selector(".btn-group a")
    self.serial = self.find_element_by_css_selector("input[name="serial_number"]")
    self.model = self.find_element_by_css_selector("input[name="model"]")
    self.purchase_date = self.find_element_by_css_selector("input[name="purchase_date"]")
    self.ownership = self.find_element_by_css_selector("select[name="ownership"]")
    self.btn_save = self.find_element_by_css_selector("a[id="save"] i")

def select_type(self,type)
    options = Select(self.type)
    options.select_by_visible_text(type)




@step('I am in "(.*?)" page$')
def registrar_dispositivo_page(step, page):
    with AssertContextManager(step):
        page in world.browser.find_element_by_css_selector('.container-fluid>h1').text
    time.sleep(2)

@step('I press Registrar Dispositivo$')
def press_Registrar_dispositivo(step):
    with AssertContextManager(step):
        button = world.browser.find_element_by_css_selector('section.sidenav i.fa.fa-plus-square.icon')
        button.click()

@step('I select Tipo like "(.*?)"$')
def select_device_type(step, content):
    with AssertContextManager(step):
        options = Select(world.browser.find_element_by_css_selector('select[name="device_type"]'))
        options.select_by_visible_text(content)

@step('I select Marca like "(.*?)"$')
def select_device_brand(step, content):
    with AssertContextManager(step):
        options = Select(world.browser.find_element_by_css_selector('select[name="device_brand"]'))
        options.select_by_visible_text(content)

@step('I select Activo like "(.*?)"$')
def select_device_activo(step, content):
    with AssertContextManager(step):
        options = world.browser.find_elements_by_css_selector('.btn-group a')
        for a in options:
            if a.is_displayed() and content in a.text:
                a.click()

@step('I register Serial like "(.*?)"$')
def register_device_serial(step, content):
    with AssertContextManager(step):
        world.browser.find_element_by_css_selector('input[name="serial_number"]').click()
        world.browser.find_element_by_css_selector('input[name="serial_number"]').clear()
        world.browser.find_element_by_css_selector('input[name="serial_number"]').send_keys(content)

@step('I register Modelo like "(.*?)"$')
def register_device_model(step, content):
    with AssertContextManager(step):
        world.browser.find_element_by_css_selector('input[name="model"]').click()
        world.browser.find_element_by_css_selector('input[name="model"]').clear()
        world.browser.find_element_by_css_selector('input[name="model"]').send_keys(content)

@step('I select Fecha de Compra like "(.*?)"$')
def register_device_purchase_date(step, content):
    with AssertContextManager(step):
        world.browser.find_element_by_css_selector('input[name="purchase_date"]').click()
        world.browser.find_element_by_css_selector('input[name="purchase_date"]').clear()
        world.browser.find_element_by_css_selector('input[name="purchase_date"]').send_keys(content)

@step('I select Propiedad like "(.*?)"$')
def select_device_ownership(step, content):
    with AssertContextManager(step):
        options = Select(world.browser.find_element_by_css_selector('select[name="ownership"]'))
        options.select_by_visible_text(content)

@step('I press Guardar$')
def save_device(step):
    with AssertContextManager(step):
        button = world.browser.find_element_by_css_selector('a[id="save"] i')
        button.click()
        time.sleep(2)