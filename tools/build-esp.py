#!/usr/bin/env python3
r"""Author "Jarl Ulfric Armor Replacer.esp" by lifting Ulfric's armour out of NordwarUA's
Guards Armor Replacer SSE (Nexus 22671) and nothing else.

WHY A GENERATOR RATHER THAN A COPIED PLUGIN
    The records are NordwarUA's. Rebuilding them from his archive at build time means this repo
    carries no copy of his plugin, the extraction is reviewable in a diff, and anyone can run it
    against the same download and get the same bytes.

WHAT IT TAKES, AND WHAT IT DELIBERATELY LEAVES BEHIND
    Traced from Ulfric's three NPC records outward: NPC_ -> DOFT -> OTFT -> ARMO -> ARMA.

    Taken:
        ARMO 06004456 UlfricEbonyHelmet    + ARMA 06004452/53/54/55  (four race variants)
        ARMO 0600444F UlfricEbonyCuirass   + ARMA 0600444E
        ARMO 06004451 UlfricEbonyGauntlets + ARMA 06004450
        ARMO 0600444D UlfricEbonyBoots     + ARMA 0600444C
        OTFT 00045C33 UlfricOutfit         (override - what he wears)
        OTFT 00101AF2 UlfricPrisonerOutfit (override - what he wears in Helgen)

    NOT taken - and this is the point of the exercise:
        * Ulfric's three NPC_ records. Guards Armor Replacer overrides them, but every one carries
          the SAME default outfit as vanilla, so they are not what puts the armour on him - the two
          outfits are. Leaving them out means this mod does not fight face, AI or appearance mods,
          which is the worst class of conflict an armour replacer can pick.
        * Every other hold's guards, the Solitude elite set, weapons, shields, and the rest of the
          1,382 files in that archive.

    Everything the taken records reference outside themselves is in Skyrim.esm - races, keywords,
    armour ratings - so this plugin declares exactly one master.

FORMIDS
    Guards Armor Replacer has six masters, so its own records sit at index 06. This plugin has one,
    so ours sit at index 01. Each lifted record is renumbered into 0x01000800+ and the references
    BETWEEN them (an ARMO's MODL pointing at its ARMA, an outfit's INAM pointing at an ARMO) are
    rewritten to match. References to Skyrim.esm are left exactly as they are.

Usage:  python build-esp.py <Guards_Armor_Replacer.esp> [out.esp]
"""
import os
import struct
import sys

AUTHOR = "ApocryphaRealm"
DESCRIPTION = "Ulfric's armour from NordwarUA's Guards Armor Replacer, on its own"
FORM_VERSION = 44  # SSE

# The records to lift, in the order they are renumbered. ARMA before the ARMO that points at it
# is not required, but it keeps the plugin readable in xEdit.
LIFT = [
    (0x0600444C, "ARMA", "UlfricEbonyBoots_1"),
    (0x0600444D, "ARMO", "UlfricEbonyBoots"),
    (0x0600444E, "ARMA", "UlfricEbonyCuirass_1"),
    (0x0600444F, "ARMO", "UlfricEbonyCuirass"),
    (0x06004450, "ARMA", "UlfricEbonyGauntlets_1"),
    (0x06004451, "ARMO", "UlfricEbonyGauntlets"),
    (0x06004452, "ARMA", "UlfricEbonyHelmet_M"),
    (0x06004453, "ARMA", "UlfricEbonyHelmet_A"),
    (0x06004454, "ARMA", "UlfricEbonyHelmet_O"),
    (0x06004455, "ARMA", "UlfricEbonyHelmet_K"),
    (0x06004456, "ARMO", "UlfricEbonyHelmet"),
]

# Skyrim.esm outfits, overridden so they hand out the armour above. FormIDs stay as they are.
OUTFITS = [0x00045C33, 0x00101AF2]

# Subrecords whose payload is a FormID (or an array of them) and therefore needs remapping.
REMAP_IN = {b"MODL", b"INAM"}


def read_records(data):
    """Walk the plugin, yielding (tag, formid, flags, body) for every record."""
    off, end = 0, len(data)
    while off + 24 <= end:
        tag = data[off:off + 4]
        size = struct.unpack_from("<I", data, off + 4)[0]
        if tag == b"GRUP":
            off += 24
            continue
        flags = struct.unpack_from("<I", data, off + 8)[0]
        formid = struct.unpack_from("<I", data, off + 12)[0]
        yield tag, formid, flags, data[off + 24:off + 24 + size]
        off += 24 + size


