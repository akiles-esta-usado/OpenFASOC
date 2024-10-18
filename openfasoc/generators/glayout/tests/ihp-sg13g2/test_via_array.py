from glayout.flow.primitives.via_gen import via_array
from glayout.flow.pdk.sg13g2_mapped import sg13g2_mapped_pdk

from pathlib import Path


sg13g2_mapped_pdk.activate()

module = "test_via_array"
module_path = Path(module)
module_gds = module_path / f"{module}.gds"

params = {
    "pdk": sg13g2_mapped_pdk,
    "glayer2": "met5",
    "size": (10, 10),
    "lay_bottom": True,  # Bottom layer connects all vias
    "lay_every_layer": True,  # All layers connect all vias
    "fullbottom": True,  # Bottom layer takes complete size
}

# comp = via_array(glayer1="poly", **params)
# comp = via_array(glayer1="active_diff", **params)
comp = via_array(glayer1="active_tap", **params)

comp.name = module
comp.show()

module_path.mkdir(parents=True, exist_ok=True)
module_gds.unlink(missing_ok=True)
comp.write_gds(module_gds)
