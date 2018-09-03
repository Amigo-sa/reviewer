from flask import request, Blueprint, current_app
from time import strftime
import logging
from logging.handlers import RotatingFileHandler
import os
from node.settings import constants

bp = Blueprint('logging', __name__)

@bp.after_app_request
def after_request(response):
    ts = strftime('[%Y-%b-%d %H:%M]')
    try:
        result = response.get_json()['result']
    except:
        result = None

    current_app.logger.info('%s %s %s %s %s %s result: %s',
                            ts,
                            request.remote_addr,
                            request.method,
                            request.scheme,
                            request.full_path,
                            response,
                            result)

    return response


def configure_logger(app):
    try:
        for handler in app.logger.handlers:
            app.logger.removeHandler(handler)

        log_path = os.path.abspath(constants.log_path)

        fh = RotatingFileHandler(log_path, maxBytes= 100000, backupCount=5)
        fh.setLevel(logging.DEBUG)

        logger = app.logger
        logger.setLevel(logging.DEBUG)

        logger.addHandler(fh)

    except Exception as e:
        logging.exception(str(e))