def fields(body):
    off, end = 0, len(body)
    override = None
    while off + 6 <= end:
        tag = body[off:off + 4]
        size = struct.unpack_from("<H", body, off + 4)[0]
        off += 6
        if tag == b"XXXX":
            override = struct.unpack_from("<I", body, off)[0]
            off += size
            continue
        if override is not None:
            size, override = override, None
        yield tag, body[off:off + size]
        off += size


def sub(tag, data):
    return tag + struct.pack("<H", len(data)) + data


def record(tag, formid, body, flags=0):
    return (tag + struct.pack("<I", len(body)) + struct.pack("<I", flags) +
            struct.pack("<I", formid) + struct.pack("<I", 0) +
            struct.pack("<H", FORM_VERSION) + struct.pack("<H", 0) + body)


def remap_body(body, mapping):
    """Rebuild a record body, rewriting FormIDs only inside subrecords that hold them."""
    out = b""
    for tag, data in fields(body):
        if tag in REMAP_IN and len(data) % 4 == 0 and data:
            ids = [struct.unpack_from("<I", data, i)[0] for i in range(0, len(data), 4)]
            data = b"".join(struct.pack("<I", mapping.get(i, i)) for i in ids)
        out += sub(tag, data)
    return out


def group(tag, records_bytes):
    return (b"GRUP" + struct.pack("<I", len(records_bytes) + 24) + tag +
            struct.pack("<I", 0) + struct.pack("<I", 0) + struct.pack("<I", 0) + records_bytes)


# Skyrim allows 254 full plugins and 4,096 light ones. The owner, 2026-09-16: "we need to make sure
# to ship any of our mods that have a plugin as an esl not an esp", and "which goes for past mods as
# well". Every new record here sits between 0x000800 and 0x000FFF, which is the light range, so the
# flag is all it takes.
ESL_FLAG = 0x00000200


def tes4_header(record_count, next_object_id):
    body = (sub(b"HEDR", struct.pack("<fiI", 1.7, record_count, next_object_id)) +
            sub(b"CNAM", AUTHOR.encode("cp1252") + b"\x00") +
            sub(b"SNAM", DESCRIPTION.encode("cp1252") + b"\x00") +
            sub(b"MAST", b"Skyrim.esm\x00") +
            sub(b"DATA", struct.pack("<Q", 0)))
    return record(b"TES4", 0, body, flags=ESL_FLAG)


def main(source, out_path):
    data = open(source, "rb").read()

    mapping = {old: 0x01000800 + i for i, (old, _, _) in enumerate(LIFT)}
    wanted = set(mapping) | set(OUTFITS)

    found = {}
    for tag, formid, flags, body in read_records(data):
        if formid in wanted and tag in (b"ARMO", b"ARMA", b"OTFT"):
            if flags & 0x00040000:
                raise SystemExit("record %08X is compressed; this builder does not expect that" % formid)
            found[formid] = (tag, body)

    missing = [("%08X" % f) for f in wanted if f not in found]
    if missing:
        raise SystemExit("not found in %s: %s" % (os.path.basename(source), ", ".join(missing)))

    armo, arma, otft = b"", b"", b""
    for old, kind, edid in LIFT:
        tag, body = found[old]
        if tag.decode() != kind:
            raise SystemExit("%08X is a %s, expected %s" % (old, tag.decode(), kind))
        built = record(tag, mapping[old], remap_body(body, mapping))
        if kind == "ARMO":
            armo += built
        else:
            arma += built

    for fid in OUTFITS:
        tag, body = found[fid]
        otft += record(tag, fid, remap_body(body, mapping))

    count = len(LIFT) + len(OUTFITS)
    blob = (tes4_header(count, (max(mapping.values()) & 0xFFFFFF) + 1) +
            group(b"ARMO", armo) + group(b"ARMA", arma) + group(b"OTFT", otft))

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(blob)

    print("wrote %s (%d bytes, %d records)" % (out_path, len(blob), count))
    for old, kind, edid in LIFT:
        print("  %s %08X -> %08X  %s" % (kind, old, mapping[old], edid))
    for fid in OUTFITS:
        print("  OTFT %08X (override, unchanged id)" % fid)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    here = os.path.dirname(os.path.abspath(__file__))
    default = os.path.normpath(os.path.join(here, "..", "dist", "Jarl Ulfric Armor Replacer.esp"))
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else default)
