
import typing as t


class IPerson(t.Protocol):  
    name: str
    age: int
    
class Person(IPerson):
    birth_date: str

def test_protocol():
    p = Person()
    
    msg = "toto"
    
    