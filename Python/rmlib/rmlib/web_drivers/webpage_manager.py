import os

from selenium import webdriver

class PageManager():
    """Base class for webpage checking and email notification
    """
    def __init__(self, *, timeout=60, geckodriver_dir=os.path.join(os.path.expanduser('~'), '.rml')):
        self.driver = webdriver.Firefox(service_log_path=os.path.join(geckodriver_dir, 'geckodriver.log'))
        self.driver.minimize_window()
        self.timeout = timeout
        self.driver.set_page_load_timeout(timeout)

    def refresh(self):
        self.driver.refresh()

    def __del__(self):
        self.driver.close()