import logging
import logging.config
from app.config.settings import settings


class Logger:

    # _instance = None
    _formater = '%(levelname)s- %(asctime)s - %(name)s - %(message)s'
    _level = logging.ERROR if settings.DEBUG == False else logging.INFO

    def __init__(self):

        LOGGING_CONFIG = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {'format': self._formater},
            },
            'handlers': {
                'default': {
                    'level': self._level,
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',  # Default is stderr
                },
            },
            'loggers': {
                '': {
                    'level': self._level,
                    'handlers': ['default'],
                },  # root logger
                'uvicorn.error': {
                    'level': self._level,
                    'handlers': ['default'],
                    #'propagate': False,
                },
                'uvicorn.access': {
                    'level': self._level,
                    'handlers': ['default'],
                },
            },
        }

        # logging.config.dictConfig(LOGGING_CONFIG)

        handler = logging.StreamHandler()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self._level)
        self.logger.addHandler(handler)

        # logging.basicConfig(level=self._level, format=self._formater)
