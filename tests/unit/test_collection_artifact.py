"""Exercise Galaxy packaging against generated files without reading real logs."""

import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path


def test_collection_artifact_excludes_generated_logs_and_test_output(tmp_path):
    repository = Path(__file__).resolve().parents[2]
    source = tmp_path / "source"
    source.mkdir()
    for name in ("galaxy.yml", "README.md", "LICENSE"):
        if (repository / name).exists():
            shutil.copy2(repository / name, source / name)
    runtime_file = "plugins/modules/server_info.py"
    (source / runtime_file).parent.mkdir(parents=True)
    shutil.copy2(repository / runtime_file, source / runtime_file)
    generated_files = ("ansible.log", "logs/nested.log", "tests/output/generated.json")
    for name in generated_files:
        target = source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("synthetic generated-file marker\n")

    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    executable = str(Path(sys.executable).parent / "ansible-galaxy")
    env = dict(os.environ)
    env.pop("ANSIBLE_CONFIG", None)
    env["ANSIBLE_LOG_PATH"] = str(tmp_path / "validation.log")
    env["ANSIBLE_COLLECTIONS_PATH"] = str(tmp_path / "installed")
    build = subprocess.run(
        [executable, "collection", "build", str(source), "--output-path", str(artifacts)],
        cwd=tmp_path,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=45,
        check=False,
    )
    assert build.returncode == 0, build.stdout
    archives = list(artifacts.glob("cisco-catalystwan-*.tar.gz"))
    assert len(archives) == 1
    with tarfile.open(archives[0]) as archive:
        names = set(archive.getnames())
    assert {"MANIFEST.json", "README.md", runtime_file} <= names
    assert names.isdisjoint(generated_files)

    installed = tmp_path / "installed"
    install = subprocess.run(
        [executable, "collection", "install", str(archives[0]), "--no-deps", "--force", "-p", str(installed)],
        cwd=tmp_path,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=45,
        check=False,
    )
    assert install.returncode == 0, install.stdout
    assert (installed / "ansible_collections/cisco/catalystwan" / runtime_file).is_file()
