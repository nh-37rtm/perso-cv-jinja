import dataclasses
import inspect
import typing as t

import pydantic_core
from pydantic import (
    BaseModel,
    Field,
    ModelWrapValidatorHandler,
    ValidationError,
    model_validator,
    ValidatorFunctionWrapHandler,
)
from pydantic_core import from_json


def add_init_annotations(cls):
    # Get the fields of the dataclass
    dataclass_fields = dataclasses.fields(cls)

    # Create a dictionary of field names and their types
    annotations = {field.name: field.type for field in dataclass_fields}

    # Add the annotations to the __init__ method
    if "__init__" in cls.__dict__:
        if len(annotations) > 0:
            cls.__init__.__annotations__ = annotations
        else:
            cls.__init__.__annotations__ = cls.__annotations__

    print(f"annotations :{annotations}")
    print(f"dataclasse fields: {dataclass_fields}")
    print(f"cls.__init__.__annotations__ :{cls.__init__.__annotations__}")
    print(f"cls :{cls.__annotations__}")

    return cls


@t.dataclass_transform()
class IDefault:
    def __init__(self, **kwargs):
        for field in dataclasses.fields(self):
            if field.name in kwargs:
                setattr(self, field.name, kwargs[field.name])
            elif field.default is not dataclasses.MISSING:
                setattr(self, field.name, field.default)
            elif field.default_factory is not dataclasses.MISSING:
                setattr(self, field.name, field.default_factory())
            else:
                raise TypeError(f"Missing required argument: {field.name}")


class IPerson:
    name: str = ""
    age: int = 0
    is_student: bool = False


@dataclasses.dataclass(init=False)
class DPerson(IPerson, IDefault):
    pass


class DefaultBaseModel(BaseModel):
    """ BaseModel override

    Args:
        BaseModel (_type_): _description_

    Raises:
        pydantic_core.PydanticUseDefault: _description_

    Returns:
        _type_: _description_
    """
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
                raise pydantic_core.PydanticUseDefault()
            else:
                raise


class PPerson(IPerson, DefaultBaseModel):
    is_student: bool = Field(
        alias="IsStudent", default=False
    )  # Optional field with default value


class User(BaseModel):
    id: int
    name: str
    email: str


# Partial JSON data
partial_json = {"id": 1, "name": "Alice"}

partial_data = """{
    "name": "John Doe",
    "IsStudent": "True"
}"""


def test_partial_json_pydantyc_load():

    person = t.cast(IPerson, PPerson.model_validate(from_json(partial_data)))

    print(f"{person.name}")

    print(f"person : {p}")
    # Parse partial data (allow missing fields)
    # person = Person.model_validate(partial_data, strict=False, )

    # Access fields
    # print(person.name)  # Output: John Doe
    # print(person.age)   # Output: Raises AttributeError (field not yet validated)
    # print(person.is_student)  # Output: False (default value)

    # try:
    #     user = User.model_validate(partial_json, strict=False)
    #     print(user)
    # except ValidationError as e:
    #     print(e)
    pass


@dataclasses.dataclass()
class TestClass:
    a: str
    b: int


def test_dataclass():

    # Inspect the __init__ method's signature

    person = IPerson(name="test")

    print(f"fields: {dataclasses.fields(TestClass)}")

    TestClass.__init__.__annotations__ = dict()

    th = t.get_type_hints(TestClass.__init__)
    th = t.get_type_hints(TestClass)

    init_signature = inspect.signature(TestClass.__init__)
    print(init_signature)
