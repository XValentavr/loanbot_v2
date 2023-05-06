from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from helpers.creds import Creds

engine = create_engine(Creds.MYSQL_HOST, query_cache_size=0)
connection = engine.connect()

Session = sessionmaker(bind=engine, expire_on_commit=True)

session = Session()
