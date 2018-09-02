from flask import request, Blueprint, current_app
from time import strftime

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



