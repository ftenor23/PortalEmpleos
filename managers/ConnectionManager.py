from functools import wraps

from config import ServerConfig

logger = ServerConfig.rootLogger.getChild(__name__)


# decorador que se utiliza para reciclar funciones y optimizar la lectura del codigo
def manage_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        final_response = {
            "ok": True,
            "data": {}
        }
        cnx = ServerConfig.cnx_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            return func(cnx, cursor, final_response, *args, **kwargs)
        except:
            logger.exception(f"{kwargs.get('request_id', 'unknown')} - error al ejecutar la función del manager")
            final_response["ok"] = False
            return final_response
        finally:
            cursor.close()
            cnx.close()

    return wrapper
