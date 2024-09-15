# context_manager.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from urllib.parse import quote_plus

username = 'root'
password = 'Abcd@1234'
host = 'localhost'
dbname = 'companyServices'

# URL-encode the password
password_encoded = quote_plus(password)
DATABASE_URL = f'mysql+pymysql://{username}:{password_encoded}@{host}/{dbname}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Context:
    @staticmethod
    @contextmanager
    def fastApi():
        db = SessionLocal()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
