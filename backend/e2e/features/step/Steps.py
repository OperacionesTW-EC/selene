import time
from lettuce import world, step
from lettuce_webdriver.util import assert_true
from selenium.webdriver.support.ui import Select
from lettuce_webdriver.util import AssertContextManager
import config
from pages import main_page, side_nav


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


@step('I am on the Selene homepage$')
def homepage_selene(step):
    with AssertContextManager(step):
        world.browser.get(config.home_url())


@step('I press "(.*?)"$')
def press(step, button_text):
    with AssertContextManager(step):
        main_page.button(button_text).click()


@step('I save$')
def save(step):
    with AssertContextManager(step):
        main_page.Guardar().click()
        time.sleep(2)


@step('I choose "(.*?)" on the side nav$')
def side_nave(step, button_text):
    with AssertContextManager(step):
        side_nav.button(button_text).click()


@step('I should see "(.*?)"$')
def should_see(step, text, timeout=15):
    with AssertContextManager(step):
        start = time.time()
        while time.time() - start < timeout:
            if contains_content(world.browser, text):
                return
        assert_true(step, contains_content(world.browser, text))
        time.sleep(10)


@step('I press Ingresar$')
def enter(step):
    with AssertContextManager(step):
        main_page.ingresar_button().click()


@step('I should be on the "(.*?)" page$')
@step('I am on the "(.*?)" page$')
def verify_header(step, page_name):
    """
    'Given' has responsibility for establishing conditions, not just verifying them.
    For example:
        "Given I am on the 'Fulano' page"
              should navigate us to the page, not just assert that we are there
    """
    with AssertContextManager(step):
        page_name in main_page.page_header().text


@step('I select Tipo "(.*?)"$')
def select_device_type(step, content):
    with AssertContextManager(step):
        options = Select(main_page.device_types())
        options.select_by_visible_text(content)


@step('I select Marca "(.*?)"$')
def select_device_brand(step, content):
    with AssertContextManager(step):
        options = Select(main_page.device_brands())
        options.select_by_visible_text(content)


@step('I select Activo "(.*?)"$')
def select_device_activo(step, content):
    with AssertContextManager(step):
        for a in main_page.active_status_buttons():
            if a.is_displayed() and content in a.text:
                a.click()


@step('I enter Serial "(.*?)"$')
def enter_device_serial(step, content):
    with AssertContextManager(step):
        main_page.enter_text('serial_number', content)


@step('I enter Modelo "(.*?)"$')
def enter_device_model(step, content):
    with AssertContextManager(step):
        world.browser.find_element_by_css_selector('input[name="model"]').click()
        world.browser.find_element_by_css_selector('input[name="model"]').clear()
        world.browser.find_element_by_css_selector('input[name="model"]').send_keys(content)


@step('I select Fecha de Compra "(.*?)"$')
def enter_device_purchase_date(step, content):
    with AssertContextManager(step):
        main_page.enter_text('purchase_date', content)


@step('I select Propiedad "(.*?)"$')
def select_device_ownership(step, content):
    with AssertContextManager(step):
        options = Select(main_page.ownership())
        options.select_by_visible_text(content)


@step('I enter Responsable "(.*?)"$')
def assignee_name(step, content):
    with AssertContextManager(step):
        world.browser.find_element_by_css_selector('input[name="assignee_name"]').click()
        world.browser.find_element_by_css_selector('input[name="assignee_name"]').clear()
        world.browser.find_element_by_css_selector('input[name="assignee_name"]').send_keys(content)


@step('I select Proyecto "(.*?)"$')
def assignment_project(step, content):
    with AssertContextManager(step):
        options = Select(main_page.project())
        options.select_by_visible_text(content)


@step('I enter Fecha de Entrega')
def assingment_expected_return_date(step):
    with AssertContextManager(step):
        main_page.expected_return_date().click()
        day = main_page.datepicker_day(3, 6)
        day.click()


@step('I select first device$')
def assignment_first_device(step):
    with AssertContextManager(step):
        main_page.device_check_boxes()[0].click()


@step('I select first device detail$')
def assignment_first_device_detail(step):
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
def assign_device_page(step):
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
        main_page.device_detail_buttons()[0].click()
