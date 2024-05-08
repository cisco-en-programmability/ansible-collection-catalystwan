#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2024 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# This file is autogenerated by `utils/feature_template_docs_generator.py`


from __future__ import annotations


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    cisco_aaa:
        description: Cisco AAA Feature Template configuration
        type: dict
        suboptions:
            authentication_group:
                description:
                - 'Whether to enable the authentication group, GUI equivalent: Authentication
                    Param'
                required: false
                default: false
                type: bool
            accounting_group:
                description:
                - 'Whether to enable the accounting group, GUI equivalent: Accounting
                    Param'
                required: false
                default: false
                type: bool
            server_auth_order:
                description:
                - ServerGroups authentication order to user access
                required: false
                default: local
                type: str
            user:
                description:
                - List of local user configurations
                required: false
                default: null
                type: list
                elements: dict
                suboptions:
                    name:
                        description:
                        - The name of the user
                        required: true
                        default: null
                        type: str
                    password:
                        description:
                        - The password for the user
                        required: false
                        default: null
                        type: str
                    secret:
                        description:
                        - The secret for the user
                        required: false
                        default: null
                        type: str
                    privilege:
                        description:
                        - The privilege level for the user
                        required: false
                        default: '15'
                        type: str
                        choices:
                        - '1'
                        - '15'
                    pubkey_chain:
                        description:
                        - List of public keys for the user
                        required: false
                        default: []
                        type: list
                        elements: dict
                        suboptions:
                            key_string:
                                description:
                                - Set the RSA key string
                                required: true
                                default: null
                                type: str
                            key_type:
                                description:
                                - Only RSA is supported
                                required: false
                                default: ssh-rsa
                                type: str
            accounting_rules:
                description:
                - Configure the accounting rules
                required: false
                default: null
                type: list
                elements: dict
                suboptions:
                    rule_id:
                        description:
                        - Accounting Rule ID
                        required: true
                        default: null
                        type: str
                    method:
                        description:
                        - Configure Accounting Method
                        required: true
                        default: null
                        type: str
                        choices:
                        - commands
                        - exec
                        - network
                        - system
                    level:
                        description:
                        - Privilege level when method is commands
                        required: false
                        default: null
                        type: str
                        choices:
                        - '1'
                        - '15'
                    start_stop:
                        description:
                        - Enable Start-Stop
                        required: false
                        default: true
                        type: bool
                    group:
                        description:
                        - List of groups.
                        required: true
                        default: null
                        type: str
            authorization_console:
                description:
                - For enabling console authorization
                required: false
                default: null
                type: bool
            authorization_config_commands:
                description:
                - For configuration mode commands
                required: false
                default: null
                type: bool
            authorization_rules:
                description:
                - Configure the accounting rules
                required: false
                default: null
                type: list
                elements: dict
                suboptions:
                    rule_id:
                        description:
                        - Authorization Rule ID
                        required: true
                        default: null
                        type: str
                    method:
                        description:
                        - Configure Authorization Method
                        required: true
                        default: null
                        type: str
                        choices:
                        - commands
                    level:
                        description:
                        - Privilege level when method is commands
                        required: false
                        default: null
                        type: str
                        choices:
                        - '1'
                        - '15'
                    group:
                        description:
                        - List of groups.
                        required: true
                        default: null
                        type: str
                    authenticated:
                        description:
                        - Succeed if user has authenticated
                        required: false
                        default: false
                        type: bool
            radius:
                description:
                - List of Radius group configurations
                required: false
                default: null
                type: list
                elements: dict
                suboptions:
                    group_name:
                        description:
                        - The name of the RADIUS group
                        required: true
                        default: null
                        type: str
                    vpn:
                        description:
                        - The VPN ID for the RADIUS group
                        required: true
                        default: null
                        type: int
                    source_interface:
                        description:
                        - The source interface for the RADIUS group
                        required: true
                        default: null
                        type: str
                    server:
                        description:
                        - The list of RADIUS servers for the group
                        required: false
                        default: []
                        type: list
                        elements: dict
                        suboptions:
                            address:
                                description:
                                - The IP address or hostname of the RADIUS server
                                required: true
                                default: null
                                type: str
                            auth_port:
                                description:
                                - The authentication port for the RADIUS server
                                required: false
                                default: null
                                type: int
                            acct_port:
                                description:
                                - The accounting port for the RADIUS server
                                required: false
                                default: null
                                type: int
                            timeout:
                                description:
                                - The timeout period in seconds for the RADIUS server
                                required: false
                                default: null
                                type: int
                            retransmit:
                                description:
                                - The number of retransmit attempts for the RADIUS
                                    server
                                required: false
                                default: null
                                type: int
                            key:
                                description:
                                - The key for the RADIUS server
                                required: true
                                default: null
                                type: str
                            secret_key:
                                description:
                                - The secret key for the RADIUS server
                                required: false
                                default: null
                                type: str
                            key_enum:
                                description:
                                - The key enumeration for the RADIUS server
                                required: false
                                default: null
                                type: str
                            key_type:
                                description:
                                - The key type for the RADIUS server
                                required: false
                                default: null
                                type: str
            radius_client:
                description:
                - Specify a RADIUS client
                required: false
                default: null
                type: list
                elements: dict
                suboptions:
                    ip:
                        description:
                        - The Client IP
                        required: true
                        default: null
                        type: str
                    vpn:
                        description:
                        - The VPN Configuration
                        required: true
                        default: null
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description:
                                - VPN ID
                                required: true
                                default: null
                                type: str
                            server_key:
                                description:
                                - Specify a RADIUS client server-key
                                required: false
                                default: null
                                type: str
            domain_stripping:
                description:
                - The domain stripping configuration
                required: false
                default: null
                type: str
                choices:
                - 'yes'
                - 'no'
                - right-to-left
            authentication_type:
                description:
                - Authentication Type
                required: false
                default: any
                type: str
                choices:
                - any
                - all
                - session-key
            port:
                description:
                - Specify Radius Dynamic Author Port
                required: false
                default: null
                type: int
            server_key_password:
                description:
                - Specify a radius dynamic author server-key
                required: false
                default: null
                type: str
            cts_authorization_list:
                description:
                - Specify a radius dynamic author server-key
                required: false
                default: null
                type: str
            radius_trustsec_group:
                description:
                - RADIUS trustsec group
                required: false
                default: null
                type: str
            tacacs:
                description:
                - List of TACACS group configurations
                required: false
                default: null
                type: list
                elements: dict
                suboptions:
                    group_name:
                        description:
                        - The name of the TACACS+ group
                        required: true
                        default: null
                        type: str
                    vpn:
                        description:
                        - The VPN ID for the TACACS+ group
                        required: false
                        default: null
                        type: int
                    source_interface:
                        description:
                        - The source interface for the TACACS+ group
                        required: false
                        default: null
                        type: str
                    server:
                        description:
                        - The list of TACACS+ servers for the group
                        required: false
                        default: []
                        type: list
                        elements: dict
                        suboptions:
                            address:
                                description:
                                - The IP address or hostname of the TACACS+ server
                                required: true
                                default: null
                                type: str
                            key:
                                description:
                                - The key for the TACACS+ server
                                required: true
                                default: null
                                type: str
                            port:
                                description:
                                - The port for the TACACS+ server
                                required: false
                                default: null
                                type: int
                            timeout:
                                description:
                                - The timeout period in seconds for the TACACS+ server
                                required: false
                                default: null
                                type: int
                            secret_key:
                                description:
                                - The secret key for the TACACS+ server
                                required: false
                                default: null
                                type: str
                            key_enum:
                                description:
                                - The key enumeration for the TACACS+ server
                                required: false
                                default: null
                                type: str
    '''