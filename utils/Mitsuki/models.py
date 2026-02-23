__all__ = ["db", "SSRServer"]

from peewee import *
import datetime
import uuid

db = SqliteDatabase('database.db')


class SSRServer(Model):
    uuid = CharField(default=uuid.uuid4)
    active = BooleanField(default=True)

    server_addr = CharField()
    server_port = IntegerField()
    protocol = CharField(default="**protocol**")
    method = CharField(default="**method**")
    obfs = CharField(default="**obfs**")
    password = CharField(default="**password**")
    obfsparam = CharField(default="**obfsparam**")
    protocolparam = CharField(default="**protocolparam**")
    name = CharField(default="**name**")

    latest_tests = DateTimeField(default=datetime.datetime.now)
    test_result = CharField(default="**timeout**")
    ep = FloatField(default=0)

    class Meta:
        primary_key = CompositeKey('server_addr', 'server_port')
        database = db
