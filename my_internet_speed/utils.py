def format_speed(speed):
    """Formats an internet speed as a humam readable string
    :param speed: (float) connection speed in bps
    :return: (str) speed in Mpbs
    """
    return f'{speed / 10 ** 6:.0f}Mbps'


def format_percentage(percentage):
    """Formats a percentage into a string
    :param value: (float) percentage
    :return: (str) Rounded percenatge (no decimals) in human-readable format
    """
    return f'{percentage * 100:.0f}%'
