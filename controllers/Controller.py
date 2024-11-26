from config import ServerConfig, ServiceConfig
from managers import Manager
from utils import Utils
from flask import g

logger = ServerConfig.rootLogger.getChild(__name__)


def register_candidate_user(name, last_name, email, password, resume_url, skill_list):
    lenght_validation = Utils.register_user_lenght_validation(name=name,
                                                              last_name=last_name,
                                                              email=email,
                                                              password=password,
                                                              resume_url=resume_url)

    if not lenght_validation['ok']:
        logger.info(f"{g.request_id} - validacion de longitud de campos no exitosa")
        return {'code': '0411',
                'description': ServiceConfig.register_user_code_map['0411']}

    logger.info(f"{g.request_id} - validacion de longitud de campos exitosa")

    user_validation_response = Manager.user_registered(email=email, is_candidate=True, request_id=g.request_id)

    if not user_validation_response['ok']:
        logger.info(f"{g.request_id} - error interno al validar usuario")
        return {'code': '0500',
                'description': ServiceConfig.register_user_code_map['0500']}

    # si se devuelve data = True, ya existe un usuario registrado con estos datos
    if user_validation_response['data']:
        logger.info(f"{g.request_id} - usuario ya registrado")
        return {'code': '0410',
                'description': ServiceConfig.register_user_code_map['0410']}

    logger.info(f"{g.request_id} - se valido que el usuario no esta registrado")

    #todo validar que la lista de skills sea valida

    create_user_response = Utils.create_user(name=name,
                                             last_name=last_name,
                                             email=email,
                                             password=password,
                                             resume_url=resume_url,
                                             skill_list=skill_list,
                                             is_candidate=True)

    if not create_user_response['ok']:
        logger.info(f"{g.request_id} - error interno al crear usuario")
        return {'code': '0500',
                'description': ServiceConfig.register_user_code_map['0500']}

    logger.info(f"{g.request_id} - usuario creado correctamente")

    return {'code': '0200',
            'description': ServiceConfig.register_user_code_map['0200']}


def register_employer_user(name, last_name, email, password, company_id):
    lenght_validation = Utils.register_user_lenght_validation(name=name,
                                                              last_name=last_name,
                                                              email=email,
                                                              password=password)

    if not lenght_validation['ok']:
        logger.info(f"{g.request_id} - validacion de longitud de campos no exitosa")
        return {'code': '0411',
                'description': ServiceConfig.register_user_code_map['0411']}

    logger.info(f"{g.request_id} - validacion de longitud de campos exitosa")

    user_validation_response = Manager.user_registered(email=email, is_candidate=False, request_id=g.request_id)

    if not user_validation_response['ok']:
        logger.info(f"{g.request_id} - error interno al validar usuario")
        return {'code': '0500',
                'description': ServiceConfig.register_user_code_map['0500']}

    # si se devuelve data = True, ya existe un usuario registrado con estos datos
    if user_validation_response['data']:
        logger.info(f"{g.request_id} - usuario ya registrado")
        return {'code': '0410',
                'description': ServiceConfig.register_user_code_map['0410']}

    logger.info(f"{g.request_id} - se valido que el usuario no esta registrado")

    # validacion de existencia de la compañia que selecciono el usuario
    company_id_exists_response = Manager.company_exists(company_id=company_id,
                                                        request_id=g.request_id)

    if not company_id_exists_response['ok']:
        logger.info(f"{g.request_id} - error al validar id de compañia")
        return {'code': '0500',
                'description': ServiceConfig.register_user_code_map['0500']}

    if not company_id_exists_response['data']:
        logger.info(f"{g.request_id} - no se encontro empresa con el id {company_id}")
        return {'code': '0404',
                'description': ServiceConfig.register_user_code_map['0404']}

    create_user_response = Utils.create_user(name=name,
                                             last_name=last_name,
                                             email=email,
                                             password=password,
                                             company_id=company_id,
                                             is_candidate=False)

    if not create_user_response['ok']:
        logger.info(f"{g.request_id} - error interno al crear usuario")
        return {'code': '0500',
                'description': ServiceConfig.register_user_code_map['0500']}

    logger.info(f"{g.request_id} - usuario creado correctamente")

    return {'code': '0200',
            'description': ServiceConfig.register_user_code_map['0200']}


