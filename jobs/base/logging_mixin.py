import logging, sys

class LoggingMixin:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        if not self.log.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.log.addHandler(handler)
