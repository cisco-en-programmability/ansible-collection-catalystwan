#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2024 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# This file is autogenerated by `utils/feature_template_docs_generator.py`


from __future__ import annotations


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    security_vsmart:
        description: Security settings for vSmart controller
        type: dict
        suboptions:
            protocol:
                description:
                - The security protocol used for control plane communication
                required: false
                default: null
                type: str
                choices:
                - dtls
                - tls
            tls_port:
                description:
                - The port used for TLS communications
                required: false
                default: null
                type: str
    '''