class YahooFFException(Exception):
    pass


class PrivateLeagueException(YahooFFException):
    pass


class InvalidLeagueException(YahooFFException):
    pass


class UnknownLeagueException(YahooFFException):
    pass
