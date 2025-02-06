# Ansible Role: manager_version

This Ansible role is checks if Manager version matches requirements.

## Role Description

The `manager_version` role performs the following tasks:

1. Get software version from Manager.
2. Verify if version matches requirements.

## Requirements

- `cisco.catalystwan` collection installed.
- Access details for the Cisco Manager instance must be provided.

## Dependencies

There are no external role dependencies. Only `cisco.catalystwan` collection is required.

## Role Variables

Variables expected by this role:

- `manager_instances`: List of Manager instances containing management IP, admin username, admin password and system IP.
- `min_version_required`: A string representing minimum version of Manager this role expects to succeed.

## Example Playbook

Including an example of how to use your role (with variables passed in as parameters):

```yaml
- hosts: all
  gather_facts: no
  tasks:
    - name: Check if Manager version is equal or greater to 20.13.1
      import_role:
        name: manager_mode
      vars:
        manager_instances:
          - mgmt_public_ip: '192.0.2.1'
            admin_username: 'admin'
            admin_password: 'password'
            system_ip: '192.168.101.1'
        min_version_required: "20.13.1"
```

## License

"GPL-3.0-only"

## Author Information

This role was created by Przemyslaw Susko <sprzemys@cisco.com>
