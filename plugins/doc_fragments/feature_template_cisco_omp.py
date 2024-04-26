#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2024 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# This file is autogenerated by `utils/feature_template_docs_generator.py`


from __future__ import annotations


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    cisco_omp:
        description: Configuration settings for the Cisco Overlay Management Protocol
            (OMP) feature template.
        type: dict
        suboptions:
            graceful_restart:
                description:
                - Enable or disable graceful restart for OMP.
                required: false
                default: null
                type: str
            overlay_as:
                description:
                - The autonomous system number used for the overlay.
                required: false
                default: null
                type: str
            send_path_limit:
                description:
                - The maximum number of paths that can be sent for each prefix.
                required: false
                default: null
                type: str
            ecmp_limit:
                description:
                - The maximum number of equal-cost multi-path routes.
                required: false
                default: null
                type: str
            shutdown:
                description:
                - Enable or disable the shutdown of OMP.
                required: false
                default: null
                type: str
            omp_admin_distance_ipv4:
                description:
                - The administrative distance for IPv4 routes learned via OMP.
                required: false
                default: null
                type: str
            omp_admin_distance_ipv6:
                description:
                - The administrative distance for IPv6 routes learned via OMP.
                required: false
                default: null
                type: str
            advertisement_interval:
                description:
                - The interval between sending unsolicited OMP route advertisements.
                required: false
                default: null
                type: str
            graceful_restart_timer:
                description:
                - The timer for graceful restart, specifying the period during which
                    peerings are preserved.
                required: false
                default: null
                type: str
            eor_timer:
                description:
                - End-of-RIB (EOR) timer which indicates stability of the route table.
                required: false
                default: null
                type: str
            holdtime:
                description:
                - The amount of time that the routes are preserved while the peer
                    is unreachable.
                required: false
                default: null
                type: str
            advertise:
                description:
                - A list of IPv4 advertise rules.
                required: false
                default: null
                type: list
                elements: dict
                suboptions:
                    protocol:
                        description:
                        - The IPv4 routing protocol whose routes are to be advertised.
                        required: true
                        default: null
                        type: str
                        choices:
                        - bgp
                        - ospf
                        - ospfv3
                        - connected
                        - static
                        - eigrp
                        - lisp
                        - isis
                    route:
                        description:
                        - The type of IPv4 routes to be advertised. For example, 'external'
                            for external routes.
                        required: false
                        default: null
                        type: str
                        choices:
                        - external
            ipv6_advertise:
                description:
                - A list of IPv6 advertise rules.
                required: false
                default: null
                type: list
                elements: dict
                suboptions:
                    protocol:
                        description:
                        - The IPv6 routing protocol whose routes are to be advertised.
                        required: true
                        default: null
                        type: str
                        choices:
                        - bgp
                        - ospf
                        - connected
                        - static
                        - eigrp
                        - lisp
                        - isis
            ignore_region_path_length:
                description:
                - Whether to ignore the region part of the path length for OMP routes.
                required: false
                default: null
                type: str
            transport_gateway:
                description:
                - Specifies the preferred transport gateway selection strategy.
                required: false
                default: null
                type: str
                choices:
                - prefer
                - ecmp-with-direct-path
            site_types:
                description:
                - A list of site types that are allowed to participate in the overlay
                    network.
                required: false
                default: null
                type: list
                elements: str
            auto_translate:
                description:
                - Enable or disable automatic translation of network settings.
                required: false
                default: null
                type: str
    '''