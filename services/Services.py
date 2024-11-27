from flask import Blueprint, g, request

from config import ServerConfig
from controllers import AuthController, Controller

logger = ServerConfig.rootLogger.getChild(__name__)
SERVICE_NAME = 'v1'
bp = Blueprint("Services", __name__, url_prefix='/portalEmpleos/' + SERVICE_NAME + '/')

@bp.route('/echo',methods=['POST'])
def echo():
    logger.info(f"{g.request_id} - ingresando a echo")
    return {'code': '0200',
            'description': 'ok'}

# 1)
# Servicio que se encarga de registrar generar usuario para un candidato
@bp.route('/registerCandidateUser', methods=['POST'])
@AuthController.token_required(endpoint='registerCandidateUser', service_required=False)
def register_candidate_user(data_request):
    logger.info(f"{g.request_id} - ingresando a registerCandidateUser")

    try:
        name = data_request['name']
        last_name = data_request['last_name']
        email = data_request['email']
        password = data_request['password']
        resume_url = data_request['resume_url']
        skill_list = data_request['skill_list']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.register_candidate_user(name=name,
                                              last_name=last_name,
                                              email=email,
                                              password=password,
                                              resume_url=resume_url,
                                              skill_list=skill_list)


# 2)
# Servicio que se encarga de registrar generar usuario para un empleador o reclutador
@bp.route('/registerEmployerUser', methods=['POST'])
@AuthController.token_required(endpoint='registerEmployerUser', service_required=False)
def register_employer_user(data_request):
    logger.info(f"{g.request_id} - ingresando a registerEmployerUser")

    try:
        name = data_request['name']
        last_name = data_request['last_name']
        email = data_request['email']
        password = data_request['password']
        company_id = data_request['company_id']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.register_employer_user(name=name,
                                             last_name=last_name,
                                             email=email,
                                             password=password,
                                             company_id=company_id)


# 3)
# Servicio que realiza el loggeo y del proceso necesario para poder ingresar a la aplicación y operar.
@bp.route('/login', methods=['POST'])
@AuthController.token_required(endpoint='login', service_required=False)
def login(data_request):
    logger.info(f"{g.request_id} - ingresando a login")

    try:
        email = data_request['email']
        password = data_request['password']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.login(email=email,
                            password=password)


# 4)
# Indica el proceso de carga de nuevas empresas en el portal.
@bp.route('/createNewCompany', methods=['POST'])
@AuthController.token_required(endpoint='createNewCompany', service_required=False)
@AuthController.employer_validation()
def create_new_company(data_request):
    logger.info(f"{g.request_id} - ingresando a createNewCompany")

    try:
        name = data_request['name']
        description = data_request['description']
        tax_id = data_request['tax_id']
        company_type = data_request['company_type']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.create_new_company(name=name,
                                         description=description,
                                         tax_id=tax_id,
                                         company_type=company_type)


# 5)
# En caso de que al cargar una nueva propuesta laboral no exista el tipo de trabajo solicitado,
# se podrá cargar a través de este servicio
@bp.route('/createNewJob', methods=['POST'])
@AuthController.token_required(endpoint='createNewJob', service_required=False)
@AuthController.employer_validation()
def create_new_job(data_request):
    logger.info(f"{g.request_id} - ingresando a createNewJob")

    try:
        name = data_request['name']
        description = data_request['description']
        requirements = data_request['requirements']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.create_new_job(name=name,
                                     description=description,
                                     requirements=requirements)


# 6)
# Una vez el empleador haya creado su cuenta correctamente,
# podrá crear un anuncio para una oferta laboral con este servicio
@bp.route('/createJobOffer', methods=['POST'])
@AuthController.token_required(endpoint='createJobOffer', service_required=False)
@AuthController.employer_validation()
def create_job_offer(data_request):
    logger.info(f"{g.request_id} - ingresando a createJobOffer")

    try:
        company_id = data_request['company_id']
        job_id = data_request['job_id']
        salary = data_request['salary']
        location = data_request['location']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.create_job_offer(company_id=company_id,
                                       job_id=job_id,
                                       salary=salary,
                                       location=location)


