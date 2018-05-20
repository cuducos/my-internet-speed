from decimal import Decimal

from decouple import config
from peewee import PostgresqlDatabase
from twitter import Api


INTERVAL = config('INTERVAL', cast=lambda x: int(x) * 60)
TIMEZONE = config('TIMEZONE')

REDIS_URL = config('REDIS_URL')
DATABASE = PostgresqlDatabase(
    database=config('POSTGRES_DB'),
    user=config('POSTGRES_USER'),
    password=config('POSTGRES_PASSWORD'),
    host=config('POSTGRES_HOST'),
    port=config('POSTGRES_PORT')
)

CELERY_CONFIG = {'broker': REDIS_URL, 'timezone': TIMEZONE}

CREDENTIALS = {
    'consumer_key': config('TWITTER_CONSUMER_KEY', default=None),
    'consumer_secret': config('TWITTER_CONSUMER_SECRET', default=None),
    'access_token_key': config('TWITTER_ACCESS_TOKEN', default=None),
    'access_token_secret': config('TWITTER_ACCESS_TOKEN_SECRET', default=None)
}
TWITTER = Api(**CREDENTIALS) if all(CREDENTIALS.values()) else None
TWEET = config('TWEET')
CONTRACT_SPEED = config('CONTRACT_SPEED', cast=lambda x: int(x) * 10 ** 6)
MINIMUM_SPEED = config('THRESHOLD', cast=lambda x: Decimal(x) * CONTRACT_SPEED)
