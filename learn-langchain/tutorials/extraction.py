from .. import lang_smith_config
from typing import Optional
from pydantic import BaseModel,Field

class Person(BaseModel):
    name: Optional[str] = Field(default=None,description="姓名")
    age: Optional[int] = Field(default=None,description="年龄")
    work: Optional[str] = Field(default=None,description="工作")
    address: Optional[str] = Field(default=None,description="住址")
    phone: Optional[str] = Field(default=None,description="电话")
    nickName: Optional[str] = Field(default=None,description="昵称")