def login(email, password):
    user_data_response = Manager.get_user_data(email=email,
                                               password=password,
                                               request_id=g.request_id)

    if not user_data_response['ok']:
        logger.info(f"{g.request_id} - error interno al obtener datos de usuario")
        return {'code': '0500',
                'description': ServiceConfig.login_code_map['0500']}

    # si no se devuelve data, no se encontro ningun usuario con ese mail y/o password
    if not user_data_response['data']:
        logger.info(f"{g.request_id} - usuario/contraseña incorrecto")
        return {'code': '0404',
                'description': ServiceConfig.login_code_map['0404']}

    logger.info(f"{g.request_id} - datos de usuario obtenidos correctamente")

    return {'code': '0200',
            'description': ServiceConfig.login_code_map['0200'],
            'data': user_data_response['data']}


def create_new_company(name, description, tax_id, company_type):
    company_exists_response = Manager.company_exists(tax_id=tax_id,
                                                     request_id=g.request_id)

    if not company_exists_response['ok']:
        logger.info(f"{g.request_id} - error interno al validar si la compañia existe")
        return {'code': '0500',
                'description': ServiceConfig.create_new_company_code_map['0500']}

    # si se devuelve data, significa que ya existe la compañia
    if company_exists_response['data']:
        logger.info(f"{g.request_id} - empresa existente")
        return {'code': '0410',
                'description': ServiceConfig.create_new_company_code_map['0410']}

    logger.info(f"{g.request_id} - se valido que la empresa no esta registrada en sistema")

    company_creation_response = Manager.create_new_company(name=name,
                                                           description=description,
                                                           tax_id=tax_id,
                                                           company_type=company_type,
                                                           request_id=g.request_id)

    if not company_creation_response['ok']:
        logger.info(f"{g.request_id} - error al cargar la empresa en base de datos")
        return {'code': '0500',
                'description': ServiceConfig.create_new_company_code_map['0500']}

    logger.info(f"{g.request_id} - empresa guardada correctamente")

    return {'code': '0200',
            'description': ServiceConfig.create_new_company_code_map['0200']}


def create_new_job(name, description, requirements):
    job_exists_response = Manager.job_exists(name=name,
                                             description=description,
                                             requirements=requirements,
                                             request_id=g.request_id)

    if not job_exists_response['ok']:
        logger.info(f"{g.request_id} - error interno al validar si el trabajo existe en base de datos")
        return {'code': '0500',
                'description': ServiceConfig.create_new_job_code_map['0500']}

    # si se devuelve data, significa que ya existe el trabajo
    if job_exists_response['data']:
        logger.info(f"{g.request_id} - trabajo existente")
        return {'code': '0410',
                'description': ServiceConfig.create_new_job_code_map['0410']}

    logger.info(f"{g.request_id} - se valido que el trabajo no esta registrado en sistema")

    job_creation_response = Manager.create_new_job(name=name,
                                                   description=description,
                                                   requirements=requirements,
                                                   request_id=g.request_id)

    if not job_creation_response['ok']:
        logger.info(f"{g.request_id} - error al cargar la empresa en base de datos")
        return {'code': '0500',
                'description': ServiceConfig.create_new_job_code_map['0500']}

    logger.info(f"{g.request_id} - trabajo registrado correctamente")

    return {'code': '0200',
            'description': ServiceConfig.create_new_job_code_map['0200']}


