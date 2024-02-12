from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

# from sqlalchemy.orm import declarative_base

# Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String(255),nullable=False)
    content = Column(String(255),nullable=False)
    published = Column(Boolean,server_default='1',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default= text('now()'))
    owner_id  = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False) 
    
    owner = relationship("User")
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String(50),nullable=False,unique=True)
    password = Column(String(250),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default= text('now()'))
    