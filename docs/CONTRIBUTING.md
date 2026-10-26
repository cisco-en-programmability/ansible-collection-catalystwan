# How to contribute

Thank you for investing your time in contributing to our project!

First, we recommended reading these if you are not familair with developing modules/collections yet:

[Developing Modules General](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)

[Developing Modules Best Practices](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html)

[Ansible module architecture](https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html)

---

## Issues

### Solve an issue

See [existing issues](https://github.com/cisco-en-programmability/ansible-collection-catalystwan/issues) and feel free to work on any.

### Create a new issue

Firstly [search if an issue already exists](https://github.com/cisco-en-programmability/ansible-collection-catalystwan/issues).

If issue related to your problem/feature request doesn't exist, create new issue.
There are 3 issue types:

- Bug report
- Feature Request
- Report a security vulnerability

Select one from [issue form](https://github.com/cisco-en-programmability/ansible-collection-catalystwan/issues/new/choose).

### Create PR

When you're finished with the changes, create a pull request, also known as a PR.

---

## Development

The full collection uses `catalystwan==0.41.5.dev2`; see the
[SDK compatibility policy](COMPATIBILITY.md) before changing that version.

Preferred way to setup environment for development:

1. Use `poetry install` and `poetry env activate` to set up the SDK/test environment
2. Install local collection with `ansible-galaxy collection install . --force`
3. Adjust configuration of variables in ``.dev_dir/dev_vars.yml``
4. Run playground playbook with `ansible-playbook .dev_dir/playground.yml` or any other playbook used for tests

You can also refer to [Ansible modules dev guide](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#verifying-your-module-code) to look for more convenient way of
testing your code.

### Separate SDK and lint environments

The SDK requires `packaging<24`. Security-fixed `virtualenv` requires
`packaging>=26.3`, so install pre-commit and the lint tools in a separate
environment. Installing both requirement files into one environment is unsupported.
For example, using Python 3.14:

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q tests/unit

python3.14 -m venv .venv-lint
.venv-lint/bin/python -m pip install -r requirements-lint.txt
.venv-lint/bin/pre-commit run --all-files
```

`requirements.txt` and Poetry define the SDK/runtime stack; `requirements-dev.txt`
adds unit tests. `requirements-lint.txt` defines the isolated lint stack, which CI
also uses. `requirements-security.txt` supplies the fixed dependency minimums for
pip installs and the SDK compatibility matrix; keep these minimums in sync with
`pyproject.toml` when updating dependencies. Collection installation through Galaxy
does not install Python requirements: install `requirements.txt` in the runtime
environment as described in the README.

---

## Release process

According to [release workflow inside .github workflows](https://github.com/cisco-en-programmability/ansible-collection-catalystwan/blob/main/.github/workflows/release-from-tag.yml) collection publication to Ansible Galaxy will happen when admin of the repository will push new tag.
This tag must much version used in [galaxy.yml](../galaxy.yml) file.
Release will happen only if desired version was not published on Ansible Galaxy yet.
