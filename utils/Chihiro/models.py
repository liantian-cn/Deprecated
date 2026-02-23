__all__ = ["db", "VMESSServer"]

from peewee import *
import datetime
import uuid

db = SqliteDatabase('database.db')


class VMESSServer(Model):
    uuid = CharField(default=uuid.uuid4)
    active = BooleanField(default=True)

    add = CharField(default="**add**")
    aid = IntegerField(default=100)
    host = CharField(null=True)
    id = CharField(null=True)
    net = CharField(null=True)
    path = CharField(null=True)
    port = CharField(default="**port**")
    ps = CharField(null=True)
    tls = CharField(null=True)
    type = CharField(null=True)
    v = CharField(null=True)

    latest_tests = DateTimeField(default=datetime.datetime.now)
    test_result = CharField(default="**timeout**")
    ep = FloatField(default=0)

    class Meta:
        primary_key = CompositeKey('add', 'port')
        database = db
