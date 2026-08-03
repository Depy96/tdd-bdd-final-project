"""
Environment for Behave Testing
"""
from os import getenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '30'))
BASE_URL = getenv('BASE_URL', 'http://localhost:8080')
DRIVER = getenv('DRIVER', 'firefox').lower()


def before_all(context):
    """ Executed once before all tests """
    context.base_url = BASE_URL
    context.wait_seconds = WAIT_SECONDS
    # Select either Chrome or Firefox
    if 'firefox' in DRIVER:
        context.driver = get_firefox()
    else:
        context.driver = get_chrome()
    context.driver.implicitly_wait(context.wait_seconds)
    context.config.setup_logging()


def after_all(context):
    """Executed after all tests"""
    driver = getattr(context, "driver", None)
    if driver:
        driver.quit()

######################################################################
# Utility functions to create web drivers
######################################################################

def get_chrome():
    """Creates a headless Chrome driver"""
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")

    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)


def get_firefox():
    """Creates a headless Firefox driver"""
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)    
    