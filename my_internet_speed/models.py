from peewee import CharField, DateTimeField, DecimalField, IntegerField, Model
from playhouse.postgres_ext import JSONField

from my_internet_speed.settings import DATABASE


class Result(Model):
    download = DecimalField(index=True, max_digits=20, decimal_places=10)
    upload = DecimalField(index=True, max_digits=20, decimal_places=10)
    timestamp = DateTimeField(index=True)
    ping = DecimalField(index=True, max_digits=10, decimal_places=5, null=True)
    bytes_sent = IntegerField(null=True)
    bytes_received = IntegerField(null=True)
    server = JSONField(null=True)
    client = JSONField(null=True)
    url = CharField(max_length=64, null=True)

    class Meta:
        database = DATABASE
