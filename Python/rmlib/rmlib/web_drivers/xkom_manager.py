from datetime import datetime

from rmlib.web_drivers.webpage_manager import PageNotifier
from rmlib.email_manager import EmailManager
from rmlib.logger import Logger

class XKomNotifier(PageNotifier):
    """Class for x-kom disabled checking and sending email to your email address
    """
    def __title_prefix(self):
        return 'XkomNotifier: '
    def __msg_prefix(self):
        return '[' + str(datetime.now()) + '] '
    def ___is_price_disabled(self):
        return self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div/div/button').get_property('disabled')

    def __validate_loaded_page(self):
        raise NotImplementedError()
        

    def __init__(self, url, email_manager: EmailManager, email_receipient, *, logger: Logger=None, send_email_at_startup: bool=True, send_email_at_change: bool=True, timeout=60):
        super(XKomNotifier, self).__init__(url, email_manager, email_receipient, logger=logger, send_email_at_startup=send_email_at_startup, send_email_at_change=send_email_at_change, timeout=timeout)
        self.disabled = self.___is_price_disabled()
        if send_email_at_startup:
            self.email_manager.send_email(
                to=self.email_receipient,
                subject=(self.__title_prefix() + self.driver.title),
                msg=(self.__msg_prefix() + 'Disabled: `' + str(self.disabled) + '`')
            )
            if self.logger:
                self.logger.log(self.__msg_prefix() + 'Email sent', console_add_prefix=False)
        if self.logger:
            self.logger.log(self.__msg_prefix() + 'Disabled: `' + str(self.disabled) + '`', console_add_prefix=False)

    def refresh(self):
        super(XKomNotifier, self).refresh()
        new_disabled = self.___is_price_disabled()
        if new_disabled != self.disabled:
            self.email_manager.send_email(
                to=self.email_receipient,
                subject=(self.__title_prefix() + self.driver.title),
                msg=(self.__msg_prefix() + 'Disabled changed from: `' + str(self.disabled) + '` to `' + str(new_disabled) + '`')
            )
            if self.logger:
                self.logger.log(self.__msg_prefix() + 'Email sent. Price changed from: `' + str(self.disabled) + '` to `' + str(new_disabled) + '`', console_add_prefix=False)
        if self.logger:
            self.logger.log(self.__msg_prefix() + 'Page refreshed. Current disabled: `' + str(new_disabled) + '`', console_add_prefix=False)
        self.disabled = new_disabled