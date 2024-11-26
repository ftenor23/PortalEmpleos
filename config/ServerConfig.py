import logging
from pathlib import Path
import configparser
import mysql.connector.pooling


ROOT_DIR = Path(__file__).parent.parent
properties = configparser.ConfigParser()
properties.read(f"{ROOT_DIR}/properties/.env")
APP_PORT = properties.get('APP', 'app_port')
APP_DEBUG = properties.get('APP', 'app_debug')
ENVIRONMENT = properties.get('APP', 'environment')
secret_key = properties.get('AUTH', 'secret_key')
token = properties.get('TOKEN', 'token')

# configuracion de los logs
rootLogger = logging.getLogger()
logging.basicConfig(level=logging.INFO,  # Nivel de los logs
                    format='"[%(asctime)s] [%(process)s] [%(name)s][%(lineno)d] [%(levelname)s] %(message)s"')

#rootLogger = logging.getLogger()
rootLogger.info("iniciando....")
database_user = properties.get('database', 'database_user')
database_password = properties.get('database', 'database_password')
database_host = properties.get('database', 'database_host')
database_port = properties.get('database', 'database_port')
database_database = properties.get('database', 'database_database')
pool_size = int(properties.get('database', 'pool_size'))

#verificar si el espacio previo a database_port es correcto
'''database_uri = 'mysql://' + database_user + ':' + database_password + '@' + database_host + ': ' + database_port \
               + '/' + database_database'''

database_uri = 'mysql://' + database_user + ':' + database_password + '@' + database_host + ':' + database_port \
               + '/' + database_database

rootLogger.info(f"database_url {database_uri}")

cnx_pool = None

try:
    rootLogger.info(f"iniciando conexion con base de datos")
    cnx_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="PortalEmpleos",
        pool_size=pool_size,
        pool_reset_session=True,
        host=database_host,
        port=database_port,
        user=database_user,
        password=database_password,
        database=database_database
    )
except:
    rootLogger.exception("error al hacer conexion con base de datos")


token_expiration_in_minutes = properties.get('AUTH', 'token_expiration_in_minutes')
rootLogger.info(f"aplicacion corriendo en {ENVIRONMENT}")


'''import socket
import os
from concurrent.futures import ThreadPoolExecutor
from logging.handlers import RotatingFileHandler
import logging
from pathlib import Path
import configparser
import mysql.connector.pooling
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql.pymysql import dbapi
import urllib3

ROOT_DIR = Path(__file__).parent.parent
properties = configparser.ConfigParser()
properties.read(f"{ROOT_DIR}/properties/.env")
APP_PORT = properties.get('APP', 'app_port')
APP_DEBUG = properties.get('APP', 'app_debug')
ENVIRONMENT = properties.get('APP', 'environment')
secret_key = properties.get('AUTH', 'secret_key')

# configuracion de los logs
rootLogger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG,  # Nivel de los logs
                    format='"[%(asctime)s] [%(process)s] [%(name)s][%(lineno)d] [%(levelname)s] %(message)s"',
                    )

#rootLogger = logging.getLogger()
rootLogger.info("iniciando....")
database_user = properties.get('database', 'database_user')
database_password = properties.get('database', 'database_password')
database_host = properties.get('database', 'database_host')
database_port = properties.get('database', 'database_port')
database_database = properties.get('database', 'database_database')
pool_size = int(properties.get('database', 'pool_size'))

#verificar si el espacio previo a database_port es correcto
database_uri = 'mysql://' + database_user + ':' + database_password + '@' + database_host + ': ' + database_port \
               + '/' + database_database

database_uri = 'mysql://' + database_user + ':' + database_password + '@' + database_host + ':' + database_port \
               + '/' + database_database

rootLogger.info(f"database_url {database_uri}")

cnx_pool = None

try:
    rootLogger.info("levantando conexion")

    rootLogger.info(f"Conectando a MySQL con usuario: {database_user}, host: {database_host}, puerto: {database_port}, "
                    f"pass: {database_password}, database: {database_database}")
    cnx = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="dFNfuD6jrQraacc",
        database="portal_empleos"
    )
    database_uri = "mysql+pymysql://root:dFNfuD6jrQraacc@localhost:3306/portal_empleos"
    engine = create_engine(database_uri)
    with engine.connect() as connection:
        print("Conexión exitosa")
    rootLogger.info("conexion exitosa")
except:
    rootLogger.debug("Entrando al bloque except", exc_info=True)
    rootLogger.exception("Error al hacer conexión con la base de datos: %s")
    raise

rootLogger.info("coneion terminada")
token_expiration_in_minutes = properties.get('AUTH', 'token_expiration_in_minutes')
rootLogger.info(f"aplicacion corriendo en {ENVIRONMENT}")'''