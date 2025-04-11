from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime

class User(Base):
    __tablename__ = 'users'

    id= Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True )
    hashed_password = Column(String, nullable=False )
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    notes=relationship('Notes', back_populates='owner', lazy='select')


class Notes(Base):
    __tablename__ = 'notes'

    id= Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id= Column(Integer, ForeignKey('users.id'))
    owner= relationship('User', back_populates='notes', lazy='select')

