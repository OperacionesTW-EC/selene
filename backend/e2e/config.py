import yaml
import os


def selene_test_env():
    env_key = 'SELENE_TEST_ENV'
    if env_key in os.environ:
        return os.environ[env_key].upper()
    return 'QA'


def config():
    e2e_dir = os.path.realpath(os.path.join(os.path.dirname(__file__)))
    yaml_path = '%s/config.yml' % e2e_dir
    print "ALGO ALGO %s" % yaml_path
    with open(yaml_path, 'r') as yml:
        _config = yaml.load(yml)

    return _config[selene_test_env()]


def home_url():
    return config()['home_url']


def browser(driver):
    "TODO: move this to config object.  We must learn how to 'import features.step.config'"
    env_key = 'SELENE_TEST_BROWSER'
    _browser = 'FIREFOX'
    if env_key in os.environ:
        _browser = os.environ[env_key].upper()

    if _browser == 'FIREFOX':
        return driver.Firefox()

    if _browser == 'CHROME':
        return driver.Chrome()