from my_internet_speed.models import Result


def test_run(speed_test_net):
    results = speed_test_net.run()
    expected = Result(
        download=22_705_960.903_082_576,
        upload=6_743_478.793_460_394,
        ping=21.134,
        timestamp="1970-01-01T00:00:00.000000Z",
        bytes_sent=11_255_808,
        bytes_received=28_753_668,
        server={
            "url": "http://example.com/speedtest/upload.php",
            "lat": "-34.0098",
            "lon": "-56.6573",
            "name": "Nowhere",
            "country": "Earth",
            "cc": "XX",
            "sponsor": "Example Inc.",
            "id": "42",
            "url2": "http://alt.example.com/speedtest/upload.php",
            "host": "example.com:8001",
            "d": 3.141_592_653_589_793_2,
            "latency": 31.415,
        },
        client={
            "ip": "192.168.0.1",
            "lat": "-36.4679",
            "lon": "-39.3789",
            "isp": "Live, universe and everything",
            "isprating": "4.2",
            "rating": "0",
            "ispdlavg": "0",
            "ispulavg": "0",
            "loggedin": "0",
            "country": "XX",
        },
        url="http://www.speedtest.net/result/42",
    )

    speed_test_net.client.get_best_server.assert_called_once_with()
    speed_test_net.client.download.assert_called_once_with()
    speed_test_net.client.upload.assert_called_once_with()
    for field in Result._meta.fields.keys():
        assert getattr(expected, field) == getattr(results, field)
