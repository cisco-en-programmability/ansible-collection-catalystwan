#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2025 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: cli_templates_info
short_description: Get information about CLI Templates on vManage.
version_added: "0.3.5"
description:
  - This module allows you to get CLI Templates Info from vManage.
options:
  filters:
    description:
      - A dictionary of filters used to select CLI Templates info.
    type: dict
    required: false
    suboptions:
      device_type:
        description:
          - The device type of the template
        required: false
        default: null
        type: list
        elements: str
      name:
        description:
          - The name of the CLI Template.
        required: false
        default: null
        type: str
      description:
        description:
          - Description of the CLI Template.
        required: false
        default: null
        type: str
      version:
        description:
          - Version of the CLI Template.
        required: false
        default: null
        type: str
      factory_default:
        description:
          - If template is Factory Default template.
        required: false
        default: null
        type: bool
      draft_mode:
        description:
          - The draft mode of template.
        required: false
        default: null
        type: str
      device_role:
        description:
          - The device role.
        required: false
        default: null
        type: str
      id:
        description:
          - CLI Template ID.
        required: false
        default: null
        type: str
      last_updated_on:
        description:
          - Last Updated on value.
        required: false
        default: null
        type: int
      last_updated_by:
        description:
          - Last Updated by value.
        required: false
        default: null
        type: str
      resource_group:
        description:
          - Resource Group value.
        required: false
        default: null
        type: str
  gather_configuration:
    description:
      - Retrieve a templates_configuration list, including detailed configurations for each device in the result.
    type: bool
    default: False
extends_documentation_fragment:
  - cisco.catalystwan.manager_authentication
notes:
  - Ensure that the provided credentials have sufficient permissions to manage templates and devices in vManage.
"""

EXAMPLES = r"""
- name: Get all vmanage CLI Templates available
  cisco.catalystwan.cli_templates:
    filters:
      device_type: vmanage
    manager_credentials: ...
"""

RETURN = r"""
msg:
  description: A message describing the result of the operation.
  returned: always
  type: str
  sample: "Succesfully got all requested CLI Templates Info from vManage"
changed:
  description: A boolean flag indicating if any changes were made.
  returned: always
  type: bool
  sample: true
templates_info:
  description: List of CLI templates filtered by arguments provided to module.
  returned: always
  type: list
templates_configuration:
  description: List of CLI templates detailed configuration filtered by arguments provided to module.
  returned: when gather_configuration is set
  type: list
"""

from catalystwan.api.template_api import CLITemplate
from catalystwan.api.templates.device_template.device_template import DeviceTemplate
from catalystwan.models.templates import DeviceTemplateInformation
from catalystwan.typed_list import DataSequence

from ..module_utils.result import ModuleResult
from ..module_utils.vmanage_module import AnsibleCatalystwanModule


def run_module():
    module_args = dict(
        filters=dict(type="dict", default=None, required=False),
        gather_configuration=dict(type="bool", default=False),
    )
    result = ModuleResult()

    module = AnsibleCatalystwanModule(argument_spec=module_args)

    filters = module.params.get("filters")

    all_templates: DataSequence[DeviceTemplateInformation] = module.get_response_safely(
        module.session.api.templates.get, template=CLITemplate
    )

    if module.params.get("filters"):
        result.templates_info = [template for template in all_templates.filter(**filters)]
    else:
        result.templates_info = [template for template in all_templates]

    if module.params.get("gather_configuration"):
        result.templates_configuration = []
        for template in result.templates_info:
            detailed_template: DeviceTemplate = module.get_response_safely(
                module.session.api.templates.get_device_template, template_id=template.id
            )
            result.templates_configuration.append(detailed_template)

    if result.templates_info:
        module.logger.info(f"All CLI Templates filtered with filters: {filters}:\n{result.templates_info}")
        result.msg = "Succesfully got all requested CLI Templates Info from vManage"
    else:
        module.logger.warning(msg=f"CLI templates filtered with `{filters}` not present.")
        result.msg = f"CLI templates filtered with `{filters}` not present on vManage."

    module.exit_json(**result.model_dump(mode="json"))


def main():
    run_module()


if __name__ == "__main__":
    main()
