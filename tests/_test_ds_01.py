

from dataclasses import dataclass, fields
from typing import get_type_hints

import inspect

import dataclasses

def add_init_annotations(cls):
    # Get the fields of the dataclass
    dataclass_fields = fields(cls)

    # Create a dictionary of field names and their types
    annotations = {field.name: field.type for field in dataclass_fields}

    # Add the annotations to the __init__ method
    if "__init__" in cls.__dict__:
        cls.__init__.__annotations__ = annotations

    return cls

@add_init_annotations
@dataclass
class Person:
    name: str
    age: int
    is_student: bool = False

    def __init__(self, **kwargs):
        for field in fields(self):
            if field.name in kwargs:
                setattr(self, field.name, kwargs[field.name])
            elif field.default is not dataclasses.MISSING:
                setattr(self, field.name, field.default)
            elif field.default_factory is not dataclasses.MISSING:
                setattr(self, field.name, field.default_factory())
            else:
                raise TypeError(f"Missing required argument: {field.name}")

        # Custom initialization logic
        if self.age < 0:
            raise ValueError("Age cannot be negative")
        
        
# Inspect the __init__ method's signature
init_signature = inspect.signature(Person.__init__)
print(init_signature)


print('dfsdfdsfds')