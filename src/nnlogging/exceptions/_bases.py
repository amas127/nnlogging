from __future__ import annotations

from abc import ABC, abstractmethod

from nnlogging.typings import override


class _MsgPromptScopeError(Exception):
    def __init__(self, msg: str = "", prompt: str = "", scope: str = "") -> None:
        msg = msg or getattr(self, "msg", "")
        prompt = prompt or getattr(self, "prompt", "")
        scope = scope or getattr(self, "scope", "")
        prompt = f"[{prompt}] " if prompt else ""
        scope = f" in {scope}" if scope else ""
        Exception.__init__(self, f"{prompt}{msg}{scope}")


class _PostmsgError(_MsgPromptScopeError, ABC):
    @property
    @abstractmethod
    def postmsg(self) -> str: ...

    def __init__(self, msg: str = "", prompt: str = "", scope: str = "") -> None:
        msg = f"{msg} {self.postmsg}" if (self.postmsg or msg) else ""
        super().__init__(msg, prompt, scope)


class _PremsgError(_MsgPromptScopeError, ABC):
    @property
    @abstractmethod
    def premsg(self) -> str: ...

    def __init__(self, msg: str = "", prompt: str = "", scope: str = "") -> None:
        msg = f"{self.premsg} {msg}" if (self.premsg or msg) else ""
        super().__init__(msg, prompt, scope)


class _PromptError(_MsgPromptScopeError, ABC):
    @property
    @abstractmethod
    def prompt(self) -> str: ...

    def __init__(self, msg: str = "", prompt: str = "", scope: str = "") -> None:
        super().__init__(msg, prompt or self.prompt, scope)


class AlreadyExistsError(_PostmsgError):
    @property
    @override
    def postmsg(self) -> str:
        return "already exists"


class NotFoundError(_PostmsgError):
    @property
    @override
    def postmsg(self) -> str:
        return "not found"


class ArchivedError(_PostmsgError):
    @property
    @override
    def postmsg(self) -> str:
        return "is archived"


class NullValueError(_PostmsgError):
    @property
    @override
    def postmsg(self) -> str:
        return "is NULL"


class TaskCtxError(_PromptError):
    @property
    @override
    def prompt(self) -> str:
        return "@Task"


class BranchCtxError(_PromptError):
    @property
    @override
    def prompt(self) -> str:
        return "@Branch"


class LevelCtxError(_PromptError):
    @property
    @override
    def prompt(self) -> str:
        return "@Level"


class StacklevelCtxError(_PromptError):
    @property
    @override
    def prompt(self) -> str:
        return "@Stacklevel"


class RunCtxError(_PromptError):
    @property
    @override
    def prompt(self) -> str:
        return "@Run"


class TrackCtxError(_PromptError):
    @property
    @override
    def prompt(self) -> str:
        return "@Track"


class WeirdError(_PostmsgError):
    @property
    @override
    def postmsg(self) -> str:
        return "is weird"


class OutRangeError(_PostmsgError):
    @property
    @override
    def postmsg(self) -> str:
        return "is out of range"


class CustomTypeError(_PremsgError):
    @property
    @override
    def premsg(self) -> str:
        return "type"


class StepError(_PremsgError):
    @property
    @override
    def premsg(self) -> str:
        return "step"
