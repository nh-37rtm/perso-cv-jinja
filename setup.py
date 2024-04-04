from setuptools import setup

setup(
   name="jinja-cv",
   requires=[ "jsonschema", "python-dateutil", "jinja2"],
   version='0.1.0',
   description='CV templating engine',
   extras_require = {
       'dev': ['pylint', 'pytest'],
   },
)