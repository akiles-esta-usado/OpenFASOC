from glayout.flow.primitives.fet import nmos
from glayout.flow.pdk.sg13g2_mapped import sg13g2_mapped_pdk

from pathlib import Path


sg13g2_mapped_pdk.activate()

module = "test_nmos"
module_path = Path(module)
module_gds = module_path / f"{module}.gds"

params = {
    "pdk": sg13g2_mapped_pdk,
    "width": 10.0,
    "length": 0.45,
}

# with_tie            Specfies if a bulk tie is required
# with_dummy          tuple(bool,bool) or bool. Specifies dummy on both sides
# with_dnwell         Use dnwell (multi well)
# with_substrate_tap  add substrate tap on the outside perimeter of nmos

# comp = nmos(
#     fingers=1, with_tie=False, with_dnwell=False, with_substrate_tap=False, **params
# )
comp = nmos(
    fingers=1, with_tie=True, with_dnwell=False, with_substrate_tap=False, **params
)  # DRC: 336
# comp = nmos(
#     fingers=1, with_tie=False, with_dnwell=True, with_substrate_tap=False, **params
# ) # Not tested
# comp = nmos(
#     fingers=1, with_tie=False, with_dnwell=False, with_substrate_tap=True, **params
# )  # no rules found between dnwell and active_tap

comp.name = module
comp.show()

module_path.mkdir(parents=True, exist_ok=True)
module_gds.unlink(missing_ok=True)
comp.write_gds(module_gds)
