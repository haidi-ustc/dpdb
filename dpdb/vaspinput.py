#/usr/bin/env python
# coding: utf-8
# Copyright (c) PThe Dpmodeling Team.


import os
from monty.io import zopen
from monty.os.path import zpath
from monty.json import MontyDecoder
from monty.json import MSONable

"""
Classes for reading/manipulating/writing VASP input files. All major VASP input
files.
"""

__author__ = "Shyue Ping Ong, Geoffroy Hautier, Rickard Armiento, " + \
             "Vincent L Chevrier, Stephen Dacek"
__copyright__ = "Copyright 2011, The Materials Project"
__version__ = "1.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__status__ = "Production"
__date__ = "Jul 16, 2012"


logger = logging.getLogger(__name__)



class VaspInput(dict, MSONable):
    """
    Class to contain a set of vasp input objects corresponding to a run.

    Args:
        incar: Incar object.
        kpoints: Kpoints object.
        poscar: Poscar object.
        potcar: Potcar object.
        optional_files: Other input files supplied as a dict of {
            filename: object}. The object should follow standard pymatgen
            conventions in implementing a as_dict() and from_dict method.
    """

    def __init__(self, incar, kpoints, poscar, potcar=None, optional_files=None,
                 **kwargs):
        super().__init__(**kwargs)
        self._potcar=True if potcar else False
        if self._potcar:
           self.update({'INCAR': incar,
                        'KPOINTS': kpoints,
                        'POSCAR': poscar,
                        'POTCAR': potcar})
        else:
           self.update({'INCAR': incar,
                        'KPOINTS': kpoints,
                        'POSCAR': poscar})
           
        if optional_files is not None:
            self.update(optional_files)

    def __str__(self):
        output = []
        for k, v in self.items():
            output.append(k)
            output.append(str(v))
            output.append("")
        return "\n".join(output)

    def as_dict(self):
        d = {k: v.as_dict() for k, v in self.items()}
        d["@module"] = self.__class__.__module__
        d["@class"] = self.__class__.__name__
        return d

    @classmethod
    def from_dict(cls, d):
        dec = MontyDecoder()
        sub_d = {"optional_files": {}}
        potcar=d.get('POTCAR',False) 
        if potcar:
           infiles=["INCAR", "POSCAR", "POTCAR", "KPOINTS"]
        else:
           infiles=["INCAR", "POSCAR", "KPOINTS"] 
        for k, v in d.items():
            if k in infiles:
                sub_d[k.lower()] = dec.process_decoded(v)
            elif k not in ["@module", "@class"]:
                sub_d["optional_files"][k] = dec.process_decoded(v)
        return cls(**sub_d)

    def write_input(self, output_dir=".", make_dir_if_not_present=True):
        """
        Write VASP input to a directory.

        Args:
            output_dir (str): Directory to write to. Defaults to current
                directory (".").
            make_dir_if_not_present (bool): Create the directory if not
                present. Defaults to True.
        """
        if make_dir_if_not_present and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for k, v in self.items():
            with zopen(os.path.join(output_dir, k), "wt") as f:
                f.write(v.__str__())

    @staticmethod
    def from_directory(input_dir, optional_files=None):
        """
        Read in a set of VASP input from a directory. Note that only the
        standard INCAR, POSCAR, POTCAR and KPOINTS files are read unless
        optional_filenames is specified.

        Args:
            input_dir (str): Directory to read VASP input from.
            optional_files (dict): Optional files to read in as well as a
                dict of {filename: Object type}. Object type must have a
                static method from_file.
        """
        sub_d = {}
        for fname, ftype in [("INCAR", Incar), ("KPOINTS", Kpoints),
                             ("POSCAR", Poscar), ("POTCAR", Potcar)]:
            fullzpath = zpath(os.path.join(input_dir, fname))
            sub_d[fname.lower()] = ftype.from_file(fullzpath)
        sub_d["optional_files"] = {}
        if optional_files is not None:
            for fname, ftype in optional_files.items():
                sub_d["optional_files"][fname] = \
                    ftype.from_file(os.path.join(input_dir, fname))
        return VaspInput(**sub_d)