def create_job_offer(company_id, job_id,salary, location):
    company_exists_response = Manager.company_exists(company_id=company_id,
                                                     request_id=g.request_id)

    if not company_exists_response['ok']:
        logger.info(f"{g.request_id} - error interno al validar si la compañia existe")
        return {'code': '0500',
                'description': ServiceConfig.create_job_offer_code_map['0500']}

    # si se devuelve data, significa que ya existe la compañia
    if not company_exists_response['data']:
        logger.info(f"{g.request_id} - empresa no existente")
        return {'code': '0411',
                'description': ServiceConfig.create_job_offer_code_map['0411']}

    logger.info(f"{g.request_id} - se valido que la empresa esta registrada en sistema")

    job_offer_exists_response = Manager.job_offer_exists(company_id=company_id,
                                                         job_id=job_id,
                                                         salary=salary,
                                                         location=location,
                                                         request_id=g.request_id)

    if not job_offer_exists_response['ok']:
        logger.info(f"{g.request_id} - error interno al validar si la oferta de trabajo existe")
        return {'code': '0500',
                'description': ServiceConfig.create_job_offer_code_map['0500']}

    # si se devuelve data, significa que ya existe la compañia
    if job_offer_exists_response['data']:
        logger.info(f"{g.request_id} - la oferta de trabajo ya esta registrada")
        return {'code': '0410',
                'description': ServiceConfig.create_job_offer_code_map['0410']}

    logger.info(f"{g.request_id} - se valido que la oferta de trabajo no esta registrada")

    job_offer_creation_response = Manager.create_new_job_offer(company_id=company_id,
                                                               job_id=job_id,
                                                               salary=salary,
                                                               location=location,
                                                               request_id=g.request_id)

    if not job_offer_creation_response['ok']:
        logger.info(f"{g.request_id} - error al cargar la empresa en base de datos")
        return {'code': '0500',
                'description': ServiceConfig.create_job_offer_code_map['0500']}

    logger.info(f"{g.request_id} - oferta de trabajo guardada correctamente")

    return {'code': '0200',
            'description': ServiceConfig.create_job_offer_code_map['0200']}


def apply_for_a_job(job_offer_id, candidate_id):
    job_offer_is_active_response = Manager.job_offer_is_active(job_offer_id=job_offer_id,
                                                               request_id=g.request_id)

    if not job_offer_is_active_response['ok']:
        logger.info(f"{g.request_id} - error al validar si la oferta de trabajo esta activa")
        return {'code': '0500',
                'description': ServiceConfig.apply_for_a_job_code_map['0500']}

    if not job_offer_is_active_response['data']:
        logger.info(f"{g.request_id} - la oferta de trabajo no esta activa")
        return {'code': '0411',
                'description': ServiceConfig.apply_for_a_job_code_map['0411']}

    logger.info(f"{g.request_id} - la oferta de trabajo esta activa")

    user_already_applied_for_job_response = Manager.user_already_applied_for_job(job_offer_id=job_offer_id,
                                                                                 candidate_id=candidate_id,
                                                                                 request_id=g.request_id)

    if not user_already_applied_for_job_response['ok']:
        logger.info(f"{g.request_id} - error al validar si la oferta de trabajo esta activa")
        return {'code': '0500',
                'description': ServiceConfig.apply_for_a_job_code_map['0500']}

    if user_already_applied_for_job_response['data']:
        logger.info(f"{g.request_id} - el usuario ya se postulo para la oferta")
        return {'code': '0410',
                'description': ServiceConfig.apply_for_a_job_code_map['0410']}

    logger.info(f"{g.request_id} - se valido que el usuario no se esta postulado para la oferta")

    job_application_response = Manager.job_application(job_offer_id=job_offer_id,
                                                       candidate_id=candidate_id,
                                                       request_id=g.request_id)

    if not job_application_response['ok']:
        logger.info(f"{g.request_id} - error al postular al usuario")
        return {'code': '0500',
                'description': ServiceConfig.apply_for_a_job_code_map['0500']}

    logger.info(f"{g.request_id} - usuario postulado correctamente")

    return {'code': '0200',
            'description': ServiceConfig.apply_for_a_job_code_map['0200']}


def get_applicants_information(job_offer_id):
    applicants_information_response = Manager.get_applicants_information(job_offer_id=job_offer_id,
                                                                         request_id=g.request_id)

    if not applicants_information_response['ok']:
        logger.info(f"{g.request_id} - error al obtener informacion de las postulaciones")
        return {'code': '0500',
                'description': ServiceConfig.get_applicants_information_code_map['0500']}

    logger.info(f"{g.request_id} - informacion de las postulaciones obtenida correctamente")

    #formateo de datos

    data_formatted = Utils.format_candidate_experience(applicants_information_response['data'])
    return {'code': '0200',
            'description': ServiceConfig.get_applicants_information_code_map['0200'],
            'data': applicants_information_response['data']}


