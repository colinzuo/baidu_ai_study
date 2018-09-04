from baidusdk.base_sdk import *
import base64
import json
from datetime import datetime, timedelta
import time


class FaceRecognition(BaseSdk):
    def __init__(self, api_key=None, secret_key=None):
        super(FaceRecognition, self).__init__(api_key=api_key, secret_key=secret_key)
        self.logger = logging.getLogger(__name__)
        self.last_access = None

    def time_constraint(self):
        cur_time = datetime.now()
        if self.last_access is None:
            self.last_access = cur_time
            return
        time_thres = 1
        if cur_time < (self.last_access + timedelta(seconds=time_thres)):
            time.sleep((self.last_access + timedelta(seconds=time_thres) - cur_time).total_seconds())
        self.last_access = cur_time
        return

    def detect(self, image_path, face_field=None):
        self.time_constraint()

        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        request_url = request_url + "?access_token=" + self.token

        request_headers = {'Content-Type': "application/json"}

        params = {
            "image_type": "BASE64",
            "image": encoded_string
        }

        if face_field is not None:
            params["face_field"] = face_field

        request_body = json.dumps(params, sort_keys=True)

        err = None
        r = None

        try:
            self.logger.info("detect: request_url %s, image_path %s, face_field %s" %
                             (request_url, image_path, face_field))

            r = requests.post(request_url, headers=request_headers, data=request_body, timeout=3)

            if 200 <= r.status_code < 300:
                call_rsp = r.json()
                self.logger.info("detect: response, %s" % (r.text,))

                if err is None and call_rsp['error_code'] != 0:
                    err = call_rsp['error_msg']

                if err is None and call_rsp["result"]["face_num"] != 1:
                    err = "detect: face_num is %d, not equal to 1" % call_rsp["result"]["face_num"]
                    self.logger.error(err)
                if err is None:
                    left_eye = call_rsp["result"]["face_list"][0]["quality"]["occlusion"]["left_eye"]
                    if left_eye > 0.6:
                        err = "detect: left_eye is %.2f, too large" % left_eye
                        self.logger.error(err)
                if err is None:
                    right_eye = call_rsp["result"]["face_list"][0]["quality"]["occlusion"]["right_eye"]
                    if right_eye > 0.6:
                        err = "detect: right_eye is %.2f, too large" % right_eye
                        self.logger.error(err)
                if err is None:
                    nose = call_rsp["result"]["face_list"][0]["quality"]["occlusion"]["nose"]
                    if nose > 0.7:
                        err = "detect: nose is %.2f, too large" % nose
                        self.logger.error(err)
                if err is None:
                    mouth = call_rsp["result"]["face_list"][0]["quality"]["occlusion"]["mouth"]
                    if mouth > 0.7:
                        err = "detect: mouth is %.2f, too large" % mouth
                        self.logger.error(err)
                if err is None:
                    left_cheek = call_rsp["result"]["face_list"][0]["quality"]["occlusion"]["left_cheek"]
                    if left_cheek > 0.8:
                        err = "detect: left_cheek is %.2f, too large" % left_cheek
                        self.logger.error(err)
                if err is None:
                    right_cheek = call_rsp["result"]["face_list"][0]["quality"]["occlusion"]["right_cheek"]
                    if right_cheek > 0.8:
                        err = "detect: right_cheek is %.2f, too large" % right_cheek
                        self.logger.error(err)
                if err is None:
                    chin_contour = call_rsp["result"]["face_list"][0]["quality"]["occlusion"]["chin_contour"]
                    if chin_contour > 0.6:
                        err = "detect: chin_contour is %.2f, too large" % chin_contour
                        self.logger.error(err)
                if err is None:
                    blur = call_rsp["result"]["face_list"][0]["quality"]["blur"]
                    if blur > 0.7:
                        err = "detect: blur is %.2f, too large" % blur
                        self.logger.error(err)
                if err is None:
                    illumination = call_rsp["result"]["face_list"][0]["quality"]["illumination"]
                    if illumination < 40:
                        err = "detect: illumination is %.2f, too little" % illumination
                        self.logger.error(err)
        except Exception as e:
            err = "detect: error, %s" % (str(e))
            self.logger.error(err)

        if err is None:
            self.logger.info("detect Successful, image_path: %s" % (image_path,))
        else:
            if r is not None:
                self.logger.error("detect failure response, image_path: %s, rsp: %s" % (image_path, r.text,))
            self.logger.error("detect Failed")

        return err

    def search(self, image_path, group_id_list):
        self.time_constraint()

        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
        request_url = request_url + "?access_token=" + self.token

        request_headers = {'Content-Type': "application/json"}

        params = {
            "image_type": "BASE64",
            "image": encoded_string,
            "group_id_list": group_id_list
        }

        request_body = json.dumps(params, sort_keys=True)

        err = None
        user_rec = None
        r = None

        try:
            self.logger.info("search: request_url %s, image_path %s, group_id_list %s" %
                             (request_url, image_path, group_id_list))

            r = requests.post(request_url, headers=request_headers, data=request_body, timeout=3)

            if 200 <= r.status_code < 300:
                call_rsp = r.json()
                self.logger.info("search: response, %s" % (r.text,))
                if err is None and call_rsp['error_code'] != 0:
                    err = call_rsp['error_msg']
                if err is None:
                    score = call_rsp['result']["user_list"][0]["score"]
                    if score < 80:
                        err = "search: score is %.2f, too little" % score
                    else:
                        user_rec = call_rsp['result']["user_list"][0]
            else:
                err = "search: failure rsp: %d, %s" % (r.status_code, r.text)
        except Exception as e:
            err = "search: error, %s" % (str(e))
            self.logger.error(err)

        if err is None:
            self.logger.info("search Successful, image_path: %s, user_rec %s" % (image_path, user_rec))
        else:
            if r is not None:
                self.logger.error("search failure response, image_path: %s, rsp: %s" % (image_path, r.text,))
            self.logger.error("search Failed")

        return user_rec, err

    def faceset_user_add(self, image_path, group_id, user_id):
        self.time_constraint()

        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
        request_url = request_url + "?access_token=" + self.token

        request_headers = {'Content-Type': "application/json"}

        params = {
            "image_type": "BASE64",
            "image": encoded_string,
            "group_id": group_id,
            "user_id": user_id
        }

        request_body = json.dumps(params, sort_keys=True)

        err = None
        face_token = None
        r = None

        try:
            self.logger.info("faceset_user_add: request_url %s, image_path %s, group_id %s, user_id %s" %
                             (request_url, image_path, group_id, user_id))

            r = requests.post(request_url, headers=request_headers, data=request_body, timeout=3)

            if 200 <= r.status_code < 300:
                call_rsp = r.json()
                self.logger.info("search: response, %s" % (r.text,))
                if err is None and call_rsp['error_code'] != 0:
                    err = call_rsp['error_msg']
                if err is None:
                    face_token = call_rsp['result']["face_token"]
            else:
                err = "faceset_user_add: failure rsp: %d, %s" % (r.status_code, r.text)
        except Exception as e:
            err = "faceset_user_add: error, %s" % (str(e))
            self.logger.error(err)

        if err is None:
            self.logger.info("faceset_user_add Successful, image_path: %s, face_token %s" % (image_path, face_token))
        else:
            if r is not None:
                self.logger.error("faceset_user_add failure response, image_path: %s, rsp: %s" % (image_path, r.text,))
            self.logger.error("faceset_user_add Failed")

        return face_token, err


if __name__ == '__main__':
    from utils import helper
    import os

    helper.setup_env('../config/module_test.ini')

    helper.set_console_logger_level(logging.WARNING)

    logging.info("test begin")

    test_image_path = os.path.join("..", "data", "pics", "fanbingbing", "2.png")

    face_recognition = FaceRecognition(api_key='gBkalyAkYxNQQsDNkWZ11N9A',
                                       secret_key='i9KBk6Tmo9dVvmdG35dBE7aC5pBOcAVt')
    face_recognition.get_token()

    if False:
        face_recognition.detect(test_image_path, face_field="quality")

    if False:
        test_user_rec, test_err = face_recognition.search(test_image_path, group_id_list="1")
        logging.info("search return: user_rec: %s, err: %s" % (test_user_rec, test_err))

    if True:
        test_face_token, test_err = face_recognition.faceset_user_add(test_image_path,
                                                                      group_id="star", user_id="fanbingbing")
        logging.info("faceset_user_add return: face_token: %s, err: %s" % (test_face_token, test_err))

    logging.info("test end")
