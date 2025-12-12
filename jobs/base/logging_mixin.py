import logging

class LoggingMixin:
    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(self.__class__.__name__)
