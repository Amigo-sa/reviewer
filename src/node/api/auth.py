# -*- coding: utf-8 -*-
from bson import ObjectId
import node.settings.errors as ERR
import node.settings.constants as constants
from flask import Blueprint, request, jsonify
from data.reviewer_model import *
from datetime import datetime, timezone, timedelta, date
import random
import requests
import hashlib
from functools import wraps
import re
from node.thirdparty import smsc_api
import os


bp = Blueprint('routes_auth', __name__)


class AuthError(Exception):
    pass


@bp.route("/user_login", methods= ["POST"])
def user_login():
    req = request.get_json()
    try:
        phone_no = req["phone_no"]
        password = req["password"]
        auth_info = AuthInfo.objects.get({"phone_no": phone_no})
        pass_hash = hash_password(password)
        if auth_info.password == pass_hash:
            session_id = gen_session_id()
            auth_info.session_id = session_id
            auth_info.attempts = 0
            auth_info.save()
            result = {"result": ERR.OK,
                      "session_id": session_id}
        else:
            result = {"result": ERR.AUTH}
            if auth_info.attempts >= constants.authorization_max_attempts:
                auth_info.is_approved = False
                auth_info.password = None
            else:
                auth_info.attempts += 1
            auth_info.save()
    except KeyError as e:
        result = {"result": ERR.INPUT}
        print(str(e))
    except Exception as e:
        result = {"result": ERR.AUTH}
        print(str(e))
    return jsonify(result), 200


@bp.route("/oauth/token", methods= ["POST"])
def grant_oauth_token():
    try:
        phone_no = request.form["username"]
        password = request.form["password"]
        auth_info = AuthInfo.objects.get({"phone_no": phone_no})
        pass_hash = hash_password(password)
        if auth_info.password == pass_hash:
            session_id = gen_session_id()
            auth_info.session_id = session_id
            auth_info.save()
            result = {"access_token": str(session_id),
                      "token_type": "bearer",
                      "expires_in": 86400
                      }
            return jsonify(result), 200

        result = {"error": "invalid_grant",
                  "error_description": "Invalid login or password"}
        if auth_info.attempts >= constants.authorization_max_attempts:
            auth_info.is_approved = False
            auth_info.password = None
        else:
            auth_info.attempts += 1
        auth_info.save()
        return jsonify(result), 400
    except KeyError as e:
        result = {"error": "invalid_request",
                  "error_description": "Invalid parameters"}
        return jsonify(result), 400
    except Exception as e:
        return 404


@bp.route("/confirm_phone_no", methods= ["POST"])
def confirm_phone():
    auth_err= None
    req = request.get_json()
    sms_timeout = timedelta(minutes=constants.sms_timeout_minutes)
    try:
        phone_no = str(req["phone_no"])
        if not check_phone_format(phone_no):
            return jsonify({"result": ERR.AUTH_INVALID_PHONE}), 200
        auth_info = AuthInfo.objects.raw({"phone_no": phone_no})
        rec_count = auth_info.count()
        if rec_count:
            old_auth_info = auth_info.first()
            if old_auth_info.is_approved:
                raise AuthError("номер уже подтверждён")
            else:
                last_send_time = old_auth_info.last_send_time.as_datetime()
                if datetime.now(timezone.utc) < last_send_time + sms_timeout:
                    auth_err = ERR.AUTH_SMS_TIMEOUT
                    raise AuthError("слишком частые СМС")
                else:
                    old_auth_info.delete()
        new_auth_info = AuthInfo()
        new_auth_info.phone_no = phone_no
        new_auth_info.last_send_time = datetime.now(timezone.utc)
        code = gen_sms_code()
        session_id = gen_session_id()
        new_auth_info.session_id = session_id
        new_auth_info.auth_code = code
        new_auth_info.attempts = 0
        new_auth_info.save()
        try:
            send_sms(phone_no, code)
        except:
            raise AuthError("не удалось отправить смс")
        result = {"result": ERR.OK,
                  "session_id": session_id}

    except KeyError as e:
        result = {"result": ERR.INPUT}
    except AuthError as e:
        err = auth_err if auth_err else ERR.AUTH
        result = {"result": err,
                  "error_message": str(e)}
    except Exception as e:
        print(str(e))
        result = {"result": ERR.DB}

    return jsonify(result), 200


@bp.route("/finish_phone_confirmation", methods= ["POST"])
def finish_phone_confirmation():
    max_attempts = constants.confirmation_max_attempts
    confirm_timeout = timedelta(minutes=constants.confirmation_timeout_minutes)
    req = request.get_json()
    err = ERR.AUTH
    try:
        auth_code = req["auth_code"]
        session_id = str(req["session_id"])
        auth_info = AuthInfo.objects.raw({"session_id": session_id})
        if auth_info.count():
            auth_info = auth_info.first()
            sent_time = auth_info.last_send_time.as_datetime()
            if auth_info.is_approved:
                result = {"result": ERR.OK}
            elif sent_time < datetime.now(timezone.utc) - confirm_timeout:
                err = ERR.AUTH_SESSION_EXPIRED
                raise AuthError("session expired")
            elif auth_info.auth_code == auth_code:
                result = {"result": ERR.OK}
                auth_info.is_approved = True
                auth_info.auth_code = None
                auth_info.save()
            else:
                auth_info.attempts += 1
                attempts_remain = max_attempts - auth_info.attempts
                if attempts_remain > 0:
                    message = "wrong code, %s attempts remain"%attempts_remain
                else:
                    message = "out of attempts, auth code destroyed"
                result = {"result": ERR.AUTH_CODE_INCORRECT,
                          "error_message": message}
                print("%s attempts remain"%attempts_remain)
                if auth_info.attempts == max_attempts:
                    auth_info.auth_code = None
                    auth_info.session_id = None
                auth_info.save()
        else:
            # выдаем ошибку аутентификации так как такой сессии не установлено
            result = {"result": ERR.AUTH_NO_SESSION,
                      "error_message": "no session found"}
    except KeyError as e:
        result = {"result": ERR.INPUT}
        print(repr(e))
    except AuthError as e:
        result = {"result": err,
                  "error_message": str(e)}
        print(repr(e))
    except Exception as e:
        result = {"result": ERR.DB}
        print(repr(e))

    return jsonify(result), 200


