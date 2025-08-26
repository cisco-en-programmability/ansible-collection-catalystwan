#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2025 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: tenants_info
short_description: Get information about temamts.
version_added: "0.3.5"
description:
  - This module allows you to get tenants Info from vManage.
options:
  filters:
    description:
      - A dictionary of filters used to select tenants info.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the tenant.
        required: false
        default: null
        type: str
      description:
        description:
          - Description of the tenant.
        required: false
        default: null
        type: str
      org_name:
        description:
          - Description of the tenant.
        required: false
        default: null
        type: str
      subdomain:
        description:
          - Description of the tenant.
        required: false
        default: null
        type: str
      id:
        description:
          - tenant ID.
        required: false
        default: null
        type: str
extends_documentation_fragment:
  - cisco.catalystwan.manager_authentication
notes:
  - Ensure that the provided credentials have sufficient permissions to manage tenants in vManage.
"""

EXAMPLES = r"""
- name: Get all vmanage tenants available
  cisco.catalystwan.tenants:
    filters:
      device_type: vmanage
    manager_credentials: ...
"""

RETURN = r"""
msg:
  description: A message describing the result of the operation.
  returned: always
  type: str
  sample: "Succesfully got all requested tenants Info from vManage"
changed:
  description: A boolean flag indicating if any changes were made.
  returned: always
  type: bool
  sample: true
tenants_info:
  description: List of tenants filtered by arguments provided to module.
  returned: always
  type: list
tenancy_mode:
  description: Current tenancy mode of cluster.
  returned: always
  type: str
tenancy_domain:
  description: Name of multitenancy domain.
  returned: always
  type: str
"""

from typing import Literal

from catalystwan.models.tenant import Tenant
from catalystwan.endpoints.cluster_management import TenancyMode
from catalystwan.typed_list import DataSequence

from ..module_utils.result import ModuleResult
from ..module_utils.vmanage_module import AnsibleCatalystwanModule


def run_module():
    module_args = dict(
        filters=dict(type="dict", default=None, required=False),
    )
    result = ModuleResult()

    module = AnsibleCatalystwanModule(argument_spec=module_args)

    filters = module.params.get("filters")

    all_tenants: DataSequence[Tenant] = module.get_response_safely(
        module.session.api.tenant_management.get
    )

    tenancy_mode: TenancyMode = module.get_response_safely(
        module.session.endpoints.cluster_management.get_tenancy_mode
    )
    result.tenancy_mode = tenancy_mode.mode
    result.tenancy_domain = tenancy_mode.domain

    if module.params.get("filters"):
        result.tenants_info = [tenant for tenant in all_tenants.filter(**filters)]
    else:
        result.tenants_info = [tenant for tenant in all_tenants]

    if result.tenants_info:
        module.logger.info(f"All tenants filtered with filters: {filters}:\n{result.tenants_info}")
        result.msg = "Succesfully got all requested tenants Info from vManage"
    else:
        module.logger.warning(msg=f"tenants filtered with `{filters}` not present.")
        result.msg = f"tenants filtered with `{filters}` not present on vManage."

    module.exit_json(**result.model_dump(mode="json"))


def main():
    run_module()


if __name__ == "__main__":
    main()
