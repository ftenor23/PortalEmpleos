from flask import request, g
from config import ServerConfig, AuthConfig
from controllers import AuthController
from flask import Blueprint
logger = ServerConfig.rootLogger.getChild(__name__)

TOKEN_EXPIRATION_IN_MINUTES = ServerConfig.token_expiration_in_minutes
TOKEN_LIST = dict()
SANCTIONS = dict()
SERVICE_NAME = "auth"
bp = Blueprint("AuthV2", __name__, url_prefix='/auth/' + '/')

@bp.route('/getToken')
def get_token():
    logger.info(f"{g.request_id} - inicio get token")
    logger.info(f"{g.request_id} - iniciando verificacion de campos obligatorios")
    try:
        auth = request.authorization
        username = auth.username
        password = auth.password
        if not auth or not auth.username or not auth.password:
            logger.info(f"faltan campos obligatorios")
            raise
    except:
        logger.exception(f"{g.request_id} - faltan campos obligatorios")
        return {"code": 403, "description": AuthConfig.get_token_code_map[403]}, 403

    logger.info(f"{g.request_id} - fin verificacion de campos obligatorios")

    return AuthController.get_token(username=username, password=password)