from my_internet_speed.models import Result


def test_init(speed_test):
    speed_test.client.get_best_server.assert_called_once_with()
    speed_test.client.download.assert_called_once_with()
    speed_test.client.upload.assert_called_once_with()
    assert speed_test.result_url == 'http://www.speedtest.net/result/42'


def test_save(mocker, speed_test):
    create = mocker.patch.object(Result, 'create')
    speed_test.save()
    data = {
        'download': speed_test.client.results.download,
        'upload': speed_test.client.results.upload,
        'ping': speed_test.client.results.ping,
        'timestamp': speed_test.client.results.timestamp,
        'bytes_sent': speed_test.client.results.bytes_sent,
        'bytes_received': speed_test.client.results.bytes_received,
        'server': speed_test.client.results.server,
        'client': speed_test.client.results.client,
    }
    create.assert_called_once_with(**data)


def test_tweet_text(mocker, speed_test):
    tweet = (
        'I pay for {contract_speed}, but now @MyISP is working at '
        "{real_speed} – merely {percentage} of what I'm paying for :( "
        '{result_url}'
    )
    expected = (
        'I pay for 60Mbps, but now @MyISP is working at 23Mbps – merely 38% '
        "of what I'm paying for :( http://www.speedtest.net/result/42"
    )
    mocker.patch('my_internet_speed.settings.TWEET', new_callable=lambda: tweet)
    assert speed_test.tweet_text == expected


def test_it_tweets_when_speed_is_below_limit(mocker, speed_test):
    minimum_speed = lambda: 25 * 10 ** 6
    mocker.patch('my_internet_speed.settings.MINIMUM_SPEED', new_callable=minimum_speed)
    twitter = mocker.patch('my_internet_speed.settings.TWITTER')
    speed_test.tweet()
    twitter.PostUpdate.assert_called_once_with(speed_test.tweet_text)


def test_does_not_tweet_when_speed_is_above_limit(mocker, speed_test):
    minimum_speed = lambda: 20 * 10 ** 6
    mocker.patch('my_internet_speed.settings.MINIMUM_SPEED', new_callable=minimum_speed)
    twitter = mocker.patch('my_internet_speed.settings.TWITTER')
    speed_test.tweet()
    twitter.PostUpdate.assert_not_called()
