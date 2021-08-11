# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String


db = SQLAlchemy()


__all__ = ["WebLink"]


class WebLink(db.Model):
    __tablename__ = "weblinks"

    id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    rotted = Column(String)
    date_added = Column(DateTime)


class RottedLinks(db.Model):
    __tablename__ = "rotted_links"

    id = Column(String, primary_key=True)
    times_failed = Column(Integer)
