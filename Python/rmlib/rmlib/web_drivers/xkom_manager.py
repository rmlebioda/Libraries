from datetime import datetime
from enum import IntEnum
from dataclasses import dataclass

from rmlib.web_drivers.webpage_manager import PageManager
from rmlib.email_manager import EmailManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TechnicalBreakException(Exception):
    pass
class CartAmountException(Exception):
    pass
class AddToCartException(Exception):
    pass
class InvalidWebpageException(Exception):
    pass
class InvalidLoginCredentialsException(Exception):
    pass
class LoadingPageFailureException(Exception):
    pass
class InvalidOrderDataException(Exception):
    pass

class ShippingEnum(IntEnum):
    Courier = 1
    PersonalPickup = 2
    ParcelLockers = 3

class PaymentMethodEnum(IntEnum):
    Blik = 1
    CreditCardOnline = 2
    FastTransferDotPay = 3
    CashTransfer = 4
    UponReceipt = 5
    Rates = 6
    Leasing = 7

@dataclass
class OrderData:
    Shipping: ShippingEnum
    PaymentMethod: PaymentMethodEnum
    FirstAndLastName: str
    Address: str
    ZipCode: str
    Town: str
    Email: str
    Phone: str
    def validate(self):
        if self.Shipping == None:
            raise InvalidOrderDataException("Shipping cannot be None")
        if self.PaymentMethod == None:
            raise InvalidOrderDataException("PaymentMethod cannot be None")
        if self.FirstAndLastName == '' or self.FirstAndLastName == None:
            raise InvalidOrderDataException("First and Last name cannot be None/empty")
        if self.Address == '' or self.Address == None:
            raise InvalidOrderDataException("Address cannot be None/empty")
        if self.ZipCode == '' or self.ZipCode == None:
            raise InvalidOrderDataException("Zip code cannot be None/empty")
        if self.Town == '' or self.Town == None:
            raise InvalidOrderDataException("Town cannot be None/empty")
        if self.Email == '' or self.Email == None:
            raise InvalidOrderDataException("Email cannot be None/empty")
        if self.Phone == '' or self.Phone == None:
            raise InvalidOrderDataException("Phone cannot be None/empty")
    @staticmethod
    def get_xpath_shipping(Shipping: ShippingEnum) -> str:
        if Shipping == ShippingEnum.Courier:
            return '/html/body/div[1]/div/div[2]/form/div/div[1]/div[2]/div/div[1]/div/label'
        elif Shipping == ShippingEnum.ParcelLockers:
            return '/html/body/div[1]/div/div[2]/form/div/div[1]/div[2]/div/div[2]/div[1]/label'
        elif Shipping == ShippingEnum.PersonalPickup:
            '/html/body/div[1]/div/div[2]/form/div/div[1]/div[2]/div/div[3]/div[1]/label'
        else:
            raise InvalidOrderDataException('Unknown Shipping method: ' + str(Shipping))
    @staticmethod
    def get_xpath_payment_mathod(PaymentMethod: PaymentMethodEnum) -> str:
        return '/html/body/div[1]/div/div[2]/form/div/div[1]/div[3]/div[2]/div[ ' + str(int(PaymentMethod)) + ']/div/label'