def get_available_jobs(company_id):
    available_jobs_response = Manager.get_available_jobs(company_id=company_id,
                                                         request_id=g.request_id)

    logger.info(f"{g.request_id} - empleos disponibles response {available_jobs_response}")
    if not available_jobs_response['ok']:
        logger.info(f"{g.request_id} - error al obtener empleos disponibles")
        return {'code': '0500',
                'description': ServiceConfig.get_available_jobs_code_map['0500']}

    logger.info(f"{g.request_id} - informacion de los empleos disponibles obtenida correctamente")

    logger.info(f"{g.request_id} - se encontraron {len(available_jobs_response['data'])} registros")

    return {'code': '0200',
            'description': ServiceConfig.get_available_jobs_code_map['0200'],
            'data': available_jobs_response['data']}


def get_user_applications(candidate_id):
    user_applications_response = Manager.get_user_applications(candidate_id=candidate_id,
                                                               request_id=g.request_id)

    if not user_applications_response['ok']:
        logger.info(f"{g.request_id} - error al obtener postulaciones del usuario")
        return {'code': '0500',
                'description': ServiceConfig.get_user_applications_code_map['0500']}

    logger.info(f"{g.request_id} - informacion de postulaciones obtenida correctamente")
    logger.info(f"{g.request_id} - se encontraron {len(user_applications_response['data'])} registros")

    return {'code': '0200',
            'description': ServiceConfig.get_user_applications_code_map['0200'],
            'data': user_applications_response['data']}


def get_application_status(application_id):
    application_status_response = Manager.get_application_status(application_id=application_id,
                                                                 request_id=g.request_id)

    if not application_status_response['ok']:
        logger.info(f"{g.request_id} - error al obtener postulaciones del usuario")
        return {'code': '0500',
                'description': ServiceConfig.get_applications_status_code_map['0500']}

    if not application_status_response['data']:
        logger.info(f"{g.request_id} - no se encontro informacion de la postulacion")
        return {'code': '0404',
                'description': ServiceConfig.get_applications_status_code_map['0404']}
    logger.info(f"{g.request_id} - estado de postulacion obtenido correctamente")

    return {'code': '0200',
            'description': ServiceConfig.get_applications_status_code_map['0200'],
            'data': application_status_response['data']}


def get_applications_with_company_id(company_id):
    # todo agregar logs con datos de busqueda
    logger.info(f"{g.request_id} - buscando postulaciones para la compania: {company_id}")

    applications_response = Manager.get_application_with_company_id(company_id=company_id,
                                                                    request_id=g.request_id)

    if not applications_response['ok']:
        logger.info(f"{g.request_id} - error al obtener postulaciones")
        return {'code': '0500',
                'description': ServiceConfig.get_applications_with_company_id_code_map['0500']}

    if not applications_response['data']:
        logger.info(f"{g.request_id} - no se encontraron postulaciones")
        return {'code': '0404',
                'description': ServiceConfig.get_applications_with_company_id_code_map['0404']}
    logger.info(f"{g.request_id} - postulaciones obtenidas correctamente")

    return {'code': '0200',
            'description': ServiceConfig.get_applications_with_company_id_code_map['0200'],
            'data': applications_response['data']}


