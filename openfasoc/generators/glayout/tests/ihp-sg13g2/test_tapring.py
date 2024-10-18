from glayout.flow.primitives.guardring import tapring
from glayout.flow.pdk.sg13g2_mapped import sg13g2_mapped_pdk

from pathlib import Path


sg13g2_mapped_pdk.activate()

module = "test_tapring"
module_path = Path(module)
module_gds = module_path / f"{module}.gds"

params = {
    "pdk": sg13g2_mapped_pdk,
}

# comp = tapring(**params)
# comp = tapring(enclosed_rectangle=(10, 10), **params)
# comp = tapring(sdlayer="n+s/d", **params)
comp = tapring(sdlayer="n+s/d", enclosed_rectangle=(10, 10), **params)

comp.name = module
comp.show()

module_path.mkdir(parents=True, exist_ok=True)
module_gds.unlink(missing_ok=True)
comp.write_gds(module_gds)
