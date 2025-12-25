import logging
from collections.abc import Collection

from nnlogging.options import ConsoleFullOpt, FilterFullOpt, HandlerFullOpt
from nnlogging.typings import Branch, Branches, Sink
from nnlogging.utils import (
    attach_handler_logfilter,
    detach_handler_logfilter,
    get_logfilter,
    get_rconsole,
    get_rhandler,
)


__all__ = ["add_branch", "remove_branch"]


def add_branch(  # noqa: PLR0913, PLR0917
    branches: Branches,
    sinks: Collection[tuple[str, Sink]],
    logger: str | None,
    console_kwargs: ConsoleFullOpt,
    handler_kwargs: HandlerFullOpt,
    filter_kwargs: FilterFullOpt,
) -> None:
    for sn, sv in sinks:
        console = get_rconsole(sv, console_kwargs)
        handler = get_rhandler(console, handler_kwargs)
        fltr = get_logfilter(filter_kwargs.filter)
        attach_handler_logfilter(handler, fltr)
        logging.getLogger(logger).addHandler(handler)
        branches[sn] = Branch(
            logger=logger or "root",
            console=console,
            handler=handler,
            filter=fltr,
            tasks={},
        )


def remove_branch(branches: Branches, names: Collection[str]) -> None:
    for n in names:
        (br := branches[n])["handler"].close()
        logging.getLogger(br["logger"]).removeHandler(br["handler"])
        detach_handler_logfilter(br["handler"], br["filter"])
        if prog := br.get("progress"):
            prog.stop()
        del branches[n]
