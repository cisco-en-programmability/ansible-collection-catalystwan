cisco_aaa_definition = { 'cisco_aaa': { 'default': None,
                 'options': { 'accounting_group': { 'default': False,
                                                    'required': False,
                                                    'type': 'bool'},
                              'accounting_rules': { 'default': None,
                                                    'elements': 'dict',
                                                    'options': { 'group': { 'default': None,
                                                                            'required': True,
                                                                            'type': 'str'},
                                                                 'level': { 'default': None,
                                                                            'required': False,
                                                                            'type': 'str'},
                                                                 'method': { 'default': None,
                                                                             'required': True,
                                                                             'type': 'str'},
                                                                 'rule_id': { 'default': None,
                                                                              'required': True,
                                                                              'type': 'str'},
                                                                 'start_stop': { 'default': True,
                                                                                 'required': False,
                                                                                 'type': 'bool'}},
                                                    'required': False,
                                                    'type': 'list'},
                              'authentication_group': { 'default': False,
                                                        'required': False,
                                                        'type': 'bool'},
                              'authentication_type': { 'default': 'any',
                                                       'required': False,
                                                       'type': 'str'},
                              'authorization_config_commands': { 'default': None,
                                                                 'required': False,
                                                                 'type': 'bool'},
                              'authorization_console': { 'default': None,
                                                         'required': False,
                                                         'type': 'bool'},
                              'authorization_rules': { 'default': None,
                                                       'elements': 'dict',
                                                       'options': { 'authenticated': { 'default': False,
                                                                                       'required': False,
                                                                                       'type': 'bool'},
                                                                    'group': { 'default': None,
                                                                               'required': True,
                                                                               'type': 'str'},
                                                                    'level': { 'default': None,
                                                                               'required': False,
                                                                               'type': 'str'},
                                                                    'method': { 'default': None,
                                                                                'required': True,
                                                                                'type': 'str'},
                                                                    'rule_id': { 'default': None,
                                                                                 'required': True,
                                                                                 'type': 'str'}},
                                                       'required': False,
                                                       'type': 'list'},
                              'cts_authorization_list': { 'default': None,
                                                          'required': False,
                                                          'type': 'str'},
                              'domain_stripping': { 'default': None,
                                                    'required': False,
                                                    'type': 'str'},
                              'port': { 'default': None,
                                        'required': False,
                                        'type': 'int'},
                              'radius': { 'default': None,
                                          'elements': 'dict',
                                          'options': { 'group_name': { 'default': None,
                                                                       'required': True,
                                                                       'type': 'str'},
                                                       'server': { 'default': [ ],
                                                                   'elements': 'dict',
                                                                   'options': { 'acct_port': { 'default': None,
                                                                                               'required': False,
                                                                                               'type': 'int'},
                                                                                'address': { 'default': None,
                                                                                             'required': True,
                                                                                             'type': 'str'},
                                                                                'auth_port': { 'default': None,
                                                                                               'required': False,
                                                                                               'type': 'int'},
                                                                                'key': { 'default': None,
                                                                                         'required': True,
                                                                                         'type': 'str'},
                                                                                'key_enum': { 'default': None,
                                                                                              'required': False,
                                                                                              'type': 'str'},
                                                                                'key_type': { 'default': None,
                                                                                              'required': False,
                                                                                              'type': 'str'},
                                                                                'retransmit': { 'default': None,
                                                                                                'required': False,
                                                                                                'type': 'int'},
                                                                                'secret_key': { 'default': None,
                                                                                                'required': False,
                                                                                                'type': 'str'},
                                                                                'timeout': { 'default': None,
                                                                                             'required': False,
                                                                                             'type': 'int'}},
                                                                   'required': False,
                                                                   'type': 'list'},
                                                       'source_interface': { 'default': None,
                                                                             'required': True,
                                                                             'type': 'str'},
                                                       'vpn': { 'default': None,
                                                                'required': True,
                                                                'type': 'int'}},
                                          'required': False,
                                          'type': 'list'},
                              'radius_client': { 'default': None,
                                                 'elements': 'dict',
                                                 'options': { 'ip': { 'default': None,
                                                                      'required': True,
                                                                      'type': 'str'},
                                                              'vpn': { 'default': None,
                                                                       'elements': 'dict',
                                                                       'options': { 'name': { 'default': None,
                                                                                              'required': True,
                                                                                              'type': 'str'},
                                                                                    'server_key': { 'default': None,
                                                                                                    'required': False,
                                                                                                    'type': 'str'}},
                                                                       'required': True,
                                                                       'type': 'list'}},
                                                 'required': False,
                                                 'type': 'list'},
                              'radius_trustsec_group': { 'default': None,
                                                         'required': False,
                                                         'type': 'str'},
                              'server_auth_order': { 'default': 'local',
                                                     'required': False,
                                                     'type': 'str'},
                              'server_key_password': { 'default': None,
                                                       'required': False,
                                                       'type': 'str'},
                              'tacacs': { 'default': None,
                                          'elements': 'dict',
                                          'options': { 'group_name': { 'default': None,
                                                                       'required': True,
                                                                       'type': 'str'},
                                                       'server': { 'default': [ ],
                                                                   'elements': 'dict',
                                                                   'options': { 'address': { 'default': None,
                                                                                             'required': True,
                                                                                             'type': 'str'},
                                                                                'key': { 'default': None,
                                                                                         'required': True,
                                                                                         'type': 'str'},
                                                                                'key_enum': { 'default': None,
                                                                                              'required': False,
                                                                                              'type': 'str'},
                                                                                'port': { 'default': None,
                                                                                          'required': False,
                                                                                          'type': 'int'},
                                                                                'secret_key': { 'default': None,
                                                                                                'required': False,
                                                                                                'type': 'str'},
                                                                                'timeout': { 'default': None,
                                                                                             'required': False,
                                                                                             'type': 'int'}},
                                                                   'required': False,
                                                                   'type': 'list'},
                                                       'source_interface': { 'default': None,
                                                                             'required': False,
                                                                             'type': 'str'},
                                                       'vpn': { 'default': None,
                                                                'required': False,
                                                                'type': 'int'}},
                                          'required': False,
                                          'type': 'list'},
                              'user': { 'default': None,
                                        'elements': 'dict',
                                        'options': { 'name': { 'default': None,
                                                               'required': True,
                                                               'type': 'str'},
                                                     'password': { 'default': None,
                                                                   'required': False,
                                                                   'type': 'str'},
                                                     'privilege': { 'default': '15',
                                                                    'required': False,
                                                                    'type': 'str'},
                                                     'pubkey_chain': { 'default': [ ],
                                                                       'elements': 'dict',
                                                                       'options': { 'key_string': { 'default': None,
                                                                                                    'required': True,
                                                                                                    'type': 'str'},
                                                                                    'key_type': { 'default': 'ssh-rsa',
                                                                                                  'required': False,
                                                                                                  'type': 'str'}},
                                                                       'required': False,
                                                                       'type': 'list'},
                                                     'secret': { 'default': None,
                                                                 'required': False,
                                                                 'type': 'str'}},
                                        'required': False,
                                        'type': 'list'}},
                 'required': False,
                 'type': 'dict'}}
