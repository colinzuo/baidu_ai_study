import requests
import logging


class BaseSdk:
    def __init__(self, api_key=None, secret_key=None):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key
        self.secret_key = secret_key
        self.token = None

    def get_token(self):
        get_token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
            'client_id=%s&client_secret=%s' % (self.api_key, self.secret_key)
        get_token_headers = {'Content-Type': "application/json; charset=UTF-8"}

        get_token_ok = False

        try:
            r = requests.post(get_token_url, headers=get_token_headers, timeout=3)

            if 200 <= r.status_code < 300:
                call_rsp = r.json()
                self.logger.info("get_token: response, %s" % (r.text,))
                self.token = call_rsp['access_token']

                get_token_ok = True
        except Exception as e:
            self.logger.error("get_token: error, %s" % (str(e)))

        if get_token_ok:
            self.logger.info("get_token Successful, token: %s" % (self.token,))
        else:
            if r is not None:
                self.logger.error("get_token failure response, %s" % (r.text,))
            self.logger.error("get_token Failed")

        return get_token_ok