# 7)
# Postulación de un candidato a una oferta de trabajo
# Una vez que el usuario haya creado su cuenta de candidato correctamente,
# podrá presentarse a los puestos de trabajo que desee
@bp.route('/applyForAJob', methods=['POST'])
@AuthController.token_required(endpoint='applyForAJob', service_required=False)
@AuthController.candidate_validation()
def apply_for_a_job(data_request):
    logger.info(f"{g.request_id} - ingresando a applyForAJob")

    try:
        job_offer_id = data_request['job_offer_id']
        candidate_id = data_request['candidate_id']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.apply_for_a_job(job_offer_id=job_offer_id, candidate_id=candidate_id)


# 8)
# Obtener datos de las postulaciones
# Como empleador, se pueden consultar los candidatos postulados para el puesto
# todo validar que el user que consume el servicio sea un empleador/reclutador
@bp.route('/getApplicantsInformation', methods=['POST'])
@AuthController.token_required(endpoint='getApplicantsInformation', service_required=False)
@AuthController.employer_validation()
def get_applicants_information(data_request):
    logger.info(f"{g.request_id} - ingresando a /getApplicantsInformation")

    try:
        job_offer_id = data_request['job_offer_id']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.get_applicants_information(job_offer_id=job_offer_id)


# 9)
# Obtener los empleos disponibles
# Como candidato, se pueden consultar los puestos de trabajo disponibles.
@bp.route('/getAvailableJobs', methods=['POST'])
@AuthController.token_required(endpoint='getAvailableJobs', service_required=False)
@AuthController.candidate_validation()
def get_available_jobs(data_request):
    logger.info(f"{g.request_id} - ingresando a /getAvailableJobs")

    try:
        if 'company_id' in data_request:
            company_id = data_request['company_id']
        else:
            company_id = None
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.get_available_jobs(company_id=company_id)


# 10)
# Consultar postulaciones de un usuario
# Se obtiene una lista de postulaciones (vigentes o no) del usuario seleccionado.
@bp.route('/getUserApplications', methods=['POST'])
@AuthController.token_required(endpoint='getUserApplications', service_required=False)
@AuthController.candidate_validation()
def get_user_applications(data_request):
    logger.info(f"{g.request_id} - ingresando a /getUserApplications")

    try:
        candidate_id = data_request['candidate_id']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.get_user_applications(candidate_id=candidate_id)


# 11)
# Consultar estado de una postulación
# A través de este servicio se puede consultar si una postulación está vigente,
# en revisión o rechazada.
@bp.route('/getApplicationStatus', methods=['POST'])
@AuthController.token_required(endpoint='getApplicationStatus', service_required=False)
def get_application_status(data_request):
    logger.info(f"{g.request_id} - ingresando a /getApplicationStatus")

    try:
        # el application_id se obtiene de
        application_id = data_request['application_id']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.get_application_status(application_id=application_id)


# 12)
# Obtener postulaciones para la compañía indicada
# Los empleadores de cada compañía pueden consultar las solicitudes vigentes
@bp.route('/getApplicationsWithCompanyId', methods=['POST'])
@AuthController.token_required(endpoint='getApplicationsWithCompanyId', service_required=False)
def get_applications_with_company_id(data_request):
    logger.info(f"{g.request_id} - ingresando a /getApplicationsWithCompanyId")

    try:
        company_id = data_request['company_id']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.get_applications_with_company_id(company_id=company_id)


# 13)
# Cambiar estado de una postulación
# El empleador puede aceptar o rechazar una postulación.
@bp.route('/changeApplicationStatus', methods=['POST'])
@AuthController.token_required(endpoint='changeApplicationStatus', service_required=False)
@AuthController.employer_validation()
def change_application_status(data_request):
    logger.info(f"{g.request_id} - ingresando a /changeApplicationStatus")

    try:
        application_id = data_request['application_id']
        new_status = data_request['new_status']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.change_application_status(application_id=application_id,
                                                new_status=new_status)


