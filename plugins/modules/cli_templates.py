#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2024 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: cli_templates
short_description: Manage CLI templates in Cisco SDWAN
version_added: "0.2.0"
description:
  - This module allows you to create or delete CLI templates in Cisco SDWAN.
options:
  state:
    description:
      - Whether the CLI template should be present or absent on the Cisco SDWAN.
    required: false
    type: str
    choices: ["present", "absent"]
    default: "present"
  template_name:
    description:
      - The name of the CLI template.
    required: true
    type: str
  template_description:
    description:
      - The description of the CLI template.
    required: false
    type: str
    default: None
  config_file:
    description:
      - The path to the configuration file that contains the CLI template content.
    required: false
    type: str
    aliases: ["running_config_file_path"]
  force:
    description:
      - Update already existing templates. When template is attached to devices, reattach new version.
    required: false
    type: bool
    default: false
  timeout_seconds:
    description:
      - The timeout in seconds for attaching the template. Default is 300.
    type: int
author:
  - Arkadiusz Cichon (acichon@cisco.com)
extends_documentation_fragment:
  - cisco.catalystwan.device_models_device_template
  - cisco.catalystwan.manager_authentication
notes:
  - Ensure that the provided credentials have sufficient permissions to manage templates and devices in vManage.
"""

EXAMPLES = r"""
- name: Using configuration from file, ensure a CLI template is present on vManage
  cisco.catalystwan.cli_templates:
    state: present
    template_name: "MyTemplate"
    template_description: "This is a CLI template for device configuration"
    device_model: "ISR4451"
    config_file: "/path/to/config_file.txt"
    manager_credentials: ...

- name: Remove a CLI template from vManage
  cisco.catalystwan.cli_templates:
    state: absent
    template_name: "MyTemplate"
    manager_credentials: ...
"""

RETURN = r"""
msg:
  description: A message describing the result of the operation.
  returned: always
  type: str
  sample: "Created template MyTemplate: MyTemplate. Template id: abc123"
changed:
  description: A boolean flag indicating if any changes were made.
  returned: always
  type: bool
  sample: true
template_id:
  description: The ID of the template that was created or modified.
  returned: when a template is created
  type: str
  sample: "abc123"
