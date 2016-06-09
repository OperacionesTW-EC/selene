from lettuce import before, after, world
import lettuce_webdriver.webdriver
from selenium import webdriver


@before.all
def setup_browser():
    world.browser = webdriver.Firefox()
    world.browser.implicitly_wait(1)
    #  world.browser.get('http://localhost:8080/#/?_k=ujlsa1')
    #  world.browser.get('http://10.71.23.244/selene/#/?_k=63ld6h')
    #  world.browser.maximize_window()


@after.all
def tear_down_feature(feature):
    world.browser.quit()
