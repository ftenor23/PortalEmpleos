from config import ServerConfig
from managers.ConnectionManager import manage_db_connection
logger = ServerConfig.rootLogger.getChild(__name__)


@manage_db_connection
def get_user_data_login(cnx, cursor, final_response,user_id, is_candidate, request_id=None):
    final_response = {'ok': True,
                      'data': {}}

    try:
        if is_candidate:
            role = '0'
        else:
            role = '1'

        query_get_user_id = """
                                    SELECT  name,
                                            last_name
                                    FROM    usuarios
                                    WHERE   user_id = %s 
                                    AND     role = %s  
                            """
        values = (user_id, role)
        cursor.execute(query_get_user_id, values)
        results_dict = cursor.fetchone()

        if not results_dict:
            logger.info(f"{request_id} - no se encontraron registros")
            final_response['data'] = False

        else:
            logger.info(f"{request_id} - usuario encontrado")
            final_response['data'] = results_dict
    except:
        logger.exception(f"{request_id} - error al obtener datos del usuario {user_id}")
        final_response['ok'] = False

    return final_response


@manage_db_connection
def user_registered(cnx, cursor, final_response, email=None, is_candidate=None, candidate_id = None, request_id=None):

    try:
        if candidate_id:
            query = f'''
                                SELECT  * 
                                FROM    Usuarios
                                WHERE   user_id = %s
                                AND     role = 0'''
            values = (candidate_id,)

        elif is_candidate:
            query = f'''
                    SELECT  * 
                    FROM    Usuarios
                    WHERE   email = %s
                    AND     role = 0'''
            values = (email,)
        else:
            query = f'''
                                SELECT  * 
                                FROM    Usuarios
                                WHERE   email = %s
                                AND     role = 1'''
            values = (email,)

        #si no es candidato, es empleador
        cursor.execute(query, values)
        results_dict = cursor.fetchone()

        final_response['data'] = results_dict
    except:
        logger.exception(f"{request_id} - {request_id} {request_id}error al acceder a la bd")
        final_response['ok'] = False
    return final_response

