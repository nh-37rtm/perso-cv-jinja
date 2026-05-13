from jinja_cv.models.base_models import JsonObject
from jinja_cv.models.base_models import CVBaseModel as PydanticBaseModel

from dataclasses import dataclass

from pydantic.alias_generators import to_snake, to_camel

import typing as t

@dataclass(init=False)
class IHarHttpHeader():
    name: str
    value: str    

@dataclass(init=False)
class IHarFileRequest():
    method: str
    url: str
    headers: t.List[IHarHttpHeader]
    postData: dict

@dataclass
class IHarFileResponse:
    pass

@dataclass
class IHarFileEntry:
    request: IHarFileRequest
    response: IHarFileResponse

@dataclass
class IHarFileStructure:
    log: IHarFileEntry
    

class HarHttpHeaderPydanticModel(IHarHttpHeader, PydanticBaseModel):
    pass
class HarFileRequestPydanticModel(IHarFileRequest, PydanticBaseModel):
    headers: t.List[HarHttpHeaderPydanticModel]
    pass
    
    