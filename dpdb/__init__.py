#/usr/bin/env python
# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

from   __future__ import unicode_literals, print_function
import logging
import os

ROOT_PATH=__path__[0]
NAME="dpdb"
SHORT_CMD="dpdb"
dlog = logging.getLogger(__name__)
dlog.setLevel(logging.DEBUG)
dlogf = logging.FileHandler(os.getcwd()+os.sep+SHORT_CMD+'.log')
dlogf_formatter=logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
#dlogf_formatter=logging.Formatter('%(asctime)s - %(name)s - [%(filename)s:%(funcName)s - %(lineno)d ] - %(levelname)s \n %(message)s')
dlogf.setFormatter(dlogf_formatter)
dlog.addHandler(dlogf)

__author__    = "Haidi Wang"
__copyright__ = "Copyright 2019"
__version__   = "0.1.0"
__status__    = "Development"
__date__      = "Jul 16, 2019"




def info():
    """
        Show basic information about """+NAME+""", its location and version.
    """

    print('DeepDB\n-------------\n')
    print('Version: ' + __version__)
    print('Path:    ' + ROOT_PATH)
    print('Date:    ' + __date__)
    print()

