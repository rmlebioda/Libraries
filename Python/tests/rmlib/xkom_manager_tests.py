import unittest
from rmlib.web_drivers.xkom_manager import XKomManager, LoginData, LoginTypeEnum, PageDuringLoadingWaitFor as Waiter

class TestXKomManager(unittest.TestCase):
    def setUp(self):
        self.xkom = XKomManager(LoginData(LoginTypeEnum.AsGuest))

    def should_load_home(self):
        self.xkom.home()
        self.assertTrue(self.xkom.driver \
            .find_element_by_xpath(self.xkom.xpath_search_bar) \
            .get_attribute('placeholder') == 'Czego szukasz?')
    
    def should_fast_load(self):
        self.xkom.load_hot_deal(Waiter.WholeWebpage)
        

if __name__ == '__main__':
    unittest.main()