import re

from speedtest import Speedtest

from my_internet_speed.backends import SpeedTestBase
from my_internet_speed.models import Result


class SpeedTest(SpeedTestBase):
    def run(self):
        self.client = Speedtest()
        self.client.get_best_server()
        self.client.download()
        self.client.upload()

        result = self.client.results.dict()
        fields = set(Result._meta.fields)  # noqa
        data = {key: value for key, value in result.items() if key in fields}
        data["url"] = re.sub(r"\.png$", "", self.client.results.share())
        return Result(**data)
