cisco_system_definition = { 'cisco_system': { 'default': None,
                    'options': { 'admin_tech_on_failure': { 'default': None,
                                                            'required': False,
                                                            'type': 'bool'},
                                 'affinity_group_number': { 'default': None,
                                                            'required': False,
                                                            'type': 'str'},
                                 'affinity_per_vrf': { 'default': None,
                                                       'elements': 'dict',
                                                       'options': { 'affinity_group_number': { 'default': None,
                                                                                               'required': False,
                                                                                               'type': 'str'},
                                                                    'vrf_range': { 'default': None,
                                                                                   'required': False,
                                                                                   'type': 'str'}},
                                                       'required': False,
                                                       'type': 'list'},
                                 'console_baud_rate': { 'default': None,
                                                        'required': False,
                                                        'type': 'str'},
                                 'control_session_pps': { 'default': None,
                                                          'required': False,
                                                          'type': 'str'},
                                 'controller_group_list': { 'default': None,
                                                            'elements': 'str',
                                                            'required': False,
                                                            'type': 'list'},
                                 'device_groups': { 'default': None,
                                                    'elements': 'str',
                                                    'required': False,
                                                    'type': 'list'},
                                 'enable_fencing': { 'default': None,
                                                     'required': False,
                                                     'type': 'bool'},
                                 'enable_management_region': { 'default': None,
                                                               'required': False,
                                                               'type': 'bool'},
                                 'enable_mrf_migration': { 'default': None,
                                                           'required': False,
                                                           'type': 'str'},
                                 'enable_sms': { 'default': False,
                                                 'required': False,
                                                 'type': 'bool'},
                                 'enable_tunnel': { 'default': None,
                                                    'required': False,
                                                    'type': 'bool'},
                                 'epfr': { 'default': None,
                                           'required': False,
                                           'type': 'str'},
                                 'hostname': { 'default': 'system_host_name',
                                               'options': { 'name': { 'default': None,
                                                                      'required': True,
                                                                      'type': 'str'}},
                                               'required': False,
                                               'type': 'dict'},
                                 'idle_timeout': { 'default': None,
                                                   'required': False,
                                                   'type': 'str'},
                                 'latitude': { 'default': None,
                                               'required': False,
                                               'type': 'str'},
                                 'location': { 'default': None,
                                               'required': False,
                                               'type': 'str'},
                                 'longitude': { 'default': None,
                                                'required': False,
                                                'type': 'str'},
                                 'management_gateway': { 'default': None,
                                                         'required': False,
                                                         'type': 'bool'},
                                 'max_omp_sessions': { 'default': None,
                                                       'required': False,
                                                       'type': 'str'},
                                 'migration_bgp_community': { 'default': None,
                                                              'required': False,
                                                              'type': 'str'},
                                 'mobile_number': { 'default': None,
                                                    'elements': 'dict',
                                                    'options': { 'number': { 'default': None,
                                                                             'required': True,
                                                                             'type': 'str'}},
                                                    'required': False,
                                                    'type': 'list'},
                                 'multi_tenant': { 'default': None,
                                                   'required': False,
                                                   'type': 'bool'},
                                 'object_track': { 'default': None,
                                                   'elements': 'dict',
                                                   'options': { 'boolean': { 'default': None,
                                                                             'required': True,
                                                                             'type': 'str'},
                                                                'interface': { 'default': None,
                                                                               'required': True,
                                                                               'type': 'str'},
                                                                'ip': { 'default': None,
                                                                        'required': True,
                                                                        'type': 'str'},
                                                                'mask': { 'default': '0.0.0.0',
                                                                          'required': False,
                                                                          'type': 'str'},
                                                                'object': { 'default': None,
                                                                            'elements': 'dict',
                                                                            'options': { 'number': { 'default': None,
                                                                                                     'required': True,
                                                                                                     'type': 'int'}},
                                                                            'required': True,
                                                                            'type': 'list'},
                                                                'object_number': { 'default': None,
                                                                                   'required': True,
                                                                                   'type': 'int'},
                                                                'sig': { 'default': None,
                                                                         'required': True,
                                                                         'type': 'str'},
                                                                'vpn': { 'default': None,
                                                                         'required': True,
                                                                         'type': 'int'}},
                                                   'required': False,
                                                   'type': 'list'},
                                 'on_demand_idle_timeout_min': { 'default': None,
                                                                 'required': False,
                                                                 'type': 'str'},
                                 'overlay_id': { 'default': None,
                                                 'required': False,
                                                 'type': 'str'},
                                 'port_hop': { 'default': None,
                                               'required': False,
                                               'type': 'bool'},
                                 'port_offset': { 'default': None,
                                                  'required': False,
                                                  'type': 'str'},
                                 'preference': { 'default': None,
                                                 'elements': 'str',
                                                 'required': False,
                                                 'type': 'list'},
                                 'preference_auto': { 'default': None,
                                                      'required': False,
                                                      'type': 'bool'},
                                 'range': { 'default': None,
                                            'required': False,
                                            'type': 'str'},
                                 'region_id': { 'default': None,
                                                'required': False,
                                                'type': 'str'},
                                 'role': { 'default': None,
                                           'required': False,
                                           'type': 'str'},
                                 'secondary_region': { 'default': None,
                                                       'required': False,
                                                       'type': 'str'},
                                 'site_id': { 'default': 'system_site_id',
                                              'required': False,
                                              'type': 'int'},
                                 'site_type': { 'default': None,
                                                'elements': 'str',
                                                'required': False,
                                                'type': 'list'},
                                 'system_ip': { 'default': 'system_system_ip',
                                                'options': { 'name': { 'default': None,
                                                                       'required': True,
                                                                       'type': 'str'}},
                                                'required': False,
                                                'type': 'dict'},
                                 'timezone': { 'default': None,
                                               'required': False,
                                               'type': 'str'},
                                 'track_default_gateway': { 'default': None,
                                                            'required': False,
                                                            'type': 'bool'},
                                 'track_interface_tag': { 'default': None,
                                                          'required': False,
                                                          'type': 'str'},
                                 'track_transport': { 'default': None,
                                                      'required': False,
                                                      'type': 'bool'},
                                 'tracker': { 'default': None,
                                              'elements': 'dict',
                                              'options': { 'boolean': { 'default': 'or',
                                                                        'required': False,
                                                                        'type': 'str'},
                                                           'elements': { 'default': None,
                                                                         'elements': 'str',
                                                                         'required': False,
                                                                         'type': 'list'},
                                                           'endpoint_api_url': { 'default': None,
                                                                                 'required': False,
                                                                                 'type': 'str'},
                                                           'endpoint_dns_name': { 'default': None,
                                                                                  'required': False,
                                                                                  'type': 'str'},
                                                           'endpoint_ip': { 'default': None,
                                                                            'required': False,
                                                                            'type': 'str'},
                                                           'endpoint_ip_transport_port': { 'default': None,
                                                                                           'required': False,
                                                                                           'type': 'str'},
                                                           'interval': { 'default': None,
                                                                         'required': False,
                                                                         'type': 'str'},
                                                           'multiplier': { 'default': None,
                                                                           'required': False,
                                                                           'type': 'str'},
                                                           'name': { 'default': None,
                                                                     'required': True,
                                                                     'type': 'str'},
                                                           'port': { 'default': None,
                                                                     'required': False,
                                                                     'type': 'str'},
                                                           'protocol': { 'default': None,
                                                                         'required': False,
                                                                         'type': 'str'},
                                                           'threshold': { 'default': None,
                                                                          'required': False,
                                                                          'type': 'str'},
                                                           'type': { 'default': 'interface',
                                                                     'required': False,
                                                                     'type': 'str'}},
                                              'required': False,
                                              'type': 'list'},
                                 'transport_gateway': { 'default': None,
                                                        'required': False,
                                                        'type': 'bool'},
                                 'vrf': { 'default': None,
                                          'elements': 'dict',
                                          'options': { 'gateway_preference': { 'default': None,
                                                                               'elements': 'str',
                                                                               'required': False,
                                                                               'type': 'list'},
                                                       'vrf_id': { 'default': None,
                                                                   'required': True,
                                                                   'type': 'int'}},
                                          'required': False,
                                          'type': 'list'}},
                    'required': False,
                    'type': 'dict'}}
