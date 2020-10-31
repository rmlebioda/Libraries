import os

from selenium import webdriver
from rmlib.email_manager import EmailManager
from rmlib.logger import Logger

class PageNotifier():
    """Base class for webpage checking and email notification
    """
    def __init__(self, url, email_manager: EmailManager, email_receipient, *, logger: Logger=None, send_email_at_startup: bool=True, send_email_at_change: bool=True, timeout=60, geckodriver_dir=os.path.join(os.path.expanduser('~'), '.rml')):
        self.email_manager = email_manager
        self.email_receipient = email_receipient
        self.logger = logger
        self.driver = webdriver.Firefox(service_log_path=os.path.join(geckodriver_dir, 'geckodriver.log'))
        self.driver.minimize_window()
        self.driver.set_page_load_timeout(timeout)
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()

    def __del__(self):
        self.driver.close()