from typing import Any, Optional

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    retcode: int = 0
    message: Optional[str] = None
    data: Any = None

    def __int__(self, retcode=0, message="ok", data=None):
        self.retcode = retcode
        self.message = message
        self.data = data

    def ok(self, data: Any = None):
        # retcode 0 表示 ok
        self.retcode = 0
        self.message = "ok"
        self.data = data
        return self

    def error(self, message: str = "error"):
        # retcode -1 表示error
        self.retcode = 1
        self.message = message
        return self
