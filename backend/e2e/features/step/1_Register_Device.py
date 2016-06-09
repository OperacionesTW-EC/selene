import time
from lettuce import step
from lettuce import world
from lettuce_webdriver.util import assert_true

@step('I select Tipo like "(.*?)"$')
def select_device_type(step, content):
    with AssertContextManager(step):
        RegisterDevicePage.select_type(content)