# Ansible Role: policies

This Ansible role provides user with a few, ready to use, legacy policies scenarios. It handles creating legacy policies along will all required policies definitions and lists.

## Role Description

The `policies` role performs the following tasks:

1. Create legacy policies based on user provided configuration. Supported scenarios:
  - hub and spoke topology
  - mesh topology
  - application route policy
  - acl policy
  - geolocation blockade

## Requirements

- `cisco.catalystwan` collection installed.
- Access details for the Cisco Manager instance must be provided.

## Dependencies

There are no external role dependencies. Only `cisco.catalystwan` collection is required.

## Role Variables

Variables expected by this role:

- `vmanage_instances`: A list of vManage instances containing management IP, admin username, and admin password.
- `policies`: A dictionary containing configuration of policies

Example of `vmanage_instances`:

```yaml
vmanage_instances:
  - hostname: 'vmanage01'
    system_ip: '192.0.2.10'
    mgmt_public_ip: '198.51.100.10'
    admin_username: 'admin'
    admin_password: 'password'
```

Example of `policies`:
```yaml
policies:
  mesh:
    - name: my_mesh_policy
      vpns:
        - 100
        - 101
      regions:
        - name: mesh_region1
          sites:
            - 100
        - name: mesh_region2
          sites:
            - 101
  app_route:
    - name: my_app_counter
      match:
        source_ip: 10.0.0.0/24
        destination_port: 64534
      action:
        counter: my_counter
```

## License

"GPL-3.0-only"

## Author Information

This role was created by Piotr Piwowarski <pipiwowa@cisco.com>
