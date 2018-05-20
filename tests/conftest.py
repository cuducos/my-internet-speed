import pytest

from my_internet_speed import SpeedTest


class SpeedTestResult:

    def __init__(self):
        self.download = 22705960.903082576
        self.upload = 6743478.793460394
        self.ping = 21.134
        self.timestamp = '1970-01-01T00:00:00.000000Z'
        self.bytes_sent = 11255808
        self.bytes_received = 28753668
        self.server = {
            'url': 'http://example.com/speedtest/upload.php',
            'lat': '-34.0098',
            'lon': '-56.6573',
            'name': 'Nowhere',
            'country': 'Earth',
            'cc': 'XX',
            'sponsor': 'Example Inc.',
            'id': '42',
            'url2': 'http://alt.example.com/speedtest/upload.php',
            'host': 'example.com:8001',
            'd': 3.1415926535897932,
            'latency': 31.415
        }
        self.client = {
            'ip': '192.168.0.1',
            'lat': '-36.4679',
            'lon': '-39.3789',
            'isp': 'Live, universe and everything',
            'isprating': '4.2',
            'rating': '0',
            'ispdlavg': '0',
            'ispulavg': '0',
            'loggedin': '0',
            'country': 'XX'
        }

    def share(self):
        return f'http://www.speedtest.net/result/42.png'

    def dict(self):
        return dict(
            download=self.download,
            upload=self.upload,
            ping=self.ping,
            timestamp=self.timestamp,
            bytes_sent=self.bytes_sent,
            bytes_received=self.bytes_received,
            server=self.server,
            client=self.client
        )


@pytest.fixture
def speed_test(mocker):
    mock = mocker.patch('my_internet_speed.Speedtest')
    mock.return_value.results = SpeedTestResult()
    return SpeedTest()
