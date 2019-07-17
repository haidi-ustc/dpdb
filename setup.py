#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from  dpdb import NAME,SHORT_CMD
import setuptools

readme_file = path.join(path.dirname(path.abspath(__file__)), 'README.md')
try:
    from m2r import parse_from_file
    readme = parse_from_file(readme_file)
except ImportError:
    with open(readme_file) as f:
        readme = f.read()

install_requires=['numpy>=1.14.3,<1.17', 'dpdata>=0.1.0', 'pymatgen', 'elasticsearch', 'monty','elasticsearch_dsl']

setuptools.setup(
    name=NAME,
    version_format='{tag}.dev{commitcount}+{gitsha}',
    version="0.1.0",
    author="Haidi Wang",
    author_email="haidi@hfut.edu.cn",
    description="Manipulating, storing and querying DeePMD-kit related data",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/deepmodeling/dpdb",
    packages=['dpdb', 
    ],
    # package_data={'example':['*.json']},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    ],
    keywords='deepmd elasticsearch json',
    install_requires=install_requires,    
       # entry_points={
       #   'console_scripts': [
       #       SHORT_CMD+'= dpgen.main:main']
   }
)

