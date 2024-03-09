import subprocess
import logging
import sys

import subprocess
import asyncio

from dataclasses import dataclass

logger = logging.getLogger()

def systemWithLogsToOutput(**args) -> subprocess.Popen : 
    try:
        result = subprocess.Popen(**args)
        logger.debug(f'{type(result)} :  {result}')
    except subprocess.CalledProcessError as err:
        logger.error(f'ERROR : {err} => {err.output}')
        raise(Exception(f'{err.output}'))
    
    return result
