#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2024 Cisco Systems, Inc. and its affiliates
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: Device_templates
short_description: Manage Device Templates on vManage.
version_added: "0.2.0"
description:
  - This module allows you to create, delete, attach and detach Device Templates
  - Device Templates can be filtered by Device Templates Info key:values.
options:
  state:
    description:
      - Desired state for the template.
      - 0(state=present) is equivalent of create template in GUI
    type: str
    choices: ["absent", "present", "attached"]
    default: "present"
  template_name:
    description:
      - The name for the Feature Template.
    type: str
    required: true
  template_description:
    description:
      - Description for the Feature Template.
    type: str
    required: true
  device_role:
    description:
      - The device role. Applicable to all devices except 'vManage' and 'vSmart'
    required: false
    default: null
    type: str
    choices: ["service-node", "sdwan-edge"]
  general_templates:
    description:
      - List of names of Feature Templates to be included in Device Template
      type: list
      elements: str
      required: false
  hostname:
    description:
      - Hostname of the device to attach template. Available only for 0(state=attached).
    type: str
author:
  - Arkadiusz Cichon (acichon@cisco.com)
extends_documentation_fragment:
  - cisco.catalystwan.device_models_device_template
  - cisco.catalystwan.manager_authentication
notes:
  - Ensure that the provided credentials have sufficient permissions to manage templates and devices in vManage.
"""

EXAMPLES = r"""
- name: Ensure a device template is present on vManage
  cisco.catalystwan.device_templates:
    state: present
    template_name: "MyDeviceTemplate"
    template_description: "This is a device template for device configuration"
    device_type: "ISR4451"
    device_role: "sdwan-edge"
    general_templates:
      - "Template1"
      - "Template2"
    manager_credentials: ...

- name: Attach a device template to a device with a specific hostname
  cisco.catalystwan.device_templates:
    state: attached
    template_name: "MyDeviceTemplate"
    hostname: "device-hostname"
    timeout_seconds: 600
    manager_credentials: ...

- name: Remove a device template from vManage
  cisco.catalystwan.device_templates:
    state: absent
    template_name: "MyDeviceTemplate"
    manager_credentials: ...
"""

RETURN = r"""
msg:
  description: A message describing the result of the operation.
  returned: always
  type: str
  sample: "Created template MyDeviceTemplate: MyDeviceTemplate"

changed:
  description: A boolean flag indicating if any changes were made.
  returned: always
  type: bool
  sample: true

templates_info:
  description: Detailed information about the templates.
  returned: when templates are queried
  type: dict
  sample: {
    "MyDeviceTemplate": {
      "template_id": "abc123",
      "template_name": "MyDeviceTemplate",
      "template_description": "This is a device template for device configuration",
      "device_type": "ISR4451",
      "device_role": "sdwan-edge",
      "general_templates": ["Template1", "Template2"]
    }
  }
"""

from typing import Dict, Literal, Optional, get_args

from catalystwan.api.template_api import DeviceTemplate
from catalystwan.dataclasses import Device, DeviceTemplateInfo
from catalystwan.models.common import DeviceModel
from catalystwan.session import ManagerHTTPError
from catalystwan.typed_list import DataSequence
from pydantic import Field

from ..module_utils.result import ModuleResult
from ..module_utils.vmanage_module import AnsibleCatalystwanModule

State = Literal["present", "absent", "attached"]


class ExtendedModuleResult(ModuleResult):
    templates_info: Optional[Dict] = Field(default={})


def run_module():
    module_args = dict(
        state=dict(
            type=str,
            choices=list(get_args(State)),
            default="present",
        ),
        template_name=dict(type="str", required=True),
        template_description=dict(type="str", default=None),
        device_type=dict(type="str", aliases=["device_model"], choices=list(get_args(DeviceModel)), default=None),
        device_role=dict(type="str", choices=["sdwan-edge", "service-node"], default=None),
        general_templates=dict(type="list", elements="str", default=[]),
        timeout_seconds=dict(type="int", default=300),
        hostname=dict(type="str"),
    )
    result = ExtendedModuleResult()

    module = AnsibleCatalystwanModule(
        argument_spec=module_args,
        required_if=[
            (
                "state",
                "present",
                (
                    "template_name",
                    "template_description",
                    "device_type",
                ),
            ),
            (
                "state",
                "absent",
                ("template_name",),
            ),
            (
                "state",
                "attached",
                (
                    "template_name",
                    "hostname",
                ),
            ),
        ],
    )

    template_name = module.params.get("template_name")

    all_templates: DataSequence[DeviceTemplateInfo] = module.get_response_safely(
        module.session.api.templates.get, template=DeviceTemplate
    )
    target_template: DeviceTemplateInfo = all_templates.filter(name=template_name)

    if module.params.get("state") == "present":
        # Code for checking if template name exists already
        if target_template:
            module.logger.debug(f"Detected existing template:\n{target_template}\n")
            result.msg = (
                f"Template with name {template_name} already present on vManage, skipping create template operation."
            )
        else:
            device_template = DeviceTemplate(
                template_name=template_name,
                template_description=module.params.get("template_description"),
                device_type=module.params.get("device_type"),
                device_role=module.params.get("device_role"),
                general_templates=module.params.get("general_templates"),
            )

            module.logger.debug(
                f"Prepared template for sending to vManage, template configuration:\n{device_template}\n"
            )
            try:
                module.session.api.templates.create(template=device_template, debug=module.params.get("debug"))
            except ManagerHTTPError as ex:
                module.fail_json(
                    msg=f"Could not perform add Feature Template {template_name}.\nManager error: {ex.info}"
                )
            result.changed = True
            result.msg += f"Created template {template_name}: {device_template}"

    if module.params.get("state") == "attached":
        hostname = module.params.get("hostname")
        device: DataSequence[Device] = (
            module.get_response_safely(module.session.api.devices.get).filter(hostname=hostname).single_or_default()
        )

        if not device:
            module.fail_json(f"No devices with hostname found, hostname provided: {hostname}")
        try:
            module.session.api.templates.attach(
                name=template_name, device=device, timeout_seconds=module.params.get("timeout_seconds")
            )
            result.changed = True
            result.msg = f"Attached template {template_name} to device: {hostname}"
        except ManagerHTTPError as ex:
            module.fail_json(msg=f"Could not perform attach Template {template_name}.\nManager error: {ex.info}")

    if module.params.get("state") == "absent":
        if target_template:
            module.send_request_safely(
                result,
                action_name="Delete Template",
                send_func=module.session.api.templates.delete,
                template=DeviceTemplate,
                name=template_name,
            )
            result.changed = True
            result.msg = f"Deleted template {template_name}"
        else:
            module.logger.debug(f"Template '{target_template}' not presend in list of Device Templates on vManage.")
            result.msg = (
                f"Template {template_name} not presend in list of Device Templates on vManage. "
                "skipping delete template operation."
            )

    module.exit_json(**result.model_dump(mode="json"))


def main():
    run_module()


if __name__ == "__main__":
    main()
