import importlib
from pathlib import Path

from catalystwan.version import parse_api_version


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_all_collection_modules_import_with_installed_sdk():
    module_paths = sorted((REPOSITORY_ROOT / "plugins" / "modules").glob("*.py"))

    for module_path in module_paths:
        if module_path.name == "__init__.py":
            continue
        importlib.import_module(f"plugins.modules.{module_path.stem}")


def test_current_manager_release_version_is_parsed():
    assert str(parse_api_version("26.1.1")) == "26.1"
    assert str(parse_api_version("26.1.2-123")) == "26.1"


def test_result_models_do_not_share_mutable_defaults():
    from plugins.module_utils.result import ModuleResult

    first = ModuleResult()
    second = ModuleResult()
    first.response["changed"] = True

    assert second.response == {}
