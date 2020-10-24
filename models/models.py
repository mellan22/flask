from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime


class OsechiWishes(Base):
    __tablename__ = 'osechiwishes'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True)
    wish = Column(Text)
    image = Column(String(128), unique=True)
    question = Column(String(128))
    want = Column(Integer)

    def __init__(self, name=None, wish=None, image=None, question=None, want=0):
        self.name = name
        self.wish = wish
        self.image = image
        self.question = question
        self.want = want

    # def __str__(self):
    #     return '{id:%r ,question: }' % (self.question, self.want)

    # def __repr__(self):
    #     return '<Name %r>' % (self.name)
