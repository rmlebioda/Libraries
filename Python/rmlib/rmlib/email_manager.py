import smtplib
from email.message import EmailMessage


class EmailManager:
    """Class for smtp email logging and sending emails
    """

    def __init__(self, email, password, stmp_server, port):
        self.email = email
        self.password = password
        self.stmp_server = stmp_server
        self.port = port
        self.gmail_server = None

    @staticmethod
    def init_from_settings(setting_section):
        return EmailManager(setting_section['email'], setting_section['password'], setting_section['server'], setting_section['port'])

    def __login(self):
        self.gmail_server = smtplib.SMTP_SSL(self.stmp_server, self.port)
        self.gmail_server.login(self.email, self.password)
        self.gmail_server.ehlo()

    def __logout(self):
        self.gmail_server.quit()

    @staticmethod
    def format_email_body(sent_from: str, to: str, subject: str, msg: str) -> str:
        return """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, msg)

    def send_email(self, to: str, subject: str, msg: str):
        self.__login()
        self.gmail_server.sendmail(
            self.email, to, EmailManager.format_email_body(self.email, to, subject, msg))
        self.__logout()
