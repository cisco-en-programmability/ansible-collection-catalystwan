#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2025 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: policy
version_added: "0.1.0"
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
  localized:
  definition:
  list:
  certificates:
    description: Configuration for controller certificate authorization.
    type: dict
    aliases: [cca, controller_certificate_authorization]
    suboptions:
      certificate_signing:
        description: Defines the certificate signing authority.
        type: str
        choices: ["cisco", "manual", "enterprise"]
        default: "cisco"
      email:
        description: Email address to use for the certificate.
        type: str
      first_name:
        description: First name to use for the certificate.
        type: str
      last_name:
        description: Last name to use for the certificate.
        type: str
      retrieve_interval:
        description: Defines the interval to retrieve certificates in minutes.
        type: str
        choices: ["1", "2", "3", ..., "60"]
        default: "5"
      validity_period:
        description: Defines the validity period for the certificate.
        type: str
        choices: ["1Y", "2Y"]
        default: "1Y"
  enterprise_root_ca:
    description: Configuration for enterprise root certificate.
    type: str
    aliases: [enterprise_root_certificate]
  org:
    description: Name of the organization.
    type: str
    aliases: [organization]
  pnp_connect_sync:
    description: Configures the PnP Connect Sync mode.
    type: str
    choices: ["on", "off"]
    default: "off"
    aliases: [pnp_connect_sync_mode]
  smart_account_credentials:
    description: Smart Account credentials for authentication.
    type: dict
    aliases: [smart_account]
    suboptions:
      password:
        description: Password for Smart Account.
        type: str
        required: true
        no_log: true
      username:
        description: Username for Smart Account.
        type: str
        required: true
  validator:
    description: Configuration for vBond validator.
    type: dict
    aliases: [vbond]
    suboptions:
      domain_ip:
        description: Domain IP of the vBond validator.
        type: str
      port:
        description: Port number for the vBond validator.
        type: int
  software_install_timeout:
    description: Configuration for upgrades timeout.
    type: dict
    suboptions:
      download_timeout:
        description: Download Timeout in minutes, should be in range 60-360.
        type: str
      activate_timeout:
        description: Activate Timeout in minutes, should be in range 30-180.
        type: str
      control_pps:
        description: Control PPS, should be in range 300-65535.
        type: str
author:
  - Piotr Piwowarski (pipiwowa@cisco.com)

extends_documentation_fragment:
  - cisco.catalystwan.manager_authentication
"""

EXAMPLES = r"""
# Example of using the module to configure vBond validator
- name: Configure vBond validator
  cisco.catalystwan.administration_settings:
    validator:
      domain_ip: "192.0.2.1"
      port: "12346"
    manager_credentials:
      url: "https://vmanage.example.com"
      username: "admin"
      password: "securepassword123"  # pragma: allowlist secret
      port: "8443"

# Example of using the module to configure certificates
- name: Configure certificates
  cisco.catalystwan.administration_settings:
    certificates:
      certificate_signing: "cisco"
      validity_period: "2Y"
      retrieve_interval: 10
      first_name: "John"
      last_name: "Doe"
      email: "john.doe@example.com"
    manager_credentials: ...

# Example of using the module to configure the certificate used for enterprise signing
- name: Configure enterprise root CA
  cisco.catalystwan.administration_settings:
    enterprise_root_ca: "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----\n"
    manager_credentials: ...

# Example of using the module to configure Smart Account credentials
- name: Configure Smart Account credentials
  cisco.catalystwan.administration_settings:
    smart_account_credentials:
      username: "smartuser"
      password: "smartpass"  # pragma: allowlist secret
    manager_credentials: ...

# Example of using the module to configure PnP Connect Sync
- name: Configure PnP Connect Sync
  cisco.catalystwan.administration_settings:
    pnp_connect_sync: "ON"
    manager_credentials: ...

# Example of using the module to configure the organization name
- name: Configure organization name
  cisco.catalystwan.administration_settings:
    org: "ExampleOrganization"
    manager_credentials: ...
"""

RETURN = r"""
msg:
  description: Message detailing the outcome of the operation.
  returned: always
  type: str
  sample: "Successfully updated requested administration settings."
