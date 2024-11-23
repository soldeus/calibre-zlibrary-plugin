"""
simple zlibrary api to be used with calibre-zlibrary-plugin


og ref: https://github.com/bipinkrish/Zlibrary-API/
"""

from urllib.parse import urlencode
import json


class ZLibrary:
    def __init__(
        self,
        browser,
        email: str = None,
        password: str = None,
        remix_userid: [int, str] = None,
        remix_userkey: str = None,
    ):
        self.browser = browser
        self.email: str
        self.name: str
        self.remix_userid: [int, str]
        self.remix_userkey: str
        self.domain = "https://1lib.sk"

        self.loggedin = False
        self.browser.set_header('User-Agent', "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
        self.browser.set_handle_robots(False)

        if email is not None and password is not None:
            self.loginWithEmail(email, password)
        elif remix_userid is not None and remix_userkey is not None:
            self.loginWithToken(remix_userid, remix_userkey)


    # login --------

    def loginWithEmail(self, email: str, password: str):
        return self.login(email, password)

    '''
    def loginWithToken(
        self, remix_userid: [int, str], remix_userkey: str
    ) -> dict[str, str]:
        return self.__checkIDandKey(remix_userid, remix_userkey)
    '''

    def login(self, email, password):
        return self.setValues(
            self.post(
                "/eapi/user/login",
                data=urlencode({
                    "email": email,
                    "password": password,
                }),
            )
        )

    def setValues(self, response):
        if not response["success"]:
            return response

        self.email = response["user"]["email"]
        self.name = response["user"]["name"]
        self.remix_userid = str(response["user"]["id"])
        self.remix_userkey = response["user"]["remix_userkey"]
        self.loggedin = True

        self.browser.set_simple_cookie("remix_userid", self.remix_userid, 'singlelogin.re')
        self.browser.set_simple_cookie("remix_userkey", self.remix_userkey, 'singlelogin.re')
        
        return response

    # --------


    # search --------
    
    def search(
        self,
        message: str = None,
        yearFrom: int = None,
        yearTo: int = None,
        languages: str = None,
        extensions: [str] = None,
        order: str = None,
        page: int = None,
        limit: int = None,
    ):
        return self.post(
            "/eapi/book/search",
            urlencode({
                k: v
                for k, v in {
                    "message": message,
                    "yearFrom": yearFrom,
                    "yearTo": yearTo,
                    "languages": languages,
                    "extensions[]": extensions,
                    "order": order,
                    "page": page,
                    "limit": limit,
                }.items()
                if v is not None
            }),
        )


    # mechanize --------

    def post(self, url: str, data=None, override=False) -> dict[str, str]:
        #if not self.loggedin and override is False:
        #    print("Not logged in")
        #    return

        res = self.browser.open(
            self.domain + url,
            data,
        ).read().decode('utf8')

        return json.loads(res)

    def get(self, url: str, data=None, cookies=None) -> dict[str, str]:
        if not self.loggedin and cookies is None:
            print("Not logged in")
            return

        res = self.browser.open(
            self.domain + url,
            data,
        ).read().decode("utf-8")
        
        return json.loads(res)