def change_application_status(application_id, new_status):
    logger.info(f"{g.request_id} - cambiando estado de la postulacion: {application_id}")
    logger.info(f"{g.request_id} - nuevo estado: {new_status}")

    status_validation = Utils.status_validation(new_status=new_status)

    if not status_validation:
        logger.info(f"{g.request_id} - estado invalido")
        return {'code': '0405',
                'description': ServiceConfig.change_application_status_code_map['0405']}

    logger.info(f"{g.request_id} - se valido el nuevo estado")

    application_status_response = Manager.get_application_status(application_id=application_id,
                                                                 request_id=g.request_id)

    if not application_status_response['ok']:
        logger.info(f"{g.request_id} - error al obtener postulaciones del usuario")
        return {'code': '0500',
                'description': ServiceConfig.change_application_status_code_map['0500']}

    if not application_status_response['data']:
        logger.info(f"{g.request_id} - no se encontro registro de la postulacion")
        return {'code': '0404',
                'description': ServiceConfig.change_application_status_code_map['0404']}

    logger.info(f"{g.request_id} - postulacion obtenida correctamente")

    old_status = application_status_response['data']['status']

    if new_status == old_status:
        logger.info(f"{g.request_id} - el nuevo estado es el mismo que esta registrado")
        return {'code': '0410',
                'description': ServiceConfig.change_application_status_code_map['0410']}

    logger.info(f"{g.request_id} - se valido que el nuevo estado es valido y no es el mismo al que esta registrado")

    change_status_response = Manager.change_application_status(application_id=application_id,
                                                               new_status=new_status,
                                                               request_id=g.request_id)

    if not change_status_response['ok']:
        logger.info(f"{g.request_id} - error modificar estado de la postulacion")
        return {'code': '0500',
                'description': ServiceConfig.change_application_status_code_map['0500']}

    logger.info(f"{g.request_id} - estado de la postulacion modificado correctamente")

    return {'code': '0200',
            'description': ServiceConfig.change_application_status_code_map['0200']}


def get_stats(total_candidates, total_companies, total_job_offers, successful_job_offers):
    data = {'total_candidates': {},
            'total_companies': {},
            'total_job_offers': {},
            'successful_job_offers': {}}

    if total_candidates:
        total_candidates_response = Manager.get_total_candidates_data(request_id=g.request_id)

        if not total_candidates_response['ok']:
            logger.info(f"{g.request_id} - error al obtener informacion del total de candidatos")
            return {'code': '0500',
                    'description': ServiceConfig.get_stats_code_map['0500']}

        logger.info(f"{g.request_id} - estadisticas de los candidatos obtenida correctamente")
        data['total_candidates'] = total_candidates_response['data']

    if total_companies:
        total_companies_response = Manager.get_total_companies_data(request_id=g.request_id)

        if not total_companies_response['ok']:
            logger.info(f"{g.request_id} - error al obtener informacion del total de candidatos")
            return {'code': '0500',
                    'description': ServiceConfig.get_stats_code_map['0500']}

        logger.info(f"{g.request_id} - estadisticas de las empresas obtenidas correctamente")
        data['total_companies'] = total_companies_response['data']

    if total_job_offers:
        total_job_offers_response = Manager.get_total_job_offers(request_id=g.request_id)

        if not total_job_offers_response['ok']:
            logger.info(f"{g.request_id} - error al obtener informacion del total de candidatos")
            return {'code': '0500',
                    'description': ServiceConfig.get_stats_code_map['0500']}

        logger.info(f"{g.request_id} - estadisticas de las ofertas de trabajo obtenidas correctamente")
        data['total_candidates'] = total_job_offers_response['data']

    if successful_job_offers:
        successful_job_offers_response = Manager.get_total_successful_job_offers(request_id=g.request_id)

        if not successful_job_offers_response['ok']:
            logger.info(f"{g.request_id} - error al obtener informacion del total de candidatos")
            return {'code': '0500',
                    'description': ServiceConfig.get_stats_code_map['0500']}

        logger.info(f"{g.request_id} - estadisticas de las ofertas de trabajo exitosas obtenidas correctamente")
        data['total_candidates'] = successful_job_offers_response['data']

    return {'code': '0200',
            'description': ServiceConfig.get_stats_code_map['0200'],
            'data': data}


def get_companies_list():
    logger.info(f"{g.request_id} - consultando lista de las empresas registradas")

    companies_list_response = Manager.get_companies_list(request_id=g.request_id)

    if not companies_list_response['data']:
        logger.error(f"{g.request_id} - error al obtener lista de empresas")
        return {'code': '0500',
                'description': ServiceConfig.get_companies_list_code_map['0500']}

    logger.info(f"{g.request_id} - informacion obtenida correctamente")

    logger.info(f"{g.request_id} - se obtuvieron {len(companies_list_response['data'])} empresas")

    return {'code': '0200',
            'description': ServiceConfig.get_stats_code_map['0200'],
            'data': companies_list_response['data']}


