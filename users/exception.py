class GithubException(Exception):
    pass


class KakaoException(Exception):
    pass


class LoggedInOnlyView(Exception):
    pass


class LoggedOutOnlyView(Exception):
    pass


class ChangePasswordException(Exception):
    pass


class VerifyUser(Exception):
    pass

class EmailLoggedInOnly(Exception):
    pass
