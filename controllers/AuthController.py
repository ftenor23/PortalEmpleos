import time
from flask import request, g
from werkzeug.security import check_password_hash
import jwt
import datetime
from functools import wraps

from config import ServerConfig, AuthConfig
from managers import Manager
from utils import Utils

logger = ServerConfig.rootLogger.getChild(__name__)


def get_token(username, password):
    g.id_context = 0
    logger.info(f"{g.request_id} - usuario: {username}")

    user_response = Manager.check_user(username=username)

    if not user_response['ok']:
        logger.info(f"{g.request_id} - error al validar usuario de contexto")
        return {'code': '0500',
                'description': AuthConfig.get_token_code_map['0500']}

    password_context = user_response['data']['password']

    if not check_password_hash(password_context, password):
        logger.info(f"{g.request_id} - contraseña incorrecta")
        return {"code": 403, "description": AuthConfig.get_token_code_map[403], "message": "invalid password"}, 403

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    exp = now + datetime.timedelta(minutes=AuthConfig.token_expiration_in_minutes)
    token = jwt.encode({'public_id': user_response['data']["public_id"], 'exp': exp}, ServerConfig.secret_key,
                       algorithm="HS256")

    return {
               'token': token,
               "code": '0200',
               "description": AuthConfig.get_token_code_map['0200'],
               'utcnow': now,
               'token_expiration': exp,
               'token_type': 'New',
               'token_expires_in_millis': int((exp - now).total_seconds() * 1000)
           }, 200


def token_required(service_required=False, endpoint=None):
    def services_validator(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            start_time = time.time()

            if 'x-access-token' not in request.headers:
                logger.exception(f"{g.request_id} - token vacio")
                g.response = "0401"
                return {"code": "0401", "description": AuthConfig.token_required_code_map["0401"]}, 403

            token = request.headers['x-access-token']

            if token != ServerConfig.token:
                logger.info(f"{g.request_id} - error al decodificar token")
                g.response = "0402"
                return {"code": "0402", "description": AuthConfig.token_required_code_map["0402"]}, 403

            logger.info(f"{g.request_id} - token validado correctamente")
            end_time = time.time()

            logger.info(f"{g.request_id} - tardo en autenticar: {(end_time - start_time)}")

            data = request.json
            return f(data, *args, **kwargs)

        return decorated

    return services_validator


def candidate_validation():
    def services_validator(f):
        @wraps(f)
        def decorated(data_request, *args, **kwargs):
            if g.user_id is None or g.user_id == "":
                logger.info(f"{g.request_id} - no se envio id_user en el header")
                return {
                           "code": "1401",
                           "description": AuthConfig.user_verify_code_map["1401"]
                       }, 400


            current_user_db = Manager.get_user_data_login(user_id=g.user_id, is_candidate=True, request_id=g.request_id)

            if not current_user_db["ok"]:
                logger.info(f"{g.request_id} - error al verificar el usuario")
                return {
                           "code": "1500",
                           "description": AuthConfig.user_verify_code_map["1500"]
                       }, 400

            if not current_user_db["data"]:
                logger.info(f"{g.request_id} - usuario no habilitado para realizar la operacion seleccionada")
                return {
                           "code": "1404",
                           "description": AuthConfig.user_verify_code_map["1404"]
                       }, 400

            logger.info(f"{g.request_id} - solicitud de usuario: {current_user_db['data']['name']} {current_user_db['data']['last_name']}")

            return f(data_request, *args, **kwargs)

        return decorated

    return services_validator


def employer_validation():
    def services_validator(f):
        @wraps(f)
        def decorated(data_request, *args, **kwargs):
            if g.user_id is None or g.user_id == "":
                logger.info(f"{g.request_id} - no se envio id_user en el header")
                return {
                           "code": "1401",
                           "description": AuthConfig.user_verify_code_map["1401"]
                       }, 400


            current_user_db = Manager.get_user_data_login(user_id=g.user_id, is_candidate=False, request_id=g.request_id)

            if not current_user_db["ok"]:
                logger.info(f"{g.request_id} - error al verificar el usuario")
                return {
                           "code": "1500",
                           "description": AuthConfig.user_verify_code_map["1500"]
                       }, 400

            if not current_user_db["data"]:
                logger.info(f"{g.request_id} - usuario no habilitado para realizar la operacion seleccionada")
                return {
                           "code": "1404",
                           "description": AuthConfig.user_verify_code_map["1404"]
                       }, 400

            logger.info(f"{g.request_id} - solicitud de usuario: {current_user_db['data']['name']} {current_user_db['data']['last_name']}")

            return f(data_request, *args, **kwargs)

        return decorated

    return services_validator
