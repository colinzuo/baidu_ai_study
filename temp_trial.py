import logging
import os
from baidusdk.face_recognition import *


if __name__ == '__main__':
    from utils import helper

    helper.setup_env()

    helper.set_console_logger_level(logging.WARNING)

    config = helper.get_configparser_inst()
    api_key = config.get('face_recognition', 'api_key')
    secret_key = config.get('face_recognition', 'secret_key')

    logging.info("hello world")

    face_recognition = FaceRecognition(api_key=api_key, secret_key=secret_key)
    face_recognition.get_token()

    train_dir = os.path.join('data', 'train', 'pics')
    test_dir = os.path.join('data', 'test', 'pics')
    group_id = "star"
    group_id_list = "star"
    import_user_pics = False
    verify_user_pics = True

    if import_user_pics:
        for user_entry in os.scandir(train_dir):
            if not user_entry.is_dir():
                continue
            for pic_entry in os.scandir(user_entry.path):
                if not pic_entry.is_file():
                    continue
                face_token, err = face_recognition.faceset_user_add(pic_entry.path, group_id=group_id, user_id=user_entry.name)
                logging.info("faceset_user_add return: face_token: %s, err: %s" % (face_token, err))

    if verify_user_pics:
        for user_entry in os.scandir(test_dir):
            if not user_entry.is_dir():
                continue
            for pic_entry in os.scandir(user_entry.path):
                if not pic_entry.is_file():
                    continue
                user_rec, err = face_recognition.search(pic_entry.path, group_id_list=group_id_list)
                logging.info("search return: user_rec: %s, err: %s" % (user_rec, err))
                if err is None and user_rec['user_id'] == user_entry.name:
                    logging.info("search match success: user_rec: %s" % user_rec)
                elif user_rec is None:
                    logging.info("search match failed not found: err: %s" % err)
                else:
                    logging.info("search match failed wrong found: user_rec: %s" % user_rec)

