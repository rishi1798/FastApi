from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote

password = "satish@123"
encoded_password = quote(password, safe="")

# SQLALCHEMY_DATABASE_URL = 'mysql://username:password@14.41.50.12/dbname'

DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@127.0.0.1/test_db"


# engine is responsible for establishing the connection
engine = create_engine(DATABASE_URL, echo=True)   
# connection = engine.connect()

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

# Dependency and get_db function is used to manage database session
# SessionLocal is used to create a local data base session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()