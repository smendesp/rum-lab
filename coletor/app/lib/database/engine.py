from sqlalchemy import create_engine
from app.config.settings import settings


_echo = True if settings.DEBUG == True else False

engine = create_engine(
    str(settings.DATABASE_URL),
    # disable default reset-on-return scheme
    pool_reset_on_return=None,
    echo=_echo,
)

# engine = create_engine(
#     "sqlite:///teste.db"
# )
