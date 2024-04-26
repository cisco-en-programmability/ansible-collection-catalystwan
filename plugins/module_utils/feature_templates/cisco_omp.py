cisco_omp_definition = { 'cisco_omp': { 'default': None,
                 'options': { 'advertise': { 'default': None,
                                             'elements': 'dict',
                                             'options': { 'protocol': { 'default': None,
                                                                        'required': True,
                                                                        'type': 'str'},
                                                          'route': { 'default': None,
                                                                     'required': False,
                                                                     'type': 'str'}},
                                             'required': False,
                                             'type': 'list'},
                              'advertisement_interval': { 'default': None,
                                                          'required': False,
                                                          'type': 'str'},
                              'auto_translate': { 'default': None,
                                                  'required': False,
                                                  'type': 'str'},
                              'ecmp_limit': { 'default': None,
                                              'required': False,
                                              'type': 'str'},
                              'eor_timer': { 'default': None,
                                             'required': False,
                                             'type': 'str'},
                              'graceful_restart': { 'default': None,
                                                    'required': False,
                                                    'type': 'str'},
                              'graceful_restart_timer': { 'default': None,
                                                          'required': False,
                                                          'type': 'str'},
                              'holdtime': { 'default': None,
                                            'required': False,
                                            'type': 'str'},
                              'ignore_region_path_length': { 'default': None,
                                                             'required': False,
                                                             'type': 'str'},
                              'ipv6_advertise': { 'default': None,
                                                  'elements': 'dict',
                                                  'options': { 'protocol': { 'default': None,
                                                                             'required': True,
                                                                             'type': 'str'}},
                                                  'required': False,
                                                  'type': 'list'},
                              'omp_admin_distance_ipv4': { 'default': None,
                                                           'required': False,
                                                           'type': 'str'},
                              'omp_admin_distance_ipv6': { 'default': None,
                                                           'required': False,
                                                           'type': 'str'},
                              'overlay_as': { 'default': None,
                                              'required': False,
                                              'type': 'str'},
                              'send_path_limit': { 'default': None,
                                                   'required': False,
                                                   'type': 'str'},
                              'shutdown': { 'default': None,
                                            'required': False,
                                            'type': 'str'},
                              'site_types': { 'default': None,
                                              'elements': 'str',
                                              'required': False,
                                              'type': 'list'},
                              'transport_gateway': { 'default': None,
                                                     'required': False,
                                                     'type': 'str'}},
                 'required': False,
                 'type': 'dict'}}
