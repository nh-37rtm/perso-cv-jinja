from setuptools import setup

setup(
   name="jinja-cv",
   requires=[ "jsonschema", "jinja2"],
   version='0.1.0',
   description='CV templating engine',
   py_modules=[],
   extras_require = {
       'dev': ['pylint', 'pytest'],
   },
)