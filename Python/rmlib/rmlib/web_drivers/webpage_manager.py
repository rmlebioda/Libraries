import os
from pathlib import Path

from selenium import webdriver
from rmlib.common import setting_path, log_path
from configparser import ConfigParser


class PageManager():
    """Base class for webpage checking and email notification
    """

    def __init__(self, *, timeout=60, geckodriver_dir=log_path, minimize_window=True):
        # opt = webdriver.FirefoxOptions()
        # opt.add_argument("--headless")
        # self.driver = webdriver.Firefox(firefox_options=opt,
        #     service_log_path=os.path.join(geckodriver_dir, 'geckodriver.log'))
        Path(geckodriver_dir).mkdir(parents=True, exist_ok=True)
        self.driver = webdriver.Firefox(
            service_log_path=os.path.join(geckodriver_dir, 'geckodriver.log'))
        self.minimize_window = minimize_window
        if self.minimize_window:
            self.driver.minimize_window()
        self.timeout = timeout
        self.driver.set_page_load_timeout(timeout)
        self.settings = ConfigParser()
        self.settings.read(setting_path)

    def refresh(self):
        self.driver.refresh()

    def __del__(self):
        self.driver.close()
