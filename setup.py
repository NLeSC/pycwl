import os
from setuptools import setup
import sys

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def conf_path(name):
  if sys.prefix == '/usr':
    conf_path = os.path.join('/etc', name)
  else:
    conf_path = os.path.join(sys.prefix, 'etc', name)
  return conf_path
setup(
    name = "pycwl",
    version = "0.0.1",
    author = "Netherlands eScience Center ",
    author_email = "cwl@esciencecenter.nl",
    description = ("Library for Common Workflow Language (CWL)"),
    license = "Apache 2.0",
    keywords = "Common Workflow Language, CWL",
    url = "https://github.com/nlesc/pycwl",
    packages=['pycwl'],
    scripts=['pycwl/scripts/pycwl-runner'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved ::Apache Software License",
    ],
)
