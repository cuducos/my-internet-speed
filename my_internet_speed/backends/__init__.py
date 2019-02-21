from abc import ABCMeta, abstractmethod

from my_internet_speed import settings


def format_speed(speed):
    """Formats an internet speed as a humam readable string
    :param speed: (float) connection speed in bps
    :return: (str) speed in Mpbs
    """
    return f"{speed / 10 ** 6:.0f}Mbps"


def format_percentage(percentage):
    """Formats a percentage into a string
    :param value: (float) percentage
    :return: (str) Human-readable rounded percentage (no decimals)
    """
    return f"{percentage * 100:.0f}%"


class SpeedTestBase(metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        """Runs the speed test and sets self.results as Result instance"""

    def tweet_text(self, results):
        percentage = results.download / settings.CONTRACT_SPEED
        return settings.TWEET.format(
            contract_speed=format_speed(settings.CONTRACT_SPEED),
            real_speed=format_speed(results.download),
            percentage=format_percentage(percentage),
            result_url=results.url,
        )

    def tweet(self, results):
        if not settings.TWITTER:
            return

        if results.download >= settings.MINIMUM_SPEED:
            return

        return settings.TWITTER.PostUpdate(self.tweet_text(results))

    def __call__(self):
        results = self.run()
        results.save()
        self.tweet(results)
