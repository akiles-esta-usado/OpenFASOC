from glayout.flow.pdk.mappedpdk import MappedPDK
from gdsfactory import Component
from gdsfactory.components import rectangle

from glayout.flow.pdk.sg13g2_mapped import sg13g2_mapped_pdk

from gdsfactory.cell import cell


from pathlib import Path

from math import sqrt


def get_metalization_via_width(
    pdk: MappedPDK, glayer: str, bottom_via: str = None, top_via: str = None
):
    """
    Estimates the minimum width of a metal or poly used on vias
    """
    width = 0

    if bottom_via:
        bottom_width = pdk.get_grule(bottom_via)["width"]
        bottom_enclosure = pdk.get_grule(glayer, bottom_via)["min_enclosure"]
        width_contender = bottom_width + 2 * bottom_enclosure

        width = width_contender if width_contender > width else width

    if top_via:
        top_width = pdk.get_grule(top_via)["width"]
        top_enclosure = pdk.get_grule(glayer, top_via)["min_enclosure"]
        width_contender = top_width + 2 * top_enclosure

        width = width_contender if width_contender > width else width

    if (
        "min_area" in pdk.get_grule(glayer)
        and pdk.get_grule(glayer)["min_area"] > width**2
    ):
        width = sqrt(pdk.get_grule(glayer)["min_area"])

    return width


def get_via_width(pdk: MappedPDK):
    """
    Returns a dictionary with the widths used by vias and metalization based on
    enclosure and min_area
    """
    width = {
        "mcon": pdk.get_grule("mcon")["width"],
        "via1": pdk.get_grule("via1")["width"],
        "via2": pdk.get_grule("via2")["width"],
        "via3": pdk.get_grule("via3")["width"],
        "via4": pdk.get_grule("via4")["width"],
    }

    width["poly"] = get_metalization_via_width(
        pdk,
        "poly",
        top_via="mcon",
    )
    width["active_diff"] = get_metalization_via_width(
        pdk,
        "active_diff",
        top_via="mcon",
    )
    width["active_tap"] = get_metalization_via_width(
        pdk,
        "active_tap",
        bottom_via="mcon",
    )
    width["met1"] = get_metalization_via_width(
        pdk,
        "met1",
        bottom_via="mcon",
        top_via="via1",
    )
    width["met2"] = get_metalization_via_width(
        pdk,
        "met2",
        bottom_via="via1",
        top_via="via2",
    )
    width["met3"] = get_metalization_via_width(
        pdk,
        "met3",
        bottom_via="via2",
        top_via="via3",
    )
    width["met4"] = get_metalization_via_width(
        pdk,
        "met4",
        bottom_via="via3",
        top_via="via4",
    )
    width["met5"] = get_metalization_via_width(
        pdk,
        "met5",
        bottom_via="via4",
    )

    return width




@cell
def via(pdk: MappedPDK, bottom_glayer, via_glayer, top_glayer):
    widths = get_via_width(pdk)

    top_level = Component(name="via")

    for glayer in {bottom_glayer, via_glayer, top_glayer}:
        top_level << rectangle(
            size=(widths[glayer], widths[glayer]),
            layer=pdk.get_glayer(glayer),
            centered=True,
        )

    return top_level


sg13g2_mapped_pdk.activate()

module = "test_via"
module_path = Path(module)
module_gds = module_path / f"{module}.gds"

# comp = via(sg13g2_mapped_pdk, "met1", "via1", "met2")
# comp = via(sg13g2_mapped_pdk, "met2", "via2", "met3")
# comp = via(sg13g2_mapped_pdk, "met3", "via3", "met4")
comp = via(sg13g2_mapped_pdk, "met4", "via4", "met5")
comp.name = module
comp.show()

module_path.mkdir(parents=True, exist_ok=True)
module_gds.unlink(missing_ok=True)
comp.write_gds(module_gds)

print(get_via_width(sg13g2_mapped_pdk))
