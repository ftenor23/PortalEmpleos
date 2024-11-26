import json

from config import ServerConfig
import jwt
from flask import g

from managers import Manager

logger = ServerConfig.rootLogger.getChild(__name__)


def register_user_lenght_validation(name, last_name, email, password, resume_url="", ):
    final_response = {'ok': True}

    logger.info(f"{g.request_id} - validando longitud de campos")

    if len(name) > 20:
        final_response['ok'] = False

    if len(last_name) > 20:
        final_response['ok'] = False

    if len(email) > 60:
        final_response['ok'] = False

    # desencriptar password y validar longitud
    if len(password) > 30:
        final_response['ok'] = False

    if len(resume_url) > 100:
        final_response['ok'] = False

    return final_response


def status_validation(new_status):

    return new_status in ['0', '1', '2']


def decode_token(token):
    final_response = {'ok': True,
                      'data': {}}
    try:
        # decodificamos el token y obtenemos public id del contexto y  fecha de expiracion
        final_response['data'] = jwt.decode(token, ServerConfig.secret_key, algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        logger.exception(f"{g.request_id} - token expirado")
        final_response['ok'] = False

    return final_response


def create_user(name, last_name, email, password, is_candidate, resume_url=None, skill_list=None, company_id=None):
    final_response = {'ok': True,
                      'data': {}}

    create_user_response = Manager.create_user(name=name,
                                               last_name=last_name,
                                               email=email,
                                               password=password,
                                               is_candidate=is_candidate,
                                               request_id=g.request_id)

    if not create_user_response['ok']:
        logger.info(f"{g.request_id} - error al crear usuario")
        return {'ok': False}

    get_user_id_response = Manager.get_user_id_with_email(email=email,
                                                          request_id=g.request_id)

    if not get_user_id_response['ok'] or not get_user_id_response['data']:
        logger.info(f"{g.request_id} - error al obtener user_id")
        return {'ok': False}

    user_id = get_user_id_response['data']['user_id']

    if is_candidate:

        insert_candidate_resume_response = Manager.insert_candidate_resume_url(user_id=user_id,
                                                                               resume_url=resume_url,
                                                                               request_id=g.request_id)

        if not insert_candidate_resume_response['ok']:
            logger.info(f"{g.request_id} - error al cargar cv")
            return {'ok': False}

        insert_candidate_skills_response = Manager.insert_candidate_skills(skill_list=skill_list,
                                                                           user_id=user_id,
                                                                           request_id=g.request_id)

        if not insert_candidate_skills_response['ok']:
            logger.info(f"{g.request_id} - error al cargar habilidades")
            return {'ok': False}

    else:

        insert_company_response = Manager.insert_employer_actual_company(user_id=user_id,
                                                                         company_id=company_id,
                                                                         request_id=g.request_id)

        if not insert_company_response['ok']:
            logger.info(f"{g.request_id} - error al cargar lugar de trabajo")
            return {'ok': False}

    # si llegamos a este punto, el usuario se genero sin problemas
    return final_response


def format_candidate_experience(data):
    for person in data:
        person['experience'] = json.loads(person['experience'])

    return data

def format_job_offers(data):
    return {
        "number_of_job_offers": sum(item['sector_count'] for item in data),
        "business_sector": {item['company_type']: item['sector_count'] for item in data}
    }

def format_succesful_job_offers(data):
    return {
        "number_of_successful_job_offers": sum(item['successful_job_offer_count'] for item in data),
        "business_sector": {item['bussines_sector']: item['successful_job_offer_count'] for item in data}
    }

def format_companies_response(data):
    for item in data:
        item['business_sector'] = json.loads(item['business_sector'])
    return data