#!/usr/bin/env python3

## Imports ###
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random
import string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer)

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, index=True)
    password_hash = Column(String(256))
    authenticated = Column(Boolean, default=False)
    oauth = Column(Boolean, default=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(64),  nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'Owner ID:': self.owner_id,
        }


class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64))
    description = Column(String(256))
    cat_id = Column(Integer, ForeignKey('categories.id'))
    owner_id = Column(Integer, ForeignKey('user.id'))
    time_added = Column(DateTime)
    categories = relationship(Categories)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cat-id': self.cat_id,
            'Owner ID:': self.owner_id,
        }

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.create_all(engine)
