from io import StringIO

from nnlogging.options import BranchConfigOption
from nnlogging.shell import Shell

log_level_map = {
    10: "DEBUG".ljust(8),
    20: "INFO".ljust(8),
    30: "WARNING".ljust(8),
    40: "ERROR".ljust(8),
    50: "CRITICAL".ljust(8),
}


def test_log(
    log_level,
    log_msg,
):
    shell = Shell(branch_config=BranchConfigOption(width=1024))
    shell.logger_configure(level=1)
    sink = StringIO()
    shell.branch_add("default", sink)
    shell.log(log_level, log_msg)
    print(sink.getvalue())
    assert log_msg in sink.getvalue()
    if log_level in log_level_map:
        assert log_level_map[log_level] in sink.getvalue()
    else:
        assert f"Level {log_level}".ljust(8) in sink.getvalue()


def test_log_renderable(renderable):
    shell = Shell(branch_config=BranchConfigOption(width=1024))
    shell.logger_configure(level=1)
    sink1 = StringIO()
    shell.branch_add("sink1", sink1)
    shell.log(30, renderable)
    shows = sink1.getvalue()

    sink2 = StringIO()
    shell.branch_add("sink2", sink2)
    shell.branches["sink2"]["console"].print(renderable)
    console_print = sink2.getvalue()

    assert console_print == "\n".join(shows.split("\n")[1:])


def test_debug(log_msg):
    shell = Shell(branch_config=BranchConfigOption(width=1024))
    shell.logger_configure(level=1)
    sink = StringIO()
    shell.branch_add("default", sink)
    shell.debug(log_msg)
    assert log_msg in sink.getvalue()
    assert log_level_map[10] in sink.getvalue()


def test_info(log_msg):
    shell = Shell(branch_config=BranchConfigOption(width=1024))
    shell.logger_configure(level=1)
    sink = StringIO()
    shell.branch_add("default", sink)
    shell.info(log_msg)
    assert log_msg in sink.getvalue()
    assert log_level_map[20] in sink.getvalue()


def test_warn(log_msg):
    shell = Shell(branch_config=BranchConfigOption(width=1024))
    shell.logger_configure(level=1)
    sink = StringIO()
    shell.branch_add("default", sink)
    shell.warn(log_msg)
    assert log_msg in sink.getvalue()
    assert log_level_map[30] in sink.getvalue()


def test_error(log_msg):
    shell = Shell(branch_config=BranchConfigOption(width=1024))
    shell.logger_configure(level=1)
    sink = StringIO()
    shell.branch_add("default", sink)
    shell.error(log_msg)
    assert log_msg in sink.getvalue()
    assert log_level_map[40] in sink.getvalue()


def test_critical(log_msg):
    shell = Shell(branch_config=BranchConfigOption(width=1024))
    shell.logger_configure(level=1)
    sink = StringIO()
    shell.branch_add("default", sink)
    shell.critical(log_msg)
    assert log_msg in sink.getvalue()
    assert log_level_map[50] in sink.getvalue()


def test_exception_capture(log_msg):
    shell = Shell(branch_config=BranchConfigOption(width=1024))
    shell.logger_configure(level=1)
    sink = StringIO()
    shell.branch_add("default", sink)
    try:
        1 / 0
    except ZeroDivisionError:
        shell.exception(log_msg)
    else:
        raise RuntimeError

    assert log_msg in sink.getvalue()
    assert "ZeroDivisionError" in sink.getvalue()


def test_exception_parse(log_msg):
    shell = Shell(branch_config=BranchConfigOption(width=1024))
    shell.logger_configure(level=1)
    sink = StringIO()
    shell.branch_add("default", sink)
    try:
        dct = dict()
        v = dct["NOTFOUND"]
    except KeyError as e:
        shell.exception(
            log_msg,
            exc_info=e,
        )
    else:
        raise RuntimeError

    assert log_msg in sink.getvalue()
    assert "KeyError" in sink.getvalue()
