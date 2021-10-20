# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String


db = SQLAlchemy()


__all__ = ["WebLink"]


class WebLink(db.Model):
    __tablename__ = "weblinks"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    url = Column(String, nullable=False)
    date_added = Column(DateTime, nullable=False)
    is_dead = Column(Integer, nullable=False, server_default="0")
    is_web_archive = Column(Integer, nullable=False, server_default="0")


class RottedLinks(db.Model):
    __tablename__ = "rotted_links"

    id = Column(String, primary_key=True)
    times_failed = Column(Integer, nullable=False)