"""

from typing import List, Literal, Optional, get_args

from catalystwan.api.template_api import CLITemplate
from catalystwan.api.templates.device_template.device_template import DeviceTemplateConfigAttached
from catalystwan.dataclasses import Device
from catalystwan.models.common import DeviceModel
from catalystwan.models.templates import DeviceTemplateInformation
from catalystwan.session import ManagerHTTPError
from catalystwan.typed_list import DataSequence
from ciscoconfparse import CiscoConfParse  # type: ignore
from pydantic import BaseModel, Field

from ..module_utils.result import ModuleResult
from ..module_utils.vmanage_module import AnsibleCatalystwanModule

State = Literal["present", "absent"]


class ExtendedManagerResponse(BaseModel):
    process_id: Optional[str] = Field(default=None, validation_alias="processId", serialization_alias="processId")
    attached_configs: Optional[List[DeviceTemplateConfigAttached]] = Field(
        default=None, validation_alias="attachedDevices", serialization_alias="attachedDevices"
    )


def run_module():
    module_args = dict(
        state=dict(
            type=str,
            choices=list(get_args(State)),
            default="present",
        ),
        template_name=dict(type="str", required=True),
        template_description=dict(type="str", default=None),
        device_model=dict(type="str", aliases=["device_type"], choices=list(get_args(DeviceModel)), default=None),
        config_file=dict(type="str", aliases=["running_config_file_path"]),
        force=dict(type="bool", default=False),
        timeout_seconds=dict(type="int", default=300),
    )
    result = ModuleResult()

    module = AnsibleCatalystwanModule(
        argument_spec=module_args,
        required_if=[
            (
                "state",
                "present",
                (
                    "template_name",
                    "template_description",
                    "device_model",
                ),
            ),
            (
                "state",
                "absent",
                ("template_name",),
            ),
        ],
    )

    template_name = module.params.get("template_name")

    all_templates: DataSequence[DeviceTemplateInformation] = module.get_response_safely(
        module.session.api.templates.get, template=CLITemplate
    )
    target_template: Optional[DeviceTemplateInformation] = all_templates.filter(name=template_name)

    if module.params.get("state") == "present":
        # Code for checking if template name exists already
        if target_template and not module.params.get("force"):
            module.logger.debug(f"Detected existing template:\n{target_template}\n")
            result.msg = (
                f"Template with name {template_name} already present on vManage, skipping create template operation."
            )
        elif target_template:
            current_template = module.get_response_safely(
                module.session.api.templates.get_device_template, template_id=target_template[0].id
            )
            current_template_configuration = CiscoConfParse(current_template.template_configuration.splitlines())

            new_template = CLITemplate(
                template_name=template_name,
                template_description=module.params.get("template_description"),
                device_model=module.params.get("device_model"),
            )
            new_template_configuration = new_template.load_from_file(file=module.params.get("config_file"))

            template_configuration_diff = CLITemplate.compare_template(
                current_template_configuration, new_template_configuration
            )
            if template_configuration_diff:
                module.logger.debug(f"Detected changes:\n{template_configuration_diff}\nTemplate will be updated")
                response = module.get_response_safely(module.session.api.templates.edit, template=new_template)
                template_config_attached = response.dataseq(ExtendedManagerResponse)[0].attached_configs
                all_devices: DataSequence[Device] = module.get_response_safely(module.session.api.devices.get)
                for attached_config in template_config_attached:
                    module.logger.debug(
                        f"Template is attached to device: {attached_config.uuid}\nReattaching new version"
                    )
                    device = all_devices.filter(uuid=attached_config.uuid)[0]
                    module.get_response_safely(
                        module.session.api.templates.edit_before_push, name=template_name, device=device
                    )
                    response = module.session.api.templates.attach(
                        name=template_name,
                        device=device,
                        timeout_seconds=module.params.get("timeout_seconds"),
                        is_edited=True,
                    )
                result.changed = True
                result.msg = (
                    f"Template with name {template_name} already present on vManage is different than provided."
                    " Updating and reattaching."
                )
            else:
                module.logger.debug(f"Detected existing template:\n{target_template}\n")
                result.msg = (
                    f"Template with name {template_name} already present on vManage and is the same as provided."
                    " Skipping template update."
                )
        else:
            cli_template = CLITemplate(
                template_name=template_name,
                template_description=module.params.get("template_description"),
                device_model=module.params.get("device_model"),
            )
            cli_template.load_from_file(file=module.params.get("config_file"))

            module.logger.debug(f"Prepared template for sending to vManage, template configuration:\n{cli_template}\n")
            try:
                template_id: str = module.session.api.templates.create(
                    template=cli_template, debug=module.params.get("debug")
                )
            except ManagerHTTPError as ex:
                module.fail_json(
                    msg=f"Could not perform create CLI Template {template_name}.\nManager error: {ex.info}"
                )
            result.changed = True
            result.msg += f"Created template {template_name}: {cli_template.template_name}. Template id: {template_id}"

    if module.params.get("state") == "absent":
        if target_template:
            module.send_request_safely(
                result,
                action_name="Delete Template",
                send_func=module.session.api.templates.delete,
                template=CLITemplate,
                name=template_name,
            )
            result.changed = True
            result.msg = f"Deleted template {template_name}"
        else:
            module.logger.debug(f"Template '{target_template}' not presend in list of Templates on vManage.")
            result.msg = (
                f"Template {template_name} not presend in list of CLI Templates on vManage. "
                "skipping delete template operation."
            )

    module.exit_json(**result.model_dump(mode="json"))


def main():
    run_module()


if __name__ == "__main__":
    main()
