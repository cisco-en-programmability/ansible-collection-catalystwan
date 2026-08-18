from typing import Mapping

from catalystwan.models import policy as policy_models

_policy_list_model_names = {
    "app": "AppList",
    "app_probe": "AppProbeClassList",
    "as_path": "ASPathList",
    "class_map": "ClassMapList",
    "color": "ColorList",
    "communities": "CommunityList",
    "data_ipv6_prefix": "DataIPv6PrefixList",
    "data_prefix": "DataPrefixList",
    "expanded_community": "ExpandedCommunityList",
    "extended_community": "ExtendedCommunityList",
    "fax_protocol": "FaxProtocolList",
    "fqdn": "FQDNList",
    "geo_location": "GeoLocationList",
    "identity": "IdentityList",
    "ips_signature": "IPSSignatureList",
    "ipv6_prefix": "IPv6PrefixList",
    "local_app": "LocalAppList",
    "local_domain": "LocalDomainList",
    "media_profile": "MediaProfileList",
    "mirror": "MirrorList",
    "modem_pass_through": "ModemPassThroughList",
    "policer": "PolicerList",
    "port": "PortList",
    "preferred_color_group": "PreferredColorGroupList",
    "prefix": "PrefixList",
    "protocol_name": "ProtocolNameList",
    "region": "RegionList",
    "scalable_group_tag": "ScalableGroupTagList",
    "site": "SiteList",
    "sla": "SLAClassList",
    "supervisory_disconnect": "SupervisoryDisconnectList",
    "threat_grid_api_key": "ThreatGridApiKeyList",  # pragma: allowlist secret
    "tloc": "TLOCList",
    "translation_profile": "TranslationProfileList",
    "translation_rules": "TranslationRulesList",
    "trunk_group": "TrunkGroupList",
    "umbrella_data": "UmbrellaDataList",
    "url_allow": "URLAllowList",
    "url_block": "URLBlockList",
    "vpn": "VPNList",
    "zone": "ZoneList",
}

policy_list_type_mapping: Mapping[str, type] = {
    key: getattr(policy_models, model_name)
    for key, model_name in _policy_list_model_names.items()
    if hasattr(policy_models, model_name)
}

policy_list_definition = {
    "list": {
        "default": None,
        "required": False,
        "type": "dict",
        "options": {
            "type": {
                "type": "str",
                "choices": policy_list_type_mapping.keys(),
                "default": "feature",
            },
            "entries": {"type": "list"},
        },
    }
}
