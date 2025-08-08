#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2025 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: policy
version_added: "0.3.4"
short_description: Manages policies on Manager instance
description:
  - Allow to create, update and delete policy lists, policy definitions, centralized policies and localized policies
  - More settings can be enhanced by reusing
    https://github.com/cisco-en-programmability/catalystwan-sdk/blob/main/catalystwan/api/policy_api.py
options:
  state:
    description:
      - Desired state for the policy.
      - Active state is available only for centralized policy
    type: str
    choices: ["absent", "present", "active"]
    default: "present"
  name:
    description:
      - The name for the Policy object.
    type: str
    required: true
  description:
    description:
      - Description for the Policy object.
    type: str
    required: false
  centralized:
    description:
      - Centralized policy definition
      - The centralized, localized, definition and list options are mutually exclusive.
    type: dictionary
  localized:
    description:
      - Localized policy definition
      - The centralized, localized, definition and list options are mutually exclusive.
    type: dictionary
  definition:
    description:
      - Policy definition object
      - The centralized, localized, definition and list options are mutually exclusive.
    type: dictionary
  list:
    description:
      - Policy list object
      - The centralized, localized, definition and list options are mutually exclusive.
    type: dictionary
author:
  - Piotr Piwowarski (pipiwowa@cisco.com)

extends_documentation_fragment:
  - cisco.catalystwan.manager_authentication
"""

EXAMPLES = r"""
# Example of creating VPN list
- name: Create VPN list
  cisco.catalystwan.policy:
    name: my_vpn_list
    list:
      type: "vpn"
      entries:
        - vpn: 100
    manager_credentials: ...

# Example of creating hub and spoke policy definition
- name: Create hub and spoke policy definition
  cisco.catalystwan.policy:
    name: my_hub_and_spoke_policy
    definition:
      type: "hub_and_spoke"
      definition:
        vpnList: "{{ vpn_list.id }}"
        subDefinitions:
          - name: "My Hub-and-Spoke"
            equalPreference: true
            advertiseTloc: false
            spokes:
              - siteList: "{{ spoke_list.id }}"
                hubs:
                  - siteList: "{{ hub_list.id }}"
    manager_credentials: ...
"""

RETURN = r"""
msg:
  description: Message detailing the outcome of the operation.
  returned: always
  type: str
  sample: "Centralized policy my-policy created on vManage."
id:
  description: The ID of the policy that was created or modified.
  returned: when a policy object is created
  type: str
  sample: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXX"
