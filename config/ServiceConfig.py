register_user_code_map = {'0200': 'ok',
                          '0400': 'bad request',
                          '0404': 'company not found',
                          '0410': 'user already registered',
                          '0411': 'incorrect data lenght',
                          '0500': 'internal error'}

login_code_map = {'0200': 'ok',
                  '0400': 'bad request',
                  '0404': 'incorrect user/password',
                  '0500': 'internal error'}

create_new_company_code_map = {'0200': 'ok',
                               '0400': 'bad request',
                               '0410': 'company already registered',
                               '0500': 'internal error'}

create_new_job_code_map = {'0200': 'ok',
                           '0400': 'bad request',
                           '0410': 'job already registered',
                           '0500': 'internal error'}

create_job_offer_code_map = {'0200': 'ok',
                             '0400': 'bad request',
                             '0410': 'job offer already registered',
                             '0500': 'internal error'}

apply_for_a_job_code_map = {'0200': 'ok',
                            '0400': 'bad request',
                            '0410': 'apply already registered',
                            '0411': 'job offer is not active',
                            '0500': 'internal error'}

get_applicants_information_code_map = {'0200': 'ok',
                                       '0400': 'bad request',
                                       '0410': 'apply already registered',
                                       '0500': 'internal error'}

get_available_jobs_code_map = {'0200': 'ok',
                               '0400': 'bad request',
                               '0500': 'internal error'}

get_user_applications_code_map = {'0200': 'ok',
                                  '0400': 'bad request',
                                  '0500': 'internal error'}

get_applications_status_code_map = {'0200': 'ok',
                                    '0400': 'bad request',
                                    '0404': 'not found',
                                    '0500': 'internal error'}

get_applications_with_company_id_code_map = {'0200': 'ok',
                                             '0400': 'bad request',
                                             '0404': 'not found',
                                             '0500': 'internal error'}

change_application_status_code_map = {'0200': 'ok',
                                      '0400': 'bad request',
                                      '0404': 'application not found',
                                      '0405': 'invalid status',
                                      '0410': 'new status is the same as old status',
                                      '0500': 'internal error'}

get_stats_code_map = {'0200': 'ok',
                      '0400': 'bad request',
                      '0500': 'internal error'}

get_companies_list_code_map = {'0200': 'ok',
                               '0400': 'bad request',
                               '0500': 'internal error'}


upload_experience_response = {'0200': 'ok',
                               '0400': 'bad request',
                              '0405': 'invalid job_id',
                              '0406': 'invalid candidate_id',
                              '0407': 'invalid company_id',
                               '0500': 'internal error'}

get_job_type_list_code_map = {'0200': 'ok',
                               '0400': 'bad request',
                               '0500': 'internal error'}
