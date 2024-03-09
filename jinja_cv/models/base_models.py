
from typing_extensions import Annotated

from datetime import datetime

from dataclasses import dataclass

import typing as t

from pydantic import (
    BaseModel,
    ValidationError,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    ConfigDict,
)

from pydantic.functional_validators import WrapValidator
from pydantic.alias_generators import to_snake, to_camel

def validate_datetime(
        v: t.Any,
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo
    ) -> datetime:
    
    if info.mode == 'json':
        assert isinstance(v, str), 'In JSON mode the input must be a string!'
        try:
            return handler(datetime.strptime(v,'%Y-%m-%d').date())
        except ValidationError as e:
            raise e
    
    if info.mode == 'python':
        if isinstance(v, str):
            return handler(datetime.strptime(v,'%Y-%m-%d').date())
        assert isinstance(v, datetime), 'In JSON mode the input must be a datetime!'
    
    return v

class CVBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, 
        arbitrary_types_allowed=True)

CustomDateTime = Annotated[
    datetime, 
    WrapValidator(validate_datetime)]

T= t.TypeVar('T')
class JsonObject():
    @classmethod   
    def from_object(cls: t.Type[T], reference: dict|list) -> T:
        instance = JsonObject()
        
        def generate_items(reference):
            while True:
                if isinstance(reference, list):
                    return [generate_items(value) for value in reference]
                    continue
                if isinstance(reference, dict):
                    return dict([(to_snake(key), generate_items(value))
                           for key, value in reference.items()])
                    continue
                return reference
            
        return generate_items(reference)

class ITimeSpanElement():
    date_debut: CustomDateTime
    date_fin: CustomDateTime

class IOptionalTimeSpanElement(CVBaseModel):
    date_debut: t.Optional[CustomDateTime] = None
    date_fin: t.Optional[CustomDateTime] = None


class Realisation():
    description: str
    realisations: t.Optional[list['Realisation']]


class BaseExperience(ITimeSpanElement):
    intitule: str
    domaine: str
    
class ExperienceGroup(BaseExperience):
    pass

@dataclass
class Experience(BaseExperience):
    client: t.Optional[str]
    domaines: list[str]
    presentation: str
    details_memory: t.Optional[str]
    references: t.Optional[str]
    environnement_technique: str
    intitule: t.Optional[str]
    realisations: list[Realisation]
    
class JExperienceList(list[Experience], JsonObject):
    pass

class JExperience(Experience, JsonObject):
    pass

class VExperience(CVBaseModel, Experience):
    pass

