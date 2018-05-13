from peewee import DateTimeField, DecimalField, IntegerField, Model
from playhouse.postgres_ext import JSONField

from my_internet_speed.settings import DATABASE


class Result(Model):
    download = DecimalField(index=True, max_digits=20, decimal_places=10)
    upload = DecimalField(index=True, max_digits=20, decimal_places=10)
    ping = DecimalField(index=True, max_digits=10, decimal_places=5)
    timestamp = DateTimeField(index=True)
    bytes_sent = IntegerField()
    bytes_received = IntegerField()
    server = JSONField()
    client = JSONField()

    class Meta:
        database = DATABASE
