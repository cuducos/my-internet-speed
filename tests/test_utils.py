from my_internet_speed.utils import format_percentage, format_speed


def test_format_percentage():
    assert '314%' == format_percentage(3.1415)


def test_format_speed():
    assert '23Mbps' == format_speed(22705960.903082576)
