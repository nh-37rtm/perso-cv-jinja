import typing as t

from pydantic import (BaseModel, ConfigDict, ModelWrapValidatorHandler,
                      ValidationError, model_validator)
from pydantic_core import PydanticUseDefault

from jinja_cv.models.har_models import IHarFileRequest
from pydantic.alias_generators import to_camel, to_snake


class DefaultBaseModel(BaseModel):
    """ BaseModel override

    Args:
        BaseModel (_type_): _description_

    Raises:
        pydantic_core.PydanticUseDefault: _description_

    Returns:
        _type_: _description_
    """

    model_config = ConfigDict(
        alias_generator=to_camel, 
        arbitrary_types_allowed=True,
        extra= "ignore")

    @model_validator(mode="wrap")
    @classmethod
    def default_on_error(
        cls, data: t.Any, handler: ModelWrapValidatorHandler[t.Self]
    ) -> t.Self:
        """
        Raise a PydanticUseDefault exception if the value is missing.

        This is useful for avoiding errors from partial
        JSON preventing successful validation.
        """

        try:
            return handler(data)
        except ValidationError as exc:
            # there might be other types of errors resulting from partial JSON parsing
            # that you allow here, feel free to customize as needed
            if all(e["type"] == "missing" for e in exc.errors()):
                raise PydanticUseDefault() from exc
            else:
                raise



class PydanticHarFileRequest(IHarFileRequest, DefaultBaseModel):
    def __repr__(self):
        return super().__repr__()
    pass