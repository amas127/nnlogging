from io import StringIO
from sys import stderr, stdout
from typing import TextIO

import pytest


class WritableSink:
    def __init__(self, target: TextIO):
        self.target: TextIO = target

    def write(self, text: str) -> int:
        return self.target.write(text)

    def flush(self):
        return self.target.flush()

    @property
    def closed(self):
        return self.target.closed


class TerminalWritableSink:
    def __init__(self, target: TextIO):
        self.target: TextIO = target

    def write(self, text: str) -> int:
        return self.target.write(text)

    def flush(self):
        return self.target.flush()

    def isatty(self):
        return True

    @property
    def closed(self):
        return self.target.closed


@pytest.fixture(params=("default", "terminal"))
def constructed_sink_type(request):
    match request.param:
        case "default":
            return WritableSink
        case "terminal":
            return TerminalWritableSink
        case _:
            raise RuntimeError


@pytest.fixture(params=("stringio", "file", "stderr", "stdout"))
def constructed_sink_target(request, file_path_gen):
    match request.param:
        case "stringio":
            f = StringIO()
            recycle = True
        case "file":
            f = file_path_gen().open("a")
            recycle = True
        case "stderr":
            f = stderr
            recycle = False
        case "stdout":
            f = stdout
            recycle = False
        case _:
            raise RuntimeError
    try:
        yield f
    finally:
        if recycle:
            f.close()
        assert not recycle ^ f.closed


@pytest.fixture
def constructed_sink(constructed_sink_type, constructed_sink_target):
    f = constructed_sink_type(constructed_sink_target)
    assert isinstance(f, (WritableSink, TerminalWritableSink))
    return f


@pytest.fixture
def stringio_sink(constructed_sink_type):
    f = constructed_sink_type(StringIO())
    assert isinstance(f, (WritableSink, TerminalWritableSink))
    return f


@pytest.fixture(params=(True, False))
def force_terminal(request):
    return request.param
