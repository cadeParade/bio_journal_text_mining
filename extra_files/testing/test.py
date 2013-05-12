from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Date, types
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session


db = create_engine("postgresql:///tutorial.db")
