from celery import Celery

from my_internet_speed import backends, settings


app = Celery("my-internet-speed", **settings.CELERY_CONFIG)
SpeedTest = __import__("my_internet_speed.backends", f"{settings.BACKEND}.SpeedTest")


@app.task
def speed_test():
    speed_test = SpeedTest()
    speed_test()


@app.on_after_finalize.connect
def setup_scheduled_task(sender, **kwargs):
    task = speed_test.s()
    sender.add_periodic_task(settings.INTERVAL, task, name="speed-test")
