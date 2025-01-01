from typing import Optional, Dict

from pydantic import BaseModel


class PluginInfo(BaseModel):
    id: Optional[int] = None
    name: str
    ordered: bool


class GetPluginsPicInfoSchema(BaseModel):
    plugins_info: Dict[int, PluginInfo]


class GetPluginDetailInfoSchema(BaseModel):
    id: Optional[int] = None
    name: str
    help: str
