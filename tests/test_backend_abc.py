from unittest.mock import Mock

from my_internet_speed.backends import SpeedTestBase, format_percentage, format_speed
from my_internet_speed.models import Result


class SpeedTest(SpeedTestBase):
    def run(self):
        return Result(
            download=23_000_000,
            upload=2_300_000,
            timestamp="1970-01-01T00:00:00.000000Z",
            url="http://imgur.com/42",
        )


def test_format_percentage():
    assert "314%" == format_percentage(3.1415)


def test_format_speed():
    assert "23Mbps" == format_speed(22_705_960.903_082_576)


def test_tweet_text(mocker):
    configs = {
        "MINIMUM_SPEED": (60 * 10 ** 6) * 0.4,
        "CONTRACT_SPEED": 60 * 10 ** 6,
        "TWEET": (
            "I pay for {contract_speed}, but now @MyISP is working at "
            "{real_speed} – merely {percentage} of what I'm paying for :( "
            "{result_url}"
        ),
    }
    for key, value in configs.items():
        mocker.patch(f"my_internet_speed.settings.{key}", new_callable=lambda: value)

    expected = (
        "I pay for 60Mbps, but now @MyISP is working at 23Mbps – merely 38% "
        "of what I'm paying for :( http://imgur.com/42"
    )
    speed_test = SpeedTest()
    result = speed_test.run()
    assert speed_test.tweet_text(result) == expected


def test_it_does_not_tweet_when_there_is_no_credentials(mocker):
    mocker.patch("my_internet_speed.settings.TWITTER", new_callable=lambda: None)
    speed_test = SpeedTest()
    result = speed_test.run()
    assert speed_test.tweet(result) is None


def test_it_tweets_when_speed_is_below_limit(mocker, speedtestnet):
    minimum = lambda: 25 * 10 ** 6
    mocker.patch("my_internet_speed.settings.MINIMUM_SPEED", new_callable=minimum)
    twitter = mocker.patch("my_internet_speed.settings.TWITTER")

    speed_test = SpeedTest()
    results = speed_test.run()
    speed_test.tweet(results)
    twitter.PostUpdate.assert_called_once_with(speed_test.tweet_text(results))


def test_does_not_tweet_when_speed_is_above_limit(mocker, speedtestnet):
    minimum = lambda: 20 * 10 ** 6
    mocker.patch("my_internet_speed.settings.MINIMUM_SPEED", new_callable=minimum)
    twitter = mocker.patch("my_internet_speed.settings.TWITTER")

    speed_test = SpeedTest()
    result = speed_test.run()
    speed_test.tweet(result)
    twitter.PostUpdate.assert_not_called()


def test_call(mocker):
    run = mocker.patch.object(SpeedTest, "run")
    tweet = mocker.patch.object(SpeedTest, "tweet")
    result = Mock()
    run.return_value = result

    speed_test = SpeedTest()
    speed_test()
    run.assert_called_once_with()
    result.create.assert_called_once_with()
    tweet.assert_called_once_with(result)
