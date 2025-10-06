# Ansible Role: multitenant_mode

An Ansible role to enable multi-tenant mode on Cisco Catalyst SD-WAN vManage.

## Role Description

The `multitenant_mode` role performs the following tasks:

1. Verifies that the required variables for the role are present.
2. Sets the tenancy mode for and vManage instance.
3. Waits until vManage reboots after change

## Requirements

- `cisco.catalystwan` collection installed.
- Access details for the Cisco Manager instance must be provided.

## Dependencies

There are no external role dependencies. Only `cisco.catalystwan` collection is required.

## Role Variables

Variables expected by this role:

- `vmanage_instances`: List of vManage instances containing management IP, admin username, and admin password.
- `vsmart_instances`: List of vSmart controller instances with hostnames.
- `vbond_instances`: List of vBond controller instances with hostnames.
- `multitenant_domain`: Multi-tenant domain name.

## Example Playbook

Including an example of how to use your role (with variables passed in as parameters):

```yaml
- hosts: all
  gather_facts: no
  tasks:
    - name: Set multi-tenant mode
      import_role:
        name: multitenant_mode
      vars:
        vmanage_instances:
          - mgmt_public_ip: '192.0.2.1'
            admin_username: 'admin'
            admin_password: 'password'
            multitenant_domain: "MyDomainName"
```

## Known Limitations


## License

"GPL-3.0-only"

## Author Information

This role was created by Piotr Piwowarski <pipiwowa@cisco.com>
