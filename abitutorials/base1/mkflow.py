#!/usr/bin/env python
from __future__ import division, print_function, unicode_literals, absolute_import

import sys
import os
import numpy as np
import abipy.abilab as abilab
import abipy.flowtk as flowtk
import abipy.data as abidata


def gs_input(x=0.7, ecut=10, acell=(10, 10, 10)):
    """
    H2 molecule in a big box

    Args:
        x:
        ecut:
        acell

    Returns:
        AbinitInput object.
    """
    # Build structure from dictionary with input variables
    structure = abilab.Structure.from_abivars(
        ntypat=1,                           # There is only one type of atom
        znucl=1,                            # Atomic numbers of the type(s) of atom
        natom=2,                            # There are two atoms
        typat=(1, 1),                       # They both are of type 1, that is, Hydrogen
        xcart=[-x, 0.0, 0.0,                # Cartesian coordinates of atom 1, in Bohr
               +x, 0.0, 0.0],               # second atom.
        acell=acell,                        # Lengths of the primitive vectors (in Bohr)
        rprim=[1, 0, 0, 0, 1, 0, 0, 0, 1]   # Orthogonal primitive vectors (default)
    )

    # Build AbinitInput from structure and pseudo(s) taken from AbiPy package.
    inp = abilab.AbinitInput(structure=structure, pseudos=abidata.pseudos("01h.pspgth"))

    # Set value of other variables.
    inp.set_vars(
        ecut=ecut,
        nband=1,
        diemac=2.0,
        toldfe=1e-6,
        prtwf=-1,
        iomode=3
    )

    # Define k-point sampling.
    inp.set_kmesh(ngkpt=(1, 1, 1), shiftk=(0, 0, 0))

    return inp


def build_flow(options):
    """
    Generate a flow to compute the total energy and forces for the H2 molecule in a big box
    as a function of the interatomic distance.
    """
    workdir = "flow_h2" if options.workdir is None else options.workdir

    inputs = [gs_input(x=x) for x in np.linspace(0.5, 1.025, 21)]

    return flowtk.Flow.from_inputs("flow_h", inputs, remove=options.remove, pickle_protocol=0)


@abilab.flow_main
def main(options):
    flow = build_flow(options)
    flow.build_and_pickle_dump()
    return flow


if __name__ == "__main__":
    sys.exit(main())
