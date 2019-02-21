from importlib import import_module

from celery import Celery

from my_internet_speed import settings


app = Celery("my-internet-speed", **settings.CELERY_CONFIG)
backend = import_module(f"my_internet_speed.backends.{settings.BACKEND}")


@app.task
def speed_test():
    speed_test = backend.SpeedTest()
    speed_test()


@app.on_after_finalize.connect
def setup_scheduled_task(sender, **kwargs):
    task = speed_test.s()
    sender.add_periodic_task(settings.INTERVAL, task, name="speed-test")
