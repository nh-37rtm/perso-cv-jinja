import typing as t
from pytest import fixture

import logging

@fixture(name="logger")
def fix0() -> logging.Logger:
    return  logging.getLogger()

def test_controller1(logger : logging.Logger):
    
    logging.info('test')
    