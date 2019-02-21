import os
import re
from datetime import datetime
from decimal import Decimal

from requests import post
from splinter.driver.webdriver.remote import WebDriver

from my_internet_speed.backends import SpeedTestBase
from my_internet_speed.models import Result
from my_internet_speed.settings import IMGUR_CLIENT_ID, SELENIUM_DRIVE_URL


class SpeedTest(SpeedTestBase):
    def __init__(self):
        self.browser = WebDriver(browser="chrome", url=SELENIUM_DRIVE_URL)
        self._divs = None

    @property
    def divs(self):
        if not self._divs:
            result = self.browser.find_by_id("medicao")
            divs = (div.text.strip() for div in result.find_by_tag("div"))
            self._divs = tuple(div for div in divs if div)

        return self._divs

    def parse_timestamp_and_server(self):
        pattern = (
            r"(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4}) "
            r"(?P<hour>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2})"
        )
        groups = ("year", "month", "day", "hour", "minutes", "seconds")
        for server, timestamp in zip(self.divs, self.divs[1:]):
            match = re.match(pattern, timestamp)
            if match:
                args = (int(match.group(group)) for group in groups)
                return server, datetime(*args)

    def upload_screenshot(self):
        if not IMGUR_CLIENT_ID:
            return

        filename = self.browser.screenshot(full=True)
        url = "https://api.imgur.com/3/image"
        headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
        with open(filename, "rb") as fobj:
            files = {"image": fobj}
            response = post(url, files=files, headers=headers).json()

        os.remove(filename)
        return response["data"]["link"]

    @staticmethod
    def mbps(value):
        return Decimal(value) * 10 ** 6

    @property
    def data(self):
        labels = {
            "Download",
            "Upload",
            "Latência",
            "Jitter",
            "Perda",
            "IP",
            "Região Servidor",
            "Região Teste",
        }
        data = {k: v for k, v in zip(self.divs, self.divs[1:]) if k in labels}
        server, timestamp = self.parse_timestamp_and_server()

        return {
            "download": self.mbps(data["Download"]),
            "upload": self.mbps(data["Upload"]),
            "timestamp": timestamp,
            "ping": data.get("Latência").replace(" ms", ""),
            "server": {
                "name": server,
                "region": data.get("Região Servidor"),
                "jitter": data.get("Jitter"),
                "loss": data.get("Perda"),
            },
            "client": {"ip": data.get("IP"), "region": data.get("Região Teste")},
            "url": self.upload_screenshot(),
        }

    def run(self):
        self.browser.visit("http://www.brasilbandalarga.com.br/bbl")
        self.browser.is_element_present_by_id("btnIniciar", wait_time=60)
        self.browser.find_by_id("btnIniciar").first.click()
        self.browser.is_text_present("Teste Finalizado", wait_time=300)
        return Result(**self.data)
