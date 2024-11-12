from glayout.flow.pdk.mappedpdk import MappedPDK

grulesobj = dict()
for glayer in MappedPDK.valid_glayers:
    grulesobj[glayer] = dict((x, None) for x in MappedPDK.valid_glayers)


def add_layer_rule(grules: dict, layer1: str, rules: dict[str, dict]):
    """
    Add each rule on the grule map on both directions
    Throws error if the entry already exists.

    This functions mutates `grules`
    """
    valid_rules = {
        "min_separation",
        "min_enclosure",
        "min_width",
        "width",
        "min_area",
        "capmettop",
        "capmetbottom",
        "overhang",
    }

    for layer2, rule_dict in rules.items():
        if grules[layer2][layer1] is not None or grules[layer1][layer2] is not None:
            raise RuntimeError(f"Rule {layer1}/{layer2} is already registered")

        grules[layer1][layer2] = rule_dict

        for rule_name in rule_dict.keys():
            if rule_name not in valid_rules:
                raise RuntimeError(
                    f"Rule {rule_name} from {layer1}/{layer2} is not valid"
                )


# Section 4.2: Special Layer Configuration
# Derived layers
# - PWell               PWell.drawing OR not in NWell and not in PWell:block
# - nSD                 nSD.drawing   OR not in pSD   and not in nSD:block
# - nBuLay (dnwell)
# - N+Activ             Activ + nSD
# - P+Activ             Activ + pSD
# - nWell Tie           n+Activ Inside Nwell
# - Substrate Tie       p+Activ Inside PWell
# - Gate                Activ + GatPoly
# - NFET                GatPoly contained on Activ not in pSD
# - PFET                GatPoly over p+Activ contained inside NWell

