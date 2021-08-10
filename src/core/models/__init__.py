from marshmallow import Schema


class OrderedSchema(Schema):
    class Meta:
        ordered = True


from .Empty import Empty
from .HttpError import HttpError
