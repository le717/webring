# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, String

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
