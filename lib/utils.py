import string
import random

def format_response(data, status_code, message=None, custom_ob=None, message_code_class=None, save=True):
    message_code = None
    if data is not None:

        try:

            if status_code == 500:
                data.failed = True
                data.charged = False

            if save:
                data.save()

            if custom_ob is not None:
                data = custom_ob
        except Exception as e:
            data = None
            status_code = 500
            message = None
    else:
        data = custom_ob

    if 200 <= status_code < 300:
        success_flag = True
        message_code = 'success'
    else:
        success_flag = False
        if status_code == 500 and message is None:
            message = "ERROR_500"
            message_code = 'contact_admin'
        elif status_code == 422 and message is None:
            message = "FAILED"
            message_code = 'failed'

    if message_code_class is not None:
        message_code = message_code_class.code
        message = message_code_class.message
    else:
        message_code = message_code

    response_json = ({
                         "data": data,
                         "status_code": status_code,
                         "message_code": message_code,
                         "message": message,
                         "success": success_flag,
                     }, status_code)

    return response_json


def generate_id(prepend_string):
    charset = string.ascii_lowercase + string.ascii_letters
    return prepend_string + "_" + "".join([random.choice(charset) for _ in range(20)])
