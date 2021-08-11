from marshmallow import Schema


class OrderedSchema(Schema):
    class Meta:
        ordered = True


from .AuthKey import *
from .BitRot import *
from .Empty import Empty
from .HttpError import HttpError
from .WebLink import *
