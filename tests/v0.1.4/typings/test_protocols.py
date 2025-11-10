from io import StringIO

from rich.console import Console

from nnlogging.typings.protocols import TerminalWritable, Writable


def test_constructed_sink_fits_sinktype(constructed_sink):
    assert isinstance(constructed_sink, Writable)
    assert not ("Terminal" in type(constructed_sink).__name__) ^ isinstance(
        constructed_sink, TerminalWritable
    )
    assert hasattr(constructed_sink, "closed") and not constructed_sink.closed


def test_console_print(
    stringio_sink,
    force_terminal,
    message_gen,
):
    console = Console(
        force_terminal=force_terminal,
        file=stringio_sink,
        width=1024,
    )
    msg = message_gen()
    console.print(msg)
    assert isinstance(stringio_sink.target, StringIO)
    assert msg in stringio_sink.target.getvalue()


def test_console_log(
    stringio_sink,
    force_terminal,
    message_gen,
):
    console = Console(
        force_terminal=force_terminal,
        file=stringio_sink,
        width=1024,
    )
    msg = message_gen()
    console.log(msg)
    assert isinstance(stringio_sink.target, StringIO)
    assert msg in stringio_sink.target.getvalue()


def test_console_capture(
    stringio_sink,
    force_terminal,
    message_gen,
):
    console = Console(
        force_terminal=force_terminal,
        file=stringio_sink,
        width=1024,
    )
    msg = message_gen()
    with console.capture() as capture:
        console.print(msg)
    assert msg in capture.get()
