from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Date, types, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

# ENGINE = None
# Session = None

engine = create_engine('postgresql://localhost/papersdb')
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


class Paper(Base):
    __tablename__ = "Papers"

    id = Column(Integer, primary_key = True)
    pubmed_id = Column(String(16))
    title = Column(Text)
    authors = Column(Text)
    

class Sentences(Base):
    __tablename__ = "Sentences"

    id = Column(Integer, primary_key = True)
    paper_id = Column(Integer)
    sentence = Column(Text)
    sentence_order = Column(Integer)
    parsed_sentence = Column(Text, nullable = True)

    #paper = relationship("Paper", backref=backref("Sentences", order_by = id))




def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
