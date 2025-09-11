from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = 'dev'
    STAGING = 'hml'   # Homologação
    PRODUCTION = 'prd'
    TESTING = 'tst'
