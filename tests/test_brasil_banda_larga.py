from datetime import datetime
from decimal import Decimal
from unittest.mock import PropertyMock, mock_open

import pytest

from my_internet_speed.backends.brasil_banda_larga import SpeedTest
from my_internet_speed.models import Result


@pytest.fixture
def brasil_banda_larga(mocker):
    browser = mocker.patch("my_internet_speed.backends.brasil_banda_larga.WebDriver")
    browser.return_value.screenshot.return_value = "/tmp/screenshot.png"
    divs = mocker.patch.object(SpeedTest, "divs", new_callable=PropertyMock)
    divs.return_value = (
        "CLARO",
        "20/02/2019 18:24:46",
        "Download",
        "37.26",
        "Mbps",
        "Upload",
        "1.96",
        "Mbps",
        "Latência",
        "12 ms",
        "Jitter",
        "5 ms",
        "Perda",
        "0 %",
        "IP",
        "12.34.56.78",
        "Região Servidor",
        "Claro - São Paulo",
        "Região Teste",
        "Sao Paulo",
    )
    return SpeedTest()


def test_parse_timestamp_and_server(brasil_banda_larga):
    expected = "CLARO", datetime(2019, 2, 20, 18, 24, 46)
    assert brasil_banda_larga.parse_timestamp_and_server() == expected


def test_it_does_not_upload_to_imgur_if_not_configured(mocker, brasil_banda_larga):
    post = mocker.patch("my_internet_speed.backends.brasil_banda_larga.post")
    os = mocker.patch("my_internet_speed.backends.brasil_banda_larga.os")
    mocker.patch(
        "my_internet_speed.backends.brasil_banda_larga.IMGUR_CLIENT_ID",
        new_callable=lambda: None,
    )

    assert brasil_banda_larga.upload_screenshot() is None
    brasil_banda_larga.browser.screenshot.assert_not_called()
    post.assert_not_called()
    os.remove.assert_not_called()


def test_it_does_upload_to_imgur_if_configured(mocker, brasil_banda_larga):
    mocked_open = mocker.patch("my_internet_speed.backends.brasil_banda_larga.open")
    mocked_open.return_value.__enter__.return_value = b"my-speed-test-result"
    post = mocker.patch("my_internet_speed.backends.brasil_banda_larga.post")
    post.return_value.json.return_value = {"data": {"link": 42}}
    os = mocker.patch("my_internet_speed.backends.brasil_banda_larga.os")
    mocker.patch(
        "my_internet_speed.backends.brasil_banda_larga.IMGUR_CLIENT_ID",
        new_callable=lambda: "my-client-id",
    )

    filename = brasil_banda_larga.upload_screenshot()
    assert filename is not None
    brasil_banda_larga.browser.screenshot.assert_called_once_with(full=True)
    post.assert_called_once_with(
        "https://api.imgur.com/3/image",
        files={"image": b"my-speed-test-result"},
        headers={"Authorization": "Client-ID my-client-id"},
    )
    os.remove.assert_called_once_with("/tmp/screenshot.png")


def test_mbps(brasil_banda_larga):
    assert Decimal("37260000") == brasil_banda_larga.mbps("37.26")


def test_data(mocker, brasil_banda_larga):
    mocker.patch(
        "my_internet_speed.backends.brasil_banda_larga.IMGUR_CLIENT_ID",
        new_callable=lambda: None,
    )
    assert brasil_banda_larga.data == {
        "client": {"ip": "12.34.56.78", "region": "Sao Paulo"},
        "download": Decimal("37260000.00"),
        "ping": "12",
        "server": {
            "jitter": "5 ms",
            "loss": "0 %",
            "name": "CLARO",
            "region": "Claro - São Paulo",
        },
        "timestamp": datetime(2019, 2, 20, 18, 24, 46),
        "upload": Decimal("1960000.00"),
        "url": None,
    }


def test_run(mocker, brasil_banda_larga):
    mocker.patch(
        "my_internet_speed.backends.brasil_banda_larga.IMGUR_CLIENT_ID",
        new_callable=lambda: None,
    )
    result = brasil_banda_larga.run()
    brasil_banda_larga.browser.visit.assert_called_once_with(
        "http://www.brasilbandalarga.com.br/bbl"
    )
    brasil_banda_larga.browser.is_element_present_by_id.assert_called_once_with(
        "btnIniciar", wait_time=60
    )
    brasil_banda_larga.browser.find_by_id.assert_called_once_with("btnIniciar")
    brasil_banda_larga.browser.is_text_present.assert_called_once_with(
        "Teste Finalizado", wait_time=300
    )
    assert isinstance(result, Result)
