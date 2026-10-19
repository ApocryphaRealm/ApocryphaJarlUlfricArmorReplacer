#!/usr/bin/env python3
r"""Add the re-dress quest to "Jarl Ulfric Armor Replacer.esp" (run after build-esp.py).

WHY
    The plugin overrides Ulfric's two outfit records. A new game reads them, so he wears the new
    armour; a save that already dressed him keeps his old clothes in his inventory and never reads the
    outfit again (FootConnoisseur's report, 2026-10-14; reproduced 2026-10-18). This adds ONE start-game-
    enabled quest carrying the script JUARRedressUlfric (tools/JUARRedressUlfric.psc, compiled to
    Scripts/JUARRedressUlfric.pex), which dresses him on such a save once he is loaded.

WHAT IT CHANGES
    * adds QUST 01000900 JUAR_RedressUlfric in its own top group, with the script and its seven properties;
    * HEDR record count + 1 and next object id above the new record.
    Every other byte of the plugin is left as it was. Refuses a plugin that already has the quest.

Usage:  python add-redress-quest.py <plugin.esp> [out.esp]     (out defaults to rewriting the input)
"""
import struct
import sys

FORM_VERSION = 44
QUEST_ID = 0x01000900
EDID = b"JUAR_RedressUlfric\x00"
SCRIPT = b"JUARRedressUlfric"

# property name -> FormID (every one lives in Skyrim.esm, master index 00, or in this plugin, index 01)
PROPS = [
    (b"UlfricRef", 0x0001B131),               # ACHR Ulfric Stormcloak, Palace of the Kings
    (b"ReplacerCuirass", 0x01000803),         # ARMO UlfricEbonyCuirass (this plugin)
    (b"VanillaClothes", 0x00062303),          # ARMO ClothesUlfric
    (b"VanillaCuffs", 0x00103941),            # ARMO PrisonerCuffs
    (b"UlfricOutfit", 0x00045C33),            # OTFT
    (b"UlfricPrisonerOutfit", 0x00101AF2),    # OTFT
]
FLOAT_PROPS = [(b"PollSeconds", 10.0)]
INT_PROPS = [(b"MaxAttempts", 6)]


def sub(tag, data):
    return tag + struct.pack("<H", len(data)) + data


def wstr(s):
    return struct.pack("<H", len(s)) + s


def vmad():
    """v5 / object-format-2, one script. Property types: 1 object, 2 string, 3 int32, 4 float, 5 bool."""
    n = len(PROPS) + len(FLOAT_PROPS) + len(INT_PROPS)
    b = struct.pack("<hhH", 5, 2, 1) + wstr(SCRIPT) + struct.pack("<BH", 0, n)
    for name, fid in PROPS:
        b += wstr(name) + struct.pack("<BB", 1, 1) + struct.pack("<HhI", 0, -1, fid)
    for name, v in FLOAT_PROPS:
        b += wstr(name) + struct.pack("<BB", 4, 1) + struct.pack("<f", v)
    for name, v in INT_PROPS:
        b += wstr(name) + struct.pack("<BB", 3, 1) + struct.pack("<i", v)
    return b


def quest_record():
    body = (sub(b"EDID", EDID) + sub(b"VMAD", vmad()) +
            # flags 0x0111: start game enabled (+ the CK's usual run-once/allow-repeat bits, as in shipped quests)
            sub(b"DNAM", struct.pack("<HBBIi", 0x0111, 0x46, 0xFF, 0, 0)) +
            sub(b"NEXT", b"") + sub(b"ANAM", struct.pack("<I", 0)))
    return (b"QUST" + struct.pack("<II", len(body), 0) + struct.pack("<I", QUEST_ID) +
            struct.pack("<I", 0) + struct.pack("<HH", FORM_VERSION, 0) + body)


def main(src, dst):
    data = bytearray(open(src, "rb").read())
    if data[:4] != b"TES4":
        raise SystemExit("not a plugin")
    if b"QUST" in bytes(data):
        raise SystemExit("this plugin already has a QUST - refusing to add a second")
    size = struct.unpack_from("<I", data, 4)[0]
    hdr_end = 24 + size
    # HEDR is the first subrecord of TES4: tag(4) len(2) version(f) numRecords(i) nextObjectId(I)
    if data[24:28] != b"HEDR":
        raise SystemExit("HEDR is not the first subrecord")
    ver, count, nxt = struct.unpack_from("<fiI", data, 30)
    struct.pack_into("<fiI", data, 30, ver, count + 1, max(nxt, (QUEST_ID & 0xFFFFFF) + 1))
    rec = quest_record()
    grp = (b"GRUP" + struct.pack("<I", len(rec) + 24) + b"QUST" + struct.pack("<III", 0, 0, 0) + rec)
    out = bytes(data) + grp
    open(dst, "wb").write(out)
    print("wrote %s: +1 record (QUST %08X %s), %d bytes" % (dst, QUEST_ID, EDID[:-1].decode(), len(out)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
