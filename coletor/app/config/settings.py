from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from typing import Optional
from app.config.environments import Environment

# TODO: Fazer com que os arquivos .env sejam carregados de acordo com o ambiente


class Settings(BaseSettings):

    # Configurações de ambiente
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = False

    # Banco de dados
    DATABASE_URL: Optional[PostgresDsn]

    # Segurança
    SECRET_KEY: str

    # Segurança
    DB_DEFAULT_FORMAT_DATE: str

    # Open Telemetry
    # OTEL_SERVICE_NAME: str
    # OTEL_EXPORTER_OTLP_PROTOCOL: str
    # OTEL_EXPORTER_OTLP_ENDPOINT: str
    # OTEL_EXPORTER_OTLP_INSECURE: bool
    # OTEL_TRACES_EXPORTER: str
    # OTEL_METRICS_EXPORTER: str
    # OTEL_LOGS_EXPORTER: str

    # OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED: bool
    # OTEL_PYTHON_LOG_CORRELATION: str
    # #OTEL_PYTHON_LOG_FORMAT: str
    # OTEL_PYTHON_LOG_LEVEL: str

    # OTEL_BSP_SCHEDULE_DELAY: int
    # OTEL_BSP_EXPORT_TIMEOUT: int
    # OTEL_BSP_MAX_QUEUE_SIZE: int
    # OTEL_BSP_MAX_EXPORT_BATCH_SIZE: int

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()