def upload_work_experience(candidate_id, job_id, company_id, start_date, end_date):
    # todo validar job_id, company_id

    # validamos que el usuario exista
    candidate_is_registered_response = Manager.user_registered(candidate_id=candidate_id,request_id=g.request_id)

    if not candidate_is_registered_response['data']:
        logger.error(f"{g.request_id} - error al validar existencia del candidato")
        return {'code': '0500',
                'description': ServiceConfig.upload_experience_response['0500']}

    if not candidate_is_registered_response['data']:
        logger.error(f"{g.request_id} - no se encontro que el usuario este registrado en bd")
        return {'code': '0406',
                'description': ServiceConfig.upload_experience_response['0406']}

    # validamos el id del trabajo exista
    job_exists_response = Manager.job_exists(job_id=job_id,
                                             request_id=g.request_id)

    if not job_exists_response['data']:
        logger.error(f"{g.request_id} - error al validar existencia del trabajo")
        return {'code': '0500',
                'description': ServiceConfig.upload_experience_response['0500']}

    if not job_exists_response['data']:
        logger.error(f"{g.request_id} - no se encontro que el trabajo este registrado en bd")
        return {'code': '0405',
                'description': ServiceConfig.upload_experience_response['0405']}

    # validamos el id de compania exista
    company_exists_response = Manager.company_exists(company_id=company_id,
                                                     request_id=g.request_id)

    if not company_exists_response['data']:
        logger.error(f"{g.request_id} - error al validar existencia del trabajo")
        return {'code': '0500',
                'description': ServiceConfig.upload_experience_response['0500']}

    if not company_exists_response['data']:
        logger.error(f"{g.request_id} - no se encontro que la compania este registrada en bd")
        return {'code': '0407',
                'description': ServiceConfig.upload_experience_response['0407']}

    # una vez esta tdo validado, insetamos la experiencia
    upload_experience_response = Manager.upload_work_experience(candidate_id=candidate_id,
                                                                job_id=job_id,
                                                                company_id=company_id,
                                                                start_date=start_date,
                                                                end_date=end_date,
                                                                request_id=g.request_id)

    if not upload_experience_response['data']:
        logger.error(f"{g.request_id} - error al obtener lista de empresas")
        return {'code': '0500',
                'description': ServiceConfig.upload_experience_response['0500']}

    logger.info(f"{g.request_id} - experiencia de usuario cargada correctamente")

    return {'code': '0200',
            'description': ServiceConfig.get_stats_code_map['0200']}


def get_job_type_list():
    job_type_list = Manager.get_job_type_list(request_id=g.request_id)

    if not job_type_list['ok']:
        logger.error(f"{g.request_id} - error al consultar trabajos registrados")
        return {'code': '0500',
                'description': ServiceConfig.get_job_type_list_code_map['0500']}

    logger.info(f"{g.request_id} - lista de empleos registrados obtenida correctamente.")
    logger.info(f"{g.request_id} - se obtuvieron {len(job_type_list['data'])} empleos de la base de datos")

    return {'code': '0200',
            'description': ServiceConfig.get_job_type_list_code_map['0200'],
            'data': job_type_list['data']}


def get_skills_list():
    skill_list_response = Manager.get_skills_list(request_id=g.request_id)

    if not skill_list_response['ok']:
        logger.error(f"{g.request_id} - error al consultar trabajos registrados")
        return {'code': '0500',
                'description': ServiceConfig.get_job_type_list_code_map['0500']}

    logger.info(f"{g.request_id} - lista de habilidades obtenida correctamente.")
    logger.info(f"{g.request_id} - se obtuvieron {len(skill_list_response['data'])} habilidades de la base de datos")

    return {'code': '0200',
            'description': ServiceConfig.get_job_type_list_code_map['0200'],
            'data': skill_list_response['data']}

