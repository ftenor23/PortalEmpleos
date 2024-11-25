from datetime import time
from flask import Flask, g, request
from config import ServerConfig
import time, datetime
import json

app = Flask(__name__, instance_relative_config=True)
logger = ServerConfig.rootLogger.getChild(__name__)

@app.before_request
def before_request():
    try:
        g.start = time.time()
        ahora = datetime.datetime.now()
        request_id = ahora.strftime("%Y%m%d%H%M%S%f")
        g.request_id = request_id
        g.id_user = ""
        logger.info(f"{request_id} - seteo de datos ok")
    except:
        logger.exception(f"error en befor request")



@app.after_request
def after_request(response):
    diff = time.time() - g.start

    logger.info(f"{g.request_id} - tiempo de ejecucion {diff} segundos")
    logger.info(f"{g.request_id} - fin")
    return response


@app.route("/echo", methods=["POST", "GET"])
def echo():
    return {}, 200

logger.info(f"iniciando")


if __name__ == "__main__":
    try:
        logger.info("Iniciando la aplicación...")
        app.run(debug=ServerConfig.APP_DEBUG)
    except:
        logger.exception(f"Error al iniciar la aplicación:")