response:
  description: Detailed response for each section of administration settings that has been touched.
    Includes current state when no changes were applied.
  returned: always
  type: complex
  contains:
    org:
      description: Organization settings.
      returned: when org is provided
      type: dict
      sample: {"name": "ExampleOrganization"}
    validator:
      description: vBond validator settings.
      returned: when validator is provided
      type: dict
      sample: {"domain_ip": "192.0.2.1", "port": "12346"}
    certificates:
      description: Controller certificate authorization settings.
      returned: when certificates are provided
      type: dict
      sample: {
        "certificate_signing": "cisco",
        "validity_period": "2Y",
        "retrieve_interval": "10",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
      }
    smart_account_credentials:
      description: Smart Account credentials settings.
      returned: when smart_account_credentials are provided
      type: dict
      sample: {"username": "smartuser"}
    pnp_connect_sync:
      description: PnP Connect Sync mode settings.
      returned: when pnp_connect_sync is provided
      type: str
      sample: "ON"
"""


from typing import Literal, Optional, get_args
from uuid import UUID

from catalystwan.api.task_status_api import Task
from catalystwan.models.policy import (
    AnyPolicyDefinition,
    AnyPolicyList,
    CentralizedPolicy,
    CentralizedPolicyInfo,
    LocalizedPolicy,
    LocalizedPolicyInfo,
)
from catalystwan.models.policy.centralized import CentralizedPolicyEditPayload
from catalystwan.session import ManagerHTTPError
from catalystwan.typed_list import DataSequence

from ..module_utils.policy_templates.centralized import policy_centralized_definition
from ..module_utils.policy_templates.definition import policy_definition_definition, policy_definition_type_mapping
from ..module_utils.policy_templates.list import policy_list_definition, policy_list_type_mapping
from ..module_utils.policy_templates.localized import policy_localized_definition
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
            ),
        ],
        mutually_exclusive=[
            (
                "centralized",
                "localized",
                "list",
                "definition",
            ),
        ],
    )

    object_name: str = module.params.get("name")
    object_description: str = module.params.get("description")

    if module.params.get("centralized"):
        object_pretty_name = "Centralized Policy"
        object_type = CentralizedPolicy
        object_endpoint = module.session.api.policy.centralized
        all_centralized_policy: DataSequence[CentralizedPolicyInfo] = module.get_response_safely(object_endpoint.get)
        filtered_definitions: Optional[DataSequence[CentralizedPolicyInfo]] = all_centralized_policy.filter(
            policy_name=object_name
        )
        if filtered_definitions:
            existing_object: DataSequence[CentralizedPolicy] = [
                module.get_response_safely(object_endpoint.get, id=filtered_definitions[0].policy_id)
            ]
            existing_object_id = filtered_definitions[0].policy_id
        else:
            existing_object = []

        if module.params.get("state") in ("active", "present") and not existing_object:
            object_to_create = object_type(
                policy_name=object_name,
                policy_description=object_description,
                policy_type=module.params.get("centralized").get("type"),
                policy_definition=module.params.get("centralized").get("definition"),
                is_policy_activated=module.params.get("state") == "active",
            )
        elif module.params.get("state") in ("active", "present"):
            object_to_create = CentralizedPolicyEditPayload(
                policy_name=object_name,
                policy_description=object_description,
                policy_type=module.params.get("centralized").get("type"),
                policy_definition=module.params.get("centralized").get("definition"),
                is_policy_activated=module.params.get("state") == "active",
                policy_id=existing_object_id,
            )

    elif module.params.get("localized"):
        object_pretty_name = "Localized Policy"
        object_type = LocalizedPolicy
        object_endpoint = module.session.api.policy.localized
        all_localized_policy: DataSequence[LocalizedPolicyInfo] = module.get_response_safely(object_endpoint.get)
        filtered_definitions: Optional[DataSequence[LocalizedPolicyInfo]] = all_localized_policy.filter(
            policy_name=object_name
        )
        if filtered_definitions:
            existing_object: DataSequence[LocalizedPolicy] = [
                module.get_response_safely(object_endpoint.get, id=filtered_definitions[0].policy_id)
            ]
            existing_object_id = filtered_definitions[0].policy_id
        else:
            existing_object = []

        if module.params.get("state") in ("active", "present") and not existing_object:
            object_to_create = object_type(
                policy_name=object_name,
                policy_description=object_description,
                policy_type=module.params.get("localized").get("type"),
                policy_definition=module.params.get("localized").get("definition"),
            )
        elif module.params.get("state") in ("active", "present"):
            object_to_create = LocalizedPolicy(
                policy_name=object_name,
                policy_description=object_description,
                policy_type=module.params.get("localized").get("type"),
                policy_definition=module.params.get("localized").get("definition"),
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
                elif module.params.get("localized"):
                    object_endpoint.edit(policy=object_to_create)
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
                if module.params.get("centralized") or module.params.get("localized"):
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
