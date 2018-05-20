import re

from celery import Celery
from speedtest import Speedtest

from my_internet_speed.models import Result
from my_internet_speed.settings import (
    CELERY_CONFIG,
    CONTRACT_SPEED,
    INTERVAL,
    MINIMUM_SPEED,
    TWEET,
    TWITTER
)


class SpeedTest:

    def __init__(self):
        client = Speedtest()
        client.get_best_server()
        client.download()
        client.upload()
        self.result = client.results
        self.result_url = re.sub(r'\.png$', '', self.result.share())

    def save(self):
        result = self.result.dict()
        fields = set(Result._meta.fields)
        data = {key: value for key, value in result.items() if key in fields}
        return Result.create(**data)

    def tweet(self):
        if not TWITTER or self.result.download >= MINIMUM_SPEED:
            return

        return TWITTER.PostUpdate(self.text)

    @property
    def text(self):
        percentage = self.result.download / CONTRACT_SPEED
        return TWEET.format(
            contract_speed=self._format_speed(CONTRACT_SPEED),
            real_speed=self._format_speed(self.result.download),
            percentage=self._format_percentage(percentage),
            result_url=self.result_url
        )

    @staticmethod
    def _format_speed(speed):
        mbps = speed / 10 ** 6
        return str(int(mbps))

    @staticmethod
    def _format_percentage(value):
        result = value * 100
        return str(int(result))


app = Celery('my-internet-speed', **CELERY_CONFIG)


@app.task
def speed_test():
    obj = SpeedTest()
    obj.tweet()
    return obj.save()


@app.on_after_finalize.connect
def setup_scheduled_task(sender, **kwargs):
    sender.add_periodic_task(INTERVAL, speed_test.s(), name='speed-test')
