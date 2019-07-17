#/usr/bin/env python
# coding: utf-8
# Copyright (c) The Dpmodeling Team.

import json
import warnings
from monty.json import MontyEncoder, MontyDecoder
from pymatgen.core.composition import Composition
from pymatgen.io.vasp import VaspInput
from monty.json import MSONable
from dpdata import System,LabeledSystem

"""
This module implements equivalents of the basic Entry objects, which
is the basic entity that can be used to perform many analyses. Entries
contain calculated information, typically from VASP or other electronic
structure codes. For example, Entries can be used as inputs for DeepMD-Kit.
"""

__author__ = "Han Wang"
__copyright__ = "Copyright 2019, The Dpmodeling Team"
__version__ = "0.1"
__maintainer__ = "Haidi Wang"
__status__ = "develop"
__date__ = "Jul 11, 2019"


class Entry(MSONable):
    """
    An lightweight Entry object containing key computed data
    for storing purpose. 

    """

    def __init__(self, composition, calculator, inputs,
                 data, entry_id=None, attribute=None, tag=None):
        """
        Initializes a Entry.

        Args:
            composition (Composition): Composition of the entry. For
                flexibility, this can take the form of all the typical input
                taken by a Composition, including a {symbol: amt} dict,
                a string formula, and others.
            inputs (dict): An dict of parameters associated with
                the entry. Defaults to None.
            data (dict): An dict of any additional data associated
                with the entry. Defaults to None.
            entry_id (obj): An optional id to uniquely identify the entry.
            attribute: Optional attribute of the entry. This can be used to
                specify that the entry is a newly found compound, or to specify
                a particular label for the entry, or else ... Used for further
                analysis and plotting purposes. An attribute can be anything
                but must be MSONable.
        """
        self.composition = Composition(composition)
        self.calculator  = calculator
        self.inputs = inputs
        self.data = data 
        self.entry_id = entry_id if entry_id else None
        self.name = self.composition.reduced_formula
        self.attribute = attribute
        self.tag = tag

    @property
    def number_element(self):
        return len(self.composition)

    def __repr__(self):
        output = ["Entry {} - {}".format(self.entry_id, self.composition.formula),
                  "calculator: {}".format(self.calculator) 
                  ]
        return "\n".join(output)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_dict(cls, d):
        dec = MontyDecoder()
        return cls(d["composition"], d["calculator"], 
                   inputs={k: dec.process_decoded(v)
                               for k, v in d.get("inputs", {}).items()},
                   data={k: dec.process_decoded(v)
                         for k, v in d.get("data", {}).items()},
                   entry_id=d.get("entry_id", None),
                   attribute=d["attribute"] if "attribute" in d else None,
                   tag=d["tag"] if "tag" in d else None
                   )
    @classmethod
    def load(cls,filename,Cls=None):
        with open(filename,'r') as f:
             fc=f.read()
        jc=json.loads(fc) 
        composition=jc['composition'] 
        calculator = jc['calculator']
        if calculator.lower() == 'vasp':
           try:
              inputs=VaspInput.from_dict(jc['inputs']).as_dict()
           except:
              inputs=jc['inputs']
              warnings.warn ("""Inproperly configure of POTCAR !
                                Returned instance cannot be used 
                                as input for from_dict() method """)
        else:
           if Cls:
              inputs=Cls.from_dict(jc['inputs']).as_dict()
           else:
              raise RuntimeError("inputs decoder must be given")
        data=LabeledSystem.from_dict(jc['data']).as_dict() 
        attribute=jc['attribute']
        entry_id=jc['entry_id']
        tag=jc['tag']
        return cls(composition,calculator,inputs,data,entry_id,attribute,tag)


    def as_dict(self):
        return {"@module": self.__class__.__module__,
                "@class": self.__class__.__name__,
                "composition": self.composition.as_dict(),
                "calculator": self.calculator,
                "inputs": json.loads(json.dumps(self.inputs,
                                                    cls=MontyEncoder)),
                "data": json.loads(json.dumps(self.data, cls=MontyEncoder)),
                "entry_id": self.entry_id,
                "attribute": self.attribute,
                "tag": self.tag}
def test():
    from monty.serialization import dumpfn,loadfn
    from monty.json import MontyDecoder,MontyEncoder 
    from pymatgen.io.vasp.inputs import PotcarSingle,Potcar
    vi=VaspInput.from_directory('.')
    ls=LabeledSystem('OUTCAR',fmt='vasp/outcar')
    en0=Entry('Al','vasp',inputs=vi.as_dict(),data=ls.as_dict(),entry_id='pku-1')
    print(en0)
    fname='pku-1.json'
    dumpfn(en0.as_dict(),fname,indent=4)
    en1=Entry.load(fname)
    #vin=VaspInput.from_dict(en1.inputs)
    #vin.write_input('./new')
    print(en1)
    print(en1.as_dict())

if __name__=="__main__":
   test()
