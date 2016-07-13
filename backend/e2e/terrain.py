from lettuce import before, after, world
from selenium import webdriver
from config import browser
import os


@before.all
def setup_browser():
    world.browser = browser(webdriver)
    world.browser.implicitly_wait(1)


@after.all
def tear_down_feature(feature):
    world.browser.quit()
