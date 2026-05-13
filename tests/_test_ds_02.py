from dataclasses import dataclass, fields
import dataclasses

class AnnotatedInitMeta(type):
    def __new__(cls, name, bases, dct):
        # Create the class
        new_class = super().__new__(cls, name, bases, dct)

        # Add annotations to the __init__ method
        if "__init__" in dct:
            dataclass_fields = fields(new_class)
            annotations = {field.name: field.type for field in dataclass_fields}
            new_class.__init__.__annotations__ = annotations

        return new_class

@dataclasses.dataclass
class Person(metaclass=AnnotatedInitMeta):
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


        
# Inspect the __init__ method's signature
init_signature = inspect.signature(Person.__init__)
print(init_signature)


print('dfsdfdsfds')