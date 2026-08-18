# Compatibility policy

## Current targets

| Layer | Tested target | Validation |
| --- | --- | --- |
| Python | 3.12, 3.13, 3.14 | CI matrix |
| Ansible | 14.3.1 / ansible-core 2.21.3 | Unit, collection build, and `ansible-doc` checks |
| catalystwan SDK | 0.41.5.dev2 | Full module import and SDK contract checks |
| catalystwan SDK | 0.41.6 | Full module import and documentation checks; removed SDK APIs fail with actionable messages |
| Cisco Catalyst SD-WAN Manager | 26.1 | SDK version parsing plus opt-in live smoke playbook |

The collection retains `requires_ansible: >=2.16.6` for existing users, while
the newest automation stack is tested on every change.

## Live Manager validation

Static SDK checks cannot prove that a Manager endpoint behaves identically in a
new software release. Before declaring a new Manager train fully validated, run:

```bash
ansible-playbook playbooks/tests/test_manager_release_compatibility.yml \
  -e @manager_credentials.yml \
  -e target_manager_release=26.1
```

`manager_credentials.yml` must define `manager_authentication` with `url`,
`username`, `password`, and the HTTPS API `port` when it is not 443. The
playbook reads the installed release and checks API readiness without changing
Manager state. If the shell also uses `VMANAGE_PORT` for SSH, pass the HTTPS
port explicitly in `manager_authentication` so the SDK does not inherit the SSH
port.

## SDK compatibility note

The stable catalystwan 0.41.x package removed high-level implementations used
by `cluster_management`, `config_groups`, `device_templates_recovery`, and the
Enterprise Root CA option of `administration_settings`. The collection remains
fully functional with the latest published legacy API artifact,
`catalystwan==0.41.5.dev2`, while also keeping all modules importable with
0.41.6. Operations whose upstream API is absent stop before making a request and
explain which SDK artifact is required.
