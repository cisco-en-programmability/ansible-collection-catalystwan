#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2024 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# This file is autogenerated by `utils/feature_template_docs_generator.py`


from __future__ import annotations


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    cisco_bfd:
        description: Cisco Bidirectional Forwarding Detection (BFD) configuration
        type: dict
        suboptions:
            multiplier:
                description:
                - The default BFD multiplier for all colors
                required: false
                default: null
                type: str
            poll_interval:
                description:
                - The BFD poll interval in milliseconds
                required: false
                default: null
                type: str
            default_dscp:
                description:
                - The default DSCP value for BFD packets
                required: false
                default: null
                type: str
            color:
                description:
                - List of color-specific BFD configurations
                required: false
                default: null
                type: list
                elements: dict
                suboptions:
                    color:
                        description:
                        - The color of the BFD session, representing various transport
                            types
                        required: true
                        default: null
                        type: str
                        choices:
                        - default
                        - mpls
                        - metro-ethernet
                        - biz-internet
                        - public-internet
                        - lte
                        - 3g
                        - red
                        - green
                        - blue
                        - gold
                        - silver
                        - bronze
                        - custom1
                        - custom2
                        - custom3
                        - private1
                        - private2
                        - private3
                        - private4
                        - private5
                        - private6
                    hello_interval:
                        description:
                        - The BFD hello interval in milliseconds
                        required: false
                        default: null
                        type: str
                    multiplier:
                        description:
                        - The BFD multiplier for the color
                        required: false
                        default: null
                        type: str
                    pmtu_discovery:
                        description:
                        - Whether to enable Path MTU Discovery
                        required: false
                        default: null
                        type: str
                    dscp:
                        description:
                        - The DSCP value used for BFD packets
                        required: false
                        default: null
                        type: str
    '''