"""


from typing import Literal, Optional, get_args
from uuid import UUID

from catalystwan.api.task_status_api import Task
from catalystwan.models.policy import (
    AnyPolicyDefinition,
    AnyPolicyList,
    AnySecurityPolicyInfo,
    CentralizedPolicy,
    CentralizedPolicyInfo,
    LocalizedPolicy,
    LocalizedPolicyInfo,
    SecurityPolicy,
)
from catalystwan.models.policy.centralized import CentralizedPolicyEditPayload
from catalystwan.session import ManagerHTTPError
from catalystwan.typed_list import DataSequence

from ..module_utils.policy_templates.centralized import policy_centralized_definition
from ..module_utils.policy_templates.definition import policy_definition_definition, policy_definition_type_mapping
from ..module_utils.policy_templates.list import policy_list_definition, policy_list_type_mapping
from ..module_utils.policy_templates.localized import policy_localized_definition
from ..module_utils.policy_templates.security import policy_security_definition
from ..module_utils.result import ModuleResult
from ..module_utils.vmanage_module import AnsibleCatalystwanModule

State = Literal["active", "present", "absent"]


def are_objects_the_same(a, b):
    for attribute in [
        "description",
        "policy_description",
        "entries",
        "definition",
        "policy_type",
        "is_policy_activated",
        "policy_definition",
    ]:
        if hasattr(a, attribute) and vars(a)[attribute] != vars(b)[attribute]:
            return False
    return True


def run_module():
    module_args = dict(
        state=dict(
            type=str,
            choices=list(get_args(State)),
            default="present",
        ),
        name=dict(type="str", default=None),
        description=dict(type="str", default=""),
        **policy_list_definition,
        **policy_definition_definition,
        **policy_centralized_definition,
        **policy_localized_definition,
        **policy_security_definition,
    )

    result = ModuleResult()

    module = AnsibleCatalystwanModule(
        argument_spec=module_args,
        required_one_of=[
            (
                "centralized",
                "localized",
                "list",
                "definition",
                "security",
            ),
        ],
        mutually_exclusive=[
            (
                "centralized",
                "localized",
                "list",
                "definition",
                "security",
            ),
        ],
    )

    object_name: str = module.params.get("name")
    object_description: str = module.params.get("description")

    if module.params.get("centralized") or module.params.get("localized") or module.params.get("security"):
        if module.params.get("centralized"):
            object_pretty_name = "Centralized Policy"
            object_type = CentralizedPolicy
            object_edit_type = CentralizedPolicyEditPayload
            object_endpoint = module.session.api.policy.centralized
            policy_definition = module.params.get("centralized")
        elif module.params.get("localized"):
            object_pretty_name = "Localized Policy"
            object_type = LocalizedPolicy
            object_edit_type = object_type
            object_endpoint = module.session.api.policy.localized
            policy_definition = module.params.get("localized")
        elif module.params.get("security"):
            object_pretty_name = "Security Policy"
            object_type = SecurityPolicy
            object_edit_type = object_type
            object_endpoint = module.session.api.policy.security
            policy_definition = module.params.get("security")

        all_policies: DataSequence[
            CentralizedPolicyInfo | LocalizedPolicyInfo | AnySecurityPolicyInfo
        ] = module.get_response_safely(object_endpoint.get)
        if module.params.get("security"):
            all_policies = all_policies.security
        filtered_definitions: Optional[
            DataSequence[CentralizedPolicyInfo | LocalizedPolicyInfo | AnySecurityPolicyInfo]
        ] = all_policies.filter(policy_name=object_name)
        if filtered_definitions:
            existing_object: DataSequence[CentralizedPolicy | LocalizedPolicy | SecurityPolicy] = [
                module.get_response_safely(object_endpoint.get, id=filtered_definitions[0].policy_id)
            ]
            existing_object_id = filtered_definitions[0].policy_id
        else:
            existing_object = []

        if module.params.get("state") in ("active", "present") and not existing_object:
            object_to_create = object_type(
                policy_name=object_name,
                policy_description=object_description,
                policy_type=policy_definition.get("type"),
                policy_definition=policy_definition.get("definition"),
                is_policy_activated=module.params.get("state") == "active",
            )
        elif module.params.get("state") in ("active", "present"):
            object_to_create = object_edit_type(
                policy_name=object_name,
                policy_description=object_description,
                policy_type=policy_definition.get("type"),
                policy_definition=policy_definition.get("definition"),
                is_policy_activated=module.params.get("state") == "active",
                policy_id=existing_object_id,
            )

    elif module.params.get("definition"):
        object_pretty_name = "Policy Definition"
        object_type = policy_definition_type_mapping[module.params.get("definition").get("type")]
        object_endpoint = module.session.api.policy.definitions
        if module.params.get("state") in ("active", "present"):
            object_to_create = object_type(
                name=object_name,
                description=object_description,
                definition=module.params.get("definition").get("definition"),
                sequences=module.params.get("definition").get("sequences"),
            )
        all_policy_definitions: DataSequence[AnyPolicyDefinition] = module.get_response_safely(
            object_endpoint.get, type=object_type
        )
        filtered_definitions: Optional[DataSequence[AnyPolicyDefinition]] = all_policy_definitions.filter(
            name=object_name
        )
        if filtered_definitions:
            existing_object: AnyPolicyDefinition = [
                module.get_response_safely(
                    object_endpoint.get, type=object_type, id=filtered_definitions[0].definition_id
                )
            ]
            existing_object_id = existing_object[0].definition_id
        else:
            existing_object = []

    elif module.params.get("list"):
        object_pretty_name = "Policy List"
        object_type = policy_list_type_mapping[module.params.get("list").get("type")]
        object_endpoint = module.session.api.policy.lists
        if module.params.get("state") in ("active", "present"):
            object_to_create = object_type(
                name=object_name,
                description=object_description,
                entries=module.params.get("list").get("entries"),
            )
        all_list_objects: DataSequence[AnyPolicyList] = module.get_response_safely(
            object_endpoint.get, type=object_type
        )
        existing_object: Optional[DataSequence[AnyPolicyList]] = all_list_objects.filter(name=object_name)
        if existing_object:
            existing_object_id = existing_object[0].list_id

    if module.params.get("state") in ("active", "present"):
        # object already exists in Manager and is the same -> return id
        if existing_object and are_objects_the_same(object_to_create, existing_object[0]):
            module.logger.debug(f"{object_pretty_name} already present: \n{object_name}\n")
            result.msg = f"{object_pretty_name} {object_name} already present on vManage, skipping create operation."
            result.id = existing_object_id

        # object already exists in Manager but is different -> update object and return id
        elif existing_object:
            try:
                if module.params.get("centralized"):
                    if object_to_create.is_policy_activated != existing_object[0].is_policy_activated:
                        if object_to_create.is_policy_activated:
                            device_action: Task = module.get_response_safely(
                                object_endpoint.activate, id=existing_object_id
                            )
                        else:
                            device_action: Task = module.get_response_safely(
                                object_endpoint.deactivate, id=existing_object_id
                            )
                        device_action.wait_for_completed()
                    object_endpoint.edit(policy=object_to_create)
                elif module.params.get("localized") or module.params.get("security"):
                    object_endpoint.edit(id=existing_object_id, policy=object_to_create)
                elif module.params.get("definition"):
                    object_endpoint.edit(
                        id=existing_object_id,
                        policy_definition=object_to_create,
                    )
                elif module.params.get("list"):
                    object_endpoint.edit(
                        id=existing_object_id,
                        policy_list=object_to_create,
                    )
            except ManagerHTTPError as ex:
                module.fail_json(
                    msg=f"Could not perform edit {object_pretty_name} {object_name}.\nManager error: {ex.info}"
                )
            result.changed = True

            module.logger.debug(f"{object_pretty_name} updated: \n{object_name}\n")
            result.msg = f"{object_pretty_name} {object_name} updated on vManage."
            result.id = existing_object_id

        # object doesn't exist in Manager and needs to be created
        else:
            try:
                if module.params.get("centralized") or module.params.get("localized") or module.params.get("security"):
                    created_uuid: UUID = module.get_response_safely(object_endpoint.create, policy=object_to_create)
                elif module.params.get("definition"):
                    created_uuid: UUID = module.get_response_safely(
                        object_endpoint.create,
                        policy_definition=object_to_create,
                    )
                elif module.params.get("list"):
                    created_uuid: UUID = module.get_response_safely(
                        object_endpoint.create,
                        policy_list=object_to_create,
                    )
            except ManagerHTTPError as ex:
                module.fail_json(
                    msg=f"Could not perform create {object_pretty_name} {object_name}.\nManager error: {ex.info}"
                )
            result.changed = True

            module.logger.debug(f"{object_pretty_name} created: \n{object_name}\n")
            result.msg = f"{object_pretty_name} {object_name} created on vManage."
            result.id = created_uuid

    if module.params.get("state") == "absent":
        if existing_object:
            if module.params.get("centralized") or module.params.get("localized"):
                if module.params.get("centralized") and existing_object[0].is_policy_activated:
                    device_action: Task = module.get_response_safely(object_endpoint.deactivate, id=existing_object_id)
                    device_action.wait_for_completed()
                module.send_request_safely(
                    result,
                    action_name=f"Delete {object_pretty_name}",
                    send_func=object_endpoint.delete,
                    id=existing_object_id,
                )
            else:
                module.send_request_safely(
                    result,
                    action_name=f"Delete {object_pretty_name}",
                    send_func=object_endpoint.delete,
                    type=object_type,
                    id=existing_object_id,
                )
            result.changed = True
            result.msg = f"Deleted {object_pretty_name} {object_name}"
        else:
            module.logger.debug(f"{object_pretty_name} '{object_name}' not present in vManage.")
            result.msg = f"{object_pretty_name} {object_name} not present in vManage. "

    module.exit_json(**result.model_dump(mode="json"))


def main():
    run_module()


if __name__ == "__main__":
    main()
