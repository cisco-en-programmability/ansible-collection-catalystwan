cisco_secure_internet_gateway_definition = { 'cisco_secure_internet_gateway': { 'default': None,
                                     'options': { 'interface': { 'default': None,
                                                                 'elements': 'dict',
                                                                 'options': { 'address': { 'default': None,
                                                                                           'required': False,
                                                                                           'type': 'str'},
                                                                              'application': { 'default': 'sig',
                                                                                               'required': False,
                                                                                               'type': 'str'},
                                                                              'auto': { 'default': None,
                                                                                        'required': True,
                                                                                        'type': 'bool'},
                                                                              'description': { 'default': None,
                                                                                               'required': False,
                                                                                               'type': 'str'},
                                                                              'dpd_interval': { 'default': None,
                                                                                                'required': False,
                                                                                                'type': 'str'},
                                                                              'dpd_retries': { 'default': None,
                                                                                               'required': False,
                                                                                               'type': 'str'},
                                                                              'if_name': { 'default': None,
                                                                                           'required': True,
                                                                                           'type': 'str'},
                                                                              'ike_ciphersuite': { 'default': 'aes256-cbc-sha1',
                                                                                                   'required': False,
                                                                                                   'type': 'str'},
                                                                              'ike_group': { 'default': '14',
                                                                                             'required': False,
                                                                                             'type': 'str'},
                                                                              'ike_local_id': { 'default': None,
                                                                                                'required': False,
                                                                                                'type': 'str'},
                                                                              'ike_rekey_interval': { 'default': None,
                                                                                                      'required': False,
                                                                                                      'type': 'str'},
                                                                              'ike_remote_id': { 'default': None,
                                                                                                 'required': False,
                                                                                                 'type': 'str'},
                                                                              'ike_version': { 'default': None,
                                                                                               'required': False,
                                                                                               'type': 'int'},
                                                                              'ipsec_ciphersuite': { 'default': 'aes256-gcm',
                                                                                                     'required': False,
                                                                                                     'type': 'str'},
                                                                              'ipsec_rekey_interval': { 'default': None,
                                                                                                        'required': False,
                                                                                                        'type': 'str'},
                                                                              'ipsec_replay_window': { 'default': None,
                                                                                                       'required': False,
                                                                                                       'type': 'str'},
                                                                              'mtu': { 'default': None,
                                                                                       'required': False,
                                                                                       'type': 'int'},
                                                                              'perfect_forward_secrecy': { 'default': 'none',
                                                                                                           'required': False,
                                                                                                           'type': 'str'},
                                                                              'pre_shared_key_dynamic': { 'default': None,
                                                                                                          'required': False,
                                                                                                          'type': 'bool'},
                                                                              'pre_shared_secret': { 'default': None,
                                                                                                     'required': False,
                                                                                                     'type': 'str'},
                                                                              'shutdown': { 'default': None,
                                                                                            'required': True,
                                                                                            'type': 'bool'},
                                                                              'tcp_mss_adjust': { 'default': None,
                                                                                                  'required': False,
                                                                                                  'type': 'str'},
                                                                              'track_enable': { 'default': None,
                                                                                                'required': False,
                                                                                                'type': 'str'},
                                                                              'tracker': { 'default': None,
                                                                                           'required': False,
                                                                                           'type': 'str'},
                                                                              'tunnel_dc_preference': { 'default': 'primary-dc',
                                                                                                        'required': False,
                                                                                                        'type': 'str'},
                                                                              'tunnel_destination': { 'default': None,
                                                                                                      'required': True,
                                                                                                      'type': 'str'},
                                                                              'tunnel_route_via': { 'default': None,
                                                                                                    'required': False,
                                                                                                    'type': 'str'},
                                                                              'tunnel_set': { 'default': 'secure-internet-gateway-umbrella',
                                                                                              'required': False,
                                                                                              'type': 'str'},
                                                                              'tunnel_source': { 'default': None,
                                                                                                 'required': False,
                                                                                                 'type': 'str'},
                                                                              'tunnel_source_interface': { 'default': None,
                                                                                                           'required': False,
                                                                                                           'type': 'str'},
                                                                              'unnumbered': { 'default': None,
                                                                                              'required': False,
                                                                                              'type': 'bool'}},
                                                                 'required': True,
                                                                 'type': 'list'},
                                                  'service': { 'default': None,
                                                               'elements': 'dict',
                                                               'options': { 'auth_required': { 'default': None,
                                                                                               'required': False,
                                                                                               'type': 'str'},
                                                                            'block_internet_until_accepted': { 'default': None,
                                                                                                               'required': False,
                                                                                                               'type': 'str'},
                                                                            'caution_enabled': { 'default': None,
                                                                                                 'required': False,
                                                                                                 'type': 'str'},
                                                                            'data_center_primary': { 'default': 'Auto',
                                                                                                     'required': False,
                                                                                                     'type': 'str'},
                                                                            'data_center_secondary': { 'default': 'Auto',
                                                                                                       'required': False,
                                                                                                       'type': 'str'},
                                                                            'display_time_unit': { 'default': 'MINUTE',
                                                                                                   'required': False,
                                                                                                   'type': 'str'},
                                                                            'enabled': { 'default': None,
                                                                                         'required': False,
                                                                                         'type': 'str'},
                                                                            'force_ssl_inspection': { 'default': None,
                                                                                                      'required': False,
                                                                                                      'type': 'str'},
                                                                            'idle_time': { 'default': None,
                                                                                           'required': False,
                                                                                           'type': 'str'},
                                                                            'interface_pair': { 'default': None,
                                                                                                'elements': 'dict',
                                                                                                'options': { 'active_interface': { 'default': None,
                                                                                                                                   'required': True,
                                                                                                                                   'type': 'str'},
                                                                                                             'active_interface_weight': { 'default': None,
                                                                                                                                          'required': False,
                                                                                                                                          'type': 'int'},
                                                                                                             'backup_interface': { 'default': None,
                                                                                                                                   'required': False,
                                                                                                                                   'type': 'str'},
                                                                                                             'backup_interface_weight': { 'default': None,
                                                                                                                                          'required': False,
                                                                                                                                          'type': 'int'}},
                                                                                                'required': True,
                                                                                                'type': 'list'},
                                                                            'ip': { 'default': None,
                                                                                    'required': False,
                                                                                    'type': 'str'},
                                                                            'ip_enforced_for_known_browsers': { 'default': None,
                                                                                                                'required': False,
                                                                                                                'type': 'str'},
                                                                            'ips_control': { 'default': None,
                                                                                             'required': False,
                                                                                             'type': 'str'},
                                                                            'ofw_enabled': { 'default': None,
                                                                                             'required': False,
                                                                                             'type': 'str'},
                                                                            'primary_data_center': { 'default': 'Auto',
                                                                                                     'required': False,
                                                                                                     'type': 'str'},
                                                                            'refresh_time': { 'default': None,
                                                                                              'required': False,
                                                                                              'type': 'str'},
                                                                            'refresh_time_unit': { 'default': 'MINUTE',
                                                                                                   'required': False,
                                                                                                   'type': 'str'},
                                                                            'secondary_data_center': { 'default': 'Auto',
                                                                                                       'required': False,
                                                                                                       'type': 'str'},
                                                                            'svc_type': { 'default': 'sig',
                                                                                          'required': False,
                                                                                          'type': 'str'},
                                                                            'timeout': { 'default': None,
                                                                                         'required': False,
                                                                                         'type': 'str'},
                                                                            'xff_forward_enabled': { 'default': None,
                                                                                                     'required': False,
                                                                                                     'type': 'str'}},
                                                               'required': True,
                                                               'type': 'list'},
                                                  'tracker': { 'default': None,
                                                               'elements': 'dict',
                                                               'options': { 'endpoint_api_url': { 'default': None,
                                                                                                  'required': True,
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
                                                                            'threshold': { 'default': None,
                                                                                           'required': False,
                                                                                           'type': 'str'},
                                                                            'tracker_type': { 'default': None,
                                                                                              'required': True,
                                                                                              'type': 'str'}},
                                                               'required': False,
                                                               'type': 'list'},
                                                  'tracker_src_ip': { 'default': None,
                                                                      'required': False,
                                                                      'type': 'str'},
                                                  'vpn_id': { 'default': None,
                                                              'required': False,
                                                              'type': 'int'}},
                                     'required': False,
                                     'type': 'dict'}}