# DNWell - NBuLay N Burried Layer
# Allows existence of isolated nmos
# NBL.a   1.00     Min. nBuLay width
# NBL.b   1.50     Min. nBuLay space or notch (same net)
# NBL.c   3.20     Min. PWell width between nBuLay regions (different net) (Note 1)
# NBL.d   2.20     Min. PWell width between nBuLay and NWell (different net) (Note 1)
# NBL.e   1.00     Min. nBuLay space to unrelated N+Activ
# NBL.f   0.50     Min. nBuLay space to unrelated P+Activ
add_layer_rule(
    grulesobj,
    "dnwell",
    {
        "dnwell": {
            "min_width": 1,  # NBL.a
        },
        "pwell": {},
        "nwell": {},
        "p+s/d": {},
        "n+s/d": {},
        "active_diff": {
            "min_enclosure": 1.0,  # NBL.e NBL.f
        },
        "active_tap": {
            "min_enclosure": 1.0,  # NBL.e NBL.f
            # "min_enclosure": 0.62,  # ?
            # "min_separation": 0.62,  # ?
        },
        "poly": {},
        "mcon": {},
        "met1": {},
        "via1": {},
        "met2": {},
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# PWell
add_layer_rule(
    grulesobj,
    "pwell",
    {
        "pwell": {
            # "min_width": 0.6,  # TODO
            # "min_separation": 1.4,  # TODO
        },
        "nwell": {
            # "min_separation": 1.80,  # NW.b1
            # "min_separation": 0.0  # TODO_
        },
        "p+s/d": {},
        "n+s/d": {},
        "active_diff": {
            "min_enclosure": 0.43  # TODO
        },
        "active_tap": {
            "min_enclosure": 0.12  # TODO
        },
        "poly": {},
        "mcon": {},
        "met1": {},
        "via1": {},
        "met2": {},
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)


# NWell (5.1)
# R NW.a    0.62    Min. NWell width
# R NW.b    0.62    Min. NWell space or notch (same net). NWell regions separated by less than this value will be merged.
# NW.b1   1.80    Min. PWell width between NWell regions (different net) (Note 3)
# R NW.c    0.31    Min. NWell enclosure of P+Activ not inside ThickGateOx
# R NW.c1   0.62    Min. NWell enclosure of P+Activ inside ThickGateOx
# R NW.d    0.31    Min. NWell space to external N+Activ not inside ThickGateOx
# R NW.d1   0.62    Min. NWell space to external N+Activ inside ThickGateOx
# R NW.e    0.24    Min. NWell enclosure of NWell tie surrounded entirely by NWell in N+Activ not inside ThickGateOx
# R NW.e1   0.62    Min. NWell enclosure of NWell tie surrounded entirely by NWell in N+Activ inside ThickGateOx
# R NW.f    0.24    Min. NWell space to substrate tie in P+Activ not inside ThickGateOx
# R NW.f1   0.62    Min. NWell space to substrate tie in P+Activ inside ThickGateOx
add_layer_rule(
    grulesobj,
    "nwell",
    {
        "nwell": {
            "min_width": 0.62,  # NW.a
            "min_separation": 0.62,  # NW.b
        },
        "p+s/d": {},
        "n+s/d": {},
        "active_diff": {
            "min_enclosure": 0.62,  # NW.c, NW.c1, NW.e, NW.e1. Don't understand anything
            "min_separation": 0.62,  # NW.d, NW.d1, NW.f, NW.f1. Don't understand anything
        },
        "active_tap": {
            "min_enclosure": 0.62,  # NW.c, NW.c1, NW.e, NW.e1. Don't understand anything
            "min_separation": 0.62,  # NW.d, NW.d1, NW.f, NW.f1. Don't understand anything
        },
        "poly": {},
        "mcon": {},
        "met1": {},
        "via1": {},
        "met2": {},
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)


# p+s/d (5.10) Region with P+ implants (Drain, Source, Resistos, Ties)
# R pSD.a    0.31   Min. pSD width
# R pSD.b    0.31   Min. pSD space or notch (Note 1)
# R pSD.k    0.25   Min. pSD area (µm²)

# pSD.c    0.18   Min. pSD enclosure of P+Activ in NWell
# pSD.c1   0.03   Min. pSD enclosure of P+Activ in PWell
# pSD.i    0.30   Min. pSD enclosure of PFET gate not inside ThickGateOx
# pSD.i1   0.40   Min. pSD enclosure of PFET gate inside ThickGateOx
# pSD.n    0.18   Min. pSD enclosure of p-type poly resistors

# pSD.d    0.18   Min. pSD space to unrelated N+Activ in PWell
# pSD.d1   0.03   Min. pSD space to N+Activ in NWell
# pSD.j    0.30   Min. pSD space to NFET gate not inside ThickGateOx
# pSD.j1   0.40   Min. pSD space to NFET gate inside ThickGateOx
# pSD.m    0.18   Min. pSD space to n-type poly resistors

# pSD.e    0.30   Min. pSD overlap of Activ at one position when forming abutted substrate tie (Note 2)
# pSD.f    0.30   Min. Activ extension over pSD at one position when forming abutted NWell tie (Note 2)
# pSD.g    0.09   Min. N+Activ or P+Activ area (µm²) when forming abutted tie (Note 2)
# pSD.l    0.25   Min. pSD enclosed area (µm²)
add_layer_rule(
    grulesobj,
    "p+s/d",
    {
        "p+s/d": {
            "min_width": 0.31,  # pSD.a
            "min_separation": 0.31,  # pSD.b
            "min_area": 0.25,  # pSD.k
        },
        "n+s/d": {},
        "active_diff": {
            "min_enclosure": 0.4  # pSD.i, pSD.i1
        },
        "active_tap": {
            "min_enclosure": 0.16  # TODO
        },
        "poly": {},
        "mcon": {},
        "met1": {},
        "via1": {},
        "met2": {},
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# n+s/d
add_layer_rule(
    grulesobj,
    "n+s/d",
    {
        "n+s/d": {
            "min_width": 0.4,  # TODO
            "min_separation": 0.4,  # TODO
        },
        "active_diff": {
            "min_enclosure": 0.23  # TODO
        },
        "active_tap": {
            "min_enclosure": 0.16  # TODO
        },
        "poly": {},
        "mcon": {},
        "met1": {},
        "via1": {},
        "met2": {},
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# Active Diff (5.5)
# R Act.a  0.15   Min. Activ width
# R Act.b  0.21   Min. Activ space or notch
# Act.c  0.23   Min. Activ drain/source extension
# R Act.d  0.122  Min. Activ area (µm²)
# Act.e  0.15   Min. Activ enclosed area (µm²)

add_layer_rule(
    grulesobj,
    "active_diff",
    {
        "active_diff": {
            "min_width": 0.35,  # Act.a, This is the size when enclosing contacts
            "min_separation": 0.21,  # Act.b
            "min_area": 0.1225,  # Act.d adjusted to a precise root
        },
        "active_tap": {
            "min_separation": 0.21,  # Act.b
        },
        "poly": {
            "overhang": 0.23,  # Act.c ?
            # "overhang": 0.40,  # Act.c ? pSD.i, pSD.i1
            "min_separation": 0.1,  # TODO
        },
        "mcon": {
            "min_enclosure": 0.07  # Cnt.c
        },
        "met1": {},
        "via1": {},
        "met2": {},
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# Active Tap (5.5)

add_layer_rule(
    grulesobj,
    "active_tap",
    {
        "active_tap": grulesobj["active_diff"]["active_diff"],
        "poly": grulesobj["active_diff"]["poly"],
        "mcon": grulesobj["active_diff"]["mcon"],
        "met1": {},
        "via1": {},
        "met2": {},
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# Poly (5.8)
# R Gat.a   0.13   Min. GatPoly width
# Gat.a1  0.13   Min. GatPoly width for channel length of 1.2 V NFET
# Gat.a2  0.13   Min. GatPoly width for channel length of 1.2 V PFET
# Gat.a3  0.45   Min. GatPoly width for channel length of 3.3 V NFET
# Gat.a4  0.4    Min. GatPoly width for channel length of 3.3 V PFET
# R Gat.b   0.18   Min. GatPoly space or notch
# Gat.b1  0.25   Min. space between unrelated 3.3 V GatPoly over Activ regions
# Gat.c   0.18   Min. GatPoly extension over Activ (end cap)
# Gat.d   0.07   Min. GatPoly space to Activ
# R Gat.e   0.09   Min. GatPoly area (µm²)
# O Gat.f          45-degree and 90-degree angles for GatPoly on Activ area are not allowed
# O Gat.g   0.16   Min. GatPoly width for 45-degree bent shapes if the bend GatPoly length is > 0.39 µm

add_layer_rule(
    grulesobj,
    "poly",
    {
        "poly": {
            "min_width": 0.13,  # Gat.a,
            "min_separation": 0.18,  # Gat.b
            "min_area": 0.09,  # Gat.e
        },
        "mcon": {
            "min_enclosure": 0.07,  # Cnt.d
            "min_separation": 0.17,  # TODO
        },
        "met1": {},
        "via1": {},
        "met2": {},
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# Mcon (5.14)
# R Cnt.a   0.16    Min. and max. Cont width
# R Cnt.b   0.18    Min. Cont space
# R Cnt.b1  0.20    Min. Cont space in a contact array of more than 4 rows and more then 4 columns (Note 1)
# Cnt.c   0.07    Min. Activ enclosure of Cont
# Cnt.d   0.07    Min. GatPoly enclosure of Cont
# Cnt.e   0.14    Min. Cont on GatPoly space to Activ
# Cnt.f   0.11    Min. Cont on Activ space to GatPoly
# Cnt.g           Cont must be within Activ or GatPoly
# Cnt.g1  0.09    Min. pSD space to Cont on nSD-Activ
# Cnt.g2  0.09    Min. pSD overlap of Cont on pSD-Activ
# R Cnt.h           Cont must be covered with Metal1
# Cnt.j           Cont on GatPoly over Activ is not allowed
add_layer_rule(
    grulesobj,
    "mcon",
    {
        "mcon": {
            "width": 0.16,  # Cnt.a
            "min_separation": 0.20,  # Cnt.b, Cnt.b1. Selected bigger spacing
        },
        "met1": {
            "min_enclosure": 0.05  # Cnt.h, M1.c, M1.c1 always handle endcap
        },
        "via1": {},
        "met2": {},
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# Met1 (5.16)
# R M1.a    0.16   Min. Metal1 width
# R M1.b    0.18   Min. Metal1 space or notch
# R M1.c    0.00   Min. Metal1 enclosure of Cont
# R M1.c1   0.05   Min. Metal1 endcap enclosure of Cont (Note 1)
# R M1.d    0.09   Min. Metal1 area (µm²)
# M1.e    0.22   Min. space of Metal1 lines if, at least one line is wider than 0.3 µm and the parallel run is more than 1.0 µm
# M1.f    0.60   Min. space of Metal1 lines if, at least one line is wider than 10.0 µm and the parallel run is more than 10.0 µm
# O M1.g    0.20   Min. 45-degree bent Metal1 width if the bent metal length is > 0.5 µm
# O M1.i    0.22   Min. space of Metal1 lines of which at least one is bent by 45-degree
# O M1.j    35.0   Min. global Metal1 density [%]
# O M1.k    60.0   Max. global Metal1 density [%]
add_layer_rule(
    grulesobj,
    "met1",
    {
        "met1": {
            "min_width": 0.16,  # M1.a
            "min_separation": 0.18,  # M1.b
            "min_area": 0.09,  # M1.d
        },
        "via1": {
            "min_enclosure": 0.05  # V1.c, V1.c1
        },
        "met2": {},
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# Via1 (5.19)
# R V1.a   0.19   Min. and max. Via1 width
# R V1.b   0.22   Min. Via1 space
# R V1.b1  0.29   Min. Via1 space in an array of more than 3 rows and more then 3 columns (Note 1)
# R V1.c   0.01   Min. Metal1 enclosure of Via1
# R V1.c1  0.05   Min. Metal1 endcap enclosure of Via1 (Note 2)
add_layer_rule(
    grulesobj,
    "via1",
    {
        "via1": {
            "width": 0.19,  # V1.a
            "min_separation": 0.29,  # V1.b, V1.b1
        },
        "met2": {
            "min_enclosure": 0.05  # Mn.c, Mn.c1 always handle endcap
        },
        "via2": {},
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)
# TODO: what's endcap?

# Met2 (5.17) Met2-5
# R Mn.a     0.20      Min. Metal(n) width
# R Mn.b     0.21      Min. Metal(n) space or notch
# R Mn.c     0.005     Min. Metal(n) enclosure of Via(n-1)
# R Mn.c1    0.05      Min. Metal(n) endcap enclosure of Via(n-1) (Note 1)
# R Mn.d     0.144     Min. Metal(n) area (µm²)
# Mn.e     0.24      Min. space of Metal(n) lines if, at least one line is wider than 0.39 µm and the parallel run is more than 1.0 µm
# Mn.f     0.60      Min. space of Metal(n) lines if, at least one line is wider than 10.0 µm and the parallel run is more than 10.0 µm
# O Mn.g     0.24      Min. 45-degree bent Metal(n) width if the bent metal length is > 0.5 µm
# O Mn.i     0.24      Min. space of Metal(n) lines of which at least one is bent by 45-degree
# O Mn.j     35.00     Min. global Metal(n) density [%]
# O Mn.k     60.00     Max. global Metal(n) density [%]
add_layer_rule(
    grulesobj,
    "met2",
    {
        "met2": {
            "min_width": 0.20,  # Mn.a
            "min_separation": 0.21,  # Mn.a
            "min_area": 0.1444,  # Mn.d, added extra 0.0004 to avoid sqrt errors
        },
        "via2": {
            "min_enclosure": 0.05  # Vn.c, Vn.c1 always handle endcap
        },
        "met3": {},
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# Via2 (5.20) Via2-Via4
# R Vn.a   0.19   Min. and max. Via(n) width
# R Vn.b   0.22   Min. Via(n) space
# R Vn.b1  0.29   Min. Via(n) space in an array of more than 3 rows and more then 3 columns (Note 1)
# R Vn.c   0.005  Min. Metal(n) enclosure of Via(n)
# R Vn.c1  0.05   Min. Metal(n) endcap enclosure of Via(n) (Note 2)
add_layer_rule(
    grulesobj,
    "via2",
    {
        "via2": {
            "width": 0.19,  # Vn.a
            "min_separation": 0.29,  # Vn.b, Vn.b1
        },
        "met3": grulesobj["via1"]["met2"],
        "via3": {},
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# Met3 (5.17)
add_layer_rule(
    grulesobj,
    "met3",
    {
        "met3": grulesobj["met2"]["met2"],
        "via3": grulesobj["met2"]["via2"],
        "met4": {},
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# Via3 (5.20)
add_layer_rule(
    grulesobj,
    "via3",
    {
        "via3": grulesobj["via2"]["via2"],
        "met4": grulesobj["via1"]["met2"],
        "via4": {},
        "met5": {},
        "capmet": {},
    },
)

# Met4 (5.17)
add_layer_rule(
    grulesobj,
    "met4",
    {
        "met4": grulesobj["met2"]["met2"],
        "via4": grulesobj["met2"]["via2"],
        "met5": {},
        "capmet": {},
    },
)

# Via4 (5.20)
add_layer_rule(
    grulesobj,
    "via4",
    {
        "via4": grulesobj["via2"]["via2"],
        "met5": grulesobj["via1"]["met2"],
        "capmet": {},
    },
)

# Met5 (5.17)
add_layer_rule(
    grulesobj,
    "met5",
    {
        "met5": grulesobj["met2"]["met2"],
        "capmet": {},
    },
)


# Capmet (6.11)
add_layer_rule(
    grulesobj,
    "capmet",
    {
        "capmet": {
            "capmettop": (42, 0),  # TODO
            "capmetbottom": (36, 0),  # TODO
            "min_separation": 1.2,  # TODO
        },
    },
)


# min_separation
# min_enclosure   Between 2 layers
# min_width       Self rule (mostly)
# width (via)     Self rule

# To greatly simplify the rule graph, context dependent rules (sometimes referred to as lambda rules) are eliminated by taking the worst case value for each rule.
# This allows the designer to lookup rules without providing any additional context of surrounding layer geometry (usually required for dependent rules).

# Rule Lookup: Get rule information
#  MappedPDK.get_grule(“metal 2”, “via 1”)
