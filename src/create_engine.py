from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from helpers.creds import Creds

engine = create_engine(Creds.MYSQL_HOST)
connection = engine.connect()

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