#se usa la misma funcion para generar usuario candidato o empleador
@manage_db_connection
def create_user(cnx, cursor, final_response, name, last_name, email, password, is_candidate, request_id=None):

    try:
        #role = 0 -> candidato
        #role = 1 -> empleador

        query_users = f"""
                            INSERT INTO 
                            Usuarios 
                                        (name, 
                                         last_name, 
                                         email, 
                                         encrypted_password, 
                                         role) 
                            VALUES 
                                        (%s, 
                                         %s, 
                                         %s, 
                                         %s, 
                                         %s)"""
        if is_candidate:
            logger.info(f"{request_id} - insertando candidato en tabla usuarios")
            values = (name, last_name, email, password, "0")
        else:
            logger.info(f"{request_id} - insertando empleador en tabla usuarios")
            values = (name, last_name, email, password, "1")

        cursor.execute(query_users, values)
        cnx.commit()

        logger.info(f"{request_id} - usuario insertado correctamente en tabla Usuarios")


    except:
        logger.exception(f"{request_id} - error al generar usuario")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def insert_employer_actual_company(cnx, cursor, final_response, user_id, company_id, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    logger.info(f"{request_id} - insertando lugar de trabajo actual del {user_id}")

    try:
        query = """
                    INSERT INTO
                    empresas_x_usuario (user_id, 
                                        company_id)
                    VALUES              (%s,
                                        %s)
                    """
        values = (user_id, company_id)

        cursor.execute(query, values)
        cnx.commit()

        logger.info(f"{request_id} - {request_id} - lugar de trabajo cargado correctamente")

    except:
        logger.exception(f"{request_id} - error al cargar lugar de trabajo")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def get_user_id_with_email(cnx, cursor, final_response, email, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:
        # Una vez generado el usuario, consultamos el id usuario para realizar inserts posteriores
        # Buscamos por mail ya que es una unique key
        query_get_user_id = """
                                    SELECT  user_id
                                    FROM    usuarios
                                    WHERE   email = %s 
                                    """
        values = (email,)
        cursor.execute(query_get_user_id, values)
        results_dict = cursor.fetchone()

        if results_dict:
            user_id = results_dict['user_id']
            logger.info(f"{request_id} - usuario dado de alta: {user_id}")
            final_response['data'] = {'user_id': user_id}
    except:
        logger.exception(f"{request_id} - error al obtener user_id")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def insert_candidate_resume_url(cnx, cursor, final_response, user_id, resume_url, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    logger.info(f"{request_id} - insertando url del cv del usuario {user_id}")

    try:
        query = """
                INSERT INTO
                candidatos (candidate_id, 
                            resume_url)
                VALUES 
                           (%s,
                            %s)
                """
        values = (user_id, resume_url)

        cursor.execute(query, values)
        cnx.commit()

        logger.info(f"{request_id} - cv cargado correctamente")

    except:
        logger.exception(f"{request_id} - error al insertar cv")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def insert_candidate_skills(cnx, cursor, final_response, skill_list, user_id, request_id=None):
    final_response = {'ok': True,
                      'data': {}}

    try:

        query = """
                INSERT INTO 
                habilidades_x_candidato 
                        (skill_id, 
                        candidate_id) 
                VALUES  (%s, 
                        %s)
                """
        # Creamos una lista de tuplas para la inserción
        values = [(skill_id, user_id) for skill_id in skill_list]

        cursor.executemany(query, values)
        cnx.commit()

        logger.info(f"{request_id} - se insertaron {len(skill_list)} habilidades para el user {user_id}")

    except:
        logger.exception(f"{request_id} - error al insertar habilidades en base de datos")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def get_user_data(cnx, cursor, final_response, email, password, request_id=None):
    final_response = {'ok': True,
                      'data': False}
    try:

        query_login = """
                    SELECT  user_id,
                            name,
                            last_name
                    FROM    usuarios
                    WHERE   email = %s 
                    AND     encrypted_password = %s
                      """
        #en este punto habria que desencriptar la password?
        values = (email, password)
        cursor.execute(query_login, values)
        results_dict = cursor.fetchone()

        # si se encuentra un usuario con los datos ingresados, se devuelve la data
        if results_dict:
            user_id = results_dict['user_id']
            first_name = results_dict['name']
            last_name = results_dict['last_name']
            final_response['data'] = {'user_id': user_id,
                                      'first_name': first_name,
                                      'last_name': last_name}

    except:
        logger.exception(f"{request_id} - error al realizar login")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def company_exists(cnx, cursor, final_response, company_id=None, tax_id=None, request_id=None):
    #verificamos si ya existe una empresa registrada con ese CUIT. si existe, devolvemos data= True
    final_response = {'ok': True,
                      'data': False}

    try:
        if company_id:
            query = """
                        SELECT  *
                        FROM    Empresas
                        WHERE   company_id = %s 
                    """
        # en este punto habria que desencriptar la password?
            values = (company_id,)

        elif tax_id:
            query = """
                        SELECT  *
                        FROM    Empresas
                        WHERE   tax_id = %s 
                    """
            values = (tax_id,)

        else:
            raise()

        cursor.execute(query, values)
        results_dict = cursor.fetchone()

        if results_dict:
            logger.info(f"{request_id} - se encontro una empresa")
            final_response['data'] = True
        else:
            logger.info(f"{request_id} - no se encontro empresa para los datos indicados")
    except:
        logger.exception(f"{request_id} - error al buscar empresa por cuit/id")
        final_response['ok'] = False
    return final_response

@manage_db_connection
def create_new_company(cnx, cursor, final_response, name, description, tax_id, company_type, request_id=None):
    final_response = {'ok': True,
                      'data': {}}

    try:

        query = """
                    INSERT INTO 
                    Empresas
                            (name, 
                            description,
                            tax_id, 
                            company_type) 
                    VALUES  (%s, 
                            %s,
                            %s,
                            %s)
                    """
        # Creamos una lista de tuplas para la inserción
        values = (name, description, tax_id, company_type)

        cursor.execute(query, values)
        cnx.commit()

        #todo seguir
        logger.info(f"{request_id} - se cargo correctamente la empresa {name}")

    except:
        logger.exception(f"{request_id} - error al cargar nueva empresa")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def job_exists(cnx, cursor, final_response, name=None,description=None, requirements=None, job_id=None, request_id=None):
    #verificamos si ya existe un trabajo registrado. si existe, devolvemos data= True
    final_response = {'ok': True,
                      'data': False}

    try:
        if job_id:
            #si se envia job_id, usamos ese criterio de busqueda
            query_job = '''
                        SELECT  *
                        FROM    Empleos
                        WHERE   job_id = %s
                    '''
            values = (job_id,)
        else:
            query_job = '''
                            SELECT  *
                            FROM    Empleos
                            WHERE   title = %s 
                            AND     description = %s
                            AND     requirements = %s
                        '''

            values = (name, description, requirements)
        cursor.execute(query_job, values)
        results_dict = cursor.fetchone()

        if not results_dict:
            logger.info(f"{request_id} - el empleo no esta registrado")
            final_response['data'] = False
        else:
            logger.info(f"{request_id} - {request_id} - se encontro un empleo registrado")
            final_response['data'] = True
    except:
        logger.exception(f"{request_id} - {request_id} - error al buscar si el empleo ya esta registrado")
        final_response['ok'] = False
    return final_response

@manage_db_connection
def create_new_job(cnx, cursor, final_response, name, description, requirements, request_id=None):
    final_response = {'ok': True,
                      'data': {}}

    try:

        query = """
                        INSERT INTO 
                        Empleos
                                (title, 
                                description,
                                requirements) 
                        VALUES  (%s, 
                                %s,
                                %s)
                        """
        # Creamos una lista de tuplas para la inserción
        values = (name, description, requirements)

        cursor.execute(query, values)
        cnx.commit()

        # todo seguir
        logger.info(f"{request_id} - se cargo correctamente el nuevo tipo de trabajo: {name}")

    except:
        logger.exception(f"{request_id} - error al cargar nueva empresa")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def job_offer_exists(cnx, cursor, final_response, company_id, job_id, salary, location, request_id=None):
    # verificamos si ya existe una oferta de trabajo registrada. si existe, devolvemos data= True
    final_response = {'ok': True,
                      'data': True}

    try:
        #verificamos que haya una busqueda activa (status = 1)
        query = '''
                SELECT  *
                FROM    Empleos_Disponibles
                WHERE   company_id = %s
                AND     job_id = %s
                AND     salary = %s
                AND     location_id = %s
                AND     status = 1
            '''

        values = (company_id, job_id, salary, location)
        cursor.execute(query, values)
        results_dict = cursor.fetchone()

        if not results_dict:
            logger.info(f"{request_id} - la oferta de trabajo no existe o no esta mas activa")
            final_response['data'] = False
        else:
            logger.info(f"{request_id} - {request_id} - la oferta se encuentra activa")
    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def create_new_job_offer(cnx, cursor, final_response, company_id, job_id, salary, location, request_id=None):
    final_response = {'ok': True,
                      'data': {}}

    try:

        query = """
                        INSERT INTO 
                        Empleos_Disponibles
                                (company_id, 
                                job_id,
                                salary,
                                location_id,
                                publication_date,
                                status) 
                        VALUES  (%s, 
                                %s,
                                %s,
                                %s,
                                NOW(),
                                1)
                        """
        # Creamos una lista de tuplas para la inserción
        values = (company_id, job_id, salary, location)

        cursor.execute(query, values)
        cnx.commit()

        logger.info(f"{request_id} - se cargo correctamente el la nueva oferta de trabajo")

    except:
        logger.exception(f"{request_id} - error al acceder a la base de datos")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def job_offer_is_active(cnx, cursor, final_response, job_offer_id, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:
        #verificamos que haya una busqueda activa (status = 1)
        query = '''
                SELECT  *
                FROM    Empleos_Disponibles
                WHERE   job_offer_id = %s
                AND     status = 1
                '''

        values = (job_offer_id,)
        cursor.execute(query, values)
        results_dict = cursor.fetchone()

        if not results_dict:
            logger.info(f"{request_id} - la oferta de trabajo no esta mas activa")
            final_response['data'] = False
        else:
            logger.info(f"{request_id} - {request_id} - la oferta se encuentra activa")
            final_response['data'] = True

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def user_already_applied_for_job(cnx, cursor, final_response, job_offer_id, candidate_id, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:
        #verificamos que haya una busqueda activa (status = 1)
        query = '''
                SELECT  *
                FROM    Solicitudes
                WHERE   job_offer_id = %s
                AND     candidate_id = %s
                '''

        values = (job_offer_id, candidate_id)
        cursor.execute(query, values)
        results_dict = cursor.fetchone()

        if not results_dict:
            logger.info(f"{request_id} - el usuario no esta postulado a la oferta")
            final_response['data'] = False
        else:
            logger.info(f"{request_id} - {request_id} - el usuario ya se postulo previamente")
            final_response['data'] = True

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    #devolver data = True en caso de que se haya postulado
    return final_response

@manage_db_connection
def job_application(cnx, cursor, final_response, job_offer_id, candidate_id, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:
        # se inserta con status = 3 -->> solicitud recibida

        query = """
                INSERT INTO 
                Solicitudes
                        (job_offer_id,
                        candidate_id,
                        application_date,
                        status) 
                VALUES  (%s, 
                        %s,
                        NOW(),
                        3)
                """
        # Creamos una lista de tuplas para la inserción
        values = (job_offer_id, candidate_id)

        cursor.execute(query, values)
        cnx.commit()

        logger.info(f"{request_id} - se cargo correctamente la postulacion")

    except:
        logger.exception(f"{request_id} - error al acceder a la base de datos")
        final_response['ok'] = False

    #devolver data = True en caso de que se haya postulado
    return final_response

@manage_db_connection
def get_applicants_information(cnx, cursor, final_response, job_offer_id, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:
        #todo verificar query
        #verificamos que haya una busqueda activa (status = 1)
        query = '''
                SELECT 
                    u.name AS first_name,
                    u.last_name AS last_name,
                    c.resume_url,
                    u.email,
                    GROUP_CONCAT(DISTINCT s.name) AS skills,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'job_name', e.title,
                            'start_date', ex.start_date,
                            'end_date', ex.end_date,
                            'company_name', em.name
                        )
                    ) AS experience
                FROM 
                    Solicitudes sol
                JOIN 
                    Candidatos c ON sol.candidate_id = c.candidate_id
                JOIN 
                    Usuarios u ON c.candidate_id = u.user_id
                LEFT JOIN 
                    Habilidades_x_Candidato hc ON c.candidate_id = hc.candidate_id
                LEFT JOIN 
                    Habilidades s ON hc.skill_id = s.skill_id
                LEFT JOIN 
                    Experiencias ex ON c.candidate_id = ex.candidate_id
                LEFT JOIN 
                    Empleos e ON ex.job_id = e.job_id
                LEFT JOIN 
                    Empresas em ON ex.company_id = em.company_id
                WHERE 
                    sol.job_offer_id = %s
                GROUP BY 
                    u.user_id;
                ;
                '''

        values = (job_offer_id,)
        cursor.execute(query, values)
        results_dict = cursor.fetchall()

        if not results_dict:
            logger.info(f"{request_id} - no se encontraron usuarios postulados")
        else:
            logger.info(f"{request_id} - {request_id} - se encontro informacion de los usuarios")
            final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    #en data se devuelve informacion de las querys
    return final_response

@manage_db_connection
def get_available_jobs(cnx, cursor, final_response, company_id, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:
        #verificamos que haya una busqueda activa (status = 1)
        if company_id:
            query = '''
                    SELECT 
                        em.name AS company_name,
                        em.company_id,
                        e.title AS job_title,
                        e.description AS job_description,
                        e.requirements,
                        CAST(ed.salary AS CHAR) AS salary,
                        u.name AS location
                    FROM 
                        Empresas em
                    JOIN 
                        Empleos_Disponibles ed ON em.company_id = ed.company_id
                    JOIN 
                        Empleos e ON ed.job_id = e.job_id
                    JOIN 
                        Ubicaciones u ON ed.location_id = u.location_id
                    WHERE 
                        em.company_id = %s
                        AND ed.status = 1;
                    '''

            values = (company_id,)
            cursor.execute(query, values)

        else:
            query = '''
                    SELECT 
                        em.name AS company_name,
                        em.company_id,
                        e.title AS job_title,
                        e.description AS job_description,
                        e.requirements,
                        CAST(ed.salary AS CHAR) AS salary,
                        u.name AS location
                    FROM 
                        Empresas em
                    JOIN 
                        Empleos_Disponibles ed ON em.company_id = ed.company_id
                    JOIN 
                        Empleos e ON ed.job_id = e.job_id
                    JOIN 
                        Ubicaciones u ON ed.location_id = u.location_id
                    WHERE ed.status = 1;
                    '''

            cursor.execute(query)

        results_dict = cursor.fetchall()

        if not results_dict:
            logger.info(f"{request_id} - no se encontraron empleos disponibles")
            final_response['data'] = {}
        else:
            logger.info(f"{request_id} - {request_id} - se encontraron registros")
            final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    #en data se devuelve informacion de las querys
    return final_response

@manage_db_connection
def get_user_applications(cnx, cursor, final_response, candidate_id, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:

        query = '''
                SELECT 
                    s.application_id,
                    s.application_date,
                    e.title AS job_title,   
                    emp.name AS company_name 
                FROM    
                    Empleos_Disponibles ed
                JOIN    
                    Solicitudes s 
                    ON ed.job_offer_id = s.job_offer_id
                JOIN    
                    Empleos e  
                    ON ed.job_id = e.job_id
                JOIN    
                    Empresas emp 
                    ON ed.company_id = emp.company_id
                WHERE   
                    s.candidate_id = %s;
                '''

        values = (candidate_id,)
        cursor.execute(query, values)
        results_dict = cursor.fetchall()

        if results_dict:
            logger.info(f"{request_id} - {request_id} - se encontraron postulaciones del usuario")
            final_response['data'] = results_dict
        else:
            logger.info(f"{request_id} - {request_id} - no se encontraron postulaciones del usuario")

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def get_application_status(cnx, cursor, final_response, application_id, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:

        query = '''
                SELECT 
                        s.application_date,
                        s.status,
                        CASE s.status
                            WHEN 0 THEN 'rejected'
                            WHEN 1 THEN 'accepted'
                            WHEN 2 THEN 'pending'
                            WHEN 3 THEN 'received'
                            ELSE 'unknown status' 
                        END AS status_description
                FROM    Solicitudes s 
                WHERE   s.application_id = %s
                '''

        values = (application_id,)
        cursor.execute(query, values)
        results_dict = cursor.fetchone()

        final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    # en data se devuelve informacion de las querys. en caso de que no se encuentre nada, significa que no se encontro
    return final_response

@manage_db_connection
def get_application_with_company_id(cnx, cursor, final_response, company_id, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:

        query = '''
                SELECT 
                    s.application_id,
                    e.title AS job_title,
                    s.application_date
                FROM 
                    Solicitudes s
                JOIN 
                    Empleos_Disponibles ed ON s.job_offer_id = ed.job_offer_id
                JOIN 
                    Empleos e ON ed.job_id = e.job_id
                WHERE 
                    ed.company_id = %s
                '''

        values = (company_id,)
        cursor.execute(query, values)
        results_dict = cursor.fetchall()

        final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    # en data se devuelve informacion de las querys
    return final_response


@manage_db_connection
def change_application_status(cnx, cursor, final_response, application_id, new_status, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:
        # se inserta con status = 3 -->> solicitud recibida

        query = """
                UPDATE
                Solicitudes
                SET status = %s
                WHERE application_id = %s
                """
        # Creamos una lista de tuplas para la inserción
        values = (new_status, application_id)

        cursor.execute(query, values)
        cnx.commit()

        logger.info(f"{request_id} - se actualizo correctamente el status")

    except:
        logger.exception(f"{request_id} - error al acceder a la base de datos")
        final_response['ok'] = False
    # en data se devuelve informacion de las querys
    return final_response


@manage_db_connection
def get_skills_list(cnx, cursor, final_response, request_id=None):
    final_response = {'ok': True,
                      'data': {}}

    logger.info(f"{request_id} - consultando total de habilidades en bd")
    try:

        query = '''
                    SELECT      *
                    FROM        Habilidades h
                    '''

        cursor.execute(query)
        results_dict = cursor.fetchall()

        final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    # en data se devuelve informacion de las querys
    return final_response

@manage_db_connection
def get_total_candidates_data(cnx, cursor, final_response, request_id=None):
    final_response = {'ok': True,
                      'data': {}}

    logger.info(f"{request_id} - consultando informacion de los candidatos")
    try:

        query = '''
                SELECT 
                            h.name AS skill_name,
                            COUNT(hc.candidate_id) AS user_count
                FROM        Habilidades h
                JOIN        Habilidades_x_Candidato hc 
                ON          h.skill_id = hc.skill_id
                GROUP BY    h.name
                '''

        cursor.execute(query)
        results_dict = cursor.fetchall()

        final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    # en data se devuelve informacion de las querys
    return final_response

@manage_db_connection
def get_total_companies_data(cnx, cursor, final_response, request_id=None):
    final_response = {'ok': True,
                      'data': {}}

    logger.info(f"{request_id} - consultando informacion de las empresas registradas")
    try:

        query = '''
                SELECT 
                    (SELECT COUNT(*) FROM empresas) AS number_of_companies,
                    JSON_OBJECTAGG(sector_empresa.company_type, sector_counts.number_of_companies) AS business_sector
                FROM 
                    sector_empresa
                JOIN 
                    (
                        SELECT 
                            empresas.company_type,
                            COUNT(*) AS number_of_companies
                        FROM 
                            empresas
                        GROUP BY 
                            empresas.company_type
                    ) AS sector_counts
                    ON sector_empresa.company_type_id = sector_counts.company_type;
                '''

        cursor.execute(query)
        results_dict = cursor.fetchall()


        final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    # en data se devuelve informacion de las querys
    return final_response

@manage_db_connection
def get_total_job_offers(cnx, cursor, final_response, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    logger.info(f"{request_id} - consultando informacion de ofertas de trabajo")
    try:

        query = '''
                SELECT 
                    se.company_type,
                    COUNT(ed.job_offer_id) AS sector_count
                FROM Empleos_Disponibles ed
                INNER JOIN Empresas e ON ed.company_id = e.company_id
                INNER JOIN Sector_empresa se ON e.company_type = se.company_type_id
                GROUP BY se.company_type;
                '''

        '''Resultado de query:
        query_result = [
                            {"sector": "technology", "job_offer_count": 1632},
                            {"sector": "law", "job_offer_count": 963},
                            {"sector": "accounting", "job_offer_count": 32},
                            {"sector": "science", "job_offer_count": 685}
                        ]
        '''

        cursor.execute(query)
        results_dict = cursor.fetchall()

        final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    # en data se devuelve informacion de las querys
    return final_response


@manage_db_connection
def get_total_successful_job_offers(cnx, cursor, final_response, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    logger.info(f"{request_id} - consultando informacion de ofertas de trabajo exitosas")
    try:

        query = '''
                SELECT      se.company_type as bussines_sector,
                            COUNT(DISTINCT s.job_offer_id) AS successful_job_offer_count
                FROM        Solicitudes s
                JOIN        Empleos_Disponibles ed 
                ON          s.job_offer_id = ed.job_offer_id
                JOIN        Empresas e 
                ON          ed.company_id = e.company_id
                JOIN        Sector_empresa se
                on          e.company_type = se.company_type_id
                WHERE       s.status = 1
                GROUP BY    e.company_type;
                '''

        '''Resultado de query:
        query_result = [
                            {"sector": "technology", "job_offer_count": 1632},
                            {"sector": "law", "job_offer_count": 963},
                            {"sector": "accounting", "job_offer_count": 32},
                            {"sector": "science", "job_offer_count": 685}
                        ]
        '''

        cursor.execute(query)
        results_dict = cursor.fetchall()

        final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    # en data se devuelve informacion de las querys
    return final_response


@manage_db_connection
def get_companies_list(cnx, cursor, final_response, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    logger.info(f"{request_id} - consultando lista de compañias registradas")
    try:

        query = '''
                SELECT      company_id,
                            name
                FROM Empresas
                '''

        cursor.execute(query)
        results_dict = cursor.fetchall()

        final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    # en data se devuelve informacion de las querys
    return final_response

@manage_db_connection
def upload_work_experience(cnx, cursor, final_response, candidate_id, job_id, company_id, start_date, end_date, request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    try:

        query = """
                    INSERT INTO 
                    Experiencias
                            (candidate_id,
                            job_id,
                            company_id,
                            start_date,
                            end_date) 
                    VALUES  (%s, 
                            %s,
                            %s,
                            %s,
                            %s)
                    """

        values = (candidate_id, job_id, company_id, start_date, end_date)

        cursor.execute(query, values)
        cnx.commit()

        logger.info(f"{request_id} - se cargo correctamente la experiencia del candidato {candidate_id}")
        final_response['data'] = True
    except:
        logger.exception(f"{request_id} - error al acceder a la base de datos")
        final_response['ok'] = False

    return final_response

@manage_db_connection
def get_job_type_list(cnx, cursor, final_response,request_id=None):
    final_response = {'ok': True,
                      'data': {}}
    logger.info(f"{request_id} - consultando lista de empleos registrados")
    try:

        query = '''
                    SELECT      title as name,
                                description,
                                job_id
                    FROM        Empleos
                    '''

        cursor.execute(query)
        results_dict = cursor.fetchall()

        final_response['data'] = results_dict

    except:
        logger.exception(f"{request_id} - {request_id} - error al acceder a la bd")
        final_response['ok'] = False
    # en data se devuelve informacion de las querys
    return final_response