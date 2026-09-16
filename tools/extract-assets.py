#!/usr/bin/env python3
r"""Pull Ulfric's meshes and textures out of NordwarUA's Guards Armor Replacer archive.

The companion to build-esp.py, and it exists for the same reason: this repository deliberately
carries NONE of NordwarUA's files. The plugin is generated from his archive and so are the assets,
so the whole package can be rebuilt by anyone holding the same download, and nothing of his is
redistributed through this repo.

WHAT IT TAKES
    25 meshes - the Stormlord set (cuirass, gauntlets, boots, helmet and their ground models) plus
                the first-person armour, each in both weight variants. The plugin names only the
                "_1" files; Skyrim derives "_0" from them, so both must travel.
    15 textures - exactly the ones those meshes name, read out of the NIFs rather than guessed.

    Two further textures the meshes reference are NOT taken, because they are vanilla and shipping
    them would be redistributing Bethesda's files for no reason:
        textures\cubemaps\chitin_e_ebony.dds
        textures\cubemaps\quickskydark_e.dds
    Both were confirmed present in Skyrim - Textures3.bsa.

    CASE MATTERS. 7-Zip matches names case-sensitively, and this archive is inconsistent -
    "Torso1.dds", "Black_cloak.dds", "helmetE.dds", "GauntletsOficer_n.dds". A first attempt using
    lowercase names extracted nothing at all and said nothing about it. The exact spellings are
    listed below for that reason; do not "tidy" them.

Usage:  python extract-assets.py <Guards Armor Replacer-22671-5-5a-....7z> [dist folder]
"""
import os
import shutil
import subprocess
import sys

MESH_DIR = r"Meshes\1_Soldier_Replacer\Guards\ElitArmor\Armor"
TEX_DIR = r"Textures\1_Soldier_Replacer\Guards"

MESH_PATTERNS = ["Stormlord*", "1stUArmor*"]

# Exact spellings as the archive stores them.
TEXTURES = [
    "Black_cloak.dds", "Black_cloak_n.dds",
    "boots1.dds", "boots1_m.dds", "boots_n.dds",
    "gauntlets1.dds", "gauntlets1_m.dds", "GauntletsOficer_n.dds",
    "helmet_n.dds", "helmetE.dds", "helmetE_m.dds",
    "Torso1.dds", "Torso1_m.dds", "Torso1_n.dds", "Torso_m.dds",
]

SEVENZIP = [
    r"C:\Program Files\7-Zip\7z.exe",
    r"C:\Program Files (x86)\7-Zip\7z.exe",
    "7z",
]


def seven_zip():
    for c in SEVENZIP:
        if c == "7z" or os.path.isfile(c):
            return c
    raise SystemExit("7-Zip not found; install it or add 7z to PATH")


def main(archive, dist):
    if not os.path.isfile(archive):
        raise SystemExit("no such archive: %s" % archive)
    exe = seven_zip()

    for sub in ("Meshes", "Textures"):
        p = os.path.join(dist, sub)
        if os.path.isdir(p):
            shutil.rmtree(p)

    args = [exe, "x", archive, "-o" + dist, "-y"]
    for pat in MESH_PATTERNS:
        args.append(os.path.join(MESH_DIR, pat))
    for t in TEXTURES:
        args.append(os.path.join(TEX_DIR, t))

    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("7-Zip failed (%d):\n%s" % (r.returncode, r.stdout[-2000:]))

    meshes = os.path.join(dist, MESH_DIR)
    texs = os.path.join(dist, TEX_DIR)
    got_m = sorted(os.listdir(meshes)) if os.path.isdir(meshes) else []
    got_t = sorted(os.listdir(texs)) if os.path.isdir(texs) else []

    print("meshes:   %d" % len(got_m))
    print("textures: %d" % len(got_t))

    # Extracting nothing must be loud, not silent - that is exactly how the case-sensitivity trap
    # cost a build.
    missing = [t for t in TEXTURES if t not in got_t]
    if missing:
        raise SystemExit("MISSING %d texture(s) - check the spelling against the archive: %s"
                         % (len(missing), ", ".join(missing)))
    if len(got_m) < 20:
        raise SystemExit("only %d meshes came out; expected the whole Stormlord set" % len(got_m))
    print("all expected files extracted")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    here = os.path.dirname(os.path.abspath(__file__))
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.normpath(os.path.join(here, "..", "dist")))