class XKomManager(PageManager):
    """Class for x-kom disabled checking and sending email to your email address
    """
    def __init__(self, *, timeout=60, login=None, password=None):
        super(XKomManager, self).__init__(timeout=timeout)
        self.login = login
        self.password = password

    def get(self, url: str):
        self.driver.get(url)
        self.__validate()

    def refresh(self):
        super(XKomManager, self).refresh()
        self.__validate()

    def __title_prefix(self):
        return 'XkomNotifier: '
    def __msg_prefix(self):
        return '[' + str(datetime.now()) + '] '
    def is_button_adding_to_chart_disabled(self):
        """Checks, if items is available for buying (can be added to chart)

        Raises:
            InvalidWebpageException: Adding to chart button was not found

        Returns:
            bool: Whenever item can be bought or not
        """        
        try:
            return self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div/div/button').get_property('disabled')
        except NoSuchElementException:
            raise InvalidWebpageException(str(e))

    def __validate(self):
        """Validates read webpage for common technical errors

        Raises:
            TechnicalBreakException: When page was not loaded successfully (not fully implemented!)
        """        
        # check technical break 
        try:
            if self.driver.find_element_by_xpath('/html/body/div[2]/div/img').get_property('alt') == 'Przerwa techniczna':
                raise TechnicalBreakException()
        except TechnicalBreakException:
            raise
        except Exception:
            pass
        # check error 503... (haven't saved the webpage...)
        # ok
        return
        
    def get_cart_members(self) -> int:
        """Returns amount of items in cart

        Raises:
            CartAmountException: When webpage is not loaded correctly or function was unable find cart amount element

        Returns:
            int: Amount of items in cart
        """        
        try:
            return int(self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/header/div[1]/div[4]/div/div[4]/div/div[1]/a/div[1]/div/div/span').text)
        except NoSuchElementException:
            return 0
        except Exception as e:
            raise CartAmountException(str(e))

    def add_to_cart(self, go_to_cart = True):
        """Adds current visiting product to cart

        Args:
            go_to_cart (bool, optional): Whenever driver should proceed to chart after adding product. Defaults to True.

        Raises:
            AddToCartException: When button "Add to chart" is not found
            TimeoutException: When popup after adding item to chart is not shown in given timeout
        """        
        try:
            button = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/button')
            if button.text != 'Dodaj do koszyka':
                raise AddToCartException('Failed to find button "Dodaj do koszyka" by xpath')
            button.click()
            if go_to_cart == True:
                def __found_continue_to_cart_button(driver):
                    try:
                        if driver.find_element_by_xpath('/html/body/div[3]/div[10]/div/div/div/div[4]/a').text == 'Przejdź do koszyka':
                            return True
                    except Exception:
                        return False
                    return False
                WebDriverWait(self.driver, self.timeout).until(lambda x: __found_continue_to_cart_button(x))
                self.driver.find_element_by_xpath('/html/body/div[3]/div[10]/div/div/div/div[4]/a').click()
        except AddToCartException:
            raise
        except NoSuchElementException:
            raise AddToCartException(str(e))
        except TimeoutException as e:
            raise AddToCartException('Timeout on adding to cart' + str(e))
        except Exception as e:
            raise AddToCartException(str(e))

    def __is_in_cart_webpage(self):
        try:
            if self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]').text.startswith('Koszyk'):
                return True
        except:
            pass
        return False

    def go_to_cart(self, load_limit=5):
        """Proceedes to cart

        Args:
            load_limit (int, optional): Max tries for opening cart. Defaults to 5.

        Raises:
            LoadingPageFailureException: When loading webpage failed more than load_limit times
        """        
        __try = 0
        while True:
            if self.__is_in_cart_webpage() or __try > load_limit:
                break
            self.get('https://www.x-kom.pl/koszyk')
            __try += 1
        if __try > load_limit:
            raise LoadingPageFailureException('Failed to load cart with limit of:' + str(load_limit))

    def __is_in_login_page(self):
        try:
            if self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[1]/div/h2').text == 'Zaloguj się':
                return True
        except:
            pass
        return False

    def confirm_cart_order(self):
        """Proceeds from popup to cart, that opens after adding product to shop cart.

        Raises:
            InvalidWebpageException: When popup is not found
        """        
        try:
            self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[3]/button').click()
        except Exception:
            raise InvalidWebpageException('Could not find confirm button on cart order on webpage: ' + self.driver.current_url)
        WebDriverWait(self.driver, self.timeout).until(lambda x: self.__is_in_login_page())

    def __is_in_order_page(self):
        try:
            if self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/form/div/div[1]/h1').text == 'Dostawa i płatność':
                return True
        except Exception:
            pass
        return False

    def login_if_necessary(self):
        """Checks if webpage requires logging in, if so then it will the data, log in and wait for order page to load up in timeout period

        Raises:
            InvalidLoginCredentialsException: When login or password is None/empty
        """        
        if self.login == None or self.login == '':
            raise InvalidLoginCredentialsException('Loging in impossible, login is empty or None')
        if self.password == None or self.password == '':
            raise InvalidLoginCredentialsException('Loging in impossible, password is empty or None')
        try:
            if self.__is_in_login_page():
                email_login_field = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[1]/div/form/div[1]/label/input')
                password_field = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[1]/div/form/div[2]/div/label/input')
                email_login_field.send_keys(self.login)
                password_field.send_keys(self.password)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[1]/div/form/button').click()
        except:
            pass
        WebDriverWait(self.driver, self.timeout).until(lambda x: self.__is_in_order_page())
    
    def __send_to_input(self, input_xpath, value):
        __input = self.driver.find_element_by_xpath(input_xpath)
        if __input.get_attribute('value') != '':
            raise InvalidOrderDataException('Input with xpath ' + input_xpath + ' should be empty before filling!')
        __input.send_keys(value)

    def __fill_order(self, order: OrderData):
        self.driver.find_element_by_xpath(OrderData.get_xpath_shipping(order.Shipping)).click()
        self.driver.find_element_by_xpath(OrderData.get_xpath_payment_mathod(order.PaymentMethod)).click()
        self.__send_to_input('/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[1]/label/input', order.FirstAndLastName)
        self.__send_to_input('/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[2]/label/input', order.Address)
        self.__send_to_input('/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[3]/label/input', order.ZipCode)
        self.__send_to_input('/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[4]/label/input', order.Town)
        self.__send_to_input('/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[5]/label/input', order.Email)
        self.__send_to_input('/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[6]/label/input', order.Phone)

    def buy(self, order: OrderData):
        """Buys everything in chart (without confirming)

        Args:
            order (OrderData): Filled order data for shipping infromation

        Raises:
            InvalidOrderDataException: When order data is None or when not all fields are filled (partial filling for personal pickup not supported yet)
        """        
        if order == None:
            raise InvalidOrderDataException('Order data must be filled')
        order.validate()
        self.go_to_cart()
        self.confirm_cart_order()
        self.login_if_necessary()
        self.__fill_order(order)
