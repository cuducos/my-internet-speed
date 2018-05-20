from unittest.mock import Mock

from my_internet_speed import setup_scheduled_task, speed_test


def test_speed_test_task(mocker):
    speed_test_mock = mocker.patch('my_internet_speed.SpeedTest')
    speed_test()
    speed_test_mock.assert_called_once_with()
    speed_test_mock.return_value.tweet.assert_called_once_with()
    speed_test_mock.return_value.save.assert_called_once_with()


def test_setup_scheduled_task(mocker):
    mocker.patch('my_internet_speed.settings.INTERVAL', new_callable=lambda: 5)
    speed_test_mock = mocker.patch('my_internet_speed.speed_test')
    sender_mock = Mock()

    setup_scheduled_task(sender_mock)
    speed_test_mock.s.assert_called_once_with()
    sender_mock.add_periodic_task.assert_called_once_with(
        5, speed_test_mock.s.return_value,
        name='speed-test'
    )

