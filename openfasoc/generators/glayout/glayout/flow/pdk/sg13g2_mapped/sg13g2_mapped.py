"""
usage: from sg13g2_mapped import sg13g2_mapped_pdk
"""

from .grules import grulesobj
from glayout.flow.pdk.mappedpdk import MappedPDK, SetupPDKFiles
from pathlib import Path

from os import environ
from .layers import LAYER

sg13g2_glayer_mapping = {
    "met5": "Metal5.drawing",
    "via4": "Via4.drawing",
    "met4": "Metal4.drawing",
    "via3": "Via3.drawing",
    "met3": "Metal3.drawing",
    "via2": "Via2.drawing",
    "met2": "Metal2.drawing",
    "via1": "Via1.drawing",
    "met1": "Metal1.drawing",
    "mcon": "Cont.drawing",
    "poly": "GatPoly.drawing",
    "active_diff": "Activ.drawing",
    "active_tap": "Activ.drawing",
    "n+s/d": "nSD.drawing",
    "p+s/d": "pSD.drawing",
    "nwell": "NWell.drawing",
    "pwell": "PWell.drawing",
    "dnwell": "TEXT.drawing",
    "capmet": "MIM.drawing",
}

pdk_dir = Path(environ["PDK_ROOT"]) / "ihp-sg13g2"

# TODO: This code should be refactored
pdk_files = SetupPDKFiles(
    lvs_setup_tcl_file="",
    magic_drc_file="",
    pdk_root=environ["PDK_ROOT"],
    klayout_drc_file=pdk_dir / "libs.tech/klayout/tech/lvs/sg13g2_full.lylvs",
    lvs_schematic_ref_file=pdk_dir / "libs.ref/sg13g2_stdcell/cdl/sg13g2_stdcell.cdl",
    temp_dir=None,
    pdk="SG13_dev",
).return_dict_of_files()

sg13g2_mapped_pdk = MappedPDK(
    name="SG13_dev",
    glayers=sg13g2_glayer_mapping,
    models={"nfet": "nmos", "pfet": "pmos", "mimcap": "cmim"},
    layers=LAYER,
    pdk_files=pdk_files,
    grules=grulesobj,
)

# configure the grid size and other settings
# sg13g2_mapped_pdk.gds_write_settings.precision = 0.005e-6
sg13g2_mapped_pdk.cell_decorator_settings.cache = False
