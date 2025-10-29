from nnlogging.shell import Shell
from nnlogging.utils import RunConfig


def test_update_metadata(root_path, run_metadata_label, run_metadata):
    shell = Shell(run_config=RunConfig(repo=str(root_path)))
    shell.update_metadata(run_metadata_label, run_metadata)
    assert shell.run is not None
    assert shell.run.get(run_metadata_label) == run_metadata


def test_add_remove_tag(root_path, run_tag):
    shell = Shell(run_config=RunConfig(repo=str(root_path)))
    shell.add_tag(run_tag)
    assert shell.run is not None
    assert run_tag in shell.run.props.tags
    shell.remove_tag(run_tag)
    assert run_tag not in shell.run.props.tags


# TODO: add `track` test
def test_track(): ...
