import yaml
import os


def selene_test_env():
    env_key = 'SELENE_TEST_ENV'
    if env_key in os.environ:
        return os.environ['SELENE_TEST_ENV'].upper()
    return 'QA'


def config():
    e2e_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
    yaml_path = '%s/config.yml' % e2e_dir
    with open(yaml_path, 'r') as yml:
        _config = yaml.load(yml)

    return _config[selene_test_env()]


def home_url():
    return config()['home_url']
