from typing import Mapping

from catalystwan.models import policy as policy_models

_policy_definition_model_names = {
    "access_control_list": "AclPolicy",
    "access_control_policy_ipv6": "AclIPv6Policy",
    "aip": "AdvancedInspectionProfilePolicy",
    "amp": "AdvancedMalwareProtectionPolicy",
    "cflowd": "CflowdPolicy",
    "control": "ControlPolicy",
    "device_access": "DeviceAccessPolicy",
    "device_access_ipv6": "DeviceAccessIPv6Policy",
    "dns_security": "DnsSecurityPolicy",
    "hub_and_spoke": "HubAndSpokePolicy",
    "intrusion_prevention": "IntrusionPreventionPolicy",
    "mesh": "MeshPolicy",
    "qos_map": "QoSMapPolicy",
    "rewrite": "RewritePolicy",
    "route_policy": "RoutePolicy",
    "rule_set": "RuleSet",
    "security_group": "SecurityGroup",
    "ssl_decryption": "SslDecryptionPolicy",
    "ssl_decryption_utd_profile": "SslDecryptionUtdProfilePolicy",
    "traffic_data": "TrafficDataPolicy",
    "url_filtering": "UrlFilteringPolicy",
    "vpn_membership": "VPNMembershipPolicy",
    "zone_based_firewall": "ZoneBasedFWPolicy",
}

policy_definition_type_mapping: Mapping[str, type] = {
    key: getattr(policy_models, model_name)
    for key, model_name in _policy_definition_model_names.items()
    if hasattr(policy_models, model_name)
}

policy_definition_definition = {
    "definition": {
        "default": None,
        "required": False,
        "type": "dict",
        "options": {
            "type": {
                "type": "str",
                "choices": policy_definition_type_mapping.keys(),
                "default": "feature",
            },
            "definition": {"type": "dict"},
        },
    }
}
