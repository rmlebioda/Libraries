import os
from datetime import datetime
from pathlib import Path
import traceback


class Logger:
    """Class for generating log files
    """

    def __init__(self, name: [str], *, use_date_prefix=True, print_logs=True, write_logs=True, log_dir=None, log_filename='%Y-%m-%d'):
        """Initializes Logger class with given arguments

        Args:
            name (list(str)): Application name (for nested logs, read from left/first to right/last)
            use_date_prefix (bool, optional): Whenever logger should add date prefix to logs. Defaults to True.
            print_logs (bool, optional): Whenever logger should print log to standard output. Defaults to True.
            write_logs (bool, optional): Whenever logger should log to destined file. Defaults to True.
            log_dir (str, optional): Directory path for log file. Defaults to None.
            log_filename (str, optional): Filename for log path, should comply datetime.strftime function requirements. Defaults to '%Y-%m-%d'.

        Raises:
            ValueError: When write_logs is set to True and log_filename or log_dir is not set
        """
        if write_logs == True and (log_filename == None or log_dir == None):
            raise ValueError(
                "Wrong arguments, log_filename and log_dir cannot be None when write_logs is True")
        if isinstance(name, list):
            self.application_name = os.sep.join(name)
        else:
            self.application_name = name
        self.print_logs = print_logs
        self.write_logs = write_logs
        self.use_date_prefix = use_date_prefix
        self.log_dir = log_dir
        self.log_filename = log_filename

    def __log_path(self):
        return os.path.join(self.log_dir, 'logs', self.application_name, datetime.today().strftime(self.log_filename) + '.txt')

    def __log_prefix(self):
        return str(datetime.now()) if self.use_date_prefix else ''

    def __full_prefix(self):
        return f'[{self.__log_prefix()}][{self.application_name}] '

    def message(self, msg=None, *, write_to_console=None, console_add_prefix=True, write_to_log=None, log_add_prefix=True) -> str:
        """Logs desired message

        Args:
            msg (str, optional): Message to be logged. Defaults to None.
            write_to_console (bool, optional): Whenever message should be printed to console. When not None, overrides default setting from __init__. Defaults to None.
            console_add_prefix (bool, optional): Whenever prefix should be added to log. When not None, overrides default setting from __init__. Defaults to True.
            write_to_log (bool, optional): Whenever message should be logged to file. When not None, overrides default setting from __init__. Defaults to None.
            log_add_prefix (bool, optional): Whenever should add prefix to message log. When not None, overrides default setting from __init__. Defaults to True.

        Returns:
            (str): Message like it would be printed on console
        """
        if write_to_console or (write_to_console == None and self.print_logs):
            print((self.__full_prefix() if console_add_prefix else '') +
                  ('' if msg == None else msg))
        if write_to_log == True or (write_to_log == None and self.write_logs):
            Path(self.__log_path()).parent.mkdir(parents=True, exist_ok=True)
            with open(self.__log_path(), 'a', encoding='UTF8') as fdesc:
                fdesc.write((self.__full_prefix() if log_add_prefix else '') +
                            ('' if msg == None else msg) + '\n')
        return (self.__full_prefix() if console_add_prefix else '') + ('' if msg == None else msg)
