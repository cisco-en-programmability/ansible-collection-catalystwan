from types import SimpleNamespace

from plugins.modules.software_upgrade import _all_devices_are_managers


def test_all_devices_are_managers_accepts_manager_only_selection():
    devices = [SimpleNamespace(personality="vmanage"), SimpleNamespace(personality="vmanage")]

    assert _all_devices_are_managers(devices)


def test_all_devices_are_managers_rejects_mixed_selection():
    devices = [SimpleNamespace(personality="vmanage"), SimpleNamespace(personality="vedge")]

    assert not _all_devices_are_managers(devices)


def test_all_devices_are_managers_rejects_edge_only_selection():
    devices = [SimpleNamespace(personality="vedge")]

    assert not _all_devices_are_managers(devices)
