#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2025 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: tenants
short_description: Manage Tenants in Cisco SDWAN
version_added: "0.2.0"
description:
  - This module allows you to create or delete Tenants in Cisco SDWAN.
options:
  state:
    description:
      - Whether the Tenant should be present or absent on the Cisco SDWAN.
    required: false
    type: str
    choices: ["present", "absent"]
    default: "present"
  name:
    description:
      - The name of the Tenant.
    required: true
    type: str
  description:
    description:
      - The description of the Tenant.
    required: false
    type: str
    default: None
  org_name:
    description:
      - The organization name of the Tenant.
    required: false
    type: str
  subdomain:
    description:
      - The subdomain of the Tenant.
    required: false
    type: str
  wan_edge_forecast:
    description:
      - Forecasted number of edges in Tenant.
    required: false
    type: int
  wait_timeout_seconds:
    description:
      - The timeout in seconds for creating Tenant. Default is 7200.
    type: int
author:
  - Piotr Piwowarski (pipiwowa@cisco.com)
extends_documentation_fragment:
  - cisco.catalystwan.manager_authentication
notes:
  - Ensure that the provided credentials have sufficient permissions to manage tenants in vManage.
"""

EXAMPLES = r"""
- name: Create tenant
  cisco.catalystwan.tenants:
    name: "MyTenant"
    org_name: "my-tenant-org"
    description: "My tenant description"
    subdomain: "tenant.domain"
    wan_edge_forecast: "3"
    manager_authentication: ...

- name: Remove a Tenant from vManage
  cisco.catalystwan.tenants:
    state: absent
    name: "MyTenant"
    manager_credentials: ...
"""

RETURN = r"""
msg:
  description: A message describing the result of the operation.
  returned: always
  type: str
  sample: "Created tenant MyTenant"
changed:
  description: A boolean flag indicating if any changes were made.
  returned: always
  type: bool
  sample: true
"""

from typing import Literal, Optional, get_args

from catalystwan.api.task_status_api import Task
from catalystwan.models.tenant import Tenant
from catalystwan.session import ManagerRequestException
from catalystwan.typed_list import DataSequence
from catalystwan.vmanage_auth import UnauthorizedAccessError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed  # type: ignore

from ..module_utils.result import ModuleResult
from ..module_utils.vmanage_module import AnsibleCatalystwanModule

State = Literal["present", "absent"]

INTERVAL_SECONDS = 30
TIMEOUT_SECONDS = 7200


@retry(
    wait=wait_fixed(INTERVAL_SECONDS),
    stop=stop_after_attempt(int(TIMEOUT_SECONDS / INTERVAL_SECONDS)),
    retry=retry_if_exception_type((ManagerRequestException, UnauthorizedAccessError)),
    reraise=True,
)
def wait_for_task_data(module: AnsibleCatalystwanModule, result: ModuleResult, task: Task):
    task.session.login()
    task_data = task.wait_for_completed(timeout_seconds=module.params.get("wait_timeout_seconds"))
    if not task_data.result:
        result.msg = [data.activity for data in task_data.sub_tasks_data]
        result.response = task_data.json()
        module.fail_json(**result.model_dump(mode="json"))
    module.logger.info(f"Task data after task completed: {task_data.dict()}")


def run_module():
    module_args = dict(
        state=dict(
            type=str,
            choices=list(get_args(State)),
            default="present",
        ),
        name=dict(type="str", required=True),
        description=dict(type="str", default=None),
        org_name=dict(type="str", default=None),
        subdomain=dict(type="str", default=None),
        wan_edge_forecast=dict(type="int", default=None),
        wait_timeout_seconds=dict(
            type="int", default=7200
        ),  # 3600 is because vManage reports: 'configuration-dbStatus it may take up to 40 mins or longer'
    )
    result = ModuleResult()

    module = AnsibleCatalystwanModule(
        argument_spec=module_args,
        required_if=[
            (
                "state",
                "present",
                (
                    "name",
                    "description",
                    "org_name",
                    "subdomain",
                    "wan_edge_forecast",
                ),
            ),
        ],
    )

    tenant_name = module.params.get("name")

    all_tenants: DataSequence[Tenant] = module.get_response_safely(module.session.api.tenant_management.get)
    filtered_tenants: Optional[DataSequence[Tenant]] = all_tenants.filter(name=tenant_name)

    if module.params.get("state") == "present":
        # Code for checking if tenant exists already
        if filtered_tenants:
            module.logger.debug(f"Detected existing tenant:\n{filtered_tenants}\n")
            result.msg = f"Tenant with name {tenant_name} already present on vManage, skipping create tenant operation."
        else:
            create_task = module.session.api.tenant_management.create(
                tenants=[
                    Tenant(
                        name=tenant_name,
                        desc=module.params.get("description"),
                        org_name=module.params.get("org_name"),
                        subdomain=module.params.get("subdomain"),
                        wan_edge_forecast=module.params.get("wan_edge_forecast"),
                    )
                ]
            )

            wait_for_task_data(module=module, result=result, task=create_task)

            result.changed = True
            result.msg += f"Created tenant {tenant_name}."

    if module.params.get("state") == "absent":
        if filtered_tenants:
            delete_task = module.session.api.tenant_management.delete(tenant_id_list=[filtered_tenants[0].id])

            wait_for_task_data(module=module, result=result, task=delete_task)

            result.changed = True
            result.msg += f"Created tenant {tenant_name}."
        else:
            module.logger.debug(f"Tenant '{tenant_name}' not presend on vManage.")
            result.msg = f"Tenant '{tenant_name}' not presend on vManage. skipping delete tenant operation."

    module.exit_json(**result.model_dump(mode="json"))


def main():
    run_module()


if __name__ == "__main__":
    main()
