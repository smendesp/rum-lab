from sqlalchemy.orm import sessionmaker

from app.lib.database.engine import engine

Session = sessionmaker(bind=engine)
session = Session()
