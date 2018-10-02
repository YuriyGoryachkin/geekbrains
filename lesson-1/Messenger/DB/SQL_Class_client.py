import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'Contact'
    ContactID = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)

    def __init__(self, name):
        self.Name = name

    # def __repr__(self):
    #     return "<Contact ({})>".format(self.Name)

    # def __eq__(self, other):
    #     return self.Name == other.Name


class Message(Base):
    __tablename__ = 'Message'
    MessageID = Column(Integer, primary_key=True)
    Text = Column(String)
    Created_Datetime = Column(DateTime, default=datetime.datetime.utcnow)
    ContactID = Column(Integer, ForeignKey('Contact.ContactID'))
    Contact = relationship('Contact', back_populates='Messages')

    def __init__(self, text, contact_id, creation_datetime=None):
        self.Text = text
        self.ContactID = contact_id
        if creation_datetime:
            self.Created_Datetime = creation_datetime

    # def __repr__(self):
    #     return "<Message ({}, {})>".format(self.Text, self.ContactID)

    # def __eq__(self, other):
    #     return self.Text == other.Text and \
    #            self.Created_Datetime == other.Created_Datetime and \
    #            self.ContactID == other.ContactID


Contact.Messages = relationship('Message',
                                order_by=Message.Created_Datetime,
                                back_populates='Contact')
