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

def contains_content(browser, content):
    for elem in browser.find_elements_by_xpath('//*[text()]'):
        # hypothetically it should be possible to make this request using
        # a contains() predicate, but that doesn't seem to behave properly
        if elem.is_displayed() and content in elem.text:
            return True
	return False
	
def wait_for_elem(browser, xpath, timeout=15):
    start = time.time()
    elems = []
    while time.time() - start < timeout:
        elems = browser.find_elements_by_xpath(xpath)
        if elems:
            return elems
        time.sleep(0.2)
    return elems


def wait_for_content(step, browser, content, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        if contains_content(world.browser, content):
            return
        time.sleep(0.2)
    assert_true(step, contains_content(world.browser, content))


@step('I am in homepage SELENE$')
def homepage_selene(step):
    with AssertContextManager(step):
        #world.browser.get('http://localhost:8080/#/?_k=ujlsa1')
        world.browser.get('http://10.71.23.244/selene/#/?_k=63ld6h')
        world.browser.find_element_by_css_selector('.login-card.paper.white')

@step('I press "(.*?)"$')
def press(step, input_button_text):
	with AssertContextManager(step):
		button = world.browser.find_elelement_by_partial_link_text(input_button_text)
		button.click()
        time.sleep(2)

@step('I fill in the textfield with "(.*?)"$')
def fill_in_textfield(step, entry):
	with AssertContextManager(step):
		textfield = world.browser.find_element_by_xpath("//input[@id='gs_htif0']")
		textfield.clear()
		textfield.send_keys(entry)

@step('I should see "(.*?)"$')
def should_see(step, text, timeout=15):
	with AssertContextManager(step):
		start = time.time()
		while time.time() - start < timeout:
			if contains_content(world.browser, text):
				return
			time.sleep(2)
		assert_true(step, contains_content(world.browser, text))
        time.sleep(10)
		
@step('I press Ingresar$')
def should_see(step):
	with AssertContextManager(step):
		button = world.browser.find_element_by_css_selector(".btn.btn-secondary.btn-block")
		button.click()
		
@step('I am in Dashboar SELENE$')
def dashboar_selene(step):
	with AssertContextManager(step):
		world.browser.find_element_by_css_selector('.fa.fa-plus-square-o.icon')

@step('I press Registrar Dispositivo$')
def press_Registrar_dispositivo(step):
	with AssertContextManager(step):
		button = world.browser.find_element_by_css_selector('section.sidenav i.fa.fa-plus-square.icon')
		button.click()
		
@step('I am in "(.*?)" page$')
def registrar_dispositivo_page(step, page):
	with AssertContextManager(step):
		page in world.browser.find_element_by_css_selector('.container-fluid>h1').text
        time.sleep(2)

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

@step('I register Responsable like "(.*?)"$')
def assignee_name(step, content):
    with AssertContextManager(step):
        world.browser.find_element_by_css_selector('input[name="assignee_name"]').click()
        world.browser.find_element_by_css_selector('input[name="assignee_name"]').clear()
        world.browser.find_element_by_css_selector('input[name="assignee_name"]').send_keys(content)

@step('I select Proyecto like "(.*?)"$')
def assignee_project(step, content):
    with AssertContextManager(step):
        options = Select(world.browser.find_element_by_css_selector('select[name="project"]'))
        options.select_by_visible_text(content)

@step('I register Fecha de Entrega')
def assingee_expected_return_date(step):
    with AssertContextManager(step):
        world.browser.find_element_by_css_selector('input[name="expected_return_date"]').click()
        day = world.browser.find_element_by_css_selector('div.datepicker-days tr:nth-child(3) td[class="day"]:nth-child(6)')
        day.click()
        time.sleep(2)

@step('I select first device$')
def assignee_first_device(step):
    with AssertContextManager(step):
        check = world.browser.find_element_by_css_selector('input[type="checkbox"]:first-child')
        check.click()

@step('I select first device detail$')
def assignee_first_device_detail(step):
    with AssertContextManager(step):
        check = world.browser.find_element_by_css_selector('tr.data-row i.fa.fa-search:first-child')
        check.click()

@step('I press Guardar$')
def save_device(step):
    with AssertContextManager(step):
        button = world.browser.find_element_by_css_selector('a[id="save"] i')
        button.click()
        time.sleep(2)

@step('I press Aceptar$')
def ok_detail(step):
    with AssertContextManager(step):
        button = world.browser.find_element_by_css_selector('a[href="#/assigned_device_list"] i')
        button.click()
        time.sleep(2)

@step('I press Dashboard$')
def press_dashboard(step):
    with AssertContextManager(step):
        button = world.browser.find_element_by_css_selector('a[href="#dashboard"] i')
        button.click()
        time.sleep(2)

@step('I press Asignar$')
def asing_device_page(step):
    with AssertContextManager(step):
        button = world.browser.find_element_by_css_selector('i.fa.fa-user-plus.icon')
        button.click()
        time.sleep(2)

@step('I press Dispositivos')
def asing_device_page(step):
    with AssertContextManager(step):
        button = world.browser.find_element_by_css_selector('i.fa.fa-desktop.icon')
        button.click()
        time.sleep(2)

@step('I press button "(.*?)"$')
def press_button(step, content):
    with AssertContextManager(step):
        buttons = world.browser.find_elements_by_css_selector('a[class*="btn-create"]')
        for a in buttons:
            if a.is_displayed() and content in a.text:
                a.click()
                break
        time.sleep(2)