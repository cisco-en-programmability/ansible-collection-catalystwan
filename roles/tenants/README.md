# Ansible Role: tenants

This Ansible role is designed to create tenants in Cisco SD-WAN environment.

## Role Description

The `tenants` role performs the following tasks:

1. Verifies that the required variables for the role are present.
2. Gets list of currently created tenants.
3. Creates missing tenants.

## Requirements

- `cisco.catalystwan` collection installed.
- Access details for the Cisco Manager instance must be provided.

## Dependencies

There are no external role dependencies. Only `cisco.catalystwan` collection is required.

## Role Variables

Variables expected by this role:

- `vmanage_instances`: List of vManage instances containing management IP, admin username, and admin password.
- `tenants`: List of tenants that will be present in system.

## Example Playbook

Including an example of how to use your role (with variables passed in as parameters):

```yaml
- hosts: all
  gather_facts: no
  tasks:
    - name: Create tenants
      import_role:
        name: tenants
      vars:
        vmanage_instances:
          - mgmt_public_ip: '192.0.2.1'
            admin_username: 'admin'
            admin_password: 'password'
        tenants:
          - name: "MyTenant"
            org_name: "my-tenant-org"
            description: "My tenant description"
            subdomain: "tenant.domain"
            wan_edge_forecast: "3"
```

## Known Limitations


## License

"GPL-3.0-only"

## Author Information

This role was created by Piotr Piwowarski <pipiwowa@cisco.com>
