import re

from celery import Celery
from speedtest import Speedtest

from my_internet_speed.models import Result
from my_internet_speed import settings
from my_internet_speed.utils import format_percentage, format_speed


class SpeedTest:

    def __init__(self):
        self.client = Speedtest()
        self.client.get_best_server()
        self.client.download()
        self.client.upload()
        self.result_url = re.sub(r'\.png$', '', self.client.results.share())

    def save(self):
        result = self.client.results.dict()
        fields = set(Result._meta.fields)  # noqa
        data = {key: value for key, value in result.items() if key in fields}
        return Result.create(**data)

    def tweet(self):
        if not TWITTER or \
                self.client.results.download >= settings.MINIMUM_SPEED:
            return

        return settings.TWITTER.PostUpdate(self.tweet_text)

    @property
    def tweet_text(self):
        percentage = self.client.results.download / settings.CONTRACT_SPEED
        return settings.TWEET.format(
            contract_speed=format_speed(settings.CONTRACT_SPEED),
            real_speed=format_speed(self.client.results.download),
            percentage=format_percentage(percentage),
            result_url=self.result_url
        )


app = Celery('my-internet-speed', **settings.CELERY_CONFIG)


@app.task
def speed_test():
    obj = SpeedTest()
    obj.tweet()
    return obj.save()


@app.on_after_finalize.connect
def setup_scheduled_task(sender, **kwargs):
    task = speed_test.s()
    sender.add_periodic_task(settings.INTERVAL, task, name='speed-test')
