from __future__ import division
import warnings
import sys
sys.path.append('')
import unittest
import pymatgen
from pymatgen.io.vaspio import Poscar
from pymatgen.io.vaspio import Vasprun
from pymatgen.io.cifio import CifWriter
from pymatgen.io.cifio import CifParser
from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import Structure
from pymatgen.transformations.standard_transformations import *
from pymatgen.core.structure_modifier import StructureEditor
import numpy as np
from pymatgen.phonons.strain import Strain
from pymatgen.phonons.strain import IndependentStrain

__author__="Maarten de Jong"
__copyright__ = "Copyright 2012, The Materials Project"
__credits__ = "Mark Asta"
__version__ = "1.0"
__maintainer__ = "Maarten de Jong"
__email__ = "maartendft@gmail.com"
__status__ = "Development"
__date__ ="Jan 24, 2012"

def DeformGeometry(rlxd_str, nd=0.01, ns=0.01, m=4, n=4):
        
    msteps = np.int(m)
    nsteps = np.int(n)

    if m%2!=0:
        raise ValueError("m has to be even.")
         
    if n%2!=0:
        raise ValueError("n has to be even.")
        
    mystrains = np.zeros((3, 3, np.int(m*3) + np.int(n*3)))
        
    defs = np.linspace(-nd, nd, num=m+1)
    defs = np.delete(defs, np.int(m/2), 0)
    sheardef = np.linspace(-ns, ns, num=n+1)
    sheardef = np.delete(sheardef, np.int(n/2), 0)
    defstructures = {}

    strcopy = rlxd_str.copy()

#    print rlxd_str.lattice
    # First apply normal deformations
    for i1 in range(0, 3):

        for i2 in range(0, len(defs)):

#            s = StructureEditor(rlxd_str)
#            print s.original_structure.lattice
            s=rlxd_str.copy()
            F = np.identity(3)
            F[i1, i1] = F[i1, i1] + defs[i2] 
            StrainObject = IndependentStrain(F)
#            print F
#            s.apply_strain_transformation(F)
#            print "old"
#            print s.lattice
            s.apply_strain_transformation(F)
#            print "new"
#            print s.lattice
            defstructures[StrainObject] = s



    # Now apply shear deformations #		
    F_index = [[0, 1], [0, 2], [1, 2]]
    for j1 in range(0, 3):
		
        for j2 in range(0, len(sheardef)):

#            s = StructureEditor(rlxd_str)
            s=rlxd_str.copy()
            F = np.identity(3)
            F[F_index[j1][0], F_index[j1][1]] = F[F_index[j1][0], F_index[j1][1]] + sheardef[j2]
#           F = np.matrix(F)   # this needs to be checked carefully, might give problems in certain cases
            StrainObject = IndependentStrain(F)
#            s.apply_strain_transformation(F)
            s.apply_strain_transformation(F)
            defstructures[StrainObject] = s

    return defstructures

if __name__ == "__main__":

    struct = CifParser('aluminum.cif').get_structures(primitive=False)[0]
#    print struct
    D = DeformGeometry(struct)
    print D
#    print D