@bp.route("/password", methods= ["POST"])
def set_password():
    req = request.get_json()
    try:
        password = req["password"]
        session_id = req["session_id"]
        auth_info = AuthInfo.objects.get({"session_id": session_id})
        if auth_info.is_approved and auth_info.password is None:
            pass_hash = hash_password(password)
            auth_info.password = pass_hash
            auth_info.save()
            result = {"result": ERR.OK}
        else:
            result = {"result": ERR.INPUT}
    except KeyError as e:
        result = {"result": ERR.INPUT}
        print(str(e))
    except Exception as e:
        result = {"result": ERR.AUTH}
        print(str(e))

    return jsonify(result), 200


def gen_sms_code():
    code = random.randint(0,9999)
    codestr = "{0:04}".format(code)
    print(codestr)
    return codestr


def gen_session_id():
    return os.urandom(16).hex()


def hash_password(password):
    pass_hash = hashlib.sha256(password.encode("utf-8"))
    hash_hex = pass_hash.hexdigest()
    print(hash_hex)
    return hash_hex


# TODO смски работают, но я пока закомментил блок потому что не знаю как тестировать
def send_sms(phone_no, message):
    requests.post(constants.mock_smsc_url + "/send_sms",json={
        "auth_code" : message,
        "phone_no" : phone_no
    })
    # smsc = smsc_api.SMSC()
    # smsc.send_sms(phone_no, message)
    # print(smsc.get_balance())


def check_phone_format(phone_no):
    pattern = r"^7\d{10}$"
    return re.match(pattern, phone_no)


def required_auth(required_permissions="admin"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''
            try:
                auth_info = AuthInfo.objects.raw({"session_id": auth_token})
                if auth_info.count():
                    auth_info = auth_info.first()
                else:
                    return jsonify({"result": ERR.AUTH}), 200
                if auth_info.permissions & 1 and required_permissions != "reviewer":
                    return f(*args, **kwargs)
                if required_permissions == "admin":
                    return jsonify({"result": ERR.AUTH}), 200
                if required_permissions == "user" and auth_info.person_id:
                    if "person_id" in kwargs:
                        person_id = kwargs["person_id"]
                    else:
                        person_id = request.get_json()["person_id"]
                    if person_id == str(auth_info.person_id.pk):
                        return f(*args, **kwargs)
                if required_permissions == "group_member" and auth_info.person_id:
                    if Person.objects.raw({"_id": auth_info.person_id.pk}).count():
                        for group_member in GroupMember.objects.raw({"person_id": auth_info.person_id.pk}):
                            if str(group_member.pk) == kwargs["id"]:
                                return f(*args, **kwargs)
                if required_permissions == "reviewer" and auth_info.person_id:
                    if request.method == "POST":
                        if str(auth_info.person_id.pk) == request.get_json()['reviewer_id']:
                            return f(*args, **kwargs)
                    if request.method == "DELETE":
                        if auth_info.person_id.pk == get_reviewer_id_by_review_id(kwargs["id"]):
                            return f(*args, **kwargs)
            except:
                return jsonify({"result": ERR.AUTH}), 200
            return jsonify({"result": ERR.AUTH}), 200

        return decorated_function
    return decorator


def get_reviewer_id_by_review_id(_id):
    if SpecializationReview.objects.raw({"_id": ObjectId(_id)}).count():
        return SpecializationReview.objects.get({"_id": ObjectId(_id)}).reviewer_id.pk
    if HSReview.objects.raw({"_id": ObjectId(_id)}).count():
        return HSReview.objects.get({"_id": ObjectId(_id)}).reviewer_id.pk
    if SSReview.objects.raw({"_id": ObjectId(_id)}).count():
        return SSReview.objects.get({"_id": ObjectId(_id)}).reviewer_id.pk
    if GroupReview.objects.raw({"_id": ObjectId(_id)}).count():
        return GroupReview.objects.get({"_id": ObjectId(_id)}).reviewer_id.pk
    if GroupTestReview.objects.raw({"_id": ObjectId(_id)}).count():
        return GroupTestReview.objects.get({"_id": ObjectId(_id)}).reviewer_id.pk
    if GroupMemberReview.objects.raw({"_id": ObjectId(_id)}).count():
        return GroupMemberReview.objects.get({"_id": ObjectId(_id)}).reviewer_id.pk
    return None