# 14)
# Obtener estadísticas
# Este servicio sirve para obtener estadísticas de las postulaciones,
# los candidatos y/o las empresas
@bp.route('/getStats', methods=['POST'])
@AuthController.token_required(endpoint='getStats', service_required=False)
def get_stats(data_request):
    logger.info(f"{g.request_id} - ingresando a /getStats")

    try:
        total_candidates = None
        total_companies = None
        total_job_offers = None
        successful_job_offers = None

        if 'total_candidates' in data_request:
            total_candidates = data_request['total_candidates']

        if 'total_companies' in data_request:
            total_companies = data_request['total_companies']

        if 'total_job_offers' in data_request:
            total_job_offers = data_request['total_job_offers']

        if 'successful_job_offers' in data_request:
            successful_job_offers = data_request['successful_job_offers']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")
    return Controller.get_stats(total_candidates=total_candidates,
                                total_companies=total_companies,
                                total_job_offers=total_job_offers,
                                successful_job_offers=successful_job_offers)


# 15)
# Obtener lista de compañias
# Servicio utilizado para mostrar las compañías en front al momento de
# hacer un onboarding de empleador
@bp.route('/getCompaniesList', methods=['POST'])
@AuthController.token_required(endpoint='getCompanies', service_required=False)
def get_companies_list(data_request):
    logger.info(f"{g.request_id} - ingresando a /getCompaniesList")

    return Controller.get_companies_list()


# 16)
# Cargar experiencia laboral
# Servicio utilizado por los candidatos una vez loggeados para cargar su experiencia laboral
@bp.route('/uploadWorkExperience', methods=['POST'])
@AuthController.token_required(endpoint='uploadWorkExperience', service_required=False)
def upload_work_experience(data_request):
    logger.info(f"{g.request_id} - ingresando a /uploadWorkExperience")

    try:
        candidate_id = data_request['candidate_id']
        job_id = data_request['job_id']
        company_id = data_request['company_id']
        start_date = data_request['start_date']
        end_date = data_request['end_date']
    except:
        logger.exception(f"{g.request_id} - mensaje malformado")
        return {"code": "0400", "description": "bad request"}, 400

    logger.info(f"{g.request_id} - validacion de datos exitosa")

    return Controller.upload_work_experience(candidate_id=candidate_id,
                                             job_id=job_id,
                                             company_id=company_id,
                                             start_date=start_date,
                                             end_date=end_date)


# 17)
# Obtener lista de tipos de trabajos
# Servicio utilizado para mostrar los tipos de trabajo
# al momento de cargar la experiencia del usuario
@bp.route('/getJobTypeList', methods=['POST'])
@AuthController.token_required(endpoint='getJobTypeList', service_required=False)
def get_job_type_list(data_request):
    logger.info(f"{g.request_id} - ingresando a /getJobTypeList")

    logger.info(f"{g.request_id} - validacion de datos exitosa")

    return Controller.get_job_type_list()


# 18)
# Obtener lista de habilidades registradas
# Servicio utilizado para mostrar las habilidades
# registradas en base de datos, necesarias para el momento de onboarding de un usuario
@bp.route('/getSkillsList', methods=['POST'])
@AuthController.token_required(endpoint='getSkillsList', service_required=False)
def get_skills_list(data_request):
    logger.info(f"{g.request_id} - ingresando a /getSkillsList")

    logger.info(f"{g.request_id} - validacion de datos exitosa")

    return Controller.get_skills_list()


@bp.route('/getLocations', methods=['POST'])
@AuthController.token_required(endpoint='getLocations', service_required=False)
def get_locations(data_request):
    logger.info(f"{g.request_id} - consultando ubicaciones")

    return Controller.get_locations()